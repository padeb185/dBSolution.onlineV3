from django.urls import path

from .views import dashboard_bougies_view

app_name = "bougies"

urlpatterns = [
    path("<uuid:exemplaire_id>/dashboard/", dashboard_bougies_view, name="dashboard_bougies"),
]
