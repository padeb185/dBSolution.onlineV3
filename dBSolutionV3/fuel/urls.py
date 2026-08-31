from django.urls import path
from . import views
from .views import ajouter_fuel_all, fuel_delete,  modifier_fuel, FuelStatView, FuelExemplaireStatView, FuelListView

app_name = "fuel"

urlpatterns = [
    # Liste des fuels
    path(
        "",
        FuelListView.as_view(),
        name="fuel_list",
    ),

    # Ajouter un fuel
    path("formulaire/", ajouter_fuel_all, name="ajouter_fuel_all"),

    # Détail d'un fuel (UUID)
    path("detail/<int:fuel_id>/", views.fuel_detail, name="fuel_detail"),


    path(
        '<int:fuel_id>/modifier/',
        modifier_fuel,
        name='modifier_fuel'
    ),

    path("stats/", FuelStatView.as_view(), name="fuel_stat"),

    # après
    path("stats_exemplaire/<uuid:exemplaire_id>/", FuelExemplaireStatView.as_view(), name="fuel_exemplaire_stat"),

    path(
        "delete/<int:fuel_id>/",
        views.fuel_delete,
        name="fuel_delete"
     ),


    path(
        "autocomplete-immatriculation/",
        views.autocomplete_immatriculation,
        name="autocomplete_immatriculation",
    ),
]

