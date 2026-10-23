"""
Vérification des identifiants en AJAX sur la page de connexion :
indique si l'e-mail et le mot de passe sont corrects et si l'utilisateur
a un TOTP configuré (le champ « code TOTP » n'est alors affiché qu'à ce moment).

Protection contre le brute-force : nombre d'essais limité par adresse IP
et par e-mail (cache Django).
"""
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django_tenants.utils import get_public_schema_name, schema_context

from .models import Utilisateur

MAX_ESSAIS = 10            # essais incorrects autorisés…
FENETRE_SECONDES = 15 * 60  # …par période de 15 minutes


def _ip(request):
    transmis = request.META.get("HTTP_X_FORWARDED_FOR", "")
    return (transmis.split(",")[0].strip() if transmis else request.META.get("REMOTE_ADDR", "")) or "inconnue"


def _cles(request, email):
    return [f"connexion_essais_ip_{_ip(request)}", f"connexion_essais_email_{email}"]


def _bloque(cles):
    return any((cache.get(c) or 0) >= MAX_ESSAIS for c in cles)


def _echec(cles):
    for c in cles:
        try:
            cache.incr(c)
        except ValueError:
            cache.set(c, 1, FENETRE_SECONDES)


@never_cache
@require_POST
def verifier_identifiants(request):
    email = (request.POST.get("email") or "").strip().lower()
    password = request.POST.get("password") or ""

    if not email or not password:
        return JsonResponse({"ok": False, "totp": False, "message": ""})

    cles = _cles(request, email)
    if _bloque(cles):
        return JsonResponse({
            "ok": False, "totp": False, "bloque": True,
            "message": _("Trop de tentatives. Réessayez dans quelques minutes."),
        }, status=429)

    with schema_context(get_public_schema_name() or "public"):
        utilisateur = (
            Utilisateur.objects.filter(email__iexact=email).only(
                "id", "password", "is_active", "totp_enabled", "totp_secret", "societe_id"
            ).first()
        )
        ok = bool(utilisateur and utilisateur.check_password(password))

    if not ok:
        _echec(cles)
        return JsonResponse({
            "ok": False, "totp": False,
            "message": _("Adresse e-mail ou mot de passe incorrect."),
        })

    if not utilisateur.is_active:
        return JsonResponse({"ok": False, "totp": False, "message": _("Ce compte utilisateur est désactivé.")})

    totp = bool(utilisateur.totp_enabled and utilisateur.totp_secret)
    return JsonResponse({
        "ok": True,
        "totp": totp,
        "message": "" if totp else _(
            "Première connexion : vous configurerez votre code TOTP à l'étape suivante."
        ),
    })
