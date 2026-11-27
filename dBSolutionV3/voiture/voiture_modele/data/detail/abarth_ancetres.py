"""Abarth (ancêtres et modèles anciens) : générations, phases, motorisations (marché européen) et moteurs liés.
Abarth & C. (Turin, fondée par Carlo Abarth en 1949) : Cisitalia-Abarth 204 A, 207 A, 750 GT Zagato « Double Bulle »,
Fiat-Abarth 1000 Bialbero, Fiat-Abarth 2300 S, Simca-Abarth 1300 / 2000, OT 1000 / 1300 / 1600 et Scorpione (non repris dans abarth.py).
Familles Fiat 600 / 850 / 1000 reprises d'abarth.py (mêmes codes et couples) ; moteurs Abarth double arbre ajoutés.
Puissances en ch. Données indicatives (modèles anciens), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .abarth import FAMILLES as FAMILLES_ABARTH

E_ = "ESS"
C = "CHAINE"
FAMILLES = {
    "ABARTH-1100": f("ATM", E_, 1.1, C, 4, 6000, 4500, "20W50", 3.5, 5000),
    "ABARTH-750": f("ATM", E_, 0.75, C, 4, 6000, 4500, "20W50", 3.0, 5000),
    "ABARTH-BIALBERO-1.0": f("ATM", E_, 1.0, C, 4, 7600, 6000, "20W50", 3.5, 3000),
    "ABARTH-L6-2.3": f("ATM", E_, 2.3, C, 6, 5600, 4000, "20W50", 5.5, 5000),
    "ABARTH-DOHC-1.3": f("ATM", E_, 1.3, C, 4, 7000, 5800, "20W50", 4.0, 3000),
    "ABARTH-DOHC-1.6": f("ATM", E_, 1.6, C, 4, 7000, 5800, "20W50", 4.5, 3000),
    "ABARTH-DOHC-2.0": f("ATM", E_, 2.0, C, 4, 7200, 6000, "20W50", 5.0, 3000),
    "ABARTH-1.3": f("ATM", E_, 1.3, C, 4, 6200, 4000, "20W50", 4.0, 5000),
    "Fiat100-1.0": FAMILLES_ABARTH["Fiat100-1.0"],
}
mg = SaisieMoteurs(FAMILLES, "Abarth", lambda fam: "Abarth")
L = []
IND = "données indicatives (modèle ancien), à vérifier"

mg(L, "204 A", "204 A", "1", "1949-01", "1950-12", [("1.1 83", "ABARTH-1100", 100)], portes=0, places=2, reservoir=60,
   remarques="Cisitalia-Abarth 204 A, barquette sur mécanique Fiat 1100, première Abarth ; " + IND)
mg(L, "207 A", "207 A", "1", "1955-01", "1956-12", [("1.1 66", "ABARTH-1100", 90)], portes=0, places=2, reservoir=60, remarques="Spider Boano sur base Fiat 1100 ; " + IND)
mg(L, "750 GT Zagato", "750", "1", "1956-01", "1960-12", [("0.75 47", "ABARTH-750", 55), ("Record Monza 0.75 57", "ABARTH-750", 60, {"debut": "1958-01"})],
   portes=2, places=2, reservoir=30, remarques="Coupé Zagato « Double Bulle » sur base Fiat 600, Record Monza à double arbre ; " + IND)
mg(L, "1000 Bialbero", "1000 Bialbero", "1", "1960-01", "1963-12", [("1.0 91", "ABARTH-BIALBERO-1.0", 90), ("GT 1.0 104", "ABARTH-BIALBERO-1.0", 98, {"debut": "1962-01"})],
   portes=2, places=2, reservoir=40, remarques="Fiat-Abarth 1000 Bialbero, coupé Zagato à double arbre ; " + IND)
mg(L, "2300 S", "2300 S", "1", "1961-01", "1965-12", [("2.3 L6 150", "ABARTH-L6-2.3", 205)], portes=2, places=4, reservoir=60,
   remarques="Coupé Ghia sur base Fiat 2300, six cylindres préparé ; " + IND)
mg(L, "Simca-Abarth", "1300 / 2000", "1", "1962-01", "1965-12", [("1300 GT 1.3 125", "ABARTH-DOHC-1.3", 138), ("2000 GT 2.0 202", "ABARTH-DOHC-2.0", 206, {"debut": "1963-01"})],
   portes=2, places=2, reservoir=60, remarques="Coupés sur plate-forme Simca 1000, moteurs Abarth double arbre ; " + IND)
mg(L, "OT", "OT", "1", "1964-01", "1968-12", [("OT 1000 1.0 60", "Fiat100-1.0", 78), ("OT 1300 1.3 147", "ABARTH-DOHC-1.3", 145, {"debut": "1965-01"}),
                                            ("OT 1600 1.6 155", "ABARTH-DOHC-1.6", 160, {"debut": "1965-01"})], portes=2, places=2, reservoir=40,
   remarques="« Omologata Turismo » sur base Fiat 850 coupé ; OT 1300 / 1600 de compétition à double arbre ; " + IND)
mg(L, "Scorpione", "Scorpione", "1", "1968-01", "1971-12", [("1.3 75", "ABARTH-1.3", 100), ("SS 1.3 100", "ABARTH-1.3", 115)], portes=2, places=2, reservoir=40,
   remarques="Coupé sur base Lombardi Grand Prix (Francis Lombardi) ; " + IND)

MOT = Motorisations("Abarth", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Abarth": L}
MOTEURS = MOT.moteurs()
