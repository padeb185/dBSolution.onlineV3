# maintenance/check_up/urls.py
from django.urls import path
from .views import CireListView, cire_form_view, modifier_cire_view, cire_detail_view, \
    cire_detail_pdf_view, delete_cire_view

app_name = "cire"


urlpatterns = [

    path('cire/<uuid:exemplaire_id>/liste/', CireListView.as_view(),name='cire_list'),

    path('cire/<uuid:exemplaire_id>/', cire_form_view, name='cire_form'),


    path('cire/<int:cire_id>/modifier/', modifier_cire_view, name='modifier_cire'),


    path('cire/<int:cire_id>/detail/', cire_detail_view, name='cire_detail'),

    path("<int:pk>/detail/", cire_detail_pdf_view, name="cire_detail_pdf"),

    path("cire/<int:cire_id>/delete/", delete_cire_view, name="delete_cire"),

]

