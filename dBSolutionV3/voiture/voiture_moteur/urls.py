from django.urls import path
from . import views
from tenant.views import moteur_view

app_name = "voiture_moteur"

urlpatterns = [
    path("ajouter/<uuid:exemplaire_id>/", views.ajouter_moteur, name="ajouter_moteur"),

    path('', moteur_view, name='list'),


]