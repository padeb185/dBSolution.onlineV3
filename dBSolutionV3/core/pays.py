"""
Pays du tenant (société) : source unique utilisée par la TVA, les factures, Peppol,
les paiements, les ventes / locations, l'énergie et la comptabilité.

    from core.pays import pays_societe, profil_pays
    pays_societe()            -> "BE" (pays du tenant courant)
    pays_societe(societe)     -> pays d'une société donnée
    profil_pays()             -> dict : plan comptable, compta/paie natives, etc.

Ordre de résolution : Societe.pays → adresse de la société (code_pays) → BE.
"""
from django.db import connection
from django.utils.translation import gettext_lazy as _

PAYS_DEFAUT = "BE"

# Profils nationaux : ce que l'application sait faire nativement pour chaque pays.
# Le pays est celui de la société (nationalité : Societe.pays, sinon adresse). Pays gérés nativement :
# Belgique, puis Allemagne (ajoutée en premier). Les autres pays utilisent le profil générique
# (TVA, factures et Peppol suivent le pays, compta et paie restent sur le modèle belge).
PROFILS = {
    # Allemagne (premier pays ajouté) : paie allemande, journal et balance en SKR03.
    # Le bilan reste établi selon le schéma BNB (schéma HGB § 266 / § 275 pas encore disponible).
    "DE": {
        "plan_comptable": "SKR03",
        "plan_comptable_nom": _("SKR03 (DATEV Standardkontenrahmen 03)"),
        "comptes_annuels": _("Schéma BNB (belge) – schéma HGB (§ 266 / § 275) non disponible"),
        "compta_native": True,
        "paie_native": True,
        "bilan_natif": False,
    },
    "BE": {
        "plan_comptable": "PCMN",
        "plan_comptable_nom": _("Plan comptable minimum normalisé (PCMN)"),
        "comptes_annuels": _("Schéma BNB (Banque nationale de Belgique)"),
        "compta_native": True,
        "paie_native": True,
        "bilan_natif": True,
    },
}

PROFIL_GENERIQUE = {
    "plan_comptable": "PCMN",
    "plan_comptable_nom": _("Plan comptable minimum normalisé belge (PCMN) – plan national non disponible"),
    "comptes_annuels": _("Schéma BNB (belge) – modèle national non disponible"),
    "compta_native": False,
    "paie_native": False,
    "bilan_natif": False,
}


def _tva_config():
    from maintenance.choices import TVAConfig
    return TVAConfig


def normaliser_pays(valeur):
    """'be' / 'BE ' / 'Belgique' (non reconnu) → 'BE' ou '' si le code n'est pas géré."""
    code = str(valeur or "").strip()[:2].upper()
    if code == "EL":  # code TVA de la Grèce
        code = "GR"
    return code if code in _tva_config().TVA_PIECES else ""


def pays_de_societe(societe):
    """Code pays d'une société, ou '' si indéterminé."""
    if societe is None:
        return ""
    code = normaliser_pays(getattr(societe, "pays", ""))
    if code:
        return code
    try:
        adresse = getattr(societe, "adresse", None)
    except Exception:
        adresse = None
    return normaliser_pays(getattr(adresse, "code_pays", ""))


def societe_courante():
    """Société (tenant) active sur la connexion, ou None (schéma public / hors requête)."""
    tenant = getattr(connection, "tenant", None)
    if tenant is None or not hasattr(tenant, "pk") or not getattr(tenant, "pk", None):
        return None
    return tenant


def pays_societe(societe=None, defaut=PAYS_DEFAUT):
    """Pays de la société donnée, sinon du tenant courant, sinon `defaut` (BE)."""
    return pays_de_societe(societe) or pays_de_societe(societe_courante()) or defaut


def pays_tenant_defaut():
    """Valeur par défaut des champs « pays » des modèles : pays du tenant courant."""
    return pays_societe()


def profil_pays(code=None):
    code = normaliser_pays(code) or pays_societe()
    profil = dict(PROFILS.get(code, PROFIL_GENERIQUE))
    profil["code"] = code
    profil["nom"] = nom_pays(code)
    profil["taux_tva_normal"] = taux_tva_normal(code)
    return profil


def nom_pays(code=None):
    code = normaliser_pays(code) or pays_societe()
    return str(dict(_tva_config().PAYS_CHOICES).get(code, code))


def taux_tva_normal(code=None):
    TVAConfig = _tva_config()
    code = normaliser_pays(code) or pays_societe()
    return TVAConfig.TVA_PIECES.get(code, TVAConfig.TVA_PIECES[PAYS_DEFAUT])


def compta_native(code=None):
    return profil_pays(code)["compta_native"]


def paie_native(code=None):
    return profil_pays(code)["paie_native"]


def nom_pays_tenant():
    """Nom du pays du tenant courant (valeur initiale des champs « pays » des adresses)."""
    return nom_pays(pays_societe())
