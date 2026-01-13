from django.urls import path
from .views import ajouter_exemplaire, liste_exemplaires, voiture_exemplaire_detail, lier_moteur_exemplaire_from_detail, \
    moteur_autocomplete, modifier_exemplaire

app_name = "voiture_exemplaire"



urlpatterns = [
    path('modele/<uuid:modele_id>/exemplaires/', liste_exemplaires, name='voiture_exemplaire'),
    path('modele/<uuid:modele_id>/ajouter/', ajouter_exemplaire, name='ajouter_exemplaire'),
    path('exemplaire/<uuid:exemplaire_id>/', voiture_exemplaire_detail, name='voiture_exemplaire_detail'),

    path('exemplaire/<uuid:exemplaire_id>/modifier/', modifier_exemplaire, name='modifier_exemplaire'),
    path('exemplaire/<uuid:exemplaire_id>/lier-moteur/', lier_moteur_exemplaire_from_detail, name='lier_moteur_exemplaire_from_detail'),
    path('autocomplete-moteur/', moteur_autocomplete, name='moteur_autocomplete'),
]

