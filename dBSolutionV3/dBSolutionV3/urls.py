from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import render
from .views import home_view
from voiture.voiture_exemplaire.views import voiture_exemplaire_detail
from django.conf import settings
from django.conf.urls.static import static





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
        include(("voiture.voiture_freins_av.urls", "voiture_freins_av"), namespace="voiture_freins_av"),
    ),
    path(
        "fr/voiture/freins_ar/",
        include(("voiture.voiture_freins_ar.urls", "voiture_freins_ar"), namespace="voiture_freins_ar"),
    ),
    path(
        "fr/voiture/pneus/",
        include(("voiture.voiture_pneus.urls", "voiture_pneus"), namespace="voiture_pneus"),
    ),

    path('maintenance/', include('maintenance.urls', namespace='maintenance')),

    # Check-up (app spécifique)
    path('maintenance/checkup/', include('maintenance.check_up.urls', namespace='check_up')),

    path("fournisseurs/", include("fournisseur.urls")),

    path("client_particulier/", include("client_particulier.urls")),

    path("carrosserie/", include("carrosserie.urls")),



    path("societe_cliente/", include("societe_cliente.urls")),

    path("adresse/", include("adresse.urls")),

    path("fuel/", include("fuel.urls", namespace="fuel")),

    path("assurance/", include("assurance.urls", namespace="assurance")),

    path("assurance_police/", include("assurance_police.urls", namespace="assurance_police")),

    path("maintenance/entretien/", include("maintenance.entretien.urls", namespace="entretien")),

    path("recharge/", include("recharge.urls")),

    path("voiture_modele/", include("voiture.voiture_modele.urls")),

    path("piece/", include("piece.urls", namespace="piece")),

    path("outillage/", include("outillage.urls", namespace="outillage")),

    path('maintenance/jeux_pieces/', include('maintenance.jeux_pieces.urls', namespace='jeux_pieces')),

    path('maintenance/nettoyage-exterieur/', include(('maintenance.nettoyage_exterieur.urls', 'nettoyage_exterieur'),namespace='nettoyage_exterieur')),

    path("__reload__/", include("django_browser_reload.urls")),

    path('maintenance/nettoyage-interieur/',include(('maintenance.nettoyage_interieur.urls', 'nettoyage_interieur'), namespace='nettoyage_interieur')),

    path('maintenance/freins/',include(('maintenance.freins.urls', 'freins'), namespace='freins')),

    path('maintenance/niveaux/', include(('maintenance.niveaux.urls', 'niveaux'), namespace='niveaux')),

    path('maintenance/silent/', include(('maintenance.silent_blocs.urls', 'silent_blocs'), namespace='silent_blocs')),

    path('maintenance/pneus/', include(('maintenance.pneus.urls', 'pneus'), namespace='pneus')),

    path('maintenance/autre/', include(('maintenance.autres_interventions.urls', 'autres_interventions'), namespace='autres_interventions')),

    path('maintenance/autre/boite/',include(('maintenance.autres_interventions.boite_de_vitesse.urls', 'boite_de_vitesse'), namespace='boite_de_vitesse')),

    path('maintenance/autre/bte_auto/',include(('maintenance.autres_interventions.bte_vitesse_auto.urls', 'bte_vitesse_auto'), namespace='bte_vitesse_auto')),

    path('maintenance/carrosserie/', include(('maintenance.carrosserie_interne.urls', 'carrosserie_interne'), namespace='carrosserie_interne')),

    path('moteur/', include(('maintenance.autres_interventions.moteur.urls', 'moteur'), namespace='moteur')),

     path('admission/', include(('maintenance.autres_interventions.moteur.admission.urls', 'admission'), namespace='admission')),

    path('alternateur/',include(('maintenance.autres_interventions.moteur.alternateur.urls', 'alternateur'), namespace='alternateur')),

    path('maintenance/autre/geometrie/',include(('maintenance.autres_interventions.geometrie.urls', 'geometrie'),namespace='geometrie')),

    path('achat_mds/',include(('achat_mds.urls', 'achat_mds'),namespace='achat_mds')),

    path('maintenance/checkup_track/', include('maintenance.checkup_track.urls', namespace='checkup_track')),

)





urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)