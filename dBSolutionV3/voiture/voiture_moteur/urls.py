from django.urls import path
from . import views

app_name = "voiture_moteur"

urlpatterns = [
    path("ajouter/<uuid:exemplaire_id>/", views.ajouter_moteur, name="ajouter_moteur"),
]
