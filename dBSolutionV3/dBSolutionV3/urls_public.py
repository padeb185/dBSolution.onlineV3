from django.contrib import admin
from django.urls import path, include
from theme.views import home
from utilisateurs import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Page d'accueil / login
    #path('', views.login_view, name='login'),

    # Setup TOTP (nouvelle route)
    #path('totp/setup/', views.totp_setup_view, name='totp_setup'),

    # Tableau de bord
    #path('dashboard/', views.dashboard_view, name='dashboard'),

    # Réinitialisation du mot de passe : voir dBSolutionV3/urls.py (/connexion/mot-de-passe-oublie/)

    # Namespace pour ton app utilisateurs
    path("auth/", include("utilisateurs.urls", namespace="authentification")),


]
