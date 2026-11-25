"""Facel Vega (Paris, 1954-1964) : modèles, motorisations et moteurs liés.
FV, HK500, Excellence, Facel II (V8 Chrysler), Facellia (Pont-à-Mousson), Facel III (Volvo) et Facel 6 (BMC).
Moteurs fournis au motoriste « Facel Vega » (codes propres). Puissances SAE brutes ; toutes les données sont indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C = "CHAINE"


def v8(l, rpm, nmrpm):
    return f("ATM", E_, l, C, 8, rpm, nmrpm, "CHOISIR", 5.7, 3000, a="V")


FAMILLES = {
    "CHRYSLER-HEMI-4.5": v8(4.5, 4400, 2400), "CHRYSLER-HEMI-4.8": v8(4.8, 4600, 2800), "CHRYSLER-HEMI-5.4": v8(5.4, 4800, 3000),
    "CHRYSLER-5.8": v8(5.8, 5000, 3200), "CHRYSLER-5.9": v8(5.9, 5200, 3600), "CHRYSLER-6.3": v8(6.3, 5200, 3600),
    "PAM-1.6": f("ATM", E_, 1.6, C, 4, 6400, 4500, "CHOISIR", 5.0, 3000),
    "VOLVO-B18-1.8": f("ATM", E_, 1.8, C, 4, 6000, 4000, "CHOISIR", 3.75, 5000),
    "BMC-C-2.8": f("ATM", E_, 2.8, C, 6, 5250, 3000, "CHOISIR", 6.5, 5000),
}

mg = SaisieMoteurs(FAMILLES, "Facel Vega")
L = []
R = "Données indicatives (marque ancienne), à vérifier"

mg(L, "FV", "FV", "1", "1954-07", "1958-12", [("FV 4.5 V8 182", "CHRYSLER-HEMI-4.5", 340, {"fin": "1955-12"}), ("FV2 4.8 V8 203", "CHRYSLER-HEMI-4.8", 380, {"debut": "1955-01", "fin": "1956-12"}),
                                              ("FV3/FV4 5.4 V8 253", "CHRYSLER-HEMI-5.4", 440, {"debut": "1956-01"})], portes=2, places=4, reservoir=100,
   remarques=R + " ; coupé et cabriolet, V8 Chrysler / DeSoto")
mg(L, "HK500", "HK500", "1", "1958-01", "1961-12", [("HK500 5.9 V8 330", "CHRYSLER-5.9", 540), ("HK500 6.3 V8 365", "CHRYSLER-6.3", 590, {"debut": "1959-01"})],
   portes=2, places=4, reservoir=100, remarques=R + " ; coupé 2+2")
mg(L, "Excellence", "EX", "1", "1958-01", "1964-12", [("Excellence 5.8 V8 330", "CHRYSLER-5.8", 520, {"fin": "1958-12"}), ("Excellence 6.3 V8 360", "CHRYSLER-6.3", 590, {"debut": "1959-01"})],
   portes=4, places=5, reservoir=100, remarques=R + " ; berline 4 portes sans montant central")
mg(L, "Facel II", "HK2", "1", "1962-01", "1964-12", [("Facel II 6.3 V8 355", "CHRYSLER-6.3", 590), ("Facel II 6.3 V8 390", "CHRYSLER-6.3", 610)], portes=2, places=4, reservoir=100,
   remarques=R + " ; coupé 2+2 (boîte manuelle 390 ch)")
mg(L, "Facellia", "F2", "1", "1959-10", "1963-12", [("Facellia 1.6 115", "PAM-1.6", 140)], portes=2, places=2, reservoir=58,
   remarques=R + " ; coupé et cabriolet, double arbre Pont-à-Mousson (fiabilité médiocre)")
mg(L, "Facel III", "F3", "1", "1963-01", "1964-12", [("Facel III 1.8 108", "VOLVO-B18-1.8", 150)], portes=2, places=2, reservoir=58, remarques=R + " ; Facellia à moteur Volvo B18")
mg(L, "Facel 6", "F6", "1", "1964-01", "1964-12", [("Facel 6 2.8 I6 150", "BMC-C-2.8", 220)], portes=2, places=2, reservoir=58,
   remarques=R + " ; six cylindres BMC (Austin-Healey), environ 40 ex.")

MOT = Motorisations("Facel Vega", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Facel Vega": L}
MOTEURS = MOT.moteurs()
