from django.urls import path
from .views import ClientParticulierListView, client_detail, check_prenom, \
    client_particulier_form_view, modifier_client_particulier_view

app_name = "client_particulier"


urlpatterns = [

    path(
        "client_particulier",
        ClientParticulierListView.as_view(),
        name="clientparticulier_list",
    ),
    path(
        "client_particulier/creer/",
        client_particulier_form_view,
        name="client_create",
    ),


    path(
        "<int:client_particulier_id>/",
        client_detail,
        name="client_detail"
    ),


    path(
        'client_particulier/<int:client_particulier_id>/modifier/',
        modifier_client_particulier_view,
        name='modifier_client_particulier'),


    path('api/check_prenom/', check_prenom, name='check_prenom'),

]
