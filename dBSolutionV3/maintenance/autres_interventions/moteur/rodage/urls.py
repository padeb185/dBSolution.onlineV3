from django.urls import path
from .views import RodageListView, rodage_check_view, modifier_rodage_view, rodage_detail_view, rodage_pdf_view

app_name = "rodage"



urlpatterns = [

    path('rodage/<uuid:exemplaire_id>/liste/', RodageListView.as_view(),name='rodage_list'),

    path('rodage/<uuid:exemplaire_id>/', rodage_check_view, name='rodage_check'),


    path('<uuid:rodage_id>/modifier/', modifier_rodage_view, name='modifier_rodage'),


    path('<uuid:rodage_id>/detail/', rodage_detail_view, name='rodage_detail'),

    path("rodage/<uuid:rodage_id>/pdf/", rodage_pdf_view, name="rodage_pdf"),
]




