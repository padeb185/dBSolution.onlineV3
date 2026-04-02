from django.shortcuts import redirect
from django.urls import path
from .views import (
    liste_freins,
    freins_detail_view,
    ajouter_freins_simple,
    dashboard_frein_view, modifier_freins_view
)

app_name = "voiture_freins"

urlpatterns = [
    path("", dashboard_frein_view, name="dashboard_frein"),

    path("avant/", liste_freins, name="freins_av_list"),

    path(
        "avant/ajouter/",
        ajouter_freins_simple,
        name="ajouter_freins_simple"
    ),

    path(
        "avant/<uuid:frein_id>/",
        freins_detail_view,
        name="freins_detail"
    ),

    path(
        "modifier_avant/<uuid:frein_id>/",
        modifier_freins_view,
        name="modifier_freins"
    ),
]




