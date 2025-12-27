import base64
from io import BytesIO
import pyotp
import qrcode
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, TOTPLoginForm
from .models import CustomUser




def login_view(request):
    """
    Login principal : identifiant/mot de passe + TOTP si activé
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user:
                if user.totp_enabled:
                    # Stocker l'utilisateur dans la session temporaire
                    request.session['pre_2fa_user_id'] = str(user.id)
                    return redirect('login_totp')
                else:
                    login(request, user)
                    return redirect('dashboard')
            else:
                messages.error(request, "Identifiant ou mot de passe incorrect.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})



def login_totp(request):
    user_id = request.session.get('pre_2fa_user_id')
    if not user_id:
        return redirect('login')  # pas d'utilisateur en attente

    user = CustomUser.objects.get(id=user_id)
    message = None

    if request.method == "POST":
        form = TOTPLoginForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            totp = pyotp.TOTP(user.totp_secret)
            if totp.verify(token):
                login(request, user)  # connexion finale
                request.session.pop('pre_2fa_user_id', None)
                return redirect('dashboard')
            else:
                message = "Code TOTP invalide."
    else:
        form = TOTPLoginForm()

    return render(request, "login.totp.html", {"form": form, "message": message})





def totp_setup(request):
    user = request.user  # c'est un Utilisateur avec email_google

    if not user.totp_secret:
        user.generate_totp_secret()
        user.totp_enabled = True
        user.save(update_fields=['totp_secret', 'totp_enabled'])

    # Génération de l'URI TOTP
    totp_uri = pyotp.totp.TOTP(user.totp_secret).provisioning_uri(
        name=user.email_google,
        issuer_name="dBSolution"
    )

    # Création du QR code
    qr = qrcode.make(totp_uri)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(
        request,
        "totp/setup.html",
        {"qr_code": qr_base64}
    )