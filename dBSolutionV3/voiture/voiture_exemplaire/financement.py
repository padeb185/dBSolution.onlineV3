"""
Financement des véhicules : achat comptant, crédit, leasing financier (location-financement),
renting (leasing opérationnel) – échéancier, règles par usage et par pays, écritures comptables.

Usage du véhicule (VoitureExemplaire.type_utilisation) :
    location                        → véhicule de location : actif de la société, TVA déductible 100 %
    societe / utilitaire / interne  → véhicule de société : TVA déductible selon le pays
                                      (BE 50 % pour les voitures, 100 % pour les utilitaires ; DE 100 % ;
                                      FR 0 % pour les voitures particulières)
    prive / client                  → véhicule privé : suivi des coûts et amortissement économique,
                                      aucune écriture comptable

Écritures (comptes internes PCMN, convertis dans le plan national à l'affichage) :
    Achat comptant      immobilisation 241000 (amortie) payée par la banque
    Crédit              idem + emprunt 173000 : versement du prêt puis mensualités (capital 173000, intérêts 650000)
    Leasing financier   immobilisation 252000 (location-financement, amortie) / dette 172000 ;
                        loyers : capital 172000, intérêts 650000, TVA 411000 (part déductible),
                        TVA non déductible 610000 ; levée d'option en fin de contrat
    Renting             loyers en charge 612400 (+ TVA non déductible), TVA déductible 411000

⚠ Estimation à faire valider par le comptable (traitement fiscal des voitures, ATN, déductibilité).
"""
import calendar
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from django.utils.translation import gettext as _

D = Decimal
ZERO = D("0.00")
R2 = D("0.01")

COMPTE_IMMO_ROULANT = "241000"
COMPTE_IMMO_LF = "252000"
COMPTE_DETTE_LF = "172000"
COMPTE_EMPRUNT = "173000"
COMPTE_INTERETS = "650000"
COMPTE_TVA_DEDUCTIBLE = "411000"
COMPTE_TVA_NON_DEDUCTIBLE = "610000"
COMPTE_RENTING = "612400"
COMPTE_FOURNISSEURS = "440000"
COMPTE_BANQUE = "550000"

INTITULES = {
    COMPTE_DETTE_LF: _("Dettes de location-financement"),
    COMPTE_EMPRUNT: _("Emprunts auprès d'établissements de crédit"),
    COMPTE_INTERETS: _("Charges financières – intérêts"),
    COMPTE_TVA_DEDUCTIBLE: _("TVA à récupérer"),
    COMPTE_TVA_NON_DEDUCTIBLE: _("TVA non déductible (véhicules)"),
    COMPTE_RENTING: _("Locations de véhicules (renting / leasing opérationnel)"),
    COMPTE_FOURNISSEURS: _("Fournisseurs"),
    COMPTE_BANQUE: _("Banque"),
}


def r2(x):
    return D(x or 0).quantize(R2, rounding=ROUND_HALF_UP)


# ==================================================================
# RÈGLES PAR USAGE ET PAR PAYS
# ==================================================================
USAGE_LOCATION, USAGE_SOCIETE, USAGE_PRIVE = "location", "societe", "prive"

# TVA déductible (%) d'une voiture de société par pays (les utilitaires et la location : 100 %)
TVA_DEDUCTIBLE_VOITURE_SOCIETE = {"BE": D("50"), "FR": D("0"), "IT": D("40")}
# Durée d'amortissement usuelle d'une voiture (années)
DUREE_AMORTISSEMENT = {"BE": 5, "DE": 6, "FR": 5, "NL": 5, "LU": 4}


def usage(exemplaire):
    t = getattr(exemplaire, "type_utilisation", "") or ""
    if t == "location":
        return USAGE_LOCATION
    if t in ("societe", "utilitaire", "interne"):
        return USAGE_SOCIETE
    return USAGE_PRIVE


def libelle_usage(u):
    return {USAGE_LOCATION: _("Véhicule de location"), USAGE_SOCIETE: _("Véhicule de société"),
            USAGE_PRIVE: _("Véhicule privé")}[u]


def comptabilise(exemplaire):
    return usage(exemplaire) != USAGE_PRIVE


def tva_deductible_auto(exemplaire, pays):
    u = usage(exemplaire)
    if u == USAGE_PRIVE:
        return ZERO
    if u == USAGE_LOCATION or getattr(exemplaire, "type_utilisation", "") == "utilitaire":
        return D("100")
    return TVA_DEDUCTIBLE_VOITURE_SOCIETE.get(pays, D("100"))


def duree_amortissement_auto(pays):
    return DUREE_AMORTISSEMENT.get(pays, 5)


def ajouter_mois(d, n):
    m = d.month - 1 + n
    a = d.year + m // 12
    m = m % 12 + 1
    return date(a, m, min(d.day, calendar.monthrange(a, m)[1]))


# ==================================================================
# ÉCHÉANCIER
# ==================================================================
def mensualite_calculee(capital, taux_annuel, n, residuelle=ZERO):
    """Mensualité constante (annuité) remboursant `capital` en `n` mois, valeur résiduelle en fin de contrat."""
    capital, residuelle = D(capital or 0), D(residuelle or 0)
    if not n:
        return ZERO
    r = D(taux_annuel or 0) / 1200
    if r == 0:
        return r2((capital - residuelle) / n)
    facteur = (1 + r) ** n
    return r2((capital - residuelle / facteur) * r / (1 - 1 / facteur))


def echeancier(f):
    """
    Lignes {num, date, mensualite, interet, capital, solde, tva, option} du contrat.
    Crédit : montants TVAC (le prêt finance le prix TVAC – apport).
    Leasing financier : loyers HTVA (+ TVA sur chaque loyer), levée d'option en dernière ligne.
    Renting : loyers HTVA constants (+ TVA), sans capital ni intérêts.
    """
    n = int(f.duree_mois or 0)
    if not n or not f.date_debut:
        return []
    taux_tva = D(f.taux_tva or 0)
    lignes = []
    if f.mode == f.Mode.RENTING:
        loyer = r2(f.mensualite_htva)
        for k in range(1, n + 1):
            lignes.append({"num": k, "date": ajouter_mois(f.date_debut, k), "mensualite": loyer, "interet": ZERO,
                           "capital": ZERO, "solde": ZERO, "tva": r2(loyer * taux_tva / 100), "option": False})
        return lignes
    if f.mode not in (f.Mode.CREDIT, f.Mode.LEASING):
        return []
    capital = capital_finance(f)
    residuelle = D(f.valeur_residuelle or 0) if f.mode == f.Mode.LEASING else ZERO
    mensualite = r2(f.mensualite_htva) if f.mensualite_htva else mensualite_calculee(capital, f.taux_interet, n, residuelle)
    r = D(f.taux_interet or 0) / 1200
    solde = capital
    for k in range(1, n + 1):
        interet = r2(solde * r)
        part = mensualite - interet
        if k == n:
            part = solde - residuelle          # dernière échéance : solde exact (arrondis)
        part = max(min(part, solde), ZERO)
        solde = r2(solde - part)
        montant = r2(part + interet)
        lignes.append({"num": k, "date": ajouter_mois(f.date_debut, k), "mensualite": montant, "interet": interet,
                       "capital": r2(part), "solde": solde,
                       "tva": r2(montant * taux_tva / 100) if f.mode == f.Mode.LEASING else ZERO, "option": False})
    if f.mode == f.Mode.LEASING and residuelle:
        lignes.append({"num": n + 1, "date": ajouter_mois(f.date_debut, n), "mensualite": residuelle, "interet": ZERO,
                       "capital": residuelle, "solde": ZERO, "tva": r2(residuelle * taux_tva / 100), "option": True})
    return lignes


def montant_tvac(f):
    return r2(D(f.valeur_htva or 0) * (1 + D(f.taux_tva or 0) / 100))


def capital_finance(f):
    if f.mode == f.Mode.CREDIT:
        return max(r2(montant_tvac(f) - D(f.apport or 0)), ZERO)
    if f.mode == f.Mode.LEASING:
        return max(r2(D(f.valeur_htva or 0) - D(f.apport or 0)), ZERO)
    return ZERO


def resume(f, aujourdhui=None):
    """Totaux du contrat et montants échus à la date du jour."""
    aujourdhui = aujourdhui or date.today()
    E = echeancier(f)
    ded = D(f.tva_deductible_effective) / 100
    echues = [l for l in E if l["date"] <= aujourdhui]
    tva_nd = lambda L: r2(sum((l["tva"] for l in L), ZERO) * (1 - ded))
    return {
        "echeancier": E,
        "nb_echeances": len([l for l in E if not l["option"]]),
        "mensualite": next((l["mensualite"] for l in E if not l["option"]), ZERO),
        "total": r2(sum((l["mensualite"] for l in E), ZERO)),
        "total_interets": r2(sum((l["interet"] for l in E), ZERO)),
        "total_tva": r2(sum((l["tva"] for l in E), ZERO)),
        "paye": r2(sum((l["mensualite"] for l in echues), ZERO)),
        "interets_payes": r2(sum((l["interet"] for l in echues), ZERO)),
        "tva_non_deductible_payee": tva_nd(echues),
        "capital_restant": echues[-1]["solde"] if echues else capital_finance(f),
        "capital_finance": capital_finance(f),
        "montant_tvac": montant_tvac(f),
        "fin": E[-1]["date"] if E else None,
    }


# ==================================================================
# COÛT POUR LA RENTABILITÉ DU VÉHICULE (HTVA + TVA non récupérable)
# ==================================================================
def cout_rentabilite(f, aujourdhui=None):
    """
    Remplace / complète le coût d'acquisition :
      achat : prix (inchangé) ; crédit : + intérêts échus ;
      leasing / renting : apport + loyers échus (HTVA + TVA non déductible) au lieu du prix d'achat.
    Retourne {"remplace_prix": bool, "lignes": {cle: montant}, "amortissement_annuel": montant}.
    """
    aujourdhui = aujourdhui or date.today()
    s = resume(f, aujourdhui)
    ded = D(f.tva_deductible_effective) / 100
    lignes = {}
    remplace = False
    apport = D(f.apport or 0) if f.date_debut and f.date_debut <= aujourdhui else ZERO
    if f.mode == f.Mode.CREDIT:
        lignes["interets"] = s["interets_payes"]
    elif f.mode in (f.Mode.LEASING, f.Mode.RENTING):
        remplace = True
        tva_apport = apport * D(f.taux_tva or 0) / 100 * (1 - ded)
        # les loyers échus comprennent déjà les intérêts du leasing
        lignes["loyers"] = r2(s["paye"] + apport + tva_apport + s["tva_non_deductible_payee"])
    duree = int(f.duree_amortissement_annees or 0)
    base = D(f.valeur_htva or 0) * (1 + D(f.taux_tva or 0) / 100 * (1 - ded)) - D(f.valeur_revente_estimee or 0)
    amort = r2(max(base, ZERO) / duree) if duree and f.mode != f.Mode.RENTING else ZERO
    return {"remplace_prix": remplace, "lignes": lignes, "amortissement_annuel": amort, "resume": s}


# ==================================================================
# ÉCRITURES (hors immobilisation, gérée par compta.Immobilisation)
# ==================================================================
def ecritures(f, debut=None, fin=None):
    ex = f.exemplaire
    if not comptabilise(ex) or f.mode == f.Mode.ACHAT or not f.date_debut:
        return []
    banque = f.compte_paiement.compte_pcmn if getattr(f, "compte_paiement", None) else COMPTE_BANQUE
    lib = f"{f.get_mode_display()} – {ex.immatriculation or ex}"
    piece = f"FIN-{str(f.pk)[:8]}"
    ded = D(f.tva_deductible_effective) / 100
    L = []

    def ligne(journal, jour, compte, debit=ZERO, credit=ZERO, libelle=lib):
        debit, credit = r2(debit), r2(credit)
        if (debit or credit) and (debut is None or jour >= debut) and (fin is None or jour <= fin):
            L.append({"journal": journal, "date": jour, "compte": compte, "intitule": INTITULES.get(compte, ""),
                      "libelle": libelle, "debit": debit, "credit": credit, "piece": piece, "source": "financement"})

    def paiement_tva(jour, journal, tva, libelle):
        ligne(journal, jour, COMPTE_TVA_DEDUCTIBLE, debit=tva * ded, libelle=libelle)
        ligne(journal, jour, COMPTE_TVA_NON_DEDUCTIBLE, debit=tva - r2(tva * ded), libelle=libelle)

    E = echeancier(f)
    taux_tva = D(f.taux_tva or 0)
    apport = D(f.apport or 0)

    if f.mode == f.Mode.CREDIT:
        cap = capital_finance(f)
        ligne("BQ", f.date_debut, banque, debit=cap, libelle=f"{_('Versement du prêt')} – {lib}")
        ligne("BQ", f.date_debut, COMPTE_EMPRUNT, credit=cap, libelle=f"{_('Versement du prêt')} – {lib}")
        for l in E:
            libm = f"{_('Mensualité')} {l['num']}/{len(E)} – {lib}"
            ligne("BQ", l["date"], COMPTE_EMPRUNT, debit=l["capital"], libelle=libm)
            ligne("BQ", l["date"], COMPTE_INTERETS, debit=l["interet"], libelle=libm)
            ligne("BQ", l["date"], banque, credit=l["mensualite"], libelle=libm)

    elif f.mode == f.Mode.LEASING:
        valeur = D(f.valeur_htva or 0)
        libd = f"{_('Contrat de location-financement')} – {lib}"
        # La reconnaissance de l'actif (252000 / fournisseurs) est passée par l'immobilisation liée
        ligne("OD", f.date_debut, COMPTE_FOURNISSEURS, debit=valeur, libelle=libd)
        ligne("OD", f.date_debut, COMPTE_DETTE_LF, credit=valeur, libelle=libd)
        if apport:
            liba = f"{_('Premier loyer / apport')} – {lib}"
            tva = r2(apport * taux_tva / 100)
            ligne("BQ", f.date_debut, COMPTE_DETTE_LF, debit=apport, libelle=liba)
            paiement_tva(f.date_debut, "BQ", tva, liba)
            ligne("BQ", f.date_debut, banque, credit=apport + tva, libelle=liba)
        nb = len([l for l in E if not l["option"]])
        for l in E:
            libm = (f"{_('Levée d’option')} – {lib}" if l["option"]
                    else f"{_('Loyer')} {l['num']}/{nb} – {lib}")
            ligne("BQ", l["date"], COMPTE_DETTE_LF, debit=l["capital"], libelle=libm)
            ligne("BQ", l["date"], COMPTE_INTERETS, debit=l["interet"], libelle=libm)
            paiement_tva(l["date"], "BQ", l["tva"], libm)
            ligne("BQ", l["date"], banque, credit=l["mensualite"] + l["tva"], libelle=libm)

    elif f.mode == f.Mode.RENTING:
        if apport:
            liba = f"{_('Premier loyer majoré')} – {lib}"
            tva = r2(apport * taux_tva / 100)
            ligne("BQ", f.date_debut, COMPTE_RENTING, debit=apport, libelle=liba)
            paiement_tva(f.date_debut, "BQ", tva, liba)
            ligne("BQ", f.date_debut, banque, credit=apport + tva, libelle=liba)
        for l in E:
            libm = f"{_('Loyer')} {l['num']}/{len(E)} – {lib}"
            ligne("BQ", l["date"], COMPTE_RENTING, debit=l["mensualite"], libelle=libm)
            paiement_tva(l["date"], "BQ", l["tva"], libm)
            ligne("BQ", l["date"], banque, credit=l["mensualite"] + l["tva"], libelle=libm)
    return L


# ==================================================================
# IMMOBILISATION LIÉE (achat, crédit, leasing financier – véhicule de location ou de société)
# ==================================================================
def synchroniser_immobilisation(f):
    """Crée / met à jour / supprime l'immobilisation comptable liée au financement."""
    from compta.models import CategorieImmobilisation, Immobilisation

    ex = f.exemplaire
    doit_exister = comptabilise(ex) and f.mode in (f.Mode.ACHAT, f.Mode.CREDIT, f.Mode.LEASING) and f.valeur_htva
    immo = f.immobilisation
    if not doit_exister:
        if immo:
            f.immobilisation = None
            type(f).objects.filter(pk=f.pk).update(immobilisation=None)
            immo.delete()
        return None

    leasing = f.mode == f.Mode.LEASING
    ded = D(f.tva_deductible_effective)
    tva = D(f.valeur_htva) * D(f.taux_tva or 0) / 100
    valeurs = {
        "societe": ex.societe,
        "categorie": CategorieImmobilisation.LOCATION_FINANCEMENT if leasing else CategorieImmobilisation.MATERIEL_ROULANT,
        "libelle": f"{ex.voiture_marque} {ex.voiture_modele}".strip()[:150] + f" – {libelle_usage(usage(ex))}",
        "immatriculation": (ex.immatriculation or "")[:50],
        "reference_facture": (f.contrat or "")[:100],
        "date_acquisition": f.date_debut,
        "valeur_acquisition": D(f.valeur_htva),
        # Leasing : la TVA est payée avec chaque loyer, pas à l'acquisition
        "taux_tva": ZERO if leasing else D(f.taux_tva or 0),
        "tva_deductible": ded,
        "frais_accessoires": ZERO if leasing else r2(tva * (1 - ded / 100)),
        "valeur_residuelle": ZERO,
        "methode": Immobilisation.Methode.LINEAIRE,
        "duree_annees": int(f.duree_amortissement_annees or duree_amortissement_auto("BE")),
        "compte_paiement": None if leasing else f.compte_paiement,
        "date_paiement": None if leasing else f.date_debut,
        "remarques": _("Créée automatiquement depuis le financement du véhicule (ne pas modifier ici)."),
    }
    if immo is None:
        immo = Immobilisation.objects.create(**valeurs)
        type(f).objects.filter(pk=f.pk).update(immobilisation=immo)
        f.immobilisation = immo
    else:
        for k, v in valeurs.items():
            setattr(immo, k, v)
        immo.save()
    return immo
