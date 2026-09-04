from django.contrib.auth import  logout
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from .forms import UtilisateurCreationForm
from .models import UserLog
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_moteur.models import MoteurVoiture
from adresse.models import Adresse
from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_boite.models import VoitureBoite
from voiture.voiture_embrayage.models import VoitureEmbrayage
from voiture.voiture_freins_av.models import VoitureFreinsAV
from voiture.voiture_freins_ar.models import VoitureFreinsAR
from voiture.voiture_pneus.models import VoiturePneus
from maintenance.models import Maintenance
from voiture.voiture_modele.models import VoitureModele
from fournisseur.models import Fournisseur
from client_particulier.models import ClientParticulier
from carrosserie.models import Carrosserie
from societe_cliente.models import SocieteCliente
from fuel.models import Fuel
from assurance.models import Assurance
from assurance_police.models import AssurancePolice
from outillage.models import Outillage
from recharge.models import Electricite
from maindoeuvre.models import MainDoeuvre
from proprietaire.models import Proprietaire
from client_atelier.models import ClientAtelier
from client_pilotage.models import ClientPilotage
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import PaieUtilisateurForm
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model, login
from django.utils.translation import get_language
from django_tenants.utils import get_public_schema_name
import base64
from io import BytesIO
import pyotp
import qrcode
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django_tenants.utils import schema_context
from utilisateurs.models import Utilisateur
from .forms import LoginForm









def logout_view(request):
    logout(request)

    request.session.flush()

    return redirect("connexion_globale")



@never_cache
@login_required
def dashboard_view(request):
    user = request.user
    context = {}

    societe = getattr(request.user, "societe", None)

    if not societe:
        messages.error(
            request,
            _("Aucune société n'est liée à cet utilisateur.")
        )
        return redirect("home")

    schema_name = getattr(societe, "schema_name", None)

    # --- Stats initialisées à zéro ---
    total_carburant = 0
    total_assurance_police = 0
    total_client_atelier = 0
    total_maintenances_user = 0


    total_marques = total_moteurs = total_exemplaires = 0
    total_boites = total_embrayages = total_freins = 0
    total_freins_ar = total_pneus = total_maintenance = 0
    total_fournisseur = total_client_particulier = 0
    total_carrosserie = total_societe_cliente = 0
    total_adresse = total_assurance = total_modele = total_outils = 0
    total_recharge = total_main = total_proprietaire = total_client = 0


    marques = moteurs = exemplaires = boites = embrayages = freins = \
        freins_ar = pneus = maintenance = fournisseurs = client_particulier = \
        carrosseries = societe_cliente = adresse = assurance = \
        assurance_police = modele = outils = recharge = maindoeuvre = proprietaire = client =\
        carburant = client_atelier = client_pilotage  = []

    if schema_name:
        with schema_context(schema_name):
            marques = VoitureMarque.objects.filter(societe=societe)
            modele = VoitureModele.objects.filter(societe=societe)
            moteurs = MoteurVoiture.objects.all()
            exemplaires = VoitureExemplaire.objects.filter(societe=societe)
            boites = VoitureBoite.objects.all()
            embrayages = VoitureEmbrayage.objects.all()
            freins = VoitureFreinsAV.objects.filter(societe=societe)
            freins_ar = VoitureFreinsAR.objects.filter(societe=societe)
            pneus = VoiturePneus.objects.filter(societe=societe)


            maintenance = Maintenance.objects.filter(societe=societe)

            fournisseurs = Fournisseur.objects.filter(societe=societe)
            client_particulier = ClientParticulier.objects.filter(societe=societe)
            client_atelier = ClientAtelier.objects.filter(societe=societe)
            client_pilotage = ClientPilotage.objects.filter(societe=societe)
            carrosseries = Carrosserie.objects.filter(societe=societe)
            maindoeuvre = MainDoeuvre.objects.filter(utilisateur__societe=societe)
            proprietaire = Proprietaire.objects.filter(societe=societe)


            societe_cliente = SocieteCliente.objects.filter(societe=societe)
            adresse = Adresse.objects.filter(societe=societe)
            carburant = Fuel.objects.filter(societe=societe)
            assurance = Assurance.objects.filter(societe=societe)
            assurance_police = AssurancePolice.objects.filter(societe=societe)
            outils = Outillage.objects.filter(societe=societe)
            recharge = Electricite.objects.filter(societe=societe)


            # Totaux
            total_marques = marques.count()
            total_modele = modele.count()
            total_moteurs = moteurs.count()
            total_exemplaires = exemplaires.count()
            total_boites = boites.count()
            total_embrayages = embrayages.count()
            total_freins = freins.count()
            total_freins_ar = freins_ar.count()
            total_pneus = pneus.count()
            total_maintenance = maintenance.count()
            total_fournisseur = fournisseurs.count()
            total_client_particulier = client_particulier.count()
            total_client_atelier = client_atelier.count()
            total_carrosserie = carrosseries.count()
            total_societe_cliente = societe_cliente.count()
            total_adresse = adresse.count()
            total_carburant = carburant.count()
            total_assurance = assurance.count()
            total_assurance_police = assurance_police.count()
            total_outils = outils.count()
            total_recharge = recharge.count()
            total_main = maindoeuvre.count()
            total_proprietaire = proprietaire.count()
            total_carburant = carburant.count()
            total_assurance_police = assurance_police.count()
            total_client_atelier = client_atelier.count()
            total_maintenances_user = maintenance.count()

            total_maintenances_user = Maintenance.objects.filter(
                societe=societe
            ).filter(
                Q(mecanicien_id=user.id) |
                Q(chef_mecanicien_id=user.id) |
                Q(apprentis__id=user.id)
            ).distinct().count()

            total_client = client_particulier.count() + client_atelier.count() + client_pilotage.count()

    context.update({
        'user': user,
        'user_nom': user.nom,
        'user_prenom': user.prenom,
        'user_role': user.role,

        # Logs dynamiques
        'date_connexion': timezone.localtime(),
        'derniere_connexion': user.last_login,
        "user_full_name": f"{user.prenom} {user.nom}",
        'societe': societe,
        'total_marques': total_marques,
        'total_modele': total_modele,
        'total_moteurs': total_moteurs,
        'total_exemplaires': total_exemplaires,
        'total_boites': total_boites,
        'total_embrayages': total_embrayages,
        'total_freins': total_freins,
        'total_freins_ar': total_freins_ar,
        'total_pneus': total_pneus,

        'total_maintenance': total_maintenance,

        'total_fournisseur': total_fournisseur,
        'total_client_particulier': total_client_particulier,
        'total_client_atelier': total_client_atelier,
        'total_carrosserie': total_carrosserie,
        'total_societe_cliente': total_societe_cliente,
        'total_adresse': total_adresse,
        'total_carburant': total_carburant,
        'total_assurance': total_assurance,
        'total_outils': total_outils,
        'total_recharge': total_recharge,
        'total_main': total_main,
        'total_proprietaire': total_proprietaire,
        'total_client': total_client,
        "total_maintenances_user": total_maintenances_user,
        "total_assurance_police" : total_assurance_police,


        'marques': marques,
        'modele' : modele,
        'moteurs': moteurs,
        'exemplaires': exemplaires,
        'boites': boites,
        'embrayages': embrayages,
        'freins': freins,
        'freins_ar': freins_ar,
        'pneus': pneus,
        'maintenance': maintenance,
        'fournisseur': fournisseurs,
        'client_particulier': client_particulier,
        'client_atelier': client_atelier,
        'carrosserie': carrosseries,
        'societe_cliente': societe_cliente,
        'adresse': adresse,
        'carburant': carburant,
        'assurance': assurance,
        'assurance_police': assurance_police,
        'outils': outils,
        'recharge': recharge,
        'maindoeuvre': maindoeuvre,
        'proprietaire': proprietaire,
        'client': client,
        'client_pilotage' : client_pilotage,



    })

    # --- Tâches et rôles ---
    context['agenda'] = []
    context['taches'] = []

    role_tasks = {
        'mecanicien': [_("Révision moteur"), _("Changement filtre")],
    }
    if user.role in role_tasks:
        context['taches'] = role_tasks[user.role]

    if user.role == 'comptable':
        context['factures'] = 12
        context['depenses'] = 5
    elif user.role == 'direction':
        context['projets'] = 24
        context['utilisateurs'] = 128

    ROLE_DISPLAY = {
        'apprentis': _("Apprenti"),
        'mecanicien': _("Mécanicien"),
        'carrossier': _("Carrossier"),
        'chef_mecanicien': _("Chef Mécanicien"),
        'magasinier': _("Magasinier"),
        'instructeur': _("Instructeur"),
        'instructeur_externe': _("Instructeur Externe"),
        'vendeur': _("Vendeur"),
        'comptable': _("Comptable"),
        'direction': _("Direction"),
    }
    context['role_display'] = ROLE_DISPLAY.get(user.role, _("Rôle inconnu"))
    context["societe"] = societe
    context["schema_name"] = schema_name

    try:
        context["dernieres_activites"] = UserLog.objects.filter(
            utilisateur=request.user,
            utilisateur__societe=request.user.societe
        ).order_by("-date_action")[:100]
    except Exception:
        context["dernieres_activites"] = []

    return render(request, 'dashboard.html', context)





def get_user_maintenance_count(user, societe):
    query = Maintenance.objects.filter(societe=societe)

    role_filters = {
        "mecanicien": {"mecanicien": user},
        "chef_mecanicien": {"chef_mecanicien": user},
        "apprentis": {"apprentis": user},
    }

    if user.role in role_filters:
        query = query.filter(**role_filters[user.role])

    return query.count()





@never_cache
def totp_setup_view(request):
    """
    Configuration initiale du TOTP.

    L'utilisateur est stocké dans le schéma public et rattaché
    à une société, par exemple au tenant campus.
    """

    user_id = request.session.get("totp_setup_user")
    schema_name = request.session.get("totp_setup_tenant")

    if not user_id or not schema_name:
        messages.error(
            request,
            _("La session d'activation a expiré. Veuillez vous reconnecter."),
        )
        return redirect("/fr/connexion/")

    erreur = None
    deja_active = False
    secret = None
    uri = None

    # =====================================================
    # Récupération de l'utilisateur dans le schéma public
    # =====================================================

    with schema_context("public"):
        try:
            user = (
                Utilisateur.objects
                .select_related("societe")
                .get(pk=user_id)
            )
        except Utilisateur.DoesNotExist:
            user = None
            erreur = _("Utilisateur introuvable.")

        if user is not None:
            if not user.is_active:
                erreur = _("Ce compte utilisateur est désactivé.")

            elif not user.societe_id:
                erreur = _(
                    "Aucune société n'est liée à cet utilisateur."
                )

            elif user.societe.schema_name != schema_name:
                erreur = _(
                    "La société de connexion ne correspond pas."
                )

            elif user.totp_enabled:
                deja_active = True

            else:
                # Génération et sauvegarde d'un secret Base32 valide.
                if not user.totp_secret:
                    user.totp_secret = pyotp.random_base32()
                    user.save(update_fields=["totp_secret"])

                secret = user.totp_secret

                # Génération explicite d'une URI compatible Authy.
                issuer_name = f"dBSolution {user.societe.schema_name.capitalize()}"

                uri = pyotp.TOTP(secret).provisioning_uri(
                    name=user.email,
                    issuer_name=issuer_name,
                )

    # =====================================================
    # Gestion des erreurs
    # =====================================================

    if erreur:
        request.session.pop("totp_setup_user", None)
        request.session.pop("totp_setup_tenant", None)
        request.session.pop("totp_setup_societe", None)

        messages.error(request, erreur)
        return redirect("/fr/connexion/")

    # =====================================================
    # TOTP déjà configuré
    # =====================================================

    if deja_active:
        request.session.pop("totp_setup_user", None)
        request.session.pop("totp_setup_tenant", None)
        request.session.pop("totp_setup_societe", None)

        messages.info(
            request,
            _(
                "La vérification à deux facteurs est déjà configurée. "
                "Connectez-vous avec votre code Authy."
            ),
        )

        return redirect("/fr/connexion/")

    # =====================================================
    # Génération du QR Code
    # =====================================================

    qr_code = None

    if uri:
        qr = qrcode.make(uri)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        qr_code = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

    # =====================================================
    # Validation du premier code Authy
    # =====================================================

    if request.method == "POST":
        # Le template utilise name="token".
        token = (
            request.POST.get("token") or ""
        ).strip().replace(" ", "")

        if not token:
            messages.error(
                request,
                _(
                    "Saisissez le code à six chiffres "
                    "affiché dans Authy."
                ),
            )

        elif not token.isdigit() or len(token) != 6:
            messages.error(
                request,
                _("Le code doit contenir exactement six chiffres."),
            )

        else:
            activation_reussie = False

            with schema_context("public"):
                try:
                    user = (
                        Utilisateur.objects
                        .select_related("societe")
                        .get(
                            pk=user_id,
                            societe__schema_name=schema_name,
                        )
                    )
                except Utilisateur.DoesNotExist:
                    user = None

                if user is not None and user.totp_secret:
                    totp = pyotp.TOTP(user.totp_secret)

                    # valid_window=1 accepte une légère différence
                    # d'horloge entre le serveur et Authy.
                    if totp.verify(token, valid_window=1):
                        user.totp_enabled = True
                        user.save(update_fields=["totp_enabled"])
                        activation_reussie = True

            if activation_reussie:
                request.session.pop("totp_setup_user", None)
                request.session.pop("totp_setup_tenant", None)
                request.session.pop("totp_setup_societe", None)

                request.session["totp_verified"] = False
                request.session.pop("totp_user_id", None)
                request.session.pop("tenant_id", None)
                request.session.pop("tenant_schema", None)

                request.session.modified = True

                messages.success(
                    request,
                    _(
                        "La vérification à deux facteurs est activée. "
                        "Connectez-vous maintenant avec votre adresse "
                        "e-mail, votre mot de passe et votre code Authy ou Google Authenticator."
                    ),
                )

                return redirect("/fr/connexion/")

            messages.error(
                request,
                _("Le code Authy est invalide ou expiré."),
            )

    return render(
        request,
        "theme/totp/setup.html",
        {
            "qr_code": qr_code,
            "secret": secret,
            "totp_uri": uri,
            "tenant_schema": schema_name,
        },
    )


def is_admin(user):
    return user.is_staff and user.is_superuser




@login_required
@user_passes_test(is_admin)
def creer_utilisateur(request):
    societe_courante = request.user.societe

    initial_data = {
        "societe": societe_courante.nom if societe_courante else "",
        "schema_name": societe_courante.schema_name if societe_courante else "",
    }

    if request.method == "POST":
        form = UtilisateurCreationForm(request.POST, initial=initial_data)

        if form.is_valid():
            data = form.cleaned_data

            try:
                adresse = Adresse.objects.create(
                    rue=data["rue"],
                    numero=data["numero"],
                    code_postal=data["code_postal"],
                    ville=data["ville"],
                    pays=data["pays"],
                )

                Utilisateur.objects.create_user(
                    email=data["email"],
                    password=data["password"],
                    nom=data["nom"],
                    prenom=data["prenom"],
                    role=data["role"],
                    telephone=data["telephone"] or None,
                    email_entreprise=data["email_entreprise"] or None,
                    date_naissance=data["date_naissance"] or None,
                    societe=societe_courante,
                    schema_name=societe_courante.schema_name,
                    adresse=adresse,
                )

                messages.success(request, _("Utilisateur créé avec succès."))
                return redirect("utilisateurs:creer_utilisateur")

            except Exception as e:
                messages.error(request, f"Erreur: {e}")

    else:
        form = UtilisateurCreationForm(initial=initial_data)

    return render(request, "utilisateurs/creer_utilisateur.html", {
        "form": form
    })



def is_admin(user):
    return user.is_staff and user.is_superuser


@never_cache
@login_required
@user_passes_test(is_admin)
def dashboard_admin(request):
    total_utilisateurs = Utilisateur.objects.count()
    utilisateurs_actifs = Utilisateur.objects.filter(is_active=True).count()
    total_admins = Utilisateur.objects.filter(is_staff=True, is_superuser=True).count()

    context = {
        "total_utilisateurs": total_utilisateurs,
        "utilisateurs_actifs": utilisateurs_actifs,
        "total_admins": total_admins,
    }
    return render(request, "admin/dashboard_admin.html", context)



@login_required
@user_passes_test(is_admin)
def liste_utilisateurs(request):
    tenant = request.user.societe

    utilisateurs = Utilisateur.objects.filter(
        societe=tenant
    ).order_by("nom")

    return render(
        request,
        "utilisateurs/liste_utilisateurs.html",
        {
            "utilisateurs": utilisateurs,
        }
    )


@receiver(user_logged_in)
def log_connexion(sender, request, user, **kwargs):
    UserLog.objects.create(
        utilisateur=user,
        action="Connexion"
    )


@receiver(user_logged_out)
def log_deconnexion(sender, request, user, **kwargs):
    if user:
        UserLog.objects.create(
            utilisateur=user,
            action="Déconnexion"
        )





@login_required
def creer_paie_utilisateur(request):
    if request.method == "POST":
        form = PaieUtilisateurForm(
            request.POST,
            societe=request.user.societe
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                _("La paie mensuelle a été enregistrée avec succès.")
            )

            return redirect("utilisateurs:dashboard")

    else:
        form = PaieUtilisateurForm(
            societe=request.user.societe,
            initial={
                "mois": timezone.now().month,
                "annee": timezone.now().year,
            }
        )

    return render(
        request,
        "utilisateurs/creer_paie_utilisateur.html",
        {
            "form": form,
            "now": timezone.now(),
        }
    )

def enable_totp(self, token):
    if not self.verify_totp(token):
        return False

    self.totp_enabled = True

    self.save(
        update_fields=[
            "totp_enabled",
            "updated_at",
        ]
    )

    return True







Utilisateur = get_user_model()

BACKEND_PATH = (
    "utilisateurs.backends.PublicSchemaModelBackend"
)


def get_langue_active():
    langue = (
        get_language() or "fr"
    ).split("-")[0].strip().lower()

    langues_autorisees = {
        "fr",
        "en",
        "de",
        "es",
        "it",
        "nl",
        "el",
    }

    if langue not in langues_autorisees:
        langue = "fr"

    return langue


def build_tenant_url(
    schema_name,
    langue,
    chemin,
):
    """
    Construit une URL tenant de la forme :

    /tenant/dbsolution/fr/utilisateurs/dashboard/
    """

    schema_name = (
        schema_name or ""
    ).strip().lower()

    langue = (
        langue or "fr"
    ).strip().lower()

    chemin = chemin.strip("/")

    return (
        f"/tenant/{schema_name}/"
        f"{langue}/{chemin}/"
    )




@never_cache
def connexion_globale_view(request):
    """
    Connexion globale multi-tenant.

    Première connexion :
        e-mail + mot de passe
        → configuration du TOTP
        → tenant de l'utilisateur

    Connexions suivantes :
        e-mail + mot de passe + code TOTP
        → connexion Django
        → dashboard du tenant
    """

    # -------------------------------------------------
    # La connexion doit toujours passer par le public.
    # -------------------------------------------------

    if request.path.startswith("/tenant/"):
        langue = (
            getattr(request, "LANGUAGE_CODE", "fr")
            or "fr"
        ).split("-")[0].lower()

        return redirect(f"/{langue}/connexion/")

    form = LoginForm(request.POST or None)

    # -------------------------------------------------
    # Affichage initial
    # -------------------------------------------------

    if request.method != "POST":
        return render(
            request,
            "utilisateurs/connexion_globale.html",
            {
                "form": form,
            },
        )

    # -------------------------------------------------
    # Validation du formulaire
    # -------------------------------------------------

    if not form.is_valid():
        return render(
            request,
            "utilisateurs/connexion_globale.html",
            {
                "form": form,
            },
        )

    email = (
        form.cleaned_data["email"]
        .strip()
        .lower()
    )

    password = form.cleaned_data["password"]

    totp_code = (
        form.cleaned_data.get("totp_code")
        or ""
    ).strip()

    utilisateur = None
    societe = None

    schema_name = ""
    societe_id = ""
    societe_uuid = ""

    totp_enabled = False
    totp_valide = False

    erreur = None

    public_schema_name = (
        get_public_schema_name()
        or "public"
    )

    # -------------------------------------------------
    # Recherche de l'utilisateur dans public
    # -------------------------------------------------

    with schema_context(public_schema_name):
        try:
            utilisateur = (
                Utilisateur.objects
                .select_related("societe")
                .get(email__iexact=email)
            )

        except Utilisateur.DoesNotExist:
            utilisateur = None

        if utilisateur is None:
            erreur = _(
                "Adresse e-mail ou mot de passe incorrect."
            )

        elif not utilisateur.check_password(password):
            erreur = _(
                "Adresse e-mail ou mot de passe incorrect."
            )

        elif not utilisateur.is_active:
            erreur = _(
                "Ce compte utilisateur est désactivé."
            )

        elif not utilisateur.societe_id:
            erreur = _(
                "Aucune société n'est associée à ce compte."
            )

        else:
            societe = utilisateur.societe

            schema_name = (
                getattr(
                    societe,
                    "schema_name",
                    "",
                )
                or ""
            ).strip().lower()

            societe_id = str(societe.pk)

            societe_uuid = str(
                getattr(
                    societe,
                    "id_societe",
                    "",
                )
                or ""
            )

            if not schema_name:
                erreur = _(
                    "Aucun schéma tenant n'est associé "
                    "à cet utilisateur."
                )

            elif schema_name == public_schema_name:
                erreur = _(
                    "Ce compte n'est associé à aucune "
                    "société privée."
                )

            else:
                totp_enabled = bool(
                    getattr(
                        utilisateur,
                        "totp_enabled",
                        False,
                    )
                )

                totp_secret_present = bool(
                    getattr(
                        utilisateur,
                        "totp_secret",
                        None,
                    )
                )

                # Un TOTP activé sans secret est invalide.
                if (
                    totp_enabled
                    and not totp_secret_present
                ):
                    utilisateur.totp_enabled = False

                    utilisateur.save(
                        update_fields=[
                            "totp_enabled",
                        ]
                    )

                    totp_enabled = False

                # Validation du code TOTP.
                if totp_enabled and totp_code:
                    try:
                        totp_valide = bool(
                            utilisateur.verify_totp(
                                totp_code
                            )
                        )

                    except (
                        TypeError,
                        ValueError,
                        AttributeError,
                    ):
                        totp_valide = False

    # -------------------------------------------------
    # Erreur d'authentification
    # -------------------------------------------------

    if erreur:
        messages.error(
            request,
            erreur,
        )

        return render(
            request,
            "utilisateurs/connexion_globale.html",
            {
                "form": form,
            },
        )

    langue = get_langue_active()

    # -------------------------------------------------
    # Première connexion : configuration du TOTP
    # -------------------------------------------------

    if not totp_enabled:
        request.session.flush()

        request.session["totp_setup_user"] = str(
            utilisateur.pk
        )

        request.session["totp_setup_tenant"] = (
            schema_name
        )

        request.session["totp_setup_societe"] = (
            societe_id
        )

        request.session["totp_setup_societe_uuid"] = (
            societe_uuid
        )

        destination_totp = build_tenant_url(
            schema_name=schema_name,
            langue=langue,
            chemin="utilisateurs/totp/setup",
        )

        return redirect(destination_totp)

    # -------------------------------------------------
    # TOTP configuré : code obligatoire
    # -------------------------------------------------

    if not totp_code:
        messages.error(
            request,
            _(
                "Veuillez saisir le code de sécurité "
                "généré par votre application Authy."
            ),
        )

        return render(
            request,
            "utilisateurs/connexion_globale.html",
            {
                "form": form,
            },
        )

    if not totp_valide:
        messages.error(
            request,
            _(
                "Le code de sécurité est incorrect "
                "ou a expiré."
            ),
        )

        return render(
            request,
            "utilisateurs/connexion_globale.html",
            {
                "form": form,
            },
        )

    # -------------------------------------------------
    # Connexion Django
    # -------------------------------------------------

    login(
        request,
        utilisateur,
        backend=BACKEND_PATH,
    )

    # Important : ces valeurs doivent être enregistrées
    # après login(), car login() renouvelle la session.
    request.session["totp_verified"] = True
    request.session["totp_user_id"] = str(
        utilisateur.pk
    )

    request.session["tenant_schema"] = schema_name
    request.session["tenant_id"] = societe_id
    request.session["tenant_uuid"] = societe_uuid

    request.session.pop(
        "totp_setup_user",
        None,
    )

    request.session.pop(
        "totp_setup_tenant",
        None,
    )

    request.session.pop(
        "totp_setup_societe",
        None,
    )

    request.session.pop(
        "totp_setup_societe_uuid",
        None,
    )

    request.session.modified = True

    messages.success(
        request,
        _("Connexion réussie."),
    )

    # -------------------------------------------------
    # Dashboard du tenant
    # -------------------------------------------------

    destination_dashboard = build_tenant_url(
        schema_name=schema_name,
        langue=langue,
        chemin="utilisateurs/dashboard",
    )


    return redirect(destination_dashboard)