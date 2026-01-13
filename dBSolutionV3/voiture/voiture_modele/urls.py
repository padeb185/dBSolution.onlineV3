from django.urls import path

from dBSolutionV3.voiture.voiture_modele.views import modeles_par_marque

app_name = "voiture_modele"

urlpatterns = [
    # Affiche les modèles pour une marque
    path("marque/<uuid:marque_id>/modeles/", modeles_par_marque, name="modeles_par_marque"),
]
