from django.urls import path

from .views import (
    ArbreTransmissionListView,
    arbre_check_view,
    arbre_detail_view,
    arbre_pdf_view,
    delete_arbre_view,
    modifier_arbre_view,
)

app_name = "arbre_transmission"

urlpatterns = [
    path("<uuid:exemplaire_id>/liste/", ArbreTransmissionListView.as_view(), name="arbre_list"),
    path("<uuid:exemplaire_id>/", arbre_check_view, name="arbre_check"),
    path("<int:arbre_id>/detail/", arbre_detail_view, name="arbre_detail"),
    path("<int:arbre_id>/modifier/", modifier_arbre_view, name="modifier_arbre"),
    path("<int:arbre_id>/pdf/", arbre_pdf_view, name="arbre_pdf"),
    path("<int:arbre_id>/delete/", delete_arbre_view, name="delete_arbre"),
]
