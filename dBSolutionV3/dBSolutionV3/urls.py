from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import render
from .views import home_view


# --- Handler 404 personnalisé ---
def custom_404(request, exception):
    return render(request, "404.html", status=404)


handler404 = custom_404

# --- URLs hors traduction (ex : i18n) ---
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # changement de langue
]

# --- URLs traduisibles (i18n) ---
urlpatterns += i18n_patterns(
    path("", home_view, name="home"),  # page d'accueil
    path("admin/", admin.site.urls),

    # Utilisateurs
    path("utilisateurs/", include("utilisateurs.urls", namespace="utilisateurs")),

    # URLs publiques
    path("public/", include("dBSolutionV3.urls_public")),

    # Tenant
    path('voiture/', include('tenant.urls', namespace='tenant')),
    # ici tout ce qui est marques/modeles/exemplaires/moteurs

    # Si nécessaire, tu peux inclure voiture_moteur **sans doublon**
    # path("voiture/moteurs/", include("voiture.voiture_moteur.urls", namespace="voiture_moteur")),
)
