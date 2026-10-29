# maintenance/check_up/urls.py
from django.urls import path
from .views import PompeAdblueListView, pompe_adblue_form_view, modifier_pompe_adblue_view, pompe_adblue_detail_view, \
    pompe_adblue_detail_pdf_view, delete_pompe_adblue_view

app_name = "pompe_adblue"


urlpatterns = [

    path('pompe_adblue/<uuid:exemplaire_id>/liste/', PompeAdblueListView.as_view(),name='pompe_adblue_list'),

    path('pompe_adblue/<uuid:exemplaire_id>/', pompe_adblue_form_view, name='pompe_adblue_form'),


    path('pompe_adblue/<int:pompe_adblue_id>/modifier/', modifier_pompe_adblue_view, name='modifier_pompe_adblue'),


    path('pompe_adblue/<int:pompe_adblue_id>/detail/', pompe_adblue_detail_view, name='pompe_adblue_detail'),

    path("<int:pk>/detail/", pompe_adblue_detail_pdf_view, name="pompe_adblue_detail_pdf"),

    path("pompe_adblue/<int:pompe_adblue_id>/delete/", delete_pompe_adblue_view, name="delete_pompe_adblue"),

]

