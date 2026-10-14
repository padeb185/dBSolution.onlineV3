from django.urls import path

from .views import dashboard_esthetique_view

app_name = "esthetique"

urlpatterns = [
    path(
        "<uuid:exemplaire_id>/dashboard/",
        dashboard_esthetique_view,
        name="dashboard_esthetique",
    ),
]
