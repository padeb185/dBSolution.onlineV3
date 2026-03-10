# pieces/urls.py
from django.urls import path
from .views import (
    PieceListView, PieceDetailView, PieceCreateView, PieceUpdateView, PieceDeleteView, check_fabricants
)

app_name = "pieces"

urlpatterns = [
    path("", PieceListView.as_view(), name="list"),
    path("add/", PieceCreateView.as_view(), name="add"),
    path("<uuid:pk>/", PieceDetailView.as_view(), name="detail"),
    path("<uuid:pk>/edit/", PieceUpdateView.as_view(), name="edit"),
    path("<uuid:pk>/delete/", PieceDeleteView.as_view(), name="delete"),
    path("api/check_fabricants", check_fabricants, name="check_fabricants"),
]