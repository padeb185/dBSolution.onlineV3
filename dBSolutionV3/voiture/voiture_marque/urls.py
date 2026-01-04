# voiture/voiture_marque/urls.py
from django.urls import path
from .views import marque_list, toggle_favori_marque

app_name = "voiture_marque"

urlpatterns = [
    path("", marque_list, name="liste"),
    path(
        "marque/<int:marque_id>/favori/",
        toggle_favori_marque,
        name="toggle_favori_marque"
    ),

]



