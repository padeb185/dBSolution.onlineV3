# maintenance/check_up/urls.py
from django.urls import path
from .views import BteVitesseAutoListView, bte_vitesse_auto_check_view, modifier_bte_vitesse_auto_view, \
    bte_vitesse_auto_detail_view

app_name = "bte_auto"

urlpatterns = [

    path('bte_auto/<uuid:exemplaire_id>/liste/', BteVitesseAutoListView.as_view(),name='bte_vitesse_auto_list'),

    path('bte_auto/<uuid:exemplaire_id>/', bte_vitesse_auto_check_view, name='bte_vitesse_auto_check'),


    path('<int:bte_auto_id>/modifier/', modifier_bte_vitesse_auto_view, name='modifier_bte_vitesse_auto'),


    path('<int:bte_auto_id>/detail/', bte_vitesse_auto_detail_view, name='bte_vitesse_auto_detail'),
]




