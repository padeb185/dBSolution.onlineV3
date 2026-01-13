from django.urls import path, include
from utilisateurs.views import dashboard_view


urlpatterns = [
    path("", dashboard_view, name="dashboard"),

    # Moteurs
    path(
        "moteurs/",
        include(("voiture.voiture_moteur.urls", "voiture_moteur"), namespace="voiture_moteur")
    ),
]
