# maintenance/check_up/urls.py
from django.urls import path
from .views import FreinMainHydrauliqueListView, frein_main_hydraulique_form_view, modifier_frein_main_hydraulique_view, frein_main_hydraulique_detail_view, \
    frein_main_hydraulique_detail_pdf_view, delete_frein_main_hydraulique_view

app_name = "frein_main_hydraulique"


urlpatterns = [

    path('frein_main_hydraulique/<uuid:exemplaire_id>/liste/', FreinMainHydrauliqueListView.as_view(),name='frein_main_hydraulique_list'),

    path('frein_main_hydraulique/<uuid:exemplaire_id>/', frein_main_hydraulique_form_view, name='frein_main_hydraulique_form'),


    path('frein_main_hydraulique/<int:frein_main_hydraulique_id>/modifier/', modifier_frein_main_hydraulique_view, name='modifier_frein_main_hydraulique'),


    path('frein_main_hydraulique/<int:frein_main_hydraulique_id>/detail/', frein_main_hydraulique_detail_view, name='frein_main_hydraulique_detail'),

    path("<int:pk>/detail/", frein_main_hydraulique_detail_pdf_view, name="frein_main_hydraulique_detail_pdf"),

    path("frein_main_hydraulique/<int:frein_main_hydraulique_id>/delete/", delete_frein_main_hydraulique_view, name="delete_frein_main_hydraulique"),

]

