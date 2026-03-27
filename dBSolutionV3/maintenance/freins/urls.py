# maintenance/check_up/urls.py
from django.urls import path
from .views import FreinsListView, controle_freins_view, modifier_freins_view, freins_detail_view

app_name = "freins"

urlpatterns = [

    path('freins/<uuid:exemplaire_id>/liste/', FreinsListView.as_view(),name='freins_list'),

    path('controle-freins/<uuid:exemplaire_id>/', controle_freins_view, name='freins_check'),


    path('<int:frein_id>/modifier/', modifier_freins_view, name='modifier_freins'),


    path('<int:frein_id>/detail/', freins_detail_view, name='freins_detail'),
]




