from django.urls import path
from .views import dashboard_assurances


app_name = "assurance_police"



urlpatterns = [
    path(
        "assurance_police/",
        dashboard_assurances,
        name="dashboard",
    ),
   ]