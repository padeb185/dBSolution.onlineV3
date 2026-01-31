from django.urls import path
from .views import FournisseurListView, fournisseur_detail, ajouter_fournisseur_all

app_name = "fournisseur"


urlpatterns = [
    path(
        "fournisseur/",
        FournisseurListView.as_view(),
        name="fournisseur_list",
    ),
    path(
        "fournisseur/creer/",
        ajouter_fournisseur_all,
        name="fournisseur_create",
    ),

path(
        "<uuid:fournisseur_id>/",
        fournisseur_detail,
        name="fournisseur_detail",
    ),
]
