from django.urls import path, include
from utilisateurs.views import dashboard_view
from voiture.voiture_exemplaire.views import ajouter_exemplaire

urlpatterns = [
    path("", dashboard_view, name="dashboard"),

    # Marques de voiture
    path(
        "marques/",
        include(("voiture.voiture_marque.urls", "voiture_marque"), namespace="voiture_marque")
    ),

    # Exemplaires de voiture
    path(
        "exemplaires/",
        include(("voiture.voiture_exemplaire.urls", "voiture_exemplaire"), namespace="voiture_exemplaire")
    ),

    # Ajouter un exemplaire
    path(
        "modele/<uuid:modele_id>/ajouter/",
        ajouter_exemplaire,
        name="ajouter_exemplaire"
    ),

    # Moteurs
    path(
        "moteurs/",
        include(("voiture.voiture_moteur.urls", "voiture_moteur"), namespace="voiture_moteur")
    ),
]
