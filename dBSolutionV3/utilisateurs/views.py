from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    user = request.user
    context = {}

    # 👇 Récupération du nombre total de marques
    with schema_context(request.tenant.schema_name):
        context['total_marques'] = VoitureMarque.objects.count()
        total_marques = VoitureMarque.objects.count()
        context['total_moteurs'] = MoteurVoiture.objects.count()  # <-- Ici


    # Initialisation par défaut
    context['agenda'] = []
    context['taches'] = []

    # Gestion des tâches selon le rôle
    role_tasks = {
        'mecanicien': [
            _("Révision moteur"),
            _("Changement filtre")
        ],
        # tu peux ajouter d'autres rôles spécifiques ici
    }
    if user.role in role_tasks:
        context['taches'] = role_tasks[user.role]

    # Rôles avec des infos supplémentaires
    if user.role == 'comptable':
        context['factures'] = 12
        context['depenses'] = 5
    elif user.role == 'direction':
        context['projets'] = 24
        context['utilisateurs'] = 128

    # Message pour rôle inconnu
    if user.role not in role_tasks and user.role not in ['comptable', 'direction',
                                                       'apprenti', 'carrossier',
                                                       'chef_mecanicien',
                                                       'magasinier', 'instructeur',
                                                       'instructeur_externe',
                                                       'vendeur']:
        context['message'] = _("Rôle inconnu")

    # Rôle affiché (version traduite)
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
                "TOTP configuré avec succès. Vous pouvez maintenant vous connecter."
            )

            # 🔁 REDIRECTION VERS LOGIN
            return redirect("utilisateurs:login")

        messages.error(request, "Code invalide")

    return render(request, "totp/setup.html", {
        "qr_code": qr_base64
    })

