from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from io import BytesIO
import base64
import qrcode
from .forms import LoginForm
from .models import Utilisateur
from django.shortcuts import render
from django.utils.translation import gettext as _



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

    if user.role == 'apprenti':
        context['agenda'] = []
        context['taches'] = []
    elif user.role == 'mecanicien':
        # Les noms de tâches traduisibles
        context['agenda'] = []
        context['taches'] = [
            _("Révision moteur"),
            _("Changement filtre")
        ]
    elif user.role == 'carrossier':
        context['agenda'] = []
        context['taches'] = []
    elif user.role == 'chef_mecanicien':
        context['agenda'] = []
        context['taches'] = []
    elif user.role == 'magasinier':
        context['agenda'] = []
        context['taches'] = []
    elif user.role == 'instructeur':
        context['agenda'] = []
        context['taches'] = []
    elif user.role == 'instructeur_externe':
        context['agenda'] = []
        context['taches'] = []
    elif user.role == 'vendeur':
        context['agenda'] = []
        context['taches'] = []
    elif user.role == 'comptable':
        context['factures'] = 12
        context['depenses'] = 5
    elif user.role == 'direction':
        context['projets'] = 24
        context['utilisateurs'] = 128
    else:
        context['message'] = _("Rôle inconnu")  # traduction

    # Pour afficher le rôle de l'utilisateur en version traduite
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

