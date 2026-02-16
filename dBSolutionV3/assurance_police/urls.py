from django.urls import path
from .views import dashboard_assurances, AssurancePoliceListView

app_name = "assurance_police"

urlpatterns = [
    path("", AssurancePoliceListView.as_view(), name="assurance_police_list"),  # /assurance_police/
    path("dashboard/", dashboard_assurances, name="dashboard"),


]
