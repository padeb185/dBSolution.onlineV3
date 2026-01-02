from django.urls import path
from .views import login_view, dashboard_view, totp_setup_view, logout_view
from dBSolutionV3.views import home_view

app_name = "utilisateurs"

urlpatterns = [

    path("login/", login_view, name="login"),  # Login
    path("dashboard/", dashboard_view, name="dashboard"),  # Dashboard
    path("logout/", logout_view, name="logout"),  # Logout
    path("totp/setup/", totp_setup_view, name="totp_setup"),
]
