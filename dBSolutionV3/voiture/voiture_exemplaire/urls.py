from django.urls import path
from .views import voiture_exemplaire_detail, lier_moteur_exemplaire_from_detail, moteur_autocomplete, \
    ajouter_exemplaire, voiture_exemplaire
from voiture.voiture_exemplaire.models import VoitureExemplaire


app_name = "voiture_exemplaire"

urlpatterns = [
    path("modele/<uuid:modele_id>/exemplaires/", voiture_exemplaire, name="voiture_exemplaire"),
    path("modele/<uuid:modele_id>/ajouter/", ajouter_exemplaire, name="ajouter_exemplaire"),
    path("<uuid:exemplaire_id>/lier-moteur/", lier_moteur_exemplaire_from_detail, name="lier_moteur_exemplaire_from_detail"),
    path("autocomplete-moteur/", moteur_autocomplete, name="moteur_autocomplete"),
    path('exemplaire/<uuid:exemplaire_id>/', voiture_exemplaire_detail, name='voiture_exemplaire_detail'),






]
