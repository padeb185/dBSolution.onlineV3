from django.urls import path

from .views import (
    ClientAtelierListView,
    check_prenom,
    client_atelier_detail_view,
    client_atelier_form_view,
    dashboard_client_view,
    modifier_client_atelier_view,
)

app_name = "client_atelier"

urlpatterns = [
    path(
        "",
        dashboard_client_view,
        name="dashboard_client",
    ),

    path(
        "liste/",
        ClientAtelierListView.as_view(),
        name="client_atelier_list",
    ),

    path(
        "creer/",
        client_atelier_form_view,
        name="client_atelier_form",
    ),

    path(
        "api/check-prenom/",
        check_prenom,
        name="check_prenom",
    ),

    path(
        "<int:client_atelier_id>/",
        client_atelier_detail_view,
        name="client_atelier_detail",
    ),

    path(
        "<int:client_atelier_id>/modifier/",
        modifier_client_atelier_view,
        name="modifier_client_atelier",
    ),
]