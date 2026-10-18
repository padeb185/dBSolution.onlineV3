# maintenance/check_up/urls.py
from django.urls import path
from .views import RegenerationFapListView, regeneration_fap_form_view, modifier_regeneration_fap_view, regeneration_fap_detail_view, \
    regeneration_fap_detail_pdf_view, delete_regeneration_fap_view

app_name = "regeneration_fap"


urlpatterns = [

    path('regeneration_fap/<uuid:exemplaire_id>/liste/', RegenerationFapListView.as_view(),name='regeneration_fap_list'),

    path('regeneration_fap/<uuid:exemplaire_id>/', regeneration_fap_form_view, name='regeneration_fap_form'),


    path('regeneration_fap/<int:regeneration_fap_id>/modifier/', modifier_regeneration_fap_view, name='modifier_regeneration_fap'),


    path('regeneration_fap/<int:regeneration_fap_id>/detail/', regeneration_fap_detail_view, name='regeneration_fap_detail'),

    path("<int:pk>/detail/", regeneration_fap_detail_pdf_view, name="regeneration_fap_detail_pdf"),

    path("regeneration_fap/<int:regeneration_fap_id>/delete/", delete_regeneration_fap_view, name="delete_regeneration_fap"),

]

