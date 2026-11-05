# maintenance/autres_interventions/boitier_electronique/urls.py
from django.urls import path
from .views import BoitierElectroniqueListView, boitier_form_view, modifier_boitier_view, boitier_detail_view, \
    boitier_detail_pdf_view, delete_boitier_view

app_name = "boitier_electronique"


urlpatterns = [

    path('boitier_electronique/<uuid:exemplaire_id>/liste/', BoitierElectroniqueListView.as_view(),name='boitier_list'),

    path('boitier_electronique/<uuid:exemplaire_id>/', boitier_form_view, name='boitier_form'),


    path('boitier_electronique/<int:boitier_id>/modifier/', modifier_boitier_view, name='modifier_boitier'),


    path('boitier_electronique/<int:boitier_id>/detail/', boitier_detail_view, name='boitier_detail'),

    path("<int:pk>/detail/", boitier_detail_pdf_view, name="boitier_detail_pdf"),

    path("boitier_electronique/<int:boitier_id>/delete/", delete_boitier_view, name="delete_boitier"),

]

