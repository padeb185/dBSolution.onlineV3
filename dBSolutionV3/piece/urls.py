# pieces/urls.py
from django.urls import path

from . import views_stock as stock
from .views import PieceDeleteView, check_fabricants

app_name = "pieces"

urlpatterns = [
    # Catalogue / stock (un OEM par pièce, plusieurs EAN)
    path("", stock.catalogue_view, name="list"),
    path("add/", stock.piece_form_view, name="add"),
    path("<uuid:pk>/", stock.piece_fiche_view, name="detail"),
    path("<uuid:pk>/edit/", stock.piece_form_view, name="edit"),
    path("<uuid:pk>/delete/", PieceDeleteView.as_view(), name="delete"),
    # Variations de stock
    path("mouvements/", stock.mouvements_view, name="mouvements"),
    # Inventaires physiques
    path("inventaires/", stock.inventaires_view, name="inventaires"),
    path("inventaires/<int:pk>/", stock.inventaire_detail_view, name="inventaire_detail"),
    # Pièces utilisées par maintenance (débitées à l'émission de la facture)
    path("maintenance/<uuid:maintenance_id>/", stock.pieces_maintenance_view, name="pieces_maintenance"),
    # API scan OEM / EAN
    path("api/recherche/", stock.api_recherche, name="api_recherche"),
    path("api/codes-intervention/", stock.api_codes_intervention, name="api_codes_intervention"),
    path("api/check_fabricants", check_fabricants, name="check_fabricants"),
]
