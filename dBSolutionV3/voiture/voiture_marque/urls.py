from django.urls import path
from .views import marque_list, toggle_favori_marque

app_name = "voiture_marque"

urlpatterns = [
    # Liste des marques
    path("", marque_list, name="list"),  # /voitures/marques/ => namespace 'voiture_marque:list'

    # Toggle favori pour une marque spécifique
    path("<uuid:id_marque>/favori/", toggle_favori_marque, name="toggle_favori_marque"),
]

