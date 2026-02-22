from django.urls import path
from .views import ElectriciteListView



app_name = "recharge"



urlpatterns = [
    path("recharge/", ElectriciteListView.as_view(), name="recharge_list"),
]