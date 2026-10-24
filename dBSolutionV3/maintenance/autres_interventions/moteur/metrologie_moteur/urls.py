from django.urls import path

from .views import (
    MetrologieMoteurListView, delete_metrologie_view, metrologie_detail_pdf_view, metrologie_detail_view,
    metrologie_form_view, modifier_metrologie_view,
)

app_name = "metrologie_moteur"

urlpatterns = [
    path("metrologie/<uuid:exemplaire_id>/liste/", MetrologieMoteurListView.as_view(), name="metrologie_list"),
    path("metrologie/<uuid:exemplaire_id>/", metrologie_form_view, name="metrologie_form"),
    path("metrologie/<int:metrologie_id>/modifier/", modifier_metrologie_view, name="modifier_metrologie"),
    path("metrologie/<int:metrologie_id>/detail/", metrologie_detail_view, name="metrologie_detail"),
    path("<int:pk>/detail/", metrologie_detail_pdf_view, name="metrologie_detail_pdf"),
    path("metrologie/<int:metrologie_id>/delete/", delete_metrologie_view, name="delete_metrologie"),
]
