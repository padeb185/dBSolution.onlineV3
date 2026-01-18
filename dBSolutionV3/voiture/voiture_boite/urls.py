# voiture_boite/urls.py
from django.urls import path
from .views import liste_boite, ajouter_boite_simple

app_name = 'voiture_boite'  # ← indispensable pour le namespace

urlpatterns = [

    path('', liste_boite, name='list'),

    path('ajouter/', ajouter_boite_simple, name='ajouter_boite_simple'),

]
