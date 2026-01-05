from django.urls import path
from . import views

app_name = "utilisateurs"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("totp/setup/", views.totp_setup_view, name="totp_setup"),
]
