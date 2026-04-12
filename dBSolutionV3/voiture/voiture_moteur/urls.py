from django.urls import path
from .views import (moteur_detail_view, ajouter_moteur_view, liste_moteur, modifier_moteur_view)

app_name = "voiture_moteur"  # ← très important

urlpatterns = [
    path("", liste_moteur, name="list"),

    path("ajouter/", ajouter_moteur_view, name="ajouter_moteur"),

    path("<uuid:moteur_id>/", moteur_detail_view, name="moteur_detail"),

    path("<uuid:moteur_id>/modifier/", modifier_moteur_view, name="modifier_moteur"),
]