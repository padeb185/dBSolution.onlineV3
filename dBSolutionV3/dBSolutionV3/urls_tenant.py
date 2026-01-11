from django.urls import path, include
from theme.views import dashboard
from voiture.voiture_exemplaire.views import ajouter_exemplaire
from utilisateurs.views import dashboard_view

urlpatterns = [
    path("", dashboard_view, name="dashboard"),

    path('voiture/', include('tenant.urls', namespace='voiture')),

    path("voitures/marques/", include("voiture.voiture_marque.urls")),

    path("voitures/exemplaires/", include("voiture.voiture_exemplaire.urls", namespace="voiture_exemplaire")),

    path('modele/<uuid:modele_id>/ajouter/', ajouter_exemplaire, name='ajouter_exemplaire'),

    path("voiture/moteurs/", include("voiture.voiture_moteur.urls", namespace="voiture_moteur")),


    path('exemplaires/', include('voiture.voiture_exemplaire.urls')),
]

