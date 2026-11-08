from datetime import date

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django_tenants.utils import get_public_schema_name, schema_context
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .. import abonnements, calculs
from ..comptes import supprimer_compte
from ..models import Depense, Document, Entretien, Plein, Rappel, ReleveKilometrique, Vehicule
from . import serializers as S
from .base import (ROLE_PARTICULIER, LimiteConnexion, SchemaParticuliersMixin, schema_particuliers,
                   servir_fichier)


# ==================================================================
# COMPTES
# ==================================================================
def _reponse_connexion(user, statut=status.HTTP_200_OK):
    from .base import noter_activite
    noter_activite(user)
    token, _c = Token.objects.get_or_create(user=user)
    with schema_context(schema_particuliers()):     # préférences (langue) : schéma des particuliers
        utilisateur = S.UtilisateurSerializer(user).data
    return Response({"token": token.key, "utilisateur": utilisateur}, status=statut)


class InscriptionView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [LimiteConnexion]

    def post(self, request):
        from societe.models import Societe
        from utilisateurs.models import Utilisateur
        ser = S.InscriptionSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        with schema_context(get_public_schema_name()):
            try:
                societe = Societe.objects.get(schema_name=schema_particuliers())
            except Societe.DoesNotExist:
                return Response({"detail": _("Espace particuliers non configuré.")}, status=503)
            with transaction.atomic():
                user = Utilisateur.objects.create_user(
                    email=d["email"], password=d["password"], nom=d["nom"], prenom=d["prenom"],
                    role=ROLE_PARTICULIER, societe=societe, schema_name=societe.schema_name, is_staff=False,
                )
                with schema_context(schema_particuliers()):
                    from ..models import PreferencesParticulier
                    from ..models import unites_par_defaut
                    pays = d.get("pays") or "BE"
                    distance, volume = unites_par_defaut(pays)
                    PreferencesParticulier.objects.create(
                        utilisateur=user, langue=d.get("langue") or "fr", pays_defaut=pays,
                        unite_distance=d.get("unite_distance") or distance, unite_volume=d.get("unite_volume") or volume)
            return _reponse_connexion(user, status.HTTP_201_CREATED)


class ConnexionView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [LimiteConnexion]

    def post(self, request):
        from utilisateurs.models import Utilisateur
        email = (request.data.get("email") or "").strip().lower()
        password = request.data.get("password") or ""
        erreur = Response({"detail": _("Email ou mot de passe incorrect.")}, status=status.HTTP_400_BAD_REQUEST)
        with schema_context(get_public_schema_name()):
            user = Utilisateur.objects.filter(email__iexact=email).select_related("societe").first()
            if user is None or not user.is_active or not user.check_password(password):
                return erreur
            if user.role != ROLE_PARTICULIER:
                return Response({"detail": _("Ce compte est un compte professionnel : connectez-vous sur le site web.")},
                                status=status.HTTP_403_FORBIDDEN)
            return _reponse_connexion(user)


class DeconnexionView(SchemaParticuliersMixin, APIView):
    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MoiView(SchemaParticuliersMixin, APIView):
    def get(self, request):
        return Response({**S.UtilisateurSerializer(request.user).data, "abonnement": abonnements.etat(request.user)})

    def patch(self, request):
        ser = S.UtilisateurSerializer(request.user, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    def delete(self, request):
        """Suppression du compte et de toutes ses données (exigence App Store / RGPD)."""
        user = request.user
        if not user.check_password(request.data.get("password") or ""):
            return Response({"detail": _("Mot de passe incorrect.")}, status=status.HTTP_400_BAD_REQUEST)
        supprimer_compte(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MotDePasseView(SchemaParticuliersMixin, APIView):
    """Changement du mot de passe : les autres appareils sont déconnectés, un nouveau jeton est renvoyé."""

    def post(self, request):
        ser = S.MotDePasseSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        user = request.user
        user.set_password(ser.validated_data["nouveau"])
        user.save(update_fields=["password", "updated_at"])
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return Response({"token": token.key})


class EmailView(SchemaParticuliersMixin, APIView):
    """Changement de l'adresse email (confirmé par le mot de passe)."""

    def post(self, request):
        ser = S.EmailSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        user = request.user
        user.email = ser.validated_data["email"]
        user.save(update_fields=["email", "updated_at"])
        return Response(S.UtilisateurSerializer(user).data)


# ==================================================================
# DONNÉES
# ==================================================================
class ProprietaireViewSet(SchemaParticuliersMixin, viewsets.ModelViewSet):
    """Filtre systématique : seules les données des véhicules de l'utilisateur."""
    model = None

    def get_queryset(self):
        qs = self.model.objects.filter(vehicule__proprietaire=self.request.user).select_related("vehicule")
        vehicule = self.request.query_params.get("vehicule")
        if vehicule:
            qs = qs.filter(vehicule_id=vehicule)
        return qs

    def _fichier(self, champ):
        return servir_fichier(getattr(self.get_object(), champ))


class LimiteFormule(APIException):
    """403 avec le détail de la formule : l'application propose alors une formule supérieure."""
    status_code = status.HTTP_403_FORBIDDEN
    default_code = "limite_formule"

    def __init__(self, erreur):
        super().__init__()
        self.detail = {"detail": erreur.message, "code": "limite_formule", "formule": erreur.formule,
                       "limite": erreur.limite, "vehicules_actifs": erreur.actifs, "formule_suivante": erreur.suivante}


def _verrouiller(user):
    """Sérialise les ajouts d'un même compte (deux ajouts simultanés ne dépassent pas la limite)."""
    from ..models import AbonnementParticulier
    AbonnementParticulier.objects.get_or_create(utilisateur=user)
    AbonnementParticulier.objects.select_for_update().get(utilisateur=user)


def _controler_limite(user, sauf=None):
    try:
        abonnements.verifier_limite(user, sauf=sauf)
    except abonnements.LimiteAtteinte as e:
        raise LimiteFormule(e)


class VehiculeViewSet(SchemaParticuliersMixin, viewsets.ModelViewSet):
    serializer_class = S.VehiculeSerializer

    def get_queryset(self):
        qs = Vehicule.objects.filter(proprietaire=self.request.user)
        # La liste masque les véhicules archivés (sauf ?archives=1) ; la fiche reste accessible (désarchiver)
        if self.action == "list" and self.request.query_params.get("archives") != "1":
            qs = qs.filter(archive=False)
        return qs

    def perform_create(self, serializer):
        with transaction.atomic():
            _verrouiller(self.request.user)
            if not serializer.validated_data.get("archive"):
                _controler_limite(self.request.user)
            serializer.save(proprietaire=self.request.user)

    def perform_update(self, serializer):
        """Désarchiver un véhicule compte dans la limite de la formule."""
        instance = serializer.instance
        with transaction.atomic():
            _verrouiller(self.request.user)
            if instance.archive and serializer.validated_data.get("archive") is False:
                _controler_limite(self.request.user, sauf=instance)
            serializer.save()

    @action(detail=True)
    def synthese(self, request, pk=None):
        return Response(calculs.synthese(self.get_object()))

    @action(detail=True)
    def consommation(self, request, pk=None):
        return Response(calculs.consommation(self.get_object()))

    @action(detail=True)
    def photo(self, request, pk=None):
        return servir_fichier(self.get_object().photo)


class ReleveViewSet(ProprietaireViewSet):
    model = ReleveKilometrique
    serializer_class = S.ReleveSerializer


class PleinViewSet(ProprietaireViewSet):
    """Pleins de carburant (les recharges électriques sont à part : RechargeViewSet)."""
    model = Plein
    serializer_class = S.PleinSerializer

    def get_queryset(self):
        return super().get_queryset().exclude(carburant="electricite")

    @action(detail=True)
    def ticket(self, request, pk=None):
        return self._fichier("ticket")


class RechargeViewSet(PleinViewSet):
    """Recharges électriques (kWh)."""
    serializer_class = S.RechargeSerializer

    def get_queryset(self):
        return ProprietaireViewSet.get_queryset(self).filter(carburant="electricite")

    def perform_create(self, serializer):
        serializer.save(carburant="electricite")


class EntretienViewSet(ProprietaireViewSet):
    model = Entretien
    serializer_class = S.EntretienSerializer

    def perform_create(self, serializer):
        entretien = serializer.save()
        calculs.avancer_rappels_entretien(entretien)

    @action(detail=True)
    def facture(self, request, pk=None):
        return self._fichier("facture")


class DocumentViewSet(ProprietaireViewSet):
    model = Document
    serializer_class = S.DocumentSerializer

    def perform_create(self, serializer):
        calculs.synchroniser_rappel_document(serializer.save())

    def perform_update(self, serializer):
        calculs.synchroniser_rappel_document(serializer.save())

    @action(detail=True)
    def fichier(self, request, pk=None):
        return self._fichier("fichier")


class RappelViewSet(ProprietaireViewSet):
    model = Rappel
    serializer_class = S.RappelSerializer

    @action(detail=True, methods=["post"])
    def fait(self, request, pk=None):
        rappel = self.get_object()
        jour = request.data.get("date")
        km = request.data.get("kilometrage")
        calculs.marquer_fait(rappel, date.fromisoformat(jour) if jour else None, int(km) if km not in (None, "") else None)
        return Response(self.get_serializer(rappel).data)


class DepenseViewSet(ProprietaireViewSet):
    model = Depense
    serializer_class = S.DepenseSerializer


# ==================================================================
# TABLEAU DE BORD ET VIN
# ==================================================================
class TableauDeBordView(SchemaParticuliersMixin, APIView):
    def get(self, request):
        vehicules = list(Vehicule.objects.filter(proprietaire=request.user, archive=False))
        km = {v.pk: v.kilometrage_actuel for v in vehicules}
        rappels = Rappel.objects.filter(vehicule__in=vehicules, actif=True).select_related("vehicule")
        ctx = {"request": request, "km_par_vehicule": km}
        alertes = [r for r in S.RappelSerializer(rappels, many=True, context=ctx).data
                   if r["statut"]["statut"] in ("proche", "en_retard")]
        debut_mois = date.today().replace(day=1)
        from django.db.models import Sum
        depenses_mois = sum(
            (m.objects.filter(vehicule__in=vehicules, date__gte=debut_mois).aggregate(s=Sum("montant"))["s"] or 0)
            for m in (Plein, Entretien, Depense))
        return Response({
            "vehicules": [dict(S.VehiculeSerializer(v, context=ctx).data) for v in vehicules],
            "rappels": sorted(alertes, key=lambda r: (r["statut"]["statut"] != "en_retard",
                                                      r["statut"]["jours_restants"] if r["statut"]["jours_restants"] is not None else 99999)),
            "depenses_mois": calculs.r2(depenses_mois),
            "abonnement": abonnements.etat(request.user),
        })


class VinView(SchemaParticuliersMixin, APIView):
    def get(self, request):
        from voiture.voiture_exemplaire.utils_vin import VinDecoderService
        vin = (request.query_params.get("vin") or "").upper().replace(" ", "")
        if len(vin) != 17 or any(c in vin for c in "IOQ"):
            return Response({"detail": _("VIN invalide : 17 caractères, sans I, O ni Q.")}, status=400)
        try:
            return Response(VinDecoderService(vin).decode())
        except Exception as e:
            return Response({"vin": vin, "detail": str(e)}, status=200)


# ==================================================================
# ABONNEMENT (formules Gratuit / Bronze / Silver / Gold)
# ==================================================================
class AbonnementView(SchemaParticuliersMixin, APIView):
    def get(self, request):
        return Response(abonnements.etat(request.user))


class AchatView(SchemaParticuliersMixin, APIView):
    """Preuve d'achat envoyée par l'application après un achat ou une restauration.

    {"plateforme": "apple" | "google" | "test", "produit": "carscosts_silver_mensuel", "jeton": "…"}
      apple  : transaction signée StoreKit 2 (JWS)  – serverVerificationData
      google : purchaseToken                          – serverVerificationData
      test   : n'importe quelle valeur, uniquement si PARTICULIERS_ACHATS_MODE = "test"
    """

    def post(self, request):
        try:
            abonnements.valider_achat(request.user, request.data.get("plateforme"),
                                      request.data.get("produit") or "", request.data.get("jeton") or "")
        except abonnements.AchatRefuse as e:
            return Response({"detail": str(e)}, status=e.statut)
        return Response(abonnements.etat(request.user))


class NotificationAppleView(APIView):
    """App Store Server Notifications V2 (URL à saisir dans App Store Connect)."""
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        with schema_context(schema_particuliers()):
            try:
                abonnements.notification_apple(request.data.get("signedPayload") or "")
            except abonnements.AchatRefuse as e:
                return Response({"detail": str(e)}, status=e.statut)
        return Response(status=status.HTTP_200_OK)


class NotificationGoogleView(APIView):
    """Real-time developer notifications (abonnement push Pub/Sub) : …/google/?jeton=<GOOGLE_RTDN_JETON>."""
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        import hmac
        from django.conf import settings
        attendu = getattr(settings, "GOOGLE_RTDN_JETON", "")
        if not attendu or not hmac.compare_digest(request.query_params.get("jeton", ""), attendu):
            return Response(status=status.HTTP_403_FORBIDDEN)
        with schema_context(schema_particuliers()):
            try:
                abonnements.notification_google(request.data.get("message") or {})
            except abonnements.AchatRefuse as e:
                # 5xx : Pub/Sub renverra la notification plus tard
                return Response({"detail": str(e)}, status=503 if e.statut >= 500 else 200)
        return Response(status=status.HTTP_200_OK)


class CatalogueView(SchemaParticuliersMixin, APIView):
    """Marques et modèles proposés à la saisie d'un véhicule (fichier particulier/donnees/marques_modeles.json).
    L'application télécharge le catalogue complet et filtre localement (premières lettres)."""

    def get(self, request):
        from ..catalogue import catalogue
        donnees = catalogue()
        if request.headers.get("If-None-Match") == f'"{donnees["version"]}"':
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        reponse = Response(donnees)
        reponse["ETag"] = f'"{donnees["version"]}"'
        return reponse
