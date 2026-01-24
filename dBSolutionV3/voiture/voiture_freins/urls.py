from django.urls import path
from .views import liste_freins, ajouter_freins_simple, freins_detail_view

app_name = "voiture_freins"

urlpatterns = [

    path("", liste_freins, name="list"),


    path("ajouter/", ajouter_freins_simple, name="ajouter"),


    path("frein/<uuid:frein_id>/", freins_detail_view, name="detail"),
]
