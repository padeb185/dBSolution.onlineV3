from django.urls import path
from voiture.views import liste_marques, liste_voitures_modele

app_name = "tenant"

urlpatterns = [
    path("voitures/marques/", liste_marques, name="marques_list"),
    path("voitures/marques/marque/<uuid:pk>/modeles/", liste_voitures_modele, name="modele_detail"),
]
