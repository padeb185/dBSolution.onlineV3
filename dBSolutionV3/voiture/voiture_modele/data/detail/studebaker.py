"""Studebaker : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Electric, Big Six, Dictator, President, Commander, Land Cruiser, Champion, M-series, US6, Starliner, Golden Hawk, Lark,
Avanti et Wagonaire. Marque fermée en 1966.
V8 Packard 5.8 et V8 Studebaker 4.7 à compresseur repris de packard.py, V8 Chevrolet 4.6 de chevrolet.py (mêmes codes) ;
six et huit cylindres Studebaker, V8 Studebaker 3.8 à 4.7, Hercules JXD et six cylindres Chevrolet ajoutés.
Puissances brutes (SAE gross) converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET
from .packard import FAMILLES as FAMILLES_PACKARD

E_ = "ESS"
C, SV = "CHAINE", "NC"


def v8(l, rpm, nmrpm, t="ATM"):
    return f(t, E_, l, C, 8, rpm, nmrpm, "10W30", 4.7, 5000, a="V")


STUDE = {
    "STUDE-EV": electrique(),
    "STUDE-L6-5.8": f("ATM", E_, 5.8, SV, 6, 2000, 1000, "SAE30", 6.0, 2000),
    "STUDE-L6-3.6": f("ATM", E_, 3.6, SV, 6, 3200, 1400, "SAE30", 5.0, 3000),
    "STUDE-L6-3.7": f("ATM", E_, 3.7, SV, 6, 3600, 1600, "SAE30", 5.0, 3000),
    "STUDE-L6-2.7": f("ATM", E_, 2.7, SV, 6, 4000, 1600, "SAE30", 4.5, 3000),
    "STUDE-L6-2.8": f("ATM", E_, 2.8, SV, 6, 4000, 2000, "SAE30", 4.5, 3000),
    "STUDE-L6-3.0": f("ATM", E_, 3.0, SV, 6, 4000, 2000, "SAE30", 4.5, 3000),
    "STUDE-L8-4.1": f("ATM", E_, 4.1, SV, 8, 3600, 1600, "SAE30", 6.0, 3000),
    "STUDE-L8-5.5": f("ATM", E_, 5.5, SV, 8, 3200, 1400, "SAE30", 7.0, 3000),
    "STUDE-V8-3.8": v8(3.8, 4000, 2000), "STUDE-V8-4.3": v8(4.3, 4500, 2800), "STUDE-V8-4.7": v8(4.7, 4500, 2800),
    "STUDEBAKER-V8-4.7SC": FAMILLES_PACKARD["STUDEBAKER-V8-4.7SC"],
}
PACKARD = {"PACKARD-V8-5.8": FAMILLES_PACKARD["PACKARD-V8-5.8"]}
HERCULES = {"HERCULES-JXD-5.2": f("ATM", E_, 5.2, SV, 6, 2800, 1200, "SAE30", 7.0, 3000)}
CHEVROLET = {"SBC-4.6": FAMILLES_CHEVROLET["SBC-4.6"], "CHEVY-I6-3.8": f("ATM", E_, 3.8, C, 6, 4400, 1600, "10W30", 4.7, 5000)}
FAMILLES = {**STUDE, **PACKARD, **HERCULES, **CHEVROLET}


def motoriste(fam):
    if fam in PACKARD:
        return "Packard"
    if fam in HERCULES:
        return "Hercules"
    if fam in CHEVROLET:
        return "Chevrolet"
    return "Studebaker"


mg = SaisieMoteurs(FAMILLES, "Studebaker", motoriste)
L = []
NA = "Marché nord-américain"
IND = NA + " ; données indicatives"

mg(L, "Electric", "Electric", "1", "1902-01", "1912-12", [("Électrique 3", "STUDE-EV", 30, {"reservoir": 0, "batterie": 5})], portes=0, places=2, reservoir=0,
   remarques="Voiture électrique (runabout), premiers véhicules Studebaker ; " + IND)
mg(L, "Big Six", "Big Six", "1", "1918-01", "1927-12", [("5.8 L6 61", "STUDE-L6-5.8", 270)], portes=4, places=7, reservoir=75, remarques=IND)
mg(L, "Dictator", "Dictator", "1", "1927-01", "1937-12", [("3.6 L6 71", "STUDE-L6-3.6", 200), ("4.1 L8 86", "STUDE-L8-4.1", 230, {"debut": "1930-01", "fin": "1933-12"})],
   portes=4, places=5, reservoir=60, remarques=IND)
mg(L, "President", "President", "1", "1927-01", "1942-12", [("5.5 L8 116", "STUDE-L8-5.5", 340, {"fin": "1933-12"}), ("4.1 L8 112", "STUDE-L8-4.1", 270, {"debut": "1934-01"})],
   portes=4, places=5, reservoir=75, remarques="Dont President Land Cruiser ; " + IND)
mg(L, "Commander", "Commander", "1", "1927-01", "1958-12",
   [("3.6 L6 71", "STUDE-L6-3.6", 200, {"fin": "1936-12"}), ("3.7 L6 91", "STUDE-L6-3.7", 230, {"debut": "1937-01", "fin": "1950-12"}), ("3.8 V8 122", "STUDE-V8-3.8", 258, {"debut": "1951-01", "fin": "1954-12"}),
    ("4.3 V8 142", "STUDE-V8-4.3", 312, {"debut": "1955-01"})], portes=4, places=6, reservoir=68, remarques=IND)
mg(L, "Commander", "Lark", "2", "1964-01", "1964-12", [("4.3 V8 182", "STUDE-V8-4.3", 353)], portes=4, places=6, reservoir=68, remarques="Sur base Lark ; " + IND)
mg(L, "Land Cruiser", "Land Cruiser", "1", "1934-01", "1954-12", [("4.1 L8 112", "STUDE-L8-4.1", 270, {"fin": "1942-12"}), ("3.7 L6 95", "STUDE-L6-3.7", 230, {"debut": "1946-01", "fin": "1950-12"}),
                                                                    ("3.8 V8 122", "STUDE-V8-3.8", 258, {"debut": "1951-01"})], portes=4, places=6, reservoir=68, remarques=IND)
mg(L, "Champion", "Champion", "1", "1939-01", "1958-12",
   [("2.7 L6 79", "STUDE-L6-2.7", 170, {"fin": "1946-12"}), ("2.8 L6 86", "STUDE-L6-2.8", 190, {"debut": "1947-01", "fin": "1954-12"}), ("3.0 L6 102", "STUDE-L6-3.0", 210, {"debut": "1955-01"})],
   portes=4, places=5, reservoir=68, remarques="Production interrompue de 1942 à 1945 ; " + IND)
mg(L, "M-series", "M", "1", "1941-01", "1948-12", [("2.8 L6 81", "STUDE-L6-2.8", 190), ("3.7 L6 95", "STUDE-L6-3.7", 230)], portes=2, places=3, reservoir=68, remarques="Pick-up ; " + IND)
mg(L, "US6", "US6", "1", "1941-06", "1945-12", [("5.2 L6 88", "HERCULES-JXD-5.2", 271)], portes=2, places=2, reservoir=150, remarques="Camion militaire 6x6 et 6x4 ; " + IND)
mg(L, "Starliner", "Starliner", "1", "1953-01", "1954-12", [("3.8 V8 122", "STUDE-V8-3.8", 258), ("3.8 V8 129", "STUDE-V8-3.8", 258, {"debut": "1954-01"})], portes=2, places=5, reservoir=68,
   remarques="Commander Starliner / Champion Starlight (design Loewy) ; " + IND)
mg(L, "Golden Hawk", "Hawk", "1", "1956-01", "1958-12", [("5.8 V8 279", "PACKARD-V8-5.8", 522, {"fin": "1956-12"}), ("4.7 V8 Supercharged 279", "STUDEBAKER-V8-4.7SC", 450, {"debut": "1957-01"})],
   portes=2, places=5, reservoir=68, remarques="V8 Packard en 1956, puis V8 289 à compresseur ; " + IND)
mg(L, "Lark", "Lark", "1", "1959-01", "1966-03",
   [("2.8 L6 91", "STUDE-L6-2.8", 197, {"fin": "1964-12"}), ("4.3 V8 182", "STUDE-V8-4.3", 353, {"fin": "1964-12"}), ("4.7 V8 228", "STUDE-V8-4.7", 407, {"fin": "1964-12"}),
    ("3.8 L6 122", "CHEVY-I6-3.8", 278, {"debut": "1965-01"}), ("4.6 V8 197", "SBC-4.6", 386, {"debut": "1965-01"})], portes=4, places=6, reservoir=68,
   remarques="Moteurs Chevrolet après l'arrêt de l'usine de South Bend (1965-1966) ; " + IND)
mg(L, "Wagonaire", "Lark", "2", "1963-01", "1966-03", [("2.8 L6 91", "STUDE-L6-2.8", 197, {"fin": "1964-12"}), ("4.3 V8 182", "STUDE-V8-4.3", 353, {"fin": "1964-12"}),
                                                        ("4.6 V8 197", "SBC-4.6", 386, {"debut": "1965-01"})],
   portes=5, places=6, reservoir=68, remarques="Break à toit coulissant sur base Lark ; " + IND)
mg(L, "Avanti", "Avanti", "1", "1962-06", "1963-12", [("R1 4.7 V8 243", "STUDE-V8-4.7", 407), ("R2 4.7 V8 Supercharged 294", "STUDEBAKER-V8-4.7SC", 450)], portes=2, places=4, reservoir=79,
   remarques="Coupé en fibre de verre (design Loewy) ; " + IND)

MOT = Motorisations("Studebaker", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Studebaker": L}
MOTEURS = MOT.moteurs()
