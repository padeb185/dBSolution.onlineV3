"""
Calcul de la TVA d'une période : TVA à payer (factures émises) et TVA à récupérer
(achats, outillage, carburant, AdBlue, électricité), avec le solde et les grilles indicatives
de la déclaration TVA belge.
"""
from calendar import monthrange
from datetime import date
from decimal import Decimal

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from maintenance.choices import TVAConfig

from .models import Facture, arrondi

ZERO = Decimal("0.00")


class CalculTVA:
    """
    Usage :
        calcul = CalculTVA.pour_periode(societe, "trimestre", 2026, 4)
        calcul.tva_a_payer      -> dict (par taux)
        calcul.tva_a_recuperer  -> dict (par source)
        calcul.solde            -> Decimal (> 0 : à payer à l'État, < 0 : crédit d'impôt)
    """

    # Sources de TVA déductible. « deductible » = pourcentage de TVA récupérable par défaut
    # (ex. carburant d'une voiture de société : souvent 50 % en Belgique — à adapter).
    SOURCES = {
        "achats": {"label": _("Achats (factures fournisseurs)"), "deductible": 100},
        "transport_achats": {"label": _("Frais de transport sur achats"), "deductible": 100},
        "outillage": {"label": _("Outillage"), "deductible": 100},
        "carburant": {"label": _("Carburant"), "deductible": 100},
        "adblue": {"label": _("AdBlue"), "deductible": 100},
        "electricite": {"label": _("Recharges électriques"), "deductible": 100},
        # Maintenances externes (garages officiels, B2B) dans le pays de la société :
        # TVA déductible via la déclaration périodique.
        "maintenances_externes": {"label": _("Maintenances externes (garages officiels, B2B)"), "deductible": 100},
        # TVA étrangère : non déductible dans la déclaration nationale, à récupérer via la
        # procédure de remboursement UE (directive 2008/9/CE) — affichée pour information.
        "maintenances_externes_etranger": {
            "label": _("Maintenances externes à l'étranger – remboursement UE (hors déclaration)"),
            "deductible": 100,
            "informatif": True,
        },
        # Factures adressées à notre propre société : TVA payée sur les pièces (prix d'achat × taux).
        # Ces pièces sont achetées via les achats fournisseurs (achat_mds), déjà comptés ci-dessus :
        # ligne affichée pour information, jamais ajoutée au total (pas de double comptage).
        "maintenances_internes": {
            "label": _("Maintenances internes (pièces) – incluses dans les achats"),
            "deductible": 100,
            "informatif": True,
        },
    }

    TYPES_PERIODE = ("mois", "trimestre", "annee")

    def __init__(self, societe, debut, fin, deductibilite=None):
        self.societe = societe
        self.debut = debut
        self.fin = fin
        self.deductibilite = {cle: Decimal(str(src["deductible"])) for cle, src in self.SOURCES.items()}
        for cle, valeur in (deductibilite or {}).items():
            if cle in self.deductibilite and valeur is not None:
                self.deductibilite[cle] = max(ZERO, min(Decimal("100"), Decimal(str(valeur))))
        self._a_payer = None
        self._a_recuperer = None

    # ------------------------------------------------------------
    # Périodes
    # ------------------------------------------------------------
    @staticmethod
    def bornes(type_periode, annee, numero=1):
        if type_periode == "mois":
            numero = min(max(int(numero), 1), 12)
            return date(annee, numero, 1), date(annee, numero, monthrange(annee, numero)[1])
        if type_periode == "trimestre":
            numero = min(max(int(numero), 1), 4)
            mois_debut = (numero - 1) * 3 + 1
            mois_fin = mois_debut + 2
            return date(annee, mois_debut, 1), date(annee, mois_fin, monthrange(annee, mois_fin)[1])
        return date(annee, 1, 1), date(annee, 12, 31)

    @classmethod
    def pour_periode(cls, societe, type_periode, annee, numero=1, deductibilite=None):
        debut, fin = cls.bornes(type_periode, annee, numero)
        return cls(societe, debut, fin, deductibilite)

    def _filtre_societe(self):
        # Données du tenant ; on accepte aussi les anciennes lignes sans société
        return Q(societe=self.societe) | Q(societe__isnull=True)

    # ------------------------------------------------------------
    # TVA à payer (ventes)
    # ------------------------------------------------------------
    def factures_periode(self):
        return (
            Facture.objects.filter(
                self._filtre_societe(),
                statut=Facture.Statut.EMISE,
                issue_date__range=(self.debut, self.fin),
            )
            .prefetch_related("lines")
            .order_by("issue_date", "numero")
        )

    def locations_periode(self):
        """Locations dont un acompte ou la prestation (fin de location) tombe dans la période."""
        from voiture.voiture_location.models import Location
        periode = (self.debut, self.fin)
        return (
            Location.objects.filter(societe=self.societe)
            .filter(
                Q(date_acompte__range=periode)
                | Q(date_fin__range=periode)
                | Q(date_fin__isnull=True, date_debut__range=periode)
            )
            .select_related("societe__adresse", "voiture_exemplaire")
            .prefetch_related("factures")
            .order_by("date_debut")
        )

    @property
    def tva_a_payer(self):
        if self._a_payer is not None:
            return self._a_payer

        from .models import FactureLine
        par_taux = {}
        base_autoliquidation = ZERO
        internes = []
        nb_factures = 0

        def ajouter(taux, base, tva):
            ligne = par_taux.setdefault(taux, {"taux": taux, "base": ZERO, "tva": ZERO})
            ligne["base"] += base
            ligne["tva"] += tva

        # 1) Factures émises de la période (hors lignes de location, comptées en 2)
        for facture in self.factures_periode():
            # Facture à notre propre société : pas une vente, hors déclaration
            if facture.client_est_societe:
                internes.append(facture)
                continue
            nb_factures += 1
            groupes = {}
            for ligne in facture.lines.all():
                if ligne.type_ligne == FactureLine.TypeLigne.LOCATION:
                    continue
                taux = ZERO if facture.autoliquidation else arrondi(ligne.vat_rate)
                groupes[taux] = groupes.get(taux, ZERO) + ligne.total_ht
            for taux, base in groupes.items():
                base = arrondi(base)
                if facture.autoliquidation:
                    base_autoliquidation += base
                    continue
                ajouter(taux, base, arrondi(base * taux / Decimal("100")))

        # 2) Locations (circuit / route), facturées ou non — exigibilité de la TVA
        #    (art. 22 Code TVA belge, art. 65 directive 2006/112/CE) :
        #    - acompte reçu avant la prestation : TVA due à la réception, sur le montant reçu ;
        #    - solde : TVA due à la fin de la prestation (fin de la location).
        #    Les lignes « Location » des factures ne sont pas recomptées en 1).
        vide = lambda: {"nb": 0, "base": ZERO, "tva": ZERO, "tvac": ZERO}
        locations = {"acomptes": vide(), "prestations": vide(), "liste": []}
        for location in self.locations_periode():
            emises = [f for f in location.factures.all() if f.statut == Facture.Statut.EMISE]
            facture = emises[0] if emises else None
            if facture is not None and facture.client_est_societe:
                continue
            for ev in location.evenements_tva():
                if not (self.debut <= ev["date"] <= self.fin):
                    continue
                groupe = locations["acomptes" if ev["nature"] == "acompte" else "prestations"]
                groupe["nb"] += 1
                groupe["tvac"] += ev["tvac"]
                if facture is not None and facture.autoliquidation:
                    base_autoliquidation += ev["tvac"]
                    groupe["base"] += ev["tvac"]
                    tva = ZERO
                else:
                    ajouter(arrondi(location.taux_tva), ev["base"], ev["tva"])
                    groupe["base"] += ev["base"]
                    groupe["tva"] += ev["tva"]
                    tva = ev["tva"]
                locations["liste"].append({
                    "location": location, "facture": facture, "nature": ev["nature"],
                    "date": ev["date"], "tvac": ev["tvac"], "tva": tva,
                })

        lignes = [
            {**l, "base": arrondi(l["base"]), "tva": arrondi(l["tva"])}
            for _t, l in sorted(par_taux.items())
        ]
        self._a_payer = {
            "lignes": lignes,
            "base": arrondi(sum((l["base"] for l in lignes), ZERO)),
            "tva": arrondi(sum((l["tva"] for l in lignes), ZERO)),
            "base_autoliquidation": arrondi(base_autoliquidation),
            # Locations (circuit / route) incluses dans la TVA à payer
            "locations": {
                "acomptes": {k: (arrondi(v) if k != "nb" else v) for k, v in locations["acomptes"].items()},
                "prestations": {k: (arrondi(v) if k != "nb" else v) for k, v in locations["prestations"].items()},
                "liste": sorted(locations["liste"], key=lambda l: l["date"]),
                "tva": arrondi(locations["acomptes"]["tva"] + locations["prestations"]["tva"]),
                "base": arrondi(locations["acomptes"]["base"] + locations["prestations"]["base"]),
                "nb": len({l["location"].pk for l in locations["liste"]}),
            },
            "nb_factures": nb_factures,
            "factures_internes": internes,
        }
        return self._a_payer

    # ------------------------------------------------------------
    # TVA à récupérer (achats)
    # ------------------------------------------------------------
    def _achats(self):
        from achat_mds.models import AchatMds
        base = tva = ZERO
        n = 0
        for achat in AchatMds.objects.filter(self._filtre_societe(), date_facture__range=(self.debut, self.fin)):
            # Marchandises / pièces (le transport est une source à part, avec sa propre déductibilité)
            base += achat.achat_montant_htva or ZERO
            tva += achat.montant_tva_achat or ZERO
            n += 1
        return base, tva, n

    def _transport_achats(self):
        from achat_mds.models import AchatMds
        base = tva = ZERO
        n = 0
        for achat in AchatMds.objects.filter(self._filtre_societe(), date_facture__range=(self.debut, self.fin),
                                             transport_montant_htva__gt=0):
            base += achat.transport_montant_htva or ZERO
            tva += achat.montant_tva_transport or ZERO
            n += 1
        from outillage.models import Outillage
        for outil in Outillage.objects.filter(self._filtre_societe(), date_facture__range=(self.debut, self.fin),
                                              transport_montant_htva__gt=0):
            base += outil.transport_montant_htva or ZERO
            tva += outil.montant_tva_transport or ZERO
            n += 1
        return base, tva, n

    def _outillage(self):
        from outillage.models import Outillage
        base = tva = ZERO
        n = 0
        for outil in Outillage.objects.filter(self._filtre_societe(), date_facture__range=(self.debut, self.fin)):
            # Outillage hors transport (le transport est dans « Frais de transport sur achats »)
            base += outil.achat_montant_htva
            tva += outil.montant_tva_achat
            n += 1
        return base, tva, n

    def _carburant(self):
        from fuel.models import Fuel
        base = tva = ZERO
        n = 0
        for plein in Fuel.objects.filter(
            self._filtre_societe(), validation=True, date__date__range=(self.debut, self.fin)
        ):
            base += plein.montant_ht or ZERO
            tva += plein.montant_tva or ZERO
            n += 1
        return base, tva, n

    def _adblue(self):
        from adblue.models import AdBlue
        base = tva = ZERO
        n = 0
        for plein in AdBlue.objects.filter(
            self._filtre_societe(), validation=True, date__date__range=(self.debut, self.fin)
        ):
            base += plein.montant_ht or ZERO
            tva += plein.montant_tva or ZERO
            n += 1
        return base, tva, n

    def _electricite(self):
        from recharge.models import Electricite
        base = tva = ZERO
        n = 0
        for recharge in Electricite.objects.filter(
            self._filtre_societe(), validation=True, date__range=(self.debut, self.fin)
        ):
            base += recharge.montant_ht or ZERO
            tva += recharge.montant_tva or ZERO
            n += 1
        return base, tva, n

    def _maintenances_externes_qs(self):
        from maintenance.maintenance_externe.models import MaintenanceExterne
        return MaintenanceExterne.objects.filter(
            self._filtre_societe(), date_facture__range=(self.debut, self.fin)
        )

    def _somme_maintenances_externes(self, qs):
        base = tva = ZERO
        n = 0
        for m in qs:
            base += m.total_htva or ZERO
            tva += m.total_tva or ZERO
            n += 1
        return base, tva, n

    def _maintenances_externes(self):
        return self._somme_maintenances_externes(
            self._maintenances_externes_qs().filter(pays=self.pays_par_defaut())
        )

    def _maintenances_externes_etranger(self):
        return self._somme_maintenances_externes(
            self._maintenances_externes_qs().exclude(pays=self.pays_par_defaut())
        )

    def _maintenances_internes(self):
        from .models import FactureLine
        base = tva = ZERO
        n = 0
        for facture in self.factures_periode().filter(client_est_societe=True):
            n += 1
            for ligne in facture.lines.all():
                if ligne.type_ligne != FactureLine.TypeLigne.PIECE or ligne.unit_cost is None:
                    continue
                montant = arrondi(Decimal(ligne.unit_cost) * Decimal(ligne.quantity or 0))
                base += montant
                tva += arrondi(montant * Decimal(ligne.vat_rate or 0) / Decimal("100"))
        return base, tva, n

    @property
    def tva_a_recuperer(self):
        if self._a_recuperer is not None:
            return self._a_recuperer

        calculs = {
            "achats": self._achats,
            "transport_achats": self._transport_achats,
            "outillage": self._outillage,
            "carburant": self._carburant,
            "adblue": self._adblue,
            "electricite": self._electricite,
            "maintenances_externes": self._maintenances_externes,
            "maintenances_externes_etranger": self._maintenances_externes_etranger,
            "maintenances_internes": self._maintenances_internes,
        }
        lignes = []
        for cle, fonction in calculs.items():
            base, tva, n = fonction()
            pourcentage = self.deductibilite[cle]
            lignes.append({
                "cle": cle,
                "informatif": self.SOURCES[cle].get("informatif", False),
                "label": self.SOURCES[cle]["label"],
                "nb": n,
                "base": arrondi(base),
                "tva": arrondi(tva),
                "deductible": pourcentage,
                "tva_deductible": arrondi(tva * pourcentage / Decimal("100")),
            })

        comptees = [l for l in lignes if not l["informatif"]]
        self._a_recuperer = {
            "lignes": lignes,
            "base": arrondi(sum((l["base"] for l in comptees), ZERO)),
            "tva": arrondi(sum((l["tva"] for l in comptees), ZERO)),
            "tva_deductible": arrondi(sum((l["tva_deductible"] for l in comptees), ZERO)),
        }
        return self._a_recuperer

    # ------------------------------------------------------------
    # Solde
    # ------------------------------------------------------------
    @property
    def solde(self):
        """> 0 : TVA à payer à l'État ; < 0 : TVA à récupérer (crédit)."""
        return arrondi(self.tva_a_payer["tva"] - self.tva_a_recuperer["tva_deductible"])

    @property
    def a_payer(self):
        return self.solde > 0

    # ------------------------------------------------------------
    # Déclarations nationales (UE)
    # ------------------------------------------------------------
    def pays_par_defaut(self):
        adresse = getattr(self.societe, "adresse", None)
        code = (getattr(adresse, "code_pays", "") or "BE")[:2].upper()
        return code if code in TVAConfig.TVA_PIECES else "BE"

    def declaration(self, pays=None):
        """
        Déclaration TVA indicative pour un pays de l'UE :
        {"pays", "formulaire", "lignes": [{"grille", "libelle", "montant"}], "officiel": bool}
        """
        pays = (pays or self.pays_par_defaut()).upper()
        modele = FORMULAIRES_TVA.get(pays)
        bases = {l["taux"]: l["base"] for l in self.tva_a_payer["lignes"]}
        due = self.tva_a_payer["tva"]
        deductible = self.tva_a_recuperer["tva_deductible"]
        solde = self.solde
        intra = self.tva_a_payer["base_autoliquidation"]

        lignes = []
        total = (modele or {}).get("total")
        if total:
            lignes.append({"grille": total[0], "libelle": total[1],
                           "montant": arrondi(self.tva_a_payer["base"] + intra)})
        cases_taux = (modele or {}).get("taux", {})
        restant = dict(bases)
        for taux, (case, libelle) in cases_taux.items():
            montant = restant.pop(Decimal(str(taux)).quantize(Decimal("0.01")), ZERO)
            lignes.append({"grille": case, "libelle": libelle, "montant": montant})
        # Taux sans case dédiée dans ce formulaire (ex. facture à 21 % déclarée en France)
        if total and not cases_taux:
            restant = {}
        for taux, base in sorted(restant.items()):
            lignes.append({
                "grille": "—",
                "libelle": _("Base à %(taux)s %% (taux sans case dédiée – à vérifier)") % {"taux": f"{taux:g}"},
                "montant": base,
            })

        cases = (modele or {}).get("cases", {})

        def ajouter(cle, libelle_generique, montant):
            case = cases.get(cle)
            if modele and cle in cases and case is None:
                return  # rubrique absente de ce formulaire
            numero, libelle = case if case else ("—", libelle_generique)
            lignes.append({"grille": numero, "libelle": libelle, "montant": arrondi(montant)})

        ajouter("intra", _("Prestations intracommunautaires (autoliquidation)"), intra)
        ajouter("due", _("TVA due"), due)
        ajouter("deductible", _("TVA déductible"), deductible)
        case_payer, case_credit = cases.get("a_payer"), cases.get("credit")
        if case_payer and case_credit and case_payer[0] == case_credit[0]:
            # Même case pour le solde (ex. DE 83, NL 5g, ES 71) : montant signé, négatif = crédit
            libelle = case_payer[1] if solde >= 0 else case_credit[1]
            lignes.append({"grille": case_payer[0], "libelle": libelle, "montant": arrondi(solde)})
        else:
            ajouter("a_payer", _("TVA à payer"), solde if solde > 0 else ZERO)
            ajouter("credit", _("Crédit de TVA (à récupérer)"), -solde if solde < 0 else ZERO)

        return {
            "pays": pays,
            "pays_nom": dict(TVAConfig.PAYS_CHOICES).get(pays, pays),
            "formulaire": (modele or {}).get("formulaire", _("Déclaration périodique de TVA")),
            "lignes": lignes,
            "officiel": bool(modele),
        }

    def grilles_belges(self):
        """Compatibilité : déclaration belge."""
        return self.declaration("BE")["lignes"]


# Formulaires nationaux : numéros de cases/rubriques officiels (indicatifs, à faire valider).
# "taux" : {taux: (case de la base, libellé)} ; "cases" : intra / due / deductible / a_payer / credit
# (None = rubrique absente du formulaire). Les pays absents utilisent un modèle générique.
FORMULAIRES_TVA = {
    "BE": {
        "formulaire": _("Déclaration périodique à la TVA (Intervat)"),
        "taux": {
            0: ("00", _("Opérations soumises à un régime particulier / 0 %")),
            6: ("01", _("Opérations à 6 %")),
            12: ("02", _("Opérations à 12 %")),
            21: ("03", _("Opérations à 21 %")),
        },
        "cases": {
            "intra": ("44", _("Services intracommunautaires (autoliquidation)")),
            "due": ("54", _("TVA due sur les opérations")),
            "deductible": ("59", _("TVA déductible")),
            "a_payer": ("71", _("Taxe due à l'État")),
            "credit": ("72", _("Sommes dues par l'État")),
        },
    },
    "FR": {
        "formulaire": _("Déclaration CA3 (formulaire 3310-CA3)"),
        "taux": {
            20: ("08", _("Taux normal 20 % – base hors taxe")),
            10: ("9B", _("Taux réduit 10 % – base hors taxe")),
            5.5: ("09", _("Taux réduit 5,5 % – base hors taxe")),
            2.1: ("10", _("Taux particulier 2,1 % – base hors taxe")),
        },
        "cases": {
            "intra": ("E2", _("Autres opérations non imposables (prestations intracommunautaires)")),
            "due": ("16", _("Total de la TVA brute due")),
            "deductible": ("23", _("Total TVA déductible")),
            "a_payer": ("28", _("TVA nette due")),
            "credit": ("25", _("Crédit de TVA")),
        },
    },
    "DE": {
        "formulaire": _("Umsatzsteuer-Voranmeldung (UStVA)"),
        "taux": {
            19: ("81", _("Steuerpflichtige Umsätze 19 % – Bemessungsgrundlage")),
            7: ("86", _("Steuerpflichtige Umsätze 7 % – Bemessungsgrundlage")),
        },
        "cases": {
            "intra": ("21", _("Nicht steuerbare sonstige Leistungen (EU, Reverse Charge)")),
            "due": None,
            "deductible": ("66", _("Vorsteuerbeträge")),
            "a_payer": ("83", _("Verbleibende Umsatzsteuer-Vorauszahlung")),
            "credit": ("83", _("Verbleibender Überschuss (negativ)")),
        },
    },
    "NL": {
        "formulaire": _("Aangifte omzetbelasting"),
        "taux": {
            21: ("1a", _("Leveringen/diensten belast met hoog tarief (21 %)")),
            9: ("1b", _("Leveringen/diensten belast met laag tarief (9 %)")),
            0: ("1e", _("Leveringen/diensten belast met 0 % of niet bij u belast")),
        },
        "cases": {
            "intra": ("3b", _("Leveringen naar/diensten in landen binnen de EU")),
            "due": ("5a", _("Verschuldigde omzetbelasting")),
            "deductible": ("5b", _("Voorbelasting")),
            "a_payer": ("5g", _("Totaal te betalen")),
            "credit": ("5g", _("Totaal terug te vragen")),
        },
    },
    "ES": {
        "formulaire": _("Modelo 303 (IVA)"),
        "taux": {
            4: ("01", _("Régimen general 4 % – base imponible")),
            10: ("04", _("Régimen general 10 % – base imponible")),
            21: ("07", _("Régimen general 21 % – base imponible")),
        },
        "cases": {
            "intra": ("120", _("Operaciones no sujetas por reglas de localización")),
            "due": ("27", _("Total cuota devengada")),
            "deductible": ("45", _("Total a deducir")),
            "a_payer": ("71", _("Resultado de la liquidación (a ingresar)")),
            "credit": ("71", _("Resultado de la liquidación (a compensar / devolver)")),
        },
    },
    "IT": {
        "formulaire": _("Comunicazione liquidazioni periodiche IVA (LIPE)"),
        "total": ("VP2", _("Totale operazioni attive (al netto dell'IVA)")),
        "taux": {},
        "cases": {
            "intra": None,
            "due": ("VP4", _("IVA esigibile")),
            "deductible": ("VP5", _("IVA detratta")),
            "a_payer": ("VP6", _("IVA dovuta")),
            "credit": ("VP6", _("IVA a credito")),
        },
    },
    "AT": {
        "formulaire": _("Umsatzsteuervoranmeldung (U30)"),
        "total": ("000", _("Gesamtbetrag der Bemessungsgrundlagen")),
        "taux": {
            20: ("022", _("Normalsteuersatz 20 % – Bemessungsgrundlage")),
            10: ("029", _("Ermäßigter Steuersatz 10 % – Bemessungsgrundlage")),
            13: ("006", _("Ermäßigter Steuersatz 13 % – Bemessungsgrundlage")),
        },
        "cases": {
            "intra": None,
            "due": None,
            "deductible": ("060", _("Gesamtbetrag der Vorsteuern")),
            "a_payer": ("095", _("Vorauszahlung (Zahllast)")),
            "credit": ("095", _("Überschuss")),
        },
    },
}
