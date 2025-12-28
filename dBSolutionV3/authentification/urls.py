from django.urls import path
from .views import login_totp, totp_setup

app_name = "authentification"

urlpatterns = [
    path("login/totp/", login_totp, name="login_totp"),
    path("login/totp/setup/", totp_setup, name="totp_setup"),
]
