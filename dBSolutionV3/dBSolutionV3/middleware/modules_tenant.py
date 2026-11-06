"""
Modules désactivés pour un tenant (Societe.modules, voir societe/modules.py) :
leurs URL renvoient vers le tableau de bord avec un message.
"""
import re

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _

LANGUES = "|".join(re.escape(code) for code, _nom in settings.LANGUAGES)
# /tenant/<schéma>/<langue>/<chemin relatif>
MOTIF = re.compile(rf"^/tenant/[^/]+/(?:{LANGUES})/(?P<chemin>.*)$")


def chemin_relatif(path):
    m = MOTIF.match(path or "")
    return m.group("chemin") if m else None


def societe_de(request):
    tenant = getattr(request, "tenant", None)
    if tenant is not None and hasattr(tenant, "modules"):
        return tenant
    user = getattr(request, "user", None)
    return getattr(user, "societe", None) if user is not None and user.is_authenticated else None


class ModulesTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        chemin = chemin_relatif(request.path)
        if chemin:
            societe = societe_de(request)
            if societe is not None and societe.modules is not None:
                from societe.modules import MODULES, module_de_chemin
                module = module_de_chemin(chemin)
                if module and module not in societe.modules:
                    messages.warning(request, _("Le module « %(module)s » n'est pas activé pour votre société.") % {
                        "module": MODULES[module][0]})
                    return redirect("utilisateurs:dashboard")
        return self.get_response(request)
