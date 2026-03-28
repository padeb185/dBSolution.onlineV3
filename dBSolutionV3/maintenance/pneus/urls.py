# maintenance/check_up/urls.py
from django.urls import path
from .views import PneusListView, controle_pneus_view, modifier_pneus_view, pneus_detail_view

app_name = "pneus"

urlpatterns = [

    path('pneus/<uuid:exemplaire_id>/liste/', PneusListView.as_view(),name='pneus_list'),

    path('pneus/<uuid:exemplaire_id>/', controle_pneus_view, name='controle_pneus'),


    path('<int:pneu_id>/modifier/', modifier_pneus_view, name='modifier_pneus'),


    path('<int:pneu_id>/detail/', pneus_detail_view, name='pneus_detail'),
]




