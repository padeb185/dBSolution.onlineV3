from django.urls import path
from .views import ClientParticulierListView, ajouter_client_all, modifier_client, client_detail, check_prenom


app_name = "client_particulier"


urlpatterns = [

    path(
        "client_particulier",
        ClientParticulierListView.as_view(),
        name="clientparticulier_list",
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
        'client_particulier/<int:client_particulier_id>/modifier/',
        modifier_client,
        name='modifier_client'),


    path('api/check_prenom/', check_prenom, name='check_prenom'),

]
