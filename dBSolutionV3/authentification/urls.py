from django.urls import path
from django.contrib.auth import views as auth_views
from authentification.views import login_totp, totp_setup
from theme.views import home, dashboard

app_name = "authentification"

urlpatterns = [
    # Page d'accueil
    path("", home, name="home"),

    # Login principal (email + mot de passe)
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),

    # Setup TOTP (pour nouveaux utilisateurs)
    path("login/totp/setup/", totp_setup, name="totp_setup"),

    # Login avec TOTP
    path("login/totp/", login_totp, name="login_totp"),

    # Dashboard (après login complet)
    path("dashboard/", dashboard, name="dashboard"),
]
