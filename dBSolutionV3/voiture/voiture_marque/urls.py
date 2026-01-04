# voiture/voiture_marque/urls.py
from django.urls import path
from .views import marque_list, liste_marques, toggle_favori_marque

app_name = "voiture_marque"

urlpatterns = [
    # Page principale affichant toutes les marques
    path("", marque_list, name="liste"),  # /fr/voiture/marques/

    # Page affichant les voitures d'une marque spécifique
    path(
        "marque/<uuid:id_marque>/",
        liste_marques,
        name="liste_voitures_marque"
    ),

    path("marque/<uuid:marque_id>/favori/",
         toggle_favori_marque,
         name="toggle_favori_marque"),
]


