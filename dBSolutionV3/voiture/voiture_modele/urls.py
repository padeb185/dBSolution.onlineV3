from django.urls import path
from .views import VoitureModeleListView, modifier_voiture_modele, voiture_modele_detail, ajouter_voiture_modele_all
from voiture.voiture_modele.views import modeles_par_marque

app_name = "voiture_modele"



urlpatterns = [
    # Affiche les modèles pour une marque
    path("marque/<uuid:marque_id>/modeles/", modeles_par_marque, name="modeles_par_marque"),

    path("modeles/", VoitureModeleListView.as_view(), name="modele_list_all"),

    path(
        "carrosserie/creer/",
        ajouter_voiture_modele_all,
        name="voiture_modele_create",
    ),

    path(
        "<uuid:voiture_modele_id>/",
        voiture_modele_detail,
        name="voiture_modele_detail",
    ),

    path(
        'carrosserie/<uuid:voiture_modele_id>/modifier/',
        modifier_voiture_modele,
        name='modifier_voiture_modele'),

]


