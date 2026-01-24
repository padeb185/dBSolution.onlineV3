from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import render
from .views import home_view
from voiture.voiture_exemplaire.views import voiture_exemplaire_detail

# Handler 404 personnalisé
def custom_404(request, exception):
    return render(request, "404.html", status=404)

handler404 = custom_404

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("", home_view, name="home"),  # page d'accueil accessible à tous

    # Utilisateurs : login, logout, dashboard, totp
    path("utilisateurs/", include(("utilisateurs.urls", "utilisateurs"), namespace="utilisateurs")),

    # Admin
    path("admin/", admin.site.urls),

    # Marques
    path("utilisateurs/tenant/", include("voiture.voiture_marque.urls", namespace="voiture_marque")),

    # Exemplaires
    path(
        "voiture/exemplaires/",
        include(("voiture.voiture_exemplaire.urls", "voiture_exemplaire"), namespace="voiture_exemplaire")
    ),

    # Moteurs
    path('voiture/moteur/', include('voiture.voiture_moteur.urls', namespace='voiture_moteur')),

    path('voiture/boite', include('voiture.voiture_boite.urls', namespace='voiture_boite')),

    path('voiture/embrayage', include('voiture.voiture_embrayage.urls', namespace='voiture_embrayage')),

    # URLs publiques
    path("public/", include("dBSolutionV3.urls_public")),

    # Détail d'exemplaire
    path('voiture/exemplaires/<uuid:exemplaire_id>/', voiture_exemplaire_detail, name='detail'),

    path(
        "fr/voiture/freins/",
        include((" voiture.voiture_freins.urls", "voiture_freins"), namespace="voiture_freins"),
    ),
)
