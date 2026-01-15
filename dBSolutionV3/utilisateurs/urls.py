from django.urls import path
from . import views

app_name = "utilisateurs"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("tenant/", views.dashboard_view, name="dashboard"),  # dashboard après login
    path("totp/setup/", views.totp_setup_view, name="totp_setup"),
    path("utilisateur/creer/", views.creer_utilisateur, name="creer_utilisateur"),
    path("admin/dashboard/", views.dashboard_admin, name="dashboard_admin"),
    path("admin/utilisateurs/", views.liste_utilisateurs, name="liste_utilisateurs"),
]
