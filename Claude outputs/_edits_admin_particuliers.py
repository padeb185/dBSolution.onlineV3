"""Branchement de l'administration du tenant des particuliers (exécuté à la racine dBSolutionV3)."""

def maj(p, a, b):
    s = open(p, encoding="utf-8").read()
    if b in s:
        print("déjà fait", p); return
    assert s.count(a) == 1, (p, a[:70], s.count(a))
    open(p, "w", encoding="utf-8").write(s.replace(a, b)); print("ok", p)

maj("dBSolutionV3/urls.py",
    '''    path("voiture/ventes/", include(("voiture.voiture_vente.urls", "voiture_vente"), namespace="voiture_vente")),
''',
    '''    path("voiture/ventes/", include(("voiture.voiture_vente.urls", "voiture_vente"), namespace="voiture_vente")),

    # Administration du tenant des particuliers (comptes de l'application)
    path("particuliers/", include(("particulier.urls_admin", "particulier_admin"), namespace="particulier_admin")),
''')

maj("utilisateurs/views.py",
    '''    schema_name = getattr(societe, "schema_name", None)

    # --- Stats initialisées à zéro ---''',
    '''    schema_name = getattr(societe, "schema_name", None)

    # Tenant des particuliers : la direction arrive sur la gestion des comptes de l'application
    from django.conf import settings as _settings
    if schema_name == getattr(_settings, "PARTICULIERS_SCHEMA", "particuliers"):
        return redirect("particulier_admin:tableau")

    # --- Stats initialisées à zéro ---''')
