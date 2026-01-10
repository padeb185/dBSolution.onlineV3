from django.urls import path
from . import views

urlpatterns = [
    path('lier-moteur/<uuid:moteur_id>/<uuid:exemplaire_id>/', lier_moteur_exemplaire, name="lier_moteur_exemplaire"),

path("api/moteur-autocomplete/", views.moteur_autocomplete, name="moteur_autocomplete"),
]
