# voiture/voiture_marque/urls.py
from django.urls import path
from .views import marque_list  # assure-toi que la vue existe et n’importe rien d’autre qui importe ce fichier urls

app_name = "voiture_marque"

urlpatterns = [
    path("", marque_list, name="liste"),
]
