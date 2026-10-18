# maintenance/check_up/urls.py
from django.urls import path
from .views import SondeFapAmontListView, sonde_fap_amont_form_view, modifier_sonde_fap_amont_view, sonde_fap_amont_detail_view, \
    sonde_fap_amont_detail_pdf_view, delete_sonde_fap_amont_view

app_name = "sonde_fap_amont"


urlpatterns = [

    path('sonde_fap_amont/<uuid:exemplaire_id>/liste/', SondeFapAmontListView.as_view(),name='sonde_fap_amont_list'),

    path('sonde_fap_amont/<uuid:exemplaire_id>/', sonde_fap_amont_form_view, name='sonde_fap_amont_form'),


    path('sonde_fap_amont/<int:sonde_fap_amont_id>/modifier/', modifier_sonde_fap_amont_view, name='modifier_sonde_fap_amont'),


    path('sonde_fap_amont/<int:sonde_fap_amont_id>/detail/', sonde_fap_amont_detail_view, name='sonde_fap_amont_detail'),

    path("<int:pk>/detail/", sonde_fap_amont_detail_pdf_view, name="sonde_fap_amont_detail_pdf"),

    path("sonde_fap_amont/<int:sonde_fap_amont_id>/delete/", delete_sonde_fap_amont_view, name="delete_sonde_fap_amont"),

]

