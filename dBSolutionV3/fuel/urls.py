from django.urls import path
from . import views
from .views import fuel_list, ajouter_fuel_all, fuel_detail, fuel_delete, check_immatriculation, get_marques, \
    get_modeles

app_name = "fuel"

urlpatterns = [
    # Liste des fuels
    path("", fuel_list, name="fuel_list"),

    # Ajouter un fuel
    path("fuel/creer/", ajouter_fuel_all, name="ajouter_fuel_all"),

    # Détail d'un fuel (UUID)
    path("<uuid:fuel_id>/", fuel_detail, name="fuel_detail"),


    # Supprimer un fuel (UUID)
    path("delete/<uuid:fuel_id>/", fuel_delete, name="fuel_delete"),


    # Routes AJAX
    path("ajax/check-immatriculation/", check_immatriculation, name="check_immatriculation"),
    path("ajax/get-marques/", get_marques, name="get_marques"),
    path("ajax/get-modeles/", get_modeles, name="get_modeles"),
]

