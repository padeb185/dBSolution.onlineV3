
import pyotp

from django import forms
from django.contrib import messages
from django.contrib.auth import (
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import (
    get_language,
    gettext_lazy as _,
)
from django.views.decorators.cache import never_cache

from django_tenants.utils import (
    get_public_schema_name,
    schema_context,
)


Utilisateur = get_user_model()

PUBLIC_AUTH_BACKEND = (
    "utilisateurs.backends.PublicSchemaModelBackend"
)


# =====================================================
# FORMULAIRE TOTP
# =====================================================

class LoginTOTPForm(forms.Form):
    totp_token = forms.CharField(
        label=_("Code de sécurité"),
        max_length=6,
        min_length=6,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "one-time-code",
                "inputmode": "numeric",
                "pattern": "[0-9]*",
                "placeholder": "123456",
            }
        ),
    )

    def clean_totp_token(self):
        token = (
            self.cleaned_data.get("totp_token")
            or ""
        ).strip()

        if not token.isdigit():
            raise forms.ValidationError(
                _(
                    "Le code de sécurité doit contenir "
                    "uniquement des chiffres."
                )
            )

        if len(token) != 6:
            raise forms.ValidationError(
                _(
                    "Le code de sécurité doit contenir "
                    "exactement 6 chiffres."
                )
            )

        return token


# =====================================================
# OUTILS
# =====================================================

def get_langue_active():
    langue = (
        get_language()
        or "fr"
    ).split("-")[0].strip().lower()

    langues_autorisees = {
        "fr",
        "en",
        "de",
        "es",
        "it",
        "nl",
        "el",
    }

    if langue not in langues_autorisees:
        langue = "fr"

    return langue


def build_tenant_url(
    schema_name,
    langue,
    chemin,
):
    schema_name = (
        schema_name
        or ""
    ).strip().lower()

    langue = (
        langue
        or "fr"
    ).strip().lower()

    chemin = chemin.strip("/")

    return (
        f"/tenant/{schema_name}/"
        f"{langue}/{chemin}/"
    )


# =====================================================
# ACCUEIL
# =====================================================

def home(request):
    return render(
        request,
        "home.html",
    )


# =====================================================
# VALIDATION TOTP SÉPARÉE
# =====================================================

@never_cache
def login_totp(request):
    """
    Valide le code TOTP après la vérification préalable
    de l'adresse e-mail et du mot de passe.
    """

    user_id = request.session.get(
        "totp_login_user"
    )

    schema_name = (
        request.session.get(
            "totp_login_tenant"
        )
        or ""
    ).strip().lower()

    societe_id = request.session.get(
        "tenant_id"
    )

    if not user_id or not schema_name:
        messages.error(
            request,
            _(
                "La session de connexion a expiré. "
                "Veuillez vous reconnecter."
            ),
        )

        return redirect("/fr/connexion/")

    public_schema = (
        get_public_schema_name()
        or "public"
    )

    erreur = None
    user = None

    # -------------------------------------------------
    # Chargement de l'utilisateur depuis public
    # -------------------------------------------------

    with schema_context(public_schema):
        try:
            user = (
                Utilisateur.objects
                .select_related("societe")
                .get(pk=user_id)
            )

        except (
            Utilisateur.DoesNotExist,
            ValueError,
            TypeError,
        ):
            user = None

        if user is None:
            erreur = _(
                "Utilisateur introuvable."
            )

        elif not user.is_active:
            erreur = _(
                "Ce compte utilisateur est désactivé."
            )

        elif not user.societe_id:
            erreur = _(
                "Aucune société n'est liée "
                "à cet utilisateur."
            )

        elif (
            (
                user.societe.schema_name
                or ""
            ).strip().lower()
            != schema_name
        ):
            erreur = _(
                "La société de connexion "
                "ne correspond pas."
            )

        elif not user.totp_secret:
            erreur = _(
                "Aucun secret TOTP n'est configuré "
                "pour ce compte."
            )

        elif not user.totp_enabled:
            erreur = _(
                "Le TOTP n'est pas activé "
                "pour ce compte."
            )

    if erreur:
        request.session.flush()

        messages.error(
            request,
            erreur,
        )

        return redirect("/fr/connexion/")

    # -------------------------------------------------
    # Formulaire
    # -------------------------------------------------

    form = LoginTOTPForm(
        request.POST or None
    )

    if request.method == "POST" and form.is_valid():
        token = form.cleaned_data[
            "totp_token"
        ]

        with schema_context(public_schema):
            totp = pyotp.TOTP(
                user.totp_secret
            )

            code_valide = totp.verify(
                token,
                valid_window=1,
            )

        if code_valide:
            # -----------------------------------------
            # Connexion Django définitive
            # -----------------------------------------

            with schema_context(public_schema):
                login(
                    request,
                    user,
                    backend=PUBLIC_AUTH_BACKEND,
                )

            # login() renouvelle la session.
            # Ajouter ces données après login().
            request.session[
                "totp_verified"
            ] = True

            request.session[
                "totp_user_id"
            ] = str(user.pk)

            request.session[
                "tenant_id"
            ] = str(
                societe_id
                or user.societe_id
            )

            request.session[
                "tenant_schema"
            ] = schema_name

            if getattr(
                user.societe,
                "id_societe",
                None,
            ):
                request.session[
                    "tenant_uuid"
                ] = str(
                    user.societe.id_societe
                )

            request.session.pop(
                "totp_login_user",
                None,
            )

            request.session.pop(
                "totp_login_tenant",
                None,
            )

            request.session.modified = True
            request.session.save()

            langue = get_langue_active()

            destination = build_tenant_url(
                schema_name=schema_name,
                langue=langue,
                chemin="utilisateurs/dashboard",
            )

            print(
                "========== LOGIN TOTP DEBUG =========="
            )
            print(
                "UTILISATEUR :",
                user.email,
            )
            print(
                "AUTHENTIFIÉ :",
                request.user.is_authenticated,
            )
            print(
                "BACKEND :",
                request.session.get(
                    "_auth_user_backend"
                ),
            )
            print(
                "TENANT SESSION :",
                request.session.get(
                    "tenant_schema"
                ),
            )
            print(
                "DESTINATION :",
                destination,
            )
            print(
                "======================================"
            )

            messages.success(
                request,
                _("Connexion réussie."),
            )

            return redirect(destination)

        messages.error(
            request,
            _(
                "Le code de vérification est "
                "incorrect ou a expiré."
            ),
        )

    return render(
        request,
        "utilisateurs/login_totp.html",
        {
            "form": form,
        },
    )


# =====================================================
# DASHBOARD
# =====================================================

@never_cache
@login_required(login_url="/fr/connexion/")
def dashboard_view(request):
    from django.db import connection

    societe = getattr(request.user, "societe", None)

    print("========== DASHBOARD VIEW ==========")
    print("PATH :", request.path)
    print("SCHEMA :", connection.schema_name)
    print("AUTHENTICATED :", request.user.is_authenticated)
    print("USER :", request.user)
    print("USER ID :", getattr(request.user, "pk", None))
    print(
        "SOCIETE :",
        getattr(societe, "schema_name", None),
    )
    print(
        "SESSION TENANT :",
        request.session.get("tenant_schema"),
    )
    print(
        "TOTP VERIFIED :",
        request.session.get("totp_verified"),
    )
    print("====================================")


    user = request.user

    request_tenant = getattr(
        request,
        "tenant",
        None,
    )

    request_schema = (
        getattr(
            request_tenant,
            "schema_name",
            "",
        )
        or ""
    ).strip().lower()

    session_schema = (
        request.session.get(
            "tenant_schema"
        )
        or ""
    ).strip().lower()

    totp_enabled = bool(
        getattr(
            user,
            "totp_enabled",
            False,
        )
    )

    totp_verified = (
        request.session.get(
            "totp_verified"
        )
        is True
    )

    totp_user_id = str(
        request.session.get(
            "totp_user_id"
        )
        or ""
    )

    current_user_id = str(user.pk)

    validation_totp_correcte = (
        totp_enabled
        and totp_verified
        and totp_user_id == current_user_id
    )

    validation_tenant_correcte = (
        bool(request_schema)
        and bool(session_schema)
        and request_schema == session_schema
    )

    print(
        "========== DASHBOARD AUTH DEBUG =========="
    )
    print(
        "PATH :",
        request.path,
    )
    print(
        "USER :",
        user,
    )
    print(
        "AUTHENTICATED :",
        user.is_authenticated,
    )
    print(
        "USER ID :",
        current_user_id,
    )
    print(
        "USER SOCIETE ID :",
        getattr(
            user,
            "societe_id",
            None,
        ),
    )
    print(
        "SESSION KEY :",
        request.session.session_key,
    )
    print(
        "AUTH BACKEND :",
        request.session.get(
            "_auth_user_backend"
        ),
    )
    print(
        "REQUEST SCHEMA :",
        request_schema,
    )
    print(
        "SESSION SCHEMA :",
        session_schema,
    )
    print(
        "TOTP ENABLED :",
        totp_enabled,
    )
    print(
        "TOTP VERIFIED :",
        totp_verified,
    )
    print(
        "TOTP USER ID :",
        totp_user_id,
    )
    print(
        "TOTP CORRECT :",
        validation_totp_correcte,
    )
    print(
        "TENANT CORRECT :",
        validation_tenant_correcte,
    )
    print(
        "=========================================="
    )

    if not validation_tenant_correcte:
        logout(request)

        messages.error(
            request,
            _(
                "Vous n'êtes pas autorisé "
                "à accéder à cette société."
            ),
        )

        return redirect("/fr/connexion/")

    if not validation_totp_correcte:
        logout(request)

        messages.error(
            request,
            _(
                "Veuillez vous connecter avec votre "
                "adresse e-mail, votre mot de passe "
                "et votre code Authy."
            ),
        )

        return redirect("/fr/connexion/")

    return render(
        request,
        "dashboard.html",
        {
            "message": _(
                "Bienvenue sur ton tableau de bord"
            ),
        },
    )


# =====================================================
# DÉCONNEXION
# =====================================================

@login_required(login_url="/fr/connexion/")
def logout_view(request):
    logout(request)

    messages.success(
        request,
        _("Vous êtes maintenant déconnecté."),
    )

    # URL globale, sans préfixe tenant.
    return redirect("/fr/connexion/")
