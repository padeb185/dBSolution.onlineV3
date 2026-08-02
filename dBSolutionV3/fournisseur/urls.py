from django.urls import path

from .views import (
    FournisseurListView,
    ajouter_fournisseur_all,
    check_nom_fournisseur_view,
    fournisseur_dashboard_view,
    fournisseur_detail,
    modifier_fournisseur,
)

app_name = "fournisseur"

urlpatterns = [
    path(
        "",
        fournisseur_dashboard_view,
        name="fournisseur_dashboard",
    ),

    path(
        "liste/",
        FournisseurListView.as_view(),
        name="fournisseur_list",
    ),

    path(
        "creer/",
        ajouter_fournisseur_all,
        name="fournisseur_form",
    ),

    path(
        "<uuid:fournisseur_id>/",
        fournisseur_detail,
        name="fournisseur_detail",
    ),

    path(
        "<uuid:fournisseur_id>/modifier/",
        modifier_fournisseur,
        name="modifier_fournisseur",
    ),

    path(
        "api/check-nom/",
        check_nom_fournisseur_view,
        name="check_nom_fournisseur",
    ),
]