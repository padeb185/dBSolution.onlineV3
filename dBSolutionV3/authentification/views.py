import pyotp
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from .forms import TOTPLoginForm
import qrcode
import base64
from io import BytesIO






@login_required
def login_totp(request):
    """
    Validation du code TOTP (Google Authenticator)
    """

    user = request.user
    message = None

    # Sécurité : vérifier que l'utilisateur a bien un secret TOTP
    if not hasattr(user, "totp_secret") or not user.totp_secret:
        message = _("Aucun secret TOTP configuré pour ce compte.")
        return render(
            request,
            "login.totp.html",
            {"form": None, "message": message},
        )

    if request.method == "POST":
        form = TOTPLoginForm(request.POST)

        if form.is_valid():
            token = form.cleaned_data["token"]

            totp = pyotp.TOTP(user.totp_secret)

            if totp.verify(token):
                # Marquer la 2FA comme validée
                request.session["totp_verified"] = True

                # Reconnecter proprement l'utilisateur
                login(request, user)

                return redirect("dashboard")  # ou admin:index
            else:
                message = _("Code de vérification invalide.")

    else:
        form = TOTPLoginForm()

    return render(
        request,
        "login.totp.html",
        {
            "form": form,
            "message": message,
        },
    )



@login_required
def totp_setup(request):
    user = request.user

    if not user.totp_secret:
        user.generate_totp_secret()  # Méthode du modèle

    uri = user.get_totp_uri()       # Méthode du modèle pour provisioning URI

    qr = qrcode.make(uri)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(
        request,
        "totp/setup.html",
        {"qr_code": qr_base64},
    )
