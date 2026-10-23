# maintenance/check_up/urls.py
from django.urls import path
from .views import AideStationnementListView, aide_stationnement_form_view, modifier_aide_stationnement_view, aide_stationnement_detail_view, \
    aide_stationnement_detail_pdf_view, delete_aide_stationnement_view

app_name = "aide_stationnement"


urlpatterns = [

    path('aide_stationnement/<uuid:exemplaire_id>/liste/', AideStationnementListView.as_view(),name='aide_stationnement_list'),

    path('aide_stationnement/<uuid:exemplaire_id>/', aide_stationnement_form_view, name='aide_stationnement_form'),


    path('aide_stationnement/<int:aide_stationnement_id>/modifier/', modifier_aide_stationnement_view, name='modifier_aide_stationnement'),


    path('aide_stationnement/<int:aide_stationnement_id>/detail/', aide_stationnement_detail_view, name='aide_stationnement_detail'),

    path("<int:pk>/detail/", aide_stationnement_detail_pdf_view, name="aide_stationnement_detail_pdf"),

    path("aide_stationnement/<int:aide_stationnement_id>/delete/", delete_aide_stationnement_view, name="delete_aide_stationnement"),

]

