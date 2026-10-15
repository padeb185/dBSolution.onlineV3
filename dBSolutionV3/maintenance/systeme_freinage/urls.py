from django.urls import path

from .views import dashboard_freinage_view

app_name = "systeme_freinage"

urlpatterns = [
    path(
        "<uuid:exemplaire_id>/dashboard/",
        dashboard_freinage_view,
        name="dashboard_freinage",
    ),
]
