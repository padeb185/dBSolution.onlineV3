from django.urls import path
from .views import moteur_detail_view, ajouter_moteur, ajouter_moteur_seul, liste_moteur

app_name = "voiture_moteur"  # ← très important

urlpatterns = [
    path("", liste_moteur, name="list"),
    path("ajouter/", ajouter_moteur_seul, name="ajouter_moteur_seul"),
    path("ajouter/<uuid:exemplaire_id>/", ajouter_moteur, name="ajouter_moteur"),
    path("<uuid:moteur_id>/", moteur_detail_view, name="detail"),
]

