from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginTOTPForm
from .models import Utilisateur
import base64
from io import BytesIO
import qrcode
import pyotp
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext as _
from .forms import LoginTOTPForm


def login_view(request):
    """Login avec email + mot de passe + TOTP"""
    form = LoginTOTPForm(request.POST or None)
    message = None

    if request.method == "POST" and form.is_valid():
        email_google = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        token = form.cleaned_data.get("totp_token")
        remember_me = form.cleaned_data.get("remember_me", False)

        # 🔑 Authentification
        utilisateur = authenticate(request, email_google=email_google, password=password)
        if utilisateur is None:
            message = _("Email ou mot de passe incorrect")
        else:
            if not getattr(utilisateur, "totp_secret", None):
                message = _("Utilisateur non configuré pour TOTP")
            else:
                totp = pyotp.TOTP(utilisateur.totp_secret)
                if not token or not totp.verify(token):
                    message = _("Code TOTP invalide ou expiré")
                else:
                    # Connexion réussie
                    login(request, utilisateur)
                    if remember_me:
                        request.session.set_expiry(1209600)  # 2 semaines
                    else:
                        request.session.set_expiry(0)
                    return redirect("dashboard")

    return render(request, "login.html", {"form": form, "message": message})


def login_totp(request):
    """Étape TOTP si login en 2 étapes"""
    utilisateur_id = request.session.get('pre_2fa_user_id')
    if not utilisateur_id:
        return redirect('login')

    utilisateur = CustomUser.objects.get(id=utilisateur_id)
    message = None

    if request.method == "POST":
        form = (LoginTOTPForm(request.POST))
        if form.is_valid():
            token = form.cleaned_data['token']
            totp = pyotp.TOTP(utilisateur.totp_secret)
            if totp.verify(token):
                login(request, utilisateur)
                request.session.pop('pre_2fa_user_id', None)
                return redirect('dashboard')
            else:
                message = _("Code TOTP invalide ou expiré")
    else:
        form = LoginTOTPForm()

    return render(request, "login.totp.html", {"form": form, "message": message})


def totp_setup(request):
    """Page de configuration TOTP avec QR code"""
    utilisateur = request.utilisateur
    if not utilisateur.totp_secret:
        utilisateur.generate_totp_secret()
        utilisateur.totp_enabled = True
        utilisateur.save(update_fields=['totp_secret', 'totp_enabled'])

    # URI TOTP pour Google Authenticator
    totp_uri = pyotp.TOTP(utilisateur.totp_secret).provisioning_uri(
        name=utilisateur.email_google,
        issuer_name="dBSolution"
    )

    # Génération QR code
    qr = qrcode.make(totp_uri)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(
        request,
        "totp/setup.html",
        {"qr_code": qr_base64}
    )


def login_totp_view(request):
    form = LoginTOTPForm(request.POST or None)
    message = ""

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data['email_google']
        password = form.cleaned_data['password']
        token = form.cleaned_data['totp_token']

        user = authenticate(request, email_google=email, password=password)
        if user is not None:
            if user.verify_totp(token):
                login(request, user)
                return redirect('home')  # page d'accueil après connexion
            else:
                message = "Code TOTP incorrect"
        else:
            message = "Email ou mot de passe incorrect"

    return render(request, 'login_totp.html', {'form': form, 'message': message})
