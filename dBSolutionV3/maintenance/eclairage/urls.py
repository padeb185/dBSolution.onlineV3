# maintenance/eclairage/urls.py
from django.urls import path
from maintenance.eclairage.views import EclairageListView, eclairage_check_view, modifier_eclairage_view, \
    eclairage_detail_view, eclairage_pdf_view, delete_eclairage_view

app_name = "eclairage"



urlpatterns = [

    path('eclairage/<uuid:exemplaire_id>/liste/', EclairageListView.as_view(),name='eclairage_list'),

    path('eclairage/<uuid:exemplaire_id>/', eclairage_check_view, name='eclairage_check_view'),


    path('<uuid:eclairage_id>/modifier/', modifier_eclairage_view, name='modifier_eclairage'),


    path('<uuid:eclairage_id>/detail/', eclairage_detail_view, name='eclairage_detail'),

    path("eclairage/<uuid:eclairage_id>/pdf/", eclairage_pdf_view, name="eclairage_detail_pdf"),

    path("eclairage/<uuid:eclairage_id>/delete/", delete_eclairage_view, name="delete_eclairage"),

]
