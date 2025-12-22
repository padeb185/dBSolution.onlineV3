from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from authentification.forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login
from django.utils.translation import gettext as _


@login_required
def home(request):
    message = _("Bienvenue sur notre site")
    return render(request, "home.html", {"message": message})



def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')  # redirige vers dashboard
            else:
                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})




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





def dashboard(request):
    message = _("Bienvenue sur ton tableau de bord")
    return render(request, 'dashboard.html', {'message': message})
