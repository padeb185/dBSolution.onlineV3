"""
Composants d'échappement : une app par composant.
Liste centralisée (ordre d'affichage du dashboard échappement) et comptages.
"""
from importlib import import_module

from django.utils.translation import gettext_lazy as _

# (app / namespace, classe du modèle, libellé)
COMPOSANTS_ECHAPPEMENT = [
    ("collecteur", "Collecteur", _("Collecteur d'échappement")),
    ("catalyseur", "Catalyseur", _("Catalyseur")),
    ("silencieux", "Silencieux", _("Silencieux")),
    ("filtre_particules", "FiltreParticules", _("Filtre à particules (FAP)")),
    ("pot_denox", "PotDenox", _("Pot DeNOx (SCR)")),
    ("sonde_lambda_amont", "SondeLambdaAmont", _("Sonde lambda amont")),
    ("sonde_lambda_aval", "SondeLambdaAval", _("Sonde lambda aval")),
    ("sonde_fap_amont", "SondeFapAmont", _("Sonde de température FAP amont")),
    ("sonde_fap_aval", "SondeFapAval", _("Sonde de température FAP aval")),
    ("capteur_fap", "CapteurFap", _("Capteur de pression différentielle FAP")),
    ("tuyaux_fap", "TuyauxFap", _("Tuyaux du capteur FAP")),
    ("regeneration_fap", "RegenerationFap", _("Régénération du FAP")),
    ("injecteur_adblue", "InjecteurAdblue", _("Injecteur AdBlue")),
    ("valves_echappement", "ValvesEchappement", _("Valves d'échappement")),
    ("silent_blocs_echappement", "SilentBlocsEchappement", _("Silent blocs d'échappement")),
]


def modele_composant(app):
    for code, classe, _label in COMPOSANTS_ECHAPPEMENT:
        if code == app:
            module = import_module(f"maintenance.autres_interventions.echappement.{code}.models")
            return getattr(module, classe)
    raise LookupError(app)


def composants_echappement(exemplaire):
    """[{code, label, total, url_list, icone}] pour un véhicule."""
    lignes = []
    for code, classe, label in COMPOSANTS_ECHAPPEMENT:
        total = modele_composant(code).objects.filter(voiture_exemplaire=exemplaire).count() if exemplaire else 0
        lignes.append({
            "code": code,
            "label": label,
            "total": total,
            "url_list": f"{code}:{code}_list",
            "icone": f"icons/ech_{code}.png",
        })
    return lignes


def total_composants_echappement(exemplaire):
    return sum(l["total"] for l in composants_echappement(exemplaire))
