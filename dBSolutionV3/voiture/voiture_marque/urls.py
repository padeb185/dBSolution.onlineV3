from django.urls import path
from .views import marques_list, modeles_par_marque

app_name = "voiture_marque"

urlpatterns = [
    path("marques/", marques_list, name="marques_list"),
    path(
        "marque/<uuid:marque_id>/modeles/",
        modeles_par_marque,
        name="modeles_par_marque",
    ),
]

