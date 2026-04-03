# voiture_freins_ar/urls.py
from django.urls import path
from .views import (
    liste_freins_ar,
    ajouter_freins_ar_simple,
    freins_ar_detail_view, 
    modifier_freins_ar_view,
)

app_name = "voiture_freins_ar"

urlpatterns = [
    # Freins arrière
    path("arriere/", liste_freins_ar, name="freins_ar_list"),

    path("arriere/ajouter/", ajouter_freins_ar_simple, name="ajouter_freins_ar_simple"),

    path("detail_arriere/<uuid:frein_ar_id>/", freins_ar_detail_view, name="detail_freins_ar"),

    path("modifier_arriere/<uuid:frein_ar_id>/", modifier_freins_ar_view , name="modifier_freins_ar"),
]