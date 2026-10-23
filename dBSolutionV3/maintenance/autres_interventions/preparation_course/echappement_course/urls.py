# maintenance/check_up/urls.py
from django.urls import path
from .views import EchappementCompetitionListView, pc_echappement_form_view, modifier_pc_echappement_view, pc_echappement_detail_view, \
    pc_echappement_detail_pdf_view, delete_pc_echappement_view

app_name = "pc_echappement"


urlpatterns = [

    path('pc_echappement/<uuid:exemplaire_id>/liste/', EchappementCompetitionListView.as_view(),name='pc_echappement_list'),

    path('pc_echappement/<uuid:exemplaire_id>/', pc_echappement_form_view, name='pc_echappement_form'),


    path('pc_echappement/<int:pc_echappement_id>/modifier/', modifier_pc_echappement_view, name='modifier_pc_echappement'),


    path('pc_echappement/<int:pc_echappement_id>/detail/', pc_echappement_detail_view, name='pc_echappement_detail'),

    path("<int:pk>/detail/", pc_echappement_detail_pdf_view, name="pc_echappement_detail_pdf"),

    path("pc_echappement/<int:pc_echappement_id>/delete/", delete_pc_echappement_view, name="delete_pc_echappement"),

]

