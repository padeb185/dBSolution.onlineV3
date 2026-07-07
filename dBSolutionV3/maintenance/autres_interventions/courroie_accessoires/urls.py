from django.urls import path
from maintenance.autres_interventions.courroie_accessoires.views import CourroieAccessoiresListView, \
    courroie_access_form_view, modifier_courroie_access_view, courroie_access_detail_view, rapport_courroie_access_view, \
    CourroieAccessoiresRapportDetailView, courroie_access_detail_pdf_view

urlpatterns = [
    path(
        "courroie_accessoires/<uuid:exemplaire_id>/liste/",
        CourroieAccessoiresListView.as_view(),
        name="courroie_list",
    ),

    path(
        "courroie_accessoires/<uuid:exemplaire_id>/",
        courroie_access_form_view,
        name="courroie_access_form",
    ),

    path(
        "courroie_accessoires/<int:courroie_id>/modifier/",
        modifier_courroie_access_view,
        name="modifier_courroie",
    ),

    path(
        "courroie_accessoires/<int:courroie_id>/detail/",
        courroie_access_detail_view,
        name="courroie_access_detail",
    ),

    path(
        "courroie_accessoires/<int:pk>/rapport/",
        rapport_courroie_access_view,
        name="rapport_courroie",
    ),

    path(
        "courroie_accessoires/<int:pk>/rapport/pdf/",
        CourroieAccessoiresRapportDetailView.as_view(),
        name="rapport_pdf_courroie",
    ),

    path(
        "courroie_accessoires/<int:pk>/detail/pdf/",
        courroie_access_detail_pdf_view,
        name="courroie_detail_pdf",
    ),
]
