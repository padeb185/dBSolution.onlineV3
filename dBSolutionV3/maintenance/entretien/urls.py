# maintenance/check_up/urls.py
from django.urls import path
from .views import EntretienListView, entretien_check_view, modifier_entretien_view, entretien_detail_view

app_name = "entretien"



urlpatterns = [

    path('entretien/<uuid:exemplaire_id>/liste/', EntretienListView.as_view(),name='entretien_list'),

    path('entretien/<uuid:exemplaire_id>/', entretien_check_view, name='entretien_check_view'),


    path('<uuid:entretien_id>/modifier/', modifier_entretien_view, name='modifier_entretien'),


    path('<uuid:entretien_id>/detail/', entretien_detail_view, name='entretien_detail'),
]




