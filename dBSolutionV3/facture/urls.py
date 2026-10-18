from django.urls import path

from . import views

app_name = "facture"

urlpatterns = [
    path("", views.maintenances_a_facturer_view, name="maintenances"),
    path("creer/", views.creer_facture_view, name="creer"),
    path("diagnostic/<uuid:diagnostic_id>/creer/", views.creer_facture_diagnostic_view, name="creer_diagnostic"),
    path("liste/", views.facture_list_view, name="liste"),
    path("tva/", views.tva_view, name="tva"),
    path("caisse-banque/", views.caisse_banque_view, name="caisse_banque"),
    path("a-payer/", views.factures_a_payer_view, name="a_payer"),
    path("parametres-peppol/", views.parametres_peppol_view, name="parametres_peppol"),
    path("<uuid:pk>/", views.facture_detail_view, name="detail"),
    path("<uuid:pk>/modifier/", views.facture_modifier_view, name="modifier"),
    path("<uuid:pk>/pdf/", views.facture_pdf_view, name="pdf"),
    path("<uuid:pk>/xml/", views.facture_xml_view, name="xml"),
    path("<uuid:pk>/peppol/", views.facture_envoyer_peppol_view, name="envoyer_peppol"),
    path("<uuid:pk>/paiement/", views.facture_paiement_view, name="paiement"),
    path("<uuid:pk>/supprimer/", views.delete_facture_view, name="delete_facture"),
]
