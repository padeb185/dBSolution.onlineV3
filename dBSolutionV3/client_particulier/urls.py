from django.urls import path
from .views import ClientParticulierListView, ajouter_client_all, modifier_client, client_detail

app_name = "client_particulier"


urlpatterns = [
    path(
        "client_particulier",
        ClientParticulierListView.as_view(),
        name="client_list",
    ),
    path(
        "client_particulier/creer/",
        ajouter_client_all,
        name="client_create",
    ),


    path(
        "<int:client_particulier_id>/",
        client_detail,
        name="client_detail"
    ),


    path(
        'client/<int:client_particulier_id>/modifier/',
        modifier_client,
        name='modifier_client'),




]
