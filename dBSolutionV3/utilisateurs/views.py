import base64
from io import BytesIO
import qrcode
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext as _
import pyotp
from .forms import LoginTOTPForm




from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Utilisateur
from .forms import LoginForm
import pyotp

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = Utilisateur.objects.get(email_entreprise=email)
                if user.check_password(password):
                    # Stocke temporairement l'utilisateur pour l'étape TOTP
                    request.session['pre_2fa_user_id'] = str(user.id)
                    return redirect('totp_verify')
                else:
                    messages.error(request, "Mot de passe incorrect")
            except Utilisateur.DoesNotExist:
                messages.error(request, "Utilisateur introuvable")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})



from .forms import TOTPForm

def totp_verify_view(request):
    user_id = request.session.get('pre_2fa_user_id')
    if not user_id:
        return redirect('login')

    user = Utilisateur.objects.get(id=user_id)

    if request.method == "POST":
        form = TOTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['totp_code']
            if user.verify_totp(code):
                # Login réussi : stocke l'id en session
                request.session['user_id'] = str(user.id)
                del request.session['pre_2fa_user_id']
                return redirect('dashboard')
            else:
                messages.error(request, "Code Google Authenticator incorrect")
    else:
        form = TOTPForm()
    return render(request, "totp_verify.html", {"form": form})


def dashboard_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = Utilisateur.objects.get(id=user_id)
    return render(request, "dashboard.html", {"user": user})





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

