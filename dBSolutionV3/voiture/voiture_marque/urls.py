from django.urls import path, include
from .views import marques_list, modeles_par_marque, toggle_marque_favorite, marques_favorites, ajouter_marque, \
    check_marque

app_name = "voiture_marque"

urlpatterns = [
    path("marques/", marques_list, name="marques_list"),
    path(
        "marque/<uuid:marque_id>/modeles/",
        modeles_par_marque,
        name="modeles_par_marque",
    ),

    path(
        "marques/<uuid:marque_id>/toggle-favorite/",
        toggle_marque_favorite,
        name="toggle_marque_favorite"
    ),
    path(
        "marques/favorites/",
        marques_favorites,
        name="marques_favorites"
    ),



    path("exemplaires/", include("voiture.voiture_exemplaire.urls")),

    path("ajouter/", ajouter_marque, name="ajouter_marque"),

    path('api/check_marque', check_marque, name='check_marque'),
]

