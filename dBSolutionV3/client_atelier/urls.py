from django.urls import path
from .views import check_prenom, ClientAtelierListView, client_atelier_form_view, client_atelier_detail_view, \
    modifier_client_atelier_view

app_name = "client_atelier"


urlpatterns = [
    path(
        "client_atelierr",
        ClientAtelierListView.as_view(),
        name="client_atelier_list",
    ),
    path(
        "client_particulier/creer/",
        client_atelier_form_view,
        name="client_atelier_form",
    ),


    path(
        "<int:client_particulier_id>/",
        client_atelier_detail_view,
        name="client_atelier_detail"
    ),


    path(
        'client_atelier/<int:client_atelier_id>/modifier/',
        modifier_client_atelier_view,
        name='modifier_client_atelier'),


    path('api/check_prenom/', check_prenom, name='check_prenom'),

]
