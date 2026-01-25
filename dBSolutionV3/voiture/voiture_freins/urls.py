from django.shortcuts import redirect
from django.urls import path
from .views import liste_freins, ajouter_freins_simple, freins_detail_view

app_name = "voiture_freins"

urlpatterns = [
    path("", lambda request: redirect('voiture_freins:list'), name="list"),
    path("avant/", liste_freins, name="list"),
    path("avant/ajouter/", ajouter_freins_simple, name="ajouter_freins_simple"),
    path("avant/<uuid:frein_id>/", freins_detail_view, name="detail_freins"),
]
