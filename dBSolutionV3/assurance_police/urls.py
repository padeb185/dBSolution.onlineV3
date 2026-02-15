from django.urls import path
from .views import dashboard_assurances
app_name = "assurance_police"



urlpatterns = [
    path(
        "assurance/",
        dashboard_assurances,
        name="dashboard",
    ),
  ]