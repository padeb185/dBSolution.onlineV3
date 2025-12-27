from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from theme.views import home
from authentification.views import login_totp, totp_setup

urlpatterns = [
    # Admin global
    path("admin/", admin.site.urls),

    # Accueil public
    path("", home, name="home"),

    # Authentification
    #path("login/", auth_views.LoginView.as_view(
     #   template_name="login.html"
    #), name="login"),

    path("login/totp/", login_totp, name="login_totp"),
    path("login/totp/setup/", totp_setup, name="totp_setup"),

    # Auth app
    path("auth/", include("authentification.urls")),

    path("voitures/marques/", include("voiture.voiture_marque.urls")),
]
