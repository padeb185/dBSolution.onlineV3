# maintenance/check_up/urls.py
from django.urls import path
from .views import PreparationMoteurListView, pc_moteur_form_view, modifier_pc_moteur_view, pc_moteur_detail_view, \
    pc_moteur_detail_pdf_view, delete_pc_moteur_view

app_name = "pc_moteur"


urlpatterns = [

    path('pc_moteur/<uuid:exemplaire_id>/liste/', PreparationMoteurListView.as_view(),name='pc_moteur_list'),

    path('pc_moteur/<uuid:exemplaire_id>/', pc_moteur_form_view, name='pc_moteur_form'),


    path('pc_moteur/<int:pc_moteur_id>/modifier/', modifier_pc_moteur_view, name='modifier_pc_moteur'),


    path('pc_moteur/<int:pc_moteur_id>/detail/', pc_moteur_detail_view, name='pc_moteur_detail'),

    path("<int:pk>/detail/", pc_moteur_detail_pdf_view, name="pc_moteur_detail_pdf"),

    path("pc_moteur/<int:pc_moteur_id>/delete/", delete_pc_moteur_view, name="delete_pc_moteur"),

]

