# maintenance/check_up/urls.py
from django.urls import path
from .views import SondeFapAvalListView, sonde_fap_aval_form_view, modifier_sonde_fap_aval_view, sonde_fap_aval_detail_view, \
    sonde_fap_aval_detail_pdf_view, delete_sonde_fap_aval_view

app_name = "sonde_fap_aval"


urlpatterns = [

    path('sonde_fap_aval/<uuid:exemplaire_id>/liste/', SondeFapAvalListView.as_view(),name='sonde_fap_aval_list'),

    path('sonde_fap_aval/<uuid:exemplaire_id>/', sonde_fap_aval_form_view, name='sonde_fap_aval_form'),


    path('sonde_fap_aval/<int:sonde_fap_aval_id>/modifier/', modifier_sonde_fap_aval_view, name='modifier_sonde_fap_aval'),


    path('sonde_fap_aval/<int:sonde_fap_aval_id>/detail/', sonde_fap_aval_detail_view, name='sonde_fap_aval_detail'),

    path("<int:pk>/detail/", sonde_fap_aval_detail_pdf_view, name="sonde_fap_aval_detail_pdf"),

    path("sonde_fap_aval/<int:sonde_fap_aval_id>/delete/", delete_sonde_fap_aval_view, name="delete_sonde_fap_aval"),

]

