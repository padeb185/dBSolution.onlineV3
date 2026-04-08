from django.urls import path, include
from .views import dashboard_moteur_view

app_name = "moteur"  # <- indispensable pour le namespace

urlpatterns = [
    path('<uuid:exemplaire_id>/dashboard', dashboard_moteur_view, name='dashboard_moteur'),

    path(
        '<uuid:exemplaire_id>/admission/',
        include(('maintenance.autres_interventions.moteur.admission.urls', 'admission'), namespace='admission')
    ),








]