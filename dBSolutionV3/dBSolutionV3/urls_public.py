from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from theme.views import home
from authentification.views import login_totp, totp_setup


urlpatterns = [
    path("", home, name="home"),

    path("login/", auth_views.LoginView.as_view(
        template_name="login.html"
    ), name="login"),

    path("auth/", include("authentification.urls", namespace="authentification")),


    path("voitures/marques/", include("voiture.voiture_marque.urls")),
]
