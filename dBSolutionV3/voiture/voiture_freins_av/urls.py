from django.shortcuts import redirect
from django.urls import path
from .views import (
    liste_freins_av,
    freins_av_detail_view,
    ajouter_freins_av_simple,
    dashboard_frein_view, modifier_freins_av_view
)

app_name = "voiture_freins_av"

urlpatterns = [
    path("", dashboard_frein_view, name="dashboard_frein"),

    path("avant/", liste_freins_av, name="freins_av_list"),

    path( "avant/ajouter/",  ajouter_freins_av_simple, name="ajouter_freins_simple"),

    path(
        'avant/<uuid:frein_av_id>/',
        freins_av_detail_view,
        name='freins_av_detail'
    ),

    path("modifier_avant/<uuid:frein_av_id>/", modifier_freins_av_view, name="modifier_freins_av"),
]




