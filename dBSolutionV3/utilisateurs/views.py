from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import LoginForm
import qrcode
from io import BytesIO
import base64
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Utilisateur
from django.contrib.auth.decorators import login_required



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

            request.session["totp_setup_user"] = user.id
            return redirect("totp_setup")

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
        request.session["totp_verified"] = True  # 🔑 TRÈS IMPORTANT
        return redirect("dashboard")

    return render(request, "login.html", {"form": form})






@login_required
def dashboard_view(request):
    return render(request, "dashboard.html", {
        "user": request.user
    })




def totp_setup_view(request):
    user_id = request.session.get("totp_setup_user")

    if not user_id:
        return redirect("login")

    user = Utilisateur.objects.get(id=user_id)

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

            login(request, user)
            request.session["totp_verified"] = True  # 🔑 AJOUT DEMANDÉ

            request.session.pop("totp_setup_user", None)
            return redirect("dashboard")

    return render(request, "totp/setup.html", {
        "qr_code": qr_base64
    })
