# maintenance/check_up/urls.py
from django.urls import path
from .views import TuyauxAdblueListView, tuyaux_adblue_form_view, modifier_tuyaux_adblue_view, tuyaux_adblue_detail_view, \
    tuyaux_adblue_detail_pdf_view, delete_tuyaux_adblue_view

app_name = "tuyaux_adblue"


urlpatterns = [

    path('tuyaux_adblue/<uuid:exemplaire_id>/liste/', TuyauxAdblueListView.as_view(),name='tuyaux_adblue_list'),

    path('tuyaux_adblue/<uuid:exemplaire_id>/', tuyaux_adblue_form_view, name='tuyaux_adblue_form'),


    path('tuyaux_adblue/<int:tuyaux_adblue_id>/modifier/', modifier_tuyaux_adblue_view, name='modifier_tuyaux_adblue'),


    path('tuyaux_adblue/<int:tuyaux_adblue_id>/detail/', tuyaux_adblue_detail_view, name='tuyaux_adblue_detail'),

    path("<int:pk>/detail/", tuyaux_adblue_detail_pdf_view, name="tuyaux_adblue_detail_pdf"),

    path("tuyaux_adblue/<int:tuyaux_adblue_id>/delete/", delete_tuyaux_adblue_view, name="delete_tuyaux_adblue"),

]

