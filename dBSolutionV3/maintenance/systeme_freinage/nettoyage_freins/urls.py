# maintenance/check_up/urls.py
from django.urls import path
from .views import NettoyageFreinsListView, nettoyage_freins_form_view, modifier_nettoyage_freins_view, nettoyage_freins_detail_view, \
    nettoyage_freins_detail_pdf_view, delete_nettoyage_freins_view

app_name = "nettoyage_freins"


urlpatterns = [

    path('nettoyage_freins/<uuid:exemplaire_id>/liste/', NettoyageFreinsListView.as_view(),name='nettoyage_freins_list'),

    path('nettoyage_freins/<uuid:exemplaire_id>/', nettoyage_freins_form_view, name='nettoyage_freins_form'),


    path('nettoyage_freins/<int:nettoyage_freins_id>/modifier/', modifier_nettoyage_freins_view, name='modifier_nettoyage_freins'),


    path('nettoyage_freins/<int:nettoyage_freins_id>/detail/', nettoyage_freins_detail_view, name='nettoyage_freins_detail'),

    path("<int:pk>/detail/", nettoyage_freins_detail_pdf_view, name="nettoyage_freins_detail_pdf"),

    path("nettoyage_freins/<int:nettoyage_freins_id>/delete/", delete_nettoyage_freins_view, name="delete_nettoyage_freins"),

]

