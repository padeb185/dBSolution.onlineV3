# dBSolutionV3/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import render
from .views import home_view

# Handler 404 personnalisé
def custom_404(request, exception):
    return render(request, "404.html", status=404)

handler404 = custom_404

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),

    # Utilisateurs
    path("utilisateurs/", include("utilisateurs.urls", namespace="utilisateurs")),

    # Marques
    path("utilisateurs/tenant/", include("voiture.voiture_marque.urls", namespace="voiture_marque")),

    # Exemplaires
    path(
        "voiture/exemplaires/", 
        include(("voiture.voiture_exemplaire.urls", "voiture_exemplaire"), namespace="voiture_exemplaire")
    ),

    # Moteurs
    path('voiture/moteur/', include('voiture.voiture_moteur.urls', namespace='voiture_moteur')),

    # URLs publiques
    path("public/", include("dBSolutionV3.urls_public")),
)
