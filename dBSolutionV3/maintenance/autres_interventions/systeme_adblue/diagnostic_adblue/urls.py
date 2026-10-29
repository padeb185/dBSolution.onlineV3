# maintenance/check_up/urls.py
from django.urls import path
from .views import DiagnosticAdblueListView, diagnostic_adblue_form_view, modifier_diagnostic_adblue_view, diagnostic_adblue_detail_view, \
    diagnostic_adblue_detail_pdf_view, delete_diagnostic_adblue_view

app_name = "diagnostic_adblue"


urlpatterns = [

    path('diagnostic_adblue/<uuid:exemplaire_id>/liste/', DiagnosticAdblueListView.as_view(),name='diagnostic_adblue_list'),

    path('diagnostic_adblue/<uuid:exemplaire_id>/', diagnostic_adblue_form_view, name='diagnostic_adblue_form'),


    path('diagnostic_adblue/<int:diagnostic_adblue_id>/modifier/', modifier_diagnostic_adblue_view, name='modifier_diagnostic_adblue'),


    path('diagnostic_adblue/<int:diagnostic_adblue_id>/detail/', diagnostic_adblue_detail_view, name='diagnostic_adblue_detail'),

    path("<int:pk>/detail/", diagnostic_adblue_detail_pdf_view, name="diagnostic_adblue_detail_pdf"),

    path("diagnostic_adblue/<int:diagnostic_adblue_id>/delete/", delete_diagnostic_adblue_view, name="delete_diagnostic_adblue"),

]

