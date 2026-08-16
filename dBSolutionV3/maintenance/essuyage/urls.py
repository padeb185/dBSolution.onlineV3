# maintenance/check_up/urls.py
from django.urls import path
from .views import EssuyageListView, essuyage_form_view, modifier_essuyage_view, essuyage_detail_view, \
    essuyage_detail_pdf_view

app_name = "essuyage"


urlpatterns = [

    path('essuyage/<uuid:exemplaire_id>/liste/', EssuyageListView.as_view(),name='essuyage_list'),

    path('essuyage/<uuid:exemplaire_id>/', essuyage_form_view, name='essuyage_form'),


    path('essuyage/<int:essuyage_id>/modifier/', modifier_essuyage_view, name='modifier_essuyage'),


    path('essuyage/<int:essuyage_id>/detail/', essuyage_detail_view, name='essuyage_detail'),

    path("<int:pk>/", essuyage_detail_pdf_view, name="essuyage_detail_pdf"),


]
