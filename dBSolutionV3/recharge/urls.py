from django.urls import path
from .views import  ElectriciteListView, ajouter_recharge_all, electricite_detail, modifier_electricite, check_immatriculation_elect, get_marques_elect,get_modeles_elect, ElectriciteStatView

app_name = "recharge"

urlpatterns = [

    path("stats/", ElectriciteStatView.as_view(), name="electricite_stat"),

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


    path("ajax/check-immatriculation_elect/", check_immatriculation_elect, name="check_immatriculation_elect"),
    path("ajax/get-marques_elect/", get_marques_elect, name="get_marques_elect"),
    path("ajax/get-modeles_elect/", get_modeles_elect, name="get_modeles_elect"),
]