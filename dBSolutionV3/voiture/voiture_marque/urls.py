from django.urls import path
from . import views

app_name = "voiture_marque"

urlpatterns = [
    path("marques/", views.marques_list, name="marques_list"),
    path(
        "marque/<uuid:marque_id>/modeles/",
        views.modeles_par_marque,
        name="modeles_par_marque",
    ),
]

