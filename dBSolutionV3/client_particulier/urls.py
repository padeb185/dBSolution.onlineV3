from django.urls import path

from .views import (
    ClientParticulierListView,
    check_prenom,
    client_detail,
    client_particulier_form_view,
    modifier_client_particulier_view,
)

app_name = "client_particulier"

urlpatterns = [
    path(
        "",
        ClientParticulierListView.as_view(),
        name="clientparticulier_list",
    ),

    path(
        "creer/",
        client_particulier_form_view,
        name="client_create",
    ),

    path(
        "api/check-prenom/",
        check_prenom,
        name="check_prenom",
    ),

    path(
        "<int:client_particulier_id>/",
        client_detail,
        name="client_detail",
    ),

    path(
        "<int:client_particulier_id>/modifier/",
        modifier_client_particulier_view,
        name="modifier_client_particulier",
    ),
]