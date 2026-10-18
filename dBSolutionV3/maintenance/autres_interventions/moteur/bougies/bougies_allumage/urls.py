# maintenance/check_up/urls.py
from django.urls import path
from .views import BougiesAllumageListView, bougies_allumage_form_view, modifier_bougies_allumage_view, bougies_allumage_detail_view, \
    bougies_allumage_detail_pdf_view, delete_bougies_allumage_view

app_name = "bougies_allumage"


urlpatterns = [

    path('bougies_allumage/<uuid:exemplaire_id>/liste/', BougiesAllumageListView.as_view(),name='bougies_allumage_list'),

    path('bougies_allumage/<uuid:exemplaire_id>/', bougies_allumage_form_view, name='bougies_allumage_form'),


    path('bougies_allumage/<int:bougies_allumage_id>/modifier/', modifier_bougies_allumage_view, name='modifier_bougies_allumage'),


    path('bougies_allumage/<int:bougies_allumage_id>/detail/', bougies_allumage_detail_view, name='bougies_allumage_detail'),

    path("<int:pk>/detail/", bougies_allumage_detail_pdf_view, name="bougies_allumage_detail_pdf"),

    path("bougies_allumage/<int:bougies_allumage_id>/delete/", delete_bougies_allumage_view, name="delete_bougies_allumage"),

]

