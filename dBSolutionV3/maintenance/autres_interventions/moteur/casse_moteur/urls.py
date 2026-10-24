from django.urls import path

from .views import (
    CasseMoteurListView, delete_casse_view, casse_detail_pdf_view, casse_detail_view,
    casse_form_view, modifier_casse_view,
)

app_name = "casse_moteur"

urlpatterns = [
    path("casse/<uuid:exemplaire_id>/liste/", CasseMoteurListView.as_view(), name="casse_list"),
    path("casse/<uuid:exemplaire_id>/", casse_form_view, name="casse_form"),
    path("casse/<int:casse_id>/modifier/", modifier_casse_view, name="modifier_casse"),
    path("casse/<int:casse_id>/detail/", casse_detail_view, name="casse_detail"),
    path("<int:pk>/detail/", casse_detail_pdf_view, name="casse_detail_pdf"),
    path("casse/<int:casse_id>/delete/", delete_casse_view, name="delete_casse"),
]
