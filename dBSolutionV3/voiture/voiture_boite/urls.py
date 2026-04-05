# voiture_boite/urls.py
from django.urls import path
from .views import liste_boite_view, ajouter_boite_view, boite_detail_view, modifier_boite_view

app_name = 'voiture_boite'  # ← indispensable pour le namespace

urlpatterns = [

    path('', liste_boite_view, name='list'),

    path('ajouter/', ajouter_boite_view, name='ajouter_boite'),


    path("<uuid:boite_id>/", boite_detail_view, name="boite_detail"),

    path('<uuid:boite_id>/modifier/', modifier_boite_view, name='modifier_boite'),
]
