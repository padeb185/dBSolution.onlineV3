# authentification/urls.py
from django.urls import path
from .views import login_totp, totp_setup

urlpatterns = [
    path('login/totp/', login_totp, name='login_totp'),
    path('login/totp/setup/', totp_setup, name='totp_setup'),
]
