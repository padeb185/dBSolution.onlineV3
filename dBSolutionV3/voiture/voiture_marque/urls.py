from django.urls import path
from . import views

app_name = "voiture_marque"

urlpatterns = [
    path(
        "",
        views.dashboard_voiture_view,
        name="dashboard_voiture",
    ),

    path(
        "marques/",
        views.marques_list_view,
        name="marques_list",
    ),

    path(
        "marque/<uuid:marque_id>/modeles/",
        views.modeles_par_marque,
        name="modeles_par_marque",
    ),

    path(
        "marques/<uuid:marque_id>/toggle-favorite/",
        views.toggle_marque_favorite,
        name="toggle_marque_favorite",
    ),

    path(
        "marques/favorites/",
        views.marques_favorites,
        name="marques_favorites",
    ),

    path(
        "ajouter/",
        views.ajouter_marque,
        name="ajouter_marque",
    ),

    path(
        "check-marque/",
        views.check_marque,
        name="check_marque",
    ),
]