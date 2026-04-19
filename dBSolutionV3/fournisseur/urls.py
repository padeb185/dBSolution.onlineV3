from django.urls import path
from .views import FournisseurListView, fournisseur_detail, ajouter_fournisseur_all, modifier_fournisseur, \
    fournisseur_dashboard_view, fournisseur_achat_view, AchatMdsListView

app_name = "fournisseur"

urlpatterns = [
    path('', fournisseur_dashboard_view, name='fournisseur_dashboard'),

    path(
        "fournisseur/",
        FournisseurListView.as_view(),
        name="fournisseur_list",
    ),

    path(
        "fournisseur/",
        AchatMdsListView.as_view(),
        name="achat_list",
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

    path(
        'fournisseurs/<uuid:fournisseur_id>/modifier/',
        modifier_fournisseur,
        name='modifier_fournisseur'),

    path(
        'fournisseurs/achat/',
        fournisseur_achat_view,
        name='fournisseur_achat'),




]
