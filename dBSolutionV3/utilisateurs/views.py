from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from io import BytesIO
import base64
import qrcode
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



def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        totp_code = form.cleaned_data.get("totp_code")

        user = authenticate(request, email_google=email, password=password)

        if not user:
            messages.error(request, "Email ou mot de passe incorrect")
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
                messages.error(request, "Code TOTP requis")
                return render(request, "login.html", {"form": form})

            if not user.verify_totp(totp_code):
                messages.error(request, "Code TOTP invalide")
                return render(request, "login.html", {"form": form})

        # ✅ Login final
        login(request, user)
        request.session["totp_verified"] = True
        return redirect("utilisateurs:dashboard")

    return render(request, "login.html", {"form": form})





def logout_view(request):
    logout(request)
    return redirect("utilisateurs:login")






@login_required
def dashboard_view(request):
    total_moteurs = MoteurVoiture.objects.count()
    moteurs = MoteurVoiture.objects.all()

    total_marques = VoitureMarque.objects.count()
    marques = VoitureMarque.objects.all()

    total_exemplaires = VoitureExemplaire.objects.count()
    exemplaires = VoitureExemplaire.objects.all()

    total_boites = VoitureBoite.objects.count()
    boites = VoitureBoite.objects.all()

    total_embrayages = VoitureEmbrayage.objects.count()
    embrayages = VoitureEmbrayage.objects.all()

    user = request.user
    context = {}


    # --- Sécurité : vérifie que request.tenant existe ---
    tenant_schema = getattr(request, 'tenant', None)
    if tenant_schema:
        schema_name = tenant_schema.schema_name
    else:
        schema_name = None

    # --- Récupération des stats ---
    total_marques = 0
    total_moteurs = 0
    total_exemplaires = 0
    total_boites = 0
    total_embrayages = 0
    if schema_name:
        with schema_context(schema_name):
            total_marques = VoitureMarque.objects.count()
            total_moteurs = MoteurVoiture.objects.count()
            total_exemplaires = VoitureExemplaire.objects.count()
            total_boites = VoitureBoite.objects.count()
            total_embrayages = VoitureEmbrayage.objects.count()

    context['total_marques'] = total_marques
    context['total_moteurs'] = total_moteurs
    context['total_exemplaires'] = total_exemplaires
    context['total_boites'] = total_boites
    context['total_embrayages'] = total_embrayages

    # --- Initialisation par défaut ---
    context['agenda'] = []
    context['taches'] = []

    # --- Tâches selon rôle ---
    role_tasks = {
        'mecanicien': [_("Révision moteur"), _("Changement filtre")],
        # autres rôles
    }
    if user.role in role_tasks:
        context['taches'] = role_tasks[user.role]

    # --- Infos supplémentaires selon rôle ---
    if user.role == 'comptable':
        context['factures'] = 12
        context['depenses'] = 5
    elif user.role == 'direction':
        context['projets'] = 24
        context['utilisateurs'] = 128

    # Message pour rôle inconnu
    if user.role not in role_tasks and user.role not in [
        'comptable', 'direction', 'apprenti', 'carrossier',
        'chef_mecanicien', 'magasinier', 'instructeur',
        'instructeur_externe', 'vendeur'
    ]:
        context['message'] = _("Rôle inconnu")

    # --- Affichage traduit du rôle ---
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

    # --- DEBUG (optionnel) ---
    # print("Dashboard stats:", context['total_marques'], context['total_moteurs'])

    return render(request, 'dashboard.html', {
        'total_moteurs': total_moteurs,
        'moteurs': moteurs,
        'total_marques': total_marques,
        'marques': marques,
        'total_exemplaires': total_exemplaires,
        'exemplaires': exemplaires,
        'total_boites': total_boites,
        'boites': boites,
        'total_embrayages': total_embrayages,
        'embrayages': embrayages,

    })





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
                "TOTP configuré avec succès. Vous pouvez maintenant vous connecter."
            )

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

            messages.success(request, "Utilisateur créé avec succès.")
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