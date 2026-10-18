# maintenance/check_up/urls.py
from django.urls import path
from .views import CapteurFapListView, capteur_fap_form_view, modifier_capteur_fap_view, capteur_fap_detail_view, \
    capteur_fap_detail_pdf_view, delete_capteur_fap_view

app_name = "capteur_fap"


urlpatterns = [

    path('capteur_fap/<uuid:exemplaire_id>/liste/', CapteurFapListView.as_view(),name='capteur_fap_list'),

    path('capteur_fap/<uuid:exemplaire_id>/', capteur_fap_form_view, name='capteur_fap_form'),


    path('capteur_fap/<int:capteur_fap_id>/modifier/', modifier_capteur_fap_view, name='modifier_capteur_fap'),


    path('capteur_fap/<int:capteur_fap_id>/detail/', capteur_fap_detail_view, name='capteur_fap_detail'),

    path("<int:pk>/detail/", capteur_fap_detail_pdf_view, name="capteur_fap_detail_pdf"),

    path("capteur_fap/<int:capteur_fap_id>/delete/", delete_capteur_fap_view, name="delete_capteur_fap"),

]

