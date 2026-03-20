# maintenance/nettoyage_exterieur/urls.py
from django.urls import path
from . import views

app_name = "nettoyage_exterieur"  # correspond au namespace dans le template

urlpatterns = [
    path('simple/<uuid:exemplaire_id>/', views.nettoyage_exterieur_view, name='nettoyage_exterieur_simple'),
]