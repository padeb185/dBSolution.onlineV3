from django.urls import path
from . import views

app_name = "voiture_exemplaire"

urlpatterns = [
    # Liste des exemplaires d'un modèle
    path("modele/<uuid:modele_id>/exemplaires/", views.voiture_exemplaire, name="voiture_exemplaire"),

    # Détail d'un exemplaire
    path('<uuid:exemplaire_id>/', views.voiture_exemplaire_detail, name='voiture_exemplaire_detail'),

    # Lier un moteur depuis la page détail d'un exemplaire
    path('<uuid:exemplaire_id>/lier-moteur/', views.lier_moteur_exemplaire_from_detail,
         name='lier_moteur_exemplaire_from_detail'),

    # Autocomplete moteur
    path('autocomplete-moteur/', views.moteur_autocomplete, name='moteur_autocomplete'),
]
