from django.urls import path
from .views import login_view, dashboard_view, totp_setup_view
from dBSolutionV3.views import home_view

app_name = "utilisateurs"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("home/" ,home_view, name="home"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("totp/setup/", totp_setup_view, name="totp_setup"),
]
