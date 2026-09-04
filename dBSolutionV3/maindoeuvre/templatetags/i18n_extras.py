# maindoeuvre/templatetags/i18n_extras.py

from django import template
from django.utils.translation import gettext

register = template.Library()


DESCRIPTIFS_TRADUISIBLES = [

    # ==========================================================
    # CHECKUPS
    # ==========================================================
    "Checkup boite de vitesse automatique",
    "Checkup boite de vitesse",
    "Checkup boite",
    "Checkup piste",
    "Checkup complet",

    # Anciennes valeurs déjà traduites enregistrées en DB
    "Automatic transmission checkup",
    "Track checkup",

    # ==========================================================
    # ABS
    # ==========================================================
    "Contrôle du système ABS",
    "Controle du système ABS",
    "Contrôle ABS",
    "Controle ABS",
    "ABS",

    # Ancienne valeur anglaise
    "ABS system check",

    # ==========================================================
    # ENTRETIEN
    # ==========================================================
    "Entretien",

    # Ancienne valeur anglaise
    "Service",

    # ==========================================================
    # ADMISSION
    # ==========================================================
    "Contrôle de l'admission",
    "Controle de l'admission",
    "Admission",

    # Ancienne valeur anglaise
    "Intake",

    # ==========================================================
    # ALLUMAGE
    # ==========================================================
    "Contrôle de l'allumage",
    "Controle de l'allumage",
    "Allumage",

    # Ancienne valeur anglaise
    "Ignition",

    # ==========================================================
    # ALTERNATEUR
    # ==========================================================
    "Contrôle de l'alternateur",
    "Controle de l'alternateur",
    "Alternateur",

    # Ancienne valeur anglaise
    "Alternator",

    # ==========================================================
    # INJECTION
    # ==========================================================
    "Contrôle de l'injection",
    "Controle de l'injection",
    "Controle Injection",
    "Système d'injection",
    "Injection",

    # ==========================================================
    # TURBO
    # ==========================================================
    "Contrôle du turbo",
    "Controle du turbo",
    "Turbo",

    # Ancienne valeur anglaise
    "Turbocharger",

    # ==========================================================
    # REFROIDISSEMENT
    # ==========================================================
    "Contrôle du système de refroidissement",
    "Controle du système de refroidissement",
    "Contrôle du refroidissement",
    "Controle du refroidissement",
    "Refroidissement",

    # ==========================================================
    # FREINS
    # ==========================================================
    "Contrôle des freins",
    "Controle des freins",
    "Freins",

    # Ancienne valeur anglaise
    "Brake inspections",

    # ==========================================================
    # PNEUS
    # ==========================================================
    "Contrôle des pneus",
    "Controle des pneus",
    "Pneus",

    # ==========================================================
    # SILENT BLOCS
    # ==========================================================
    "Contrôle des silent blocs",
    "Controle des silent blocs",
    "Silent blocs",

    # ==========================================================
    # NIVEAUX
    # ==========================================================
    "Contrôle des niveaux",
    "Controle des niveaux",
    "Niveaux",

    # ==========================================================
    # JEUX
    # ==========================================================
    "Contrôle des jeux",
    "Controle des jeux",
    "Jeux",

    # ==========================================================
    # ESSUYAGE
    # ==========================================================
    "Contrôle du système d'essuyage",
    "Controle du système d'essuyage",
    "Essuyage",

    # ==========================================================
    # NETTOYAGE
    # ==========================================================
    "Nettoyage extérieur",
    "Nettoyage Extérieur",
    "Nettoyage intérieur",
    "Nettoyage Intérieur",

    # Anciennes valeurs anglaises
    "Exterior cleaning",
    "Interior cleaning",

    # ==========================================================
    # CARROSSERIE
    # ==========================================================
    "Carrosserie interne",
    "Carrosserie",
    "BodyShop interne",

    # ==========================================================
    # GÉOMÉTRIE
    # ==========================================================
    "Contrôle de la géométrie",
    "Controle de la géométrie",
    "Géométrie",

    # ==========================================================
    # BOITE DE VITESSE
    # ==========================================================
    "Contrôle de la boite de vitesse",
    "Controle de la boite de vitesse",
    "Checkup boite de vitesse",
    "Checkup boite",

    # ==========================================================
    # BOITE AUTOMATIQUE
    # ==========================================================
    "Checkup boite de vitesse automatique",
    "Contrôle de la boite automatique",
    "Controle de la boite automatique",
    "Contrôle boite auto",
    "Controle boite auto",

    # ==========================================================
    # CLIMATISATION
    # ==========================================================
    "Contrôle de la climatisation",
    "Controle de la climatisation",
    "Climatisation",

    # ==========================================================
    # ÉCHAPPEMENT
    # ==========================================================
    "Contrôle de l'échappement",
    "Controle de l'échappement",
    "Echappement",
    "Échappement",

    # ==========================================================
    # COURROIE ACCESSOIRES
    # ==========================================================
    "Contrôle de la courroie d'accessoires",
    "Controle de la courroie d'accessoires",
    "Courroie d'accessoires",

    # ==========================================================
    # COURROIE DISTRIBUTION
    # ==========================================================
    "Courroie de distribution",
    "Contrôle de la courroie de distribution",
    "Controle de la courroie de distribution",

    # ==========================================================
    # EMBRAYAGE
    # ==========================================================
    "Remplacement de l'embrayage",
    "Remplacement embrayage",

    # ==========================================================
    # MOTEUR
    # ==========================================================
    "Remplacement moteur",
    "Remplacement du moteur",

    # ==========================================================
    # RODAGE
    # ==========================================================
    "Rodage",

    # ==========================================================
    # AUTRES
    # ==========================================================
    "transfert voiture",
    "Transfert voiture",
]


@register.filter
def db_trans(value):
    if not value:
        return "-"

    value = str(value).strip()

    # On cherche le descriptif fixe au début de la chaîne
    for descriptif in sorted(
        DESCRIPTIFS_TRADUISIBLES,
        key=len,
        reverse=True
    ):
        if value.startswith(descriptif):

            # Tout ce qui suit le descriptif reste inchangé
            reste = value[len(descriptif):]

            return f"{gettext(descriptif)}{reste}"

    # Si aucun descriptif connu n'est trouvé
    return gettext(value)