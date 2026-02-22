from django.urls import path
from .views import ElectriciteListView, ajouter_recharge_all

app_name = "recharge"



urlpatterns = [
    path("recharge/", ElectriciteListView.as_view(), name="recharge_list"),

    path("recharge/formulaire/", ajouter_recharge_all, name="ajouter_recharge_all"),
]