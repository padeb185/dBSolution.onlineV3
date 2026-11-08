from django.urls import path

from . import admin_web

app_name = "particulier_admin"

urlpatterns = [
    path("", admin_web.tableau, name="tableau"),
    path("comptes/<uuid:pk>/", admin_web.compte, name="compte"),
    path("comptes/<uuid:pk>/activer/", admin_web.compte_activer, name="compte_activer"),
    path("comptes/<uuid:pk>/formule/", admin_web.compte_formule, name="compte_formule"),
    path("comptes/<uuid:pk>/supprimer/", admin_web.compte_supprimer, name="compte_supprimer"),
    path("monitoring/", admin_web.monitoring, name="monitoring"),
    path("monitoring/api/", admin_web.monitoring_api, name="monitoring_api"),
    path("fichiers/<str:modele>/<str:pk>/<str:champ>/", admin_web.fichier, name="fichier"),
]
