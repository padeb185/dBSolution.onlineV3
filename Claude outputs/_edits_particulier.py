"""Modifications du projet pour l'espace particuliers (exécuté à la racine dBSolutionV3)."""
import re, sys

def maj(p, a, b, n=1):
    s = open(p, encoding="utf-8").read()
    if b in s:
        print("déjà fait", p); return
    assert s.count(a) == n, (p, a[:60], s.count(a))
    open(p, "w", encoding="utf-8").write(s.replace(a, b))

# settings
maj("dBSolutionV3/settings.py", "TENANT_APPS = (\n", "TENANT_APPS = (\n\n    # Espace particuliers (application Flutter, API /api/v1/)\n    'particulier',\n")
s = open("dBSolutionV3/settings.py", encoding="utf-8").read()
if "PARTICULIERS_SCHEMA" not in s:
    s += '''

# ------------------------------------------------------------------------------
# ESPACE PARTICULIERS (application Flutter) – voir particulier/
# ------------------------------------------------------------------------------
# Tenant partagé par tous les particuliers (données filtrées par propriétaire)
PARTICULIERS_SCHEMA = env("PARTICULIERS_SCHEMA", default="particuliers")

REST_FRAMEWORK = {
    # Montants en nombres JSON (et non en chaînes) pour l'application
    "COERCE_DECIMAL_TO_STRING": False,
    # Par défaut, aucune API n'est ouverte : chaque vue déclare son authentification
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
}
'''
    open("dBSolutionV3/settings.py", "w", encoding="utf-8").write(s)

# urls : API hors i18n (pas de préfixe de langue)
maj("dBSolutionV3/urls.py", '''urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]''', '''urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    # API de l'application particuliers (Flutter) – jeton, sans session ni préfixe de langue
    path("api/v1/", include(("particulier.api.urls", "api_particulier"), namespace="api_particulier")),
]''')

# middlewares : l'API n'utilise pas la session
for p in ("dBSolutionV3/middleware/tenant_required.py", "utilisateurs/middleware.py"):
    s = open(p, encoding="utf-8").read()
    n = s.count('        "/i18n/",\n    )')
    s2 = s.replace('        "/i18n/",\n    )', '        "/i18n/",\n        "/api/",\n    )')
    if '"/api/"' not in s:
        open(p, "w", encoding="utf-8").write(s2); print(p, n, "exclusions /api/")

# rôle particulier
maj("utilisateurs/models.py", "        ('direction', _('Direction')),\n    ]",
    "        ('direction', _('Direction')),\n        ('particulier', _('Particulier (application)')),\n    ]")
