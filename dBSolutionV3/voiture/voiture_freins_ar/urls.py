from django.shortcuts import redirect
from django.urls import path
from .views import (
    liste_freins_ar,
    ajouter_freins_ar_simple,
    freins_ar_detail_view,
)

app_name = "voiture_freins_ar"

urlpatterns = [
    # Page principale → redirige vers avant par défaut
    path("", lambda request: redirect('voiture_freins_ar:list_ar'), name="list_ar"),

    # Freins arrière
    path("arriere/", liste_freins_ar, name="list_ar"),
    path("arriere/ajouter/", ajouter_freins_ar_simple, name="ajouter_freins_ar_simple"),
    path("arriere/<uuid:frein_ar_id>/", freins_ar_detail_view, name="detail_freins_ar"),
]
