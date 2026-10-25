from django.urls import path

from . import views
from . import views_paie
from . import views_tenants
from . import views_mot_de_passe
from . import views_mon_compte


app_name = "utilisateurs"


urlpatterns = [
    # Connexion interne au tenant, seulement si elle reste nécessaire

    #path(
     #   "login/",
     #   views.login_view,
     #   name="login",
   # ),

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),

    # Tableau de bord du tenant
    path(
        "dashboard/",
        views.dashboard_view,
        name="dashboard",
    ),

    # Dashboard utilisateur (cartouche « Utilisateur » du tableau de bord)
    path(
        "mon-compte/",
        views_mon_compte.mon_compte_view,
        name="mon_compte",
    ),

    path(
        "totp/setup/",
        views.totp_setup_view,
        name="totp_setup",
    ),

    path(
        "creer/",
        views.creer_utilisateur,
        name="creer_utilisateur",
    ),

    path(
        "admin/dashboard/",
        views.dashboard_admin,
        name="dashboard_admin",
    ),

    path(
        "admin/utilisateurs/",
        views.liste_utilisateurs,
        name="liste_utilisateurs",
    ),

    path(
        "admin/utilisateurs/<uuid:pk>/reinitialiser-mot-de-passe/",
        views_mot_de_passe.envoyer_lien_reinitialisation,
        name="envoyer_reinitialisation",
    ),

    # -------------------------
    # ADMINISTRATION DES TENANTS
    # -------------------------
    path("admin/tenants/", views_tenants.tenants_liste, name="tenants_liste"),
    path("admin/tenants/creer/", views_tenants.tenant_creer, name="tenant_creer"),
    path("admin/tenants/<int:pk>/", views_tenants.tenant_detail, name="tenant_detail"),
    path("admin/tenants/<int:pk>/modifier/", views_tenants.tenant_modifier, name="tenant_modifier"),
    path("admin/tenants/<int:pk>/utilisateur/creer/", views_tenants.tenant_utilisateur_creer,
         name="tenant_utilisateur_creer"),
    path("admin/tenants/<int:pk>/utilisateur/<uuid:utilisateur_id>/activer/",
         views_tenants.tenant_utilisateur_activer, name="tenant_utilisateur_activer"),

    # IBAN d'un utilisateur (contrôle + mise en forme)
    path(
        "admin/utilisateurs/<uuid:pk>/iban/",
        views.modifier_iban_utilisateur,
        name="modifier_iban",
    ),

    # -------------------------
    # PAIES MENSUELLES
    # -------------------------
    path("paie/", views_paie.paie_panneau, name="paie_panneau"),
    path("paie/liste/", views_paie.paie_list, name="paie_list"),
    path(
        "paie/travailleur/<uuid:utilisateur_id>/",
        views_paie.paie_list_travailleur,
        name="paie_list_travailleur",
    ),
    path("paie/creer/", views_paie.creer_paie_utilisateur, name="creer_paie_utilisateur"),
    path("paie/<int:pk>/", views_paie.paie_detail, name="paie_detail"),
    path("paie/<int:pk>/pdf/", views_paie.paie_pdf, name="paie_pdf"),
    path("paie/<int:pk>/modifier/", views_paie.modifier_paie, name="modifier_paie"),
    path("paie/<int:pk>/supprimer/", views_paie.delete_paie, name="delete_paie"),
    path("paie/<int:pk>/payer/", views_paie.paie_payer, name="paie_payer"),
    path("paie/comptabilite/", views_paie.paie_comptabilite, name="paie_comptabilite"),
    path("paie/cout-main-oeuvre/", views_paie.cout_main_oeuvre, name="cout_main_oeuvre"),
    path("paie/comptabilite/export.csv", views_paie.paie_comptabilite_csv, name="paie_comptabilite_csv"),
]