import base64
from io import BytesIO
import qrcode
import pyotp
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext as _
from .forms import LoginForm, LoginTOTPForm
from .models import CustomUser


def login_view(request):
    """Login avec email + mot de passe + TOTP"""
    form = LoginTOTPForm(request.POST or None)
    message = None

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data.get("email_google")
        password = form.cleaned_data.get("password")
        token = form.cleaned_data.get("totp_token")
        remember_me = form.cleaned_data.get("remember_me", False)

        user = authenticate(request, email_google=email, password=password)
        if user is None:
            message = _("Email ou mot de passe incorrect")
        else:
            if not getattr(user, "totp_secret", None):
                message = _("Utilisateur non configuré pour TOTP")
            else:
                totp = pyotp.TOTP(user.totp_secret)
                if not totp.verify(token):
                    message = _("Code TOTP invalide ou expiré")
                else:
                    # Connexion réussie
                    login(request, user)
                    if remember_me:
                        request.session.set_expiry(1209600)  # 2 semaines
                    else:
                        request.session.set_expiry(0)
                    return redirect("dashboard")

    return render(request, "login.html", {"form": form, "message": message})


def login_totp(request):
    """Étape TOTP si login en 2 étapes"""
    user_id = request.session.get('pre_2fa_user_id')
    if not user_id:
        return redirect('login')

    user = CustomUser.objects.get(id=user_id)
    message = None

    if request.method == "POST":
        form = (LoginTOTPForm(request.POST))
        if form.is_valid():
            token = form.cleaned_data['token']
            totp = pyotp.TOTP(user.totp_secret)
            if totp.verify(token):
                login(request, user)
                request.session.pop('pre_2fa_user_id', None)
                return redirect('dashboard')
            else:
                message = _("Code TOTP invalide ou expiré")
    else:
        form = LoginTOTPForm()

    return render(request, "login.totp.html", {"form": form, "message": message})


def totp_setup(request):
    """Page de configuration TOTP avec QR code"""
    user = request.user
    if not user.totp_secret:
        user.generate_totp_secret()
        user.totp_enabled = True
        user.save(update_fields=['totp_secret', 'totp_enabled'])

    # URI TOTP pour Google Authenticator
    totp_uri = pyotp.TOTP(user.totp_secret).provisioning_uri(
        name=user.email_google,
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
