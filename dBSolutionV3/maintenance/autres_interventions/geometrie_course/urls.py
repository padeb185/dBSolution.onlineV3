from django.urls import path

from .views import (
    GeometrieCourseListView,
    geocourse_check_view,
    geocourse_detail_view,
    geocourse_pdf_view,
    delete_geocourse_view,
    modifier_geocourse_view,
)

app_name = "geometrie_course"

urlpatterns = [
    path("<uuid:exemplaire_id>/liste/", GeometrieCourseListView.as_view(), name="geocourse_list"),
    path("<uuid:exemplaire_id>/", geocourse_check_view, name="geocourse_check"),
    path("<int:geo_id>/detail/", geocourse_detail_view, name="geocourse_detail"),
    path("<int:geo_id>/modifier/", modifier_geocourse_view, name="modifier_geocourse"),
    path("<int:geo_id>/pdf/", geocourse_pdf_view, name="geocourse_pdf"),
    path("<int:geo_id>/delete/", delete_geocourse_view, name="delete_geocourse"),
]
