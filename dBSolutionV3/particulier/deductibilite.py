"""
Déductibilité des frais d'un véhicule selon le pays d'immatriculation (Europe).

Deux volets, pour un indépendant ou une société (un particulier ne déduit rien) :
  - TVA récupérable sur l'achat, la location (leasing / renting), le carburant, l'électricité et l'entretien ;
  - frais déductibles à l'impôt sur le revenu / des sociétés (amortissement de l'achat, frais, intérêts).

Règles générales indicatives (voitures de tourisme, 2026) : elles ne remplacent pas l'avis d'un comptable.
Le profil fiscal du véhicule permet d'imposer ses propres taux (taux_tva_manuel, taux_impot_manuel).

Modes TVA :
  « prorata » : taux × usage professionnel (ex. DE, LU, NL : 100 % de la part professionnelle) ;
  « plafond » : usage professionnel plafonné au taux (BE : au plus 50 %) ;
  « forfait » : taux fixe dès qu'il y a un usage professionnel (IT 40 %, ES / PL / RO / SK 50 %, FR carburant 80 %).
"""
from datetime import date
from decimal import Decimal as D

from django.utils.translation import gettext_lazy as _

from .calculs import ZERO, ajouter_mois, financement, r2
from .tva import taux_tva, ventiler


def _t(achat, location, entretien, essence, diesel=None, gpl=None, gnc=None, electricite=None):
    """Taux de TVA déductibles (%) par catégorie de frais."""
    diesel = essence if diesel is None else diesel
    return {"achat": achat, "location": location, "entretien": entretien, "essence": essence, "diesel": diesel,
            "gpl": diesel if gpl is None else gpl, "gnc": diesel if gnc is None else gnc,
            "electricite": essence if electricite is None else electricite}


def _uniforme(taux):
    return _t(taux, taux, taux, taux)


N_PRIVE_FORFAIT = _("L'usage privé d'une voiture de société est imposé à part (avantage en nature).")

# pays : mode TVA, taux TVA, taux TVA d'une voiture électrique (sinon les mêmes), règle impôt, notes
REGLES = {
    "AT": {"mode": "prorata", "tva": _uniforme(0), "tva_ve": _uniforme(100), "impot": "prorata",
           "notes": [_("Autriche : TVA récupérable seulement sur les voitures électriques (totalement jusqu'à 40 000 € TTC, "
                       "partiellement jusqu'à 80 000 €). Amortissement plafonné à 40 000 € (8 ans)."), N_PRIVE_FORFAIT]},
    "BE": {"mode": "plafond", "tva": _uniforme(50), "impot": "be",
           "notes": [_("Belgique : TVA déductible au maximum à 50 % (et pas plus que l'usage professionnel)."),
                     _("Belgique, impôt : formule CO2 (120 % − 0,5 % × coefficient × CO2, entre 50 % et 100 %). Société : "
                       "voiture thermique commandée depuis le 01/07/2023 dégressive (75 % en 2025, 50 % en 2026, 25 % en 2027, "
                       "0 % ensuite) ; électrique 100 % si commandée avant 2027."), N_PRIVE_FORFAIT]},
    "BG": {"mode": "forfait", "tva": _uniforme(0), "impot": "prorata", "notes": []},
    "HR": {"mode": "forfait", "tva": _uniforme(50), "impot": "prorata", "notes": []},
    "CY": {"mode": "forfait", "tva": _uniforme(0), "impot": "prorata", "notes": []},
    "CZ": {"mode": "prorata", "tva": _uniforme(100), "impot": "prorata",
           "notes": [_("Tchéquie : TVA de l'achat récupérable au plus sur 2 000 000 CZK de prix (plafond supprimé en 2027).")]},
    "DK": {"mode": "forfait", "tva": _t(0, 33.33, 0, 0), "impot": "prorata",
           "notes": [_("Danemark : TVA de location récupérable à un tiers ; pas de TVA récupérable sur l'achat ni le carburant.")]},
    "EE": {"mode": "forfait", "tva": _uniforme(50), "impot": "prorata",
           "notes": [_("Usage exclusivement professionnel : TVA récupérable à 100 %.")]},
    "FI": {"mode": "forfait", "tva": _uniforme(0), "impot": "prorata", "notes": []},
    "FR": {"mode": "forfait", "tva": _t(0, 0, 0, 80, 80, 100, 100, 100), "impot": "fr",
           "notes": [_("France : TVA non récupérable sur l'achat, la location et l'entretien d'une voiture de tourisme ; "
                       "carburant 80 %, GPL / GNV et électricité 100 %."),
                     _("France, impôt : amortissement plafonné selon le CO2 (30 000 € sous 20 g, 20 300 € de 20 à 49 g, "
                       "18 300 € de 50 à 130 g, 9 900 € au-delà).")]},
    "DE": {"mode": "prorata", "tva": _uniforme(100), "impot": "prorata",
           "notes": [_("Allemagne : usage privé imposé à 1 % du prix catalogue par mois (0,25 % pour une électrique) ou selon un carnet de bord.")]},
    "GR": {"mode": "forfait", "tva": _uniforme(0), "impot": "prorata", "notes": []},
    "HU": {"mode": "forfait", "tva": _t(0, 50, 50, 0), "impot": "prorata", "notes": []},
    "IE": {"mode": "prorata", "tva": _t(20, 20, 100, 0, 100, 100, 100, 100), "impot": "prorata",
           "notes": [_("Irlande : 20 % de la TVA d'achat ou de location récupérable si le CO2 est inférieur à 156 g/km "
                       "(usage professionnel d'au moins 60 %) ; TVA sur l'essence non récupérable.")]},
    "IT": {"mode": "forfait", "tva": _uniforme(40), "impot": "it",
           "notes": [_("Italie : TVA récupérable à 40 % ; frais déductibles à 20 % (70 % pour un véhicule attribué à un salarié), "
                       "achat retenu au plus à 18 075,99 €.")]},
    "LV": {"mode": "forfait", "tva": _uniforme(0), "impot": "prorata",
           "notes": [_("Usage exclusivement professionnel : TVA récupérable à 100 %.")]},
    "LT": {"mode": "forfait", "tva": _uniforme(0), "impot": "prorata", "notes": []},
    "LU": {"mode": "prorata", "tva": _uniforme(100), "impot": "prorata",
           "notes": [_("Luxembourg : TVA récupérable sur la part professionnelle ; avantage en nature de 0,5 % à 2 % du prix "
                       "catalogue par mois selon le CO2.")]},
    "MT": {"mode": "forfait", "tva": _uniforme(0), "impot": "prorata", "notes": []},
    "NL": {"mode": "prorata", "tva": _uniforme(100), "impot": "prorata",
           "notes": [_("Pays-Bas : TVA récupérable puis corrigée pour l'usage privé (forfait de 2,7 % du prix catalogue) ; "
                       "avantage en nature (bijtelling) de 22 %, réduit pour les électriques.")]},
    "PL": {"mode": "forfait", "tva": _uniforme(50), "impot": "prorata",
           "notes": [_("Usage exclusivement professionnel : TVA récupérable à 100 %.")]},
    "PT": {"mode": "forfait", "tva": _t(0, 0, 0, 0, 50, 50, 50, 100), "tva_ve": _t(100, 100, 0, 0, 50, 50, 50, 100),
           "impot": "prorata",
           "notes": [_("Portugal : TVA récupérable à 50 % sur le diesel, le GPL et le GNV, à 100 % sur l'électricité ; "
                       "achat d'une électrique jusqu'à 62 500 € (TVA récupérable).")]},
    "RO": {"mode": "forfait", "tva": _uniforme(50), "impot": "prorata", "notes": []},
    "SK": {"mode": "forfait", "tva": _uniforme(50), "impot": "prorata",
           "notes": [_("Slovaquie : depuis 2026, TVA récupérable à 50 % forfaitaire pour une voiture aussi utilisée à titre privé.")]},
    "SI": {"mode": "forfait", "tva": _uniforme(0), "impot": "prorata", "notes": []},
    "ES": {"mode": "forfait", "tva": _uniforme(50), "impot": "prorata",
           "notes": [_("Espagne : usage professionnel présumé à 50 % pour la TVA (plus si vous le prouvez).")]},
    "SE": {"mode": "prorata", "tva": _t(0, 50, 100, 100), "impot": "prorata", "notes": []},
    "GB": {"mode": "prorata", "tva": _t(0, 50, 100, 100), "impot": "prorata",
           "notes": [_("Royaume-Uni : TVA d'achat non récupérable (sauf usage exclusivement professionnel), location 50 % ; "
                       "TVA du carburant récupérable avec le forfait « fuel scale charge ».")]},
    "CH": {"mode": "prorata", "tva": _uniforme(100), "impot": "prorata",
           "notes": [_("Suisse : usage privé compté forfaitairement à 0,9 % du prix d'achat par mois.")]},
    "NO": {"mode": "forfait", "tva": _uniforme(0), "impot": "prorata", "notes": []},
}

PLAFONDS_FR = ((20, D(30000)), (50, D(20300)), (131, D(18300)), (None, D(9900)))   # CO2 < seuil → plafond
FAMILLE_CARBURANT = {"sp95": "essence", "sp95_e10": "essence", "sp98": "essence", "sp102": "essence", "e85": "essence",
                     "diesel": "diesel", "diesel_premium": "diesel", "hvo": "diesel", "gpl": "gpl", "gnc": "gnc",
                     "electricite": "electricite"}


# ------------------------------------------------------------------ Impôt
def formule_co2_be(vehicule, co2):
    """Belgique : 120 % − 0,5 % × coefficient × CO2, entre 50 % et 100 % (40 % à 200 g et plus)."""
    if vehicule.energie == "electrique" or co2 == 0:
        return D(100)
    if co2 is None:
        return None
    if co2 >= 200:
        return D(40)
    coef = {"diesel": D(1), "gnc": D("0.95")}.get(vehicule.energie, D("0.90"))
    return min(max(D(120) - D("0.5") * coef * D(co2), D(50)), D(100))


def taux_impot(vehicule, profil, annee, regle):
    """Part des frais déductible (%) avant l'usage professionnel, et une explication."""
    if profil.taux_impot_manuel is not None:
        return D(profil.taux_impot_manuel), _("taux imposé dans le profil")
    mode = regle["impot"] if regle else "prorata"
    if mode == "it":
        return D(20), _("Italie : 20 %")
    if mode != "be":
        return D(100), _("part professionnelle")
    formule = formule_co2_be(vehicule, profil.co2)
    if formule is None:
        return None, _("indiquez les émissions de CO2")
    commande = profil.date_commande or vehicule.date_achat
    if profil.statut != "societe" or commande is None or commande < date(2023, 7, 1):
        return formule, _("formule CO2")
    if vehicule.energie == "electrique":
        return {2027: D(95), 2028: D(90), 2029: D(85)}.get(commande.year, D(100) if commande.year < 2027 else D(75)), \
            _("électrique, selon l'année de commande")
    if commande.year >= 2026 and vehicule.energie != "phev":
        return D(0), _("thermique commandée depuis 2026")
    if vehicule.energie == "phev" and annee <= 2027:
        return min(formule, D(75)), _("hybride rechargeable : 75 % au plus jusqu'en 2027")
    plafond = {2024: D(100), 2025: D(75), 2026: D(50), 2027: D(25)}.get(annee, D(100) if annee < 2024 else D(0))
    return min(formule, plafond), _("thermique commandée depuis le 01/07/2023 : dégressif")


# ------------------------------------------------------------------ Calcul
def deductibilite(vehicule, annee=None, aujourdhui=None):
    from .models import ProfilFiscal
    aujourdhui = aujourdhui or date.today()
    annee = annee or aujourdhui.year
    pays = (vehicule.pays_immatriculation or "").upper()
    regle = REGLES.get(pays)
    profil = ProfilFiscal.objects.filter(vehicule=vehicule).first() or ProfilFiscal(vehicule=vehicule)
    prive = profil.statut == "particulier"
    usage = D(min(profil.usage_pro, 100))
    taux_std = taux_tva(pays)
    taux_tva_regle = (regle.get("tva_ve") if vehicule.energie == "electrique" else None) or (regle or {}).get("tva")
    pct_impot, explication_impot = taux_impot(vehicule, profil, annee, regle)

    def pct_tva(categorie):
        """TVA déductible (%) pour la catégorie, usage professionnel compris."""
        if prive or usage == 0:
            return ZERO
        if profil.taux_tva_manuel is not None:
            return D(profil.taux_tva_manuel)
        if not taux_tva_regle:
            return usage                                   # pays sans règle : part professionnelle
        taux = D(str(taux_tva_regle[categorie]))
        return {"prorata": taux * usage / 100, "plafond": min(taux, usage)}.get(regle["mode"], taux)

    def pct_frais():
        if prive or pct_impot is None:
            return ZERO
        return pct_impot * usage / 100

    lignes = []

    def ligne(code, ttc, tva=None, categorie=None, base_impot=None, deductible_impot=True, detail=""):
        ttc = r2(ttc)
        if not ttc:
            return
        tva = r2(tva or 0)
        p_tva = pct_tva(categorie) if categorie and tva else ZERO
        tva_ded = r2(tva * p_tva / 100)
        base = r2(base_impot if base_impot is not None else ttc - tva_ded)
        p_imp = pct_frais() if deductible_impot else ZERO
        lignes.append({"code": code, "detail": str(detail), "montant": ttc, "tva": tva, "taux_tva_deductible": r2(p_tva),
                       "tva_deductible": tva_ded, "base_impot": base, "taux_impot": r2(p_imp),
                       "deductible_impot": r2(base * p_imp / 100)})

    dans = lambda d: d is not None and d.year == annee and d <= aujourdhui  # noqa: E731

    # Énergie : TVA réelle de chaque plein / recharge
    for famille in ("essence", "diesel", "gpl", "gnc", "electricite"):
        pleins = [p for p in vehicule.pleins.all() if dans(p.date) and FAMILLE_CARBURANT.get(p.carburant) == famille]
        if pleins:
            tva = sum((D(p.montant_tva) if p.montant_tva is not None else (ventiler(p.montant, taux_std)[1] or ZERO)
                       for p in pleins), ZERO)
            ligne("electricite" if famille == "electricite" else "carburant", sum((D(p.montant) for p in pleins), ZERO),
                  tva, famille, detail=famille)

    def tva_std(montant):
        return ventiler(montant, taux_std)[1] or ZERO

    entretiens = sum((D(e.montant) for e in vehicule.entretiens.all() if dans(e.date)), ZERO)
    ligne("entretien", entretiens, tva_std(entretiens), "entretien")
    # Maintenances par un garage : TVA réelle de la facture (pièces + main-d'œuvre)
    maintenances = [m for m in vehicule.maintenances.all() if dans(m.date)]
    ligne("maintenances", sum((D(m.total_tvac) for m in maintenances), ZERO),
          sum((D(m.total_tva) for m in maintenances), ZERO), "entretien")

    # Assurances et taxes : sans TVA ; amendes : jamais déductibles
    sans_tva = sum((D(d.montant) for d in vehicule.documents.all() if dans(d.date_debut) and d.montant), ZERO)
    depenses = {}
    for d in vehicule.depenses.all():
        if dans(d.date):
            depenses[d.categorie] = depenses.get(d.categorie, ZERO) + D(d.montant)
    sans_tva += depenses.pop("taxe", ZERO) + depenses.pop("assurance", ZERO)
    ligne("assurances_taxes", sans_tva)
    ligne("amendes", depenses.pop("amende", ZERO), deductible_impot=False)
    autres = sum(depenses.values(), ZERO)
    ligne("autres", autres, tva_std(autres), "entretien")

    # Achat (comptant / prêt) : TVA l'année de l'achat, amortissement sur la durée choisie
    fin = financement(vehicule, aujourdhui)
    type_achat = fin["type_achat"] if fin else "comptant"
    if type_achat in ("comptant", "pret") and vehicule.prix_achat and vehicule.date_achat:
        prix = D(vehicule.prix_achat)
        tva_achat = tva_std(prix)
        p_tva = pct_tva("achat")
        tva_recup = r2(tva_achat * p_tva / 100)
        if vehicule.date_achat.year == annee:
            lignes.append({"code": "achat_tva", "detail": "", "montant": r2(prix), "tva": r2(tva_achat),
                           "taux_tva_deductible": r2(p_tva), "tva_deductible": tva_recup, "base_impot": ZERO,
                           "taux_impot": ZERO, "deductible_impot": ZERO})
        if vehicule.date_achat.year <= annee < vehicule.date_achat.year + profil.duree_amortissement:
            base = prix - tva_recup
            if regle and regle["impot"] == "fr":
                plafond = next(p for seuil, p in PLAFONDS_FR if seuil is None or (profil.co2 or 999) < seuil)
                base = min(base, plafond if profil.co2 is not None else PLAFONDS_FR[-1][1])
            if regle and regle["impot"] == "it":
                base = min(base, D("18075.99"))
            annuite = base / profil.duree_amortissement
            p_imp = pct_frais()
            lignes.append({"code": "amortissement", "detail": str(profil.duree_amortissement), "montant": r2(annuite),
                           "tva": ZERO, "taux_tva_deductible": ZERO, "tva_deductible": ZERO, "base_impot": r2(annuite),
                           "taux_impot": r2(p_imp), "deductible_impot": r2(annuite * p_imp / 100)})

    # Financement : intérêts du prêt (sans TVA), loyers de leasing / renting (avec TVA)
    if fin and fin.get("date_debut") and fin.get("mensualite"):
        debut, mensualite, duree = fin["date_debut"], D(fin["mensualite"]), fin.get("duree_mois") or 0
        if type_achat == "pret" and fin.get("capital"):
            restant, r, interets = D(fin["capital"]), D(vehicule.financement.taux_annuel or 0) / D(1200), ZERO
            for n in range(1, duree + 1):
                i = restant * r
                restant = max(restant - (mensualite - i), ZERO)
                if dans(ajouter_mois(debut, n)):
                    interets += i
            ligne("interets", interets)
        elif type_achat in ("leasing", "renting"):
            loyers = sum((mensualite for n in range(1, duree + 1) if dans(ajouter_mois(debut, n))), ZERO)
            if dans(debut):
                loyers += D(vehicule.financement.premier_loyer or 0)
            ligne("location", loyers, tva_std(loyers), "location")

    total = lambda cle: r2(sum((l[cle] for l in lignes), ZERO))  # noqa: E731
    return {
        "annee": annee,
        "pays": pays,
        "regles_disponibles": regle is not None,
        "mode_tva": regle["mode"] if regle else None,
        "taux_tva_pays": taux_std,
        "taux_regles": taux_tva_regle,
        "taux_impot": pct_impot,
        "explication_impot": str(explication_impot),
        "profil": {"statut": profil.statut, "usage_pro": profil.usage_pro, "co2": profil.co2,
                   "date_commande": profil.date_commande, "duree_amortissement": profil.duree_amortissement,
                   "taux_tva_manuel": profil.taux_tva_manuel, "taux_impot_manuel": profil.taux_impot_manuel,
                   "enregistre": profil.pk is not None},
        "lignes": lignes,
        "totaux": {"montant": total("montant"), "tva": total("tva"), "tva_deductible": total("tva_deductible"),
                   "deductible_impot": total("deductible_impot")},
        "notes": [str(n) for n in (regle or {}).get("notes", [])],
    }
