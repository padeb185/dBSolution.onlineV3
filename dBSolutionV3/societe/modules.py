"""
Modules activables par tenant (société).

Toutes les apps restent installées dans chaque schéma (django-tenants ne permet pas d'installer
des apps différentes par tenant) : un module désactivé est masqué dans le tableau de bord et ses
URL sont refusées (dBSolutionV3/middleware/modules_tenant.py).

Societe.modules = None  → tous les modules (tenants existants, aucun changement)
Societe.modules = [...] → seuls les modules listés (le socle est toujours actif)

Socle (toujours actif) : véhicules et exemplaires, maintenances, agenda, utilisateurs, adresses, compte.
"""
from collections import OrderedDict

from django.utils.translation import gettext_lazy as _

# code : (libellé, description, préfixes d'URL après /tenant/<schéma>/<langue>/)
MODULES = OrderedDict([
    ("location", (_("Locations"), _("Locations de véhicules (circuit / route), ventes, statistiques et objectifs des vendeurs, pilotes."),
                  ["location/", "client_pilotage/"])),
    ("trackday", (_("Trackdays"), _("Organisation des trackdays : inscriptions, affichage, statistiques."),
                  ["location/trackdays/"])),
    ("proprietaires", (_("Propriétaires multiples"), _("Parts de propriété des véhicules et reversements aux propriétaires."),
                       ["proprietaire/", "location/reversements/"])),
    ("clients", (_("Clients atelier"), _("Clients particuliers, clients atelier et sociétés clientes."),
                 ["client_atelier/", "client_particulier/", "societe_cliente/"])),
    ("facturation", (_("Facturation"), _("Factures, notes de crédit, encaissements, TVA, Peppol, conditions générales."),
                     ["facture/"])),
    ("comptabilite", (_("Comptabilité"), _("Caisse, banque, journaux, immobilisations, bilan."),
                      ["compta/"])),
    ("paie", (_("Paie"), _("Fiches de paie mensuelles du personnel."),
              ["utilisateurs/paie/"])),
    ("main_oeuvre", (_("Main d'œuvre"), _("Taux horaires et temps de main d'œuvre de l'atelier."),
                     ["maindoeuvre/"])),
    ("stock", (_("Stock pièces et fluides"), _("Catalogue, stock, inventaire et sorties de pièces et fluides."),
               ["piece/"])),
    ("achats", (_("Fournisseurs et achats"), _("Fournisseurs, factures d'achat, statistiques fournisseurs."),
                ["fournisseurs/", "achat_mds/", "stats_fournisseurs/"])),
    ("outillage", (_("Outillage"), _("Inventaire et achats d'outillage."),
                   ["outillage/"])),
    ("energie", (_("Carburant et énergie"), _("Pleins de carburant, AdBlue et recharges électriques."),
                 ["fuel/", "adblue/", "recharge/"])),
    ("composants", (_("Suivi des composants"), _("Moteurs, boîtes de vitesses, embrayages, freins, pneus et jantes."),
                    ["voiture/moteur/", "voiture/boite/", "voiture/embrayage/", "voiture/freins/", "voiture/freins_ar/",
                     "voiture/pneus/", "voiture/jantes/"])),
    ("diagnostic", (_("Diagnostics"), _("Codes défaut relevés sur les véhicules."),
                    ["diagnostic/"])),
    ("carrosserie", (_("Carrosserie"), _("Carrosseries et carrossiers."),
                     ["carrosserie/"])),
    ("garages_externes", (_("Garages externes"), _("Garages officiels et maintenances réalisées à l'extérieur."),
                          ["garage_officiel/", "maintenance/externe/"])),
    ("parking", (_("Parking"), _("Emplacements et occupation du parking."),
                 ["parking/"])),
    ("remorques", (_("Remorques"), _("Remorques et leur suivi."),
                   ["voiture/remorques/"])),
    ("assurances", (_("Assurances"), _("Assureurs et polices d'assurance des véhicules."),
                    ["assurance/", "assurance_police/"])),
    ("finances_vehicules", (_("Finances des véhicules"), _("Prix d'achat, financement, coûts annuels et rentabilité des véhicules."),
                            ["voiture/exemplaires/finances/"])),
    ("revente", (_("Revente de véhicules"), _("Facture de vente, cession et bilan des véhicules d'occasion."),
                 ["voiture/ventes/"])),
])

# Modules qui n'ont de sens qu'avec un autre module
DEPENDANCES = {
    "proprietaires": ["location"],
    "revente": ["finances_vehicules"],
    "paie": ["comptabilite"],
}

TOUS = list(MODULES)

# Profils proposés à la création du tenant (la sélection reste modifiable case par case)
PROFILS = OrderedDict([
    ("complet", (_("Complet (tous les modules)"), TOUS)),
    ("garage", (_("Garage (atelier)"), [
        "clients", "facturation", "comptabilite", "paie", "main_oeuvre", "stock", "achats", "outillage",
        "composants", "diagnostic", "carrosserie", "garages_externes", "parking",
    ])),
    ("flotte_entreprise", (_("Flotte d'entreprise"), [
        "comptabilite", "achats", "energie", "composants", "diagnostic", "garages_externes", "parking",
        "remorques", "assurances", "finances_vehicules", "revente",
    ])),
    ("particulier", (_("Particulier (plus de cinq véhicules)"), [
        "energie", "composants", "diagnostic", "garages_externes", "remorques", "assurances",
        "finances_vehicules", "revente",
    ])),
])


def choix_modules():
    return [(code, libelle) for code, (libelle, _d, _p) in MODULES.items()]


def choix_profils():
    return [("", _("— Personnalisé —"))] + [(code, libelle) for code, (libelle, _m) in PROFILS.items()]


def normaliser(codes):
    """Codes connus + dépendances ; None si tous les modules sont actifs."""
    if codes is None:
        return None
    retenus = {c for c in codes if c in MODULES}
    for module, requis in DEPENDANCES.items():
        if module in retenus and not all(r in retenus for r in requis):
            retenus.discard(module)
    if retenus == set(TOUS):
        return None
    return [c for c in TOUS if c in retenus]


def profil_de(codes):
    """Profil correspondant exactement à une sélection, sinon ""."""
    actifs = set(TOUS if codes is None else codes)
    for code, (_l, modules) in PROFILS.items():
        if set(modules) == actifs:
            return code
    return ""


def module_de_chemin(chemin):
    """Module dont dépend un chemin relatif (préfixe le plus long), sinon None (socle)."""
    meilleur, longueur = None, 0
    for code, (_l, _d, prefixes) in MODULES.items():
        for p in prefixes:
            if chemin.startswith(p) and len(p) > longueur:
                meilleur, longueur = code, len(p)
    return meilleur


class ModulesActifs:
    """Accès dans les templates : {% if modules.location %} … {% endif %}"""

    def __init__(self, societe):
        codes = getattr(societe, "modules", None) if societe is not None else None
        self.codes = set(TOUS if codes is None else codes)
        self.tous = codes is None

    def __contains__(self, code):
        return code in self.codes

    def __getitem__(self, code):
        return code in self.codes

    def __getattr__(self, code):
        if code.startswith("_"):
            raise AttributeError(code)
        return code in self.codes

    def __bool__(self):
        return True
