from datetime import date, timedelta
from decimal import Decimal as D

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
from ..models import Depense, Document, Entretien, MaintenanceParticulier, Plein, TrainPneus, Rappel, ReleveKilometrique, Vehicule
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

    @action(detail=True, methods=["get", "put", "delete"])
    def financement(self, request, pk=None):
        """Type d'achat (formule Bronze minimum pour l'enregistrer) : GET / PUT / DELETE."""
        from ..models import Financement
        vehicule = self.get_object()
        existant = Financement.objects.filter(vehicule=vehicule).first()
        disponible = abonnements.formule_effective(request.user) != "gratuit"
        if request.method != "GET":
            if not disponible:
                return Response({"detail": _("Le type d'achat est disponible à partir de la formule Bronze."),
                                 "code": "formule_requise", "formule_requise": "bronze"},
                                status=status.HTTP_403_FORBIDDEN)
            if request.method == "DELETE":
                if existant:
                    existant.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            ser = S.FinancementSerializer(existant, data=request.data)
            ser.is_valid(raise_exception=True)
            existant = ser.save(vehicule=vehicule)
            vehicule = Vehicule.objects.get(pk=vehicule.pk)
        return Response({
            "disponible": disponible,
            "donnees": S.FinancementSerializer(existant).data if existant else None,
            "calculs": calculs.financement(vehicule),
        })

    @action(detail=True)
    def rapport(self, request, pk=None):
        """Rapport : carburant, électricité, financement, coûts et kilomètres par mois (?periode=12m|annee|tout|2025).
        Formule payante (Bronze minimum)."""
        vehicule = self.get_object()
        if abonnements.formule_effective(request.user) == "gratuit":
            return Response({"detail": _("Le rapport est disponible à partir de la formule Bronze."),
                             "code": "formule_requise", "formule_requise": "bronze"},
                            status=status.HTTP_403_FORBIDDEN)
        return Response(calculs.rapport(vehicule, request.query_params.get("periode")))

    @action(detail=True, methods=["get", "put"])
    def deductibilite(self, request, pk=None):
        """Déductibilité (TVA, impôt) selon le pays d'immatriculation : GET ?annee=2026, PUT le profil fiscal.
        Formule payante (Bronze minimum)."""
        from .. import deductibilite
        from ..models import ProfilFiscal
        vehicule = self.get_object()
        if abonnements.formule_effective(request.user) == "gratuit":
            return Response({"detail": _("La déductibilité est disponible à partir de la formule Bronze."),
                             "code": "formule_requise", "formule_requise": "bronze"},
                            status=status.HTTP_403_FORBIDDEN)
        if request.method == "PUT":
            ser = S.ProfilFiscalSerializer(ProfilFiscal.objects.filter(vehicule=vehicule).first(), data=request.data)
            ser.is_valid(raise_exception=True)
            ser.save(vehicule=vehicule)
        annee = request.query_params.get("annee")
        annee = int(annee) if annee and annee.isdigit() and 2000 <= int(annee) <= 2100 else None
        return Response(deductibilite.deductibilite(vehicule, annee))

    # ------------------------------------------------------------------ (Re)vente (formule Bronze)
    def _vente_bronze(self, request):
        if abonnements.formule_effective(request.user) == "gratuit":
            return Response({"detail": _("La vente est disponible à partir de la formule Bronze."),
                             "code": "formule_requise", "formule_requise": "bronze"}, status=status.HTTP_403_FORBIDDEN)
        return None

    def _reponse_vente(self, vehicule, vente):
        from .. import vente as module_vente
        if vente is None:
            return Response({"vente": None, "proposition": self._proposition_vente(vehicule)})
        return Response({"vente": S.VenteSerializer(vente).data, **module_vente.etat(vente)})

    def _proposition_vente(self, vehicule):
        u = self.request.user
        adresse = getattr(u, "adresse", None)
        return {"vendeur_nom": f"{u.prenom or ''} {u.nom or ''}".strip(),
                "vendeur_adresse": f"{adresse.rue} {adresse.numero}\n{adresse.code_postal} {adresse.ville}".strip()
                if adresse else "",
                "kilometrage_vente": vehicule.kilometrage_actuel,
                "montant_saisi": vehicule.valeur_estimee,
                "doc_car_pass": (vehicule.pays_immatriculation or "").upper() == "BE"}

    @action(detail=True, methods=["get", "put", "delete"])
    def vente(self, request, pk=None):
        """Vente du véhicule : GET (vente ou proposition), PUT (brouillon), DELETE (brouillon seulement)."""
        from ..models import VenteParticulier
        refus = self._vente_bronze(request)
        if refus:
            return refus
        vehicule = get_object_or_404(Vehicule, pk=pk, proprietaire=request.user)   # vendu (archivé) compris
        vente = VenteParticulier.objects.filter(vehicule=vehicule).first()
        if request.method == "DELETE":
            if vente and vente.statut == "vendue":
                return Response({"detail": _("Annulez d'abord la vente.")}, status=status.HTTP_400_BAD_REQUEST)
            if vente:
                vente.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == "PUT":
            ser = S.VenteSerializer(vente, data=request.data)
            ser.is_valid(raise_exception=True)
            vente = ser.save(vehicule=vehicule)
        return self._reponse_vente(vehicule, vente)

    @action(detail=True, methods=["post"], url_path="vente/finaliser")
    def finaliser_vente(self, request, pk=None):
        from .. import vente as module_vente
        from ..models import VenteParticulier
        refus = self._vente_bronze(request)
        if refus:
            return refus
        vente = get_object_or_404(VenteParticulier, vehicule__pk=pk, vehicule__proprietaire=request.user)
        etat = module_vente.etat(vente)
        if not etat["peut_finaliser"]:
            return Response({"detail": " ".join(a["message"] for a in etat["alertes"] if a["niveau"] == "erreur")},
                            status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            module_vente.finaliser(vente)
        return self._reponse_vente(vente.vehicule, vente)

    @action(detail=True, methods=["post"], url_path="vente/annuler")
    def annuler_vente(self, request, pk=None):
        """Retour en brouillon : le véhicule redevient actif (limite de la formule vérifiée)."""
        from .. import vente as module_vente
        from ..models import VenteParticulier
        refus = self._vente_bronze(request)
        if refus:
            return refus
        vente = get_object_or_404(VenteParticulier, vehicule__pk=pk, vehicule__proprietaire=request.user)
        if vente.statut == "vendue":
            with transaction.atomic():
                _verrouiller(request.user)
                _controler_limite(request.user, sauf=vente.vehicule.pk)
                module_vente.annuler(vente)
        return self._reponse_vente(vente.vehicule, vente)

    @action(detail=True, url_path="recapitulatif/pdf")
    def recapitulatif_pdf(self, request, pk=None):
        """Récapitulatif imprimable du véhicule et de ses coûts totaux (PDF). Formule Bronze minimum."""
        from django.http import HttpResponse
        from .. import recapitulatif
        if abonnements.formule_effective(request.user) == "gratuit":
            return Response({"detail": _("Le récapitulatif PDF est disponible à partir de la formule Bronze."),
                             "code": "formule_requise", "formule_requise": "bronze"}, status=status.HTTP_403_FORBIDDEN)
        vehicule = get_object_or_404(Vehicule, pk=pk, proprietaire=request.user)   # archivé compris
        reponse = HttpResponse(recapitulatif.pdf(vehicule), content_type="application/pdf")
        nom = f"recapitulatif_{vehicule.marque}_{vehicule.modele}_{vehicule.immatriculation}".replace(" ", "_")
        reponse["Content-Disposition"] = f'inline; filename="{nom}.pdf"'
        return reponse

    @action(detail=True, url_path="vente/pdf")
    def pdf_vente(self, request, pk=None):
        """Certificat de cession et bon de livraison (PDF, à signer par les deux parties)."""
        from django.http import HttpResponse
        from django.template.loader import render_to_string
        from weasyprint import HTML
        from .. import vente as module_vente
        from ..plaque import plaque_svg
        from ..models import VenteParticulier
        refus = self._vente_bronze(request)
        if refus:
            return refus
        vente = get_object_or_404(VenteParticulier, vehicule__pk=pk, vehicule__proprietaire=request.user)
        html = render_to_string("particulier/pdf_cession.html", {
            "vente": vente, "v": vente.vehicule, "mention": module_vente.mention_legale(vente),
            "plaque": plaque_svg(vente.vehicule.immatriculation, vente.vehicule.pays_immatriculation, 28),
            "tva_affichee": vente.regime_tva in ("NORMAL",)})
        reponse = HttpResponse(HTML(string=html).write_pdf(), content_type="application/pdf")
        nom = f"cession_{vente.vehicule.immatriculation or vente.vehicule.marque}.pdf".replace(" ", "_")
        reponse["Content-Disposition"] = f'inline; filename="{nom}"'
        return reponse

    @action(detail=True, methods=["get", "put"])
    def plan_entretien(self, request, pk=None):
        """Plan d'entretien : rappels automatiques d'entretien (normal 1 an / Long Life 2 ans + km),
        de contrôle technique (règle du pays) et échéance d'assurance. PUT : {entretien: {...}, controle_technique: {...}}."""
        from .. import rappels_auto
        vehicule = self.get_object()
        if request.method == "PUT":
            with transaction.atomic():
                return Response(rappels_auto.appliquer(vehicule, request.data.get("entretien"),
                                                       request.data.get("controle_technique")))
        return Response(rappels_auto.plan(vehicule))

    @action(detail=True)
    def tva(self, request, pk=None):
        """TVA à récupérer (usage professionnel) : dépenses avec TVA par trimestre ou par mois
        (?annee=2026&periode=trimestre|mois). Formule Bronze minimum."""
        from .. import deductibilite
        vehicule = self.get_object()
        if abonnements.formule_effective(request.user) == "gratuit":
            return Response({"detail": _("La déductibilité est disponible à partir de la formule Bronze."),
                             "code": "formule_requise", "formule_requise": "bronze"},
                            status=status.HTTP_403_FORBIDDEN)
        annee = request.query_params.get("annee")
        annee = int(annee) if annee and annee.isdigit() and 2000 <= int(annee) <= 2100 else None
        periode = "mois" if request.query_params.get("periode") == "mois" else "trimestre"
        return Response(deductibilite.journal_tva(vehicule, annee, periode))

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

    def list(self, request, *args, **kwargs):
        """?historique=1 : tous les kilométrages connus (relevés, pleins, recharges, entretiens, achat),
        du plus récent au plus ancien, avec la distance parcourue depuis le précédent (« ecart »)."""
        if request.query_params.get("historique") != "1":
            return super().list(request, *args, **kwargs)
        vehicules = Vehicule.objects.filter(proprietaire=request.user)
        if request.query_params.get("vehicule"):
            vehicules = vehicules.filter(pk=request.query_params["vehicule"])
        lignes = [{**d, "source": "releve", "libelle": ""}
                  for d in self.get_serializer(self.get_queryset(), many=True).data]
        for p in Plein.objects.filter(vehicule__in=vehicules):
            lignes.append({"id": f"plein-{p.pk}", "vehicule": str(p.vehicule_id), "date": p.date.isoformat(),
                           "kilometrage": p.kilometrage, "libelle": p.get_carburant_display(),
                           "source": "recharge" if p.carburant == "electricite" else "plein"})
        for e in Entretien.objects.filter(vehicule__in=vehicules, kilometrage__isnull=False):
            lignes.append({"id": f"entretien-{e.pk}", "vehicule": str(e.vehicule_id), "date": e.date.isoformat(),
                           "kilometrage": e.kilometrage, "libelle": e.get_type_display(), "source": "entretien"})
        for m in MaintenanceParticulier.objects.filter(vehicule__in=vehicules, kilometrage__isnull=False):
            lignes.append({"id": f"maintenance-{m.pk}", "vehicule": str(m.vehicule_id), "date": m.date.isoformat(),
                           "kilometrage": m.kilometrage, "libelle": m.get_type_maintenance_display(),
                           "source": "maintenance"})
        for v in vehicules.filter(kilometrage_achat__isnull=False):
            lignes.append({"id": f"achat-{v.pk}", "vehicule": str(v.pk),
                           "date": v.date_achat.isoformat() if v.date_achat else None,
                           "kilometrage": v.kilometrage_achat, "libelle": "", "source": "achat"})
        # Chronologique (achat en premier si sans date) pour l'écart, puis du plus récent au plus ancien
        lignes.sort(key=lambda l: (str(l["vehicule"]), l["date"] or "", l["kilometrage"]))
        precedent = {}
        for l in lignes:
            km_avant = precedent.get(str(l["vehicule"]))
            l["ecart"] = l["kilometrage"] - km_avant if km_avant is not None else None
            precedent[str(l["vehicule"])] = l["kilometrage"]
        lignes.sort(key=lambda l: (l["date"] or "", l["kilometrage"]), reverse=True)
        return Response(lignes)


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


class FormuleBronze(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = "formule_requise"


def _noter_kilometrage(vehicule, jour, km):
    """Kilométrage saisi avec les pneus plus élevé que le dernier connu : relevé ajouté."""
    if km and km > vehicule.kilometrage_actuel:
        ReleveKilometrique.objects.create(vehicule=vehicule, date=jour or date.today(), kilometrage=km)


class PneusViewSet(ProprietaireViewSet):
    """Pneus par train (avant / arrière), première et seconde monte, kilométrage mémorisé par train.
    Formule Bronze minimum."""
    model = TrainPneus
    serializer_class = S.TrainPneusSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if abonnements.formule_effective(request.user) == "gratuit":
            exc = FormuleBronze()
            exc.detail = {"detail": _("Les pneus sont disponibles à partir de la formule Bronze."),
                          "code": "formule_requise", "formule_requise": "bronze"}
            raise exc

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = dict(ser.validated_data)
        vehicule = d["vehicule"]
        monter = d.pop("monter_maintenant", True)
        position = d.pop("position")
        positions = ["avant", "arriere"] if position == "les_deux" else [position]
        km = d.pop("km_montage", None)
        km = vehicule.kilometrage_actuel if km is None else km
        if d.get("prix") is not None and len(positions) == 2:
            d["prix"] = (d["prix"] / 2).quantize(D("0.01"))
        crees = []
        with transaction.atomic():
            for pos in positions:
                trains = TrainPneus.objects.select_for_update().filter(vehicule=vehicule, position=pos)
                ancien = trains.filter(monte=d.get("monte", "premiere"), actif=True).first()
                monte_ancien = bool(ancien and ancien.est_monte)
                if ancien:   # remplacement : l'ancien train est archivé avec ses km
                    ancien.demonter(km)
                    ancien.actif = False
                    ancien.date_remplacement = d.get("date_montage") or date.today()
                    ancien.km_remplacement = km
                    ancien.save()
                numero = (max((t.numero for t in trains), default=0)) + 1
                train = TrainPneus(**d, position=pos, numero=numero, km_montage=km, train_remplace=ancien)
                train.date_achat = train.date_achat or train.date_montage
                personne_monte = not trains.filter(actif=True, est_monte=True).exists()
                if monter or monte_ancien or personne_monte:
                    for autre in trains.filter(actif=True, est_monte=True):
                        autre.demonter(km)
                        autre.save()
                    train.monter(km)
                train.save()
                crees.append(train)
            _noter_kilometrage(vehicule, d.get("date_montage"), km)
        return Response(self.get_serializer(crees[0]).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def changer_monte(self, request):
        """Été ↔ hiver : sur chaque essieu, la monte montée est démontée (km mémorisés) et l'autre est montée."""
        vehicule = get_object_or_404(Vehicule, pk=request.data.get("vehicule"), proprietaire=request.user)
        try:
            km = int(request.data.get("kilometrage") or vehicule.kilometrage_actuel)
            jour = date.fromisoformat(request.data["date"]) if request.data.get("date") else date.today()
        except (TypeError, ValueError):
            return Response({"detail": _("Kilométrage ou date invalide.")}, status=status.HTTP_400_BAD_REQUEST)
        changes = 0
        with transaction.atomic():
            for pos in ("avant", "arriere"):
                trains = TrainPneus.objects.select_for_update().filter(vehicule=vehicule, position=pos, actif=True)
                actuel = trains.filter(est_monte=True).first()
                autre = trains.exclude(pk=actuel.pk if actuel else None).filter(
                    monte="seconde" if actuel and actuel.monte == "premiere" else "premiere").first()
                if not autre:
                    continue
                if actuel:
                    if km < actuel.km_montage:
                        return Response({"detail": _("Le kilométrage est inférieur à celui du dernier montage ({km} km).")
                                         .replace("{km}", str(actuel.km_montage))}, status=status.HTTP_400_BAD_REQUEST)
                    actuel.demonter(km)
                    actuel.save()
                autre.monter(km)
                autre.date_montage = jour
                autre.save()
                changes += 1
            if not changes:
                return Response({"detail": _("Aucune autre monte enregistrée : ajoutez d'abord les pneus de la seconde monte.")},
                                status=status.HTTP_400_BAD_REQUEST)
            _noter_kilometrage(vehicule, jour, km)
        return Response(self.get_serializer(TrainPneus.objects.filter(vehicule=vehicule), many=True).data)


class MaintenanceViewSet(ProprietaireViewSet):
    """Maintenances par un garage (pièces / main-d'œuvre séparées) : formule Bronze minimum."""
    model = MaintenanceParticulier
    serializer_class = S.MaintenanceSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if abonnements.formule_effective(request.user) == "gratuit":
            exc = FormuleBronze()
            exc.detail = {"detail": _("Les maintenances sont disponibles à partir de la formule Bronze."),
                          "code": "formule_requise", "formule_requise": "bronze"}
            raise exc

    def perform_create(self, serializer):
        m = serializer.save()
        from ..rappels_auto import apres_entretien
        apres_entretien(m.vehicule, m.date, m.kilometrage, type_maintenance=m.type_maintenance)

    @action(detail=False)
    def types(self, request):
        """Types de maintenance (libellés traduits dans la langue de l'utilisateur) et leur famille."""
        from ..models import famille_maintenance, types_maintenance
        return Response([{"code": c, "libelle": str(l), "famille": famille_maintenance(c)}
                         for c, l in types_maintenance()])

    @action(detail=True)
    def facture(self, request, pk=None):
        return self._fichier("facture")


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
        self._apres(serializer.save())

    def perform_update(self, serializer):
        self._apres(serializer.save())

    def _apres(self, document):
        calculs.synchroniser_rappel_document(document)
        if document.type == "controle_technique":      # nouveau contrôle : rappel automatique recalculé
            from ..rappels_auto import apres_entretien
            apres_entretien(document.vehicule, document.date_debut, None, type_entretien="controle_technique")

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
            for m in (Plein, Entretien, Depense)) + (MaintenanceParticulier.objects.filter(
                vehicule__in=vehicules, date__gte=debut_mois).aggregate(s=Sum("total_tvac"))["s"] or 0) + (
            TrainPneus.objects.filter(vehicule__in=vehicules, date_achat__gte=debut_mois)
            .aggregate(s=Sum("prix"))["s"] or 0)
        # Documents : prime d'assurance mensuelle de ce mois (et prime annuelle ou montant unique tombant ce mois-ci)
        # (jusqu'à la fin du mois : une prime prélevée le 25 compte dès le 1er)
        fin_mois = calculs.ajouter_mois(debut_mois, 1) - timedelta(days=1)
        depenses_mois += sum((montant for d in Document.objects.filter(vehicule__in=vehicules, montant__isnull=False)
                              for jour, montant in calculs.paiements_document(d, fin_mois)
                              if jour and debut_mois <= jour <= fin_mois), 0)
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
        # Logos : URL complètes (fichiers statiques publics, servis par le serveur web)
        from django.templatetags.static import static
        donnees = {**donnees, "logos": {m: request.build_absolute_uri(static(chemin))
                                         for m, chemin in donnees.get("logos", {}).items()}}
        reponse = Response(donnees)
        reponse["ETag"] = f'"{donnees["version"]}"'
        return reponse
