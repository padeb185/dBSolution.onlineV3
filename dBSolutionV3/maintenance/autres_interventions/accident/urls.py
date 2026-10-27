from django.urls import path

from .views import (
    RapportAccidentListView, accident_detail_view, accident_form_view, accident_pdf_view,
    delete_accident_view, modifier_accident_view,
)

app_name = "accident"

urlpatterns = [
    path("<uuid:exemplaire_id>/liste/", RapportAccidentListView.as_view(), name="accident_list"),
    path("<uuid:exemplaire_id>/", accident_form_view, name="accident_form"),
    path("<int:accident_id>/modifier/", modifier_accident_view, name="modifier_accident"),
    path("<int:accident_id>/detail/", accident_detail_view, name="accident_detail"),
    path("<int:pk>/pdf/", accident_pdf_view, name="accident_pdf"),
    path("<int:accident_id>/delete/", delete_accident_view, name="delete_accident"),
]
