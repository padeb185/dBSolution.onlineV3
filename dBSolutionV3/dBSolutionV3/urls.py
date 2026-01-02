from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from .views import home_view

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("", home_view, name="home"),  # page d'accueil
    path("admin/", admin.site.urls),
    path("utilisateurs/", include("utilisateurs.urls", namespace="utilisateurs")),  # login, dashboard, logout
    path("", include("dBSolutionV3.urls_public")),   # autres URLs publiques
    path("", include("dBSolutionV3.urls_tenant")),   # tenant
)

