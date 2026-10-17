"""
Totaux énergie (carburants, recharges électriques, AdBlue)
+ ventilation TVA par pays + écritures comptables (PCMN belge).

Utilisé par fuel/views_totaux.py (écran, PDF, CSV).
"""
import calendar
from collections import OrderedDict
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP

from django.utils import timezone
from django.utils.translation import gettext as _, gettext_noop

from adblue.models import AdBlue
from recharge.models import Electricite, RechargeCarburant
from .models import Fuel, TypeCarburant

ZERO = Decimal("0.00")


def r2(x):
    return Decimal(x or 0).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# ==================================================================
# PARAMÈTRES COMPTABLES (à adapter au plan comptable de la société)
# ==================================================================
COMPTE_CARBURANT = "612700"
COMPTE_ELECTRICITE = "612710"
COMPTE_ADBLUE = "612720"
COMPTE_TVA_DEDUCTIBLE = "411000"
COMPTE_TVA_ETRANGERE = "416100"
COMPTE_CONTREPARTIE = "550000"

COMPTES = OrderedDict([
    (COMPTE_CARBURANT, gettext_noop("Carburants véhicules")),
    (COMPTE_ELECTRICITE, gettext_noop("Recharges électriques véhicules")),
    (COMPTE_ADBLUE, gettext_noop("AdBlue")),
    (COMPTE_TVA_DEDUCTIBLE, gettext_noop("TVA à récupérer")),
    (COMPTE_TVA_ETRANGERE, gettext_noop("TVA étrangère à récupérer (remboursement UE)")),
    (COMPTE_CONTREPARTIE, gettext_noop("Banque – compte courant")),
])

PAYS_SOCIETE = "BE"
PAYS_HORS_UE = {"GB"}

FAMILLES = OrderedDict([
    ("carburant", {"label": gettext_noop("Carburants"), "compte": COMPTE_CARBURANT, "prefixe": "CARB"}),
    ("electricite", {"label": gettext_noop("Recharges électriques"), "compte": COMPTE_ELECTRICITE, "prefixe": "ELEC"}),
    ("adblue", {"label": gettext_noop("AdBlue"), "compte": COMPTE_ADBLUE, "prefixe": "ADB"}),
])

MOIS_NOMS = [
    "", gettext_noop("Janvier"), gettext_noop("Février"), gettext_noop("Mars"), gettext_noop("Avril"), gettext_noop("Mai"), gettext_noop("Juin"),
    gettext_noop("Juillet"), gettext_noop("Août"), gettext_noop("Septembre"), gettext_noop("Octobre"), gettext_noop("Novembre"), gettext_noop("Décembre"),
]


# ==================================================================
# PÉRIODE
# ==================================================================
class Periode:
    """type_ = 'mois' | 'trimestre' | 'annee'."""

    def __init__(self, type_, annee, mois=None, trimestre=None):
        self.type = type_
        self.annee = annee
        self.mois = mois
        self.trimestre = trimestre
        if type_ == "mois":
            self.liste_mois = [mois]
        elif type_ == "trimestre":
            self.liste_mois = [3 * (trimestre - 1) + i for i in (1, 2, 3)]
        else:
            self.liste_mois = list(range(1, 13))
        self.debut = date(annee, self.liste_mois[0], 1)
        dm = self.liste_mois[-1]
        self.fin = date(annee, dm, calendar.monthrange(annee, dm)[1])

    @classmethod
    def depuis_requete(cls, request):
        today = timezone.localdate()
        g = request.GET

        def entier(nom, defaut):
            try:
                return int(g.get(nom) or defaut)
            except (TypeError, ValueError):
                return defaut

        type_ = g.get("periode") if g.get("periode") in ("mois", "trimestre", "annee") else "mois"
        annee = entier("annee", today.year)
        mois = min(max(entier("mois", today.month), 1), 12)
        trimestre = min(max(entier("trimestre", (today.month - 1) // 3 + 1), 1), 4)
        return cls(type_, annee, mois=mois, trimestre=trimestre)

    @property
    def libelle(self):
        if self.type == "mois":
            return f"{_(MOIS_NOMS[self.mois])} {self.annee}"
        if self.type == "trimestre":
            return f"T{self.trimestre} {self.annee}"
        return str(self.annee)

    @property
    def slug(self):
        if self.type == "mois":
            return f"{self.annee}-{self.mois:02d}"
        if self.type == "trimestre":
            return f"{self.annee}-T{self.trimestre}"
        return str(self.annee)

    def querystring(self):
        qs = f"periode={self.type}&annee={self.annee}"
        if self.type == "mois":
            qs += f"&mois={self.mois}"
        elif self.type == "trimestre":
            qs += f"&trimestre={self.trimestre}"
        return qs


# ==================================================================
# COLLECTE DES OPÉRATIONS
# ==================================================================
def _jour(d):
    if isinstance(d, datetime):
        return timezone.localtime(d).date() if timezone.is_aware(d) else d.date()
    return d


def _ventiler(ttc, ht, tva, taux):
    """Utilise HT/TVA enregistrés ; recalcule si absents."""
    ttc = r2(ttc)
    if ht is not None and tva is not None and (ht or tva or not ttc):
        return r2(ht), r2(tva)
    ht = r2(ttc / (Decimal("1") + Decimal(str(taux)) / Decimal("100")))
    return ht, ttc - ht


def _vehicule(obj):
    ve = getattr(obj, "voiture_exemplaire", None)
    if not ve:
        return "—", getattr(obj, "immatriculation", "") or "—"
    try:
        nom = f"{ve.voiture_modele.voiture_marque.nom_marque} {ve.voiture_modele.nom_modele}"
    except Exception:
        nom = str(ve)
    return nom, ve.immatriculation or getattr(obj, "immatriculation", "") or "—"


def _marque(obj):
    try:
        return obj.voiture_exemplaire.voiture_modele.voiture_marque.nom_marque.strip()
    except Exception:
        return ""


def _modele(obj):
    try:
        m = obj.voiture_exemplaire.voiture_modele
        return " ".join(x for x in (m.nom_modele, getattr(m, "nom_variante", "")) if x)
    except Exception:
        return ""


def operations(societe, periode):
    pays_labels = dict(Fuel.PAYS_CHOICES)
    labels_carburant = dict(TypeCarburant.choices)
    ops = []

    def ajouter(famille, obj, categorie, categorie_label, quantite, unite, ttc, taux, piece):
        ht, tva = _ventiler(ttc, obj.montant_ht, obj.montant_tva, taux)
        vehicule, immat = _vehicule(obj)
        pays = obj.pays or PAYS_SOCIETE
        ops.append({
            "famille": famille,
            "famille_label": _(FAMILLES[famille]["label"]),
            "categorie": categorie,
            "categorie_label": categorie_label,
            "date": _jour(obj.date),
            "piece": piece,
            "vehicule": vehicule,
            "immatriculation": immat,
            "pays_vehicule": getattr(getattr(obj, "voiture_exemplaire", None), "pays", "") or "",
            "marque": _marque(obj),
            "modele": _modele(obj),
            "station": getattr(obj, "nom_station", "") or "",
            "pays": pays,
            "pays_nom": str(pays_labels.get(pays, pays)),
            "taux": Decimal(str(taux)),
            "quantite": Decimal(str(quantite or 0)),
            "unite": unite,
            "ttc": r2(ttc),
            "ht": ht,
            "tva": tva,
        })

    sel = ("voiture_exemplaire", "voiture_exemplaire__voiture_modele",
           "voiture_exemplaire__voiture_modele__voiture_marque")

    for f in (Fuel.objects.filter(societe=societe, date__year=periode.annee,
                                  date__month__in=periode.liste_mois).select_related(*sel)):
        ajouter("carburant", f, f.type_carburant, str(labels_carburant.get(f.type_carburant, f.type_carburant)),
                f.litres, "L", f.prix_refuelling, Fuel.TVA_CARBURANT.get(f.pays, 0), f"CARB-{f.pk}")

    for e in (Electricite.objects.filter(societe=societe, date__year=periode.annee,
                                         date__month__in=periode.liste_mois).select_related(*sel)):
        ajouter("electricite", e, "ELECTRICITE", _("Électricité"),
                e.kW, "kWh", e.prix_recharge,
                RechargeCarburant.TVA_ELECTRICITE.get(e.pays or PAYS_SOCIETE, 0), f"ELEC-{str(e.pk)[:8]}")

    for a in (AdBlue.objects.filter(societe=societe, date__year=periode.annee,
                                    date__month__in=periode.liste_mois).select_related(*sel)):
        ajouter("adblue", a, "ADBLUE", _("AdBlue"),
                a.litres, "L", a.prix_adblue, AdBlue.TVA_CARBURANT.get(a.pays, 0), f"ADB-{a.pk}")

    ops.sort(key=lambda o: (o["date"], o["famille"], o["piece"]))
    return ops


# ==================================================================
# TOTAUX
# ==================================================================
def _vide():
    return {"nb": 0, "quantite": Decimal("0"), "ht": ZERO, "tva": ZERO, "ttc": ZERO}


def _cumuler(t, o):
    t["nb"] += 1
    t["quantite"] += o["quantite"]
    t["ht"] += o["ht"]
    t["tva"] += o["tva"]
    t["ttc"] += o["ttc"]


def regime_tva(pays):
    if pays == PAYS_SOCIETE:
        return "deductible"
    if pays in PAYS_HORS_UE:
        return "non_recuperable"
    return "remboursement_ue"


REGIMES = {
    "deductible": gettext_noop("Déductible (déclaration TVA belge)"),
    "remboursement_ue": gettext_noop("À récupérer via la procédure de remboursement UE"),
    "non_recuperable": gettext_noop("Non récupérable (hors UE)"),
}


def totaux(ops, periode, deduction=Decimal("100")):
    total = _vide()

    # --- par famille / par catégorie (essence 95, 98, diesel, électricité, AdBlue…)
    par_famille = OrderedDict((k, dict(_vide(), label=_(v["label"]), unites=set())) for k, v in FAMILLES.items())
    par_categorie = OrderedDict()

    # --- par pays (avec détail par famille)
    par_pays = OrderedDict()

    # --- sous-périodes
    par_mois = OrderedDict((m, dict(_vide(), label=_(MOIS_NOMS[m]))) for m in periode.liste_mois)
    par_trimestre = OrderedDict()
    if periode.type == "annee":
        par_trimestre = OrderedDict((t, dict(_vide(), label=f"T{t}")) for t in (1, 2, 3, 4))

    # --- par véhicule
    par_vehicule = OrderedDict()

    for o in ops:
        _cumuler(total, o)

        pf = par_famille[o["famille"]]
        _cumuler(pf, o)
        pf["unites"].add(o["unite"])

        cle_cat = (o["famille"], o["categorie"])
        if cle_cat not in par_categorie:
            par_categorie[cle_cat] = dict(_vide(), label=o["categorie_label"], famille=o["famille_label"],
                                          unite=o["unite"])
        _cumuler(par_categorie[cle_cat], o)

        p = o["pays"]
        if p not in par_pays:
            par_pays[p] = dict(_vide(), code=p, nom=o["pays_nom"], taux=o["taux"],
                               regime=regime_tva(p), regime_label=_(REGIMES[regime_tva(p)]),
                               familles=OrderedDict((k, _vide()) for k in FAMILLES))
        _cumuler(par_pays[p], o)
        _cumuler(par_pays[p]["familles"][o["famille"]], o)

        _cumuler(par_mois[o["date"].month], o)
        if par_trimestre:
            _cumuler(par_trimestre[(o["date"].month - 1) // 3 + 1], o)

        cle_v = o["immatriculation"]
        if cle_v not in par_vehicule:
            par_vehicule[cle_v] = dict(_vide(), vehicule=o["vehicule"], immatriculation=cle_v,
                                       pays_vehicule=o["pays_vehicule"],
                                       marque=o["marque"], modele=o["modele"],
                                       logo=f"images/marques/{o['marque'].lower()}.png" if o["marque"] else "",
                                       familles=OrderedDict((k, ZERO) for k in FAMILLES))
        _cumuler(par_vehicule[cle_v], o)
        par_vehicule[cle_v]["familles"][o["famille"]] += o["ttc"]

    for pf in par_famille.values():
        pf["unite"] = " / ".join(sorted(pf.pop("unites")))
    for c in par_categorie.values():
        c["prix_moyen"] = (c["ttc"] / c["quantite"]).quantize(Decimal("0.001")) if c["quantite"] else None
    for pays in par_pays.values():
        pays["familles_liste"] = [dict(v, code=k, label=_(FAMILLES[k]["label"]))
                                  for k, v in pays["familles"].items() if v["nb"]]

    pays_tries = sorted(par_pays.values(), key=lambda x: (x["code"] != PAYS_SOCIETE, x["nom"]))

    # --- synthèse TVA par régime
    regimes = OrderedDict((k, {"code": k, "label": _(v), "ht": ZERO, "tva": ZERO, "ttc": ZERO})
                          for k, v in REGIMES.items())
    for p in pays_tries:
        r = regimes[p["regime"]]
        r["ht"] += p["ht"]
        r["tva"] += p["tva"]
        r["ttc"] += p["ttc"]

    # --- grilles de la déclaration TVA belge (achats en Belgique)
    be = par_pays.get(PAYS_SOCIETE)
    tva_be = be["tva"] if be else ZERO
    tva_be_deductible = r2(tva_be * deduction / Decimal("100"))
    declaration_be = {
        "grille_82": be["ht"] if be else ZERO,
        "grille_59": tva_be_deductible,
        "tva_non_deductible": tva_be - tva_be_deductible,
    }

    return {
        "total": total,
        "par_famille": [dict(v, code=k) for k, v in par_famille.items()],
        "par_categorie": list(par_categorie.values()),
        "par_pays": pays_tries,
        "regimes": [r for r in regimes.values() if r["ttc"]],
        "par_mois": list(par_mois.values()) if periode.type != "mois" else [],
        "par_trimestre": list(par_trimestre.values()),
        "par_vehicule": sorted(par_vehicule.values(), key=lambda v: -v["ttc"]),
        "declaration_be": declaration_be,
        "echeance_remboursement_ue": date(periode.annee + 1, 9, 30),
    }


# ==================================================================
# COMPTABILITÉ
# ==================================================================
def ecritures(o, deduction=Decimal("100")):
    """Écriture d'achat d'une opération : liste de lignes {compte, intitule, libelle, debit, credit}."""
    L = []

    def ligne(compte, libelle, debit=ZERO, credit=ZERO):
        debit, credit = r2(debit), r2(credit)
        if debit or credit:
            L.append({"compte": compte, "intitule": _(COMPTES[compte]), "libelle": libelle,
                      "debit": debit, "credit": credit})

    compte_charge = FAMILLES[o["famille"]]["compte"]
    libelle = f"{o['categorie_label']} – {o['immatriculation']} – {o['pays']}"
    regime = regime_tva(o["pays"])

    ligne(compte_charge, libelle, debit=o["ht"])
    if regime == "deductible":
        deductible = r2(o["tva"] * deduction / Decimal("100"))
        ligne(COMPTE_TVA_DEDUCTIBLE, _("TVA déductible %(taux)s %%") % {"taux": o["taux"]}, debit=deductible)
        ligne(compte_charge, _("TVA non déductible"), debit=o["tva"] - deductible)
    elif regime == "remboursement_ue":
        ligne(COMPTE_TVA_ETRANGERE, _("TVA %(pays)s %(taux)s %% à récupérer")
              % {"pays": o["pays"], "taux": o["taux"]}, debit=o["tva"])
    else:
        ligne(compte_charge, _("TVA %(pays)s non récupérable") % {"pays": o["pays"]}, debit=o["tva"])
    ligne(COMPTE_CONTREPARTIE, libelle, credit=o["ttc"])
    return L


def comptabilite(ops, deduction=Decimal("100")):
    balance = OrderedDict((c, {"compte": c, "intitule": _(i), "debit": ZERO, "credit": ZERO})
                          for c, i in COMPTES.items())
    journal = []
    for o in ops:
        lignes = ecritures(o, deduction)
        journal.append({"op": o, "lignes": lignes})
        for l in lignes:
            balance[l["compte"]]["debit"] += l["debit"]
            balance[l["compte"]]["credit"] += l["credit"]
    balance = [b for b in balance.values() if b["debit"] or b["credit"]]
    for b in balance:
        b["solde"] = b["debit"] - b["credit"]
    return {
        "balance": balance,
        "journal": journal,
        "total_debit": sum((b["debit"] for b in balance), ZERO),
        "total_credit": sum((b["credit"] for b in balance), ZERO),
    }
