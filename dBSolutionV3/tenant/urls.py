from django.urls import path
from voiture.views import liste_marques, liste_voitures_modele
from voiture.voiture_modele.views import modeles_par_marque
from tenant.views import moteur_view

app_name = "tenant"

urlpatterns = [
    path("voitures/marques/", liste_marques, name="marques_list"),
    path('marques/marque/<uuid:marque_id>/modeles/', modeles_par_marque, name='modeles_par_marque'),

]


