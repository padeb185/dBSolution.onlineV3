from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from io import BytesIO
import base64
import qrcode
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django_otp.conf import settings
from django_tenants.utils import schema_context, get_public_schema_name
from .forms import LoginForm, UtilisateurCreationForm
from .models import Utilisateur, UserLog
from django.utils.translation import gettext as _, get_language
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




def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        totp_code = form.cleaned_data.get("totp_code")

        user = authenticate(request, email=email, password=password)

        if not user:
            messages.error(request, _("Email ou mot de passe incorrect"))
            return render(request, "login.html", {"form": form})

        # 🔐 TOTP non configuré → enrôlement
        if not user.totp_enabled:
            if not user.totp_secret:
                user.generate_totp_secret()

            request.session["totp_setup_user"] = str(user.id)
            return redirect("utilisateurs:totp_setup")

        # 🔐 TOTP activé → validation
        if not totp_code:
            messages.error(request, _("Code TOTP requis"))
            return render(request, "login.html", {"form": form})

        if not user.verify_totp(totp_code):
            messages.error(request, _("Code TOTP invalide"))
            return render(request, "login.html", {"form": form})

        # ✅ Login final
        login(request, user)
        request.session["totp_verified"] = True
        request.session["tenant_id"] = str(user.societe.id)

        return redirect("utilisateurs:dashboard")

    return render(request, "login.html", {"form": form})







def logout_view(request):
    logout(request)
    return redirect("utilisateurs:login")




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
        freins_ar = pneus = maintenance = fournisseurs = client_particulier = client_atelier =\
        carrosseries = societe_cliente = adresse = assurance = \
        assurance_police = modele = outils = recharge = maindoeuvre = proprietaire = client =\
        carburant = assurance_police = client_atelier = client_pilotage =  modeles = []

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

            # Récupère les modèles existants pour les liens maintenance
            modeles = VoitureModele.objects.all()
    else:
        modeles = []

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
        'modeles': modeles,
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




def totp_setup_view(request):
    user_id = request.session.get("totp_setup_user")

    if not user_id:
        return redirect("utilisateurs:login")

    user = Utilisateur.objects.get(id=user_id)

    # ❌ Si déjà activé → retour login
    if user.totp_enabled:
        return redirect("utilisateurs:login")

    uri = user.get_totp_uri()
    qr = qrcode.make(uri)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    if request.method == "POST":
        token = request.POST.get("token")

        if user.verify_totp(token):
            user.totp_enabled = True
            user.save()

            # 🧹 Nettoyage de la session
            request.session.pop("totp_setup_user", None)

            messages.success(
                request,
                _("TOTP configuré avec succès. Vous pouvez maintenant vous connecter."
            ))

            # 🔁 REDIRECTION VERS LOGIN
            return redirect("utilisateurs:login")

        messages.error(request, "Code invalide")

    return render(request, "totp/setup.html", {
        "qr_code": qr_base64
    })





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
    utilisateurs = Utilisateur.objects.all().order_by("nom")
    return render(request, "utilisateurs/liste_utilisateurs.html", {
        "utilisateurs": utilisateurs
    })




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


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Utilisateur, PaieUtilisateur
from .forms import PaieUtilisateurForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .forms import PaieUtilisateurForm


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




from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.utils.translation import get_language
from django_tenants.utils import get_public_schema_name


def connexion_globale_view(request):
    tenant = getattr(request, "tenant", None)

    if (
        tenant is not None
        and tenant.schema_name != get_public_schema_name()
    ):
        return redirect("/fr/connexion/")

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        totp_code = request.POST.get("totp_code", "").strip()

        if not email or not password:
            messages.error(
                request,
                "Veuillez saisir votre adresse email et votre mot de passe.",
            )
            return render(
                request,
                "utilisateurs/connexion_globale.html",
            )

        user = authenticate(
            request,
            username=email,
            password=password,
        )

        if user is None:
            messages.error(
                request,
                "Adresse email ou mot de passe incorrect.",
            )
            return render(
                request,
                "utilisateurs/connexion_globale.html",
            )

        if not user.is_active:
            messages.error(
                request,
                "Ce compte utilisateur est désactivé.",
            )
            return render(
                request,
                "utilisateurs/connexion_globale.html",
            )

        if not user.societe_id:
            messages.error(
                request,
                "Aucune société n'est associée à ce compte.",
            )
            return render(
                request,
                "utilisateurs/connexion_globale.html",
            )

        societe = user.societe
        schema_name = societe.schema_name

        if not schema_name:
            messages.error(
                request,
                "La société associée à ce compte ne possède aucun schéma.",
            )
            return render(
                request,
                "utilisateurs/connexion_globale.html",
            )

        if schema_name == get_public_schema_name():
            messages.error(
                request,
                "Ce compte n'est associé à aucun espace client.",
            )
            return render(
                request,
                "utilisateurs/connexion_globale.html",
            )

        # Garde ici ta vérification TOTP actuelle.
        if getattr(user, "totp_enabled", False):
            if not totp_code:
                messages.error(
                    request,
                    "Veuillez saisir votre code TOTP.",
                )
                return render(
                    request,
                    "utilisateurs/connexion_globale.html",
                )

        login(request, user)

        langue = get_language() or settings.LANGUAGE_CODE or "fr"
        langue = langue.split("-")[0]

        prefixe = settings.TENANT_SUBFOLDER_PREFIX.strip("/")

        return redirect(
            f"/{prefixe}/{schema_name}/{langue}/"
        )

    return render(
        request,
        "utilisateurs/connexion_globale.html",
    )