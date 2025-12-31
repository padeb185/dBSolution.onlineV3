from django.contrib import admin
from django.urls import path, include
from theme.views import home
from utilisateurs import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", home, name="home"),

    # Login uniquement via TOTP
    path('login/', views.login_totp_view, name='login'),

    # Configuration du TOTP pour les utilisateurs
    path('totp/setup/', views.totp_setup, name='totp_setup'),

    # Password reset
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
        name="password_reset"
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
        name="password_reset_done"
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),
        name="password_reset_confirm"
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
        name="password_reset_complete"
    ),

    # Namespace pour ton app utilisateurs
    path("auth/", include("utilisateurs.urls", namespace="authentification")),

    # Autres routes
    path("voitures/marques/", include("voiture.voiture_marque.urls")),
]
