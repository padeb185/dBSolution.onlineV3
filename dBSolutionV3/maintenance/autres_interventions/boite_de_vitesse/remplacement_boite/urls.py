from django.urls import path
from .views import RemplacementBoiteListView, remplacement_boite_form_view, remplacement_boite_detail_view, \
    modifier_remplacement_boite_view

app_name = "remplacement_moteur"


urlpatterns = [

    path('<uuid:exemplaire_id>/liste/', RemplacementBoiteListView.as_view(), name='remplacement_boite_list'),

    path( '<uuid:exemplaire_id>/', remplacement_boite_form_view, name='remplacement_boite_form'),

    path('<uuid:remplacement_boite_id>/detail/', remplacement_boite_detail_view, name='remplacement_boite_detail'),

    path('<uuid:remplacement_boite_id>/modifier/', modifier_remplacement_boite_view, name='modifier_remplacement_boite'),

]

