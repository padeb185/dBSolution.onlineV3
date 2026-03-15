from django.urls import path
from .views import ElectriciteListView, ajouter_recharge_all, check_immatriculation, get_marques, get_modeles

app_name = "recharge"
from django.urls import path
from .views import (
    ElectriciteListView,
    ajouter_recharge_all,
    electricite_detail,
    modifier_electricite,
    check_immatriculation,
    get_marques,
    get_modeles,
)

app_name = "recharge"

urlpatterns = [
    path("recharge/", ElectriciteListView.as_view(), name="recharge_list"),

    path("recharge/formulaire/", ajouter_recharge_all, name="ajouter_recharge_all"),

    path(
        "recharge/<uuid:electricite_id>/",
        electricite_detail,
        name="electricite_detail",
    ),

    path(
        "recharge/<uuid:electricite_id>/modifier/",
        modifier_electricite,
        name="modifier_electricite",
    ),

    path("stats/", ElectriciteListView.as_view(), name="electricite_stat"),

    path("ajax/check-immatriculation/", check_immatriculation, name="check_immatriculation"),
    path("ajax/get-marques/", get_marques, name="get_marques"),
    path("ajax/get-modeles/", get_modeles, name="get_modeles"),
]