from django.urls import path
from .views import ClientListView, ajouter_client_all, modifier_client, client_detail

app_name = "client"


urlpatterns = [
    path(
        "client",
        ClientListView.as_view(),
        name="client_list",
    ),
    path(
        "client/creer/",
        ajouter_client_all,
        name="client_create",
    ),


    path(
        "<int:client_id>/",
        client_detail,
        name="client_detail"
    ),


    path(
        'client/<int:client_id>/modifier/',
        modifier_client,
        name='modifier_client'),




]
