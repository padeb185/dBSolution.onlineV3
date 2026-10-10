from django.urls import path

from .views import (
    CardanListView,
    cardan_check_view,
    cardan_detail_view,
    cardan_pdf_view,
    delete_cardan_view,
    modifier_cardan_view,
)

app_name = "cardan"

urlpatterns = [
    path("<uuid:exemplaire_id>/liste/", CardanListView.as_view(), name="cardan_list"),
    path("<uuid:exemplaire_id>/", cardan_check_view, name="cardan_check"),
    path("<int:cardan_id>/detail/", cardan_detail_view, name="cardan_detail"),
    path("<int:cardan_id>/modifier/", modifier_cardan_view, name="modifier_cardan"),
    path("<int:cardan_id>/pdf/", cardan_pdf_view, name="cardan_pdf"),
    path("<int:cardan_id>/delete/", delete_cardan_view, name="delete_cardan"),
]
