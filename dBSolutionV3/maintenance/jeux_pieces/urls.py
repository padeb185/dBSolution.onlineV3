from django.urls import path
from .views import controle_jeux_pieces_view

app_name = "jeux_pieces"

urlpatterns = [
    path(
        "controle_jeux/<uuid:exemplaire_id>/", controle_jeux_pieces_view, name="controle_jeux_pieces_view"),
]


