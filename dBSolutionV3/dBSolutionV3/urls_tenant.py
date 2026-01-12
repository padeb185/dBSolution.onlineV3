from django.urls import path, include
from utilisateurs.views import dashboard_view
from voiture.voiture_exemplaire.views import ajouter_exemplaire

urlpatterns = [
    # Dashboard principal
    path("", dashboard_view, name="dashboard"),

    # Tenant
    path('voiture/', include('tenant.urls', namespace='voiture')),

    # Marques de voiture
    path("voitures/marques/", include("voiture.voiture_marque.urls", namespace="voiture_marque")),

    # Exemplaires de voiture
    path("voitures/exemplaires/", include("voiture.voiture_exemplaire.urls", namespace="voiture_exemplaire")),

    # Ajouter un exemplaire pour un modèle spécifique
    path('modele/<uuid:modele_id>/ajouter/', ajouter_exemplaire, name='ajouter_exemplaire'),

    # Moteurs
    path("voiture/moteurs/", include("voiture.voiture_moteur.urls", namespace="voiture_moteur")),
]
