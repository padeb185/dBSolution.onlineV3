from django.urls import path
from .views import proprietaire_dashboard_view, ProprietaireListView, ProprietaireVoitureListView, check_prenom, \
    proprietaire_form_view, proprietaire_detail_view, modifier_proprietaire_view

app_name = "proprietaire"

urlpatterns = [
    path('', proprietaire_dashboard_view, name='proprietaire_dashboard'),

    path('proprietaire', ProprietaireListView.as_view(), name='proprietaire_list'),

    path("proprietaire/creer/",
        proprietaire_form_view,
        name="proprietaire_form",
    ),

    path(
        "proprietaire_voiture/",
        ProprietaireVoitureListView.as_view(),
        name="proprietaire_voiture_list"
    ),

    path('api/check_prenom/', check_prenom, name='check_prenom'),

    path(
        "<int:proprietaire_id>/",
        proprietaire_detail_view,
        name="proprietaire_detail"
    ),

    path(
        'proprietaire/<int:proprietaire_id>/modifier/',
        modifier_proprietaire_view,
        name='modifier_proprietaire'),

]
