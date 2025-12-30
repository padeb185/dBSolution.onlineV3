import pyotp
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from utilisateurs.forms import LoginForm, LoginTOTPForm


def home(request):
    return render(request, 'home.html')


def login_view(request):
    """Vue pour la connexion classique"""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email_google']
            password = form.cleaned_data['password']

            user = authenticate(request, email_google=email, password=password)

            if user is not None:
                auth_login(request, user)

                # Réinitialiser la vérification TOTP
                request.session["totp_verified"] = False

                # Rediriger vers la page TOTP si activé
                if getattr(user, "totp_enabled", False):
                    return redirect("login_totp")
                else:
                    return redirect("dashboard")
            else:
                form.add_error(None, _("Nom d'utilisateur ou mot de passe incorrect"))
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


@login_required
def login_totp(request):
    """Validation du code TOTP (Google Authenticator)"""
    user = request.user
    message = None

    # Vérifie que l'utilisateur a un secret TOTP
    if not getattr(user, "totp_secret", None):
        message = _("Aucun secret TOTP configuré pour ce compte.")
        return render(request, "login.totp.html", {"form": None, "message": message})

    if request.method == "POST":
        form = LoginTOTPForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data["totp_token"]
            totp = pyotp.TOTP(user.totp_secret)

            if totp.verify(token):
                # Marquer la 2FA comme validée
                request.session["totp_verified"] = True
                return redirect("dashboard")
            else:
                message = _("Code de vérification invalide.")
    else:
        form = LoginTOTPForm(initial={"email_google": user.email_google})

    return render(request, "login.totp.html", {"form": form, "message": message})


@login_required
def dashboard(request):
    """Tableau de bord utilisateur"""
    if getattr(request.user, "totp_enabled", False) and not request.session.get("totp_verified", False):
        return redirect("login_totp")

    message = _("Bienvenue sur ton tableau de bord")
    return render(request, 'dashboard.html', {'message': message})


@login_required
def logout_view(request):
    """Déconnexion de l'utilisateur"""
    auth_logout(request)
    return redirect("login")
