from django.urls import path
from .views import SocieteClienteListView, ajouter_societe_cliente_all, societe_cliente_detail, modifier_societe_cliente

app_name = "societe_cliente"


urlpatterns = [
    path(
        "societe_cliente",
        SocieteClienteListView.as_view(),
        name="societe_cliente_list",
    ),


    path(
        "societe_cliente/creer/",
        ajouter_societe_cliente_all,
        name="societe_cliente_create",
    ),


    path(
        "<int:societe_cliente_id>/",
        societe_cliente_detail,
        name="societe_cliente_detail"
    ),


    path(
        'societe_cliente/<int:client_id>/modifier/',
        modifier_societe_cliente,
        name='modifier_societe_cliente'),




]
