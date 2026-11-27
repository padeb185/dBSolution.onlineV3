"""Geo : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Marque de General Motors (1989-1997) pour des modèles importés ou coproduits : Metro (Suzuki Swift), Prizm (Toyota Corolla, NUMMI),
Spectrum (Isuzu), Storm (Isuzu Impulse) et Tracker (Suzuki Vitara). Moteurs Suzuki, Toyota et Isuzu.
Puissances SAE converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
B = "COURROIE"
SUZUKI = {
    "SUZUKI-G10-1.0": f("ATM", E_, 1.0, B, 3, 5700, 3300, "10W30", 3.5, 7500),
    "SUZUKI-G13-1.3": f("ATM", E_, 1.3, B, 4, 6000, 3000, "10W30", 3.5, 7500),
    "SUZUKI-G16-1.6": f("ATM", E_, 1.6, B, 4, 5400, 3000, "10W30", 4.0, 7500),
}
TOYOTA = {
    "TOYOTA-4A-1.6": f("ATM", E_, 1.6, B, 4, 5800, 4800, "10W30", 3.5, 7500),
    "TOYOTA-7A-1.8": f("ATM", E_, 1.8, B, 4, 5200, 2800, "10W30", 3.7, 7500),
}
ISUZU = {
    "ISUZU-4XC1-1.5": f("ATM", E_, 1.5, B, 4, 5400, 3400, "10W30", 3.5, 7500),
    "ISUZU-4XE1-1.6": f("ATM", E_, 1.6, B, 4, 5800, 4800, "10W30", 3.5, 7500),
    "ISUZU-4XF1-1.8": f("ATM", E_, 1.8, B, 4, 6800, 4800, "10W30", 3.5, 7500),
}
FAMILLES = {**SUZUKI, **TOYOTA, **ISUZU}


def motoriste(fam):
    if fam in SUZUKI:
        return "Suzuki"
    if fam in TOYOTA:
        return "Toyota"
    return "Isuzu"


mg = SaisieMoteurs(FAMILLES, "Geo", motoriste)
L = []
NA = "marché nord-américain ; données indicatives"

mg(L, "Metro", "M", "1", "1989-01", "1997-12", [("1.0 56", "SUZUKI-G10-1.0", 80), ("1.3 71", "SUZUKI-G13-1.3", 101, {"debut": "1995-01"})], portes=3, places=4, reservoir=40,
   remarques="Suzuki Swift (Cultus) assemblée par CAMI (Canada) ; 3 et 5 portes, cabriolet ; " + NA)
mg(L, "Prizm", "E90 / E100", "1", "1990-01", "1997-12", [("1.6 103", "TOYOTA-4A-1.6", 135, {"fin": "1992-12"}), ("1.8 107", "TOYOTA-7A-1.8", 160, {"debut": "1993-01"})],
   portes=4, places=5, reservoir=50, remarques="Toyota Corolla assemblée par NUMMI ; " + NA)
mg(L, "Spectrum", "R", "1", "1989-01", "1989-12", [("1.5 71", "ISUZU-4XC1-1.5", 118)], portes=4, places=5, reservoir=42, remarques="Isuzu I-Mark ; " + NA)
mg(L, "Storm", "Storm", "1", "1990-01", "1993-12", [("1.6 96", "ISUZU-4XE1-1.6", 132), ("GSi 1.6 132", "ISUZU-4XE1-1.6", 138, {"fin": "1991-12"}),
                                                  ("GSi 1.8 142", "ISUZU-4XF1-1.8", 170, {"debut": "1992-01"})], portes=3, places=4, reservoir=47,
   remarques="Isuzu Impulse, coupé et hayon ; " + NA)
mg(L, "Tracker", "Tracker", "1", "1989-01", "1997-12", [("1.6 81", "SUZUKI-G16-1.6", 127), ("1.6 16V 96", "SUZUKI-G16-1.6", 132, {"debut": "1996-01"})],
   portes=3, places=4, reservoir=42, remarques="Suzuki Vitara (CAMI), 3 portes et cabriolet ; " + NA)

MOT = Motorisations("Geo", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Geo": L}
MOTEURS = MOT.moteurs()
