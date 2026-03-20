# maintenance/nettoyage_exterieur/urls.py
from django.urls import path

from .views import nettoyage_exterieur_view

app_name = "nettoyage_exterieur"  # correspond au namespace dans le template

urlpatterns = [
    path('simple/<uuid:exemplaire_id>/', nettoyage_exterieur_view, name='nettoyage_exterieur_view'),
]