# maintenance/check_up/urls.py
from django.urls import path
from .views import TuyauxFapListView, tuyaux_fap_form_view, modifier_tuyaux_fap_view, tuyaux_fap_detail_view, \
    tuyaux_fap_detail_pdf_view, delete_tuyaux_fap_view

app_name = "tuyaux_fap"


urlpatterns = [

    path('tuyaux_fap/<uuid:exemplaire_id>/liste/', TuyauxFapListView.as_view(),name='tuyaux_fap_list'),

    path('tuyaux_fap/<uuid:exemplaire_id>/', tuyaux_fap_form_view, name='tuyaux_fap_form'),


    path('tuyaux_fap/<int:tuyaux_fap_id>/modifier/', modifier_tuyaux_fap_view, name='modifier_tuyaux_fap'),


    path('tuyaux_fap/<int:tuyaux_fap_id>/detail/', tuyaux_fap_detail_view, name='tuyaux_fap_detail'),

    path("<int:pk>/detail/", tuyaux_fap_detail_pdf_view, name="tuyaux_fap_detail_pdf"),

    path("tuyaux_fap/<int:tuyaux_fap_id>/delete/", delete_tuyaux_fap_view, name="delete_tuyaux_fap"),

]

