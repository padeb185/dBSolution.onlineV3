# maintenance/check_up/urls.py
from django.urls import path
from .views import DemontageAllegementListView, pc_demontage_form_view, modifier_pc_demontage_view, pc_demontage_detail_view, \
    pc_demontage_detail_pdf_view, delete_pc_demontage_view

app_name = "pc_demontage"


urlpatterns = [

    path('pc_demontage/<uuid:exemplaire_id>/liste/', DemontageAllegementListView.as_view(),name='pc_demontage_list'),

    path('pc_demontage/<uuid:exemplaire_id>/', pc_demontage_form_view, name='pc_demontage_form'),


    path('pc_demontage/<int:pc_demontage_id>/modifier/', modifier_pc_demontage_view, name='modifier_pc_demontage'),


    path('pc_demontage/<int:pc_demontage_id>/detail/', pc_demontage_detail_view, name='pc_demontage_detail'),

    path("<int:pk>/detail/", pc_demontage_detail_pdf_view, name="pc_demontage_detail_pdf"),

    path("pc_demontage/<int:pc_demontage_id>/delete/", delete_pc_demontage_view, name="delete_pc_demontage"),

]

