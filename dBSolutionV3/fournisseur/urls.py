from django.urls import path
from .views import FournisseurListView, FournisseurCreateView, fournisseur_detail

app_name = "fournisseur"


urlpatterns = [
    path(
        "fournisseur/",
        FournisseurListView.as_view(),
        name="fournisseur_list",
    ),
    path(
        "fournisseur/creer/",
        FournisseurCreateView.as_view(),
        name="fournisseur_create",
    ),

path(
        "<uuid:fournisseur_id>/",
        fournisseur_detail,
        name="fournisseur_detail",
    ),
]
