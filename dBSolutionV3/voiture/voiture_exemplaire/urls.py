from django.urls import path
from .views import ajouter_exemplaire_all, liste_exemplaires, voiture_exemplaire_detail, \
    lier_moteur_exemplaire_from_detail, moteur_autocomplete, modifier_exemplaire, get_cylindrees, get_code_moteur, \
    liste_exemplaires_all, get_type_de_boite, get_nom_du_type, lier_boite_exemplaire_from_detail, \
    exemplaire_detail

app_name = "voiture_exemplaire"



urlpatterns = [
    path('modele/<uuid:modele_id>/exemplaires/', liste_exemplaires, name='voiture_exemplaire'),
    path('modele/<uuid:modele_id>/ajouter/', ajouter_exemplaire_all, name='ajouter_exemplaire_all'),
    path('exemplaire/<uuid:exemplaire_id>/', voiture_exemplaire_detail, name='voiture_exemplaire_detail'),

    path('exemplaire/<uuid:exemplaire_id>/modifier/', modifier_exemplaire, name='modifier_exemplaire'),
    path('exemplaire/<uuid:exemplaire_id>/lier-moteur/', lier_moteur_exemplaire_from_detail, name='lier_moteur_exemplaire_from_detail'),
    path('autocomplete-moteur/', moteur_autocomplete, name='moteur_autocomplete'),

    path('ajax/get_cylindrees/', get_cylindrees, name='ajax_get_cylindrees'),
    path('ajax/get_code_moteur/', get_code_moteur, name='ajax_get_code_moteur'),

    path("modele/<uuid:id_modele>/", liste_exemplaires, name="liste_exemplaires"),

    path('exemplaires/', liste_exemplaires_all, name='liste_exemplaires_all'),

    path('ajax/get_type_de_boite/', get_type_de_boite, name='ajax_get_type_de_boite'),
    path('ajax/get_nom_du_type/', get_nom_du_type, name='ajax_get_nom_du_type'),

    path('exemplaire/<uuid:exemplaire_id>/lier-moteur/', lier_boite_exemplaire_from_detail,
         name='lier_boite_exemplaire_from_detail'),



    path(
        "exemplaire/<uuid:exemplaire_id>/",
        exemplaire_detail,
        name="detail_exemplaire"  # ← exactement ce nom
    ),
    path(
        "exemplaire/<uuid:exemplaire_id>/lier-moteur/",
        lier_moteur_exemplaire_from_detail,
        name="lier_moteur_exemplaire_from_detail"
    ),


]

