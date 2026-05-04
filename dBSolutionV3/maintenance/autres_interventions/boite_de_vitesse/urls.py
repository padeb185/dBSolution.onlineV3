# maintenance/check_up/urls.py
from django.urls import path
from .views import BoiteListView, boite_check_view, modifier_boite_view, boite_detail_view, dashboard_boite_view

app_name = "boite_de_vitesse"

urlpatterns = [

    path('<uuid:exemplaire_id>/dashboard', dashboard_boite_view, name='dashboard_boite'),

    path('boite/<uuid:exemplaire_id>/liste/', BoiteListView.as_view(),name='boite_list'),

    path('boite/<uuid:exemplaire_id>/', boite_check_view, name='boite_check'),


    path('boite/<int:boite_id>/modifier/', modifier_boite_view, name='modifier_boite'),


    path('boite/<int:boite_id>/detail/', boite_detail_view, name='boite_detail'),
]




