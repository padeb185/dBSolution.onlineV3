"""Rover : générations, phases, motorisations (marché européen) et moteurs liés.
10, 14, P4, P5, P6, SD1, 200 (SD3, R8, R3), 400, 600, 800, 25, 45, 75, Streetwise et CityRover. Marque fermée en 2005.
Moteurs Rover repris de land_rover.py et mg.py, Honda de honda.py, V8 Ford de lincoln.py, BMW via land_rover.py (mêmes codes) ;
moteurs Rover anciens (IOE, OHC, O-series, M16), Honda F18 / H23 / V6, VM et Tata ajoutés. Données anciennes indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .honda import FAMILLES as FAMILLES_HONDA
from .land_rover import FAMILLES as FAMILLES_LR
from .lincoln import FAMILLES as FAMILLES_LINCOLN
from .mg import FAMILLES as FAMILLES_MG
from .peugeot import FAMILLES as FAMILLES_PEUGEOT

E_, D = "ESS", "DSL"
C, B, SV = "CHAINE", "COURROIE", "NC"

ROVER_PROPRES = {
    "ROVER-L4-1.4": f("ATM", E_, 1.4, SV, 4, 4000, 2000, "SAE30", 4.0, 3000),
    "ROVER-L6-1.6": f("ATM", E_, 1.6, SV, 6, 4200, 2200, "SAE30", 4.5, 3000),
    "ROVER-IOE-2.0": f("ATM", E_, 2.0, C, 4, 4000, 2000, "20W50", 5.0, 5000),
    "ROVER-IOE-2.6": f("ATM", E_, 2.6, C, 6, 4500, 2000, "20W50", 6.0, 5000),
    "ROVER-IOE-3.0": f("ATM", E_, 3.0, C, 6, 5000, 2500, "20W50", 6.0, 5000),
    "ROVER-P6-2.0": f("ATM", E_, 2.0, C, 4, 5000, 3000, "20W50", 4.5, 5000),
    "ROVER-P6-2.2": f("ATM", E_, 2.2, C, 4, 5000, 3000, "20W50", 4.5, 5000),
    "ROVER-PE-2.6": f("ATM", E_, 2.6, B, 6, 5000, 3750, "20W50", 5.0, 10000),
    "BL-O-2.0": f("ATM", E_, 2.0, B, 4, 5250, 3250, "20W50", 4.5, 10000),
    "BL-S-1.6": f("ATM", E_, 1.6, B, 4, 5600, 3500, "20W50", 4.0, 10000),
    "ROVER-M16-2.0": f("ATM", E_, 2.0, B, 4, 6000, 4500, "10W40", 4.5, 10000),
    "ROVER-T16-2.0T": f("TURBO", E_, 2.0, B, 4, 6000, 2500, "10W40", 4.5, 10000),
    "ROVER-KV6-2.0": f("ATM", E_, 2.0, B, 6, 6500, 4000, "10W40", 5.0, 15000, a="V"),
    "ROVER-K-1.1": f("ATM", E_, 1.1, B, 4, 6000, 3500, "10W40", 4.5, 15000),
}
VM = {"VM-2.4TD": f("TURBO", D, 2.4, B, 4, 4200, 2200, "15W40", 6.0, 10000), "VM-2.5TD-R": f("TURBO", D, 2.5, B, 4, 4200, 2100, "15W40", 6.0, 10000)}
HONDA_PROPRES = {
    "HONDA-EV-1.3": f("ATM", E_, 1.3, B, 4, 6000, 3500, "10W40", 3.5, 10000),
    "HONDA-F18": f("ATM", E_, 1.8, B, 4, 6100, 4200, "10W40", 4.0, 10000),
    "HONDA-H23": f("ATM", E_, 2.3, B, 4, 5800, 4800, "10W40", 4.5, 10000),
    "HONDA-C25": f("ATM", E_, 2.5, B, 6, 6000, 4500, "10W40", 4.5, 10000, a="V"),
    "HONDA-C27": f("ATM", E_, 2.7, B, 6, 6000, 4500, "10W40", 4.5, 10000, a="V"),
}
TATA = {"TATA-1.4": f("ATM", E_, 1.4, B, 4, 5500, 3000, "15W40", 3.5, 10000)}
ROVER = {**ROVER_PROPRES, **{k: FAMILLES_LR[k] for k in ("ROVER-V8-3.5", "ROVER-T16-2.0", "ROVER-K-1.8", "ROVER-KV6-2.5", "ROVER-L-2.0DI")},
         **{k: FAMILLES_MG[k] for k in ("ROVER-K-1.4", "ROVER-K-1.6", "ROVER-K-1.8T")}}
HONDA = {**HONDA_PROPRES, **{k: FAMILLES_HONDA[k] for k in ("D16", "F20")}}
BMW = {"M47-2.0": FAMILLES_LR["M47-2.0"]}
FORD = {"MODULAR-4.6": FAMILLES_LINCOLN["MODULAR-4.6"]}
PSA = {"XUD7TE": FAMILLES_PEUGEOT["XUD7TE"]}
FAMILLES = {**ROVER, **VM, **HONDA, **TATA, **BMW, **FORD, **PSA}


def motoriste(fam):
    if fam in HONDA:
        return "Honda"
    if fam in VM:
        return "VM Motori"
    if fam in TATA:
        return "Tata"
    if fam in BMW:
        return "BMW"
    if fam in FORD:
        return "Ford"
    if fam in PSA:
        return "Peugeot"
    if fam.startswith("BL-"):
        return "British Leyland"
    return "Rover"


mg = SaisieMoteurs(FAMILLES, "Rover", motoriste)
L = []
IND = "données indicatives"

# ---------------------------------------------------------------- anciennes
mg(L, "14", "14", "1", "1924-01", "1948-12", [("1.6 L6 48", "ROVER-L6-1.6", 100)], portes=4, places=5, reservoir=50, remarques="Rover 14 et Fourteen ; " + IND)
mg(L, "10", "10", "1", "1927-01", "1947-12", [("1.4 39", "ROVER-L4-1.4", 80)], portes=4, places=5, reservoir=45, remarques="Rover 10 / Ten ; " + IND)
mg(L, "P4", "P4", "1", "1949-09", "1964-05",
   [("60 2.0 61", "ROVER-IOE-2.0", 137, {"debut": "1954-01", "fin": "1959-12"}), ("75 2.1 L6 76", "ROVER-IOE-2.6", 144, {"fin": "1959-12"}), ("90 2.6 L6 91", "ROVER-IOE-2.6", 176, {"debut": "1954-01", "fin": "1959-12"}),
    ("100 2.6 L6 105", "ROVER-IOE-2.6", 189, {"debut": "1960-01"}), ("110 2.6 L6 125", "ROVER-IOE-2.6", 189, {"debut": "1962-01"})],
   portes=4, places=5, reservoir=52, remarques="« Auntie » Rover ; 2.1 rattaché à la famille 2.6 ; " + IND)
mg(L, "P5", "P5", "1", "1958-09", "1973-06", [("3 Litre 3.0 L6 117", "ROVER-IOE-3.0", 217, {"fin": "1966-12"}), ("3 Litre 3.0 L6 136", "ROVER-IOE-3.0", 220, {"debut": "1962-09", "fin": "1967-08"}),
                                              ("P5B 3.5 V8 164", "ROVER-V8-3.5", 281, {"debut": "1967-09"})],
   portes=4, places=5, reservoir=64, remarques="Berline et Coupé ; P5B à V8 (B pour Buick) ; " + IND)
mg(L, "P6", "P6", "1", "1963-10", "1977-03",
   [("2000 2.0 92", "ROVER-P6-2.0", 153, {"fin": "1973-09"}), ("2000 TC 2.0 112", "ROVER-P6-2.0", 168, {"debut": "1966-03", "fin": "1973-09"}), ("2200 2.2 99", "ROVER-P6-2.2", 171, {"debut": "1973-10"}),
    ("2200 TC 2.2 117", "ROVER-P6-2.2", 183, {"debut": "1973-10"}), ("3500 3.5 V8 146", "ROVER-V8-3.5", 271, {"debut": "1968-04"}), ("3500 S 3.5 V8 152", "ROVER-V8-3.5", 274, {"debut": "1971-10"})],
   portes=4, places=5, reservoir=55, remarques="Voiture européenne de l'année 1964 ; " + IND)
mg(L, "SD1", "SD1", "1", "1976-07", "1986-12",
   [("2000 2.0 101", "BL-O-2.0", 164, {"debut": "1982-01"}), ("2300 2.3 L6 125", "ROVER-PE-2.6", 182, {"debut": "1977-10", "remarques": "2.3 rattaché à la famille 2.6 PE"}),
    ("2600 2.6 L6 138", "ROVER-PE-2.6", 206, {"debut": "1977-10"}), ("3500 3.5 V8 157", "ROVER-V8-3.5", 271), ("Vitesse 3.5 V8 193", "ROVER-V8-3.5", 298, {"debut": "1982-10"}),
    ("2400 SD Turbo 2.4 91", "VM-2.4TD", 192, {"debut": "1982-06"})], portes=5, places=5, reservoir=66, remarques="Voiture européenne de l'année 1977 ; " + IND)

# ---------------------------------------------------------------- 200 / 400 / 600 / 800
mg(L, "200", "SD3", "1", "1984-06", "1989-10", [("213 1.3 71", "HONDA-EV-1.3", 101), ("216 1.6 86", "BL-S-1.6", 130), ("216 Vitesse 1.6 104", "BL-S-1.6", 137, {"debut": "1985-01"})],
   portes=4, places=5, reservoir=50, remarques="Berline sur base Honda Ballade ; " + IND)
mg(L, "200", "R8", "1", "1989-10", "1995-11",
   [("214 1.4 75", "ROVER-K-1.4", 117), ("214 16V 1.4 95", "ROVER-K-1.4", 124), ("216 GTi 1.6 16V 131", "D16", 142, {"remarques": "Honda D16"}), ("216 1.6 112", "D16", 142),
    ("220 GTi 2.0 16V 136", "ROVER-T16-2.0", 185, {"debut": "1992-01"}), ("220 Turbo 2.0 200", "ROVER-T16-2.0T", 240, {"debut": "1992-06"}), ("218 TD 1.8 88", "XUD7TE", 180)],
   portes=5, places=5, reservoir=50, remarques="3 et 5 portes, coupé, cabriolet, Tourer ; " + IND)
mg(L, "200", "R3", "1", "1995-11", "1999-12",
   [("211 1.1 60", "ROVER-K-1.1", 90), ("214 1.4 75", "ROVER-K-1.4", 117), ("214 16V 1.4 103", "ROVER-K-1.4", 127), ("216 1.6 112", "ROVER-K-1.6", 145), ("218 VVC 1.8 145", "ROVER-K-1.8", 174),
    ("220 D 2.0 86", "ROVER-L-2.0DI", 185), ("220 SDi 2.0 105", "ROVER-L-2.0DI", 210)], portes=5, places=5, reservoir=50, remarques="3 et 5 portes ; " + IND)
mg(L, "400", "R8", "1", "1990-04", "1995-12",
   [("414 1.4 95", "ROVER-K-1.4", 124), ("416 1.6 112", "D16", 142), ("420 GSi 2.0 136", "ROVER-T16-2.0", 185, {"debut": "1992-01"}), ("420 Turbo 2.0 200", "ROVER-T16-2.0T", 240, {"debut": "1993-01"})],
   portes=4, places=5, reservoir=55, remarques="Berline et Tourer ; " + IND)
mg(L, "400", "HH-R", "1", "1995-05", "1999-12",
   [("414 1.4 103", "ROVER-K-1.4", 127), ("416 1.6 112", "ROVER-K-1.6", 145), ("420 2.0 136", "ROVER-T16-2.0", 185), ("420 D 2.0 86", "ROVER-L-2.0DI", 185), ("420 SDi 2.0 105", "ROVER-L-2.0DI", 210)],
   portes=5, places=5, reservoir=55, remarques="Base Honda Domani ; berline et 5 portes ; " + IND)
mg(L, "600", "RH", "1", "1993-04", "1999-12",
   [("618 1.8 115", "HONDA-F18", 158), ("620 2.0 131", "F20", 179), ("623 2.3 158", "HONDA-H23", 202), ("620 Ti 2.0 Turbo 200", "ROVER-T16-2.0T", 240, {"debut": "1995-01"}),
    ("620 SDi 2.0 105", "ROVER-L-2.0DI", 210, {"debut": "1995-01"})], portes=4, places=5, reservoir=65, remarques="Base Honda Accord ; " + IND)
mg(L, "800", "XX", "1", "1986-07", "1991-12", [("820 2.0 140", "ROVER-M16-2.0", 178), ("825 2.5 V6 173", "HONDA-C25", 217), ("827 2.7 V6 177", "HONDA-C27", 228, {"debut": "1988-01"}),
                                               ("825 SD 2.5 118", "VM-2.5TD-R", 266, {"debut": "1990-01"})], portes=4, places=5, reservoir=68, remarques="Développée avec Honda (Legend) ; " + IND)
mg(L, "800", "R17", "1", "1992-01", "1999-12",
   [("820 2.0 136", "ROVER-T16-2.0", 185), ("820 Turbo 2.0 180", "ROVER-T16-2.0T", 240, {"debut": "1994-01"}), ("827 2.7 V6 169", "HONDA-C27", 228, {"fin": "1996-06"}),
    ("825 2.5 KV6 175", "ROVER-KV6-2.5", 240, {"debut": "1996-07"}), ("825 SD 2.5 118", "VM-2.5TD-R", 266)], portes=4, places=5, reservoir=68,
   remarques="Restylage ; berline, Fastback et Coupé ; " + IND)

# ---------------------------------------------------------------- 25 / 45 / 75 / Streetwise / CityRover
mg(L, "25", "R3", "1", "1999-10", "2005-04",
   [("1.1 75", "ROVER-K-1.1", 95), ("1.4 84", "ROVER-K-1.4", 120), ("1.4 103", "ROVER-K-1.4", 127), ("1.6 109", "ROVER-K-1.6", 138), ("1.8 117", "ROVER-K-1.8", 160),
    ("GTi 1.8 VVC 145", "ROVER-K-1.8", 174), ("2.0 iDT 101", "ROVER-L-2.0DI", 240), ("2.0 iDT 113", "ROVER-L-2.0DI", 260)],
   portes=5, places=5, reservoir=50, remarques="3 et 5 portes ; restylage 2004")
mg(L, "45", "HH-R", "1", "1999-12", "2005-04",
   [("1.4 103", "ROVER-K-1.4", 127), ("1.6 109", "ROVER-K-1.6", 138), ("1.8 117", "ROVER-K-1.8", 160), ("2.0 V6 150", "ROVER-KV6-2.0", 185), ("2.0 iDT 101", "ROVER-L-2.0DI", 240),
    ("2.0 iDT 113", "ROVER-L-2.0DI", 260)], portes=5, places=5, reservoir=55, remarques="Berline et 5 portes ; restylage 2004")
mg(L, "75", "R40", "1", "1998-10", "2005-04",
   [("1.8 120", "ROVER-K-1.8", 165), ("1.8 Turbo 150", "ROVER-K-1.8T", 215, {"debut": "2002-01"}), ("2.0 V6 150", "ROVER-KV6-2.0", 185), ("2.5 V6 177", "ROVER-KV6-2.5", 240),
    ("2.0 CDT 116", "M47-2.0", 280), ("2.0 CDTi 131", "M47-2.0", 300, {"debut": "2001-06"}), ("4.6 V8 260", "MODULAR-4.6", 410, {"debut": "2004-06"})],
   portes=4, places=5, reservoir=65, remarques="Berline, Tourer et Limousine ; restylage 2004 ; dernière Rover")
mg(L, "Streetwise", "R3", "2", "2003-06", "2005-04", [("1.4 103", "ROVER-K-1.4", 127), ("1.6 109", "ROVER-K-1.6", 138), ("2.0 TD 101", "ROVER-L-2.0DI", 240)],
   portes=5, places=4, reservoir=50, remarques="Version surélevée de la 25")
mg(L, "CityRover", "Indica", "1", "2003-11", "2005-04", [("1.4 85", "TATA-1.4", 120)], portes=5, places=5, reservoir=37, remarques="Base Tata Indica")

MOT = Motorisations("Rover", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Rover": L}
MOTEURS = MOT.moteurs()
