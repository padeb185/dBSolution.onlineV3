from django.urls import path
from .views import RemplacementMoteurListView, RemplacementMoteurCreateView

app_name = "remplacement_moteur"


urlpatterns = [

    path('<uuid:exemplaire_id>/liste/', RemplacementMoteurListView.as_view(), name='remplacement_moteur_list'),

    path( '<uuid:exemplaire_id>/', RemplacementMoteurCreateView.as_view(), name='remplacement_moteur_form'),


]

