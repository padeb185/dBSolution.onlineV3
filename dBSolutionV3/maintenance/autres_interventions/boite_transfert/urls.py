from django.urls import path

from .views import (
    BoiteTransfertListView,
    transfert_check_view,
    transfert_detail_view,
    transfert_pdf_view,
    delete_transfert_view,
    modifier_transfert_view,
)

app_name = "boite_transfert"

urlpatterns = [
    path("<uuid:exemplaire_id>/liste/", BoiteTransfertListView.as_view(), name="transfert_list"),
    path("<uuid:exemplaire_id>/", transfert_check_view, name="transfert_check"),
    path("<int:transfert_id>/detail/", transfert_detail_view, name="transfert_detail"),
    path("<int:transfert_id>/modifier/", modifier_transfert_view, name="modifier_transfert"),
    path("<int:transfert_id>/pdf/", transfert_pdf_view, name="transfert_pdf"),
    path("<int:transfert_id>/delete/", delete_transfert_view, name="delete_transfert"),
]
