from django.urls import path
from .views import ElectriciteListView, ajouter_recharge_all, electricite_detail, modifier_electricite, \
    ElectriciteStatView, \
    ElectriciteExemplaireStatView, electricite_delete, autocomplete_immatriculation

app_name = "recharge"

urlpatterns = [

    path("stats/", ElectriciteStatView.as_view(), name="electricite_stat"),

    path("stats_exemplaire/<uuid:exemplaire_id>/", ElectriciteExemplaireStatView.as_view(), name="electricite_exemplaire_stat"),

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

    path(
        "recharge/<uuid:electricite_id>/delete/",
        electricite_delete,
        name="electricite_delete",
    ),

    path(
        "autocomplete-immatriculation/",
        autocomplete_immatriculation,
        name="autocomplete_immatriculation",
    ),
]