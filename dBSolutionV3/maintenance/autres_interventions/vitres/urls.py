from django.urls import path

from .views import (
    VitrageListView,
    vitrage_check_view,
    vitrage_detail_view,
    vitrage_pdf_view,
    delete_vitrage_view,
    modifier_vitrage_view,
)

app_name = "vitrage"

urlpatterns = [
    path("<uuid:exemplaire_id>/liste/", VitrageListView.as_view(), name="vitrage_list"),
    path("<uuid:exemplaire_id>/", vitrage_check_view, name="vitrage_check"),
    path("<int:vitrage_id>/detail/", vitrage_detail_view, name="vitrage_detail"),
    path("<int:vitrage_id>/modifier/", modifier_vitrage_view, name="modifier_vitrage"),
    path("<int:vitrage_id>/pdf/", vitrage_pdf_view, name="vitrage_pdf"),
    path("<int:vitrage_id>/delete/", delete_vitrage_view, name="delete_vitrage"),
]
