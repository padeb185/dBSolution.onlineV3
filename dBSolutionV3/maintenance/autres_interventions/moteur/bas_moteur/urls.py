# maintenance/check_up/urls.py
from django.urls import path
from .views import BasMoteurListView, bas_moteur_form_view, modifier_bas_moteur_view, bas_moteur_detail_view, \
    bas_moteur_detail_pdf_view, delete_bas_moteur_view

app_name = "bas_moteur"


urlpatterns = [

    path('bas_moteur/<uuid:exemplaire_id>/liste/', BasMoteurListView.as_view(),name='bas_moteur_list'),

    path('bas_moteur/<uuid:exemplaire_id>/', bas_moteur_form_view, name='bas_moteur_form'),


    path('bas_moteur/<int:bas_moteur_id>/modifier/', modifier_bas_moteur_view, name='modifier_bas_moteur'),


    path('bas_moteur/<int:bas_moteur_id>/detail/', bas_moteur_detail_view, name='bas_moteur_detail'),

    path("<int:pk>/detail/", bas_moteur_detail_pdf_view, name="bas_moteur_detail_pdf"),

    path("bas_moteur/<int:bas_moteur_id>/delete/", delete_bas_moteur_view, name="delete_bas_moteur"),

]

