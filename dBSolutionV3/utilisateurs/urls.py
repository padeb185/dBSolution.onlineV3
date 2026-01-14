from django.urls import path
from . import views
from .views import creer_utilisateur, dashboard_admin, liste_utilisateurs

app_name = "utilisateurs"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('tenant/', views.dashboard_view, name='dashboard'),
    path("totp/setup/", views.totp_setup_view, name="totp_setup"),
    path("utilisateur/creer/", creer_utilisateur, name="creer_utilisateur"),
    path("admin/dashboard/", dashboard_admin, name="dashboard_admin"),
    path("admin/utilisateurs/", liste_utilisateurs, name="liste_utilisateurs"),
    path('admin/creer/', views.creer_utilisateur, name='creer_utilisateur'),


]
