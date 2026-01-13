from django.urls import path
from . import views

app_name = "voiture_exemplaire"

urlpatterns = [
    path("modele/<uuid:modele_id>/exemplaires/", views.voiture_exemplaire, name="voiture_exemplaire"),
    path("modele/<uuid:modele_id>/ajouter/", views.ajouter_exemplaire, name="ajouter_exemplaire"),
    path("<uuid:exemplaire_id>/", views.voiture_exemplaire_detail, name="voiture_exemplaire_detail"),
    path("<uuid:exemplaire_id>/lier-moteur/", views.lier_moteur_exemplaire_from_detail, name="lier_moteur_exemplaire_from_detail"),
    path("autocomplete-moteur/", views.moteur_autocomplete, name="moteur_autocomplete"),
]
