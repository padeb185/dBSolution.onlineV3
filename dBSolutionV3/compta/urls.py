from django.urls import path

from . import views, views_bilan as vb, views_immo as vim, views_instructeur as vi

app_name = "compta"

urlpatterns = [
    path("", views.compta_tableau_de_bord, name="tableau_de_bord"),
    path("comptes/ouvrir/", views.compte_ouvrir, name="compte_ouvrir"),
    path("comptes/<uuid:pk>/", views.compte_journal, name="compte_journal"),
    path("comptes/<uuid:pk>/modifier/", views.compte_modifier, name="compte_modifier"),
    path("comptes/<uuid:pk>/supprimer/", views.compte_supprimer, name="compte_supprimer"),
    path("comptes/<uuid:pk>/mouvement/", views.mouvement_ajouter, name="mouvement_ajouter"),
    path("mouvements/<uuid:pk>/modifier/", views.mouvement_modifier, name="mouvement_modifier"),
    path("mouvements/<uuid:pk>/supprimer/", views.mouvement_supprimer, name="mouvement_supprimer"),
    path("virement/", views.virement_interne, name="virement_interne"),

    # Immobilisations / amortissements, stock, salaires, journal général
    path("immobilisations/", vim.immobilisations_liste, name="immobilisations_liste"),
    path("immobilisations/ajouter/", vim.immobilisation_ajouter, name="immobilisation_ajouter"),
    path("immobilisations/<uuid:pk>/", vim.immobilisation_detail, name="immobilisation_detail"),
    path("immobilisations/<uuid:pk>/modifier/", vim.immobilisation_modifier, name="immobilisation_modifier"),
    path("immobilisations/<uuid:pk>/supprimer/", vim.immobilisation_supprimer, name="immobilisation_supprimer"),
    path("stock/", vim.stock_compta, name="stock_compta"),
    path("stock/<uuid:pk>/supprimer/", vim.stock_supprimer, name="stock_supprimer"),
    path("salaires/", vim.salaires_compta, name="salaires_compta"),
    path("salaires/versements/<uuid:pk>/supprimer/", vim.versement_supprimer, name="versement_supprimer"),
    path("journal/", vim.journal_general, name="journal_general"),
    path("bilan/", vb.bilan, name="bilan"),
    path("bilan/pdf/", vb.bilan_pdf, name="bilan_pdf"),
    path("bilan/dernier/", vb.references_liste, name="references_liste"),
    path("bilan/dernier/ajouter/", vb.reference_ajouter, name="reference_ajouter"),
    path("bilan/dernier/<uuid:pk>/modifier/", vb.reference_modifier, name="reference_modifier"),
    path("bilan/dernier/<uuid:pk>/supprimer/", vb.reference_supprimer, name="reference_supprimer"),
    path("operations-diverses/", vb.od_liste, name="od_liste"),
    path("operations-diverses/ajouter/", vb.od_ajouter, name="od_ajouter"),
    path("operations-diverses/<uuid:pk>/modifier/", vb.od_modifier, name="od_modifier"),
    path("operations-diverses/<uuid:pk>/supprimer/", vb.od_supprimer, name="od_supprimer"),

    # Instructeurs indépendants (factures d'achat / autofacturation)
    path("instructeurs/", vi.instructeurs_liste, name="instructeurs_liste"),
    path("instructeurs/<uuid:utilisateur_id>/profil/", vi.profil_instructeur, name="profil_instructeur"),
    path("instructeurs/factures/", vi.factures_instructeurs, name="factures_instructeurs"),
    path("instructeurs/factures/creer/", vi.facture_instructeur_creer, name="facture_instructeur_creer"),
    path("instructeurs/factures/<uuid:pk>/", vi.facture_instructeur_detail, name="facture_instructeur_detail"),
    path("instructeurs/factures/<uuid:pk>/modifier/", vi.facture_instructeur_modifier, name="facture_instructeur_modifier"),
    path("instructeurs/factures/<uuid:pk>/emettre/", vi.facture_instructeur_emettre, name="facture_instructeur_emettre"),
    path("instructeurs/factures/<uuid:pk>/payer/", vi.facture_instructeur_payer, name="facture_instructeur_payer"),
    path("instructeurs/factures/<uuid:pk>/annuler-paiement/", vi.facture_instructeur_annuler_paiement, name="facture_instructeur_annuler_paiement"),
    path("instructeurs/factures/<uuid:pk>/supprimer/", vi.facture_instructeur_supprimer, name="facture_instructeur_supprimer"),
    path("instructeurs/factures/<uuid:pk>/pdf/", vi.facture_instructeur_pdf, name="facture_instructeur_pdf"),
]
