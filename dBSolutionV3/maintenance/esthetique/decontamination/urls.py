# maintenance/check_up/urls.py
from django.urls import path
from .views import DecontaminationListView, decontamination_form_view, modifier_decontamination_view, decontamination_detail_view, \
    decontamination_detail_pdf_view, delete_decontamination_view

app_name = "decontamination"


urlpatterns = [

    path('decontamination/<uuid:exemplaire_id>/liste/', DecontaminationListView.as_view(),name='decontamination_list'),

    path('decontamination/<uuid:exemplaire_id>/', decontamination_form_view, name='decontamination_form'),


    path('decontamination/<int:decontamination_id>/modifier/', modifier_decontamination_view, name='modifier_decontamination'),


    path('decontamination/<int:decontamination_id>/detail/', decontamination_detail_view, name='decontamination_detail'),

    path("<int:pk>/detail/", decontamination_detail_pdf_view, name="decontamination_detail_pdf"),

    path("decontamination/<int:decontamination_id>/delete/", delete_decontamination_view, name="delete_decontamination"),

]

