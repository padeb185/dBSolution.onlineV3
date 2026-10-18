# maintenance/check_up/urls.py
from django.urls import path
from .views import FiltreParticulesListView, filtre_particules_form_view, modifier_filtre_particules_view, filtre_particules_detail_view, \
    filtre_particules_detail_pdf_view, delete_filtre_particules_view

app_name = "filtre_particules"


urlpatterns = [

    path('filtre_particules/<uuid:exemplaire_id>/liste/', FiltreParticulesListView.as_view(),name='filtre_particules_list'),

    path('filtre_particules/<uuid:exemplaire_id>/', filtre_particules_form_view, name='filtre_particules_form'),


    path('filtre_particules/<int:filtre_particules_id>/modifier/', modifier_filtre_particules_view, name='modifier_filtre_particules'),


    path('filtre_particules/<int:filtre_particules_id>/detail/', filtre_particules_detail_view, name='filtre_particules_detail'),

    path("<int:pk>/detail/", filtre_particules_detail_pdf_view, name="filtre_particules_detail_pdf"),

    path("filtre_particules/<int:filtre_particules_id>/delete/", delete_filtre_particules_view, name="delete_filtre_particules"),

]

