from django.urls import path
from .views import controle_jeux_pieces_view, JeuListView, modifier_jeux_pieces_view, jeux_pieces_detail_view, \
    controle_jeux_pdf_view

app_name = "jeux_pieces"

urlpatterns = [
    path(
        "controle_jeux/<uuid:exemplaire_id>/", controle_jeux_pieces_view, name="controle_jeux"),

    path('jeux/<uuid:exemplaire_id>/liste/', JeuListView.as_view(),name='jeux_pieces_list'),


    path('<int:jeu_id>/modifier/', modifier_jeux_pieces_view, name='modifier_jeux_pieces'),


    path('<int:jeu_id>/detail/', jeux_pieces_detail_view, name='jeux_pieces_detail'),

    path("controle/<int:controle_id>/pdf/", controle_jeux_pdf_view, name="controle_jeux_pdf"),
]




