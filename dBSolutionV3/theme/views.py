import pyotp
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.cache import never_cache
from utilisateurs.forms import LoginForm
from utilisateurs.models import UserLog


def home(request):
    return render(request, 'home.html')







def login_view(request):
    """
    Ancienne vue de connexion conservée temporairement
    pour rediriger vers la connexion globale.
    """
    return redirect("/fr/connexion/")



class LoginTOTPForm:
    pass


from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django_tenants.utils import schema_context

import pyotp

Utilisateur = get_user_model()


@never_cache
def login_totp(request):
    """Validation du code TOTP après le mot de passe."""

    user_id = request.session.get("totp_login_user")
    schema_name = request.session.get("totp_login_tenant")
    societe_id = request.session.get("tenant_id")

    if not user_id or not schema_name:
        messages.error(
            request,
            _("La session de connexion a expiré. Reconnectez-vous."),
        )
        return redirect("/fr/connexion/")

    with schema_context("public"):
        try:
            user = (
                Utilisateur.objects
                .select_related("societe")
                .get(pk=user_id)
            )
        except Utilisateur.DoesNotExist:
            user = None

        if user is None:
            erreur = _("Utilisateur introuvable.")

        elif not user.is_active:
            erreur = _("Ce compte utilisateur est désactivé.")

        elif not user.societe_id:
            erreur = _("Aucune société n'est liée à cet utilisateur.")

        elif user.societe.schema_name != schema_name:
            erreur = _("La société de connexion ne correspond pas.")

        elif not user.totp_secret:
            erreur = _("Aucun secret TOTP configuré pour ce compte.")

        else:
            erreur = None

    if erreur:
        request.session.flush()
        messages.error(request, erreur)
        return redirect("/fr/connexion/")

    message = None

    if request.method == "POST":
        form = LoginTOTPForm(request.POST)

        if form.is_valid():
            token = form.cleaned_data["totp_token"].strip()

            with schema_context("public"):
                totp = pyotp.TOTP(user.totp_secret)

                # valid_window=1 accepte un léger décalage horaire
                code_valide = totp.verify(
                    token,
                    valid_window=1,
                )

            if code_valide:
                # Connexion Django définitive
                login(request, user)

                request.session["totp_verified"] = True
                request.session["totp_user_id"] = str(user.pk)
                request.session["tenant_id"] = (
                    societe_id or str(user.societe_id)
                )
                request.session["tenant_schema"] = schema_name

                # Nettoyage des variables temporaires
                request.session.pop("totp_login_user", None)
                request.session.pop("totp_login_tenant", None)

                request.session.modified = True

                langue = get_language() or "fr"

                return redirect(
                    f"/tenant/{schema_name}/"
                    f"{langue}/utilisateurs/dashboard/"
                )

            message = _("Code de vérification invalide.")

    else:
        form = LoginTOTPForm()

    return render(
        request,
        "utilisateurs/login_totp.html",
        {
            "form": form,
            "message": message,
        },
    )



from django.contrib.auth import logout



@never_cache
@login_required(login_url="/fr/connexion/")
def dashboard(request):
    """
    Tableau de bord utilisateur.

    L'accès est autorisé uniquement si :
    - l'utilisateur est authentifié ;
    - le TOTP est configuré ;
    - le code TOTP a été validé pendant cette connexion ;
    - la validation correspond bien à cet utilisateur.
    """

    user = request.user

    totp_enabled = bool(
        getattr(user, "totp_enabled", False)
    )

    totp_verified = (
        request.session.get("totp_verified") is True
    )

    totp_user_id = request.session.get("totp_user_id")

    validation_correcte = (
        totp_enabled
        and totp_verified
        and totp_user_id == str(user.pk)
    )

    if not validation_correcte:
        logout(request)

        messages.error(
            request,
            _(
                "Veuillez vous connecter avec votre adresse e-mail, "
                "votre mot de passe et votre code Authy."
            ),
        )

        return redirect("/fr/connexion/")

    message = _("Bienvenue sur ton tableau de bord")

    return render(
        request,
        "dashboard.html",
        {
            "message": message,
        },
    )





@login_required
def logout_view(request):
    auth_logout(request)
    return redirect("login")
