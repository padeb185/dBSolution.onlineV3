# maintenance/check_up/urls.py
from django.urls import path
from .views import AjoutAdblueListView, ajout_adblue_form_view, modifier_ajout_adblue_view, ajout_adblue_detail_view, \
    ajout_adblue_detail_pdf_view, delete_ajout_adblue_view

app_name = "ajout_adblue"


urlpatterns = [

    path('ajout_adblue/<uuid:exemplaire_id>/liste/', AjoutAdblueListView.as_view(),name='ajout_adblue_list'),

    path('ajout_adblue/<uuid:exemplaire_id>/', ajout_adblue_form_view, name='ajout_adblue_form'),


    path('ajout_adblue/<int:ajout_adblue_id>/modifier/', modifier_ajout_adblue_view, name='modifier_ajout_adblue'),


    path('ajout_adblue/<int:ajout_adblue_id>/detail/', ajout_adblue_detail_view, name='ajout_adblue_detail'),

    path("<int:pk>/detail/", ajout_adblue_detail_pdf_view, name="ajout_adblue_detail_pdf"),

    path("ajout_adblue/<int:ajout_adblue_id>/delete/", delete_ajout_adblue_view, name="delete_ajout_adblue"),

]

