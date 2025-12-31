from django.contrib import admin
from django.urls import path, include
from theme.views import home
from utilisateurs import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Page d'accueil / login
    path('', views.login_view, name='login'),

    # Vérification TOTP
    path('totp-verify/', views.totp_verify_view, name='totp_verify'),

    # Setup TOTP (nouvelle route)
    path('totp/setup/', views.totp_setup_view, name='totp_setup'),

    # Tableau de bord
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Reset password
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
