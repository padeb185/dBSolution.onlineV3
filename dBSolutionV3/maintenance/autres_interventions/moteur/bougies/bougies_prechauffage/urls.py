# maintenance/check_up/urls.py
from django.urls import path
from .views import BougiesPrechauffageListView, bougies_prechauffage_form_view, modifier_bougies_prechauffage_view, bougies_prechauffage_detail_view, \
    bougies_prechauffage_detail_pdf_view, delete_bougies_prechauffage_view

app_name = "bougies_prechauffage"


urlpatterns = [

    path('bougies_prechauffage/<uuid:exemplaire_id>/liste/', BougiesPrechauffageListView.as_view(),name='bougies_prechauffage_list'),

    path('bougies_prechauffage/<uuid:exemplaire_id>/', bougies_prechauffage_form_view, name='bougies_prechauffage_form'),


    path('bougies_prechauffage/<int:bougies_prechauffage_id>/modifier/', modifier_bougies_prechauffage_view, name='modifier_bougies_prechauffage'),


    path('bougies_prechauffage/<int:bougies_prechauffage_id>/detail/', bougies_prechauffage_detail_view, name='bougies_prechauffage_detail'),

    path("<int:pk>/detail/", bougies_prechauffage_detail_pdf_view, name="bougies_prechauffage_detail_pdf"),

    path("bougies_prechauffage/<int:bougies_prechauffage_id>/delete/", delete_bougies_prechauffage_view, name="delete_bougies_prechauffage"),

]

