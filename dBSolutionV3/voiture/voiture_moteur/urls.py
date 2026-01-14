from django.urls import path
from .views import MoteurListView, moteur_detail_view, ajouter_moteur, ajouter_moteur_seul

app_name = "voiture_moteur"  # ← très important

urlpatterns = [
    path("", MoteurListView.as_view(), name="list"),
    path("ajouter/", ajouter_moteur_seul, name="ajouter_moteur_seul"),
    path("ajouter/<uuid:exemplaire_id>/", ajouter_moteur, name="ajouter_moteur"),
    path("<uuid:moteur_id>/", moteur_detail_view, name="detail"),
]

