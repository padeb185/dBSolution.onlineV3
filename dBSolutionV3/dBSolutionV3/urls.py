from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import render
from .views import home_view

# --- Handler 404 personnalisé ---
def custom_404(request, exception):
    return render(request, "404.html", status=404)

handler404 = custom_404

# --- URLs hors traduction ---
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # changement de langue
]

# --- URLs traduisibles (i18n) ---
urlpatterns += i18n_patterns(
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),

    # Utilisateurs
    path("utilisateurs/", include("utilisateurs.urls", namespace="utilisateurs")),

    path("utilisateurs/tenant/", include("voiture.voiture_marque.urls")),


    path("public/", include("dBSolutionV3.urls_public")),


    path("voiture/", include(("tenant.urls", "voiture_marque"), namespace="voiture_marque")),

    path('voiture/moteur/', include('voiture.voiture_moteur.urls', namespace='voiture_moteur')),
)
