import base64
from io import BytesIO
import qrcode
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext as _
import pyotp
from .forms import LoginTOTPForm




def login_view(request):
    """Login avec email + mot de passe + TOTP"""
    form = LoginTOTPForm(request.POST or None)
    message = None

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data.get("email_entreprise")
        password = form.cleaned_data.get("password")
        token = form.cleaned_data.get("totp_token")
        remember_me = form.cleaned_data.get("remember_me", False)

        # 🔑 Authentification
        utilisateur = authenticate(request, email_entreprise=email, password=password)
        if not utilisateur:
            message = _("Email ou mot de passe incorrect")
        else:
            if utilisateur.totp_enabled:
                # TOTP requis
                if not token or not pyotp.TOTP(utilisateur.totp_secret).verify(token):
                    message = _("Code TOTP invalide ou expiré")
                else:
                    # Connexion réussie
                    login(request, utilisateur)
                    request.session.set_expiry(1209600 if remember_me else 0)
                    return redirect("dashboard")
            else:
                # Aucun TOTP configuré → connexion directe
                login(request, utilisateur)
                request.session.set_expiry(1209600 if remember_me else 0)
                return redirect("dashboard")

    return render(request, "login_totp.html", {"form": form, "message": message})




def login_totp_view(request):
    """Login sécurisé obligatoire avec email + mot de passe + TOTP"""
    form = LoginTOTPForm(request.POST or None)
    message = None

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data.get("email_google")
        password = form.cleaned_data.get("password")
        token = form.cleaned_data.get("totp_token")
        remember_me = form.cleaned_data.get("remember_me", False)

        utilisateur = authenticate(request, email_google=email, password=password)
        if utilisateur is None:
            message = _("Email ou mot de passe incorrect")
        else:
            if not utilisateur.totp_secret:
                message = _("Utilisateur non configuré pour TOTP")
            else:
                import pyotp
                totp = pyotp.TOTP(utilisateur.totp_secret)
                if not token or not totp.verify(token):
                    message = _("Code TOTP invalide ou expiré")
                else:
                    login(request, utilisateur)
                    if remember_me:
                        request.session.set_expiry(1209600)  # 2 semaines
                    else:
                        request.session.set_expiry(0)
                    return redirect("dashboard")

    return render(request, "login_totp.html", {"form": form, "message": message})







def totp_setup(request):
    utilisateur = request.user
    if not utilisateur.totp_secret:
        utilisateur.generate_totp_secret()
        utilisateur.totp_enabled = True
        utilisateur.save(update_fields=['totp_secret', 'totp_enabled'])

    totp_uri = pyotp.TOTP(utilisateur.totp_secret).provisioning_uri(
        name=utilisateur.email_entreprise,
        issuer_name="dBSolution"
    )

    qr = qrcode.make(totp_uri)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "totp/setup.html", {"qr_code": qr_base64})

