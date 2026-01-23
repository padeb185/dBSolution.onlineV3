from django.urls import path
from .views import ajouter_exemplaire_all, liste_exemplaires, voiture_exemplaire_detail, \
    moteur_autocomplete, modifier_exemplaire,\
    liste_exemplaires_all, lier_boite_exemplaire, lier_moteur_exemplaire

app_name = "voiture_exemplaire"



urlpatterns = [
    path('modele/<uuid:modele_id>/exemplaires/', liste_exemplaires, name='voiture_exemplaire'),
    path('modele/<uuid:modele_id>/ajouter/', ajouter_exemplaire_all, name='ajouter_exemplaire_all'),
    path('exemplaire/<uuid:exemplaire_id>/', voiture_exemplaire_detail, name='voiture_exemplaire_detail'),

    path('exemplaire/<uuid:exemplaire_id>/modifier/', modifier_exemplaire, name='modifier_exemplaire'),

    path('autocomplete-moteur/', moteur_autocomplete, name='moteur_autocomplete'),



    path("modele/<uuid:id_modele>/", liste_exemplaires, name="liste_exemplaires"),

    path('exemplaires/', liste_exemplaires_all, name='liste_exemplaires_all'),

    path(
        'exemplaire/<uuid:exemplaire_id>/lier-boite/',lier_boite_exemplaire,name='lier_boite_exemplaire'),
    path(
        'exemplaire/<uuid:exemplaire_id>/lier-moteur/',lier_moteur_exemplaire,name='lier_moteur_exemplaire'),


]

