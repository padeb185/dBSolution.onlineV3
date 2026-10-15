# maintenance/check_up/urls.py
from django.urls import path
from .views import TamboursListView, tambours_form_view, modifier_tambours_view, tambours_detail_view, \
    tambours_detail_pdf_view, delete_tambours_view

app_name = "tambours"


urlpatterns = [

    path('tambours/<uuid:exemplaire_id>/liste/', TamboursListView.as_view(),name='tambours_list'),

    path('tambours/<uuid:exemplaire_id>/', tambours_form_view, name='tambours_form'),


    path('tambours/<int:tambours_id>/modifier/', modifier_tambours_view, name='modifier_tambours'),


    path('tambours/<int:tambours_id>/detail/', tambours_detail_view, name='tambours_detail'),

    path("<int:pk>/detail/", tambours_detail_pdf_view, name="tambours_detail_pdf"),

    path("tambours/<int:tambours_id>/delete/", delete_tambours_view, name="delete_tambours"),

]

