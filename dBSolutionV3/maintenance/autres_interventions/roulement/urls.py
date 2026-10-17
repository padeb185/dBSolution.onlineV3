from django.urls import path

from .views import (
    RoulementListView,
    roulement_check_view,
    roulement_detail_view,
    roulement_pdf_view,
    delete_roulement_view,
    modifier_roulement_view,
)

app_name = "roulement"

urlpatterns = [
    path("<uuid:exemplaire_id>/liste/", RoulementListView.as_view(), name="roulement_list"),
    path("<uuid:exemplaire_id>/", roulement_check_view, name="roulement_check"),
    path("<int:roulement_id>/detail/", roulement_detail_view, name="roulement_detail"),
    path("<int:roulement_id>/modifier/", modifier_roulement_view, name="modifier_roulement"),
    path("<int:roulement_id>/pdf/", roulement_pdf_view, name="roulement_pdf"),
    path("<int:roulement_id>/delete/", delete_roulement_view, name="delete_roulement"),
]
