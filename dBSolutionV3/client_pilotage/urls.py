from django.urls import path
from .views import ClientPilotageListView, client_pilotage_form_view, client_pilotage_detail_view, \
    modifier_client_pilotage_view
from client_particulier.views import check_prenom

app_name = "client_pilotage"


urlpatterns = [

    path(
        "client_pilotage",
        ClientPilotageListView.as_view(),
        name="client_pilotage_list",
    ),
    path(
        "creer/",
        client_pilotage_form_view,
        name="client_pilotage_form",
    ),


    path(
        "<int:client_pilotage_id>/",
        client_pilotage_detail_view,
        name="client_pilotage_detail"
    ),


    path(
        'client_pilotage/<int:client_pilotage_id>/modifier/',
        modifier_client_pilotage_view,
        name='modifier_client_pilotage'),


    path('api/check_prenom/', check_prenom, name='check_prenom'),

]
