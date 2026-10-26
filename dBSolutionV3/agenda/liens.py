"""
Liens directs depuis l'agenda vers la maintenance à effectuer
(formulaire de la maintenance pour le véhicule concerné).

Pour chaque type de maintenance, on essaie les noms d'URL dans l'ordre ;
le premier qui existe est utilisé. À défaut : page « Choisir le type de
maintenance » du véhicule.
"""
from django.urls import NoReverseMatch, reverse

URLS_MAINTENANCE = {
    "checkup": ["check_up:controle_total_view", "maintenance:controle_total_view", "check_up:checkup_list"],
    "checkup_track": ["checkup_track:track_check_form", "checkup_track:checkup_track_list"],
    "entretien": ["entretien:entretien_check_view", "entretien:entretien_list"],
    "freins": ["freins:freins_check", "systeme_freinage:dashboard_freinage"],
    "pneus": ["pneus:controle_pneus", "pneus:pneus_list"],
    "nettoyage_exterieur": ["nettoyage_exterieur:nettoyage_exterieur_view", "esthetique:dashboard_esthetique"],
    "nettoyage_interieur": ["nettoyage_interieur:nettoyage_interieur_view", "nettoyage_interieur:nettoyage_int_list"],
    "niveaux": ["niveaux:niveau_form_view", "niveaux:niveaux_list"],
    "autres": ["autres_interventions:choisir_autre"],
    "ABS": ["abs:abs_form", "abs:abs_list"],
    "remplacement_boite": ["remplacement_boite:remplacement_boite_form", "remplacement_moteur:remplacement_boite_form"],
    "jeux_pieces": ["jeux_pieces:controle_jeux", "jeux_pieces:jeux_pieces_list"],
    "silent_bloc": ["silent_blocs:silent_check", "silent_blocs:silent_list"],
    "BOITE": ["boite_de_vitesse:boite_check", "boite_de_vitesse:dashboard_boite"],
    "BOITE_AUTO": ["bte_vitesse_auto:bte_auto_check", "bte_auto:bte_auto_check", "bte_auto:dashboard_bte_auto"],
    "ADMISSION": ["admission:admission_check"],
    "TURBO": ["turbo:turbo_check"],
    "MONTAGE_TURBO": ["montage_turbo:montage_turbo_form", "montage_turbo:montage_turbo_list"],
    "CARROSSERIE_INTERNE": ["carrosserie_interne:carrosserie_interne_create", "carrosserie_interne:carrosserie_interne_list"],
    "REMPLACEMENT_MOTEUR": ["remplacement_moteur:remplacement_moteur_form"],
    "COURROIE_DISTRI": ["courroie:courroie_form"],
    "CHAINE_DISTRI": ["chaine_distribution:chaine_form"],
    "BATTERIE": ["batterie:batterie_form", "batterie:batterie_list"],
    "ELECTRONIQUE_MOTEUR": ["electronique_moteur:electronique_form"],
    "LUBRIFICATION": ["lubrification:lubrification_form"],
    "NETTOYAGE_FREINS": ["nettoyage_freins:nettoyage_freins_form"],
    "TAMBOURS": ["tambours:tambours_form"],
    "FREIN_MAIN": ["frein_main:frein_main_form"],
    "FREIN_MAIN_HYDRAULIQUE": ["frein_main_hydraulique:frein_main_hydraulique_form"],
    "RENOVATION_MACHOIRES": ["renovation_machoires:renovation_machoires_form"],
    "POLISH": ["polish:polish_form"],
    "DECONTAMINATION": ["decontamination:decontamination_form"],
    "CIRE": ["cire:cire_form"],
    "CERAMIQUE": ["ceramique:ceramique_form"],
    "RODAGE": ["rodage:rodage_check"],
    "COURROIE_ACCESS": ["courroie_accessoires:courroie_form", "courroie_accessoires:courroie_list"],
    "ECHAPPEMENT": ["dashboard_echappement:echappement_check", "echappement:echappement_check",
                    "echappement:dashboard_echappement"],
    "CLIMATISATION": ["climatisation:clim_form", "climatisation:clim_list"],
    "ALTERNATEUR": ["alternateur:alternateur_check"],
    "REFROIDISSEMENT": ["refroidissement:ref_form", "refroidissement:ref_list"],
    "EMBRAYAGE": ["embrayage:embrayage_form", "embrayage:embrayage_list"],
    "ALLUMAGE": ["allumage:allumage_check"],
    "ESSUYAGE": ["essuyage:essuyage_form", "essuyage:essuyage_list"],
    "INJECTION": ["injection:injection_form"],
    "GEOMETRIE": ["geometrie:geometrie_check", "geometrie:geometrie_list"],
    "ECLAIRAGE": ["eclairage:eclairage_check_view", "eclairage:eclairage_list"],
    "CARDAN": ["cardan:cardan_check", "cardan:cardan_list"],
    "GEOMETRIE_COURSE": ["geometrie_course:geocourse_check", "geometrie_course:geocourse_list"],
    "CREVAISON": ["crevaison:crevaison_check", "crevaison:crevaison_list"],
    "VITRAGE": ["vitrage:vitrage_check", "vitrage:vitrage_list"],
    "ARBRE_TRANSMISSION": ["arbre_transmission:arbre_check", "arbre_transmission:arbre_list"],
    "BOITE_TRANSFERT": ["boite_transfert:transfert_check", "boite_transfert:transfert_list"],
    "CULASSE": ["culasse:culasse_form"],
    "ROULEMENT": ["roulement:roulement_check", "roulement:roulement_list"],
    "remplacement_bte_auto": ["remplacement_bte_auto:remplacement_bte_auto_form"],
    "BAS_MOTEUR": ["bas_moteur:bas_moteur_form"],
    "METROLOGIE_MOTEUR": ["metrologie_moteur:metrologie_form", "metrologie_moteur:metrologie_list"],
    "CASSE_MOTEUR": ["casse_moteur:casse_form", "casse_moteur:casse_list"],
    "CASSE_BOITE": ["casse_boite:casse_form", "casse_boite:casse_list"],
    "ESP": ["esp:esp_form", "esp:esp_list"],
    "AIDE_STATIONNEMENT": ["aide_stationnement:aide_stationnement_form", "aide_stationnement:aide_stationnement_list"],
    "VENTILATION": ["ventilation:ventilation_form", "ventilation:ventilation_list"],
    "SECURITE": ["securite:securite_form", "securite:securite_list"],
    "PC_ARCEAU": ["pc_arceau:pc_arceau_form", "pc_arceau:pc_arceau_list"],
    "PC_EXTINCTEUR": ["pc_extincteur:pc_extincteur_form", "pc_extincteur:pc_extincteur_list"],
    "PC_SIEGES": ["pc_sieges:pc_sieges_form", "pc_sieges:pc_sieges_list"],
    "PC_CABLAGE": ["pc_cablage:pc_cablage_form", "pc_cablage:pc_cablage_list"],
    "PC_BOITIER": ["pc_boitier:pc_boitier_form", "pc_boitier:pc_boitier_list"],
    "PC_MOTEUR": ["pc_moteur:pc_moteur_form", "pc_moteur:pc_moteur_list"],
    "PC_ECHAPPEMENT": ["pc_echappement:pc_echappement_form", "pc_echappement:pc_echappement_list"],
    "PC_DEMONTAGE": ["pc_demontage:pc_demontage_form", "pc_demontage:pc_demontage_list"],
    "PC_AIR_JACK": ["pc_air_jack:pc_air_jack_form", "pc_air_jack:pc_air_jack_list"],
    "FUSIBLES": ["fusibles:fusibles_form", "fusibles:fusibles_list"],
    "DEMARREUR": ["demarreur:demarreur_form", "demarreur:demarreur_list"],
    "SUSPENSION_ORIGINE": ["suspension_origine:suspension_origine_form", "suspension:dashboard_suspension"],
    "SUSPENSION_SPORT": ["suspension_sport:suspension_sport_form", "suspension:dashboard_suspension"],
    "BOUGIES_ALLUMAGE": ["bougies_allumage:bougies_allumage_form"],
    "BOUGIES_PRECHAUFFAGE": ["bougies_prechauffage:bougies_prechauffage_form"],
    "ECH_COLLECTEUR": ["collecteur:collecteur_form"],
    "ECH_CATALYSEUR": ["catalyseur:catalyseur_form"],
    "ECH_SILENCIEUX": ["silencieux:silencieux_form"],
    "ECH_FILTRE_PARTICULES": ["filtre_particules:filtre_particules_form"],
    "ECH_POT_DENOX": ["pot_denox:pot_denox_form"],
    "ECH_SONDE_LAMBDA_AMONT": ["sonde_lambda_amont:sonde_lambda_amont_form"],
    "ECH_SONDE_LAMBDA_AVAL": ["sonde_lambda_aval:sonde_lambda_aval_form"],
    "ECH_SONDE_FAP_AMONT": ["sonde_fap_amont:sonde_fap_amont_form"],
    "ECH_SONDE_FAP_AVAL": ["sonde_fap_aval:sonde_fap_aval_form"],
    "ECH_CAPTEUR_FAP": ["capteur_fap:capteur_fap_form"],
    "ECH_TUYAUX_FAP": ["tuyaux_fap:tuyaux_fap_form"],
    "ECH_REGENERATION_FAP": ["regeneration_fap:regeneration_fap_form"],
    "ECH_INJECTEUR_ADBLUE": ["injecteur_adblue:injecteur_adblue_form"],
    "ECH_VALVES_ECHAPPEMENT": ["valves_echappement:valves_echappement_form"],
    "ECH_SILENT_BLOCS_ECHAPPEMENT": ["silent_blocs_echappement:silent_blocs_echappement_form"],
}


def _reverse(nom, exemplaire_id):
    for kwargs, args in (({"exemplaire_id": exemplaire_id}, None), (None, [exemplaire_id])):
        try:
            return reverse(nom, kwargs=kwargs, args=args)
        except NoReverseMatch:
            continue
    return None


def url_maintenance(type_maintenance, exemplaire_id):
    """URL du formulaire de la maintenance pour ce véhicule (ou page de choix en secours)."""
    if not exemplaire_id:
        return ""
    for nom in URLS_MAINTENANCE.get(type_maintenance, []):
        url = _reverse(nom, exemplaire_id)
        if url:
            return url
    return _reverse("maintenance:choisir_type", exemplaire_id) or ""


def url_vehicule(exemplaire_id):
    if not exemplaire_id:
        return ""
    return _reverse("voiture_exemplaire:voiture_exemplaire_detail", exemplaire_id) or ""
