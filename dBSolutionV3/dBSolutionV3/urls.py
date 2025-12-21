from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from dBSolutionV3 import views
from rest_framework.authtoken import views as drf_views
from django.shortcuts import redirect

# URLs globales (non traduisibles)
urlpatterns = [
    # Endpoint obligatoire pour changer de langue
    path("i18n/", include("django.conf.urls.i18n")),

    # Redirection racine vers /fr/
    path("", lambda request: redirect("/fr/")),

    # Reload Django Browser Reload
    path("__reload__/", include("django_browser_reload.urls")),
]

# URLs traduisibles (i18n)
urlpatterns += i18n_patterns(
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # Admin
    path("admin/", admin.site.urls),

    # Auth (login/logout/password)
    path("accounts/", include("django.contrib.auth.urls")),

    # DRF Token Auth
    path("api-token-auth/", drf_views.obtain_auth_token, name="api-token-auth"),
)
