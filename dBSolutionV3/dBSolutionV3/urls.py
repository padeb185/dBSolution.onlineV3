from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import render
from .views import home_view
from django.conf import settings
from django.conf.urls.static import static
from voiture.voiture_exemplaire.views import voiture_exemplaire_detail
from utilisateurs.views import connexion_globale_view
from utilisateurs.views_connexion import verifier_identifiants
from utilisateurs import views_mot_de_passe as mdp


# Handler 404 personnalisé
def custom_404(request, exception):
    return render(request, "404.html", status=404)

handler404 = custom_404


# Handler 500 personnalisé (actif uniquement quand DEBUG = False)
def custom_500(request):
    from django.http import HttpResponseServerError
    try:
        return render(request, "500.html", status=500)
    except Exception:
        # Si la mise en page elle-même plante (base de données, contexte…),
        # on renvoie une page minimale qui ne dépend de rien.
        return HttpResponseServerError(
            "<!doctype html><html lang='fr'><head><meta charset='utf-8'>"
            "<title>500 – Erreur interne</title></head>"
            "<body style='font-family:Arial,sans-serif;text-align:center;padding:80px 20px;color:#374151'>"
            "<h1 style='font-size:64px;color:#dc2626;margin:0'>500</h1>"
            "<h2>Une erreur est survenue</h2>"
            "<p>Le serveur a rencontré un problème inattendu. Veuillez réessayer dans quelques instants.</p>"
            "<p><a href='javascript:history.back()'>← Retour à la page précédente</a> · <a href='/'>Accueil</a></p>"
            "</body></html>"
        )

handler500 = custom_500

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("", home_view, name="home"),
    path("connexion/", connexion_globale_view, name="connexion_globale"),
    path("connexion/verifier/", verifier_identifiants, name="connexion_verifier"),

    # Mot de passe oublié → lien par e-mail (adresse de récupération) → nouveau mot de passe
    path("connexion/mot-de-passe-oublie/", mdp.MotDePasseOublieView.as_view(), name="password_reset"),
    path("connexion/mot-de-passe-oublie/envoye/", mdp.MotDePasseOublieEnvoyeView.as_view(), name="password_reset_done"),
    path("connexion/reinitialiser/<uidb64>/<token>/", mdp.NouveauMotDePasseView.as_view(), name="password_reset_confirm"),
    path("connexion/reinitialiser/termine/", mdp.NouveauMotDePasseTermineView.as_view(), name="password_reset_complete"),

    # Changement du mot de passe par l'utilisateur connecté
    path("compte/mot-de-passe/", mdp.ChangerMotDePasseView.as_view(), name="password_change"),
    path("compte/mot-de-passe/modifie/", mdp.ChangerMotDePasseTermineView.as_view(), name="password_change_done"),

    path("admin/", admin.site.urls),

    path(
        "utilisateurs/",
        include(
            ("utilisateurs.urls", "utilisateurs"),
            namespace="utilisateurs",
        ),
    ),

    path(
        "voiture/marques/",
        include(
            ("voiture.voiture_marque.urls", "voiture_marque"),
            namespace="voiture_marque",
        ),
    ),

    path(
        "voiture/modeles/",
        include(
            ("voiture.voiture_modele.urls", "voiture_modele"),
            namespace="voiture_modele",
        ),
    ),


    # Exemplaires
    path(
        "voiture/exemplaires/",
        include(("voiture.voiture_exemplaire.urls", "voiture_exemplaire"), namespace="voiture_exemplaire")
    ),

    # Garages officiels et maintenances externes
    path("garage_officiel/", include(("garage_officiel.urls", "garage_officiel"), namespace="garage_officiel")),
    path("maintenance/externe/", include(("maintenance.maintenance_externe.urls", "maintenance_externe"), namespace="maintenance_externe")),

    # Diagnostics (codes défaut)
    path("diagnostic/", include(("voiture.voiture_diagnostic.urls", "voiture_diagnostic"), namespace="voiture_diagnostic")),

    # Locations (circuit / route)
    path("location/", include(("voiture.voiture_location.urls", "voiture_location"), namespace="voiture_location")),

    # Moteurs
    path('voiture/moteur/', include('voiture.voiture_moteur.urls', namespace='voiture_moteur')),

    path('voiture/boite/', include('voiture.voiture_boite.urls', namespace='voiture_boite')),

    path('voiture/embrayage/', include('voiture.voiture_embrayage.urls', namespace='voiture_embrayage')),

    # URLs publiques
    path("public/", include("dBSolutionV3.urls_public")),

    # Détail d'exemplaire
    path('voiture/exemplaires/<uuid:exemplaire_id>/', voiture_exemplaire_detail, name='detail'),

    path(
        "voiture/freins/",
        include(("voiture.voiture_freins_av.urls", "voiture_freins_av"), namespace="voiture_freins_av"),
    ),
    path(
        "voiture/freins_ar/",
        include(("voiture.voiture_freins_ar.urls", "voiture_freins_ar"), namespace="voiture_freins_ar"),
    ),
    path(
        "voiture/pneus/",
        include(("voiture.voiture_pneus.urls", "voiture_pneus"), namespace="voiture_pneus"),
    ),

    path('maintenance/', include('maintenance.urls', namespace='maintenance')),

    # Check-up (app spécifique)
    path('maintenance/checkup/', include('maintenance.check_up.urls', namespace='check_up')),

    path("fournisseurs/", include("fournisseur.urls")),

    path("client_particulier/", include("client_particulier.urls")),

    path("client_atelier/", include("client_atelier.urls")),

    path("client_pilotage/", include("client_pilotage.urls")),

    path("carrosserie/", include("carrosserie.urls")),

    path("societe_cliente/", include("societe_cliente.urls")),

    path("adresse/", include("adresse.urls")),

    path("fuel/", include("fuel.urls", namespace="fuel")),

    path("adblue/", include("adblue.urls", namespace="adblue")),

    path("assurance/", include("assurance.urls", namespace="assurance")),

    path("assurance_police/", include("assurance_police.urls", namespace="assurance_police")),

    path("maintenance/entretien/", include("maintenance.entretien.urls", namespace="entretien")),

    path("recharge/", include("recharge.urls")),

    path("piece/", include("piece.urls", namespace="piece")),

    path("outillage/", include("outillage.urls", namespace="outillage")),

    path('maintenance/jeux_pieces/', include('maintenance.jeux_pieces.urls', namespace='jeux_pieces')),

    path('maintenance/nettoyage-exterieur/', include(('maintenance.esthetique.nettoyage_exterieur.urls', 'nettoyage_exterieur'),namespace='nettoyage_exterieur')),
    path('maintenance/esthetique/', include(('maintenance.esthetique.urls', 'esthetique'), namespace='esthetique')),
    path('maintenance/freinage/', include(('maintenance.systeme_freinage.urls', 'systeme_freinage'), namespace='systeme_freinage')),
    path('maintenance/freinage/nettoyage-freins/', include(('maintenance.systeme_freinage.nettoyage_freins.urls', 'nettoyage_freins'), namespace='nettoyage_freins')),
    path('maintenance/freinage/tambours/', include(('maintenance.systeme_freinage.tambours.urls', 'tambours'), namespace='tambours')),
    path('maintenance/freinage/frein-main/', include(('maintenance.systeme_freinage.frein_main.urls', 'frein_main'), namespace='frein_main')),
    path('maintenance/freinage/frein-main-hydraulique/', include(('maintenance.systeme_freinage.frein_main_hydraulique.urls', 'frein_main_hydraulique'), namespace='frein_main_hydraulique')),
    path('maintenance/freinage/renovation-machoires/', include(('maintenance.systeme_freinage.renovation_machoires.urls', 'renovation_machoires'), namespace='renovation_machoires')),
    path('maintenance/esthetique/polish/', include(('maintenance.esthetique.polish.urls', 'polish'), namespace='polish')),
    path('maintenance/esthetique/decontamination/', include(('maintenance.esthetique.decontamination.urls', 'decontamination'), namespace='decontamination')),
    path('maintenance/esthetique/cire/', include(('maintenance.esthetique.cire.urls', 'cire'), namespace='cire')),
    path('maintenance/esthetique/ceramique/', include(('maintenance.esthetique.ceramique.urls', 'ceramique'), namespace='ceramique')),

    path("__reload__/", include("django_browser_reload.urls")),

    path('maintenance/nettoyage-interieur/',include(('maintenance.nettoyage_interieur.urls', 'nettoyage_interieur'), namespace='nettoyage_interieur')),

    path('maintenance/freins/',include(('maintenance.freins.urls', 'freins'), namespace='freins')),

    path('maintenance/niveaux/', include(('maintenance.niveaux.urls', 'niveaux'), namespace='niveaux')),

    path('maintenance/silent/', include(('maintenance.silent_blocs.urls', 'silent_blocs'), namespace='silent_blocs')),

    path('maintenance/pneus/crevaison/', include(('maintenance.pneus.crevaison.urls', 'crevaison'), namespace='crevaison')),
    path('maintenance/pneus/', include(('maintenance.pneus.urls', 'pneus'), namespace='pneus')),

    path('maintenance/autre/', include(('maintenance.autres_interventions.urls', 'autres_interventions'), namespace='autres_interventions')),

    path('maintenance/autre/boite/',include(('maintenance.autres_interventions.boite_de_vitesse.urls', 'boite_de_vitesse'), namespace='boite_de_vitesse')),

    path('maintenance/autre/bte_auto/',include(('maintenance.autres_interventions.bte_vitesse_auto.urls', 'bte_vitesse_auto'), namespace='bte_vitesse_auto')),
    path('maintenance/autre/cardan/', include(('maintenance.autres_interventions.cardan.urls', 'cardan'), namespace='cardan')),
    path('maintenance/autre/geometrie-course/', include(('maintenance.autres_interventions.geometrie_course.urls', 'geometrie_course'), namespace='geometrie_course')),
    path('maintenance/autre/vitrage/', include(('maintenance.autres_interventions.vitres.urls', 'vitrage'), namespace='vitrage')),
    path('maintenance/autre/boite-transfert/', include(('maintenance.autres_interventions.boite_transfert.urls', 'boite_transfert'), namespace='boite_transfert')),
    path('maintenance/autre/arbre-transmission/', include(('maintenance.autres_interventions.arbre_transmission.urls', 'arbre_transmission'), namespace='arbre_transmission')),
    path('maintenance/autre/roulement/', include(('maintenance.autres_interventions.roulement.urls', 'roulement'), namespace='roulement')),
    path('agenda/', include(('agenda.urls', 'agenda'), namespace='agenda')),

    path('facture/', include(('facture.urls', 'facture'), namespace='facture')),
    path('compta/', include(('compta.urls', 'compta'), namespace='compta')),

    path('maintenance/carrosserie/', include(('maintenance.carrosserie_interne.urls', 'carrosserie_interne'), namespace='carrosserie_interne')),

    path('moteur/', include(('maintenance.autres_interventions.moteur.urls', 'moteur'), namespace='moteur')),

     path('admission/', include(('maintenance.autres_interventions.moteur.admission.urls', 'admission'), namespace='admission')),

    path('alternateur/',include(('maintenance.autres_interventions.moteur.alternateur.urls', 'alternateur'), namespace='alternateur')),

    path('maintenance/autre/geometrie/',include(('maintenance.autres_interventions.geometrie.urls', 'geometrie'),namespace='geometrie')),

    path('achat_mds/',include(('achat_mds.urls', 'achat_mds'),namespace='achat_mds')),

    path('maintenance/checkup_track/', include('maintenance.checkup_track.urls', namespace='checkup_track')),

    path('courroie/',include(('maintenance.autres_interventions.moteur.courroie.urls', 'courroie'), namespace='courroie')),
    path('chaine_distribution/', include(('maintenance.autres_interventions.moteur.chaine_distribution.urls', 'chaine_distribution'), namespace='chaine_distribution')),
    path('culasse/', include(('maintenance.autres_interventions.moteur.culasse.urls', 'culasse'), namespace='culasse')),
    path("bougies/", include(("maintenance.autres_interventions.moteur.bougies.urls", "bougies"), namespace="bougies")),
    path("bougies/allumage/", include(("maintenance.autres_interventions.moteur.bougies.bougies_allumage.urls", "bougies_allumage"), namespace="bougies_allumage")),
    path("bougies/prechauffage/", include(("maintenance.autres_interventions.moteur.bougies.bougies_prechauffage.urls", "bougies_prechauffage"), namespace="bougies_prechauffage")),
    path("suspension/", include(("maintenance.autres_interventions.suspension.urls", "suspension"), namespace="suspension")),
    path("suspension/origine/", include(("maintenance.autres_interventions.suspension.suspension_origine.urls", "suspension_origine"), namespace="suspension_origine")),
    path("suspension/sport/", include(("maintenance.autres_interventions.suspension.suspension_sport.urls", "suspension_sport"), namespace="suspension_sport")),
    path("demarreur/", include(("maintenance.autres_interventions.demarreur.urls", "demarreur"), namespace="demarreur")),
    path("esp/", include(("maintenance.autres_interventions.esp.urls", "esp"), namespace="esp")),
    path("aide-stationnement/", include(("maintenance.autres_interventions.aide_stationnement.urls", "aide_stationnement"), namespace="aide_stationnement")),
    path("ventilation/", include(("maintenance.autres_interventions.ventilation.urls", "ventilation"), namespace="ventilation")),
    path("securite/", include(("maintenance.autres_interventions.securite.urls", "securite"), namespace="securite")),
    path("preparation-course/", include(("maintenance.autres_interventions.preparation_course.urls", "preparation_course"), namespace="preparation_course")),
    path("preparation-course/arceau/", include(("maintenance.autres_interventions.preparation_course.arceau.urls", "pc_arceau"), namespace="pc_arceau")),
    path("preparation-course/extincteur/", include(("maintenance.autres_interventions.preparation_course.extincteur.urls", "pc_extincteur"), namespace="pc_extincteur")),
    path("preparation-course/sieges/", include(("maintenance.autres_interventions.preparation_course.sieges_baquets.urls", "pc_sieges"), namespace="pc_sieges")),
    path("preparation-course/cablage/", include(("maintenance.autres_interventions.preparation_course.cablage.urls", "pc_cablage"), namespace="pc_cablage")),
    path("preparation-course/boitier/", include(("maintenance.autres_interventions.preparation_course.boitier_competition.urls", "pc_boitier"), namespace="pc_boitier")),
    path("preparation-course/moteur/", include(("maintenance.autres_interventions.preparation_course.preparation_moteur.urls", "pc_moteur"), namespace="pc_moteur")),
    path("preparation-course/echappement/", include(("maintenance.autres_interventions.preparation_course.echappement_course.urls", "pc_echappement"), namespace="pc_echappement")),
    path("preparation-course/demontage/", include(("maintenance.autres_interventions.preparation_course.demontage.urls", "pc_demontage"), namespace="pc_demontage")),
    path("preparation-course/air-jack/", include(("maintenance.autres_interventions.preparation_course.air_jack.urls", "pc_air_jack"), namespace="pc_air_jack")),
    path("fusibles/", include(("maintenance.autres_interventions.fusibles.urls", "fusibles"), namespace="fusibles")),
    path('bas_moteur/', include(('maintenance.autres_interventions.moteur.bas_moteur.urls', 'bas_moteur'), namespace='bas_moteur')),
    path('metrologie_moteur/', include(('maintenance.autres_interventions.moteur.metrologie_moteur.urls', 'metrologie_moteur'), namespace='metrologie_moteur')),
    path('casse_moteur/', include(('maintenance.autres_interventions.moteur.casse_moteur.urls', 'casse_moteur'), namespace='casse_moteur')),
    path('electronique_moteur/', include(('maintenance.autres_interventions.moteur.electronique_moteur.urls', 'electronique_moteur'), namespace='electronique_moteur')),
    path('lubrification/', include(('maintenance.autres_interventions.moteur.lubrification.urls', 'lubrification'), namespace='lubrification')),

    path("abs/", include("maintenance.autres_interventions.abs.urls", namespace="abs")),

    path('stats_fournisseurs/', include(('stats_fournisseurs.urls', 'stats_fournisseurs'), namespace='stats_fournisseurs')),

    path('maindoeuvre/',include(('maindoeuvre.urls', 'maindoeuvre'), namespace='maindoeuvre')),

    path('proprietaire/', include(('proprietaire.urls', 'proprietaire'), namespace='proprietaire')),

    path("remplacement_moteur/",include(("maintenance.autres_interventions.moteur.remplacement_moteur.urls", "remplacement_moteur"), namespace="remplacement_moteur")),

    path("turbo/",include(("maintenance.autres_interventions.moteur.turbo.urls", "turbo"),namespace="turbo")),
    path("montage-turbo/", include(("maintenance.autres_interventions.moteur.montage_turbo.urls", "montage_turbo"), namespace="montage_turbo")),

    path("remplacement_boite/",include(("maintenance.autres_interventions.boite_de_vitesse.remplacement_boite.urls", "remplacement_boite"),namespace="remplacement_boite")),
    path("casse_boite/", include(("maintenance.autres_interventions.boite_de_vitesse.casse_boite.urls", "casse_boite"), namespace="casse_boite")),
    path("remplacement_bte_auto/",include(("maintenance.autres_interventions.bte_vitesse_auto.remplacement_bte_auto.urls", "remplacement_bte_auto"),namespace="remplacement_bte_auto")),

    path("rodage/",include(("maintenance.autres_interventions.moteur.rodage.urls", "rodage"),namespace="rodage")),

    path("courroie_accessoires/", include(("maintenance.autres_interventions.courroie_accessoires.urls", "courroie_accessoires"), namespace="courroie_accessoires")),

    path("echappement/collecteur/", include(("maintenance.autres_interventions.echappement.collecteur.urls", "collecteur"), namespace="collecteur")),
    path("echappement/catalyseur/", include(("maintenance.autres_interventions.echappement.catalyseur.urls", "catalyseur"), namespace="catalyseur")),
    path("echappement/silencieux/", include(("maintenance.autres_interventions.echappement.silencieux.urls", "silencieux"), namespace="silencieux")),
    path("echappement/filtre_particules/", include(("maintenance.autres_interventions.echappement.filtre_particules.urls", "filtre_particules"), namespace="filtre_particules")),
    path("echappement/pot_denox/", include(("maintenance.autres_interventions.echappement.pot_denox.urls", "pot_denox"), namespace="pot_denox")),
    path("echappement/sonde_lambda_amont/", include(("maintenance.autres_interventions.echappement.sonde_lambda_amont.urls", "sonde_lambda_amont"), namespace="sonde_lambda_amont")),
    path("echappement/sonde_lambda_aval/", include(("maintenance.autres_interventions.echappement.sonde_lambda_aval.urls", "sonde_lambda_aval"), namespace="sonde_lambda_aval")),
    path("echappement/sonde_fap_amont/", include(("maintenance.autres_interventions.echappement.sonde_fap_amont.urls", "sonde_fap_amont"), namespace="sonde_fap_amont")),
    path("echappement/sonde_fap_aval/", include(("maintenance.autres_interventions.echappement.sonde_fap_aval.urls", "sonde_fap_aval"), namespace="sonde_fap_aval")),
    path("echappement/capteur_fap/", include(("maintenance.autres_interventions.echappement.capteur_fap.urls", "capteur_fap"), namespace="capteur_fap")),
    path("echappement/tuyaux_fap/", include(("maintenance.autres_interventions.echappement.tuyaux_fap.urls", "tuyaux_fap"), namespace="tuyaux_fap")),
    path("echappement/regeneration_fap/", include(("maintenance.autres_interventions.echappement.regeneration_fap.urls", "regeneration_fap"), namespace="regeneration_fap")),
    path("echappement/injecteur_adblue/", include(("maintenance.autres_interventions.echappement.injecteur_adblue.urls", "injecteur_adblue"), namespace="injecteur_adblue")),
    path("echappement/valves_echappement/", include(("maintenance.autres_interventions.echappement.valves_echappement.urls", "valves_echappement"), namespace="valves_echappement")),
    path("echappement/silent_blocs_echappement/", include(("maintenance.autres_interventions.echappement.silent_blocs_echappement.urls", "silent_blocs_echappement"), namespace="silent_blocs_echappement")),
    path("echappement/",include(("maintenance.autres_interventions.echappement.urls", "dashboard_echappement"),namespace="dashboard_echappement")),
    path("batterie/", include(("maintenance.autres_interventions.batterie.urls", "batterie"), namespace="batterie")),

    path("climatisation/",include(("maintenance.autres_interventions.climatisation.urls", "climatisation"),namespace="climatisation")),

    path("refroidissement/",include(("maintenance.autres_interventions.refroidissement.urls", "refroidissement"), namespace="refroidissement")),

    path('embrayage/', include(('maintenance.autres_interventions.embrayage.urls', 'embrayage'), namespace='embrayage')),

    path("allumage/", include(("maintenance.autres_interventions.moteur.allumage.urls", "allumage"), namespace="allumage")),

    path('maintenance/essuyage/', include(('maintenance.essuyage.urls', 'essuyage'), namespace='essuyage')),

    path("injection/",include(("maintenance.autres_interventions.moteur.injection.urls", "injection"), namespace="injection")),

    path("maintenance/eclairage/", include("maintenance.eclairage.urls", namespace="eclairage")),



)





urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)