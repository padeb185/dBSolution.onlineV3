from django.urls import path

from .views import (
    BancPuissanceListView,
    banc_check_view,
    banc_detail_view,
    banc_pdf_view,
    delete_banc_view,
    banc_document_view,
    modifier_banc_view,
)

app_name = "banc_puissance"

urlpatterns = [
    path("<uuid:exemplaire_id>/liste/", BancPuissanceListView.as_view(), name="banc_list"),
    path("<uuid:exemplaire_id>/", banc_check_view, name="banc_check"),
    path("<int:banc_id>/detail/", banc_detail_view, name="banc_detail"),
    path("<int:banc_id>/modifier/", modifier_banc_view, name="modifier_banc"),
    path("<int:banc_id>/pdf/", banc_pdf_view, name="banc_pdf"),
    path("<int:banc_id>/delete/", delete_banc_view, name="delete_banc"),
    path("<int:banc_id>/courbe/<str:document>.pdf", banc_document_view, name="banc_document"),
]
