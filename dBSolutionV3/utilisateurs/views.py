from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from io import BytesIO
import base64
import qrcode
from django.views.decorators.cache import never_cache
from django_tenants.utils import schema_context
from .forms import LoginForm
from .models import Utilisateur
from django.utils.translation import gettext as _
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


def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        totp_code = form.cleaned_data.get("totp_code")

        user = authenticate(request, email_google=email, password=password)

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
        if user.totp_enabled:
            if not totp_code:
                messages.error(request, _("Code TOTP requis"))
                return render(request, "login.html", {"form": form})

            if not user.verify_totp(totp_code):
                messages.error(request, _("Code TOTP invalide"))
                return render(request, "login.html", {"form": form})

        # ✅ Login final
        login(request, user)
        request.session["totp_verified"] = True
        return redirect("utilisateurs:dashboard")

    return render(request, "login.html", {"form": form})





def logout_view(request):
    logout(request)
    return redirect("utilisateurs:login")


@never_cache
@login_required
def dashboard_view(request):
    user = request.user
    societe = user.societe
    context = {}

    # --- Sécurité : récupère le tenant (la société de l'utilisateur) ---
    societe = request.user.societe
    schema_name = societe.schema_name  # pour django-tenants



    # --- Stats initialisées à zéro ---
    total_marques = total_moteurs = total_exemplaires = 0
    total_boites = total_embrayages = total_freins = 0
    total_freins_ar = total_pneus = total_maintenance = 0
    total_fournisseur = total_client_particulier = 0
    total_carrosserie = total_societe_cliente = 0
    total_adresse = total_assurance = total_modele = total_outils = 0
    total_recharge =  0

    marques = moteurs = exemplaires = boites = embrayages = freins = \
        freins_ar = pneus = maintenance = fournisseurs = client_particulier =\
        carrosseries = societe_cliente = adresse = assurance = \
        assurance_police = modele = outils = recharge = []

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
            carrosseries = Carrosserie.objects.filter(societe=societe)

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
            total_carrosserie = carrosseries.count()
            total_societe_cliente = societe_cliente.count()
            total_adresse = adresse.count()
            total_carburant = carburant.count()
            total_assurance = assurance.count()
            total_assurance_police = assurance_police.count()
            total_outils = outils.count()
            total_recharge = recharge.count()

            # Récupère les modèles existants pour les liens maintenance
            modeles = VoitureModele.objects.all()
    else:
        modeles = []

    context.update({
        'user': user,
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
        'total_carrosserie': total_carrosserie,
        'total_societe_cliente': total_societe_cliente,
        'total_adresse': total_adresse,
        'total_carburant': total_carburant,
        'total_assurance': total_assurance,
        'total_assurance_police': total_assurance_police,
        'total_outils': total_outils,
        'total_recharge': total_recharge,

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
        'carrosserie': carrosseries,
        'societe_cliente': societe_cliente,
        'adresse': adresse,
        'carburant': carburant,
        'assurance': assurance,
        'assurance_police': assurance_police,
        'outils': outils,
        'recharge': recharge,
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
        'apprenti': _("Apprenti"),
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

    return render(request, 'dashboard.html', context)







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
    if request.method == "POST":
        data = request.POST

        try:
            # 1. Création de l’adresse
            adresse = Adresse.objects.create(
                rue=data.get("rue"),
                numero=data.get("numero"),
                code_postal=data.get("code_postal"),
                ville=data.get("ville"),
                pays=data.get("pays"),
            )

            # 2. Création de l’utilisateur avec l’adresse créée
            user = Utilisateur.objects.create_user(
                email_google=data.get("email_google"),
                password=data.get("password"),
                nom=data.get("nom"),
                prenom=data.get("prenom"),
                role=data.get("role"),
                telephone=data.get("telephone") or None,
                email_entreprise=data.get("email_entreprise") or None,
                date_naissance=data.get("date_naissance") or None,
                schema_name=data.get("societe") or None,
                adresse=adresse,   # <-- objet directement
            )

            messages.success(request, _("Utilisateur créé avec succès."))
            return redirect("liste_utilisateurs")

        except Exception as e:
            messages.error(request, f"Erreur: {e}")

    return render(request, "utilisateurs/creer_utilisateur.html", {
        "roles": Utilisateur.ROLE_CHOICES
    })




def is_admin(user):
    return user.is_staff and user.is_superuser



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