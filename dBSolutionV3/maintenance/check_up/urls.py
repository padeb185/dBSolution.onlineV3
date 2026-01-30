# maintenance/check_up/urls.py
from django.urls import path
from .views import detail_exemplaire_maintenance,  \
    creer_checkup_complet

app_name = "check_up"

urlpatterns = [

    # Détail d’un exemplaire
    path('exemplaire/<uuid:exemplaire_id>/', detail_exemplaire_maintenance, name='detail_exemplaire'),

    # Créer un check-up complet
    path('creer/<uuid:exemplaire_id>/', creer_checkup_complet, name='creer_checkup'),

    # Exemple : générer PDF pour une maintenance
    #path('maintenance/<int:maintenance_id>/rapport/', maintenance_pdf_report, name='pdf_report'),
]
