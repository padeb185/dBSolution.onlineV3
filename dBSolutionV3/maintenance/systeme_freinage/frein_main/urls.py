# maintenance/check_up/urls.py
from django.urls import path
from .views import FreinMainListView, frein_main_form_view, modifier_frein_main_view, frein_main_detail_view, \
    frein_main_detail_pdf_view, delete_frein_main_view

app_name = "frein_main"


urlpatterns = [

    path('frein_main/<uuid:exemplaire_id>/liste/', FreinMainListView.as_view(),name='frein_main_list'),

    path('frein_main/<uuid:exemplaire_id>/', frein_main_form_view, name='frein_main_form'),


    path('frein_main/<int:frein_main_id>/modifier/', modifier_frein_main_view, name='modifier_frein_main'),


    path('frein_main/<int:frein_main_id>/detail/', frein_main_detail_view, name='frein_main_detail'),

    path("<int:pk>/detail/", frein_main_detail_pdf_view, name="frein_main_detail_pdf"),

    path("frein_main/<int:frein_main_id>/delete/", delete_frein_main_view, name="delete_frein_main"),

]

