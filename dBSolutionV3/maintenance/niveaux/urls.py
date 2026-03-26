# maintenance/check_up/urls.py
from django.urls import path
from .views import niveaux_detail, modifier_niveaux_view, NiveauxListView, niveau_form_view

app_name = "niveaux"


urlpatterns = [

    path('niveaux/<uuid:exemplaire_id>/liste/', NiveauxListView.as_view(),name='niveaux_list'),

    path('niveaux_form/<uuid:exemplaire_id>/', niveau_form_view, name='niveau_form_view'),


    path('modifier/<int:niveau_id>/<uuid:exemplaire_id>/', modifier_niveaux_view, name='modifier_niveaux'),


    path('<int:niveau_id>/detail/', niveaux_detail, name='niveaux_detail')
]




