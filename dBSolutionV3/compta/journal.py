"""
Journal général (débit / crédit) – consolidation des écritures PCMN de l'application :
ventes, encaissements, achats, salaires (et leur paiement), versements ONSS / précompte,
instructeurs indépendants, immobilisations (acquisitions, amortissements, cessions),
variations de stock et mouvements de trésorerie encodés à la main.
"""
import calendar
from collections import OrderedDict
from datetime import date
from decimal import Decimal

from django.utils.translation import gettext as _, gettext_lazy

ZERO = Decimal("0.00")

SOURCES = OrderedDict([
    ("vente", gettext_lazy("Ventes")),
    ("encaissement", gettext_lazy("Encaissements")),
    ("achat", gettext_lazy("Achats")),
    ("salaire", gettext_lazy("Salaires")),
    ("paiement_salaire", gettext_lazy("Paiement des salaires")),
    ("versement_social", gettext_lazy("Versements ONSS / précompte")),
    ("instructeur", gettext_lazy("Instructeurs indépendants")),
    ("immobilisation", gettext_lazy("Immobilisations et amortissements")),
    ("stock", gettext_lazy("Stock")),
    ("tresorerie", gettext_lazy("Trésorerie (mouvements manuels)")),
])


def _dans(jour, debut, fin):
    return jour is not None and (debut is None or jour >= debut) and (fin is None or jour <= fin)


def _norm(l, source, piece="", journal=None, jour=None):
    return {
        "date": jour or l.get("date"), "journal": journal or l.get("journal", "OD"), "piece": piece or l.get("piece", ""),
        "compte": l["compte"], "intitule": str(l.get("intitule") or ""), "libelle": str(l.get("libelle") or ""),
        "debit": Decimal(l.get("debit") or 0), "credit": Decimal(l.get("credit") or 0), "source": source,
    }


def ecritures_societe(societe, debut=None, fin=None, sources=None):
    sources = set(sources or SOURCES.keys())
    E = []

    # ---- Ventes et encaissements
    try:
        from facture.models import Facture, PaiementFacture
        from facture.paiements import ecritures_paiement
        if "vente" in sources:
            qs = Facture.objects.filter(societe=societe, statut=Facture.Statut.EMISE, client_est_societe=False)
            if debut:
                qs = qs.filter(issue_date__gte=debut)
            if fin:
                qs = qs.filter(issue_date__lte=fin)
            for f in qs:
                lib = f"{f.numero} – {f.nom_client_courant()}"
                base = {"libelle": lib, "date": f.issue_date}
                E.append(_norm(dict(base, compte="400000", intitule=_("Clients"), debit=f.total), "vente", f.numero, "VEN"))
                E.append(_norm(dict(base, compte="700000", intitule=_("Chiffre d'affaires – ventes"), credit=f.total_ht), "vente", f.numero, "VEN"))
                if f.total_tva:
                    E.append(_norm(dict(base, compte="451000", intitule=_("TVA à payer"), credit=f.total_tva), "vente", f.numero, "VEN"))
        if "encaissement" in sources:
            qs = PaiementFacture.objects.filter(facture__societe=societe).select_related("facture")
            if debut:
                qs = qs.filter(date__gte=debut)
            if fin:
                qs = qs.filter(date__lte=fin)
            for p in qs:
                journal = "CAI" if p.est_especes else "BQ"
                for l in ecritures_paiement(p):
                    E.append(_norm(l, "encaissement", p.facture.numero or "", journal, p.date))
    except Exception:
        pass

    # ---- Achats (marchandises, outillage)
    if "achat" in sources:
        for chemin, nom in (("achat_mds.models", "AchatMds"), ("outillage.models", "Outillage")):
            try:
                from importlib import import_module
                modele = getattr(import_module(chemin), nom)
                for a in modele.objects.filter(societe=societe).select_related("fournisseur"):
                    for l in a.ecritures_comptables():
                        if _dans(l["date"], debut, fin):
                            E.append(_norm(l, "achat", a.reference_facture or ""))
            except Exception:
                pass

    # ---- Salaires et paiement des salaires
    if sources & {"salaire", "paiement_salaire"}:
        try:
            from utilisateurs.models import PaieUtilisateur
            for paie in PaieUtilisateur.objects.filter(utilisateur__societe=societe).select_related("utilisateur"):
                fin_mois = date(paie.annee, paie.mois, calendar.monthrange(paie.annee, paie.mois)[1])
                piece = f"PAIE-{paie.annee}{paie.mois:02d}-{paie.pk}"
                nom = f"{paie.utilisateur.prenom} {paie.utilisateur.nom}"
                for l in paie.ecritures_comptables(avec_paiement=True):
                    paiement = l.get("type") == "paiement"
                    source = "paiement_salaire" if paiement else "salaire"
                    jour = paie.date_paiement if paiement else fin_mois
                    if source in sources and _dans(jour, debut, fin):
                        l = dict(l, libelle=f"{l['libelle']} – {nom} {paie.mois:02d}/{paie.annee}")
                        E.append(_norm(l, source, piece, "BQ" if paiement else "OD", jour))
        except Exception:
            pass

    # ---- Objets de la comptabilité
    from .models import FactureInstructeur, Immobilisation, MouvementTresorerie, ValorisationStock, VersementSocial
    if "versement_social" in sources:
        for v in VersementSocial.objects.filter(societe=societe):
            for l in v.ecritures():
                if _dans(l["date"], debut, fin):
                    E.append(_norm(l, "versement_social", v.reference))
    if "instructeur" in sources:
        for f in FactureInstructeur.objects.filter(societe=societe).exclude(statut=FactureInstructeur.Statut.BROUILLON).select_related("instructeur", "compte_paiement"):
            for l in f.ecritures():
                if _dans(l["date"], debut, fin):
                    E.append(_norm(l, "instructeur", f.piece))
    if "immobilisation" in sources:
        for i in Immobilisation.objects.filter(societe=societe).select_related("compte_paiement"):
            for l in i.ecritures(debut, fin):
                E.append(_norm(l, "immobilisation", i.reference_facture))
    if "stock" in sources:
        for v in ValorisationStock.objects.filter(societe=societe):
            for l in v.ecritures():
                if _dans(l["date"], debut, fin):
                    E.append(_norm(l, "stock", f"INV-{v.date:%Y%m%d}"))
    if "tresorerie" in sources:
        qs = MouvementTresorerie.objects.filter(compte__societe=societe).select_related("compte")
        if debut:
            qs = qs.filter(date__gte=debut)
        if fin:
            qs = qs.filter(date__lte=fin)
        for m in qs:
            entree = m.sens == m.Sens.ENTREE
            journal = m.compte.journal_code
            base = {"libelle": m.libelle, "date": m.date}
            E.append(_norm(dict(base, compte=m.compte.compte_pcmn, intitule=m.compte.nom,
                                debit=m.montant if entree else ZERO, credit=ZERO if entree else m.montant),
                           "tresorerie", m.piece, journal))
            E.append(_norm(dict(base, compte=m.compte_contrepartie, intitule=m.intitule_contrepartie,
                                debit=ZERO if entree else m.montant, credit=m.montant if entree else ZERO),
                           "tresorerie", m.piece, journal))

    E.sort(key=lambda e: (e["date"], e["journal"], e["piece"], -e["debit"]))
    return E


def balance(ecritures):
    comptes = {}
    for e in ecritures:
        c = comptes.setdefault(e["compte"], {"compte": e["compte"], "intitule": e["intitule"], "debit": ZERO, "credit": ZERO})
        if not c["intitule"] and e["intitule"]:
            c["intitule"] = e["intitule"]
        c["debit"] += e["debit"]
        c["credit"] += e["credit"]
    lignes = sorted(comptes.values(), key=lambda c: c["compte"])
    for c in lignes:
        c["solde"] = c["debit"] - c["credit"]
        c["classe"] = c["compte"][:1]
    return lignes
