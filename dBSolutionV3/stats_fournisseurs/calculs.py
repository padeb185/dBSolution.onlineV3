"""
Statistiques fournisseurs : liste unifiée des achats de la société
(marchandises, outillage, factures d'achat réceptionnées en stock) et regroupements.
"""
from collections import OrderedDict
from decimal import Decimal

from django.utils.translation import gettext_lazy as _

ZERO = Decimal("0.00")
R2 = Decimal("0.01")

SOURCES = OrderedDict([
    ("mds", _("Marchandises")),
    ("outillage", _("Outillage")),
    ("stock", _("Stock pièces")),
])

NOMS_MOIS = [_("Janvier"), _("Février"), _("Mars"), _("Avril"), _("Mai"), _("Juin"), _("Juillet"),
             _("Août"), _("Septembre"), _("Octobre"), _("Novembre"), _("Décembre")]


def q(valeur):
    return Decimal(valeur or 0).quantize(R2)


def lignes_achats(societe, fournisseur=None, annee=None, mois=None, sources=None):
    """
    [{date, fournisseur_id, fournisseur, reference, libelle, htva, tva, tvac, source, url_nom, url_arg}]
    Notes de crédit en négatif. Triées par date.
    """
    sources = set(sources or SOURCES)
    lignes = []

    def filtrer(qs, champ_date="date_facture"):
        qs = qs.filter(societe=societe)
        if fournisseur is not None:
            qs = qs.filter(fournisseur=fournisseur)
        if annee:
            qs = qs.filter(**{f"{champ_date}__year": annee})
        if mois:
            qs = qs.filter(**{f"{champ_date}__month": mois})
        return qs.select_related("fournisseur")

    if "mds" in sources:
        from achat_mds.models import AchatMds
        for a in filtrer(AchatMds.objects.all()):
            sg = getattr(a, "signe", 1)
            htva = (a.montant_htva_total or ZERO) * sg
            tva = (a.montant_tva or ZERO) * sg
            lignes.append({
                "date": a.date_facture, "fournisseur_id": a.fournisseur_id, "fournisseur": a.fournisseur,
                "reference": a.reference_facture or "", "libelle": a.libelle_facture or "",
                "htva": htva, "tva": tva, "tvac": htva + tva, "source": "mds",
                "url_nom": "achat_mds:achat_detail", "url_arg": a.pk, "note_credit": sg < 0,
            })

    if "outillage" in sources:
        from outillage.models import Outillage
        for o in filtrer(Outillage.objects.all()):
            sg = getattr(o, "signe", 1)
            htva = (o.prix_htva or ZERO) * (o.quantite or 0) * sg
            tva = (o.tva_a_recuperer or ZERO) * sg
            lignes.append({
                "date": o.date_facture, "fournisseur_id": o.fournisseur_id, "fournisseur": o.fournisseur,
                "reference": o.reference or "", "libelle": o.libelle or "",
                "htva": htva, "tva": tva, "tvac": htva + tva, "source": "outillage",
                "url_nom": "outillage:outillage_detail", "url_arg": o.pk, "note_credit": sg < 0,
            })

    if "stock" in sources:
        try:
            from piece.models import FactureAchatStock
        except ImportError:
            FactureAchatStock = None
        if FactureAchatStock is not None:
            for f in filtrer(FactureAchatStock.objects.exclude(fournisseur__isnull=True)):
                lignes.append({
                    "date": f.date_facture, "fournisseur_id": f.fournisseur_id, "fournisseur": f.fournisseur,
                    "reference": f.numero_facture, "libelle": f.commentaire or "",
                    "htva": f.total_htva, "tva": f.total_tva, "tvac": f.total_tvac, "source": "stock",
                    "url_nom": "piece:facture_achat_detail", "url_arg": f.pk, "note_credit": False,
                })

    lignes = [l for l in lignes if l["date"]]
    for l in lignes:
        l["htva"], l["tva"], l["tvac"] = q(l["htva"]), q(l["tva"]), q(l["tvac"])
        l["source_libelle"] = SOURCES[l["source"]]
    lignes.sort(key=lambda l: (l["date"], l["reference"]))
    return lignes


def totaux(lignes):
    htva = sum((l["htva"] for l in lignes), ZERO)
    tva = sum((l["tva"] for l in lignes), ZERO)
    nb = len(lignes)
    return {"nb": nb, "htva": q(htva), "tva": q(tva), "tvac": q(htva + tva),
            "moyenne": q(htva / nb) if nb else ZERO}


def par_mois(lignes, annee):
    """12 mois de l'année (mois sans achat à zéro)."""
    res = []
    for m in range(1, 13):
        t = totaux([l for l in lignes if l["date"].year == annee and l["date"].month == m])
        res.append({"mois": m, "nom": NOMS_MOIS[m - 1], **t})
    return res


def par_annee(lignes):
    annees = sorted({l["date"].year for l in lignes})
    res = []
    precedent = None
    for a in annees:
        t = totaux([l for l in lignes if l["date"].year == a])
        t["annee"] = a
        t["evolution"] = (q((t["htva"] - precedent) * 100 / precedent) if precedent else None)
        precedent = t["htva"] or None
        res.append(t)
    return res


def par_source(lignes):
    return [{"source": s, "libelle": lib, **totaux([l for l in lignes if l["source"] == s])}
            for s, lib in SOURCES.items()]


def par_fournisseur(lignes):
    groupes = OrderedDict()
    for l in lignes:
        groupes.setdefault(l["fournisseur_id"], []).append(l)
    total = sum((l["htva"] for l in lignes), ZERO)
    res = []
    for fid, ls in groupes.items():
        t = totaux(ls)
        t.update({
            "fournisseur": ls[0]["fournisseur"], "fournisseur_id": fid,
            "derniere": max(l["date"] for l in ls),
            "part": q(t["htva"] * 100 / total) if total else ZERO,
        })
        res.append(t)
    res.sort(key=lambda r: r["htva"], reverse=True)
    return res
