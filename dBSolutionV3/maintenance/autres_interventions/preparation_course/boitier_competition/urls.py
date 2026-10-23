# maintenance/check_up/urls.py
from django.urls import path
from .views import BoitierCompetitionListView, pc_boitier_form_view, modifier_pc_boitier_view, pc_boitier_detail_view, \
    pc_boitier_detail_pdf_view, delete_pc_boitier_view

app_name = "pc_boitier"


urlpatterns = [

    path('pc_boitier/<uuid:exemplaire_id>/liste/', BoitierCompetitionListView.as_view(),name='pc_boitier_list'),

    path('pc_boitier/<uuid:exemplaire_id>/', pc_boitier_form_view, name='pc_boitier_form'),


    path('pc_boitier/<int:pc_boitier_id>/modifier/', modifier_pc_boitier_view, name='modifier_pc_boitier'),


    path('pc_boitier/<int:pc_boitier_id>/detail/', pc_boitier_detail_view, name='pc_boitier_detail'),

    path("<int:pk>/detail/", pc_boitier_detail_pdf_view, name="pc_boitier_detail_pdf"),

    path("pc_boitier/<int:pc_boitier_id>/delete/", delete_pc_boitier_view, name="delete_pc_boitier"),

]

