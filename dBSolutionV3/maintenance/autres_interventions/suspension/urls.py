from django.urls import path

from .views import dashboard_suspension_view

app_name = "suspension"

urlpatterns = [
    path("<uuid:exemplaire_id>/dashboard/", dashboard_suspension_view, name="dashboard_suspension"),
]
