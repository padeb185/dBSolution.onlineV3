from django.urls import path
from .views import RemplacementMoteurListView, remplacement_moteur_form_view, remplacement_moteur_detail_view

app_name = "remplacement_moteur"


urlpatterns = [

    path('<uuid:exemplaire_id>/liste/', RemplacementMoteurListView.as_view(), name='remplacement_moteur_list'),

    path( '<uuid:exemplaire_id>/', remplacement_moteur_form_view, name='remplacement_moteur_form'),

    path('<uuid:remplacement_moteur_id>/detail/', remplacement_moteur_detail_view, name='remplacement_moteur_detail'),

]

