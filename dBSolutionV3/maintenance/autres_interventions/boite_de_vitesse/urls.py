# maintenance/check_up/urls.py
from django.urls import path
from .views import BoiteListView, boite_check_view, modifier_boite_view, boite_detail_view

app_name = "boite_de_vitesse"

urlpatterns = [

    path('check_up/<uuid:exemplaire_id>/liste/', BoiteListView.as_view(),name='boite_list'),

    path('controle-total/<uuid:exemplaire_id>/', boite_check_view, name='boite_check'),


    path('<int:checkup_id>/modifier/', modifier_boite_view, name='modifier_boite'),


    path('<int:checkup_id>/detail/', boite_detail_view, name='boite_detail'),
]




