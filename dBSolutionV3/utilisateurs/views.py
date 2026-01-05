from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from io import BytesIO
import base64
import qrcode

from .forms import LoginForm
from .models import Utilisateur


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
    return render(request, "dashboard.html", {
        "user": request.user
    })



def totp_setup_view(request):
    user_id = request.session.get("totp_setup_user")

    if not user_id:
        return redirect("utilisateurs:login")

    user = Utilisateur.objects.get(id=user_id)

    # ❌ Si déjà activé → dehors
    if user.totp_enabled:
        return redirect("utilisateurs:dashboard")

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
            request.session["totp_verified"] = True
            request.session.pop("totp_setup_user", None)

            return redirect("utilisateurs:dashboard")

        messages.error(request, "Code invalide")

    return render(request, "totp/setup.html", {
        "qr_code": qr_base64
    })
