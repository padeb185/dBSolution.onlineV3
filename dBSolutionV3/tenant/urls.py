from django.urls import path
from voiture.views import liste_marques, liste_voitures_modele
from voiture.voiture_modele.views import modeles_par_marque

app_name = "tenant"

urlpatterns = [
    # Liste des marques (chemin propre à tenant si nécessaire)
    path("marques/", liste_marques, name="marques_list"),

    # Modèles d’une marque spécifique
    path("marques/<uuid:marque_id>/modeles/", modeles_par_marque, name="modeles_par_marque"),
]

