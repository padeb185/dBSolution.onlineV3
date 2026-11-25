"""Dallara (Varano de' Melegari) : voiture de route Stradale et principaux châssis de course, motorisations et moteurs liés.
Stradale / EXP, IndyCar (DW12 et kit IR-18), GP2, F2, F3, Super Formula, P217 (LMP2).
Moteurs de fournisseurs (Ford, Mecachrome, Chevrolet, Honda, Toyota, Gibson) au motoriste « Dallara » (codes propres).
Châssis de course non homologués route ; puissances de course et données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C = "CHAINE"


def course(t, l, n, rpm, nmrpm, a="V"):
    return f(t, E_, l, C, n, rpm, nmrpm, "CHOISIR", 8.0, 1000, a=a)


FAMILLES = {
    "FORD-ECOBOOST-2.3": f("TURBO", E_, 2.3, C, 4, 6200, 3000, "5W30", 5.7, 15000),
    "INDY-2.2-V6TT": course("TURBO", 2.2, 6, 12000, 9000),
    "INDY-2.2-V6TT-HYB": course("HYB_TE", 2.2, 6, 12000, 9000),
    "MECA-4.0-V8": course("ATM", 4.0, 8, 10000, 8000),
    "MECA-3.4-V6T": course("TURBO", 3.4, 6, 8750, 6000),
    "MECA-3.4-V6": course("ATM", 3.4, 6, 8000, 6000),
    "SF-2.0-T": course("TURBO", 2.0, 4, 10000, 7000, a="EN_LIGNE"),
    "GIBSON-4.2-V8": course("ATM", 4.2, 8, 9000, 7000),
}

mg = SaisieMoteurs(FAMILLES, "Dallara")
L = []
R = "Châssis de course (non homologué route) ; données indicatives"

mg(L, "Stradale", "Stradale", "1", "2017-11", None,
   [("Stradale 2.3 Turbo 400", "FORD-ECOBOOST-2.3", 500), ("EXP 2.3 Turbo 500", "FORD-ECOBOOST-2.3", 540, {"debut": "2022-06"})], portes=2, places=2, reservoir=90,
   remarques="Voiture de route (roadster, targa, coupé) ; EXP réservée à la piste ; données indicatives")
mg(L, "DW12", "DW12", "1", "2012-01", "2017-12", [("DW12 2.2 V6 Biturbo 700", "INDY-2.2-V6TT", 500)], portes=0, places=1, reservoir=70,
   remarques=R + " ; IndyCar (Chevrolet / Honda), kits aéro 2015-2017")
mg(L, "DW12", "DW12", "IR18", "2018-01", "2023-12", [("IR-18 2.2 V6 Biturbo 700", "INDY-2.2-V6TT", 500)], portes=0, places=1, reservoir=70, remarques=R + " ; kit universel IR-18, aeroscreen (2020)")
mg(L, "DW12", "DW12", "HYB", "2024-07", None, [("IR-18 Hybrid 2.2 V6 Biturbo 800", "INDY-2.2-V6TT-HYB", 520)], portes=0, places=1, reservoir=70,
   remarques=R + " ; IndyCar hybride (supercondensateur, puissance cumulée)")
mg(L, "GP2", "GP2", "1", "2005-01", "2017-12", [("GP2 4.0 V8 612", "MECA-4.0-V8", 500)], portes=0, places=1, reservoir=125, remarques=R + " ; GP2/05, GP2/08, GP2/11")
mg(L, "F2", "F2 2018", "1", "2018-01", "2023-12", [("F2 2018 3.4 V6 Turbo 620", "MECA-3.4-V6T", 550)], portes=0, places=1, reservoir=125, remarques=R + " ; Formule 2 FIA")
mg(L, "F2", "F2 2024", "1", "2024-01", None, [("F2 2024 3.4 V6 Turbo 620", "MECA-3.4-V6T", 550)], portes=0, places=1, reservoir=125, remarques=R + " ; Formule 2 FIA")
mg(L, "F3", "F3 2019", "1", "2019-01", "2024-12", [("F3 2019 3.4 V6 380", "MECA-3.4-V6", 420)], portes=0, places=1, reservoir=100, remarques=R + " ; Formule 3 FIA")
mg(L, "F3", "F3 2025", "1", "2025-01", None, [("F3 2025 3.4 V6 380", "MECA-3.4-V6", 420)], portes=0, places=1, reservoir=100, remarques=R + " ; Formule 3 FIA")
mg(L, "Super Formula", "SF19", "1", "2019-01", "2022-12", [("SF19 2.0 Turbo 550", "SF-2.0-T", 500)], portes=0, places=1, reservoir=95, remarques=R + " ; Super Formula (Honda / Toyota)")
mg(L, "Super Formula", "SF23", "1", "2023-01", None, [("SF23 2.0 Turbo 550", "SF-2.0-T", 500)], portes=0, places=1, reservoir=95, remarques=R + " ; Super Formula (Honda / Toyota)")
mg(L, "P217", "P217", "1", "2017-01", None, [("P217 4.2 V8 600", "GIBSON-4.2-V8", 520)], portes=2, places=1, reservoir=75, remarques=R + " ; prototype LMP2 (Gibson)")

MOT = Motorisations("Dallara", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Dallara": L}
MOTEURS = MOT.moteurs()
