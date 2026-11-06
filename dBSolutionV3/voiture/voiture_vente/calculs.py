"""
Revente d'un véhicule de la flotte : calculs de TVA, mentions légales, alertes et bilan financier.

Régimes de TVA (directive 2006/112/CE ; Belgique, France, Allemagne) :
    NORMAL    TVA sur le prix de vente. Base éventuellement limitée au pourcentage de TVA déduit
              à l'achat (tolérance administrative belge pour les voitures à déduction limitée).
    MARGE     Régime particulier des biens d'occasion : TVA comprise dans la marge
              (prix de vente − prix d'achat), non mentionnée sur la facture. Applicable uniquement
              si aucune TVA n'a été déduite à l'achat (achat à un particulier ou sous le régime de la marge).
    INTRACOM  Livraison intracommunautaire exonérée (acheteur assujetti dans un autre État membre).
    EXPORT    Exportation hors de l'Union européenne, exonérée.
    EXONERE   Exonéré : bien dont la TVA n'a pas pu être déduite à l'achat (ex. voiture particulière en France).

⚠ Traitement fiscal à faire valider par le comptable (régularisations, déductibilité, mentions).
"""
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from django.utils.translation import gettext_lazy as _

D = Decimal
ZERO = D("0.00")
CENT = D("100")

NORMAL, MARGE, INTRACOM, EXPORT, EXONERE = "NORMAL", "MARGE", "INTRACOM", "EXPORT", "EXONERE"
REGIMES_EXONERES = (INTRACOM, EXPORT, EXONERE)

# Durée de révision de la TVA déduite sur un bien d'investissement (années) – Belgique : 5 ans
DUREE_REVISION_TVA = {"BE": 5, "FR": 5, "DE": 5, "LU": 5, "NL": 5}

# Plafond des paiements en espèces entre un commerçant et un particulier (Belgique : 3 000 €)
PLAFOND_ESPECES = {"BE": D("3000"), "FR": D("1000")}


def r2(x):
    return D(x or 0).quantize(D("0.01"), rounding=ROUND_HALF_UP)


# ==================================================================
# PRIX ET TVA
# ==================================================================
def calculer_prix(regime, montant, saisie_tvac=False, taux=ZERO, pourcentage_taxable=CENT, prix_achat_marge=None):
    """
    Retourne {"htva", "base_tva", "tva", "tvac", "marge"} :
        htva      produit de la vente hors TVA (= prix de cession comptable)
        base_tva  base imposable déclarée (marge HTVA en régime de la marge)
        tva       TVA due
        tvac      montant facturé à l'acheteur
        marge     marge brute TVAC (régime de la marge uniquement)
    """
    montant = D(montant or 0)
    t = D(taux or 0) / CENT
    marge = None
    if regime == NORMAL:
        p = D(pourcentage_taxable if pourcentage_taxable is not None else CENT) / CENT
        htva = r2(montant / (1 + t * p)) if saisie_tvac else r2(montant)
        base = r2(htva * p)
        tva = r2(base * t)
        tvac = r2(htva + tva)
    elif regime == MARGE:
        tvac = r2(montant)
        marge = r2(tvac - D(prix_achat_marge or 0))
        if marge > 0 and t:
            tva = r2(marge * t / (1 + t))
            base = r2(marge - tva)
        else:
            tva, base = ZERO, ZERO
        htva = r2(tvac - tva)
    else:
        htva = tvac = r2(montant)
        base, tva = htva, ZERO
    return {"htva": htva, "base_tva": base, "tva": tva, "tvac": tvac, "marge": marge}


# ==================================================================
# MENTIONS LÉGALES SUR LA FACTURE
# ==================================================================
MENTIONS = {
    MARGE: {
        "BE": _("Régime particulier – biens d'occasion (art. 58, § 4, du Code de la TVA ; art. 313 de la directive 2006/112/CE). TVA non déductible par l'acheteur."),
        "FR": _("Régime particulier – biens d'occasion (art. 297 A du CGI ; art. 313 de la directive 2006/112/CE). TVA non récupérable par l'acheteur."),
        "DE": _("Gebrauchtgegenstände / Sonderregelung (§ 25a UStG ; art. 313 de la directive 2006/112/CE)."),
        "*": _("Régime particulier – biens d'occasion (art. 313 de la directive 2006/112/CE). TVA non déductible par l'acheteur."),
    },
    INTRACOM: {
        "BE": _("Livraison intracommunautaire exonérée de TVA (art. 39bis du Code de la TVA ; art. 138 de la directive 2006/112/CE)."),
        "FR": _("Exonération de TVA – livraison intracommunautaire (art. 262 ter, I du CGI ; art. 138 de la directive 2006/112/CE)."),
        "DE": _("Steuerfreie innergemeinschaftliche Lieferung (§ 4 Nr. 1b UStG ; art. 138 de la directive 2006/112/CE)."),
        "*": _("Livraison intracommunautaire exonérée de TVA (art. 138 de la directive 2006/112/CE)."),
    },
    EXPORT: {
        "BE": _("Exportation exonérée de TVA (art. 39 du Code de la TVA ; art. 146 de la directive 2006/112/CE)."),
        "FR": _("Exonération de TVA – exportation (art. 262, I du CGI ; art. 146 de la directive 2006/112/CE)."),
        "DE": _("Steuerfreie Ausfuhrlieferung (§ 4 Nr. 1a UStG ; art. 146 de la directive 2006/112/CE)."),
        "*": _("Exportation exonérée de TVA (art. 146 de la directive 2006/112/CE)."),
    },
    EXONERE: {
        "BE": _("Exonération de TVA – art. 44, § 2, 13°, du Code de la TVA (bien dont la TVA n'a pas été déduite à l'achat)."),
        "FR": _("Exonération de TVA – art. 261, 3, 1° du CGI (bien n'ayant pas ouvert droit à déduction)."),
        "DE": _("Steuerfrei gemäß § 4 Nr. 28 UStG."),
        "*": _("Exonération de TVA – art. 136 de la directive 2006/112/CE (bien n'ayant pas ouvert droit à déduction)."),
    },
}


def mention_legale(regime, pays):
    textes = MENTIONS.get(regime)
    if not textes:
        return ""
    return textes.get((pays or "").upper(), textes["*"])


# ==================================================================
# OUTILS
# ==================================================================
def mois_entre(debut, fin):
    if not debut or not fin:
        return None
    n = (fin.year - debut.year) * 12 + fin.month - debut.month
    if fin.day < debut.day:
        n -= 1
    return max(n, 0)


def tva_deduite_achat(vente):
    """(montant de TVA déduit à l'achat, pourcentage déduit) – immobilisation liée, sinon financement."""
    immo = vente.immobilisation
    if immo is not None:
        return r2(immo.tva_recuperable), D(immo.tva_deductible or 0)
    fv = getattr(vente.exemplaire, "financement", None) if vente.exemplaire_id else None
    if fv is not None and fv.valeur_htva and fv.mode != fv.Mode.RENTING:
        ded = D(fv.tva_deductible_effective)
        return r2(D(fv.valeur_htva) * D(fv.taux_tva or 0) / CENT * ded / CENT), ded
    return None, None


def revision_tva(vente, pays="BE"):
    """
    Estimation de la TVA déduite à reverser lorsqu'un véhicule (bien d'investissement) est revendu
    sans TVA pendant la période de révision : TVA déduite × années restantes / durée.
    Période : année d'acquisition + (durée − 1) ans.
    """
    if vente.regime_tva not in (EXONERE, MARGE):
        return None
    tva, _pct = tva_deduite_achat(vente)
    if not tva:
        return None
    immo = vente.immobilisation
    fv = getattr(vente.exemplaire, "financement", None) if vente.exemplaire_id else None
    debut = immo.date_acquisition if immo else (fv.date_debut if fv else None)
    if not debut or not vente.date_vente:
        return None
    duree = DUREE_REVISION_TVA.get((pays or "BE").upper(), 5)
    restantes = max(0, (debut.year + duree - 1) - vente.date_vente.year)
    if not restantes:
        return None
    return {"tva_deduite": tva, "annees_restantes": restantes, "duree": duree,
            "montant": r2(tva * restantes / duree)}


# ==================================================================
# ALERTES
# ==================================================================
def alertes(vente, pays="BE"):
    """[(niveau, message)] – niveau : "erreur" (bloque l'émission), "attention" ou "info"."""
    A = []
    ex = vente.exemplaire
    fv = getattr(ex, "financement", None) if vente.exemplaire_id else None
    ref = vente.date_vente or date.today()

    if fv is not None:
        from voiture.voiture_exemplaire.financement import resume
        if fv.mode == fv.Mode.RENTING:
            A.append(("erreur", _("Véhicule en renting : il appartient à la société de renting et ne peut pas être revendu par la société.")))
        elif fv.mode == fv.Mode.LEASING:
            s = resume(fv, ref)
            if s["fin"] and s["fin"] > ref:
                A.append(("attention", _("Leasing financier en cours (fin le %(fin)s) : l'option d'achat doit être levée avant la revente.") % {"fin": s["fin"].strftime("%d/%m/%Y")}))
        elif fv.mode == fv.Mode.CREDIT:
            s = resume(fv, ref)
            if s["capital_restant"] and s["capital_restant"] > 0:
                A.append(("attention", _("Crédit en cours : capital restant dû de %(m)s € à rembourser à l'organisme prêteur.") % {"m": f"{s['capital_restant']:.2f}"}))

    tva, pct = tva_deduite_achat(vente)
    if vente.regime_tva == MARGE and tva:
        A.append(("erreur", _("Régime de la marge non applicable : la TVA a été déduite à l'achat (%(p)s %%). Utilisez le régime normal.") % {"p": f"{pct:.0f}"}))
    if vente.regime_tva == MARGE and not vente.prix_achat_marge:
        A.append(("attention", _("Régime de la marge : indiquez le prix d'achat TVAC pour calculer la marge.")))
    if vente.regime_tva == EXONERE and tva:
        A.append(("attention", _("Vente exonérée alors que de la TVA a été déduite à l'achat : vérifiez le régime et la révision de la déduction avec votre comptable.")))
    rev = revision_tva(vente, pays)
    if rev:
        A.append(("attention", _("Révision de la TVA déduite estimée à %(m)s € (%(n)s année(s) restante(s) sur %(d)s).") % {
            "m": f"{rev['montant']:.2f}", "n": rev["annees_restantes"], "d": rev["duree"]}))
    if vente.regime_tva == NORMAL and pct is not None and pct < CENT and vente.pourcentage_taxable >= CENT and (pays or "").upper() == "BE":
        A.append(("info", _("TVA déduite à %(p)s %% à l'achat : la TVA due sur la revente peut être limitée au même pourcentage (pourcentage taxable). À valider par le comptable.") % {"p": f"{pct:.0f}"}))

    if vente.regime_tva == INTRACOM:
        if not (vente.acheteur_tva or "").strip():
            A.append(("erreur", _("Livraison intracommunautaire : le numéro de TVA de l'acheteur est obligatoire.")))
        if (vente.acheteur_pays or "").upper() == (pays or "").upper():
            A.append(("erreur", _("Livraison intracommunautaire : l'acheteur doit être établi dans un autre État membre.")))
        mois = mois_entre(ex.date_mise_en_circulation, ref) if ex.date_mise_en_circulation else None
        km = vente.kilometrage_vente
        if (mois is not None and mois <= 6) or (km is not None and km <= 6000):
            A.append(("attention", _("Moyen de transport neuf (≤ 6 mois ou ≤ 6 000 km) : la TVA est due dans le pays de destination ; une déclaration spécifique peut être requise.")))
        A.append(("info", _("Conservez la preuve du transport (CMR, document d'immatriculation à l'étranger) et reprenez la livraison dans le relevé intracommunautaire.")))
    if vente.regime_tva == EXPORT:
        A.append(("info", _("Conservez la preuve de sortie de l'Union (document d'exportation visé par la douane).")))

    plafond = PLAFOND_ESPECES.get((pays or "").upper())
    if plafond and vente.mode_paiement == "ESPECES" and vente.prix_tvac > plafond:
        A.append(("attention", _("Paiement en espèces supérieur au plafond légal de %(p)s € : seuls 10 %% du prix peuvent être payés en espèces.") % {"p": f"{plafond:.0f}"}))

    if vente.immobilisation is None and fv is not None and fv.mode in (fv.Mode.ACHAT, fv.Mode.CREDIT, fv.Mode.LEASING) and fv.comptabilise:
        A.append(("attention", _("Aucune immobilisation liée : la sortie de l'actif et la plus-value ne seront pas comptabilisées.")))
    if vente.type_acheteur == "PARTICULIER" and not vente.garantie_mois:
        A.append(("info", _("Vente à un consommateur : la garantie légale de conformité s'applique (au moins 1 an pour un bien d'occasion vendu par un professionnel).")))
    return A


def peut_emettre(vente, pays="BE"):
    return not any(niveau == "erreur" for niveau, _m in alertes(vente, pays))


# ==================================================================
# BILAN FINANCIER
# ==================================================================
def bilan(vente):
    ex = vente.exemplaire
    from voiture.voiture_exemplaire.rentabilite import date_depart, rentabilite

    rent = rentabilite(ex)
    produit = r2(vente.prix_htva)
    frais = r2(vente.frais_vente_htva)

    # Valeur nette comptable et plus / moins-value
    immo = vente.immobilisation
    vnc = plus_value = None
    if immo is not None and vente.date_vente:
        vnc = r2(immo.valeur_comptable_brute - immo.cumul_fin(vente.date_vente.year - 1))
        plus_value = r2(produit - vnc)

    # Coût de détention : le calcul de rentabilité déduit la valeur de revente ; on repart du coût total
    cout_total = r2(rent["cout_total"])
    revenus = r2(rent["locations"]["htva"])
    resultat = r2(revenus + produit - cout_total - frais)

    debut = date_depart(ex)
    mois = mois_entre(debut, vente.date_vente)
    km_achat = int(ex.kilometrage_achat or 0)
    km = max(int(vente.kilometrage_vente or 0) - km_achat, 0) if vente.kilometrage_vente else rent["km"]
    cout_net = r2(cout_total + frais - produit)

    estimee = vente.valeur_revente_avant if vente.valeur_revente_avant is not None else ex.valeur_revente
    ecart = r2(produit - D(estimee)) if estimee else None

    return {
        "rent": rent,
        "produit": produit,
        "frais": frais,
        "vnc": vnc,
        "plus_value": plus_value,
        "cout_total": cout_total,
        "cout_net": cout_net,
        "revenus": revenus,
        "resultat": resultat,
        "debut": debut,
        "mois": mois,
        "km": km,
        "cout_km": (cout_net / km).quantize(D("0.001"), rounding=ROUND_HALF_UP) if km else None,
        "cout_mois": r2(cout_net / mois) if mois else None,
        "valeur_estimee": r2(estimee) if estimee else None,
        "ecart_estimation": ecart,
    }
