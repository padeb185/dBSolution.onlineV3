# maintenance/check_up/urls.py
from django.urls import path

from .models import GeometrieVoiture
from .views import  rapport_view, geometrie_detail_view, \
    geometrie_modifier_view, geometrie_check_view, GeometrieListView

app_name = "geometrie"

urlpatterns = [

    path('geometrie/<uuid:exemplaire_id>/liste/', GeometrieListView.as_view(),name='geometrie_list'),

    path('geometrie/<uuid:exemplaire_id>/', geometrie_check_view, name='geometrie_check'),


    path('geometrie/<int:geometrie_id>/modifier/', geometrie_modifier_view, name='geometrie_modifier'),


    path('geometrie/<int:geometrie_id>/detail/', geometrie_detail_view, name='geometrie_detail'),

    path("rapport/<int:pk>/", rapport_view, name="rapport"),
]




