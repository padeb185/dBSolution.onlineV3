from django.urls import path
from .views import SocieteClienteListView, ajouter_societe_cliente_all, societe_cliente_detail, modifier_societe_cliente

app_name = "societe_cliente"

urlpatterns = [
    # Liste des sociétés clientes
    path("", SocieteClienteListView.as_view(), name="societe_cliente_list"),

    # Créer une société cliente
    path("creer/", ajouter_societe_cliente_all, name="societe_cliente_form"),

    # Détail d’une société cliente
    path("<uuid:societe_cliente_id>/", societe_cliente_detail, name="societe_cliente_detail"),

    # Modifier une société cliente
    path("<uuid:societe_cliente_id>/modifier/", modifier_societe_cliente, name="modifier_societe_cliente"),
]
