from django.urls import include, path

from .views import (
    ajouter_marque,
    check_marque,
    dashboard_voiture_view,
    marques_favorites,
    marques_list,
    modeles_par_marque,
    toggle_marque_favorite,
)

app_name = "voiture_marque"

urlpatterns = [
    path(
        "dashboard-voiture/",
        dashboard_voiture_view,
        name="dashboard_voiture",
    ),

    path(
        "marques/",
        marques_list,
        name="marques_list",
    ),

    path(
        "marque/<uuid:marque_id>/modeles/",
        modeles_par_marque,
        name="modeles_par_marque",
    ),

    path(
        "marques/<uuid:marque_id>/toggle-favorite/",
        toggle_marque_favorite,
        name="toggle_marque_favorite",
    ),

    path(
        "marques/favorites/",
        marques_favorites,
        name="marques_favorites",
    ),

    path(
        "exemplaires/",
        include("voiture.voiture_exemplaire.urls"),
    ),

    path(
        "ajouter/",
        ajouter_marque,
        name="ajouter_marque",
    ),

    path(
        "check-marque/",
        check_marque,
        name="check_marque",
    ),
]