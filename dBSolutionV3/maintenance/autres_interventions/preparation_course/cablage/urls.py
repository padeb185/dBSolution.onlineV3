# maintenance/check_up/urls.py
from django.urls import path
from .views import CablageCompetitionListView, pc_cablage_form_view, modifier_pc_cablage_view, pc_cablage_detail_view, \
    pc_cablage_detail_pdf_view, delete_pc_cablage_view

app_name = "pc_cablage"


urlpatterns = [

    path('pc_cablage/<uuid:exemplaire_id>/liste/', CablageCompetitionListView.as_view(),name='pc_cablage_list'),

    path('pc_cablage/<uuid:exemplaire_id>/', pc_cablage_form_view, name='pc_cablage_form'),


    path('pc_cablage/<int:pc_cablage_id>/modifier/', modifier_pc_cablage_view, name='modifier_pc_cablage'),


    path('pc_cablage/<int:pc_cablage_id>/detail/', pc_cablage_detail_view, name='pc_cablage_detail'),

    path("<int:pk>/detail/", pc_cablage_detail_pdf_view, name="pc_cablage_detail_pdf"),

    path("pc_cablage/<int:pc_cablage_id>/delete/", delete_pc_cablage_view, name="delete_pc_cablage"),

]

