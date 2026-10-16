from django.urls import path

from . import views
from . import views_paie


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
    path("paie/<int:pk>/modifier/", views_paie.modifier_paie, name="modifier_paie"),
    path("paie/<int:pk>/supprimer/", views_paie.delete_paie, name="delete_paie"),
    path("paie/<int:pk>/payer/", views_paie.paie_payer, name="paie_payer"),
    path("paie/comptabilite/", views_paie.paie_comptabilite, name="paie_comptabilite"),
    path("paie/comptabilite/export.csv", views_paie.paie_comptabilite_csv, name="paie_comptabilite_csv"),
]