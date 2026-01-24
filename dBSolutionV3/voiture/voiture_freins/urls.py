from django.shortcuts import redirect
from django.urls import path
from .views import (
    liste_freins_ar,
    ajouter_freins_simple,
    ajouter_freins_ar_simple,
    freins_detail_view,
    freins_ar_detail_view, liste_freins,
)

app_name = "voiture_freins"

urlpatterns = [
    # Page principale → redirige vers avant par défaut
    path("", lambda request: redirect('voiture_freins:list'), name="list"),

    # Freins avant
    path("avant/", liste_freins, name="list"),
    path("avant/ajouter/", ajouter_freins_simple, name="ajouter_freins_simple"),
    path("avant/<uuid:frein_id>/", freins_detail_view, name="detail_freins"),

    # Freins arrière
    path("arriere/", liste_freins_ar, name="list_ar"),
    path("arriere/ajouter/", ajouter_freins_ar_simple, name="ajouter_freins_ar_simple"),
    path("arriere/<uuid:frein_ar_id>/", freins_ar_detail_view, name="detail_freins_ar"),
]
