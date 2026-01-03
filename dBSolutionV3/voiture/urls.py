# voiture/urls.py
from django.urls import path
from . import views

app_name = 'voiture'

urlpatterns = [
    path('marques/', views.liste_marques, name='liste_marques'),
    path('marque/<uuid:marque_id>/', views.liste_voitures_marque, name='liste_voitures_marque'),
]
