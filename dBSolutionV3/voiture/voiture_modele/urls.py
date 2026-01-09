from django.urls import path
from . import views

app_name = "voiture_modele"

urlpatterns = [
    # Affiche les modèles pour une marque
    path("marque/<uuid:marque_id>/modeles/", views.modeles_par_marque, name="modeles_par_marque"),
]
