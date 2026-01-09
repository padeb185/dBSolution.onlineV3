# moteur/urls.py
from django.urls import path
from .views import AjouterMoteurView

app_name = "voiture_moteur"


urlpatterns = [
    path("ajouter/<uuid:exemplaire_id>/", AjouterMoteurView.as_view(), name="ajouter_moteur"),
]
