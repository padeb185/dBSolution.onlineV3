from django.urls import path
from . import views
from .views import fuel_list, ajouter_fuel_all, fuel_detail, fuel_delete, check_immatriculation, get_marques, \
    get_modeles, modifier_fuel, FuelStatView

app_name = "fuel"

urlpatterns = [
    # Liste des fuels
    path("", fuel_list, name="fuel_list"),

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


    # Supprimer un fuel (UUID)
    path("delete/<uuid:fuel_id>/", fuel_delete, name="fuel_delete"),


    # Routes AJAX
    path("ajax/check-immatriculation/", check_immatriculation, name="check_immatriculation"),
    path("ajax/get-marques/", get_marques, name="get_marques"),
    path("ajax/get-modeles/", get_modeles, name="get_modeles"),
]

