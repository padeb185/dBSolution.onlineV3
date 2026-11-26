"""Plymouth : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Model U, PA, Deluxe, Belvedere, Fury, Valiant, Barracuda, 'Cuda, GTX, Road Runner, Superbird, Duster, Volaré, Horizon, Reliant,
Voyager, Acclaim, Laser, Neon, Breeze et Prowler. Marque fermée en 2001.
Moteurs Chrysler récents repris de chrysler.py, Mitsubishi de mitsubishi.py (mêmes codes) ; moteurs Mopar anciens (quatre et
six cylindres à soupapes latérales, Slant Six, V8 Poly, LA, B/RB et Hemi 426), K 2.2, VW 1.7, Simca 1.6 et Mitsubishi
1.8 / 2.6 ajoutés. Puissances SAE converties en ch (× 1,014) ; jusqu'en 1971 puissances brutes (SAE gross). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .chrysler import FAMILLES as FAMILLES_CHRYSLER
from .mitsubishi import FAMILLES as FAMILLES_MITSUBISHI

E_ = "ESS"
C, B, SV = "CHAINE", "COURROIE", "NC"


def v8(l, rpm, nmrpm, t="ATM"):
    return f(t, E_, l, C, 8, rpm, nmrpm, "10W30", 4.7, 5000, a="V")


MOPAR = {
    "PLY-L4-3.2": f("ATM", E_, 3.2, SV, 4, 3400, 1200, "SAE30", 4.5, 2000),
    "FLATHEAD6-3.3": f("ATM", E_, 3.3, SV, 6, 3600, 1200, "SAE30", 4.7, 3000),
    "FLATHEAD6-3.6": f("ATM", E_, 3.6, SV, 6, 3600, 1600, "SAE30", 4.7, 3000),
    "FLATHEAD6-3.8": f("ATM", E_, 3.8, SV, 6, 3600, 1600, "SAE30", 4.7, 3000),
    "SLANT6-2.8": f("ATM", E_, 2.8, C, 6, 4400, 2400, "10W30", 4.7, 5000),
    "SLANT6-3.2": f("ATM", E_, 3.2, C, 6, 4400, 2000, "10W30", 4.7, 5000),
    "SLANT6-3.7": f("ATM", E_, 3.7, C, 6, 4000, 2400, "10W30", 4.7, 5000),
    "POLY-4.3": v8(4.3, 4400, 2400), "POLY-5.2": v8(5.2, 4400, 2400),
    "FURY-V8-5.0": v8(5.0, 4800, 3200), "B-V8-5.7": v8(5.7, 4800, 3000),
    "LA-4.5": v8(4.5, 4400, 2400), "LA-5.2": v8(5.2, 4400, 2400), "LA-5.6": v8(5.6, 5000, 3200), "LA-5.9": v8(5.9, 4000, 2400),
    "B-6.3": v8(6.3, 5200, 3400), "B-6.6": v8(6.6, 4400, 3200), "RB-7.2": v8(7.2, 4600, 3200), "HEMI-7.0": v8(7.0, 5000, 4000),
    "K-2.2": f("ATM", E_, 2.2, B, 4, 5200, 3200, "10W30", 4.3, 7500),
    "VW-1.7": f("ATM", E_, 1.7, B, 4, 5200, 2800, "10W40", 3.5, 7500),
    "SIMCA-1.6": f("ATM", E_, 1.6, C, 4, 5600, 3200, "10W40", 3.5, 7500),
    "MITSU-1.8": f("ATM", E_, 1.8, B, 4, 5000, 3500, "10W30", 4.0, 7500),
    "MITSU-2.6": f("ATM", E_, 2.6, C, 4, 4800, 2800, "10W30", 4.5, 7500),
}
CHRYSLER = {k: FAMILLES_CHRYSLER[k] for k in ("K-2.5", "K-2.5T", "MITSU-3.0", "EGA-3.3", "EGH-3.8", "NEON-2.0", "NEON-2.4", "EGJ-3.5")}
MITSUBISHI = {k: FAMILLES_MITSUBISHI[k] for k in ("4G63-2.0", "4G63T-2.0")}
VW = {"VW-1.7": MOPAR.pop("VW-1.7")}
SIMCA = {"SIMCA-1.6": MOPAR.pop("SIMCA-1.6")}
MOPAR_MITSU = {k: MOPAR.pop(k) for k in ("MITSU-1.8", "MITSU-2.6")}
FAMILLES = {**MOPAR, **CHRYSLER, **MITSUBISHI, **VW, **SIMCA, **MOPAR_MITSU}


def motoriste(fam):
    if fam in MITSUBISHI or fam in MOPAR_MITSU:
        return "Mitsubishi"
    if fam in VW:
        return "Volkswagen"
    if fam in SIMCA:
        return "Simca"
    return "Chrysler"


mg = SaisieMoteurs(FAMILLES, "Plymouth", motoriste)
L = []
NA = "Marché nord-américain"
IND = NA + " ; données indicatives"

# ---------------------------------------------------------------- avant-guerre
mg(L, "Model U", "Model U", "1", "1929-01", "1929-12", [("3.2 46", "PLY-L4-3.2", 163)], portes=4, places=5, reservoir=45, remarques="Première Plymouth (Model Q / U) ; " + IND)
mg(L, "PA", "PA", "1", "1931-01", "1932-12", [("3.2 57", "PLY-L4-3.2", 163)], portes=4, places=5, reservoir=45, remarques="Moteur « Floating Power » ; " + IND)
mg(L, "Deluxe", "Deluxe", "1", "1933-01", "1950-12", [("3.3 L6 71", "FLATHEAD6-3.3", 176, {"fin": "1941-12"}), ("3.6 L6 96", "FLATHEAD6-3.6", 237, {"debut": "1942-01"})],
   portes=4, places=6, reservoir=60, remarques="Six cylindres à soupapes latérales ; production interrompue de 1942 à 1945 ; " + IND)

# ---------------------------------------------------------------- Belvedere / Fury
mg(L, "Belvedere", "1951", "1", "1951-01", "1954-12", [("3.8 L6 98", "FLATHEAD6-3.8", 251)], portes=2, places=6, reservoir=64, remarques="Coupé hardtop puis gamme complète ; " + IND)
mg(L, "Belvedere", "1955", "1", "1955-01", "1961-12",
   [("3.8 L6 119", "FLATHEAD6-3.8", 271, {"fin": "1959-12"}), ("3.7 Slant Six 147", "SLANT6-3.7", 291, {"debut": "1960-01"}), ("4.3 V8 Hy-Fire 159", "POLY-4.3", 339, {"fin": "1956-12"}),
    ("5.2 V8 233", "POLY-5.2", 393, {"debut": "1957-01"})], portes=4, places=6, reservoir=76, remarques=IND)
mg(L, "Belvedere", "B-body 1962", "1", "1962-01", "1964-12",
   [("3.7 Slant Six 147", "SLANT6-3.7", 291), ("5.2 V8 233", "POLY-5.2", 393), ("6.3 V8 335", "B-6.3", 576), ("Max Wedge 7.0 V8 431", "HEMI-7.0", 664, {"remarques": "426 Max Wedge rattaché à la famille 426"})],
   portes=4, places=6, reservoir=76, remarques=IND)
mg(L, "Belvedere", "B-body 1965", "1", "1965-01", "1970-12",
   [("3.7 Slant Six 147", "SLANT6-3.7", 291), ("4.5 V8 182", "LA-4.5", 353), ("5.2 V8 233", "LA-5.2", 461), ("6.3 V8 335", "B-6.3", 576), ("7.0 V8 Hemi 431", "HEMI-7.0", 664, {"debut": "1966-01"})],
   portes=4, places=6, reservoir=72, remarques="Dont Satellite ; " + IND)
mg(L, "Fury", "1956", "1", "1956-01", "1958-12", [("5.0 V8 243", "FURY-V8-5.0", 400), ("Golden Commando 5.7 V8 309", "B-V8-5.7", 495, {"debut": "1958-01"})],
   portes=2, places=6, reservoir=76, remarques="Coupé hardtop sportif ; " + IND)
mg(L, "Fury", "1959", "1", "1959-01", "1964-12", [("3.7 Slant Six 147", "SLANT6-3.7", 291, {"debut": "1960-01"}), ("5.2 V8 233", "POLY-5.2", 393), ("6.3 V8 335", "B-6.3", 576)],
   portes=4, places=6, reservoir=76, remarques=IND)
mg(L, "Fury", "C-body 1965", "1", "1965-01", "1973-12",
   [("3.7 Slant Six 147", "SLANT6-3.7", 291), ("5.2 V8 233", "LA-5.2", 461), ("6.3 V8 335", "B-6.3", 576), ("7.2 V8 380", "RB-7.2", 651, {"debut": "1966-01"})],
   portes=4, places=6, reservoir=91, remarques="Fury I à III, Sport Fury, VIP ; " + IND)
mg(L, "Fury", "B-body 1975", "1", "1975-01", "1978-12", [("3.7 Slant Six 96", "SLANT6-3.7", 230), ("5.2 V8 152", "LA-5.2", 346), ("5.9 V8 177", "LA-5.9", 380), ("6.6 V8 193", "B-6.6", 434)],
   portes=4, places=6, reservoir=80, remarques="Puissances nettes ; " + IND)

# ---------------------------------------------------------------- Valiant / Barracuda / Duster / Volaré
mg(L, "Valiant", "1960", "1", "1960-01", "1962-12", [("2.8 Slant Six 103", "SLANT6-2.8", 210), ("3.7 Slant Six 147", "SLANT6-3.7", 291, {"debut": "1961-01"})],
   portes=4, places=5, reservoir=50, remarques=IND)
mg(L, "Valiant", "A-body 1963", "1", "1963-01", "1966-12", [("2.8 Slant Six 103", "SLANT6-2.8", 210), ("3.7 Slant Six 147", "SLANT6-3.7", 291), ("4.5 V8 182", "LA-4.5", 353, {"debut": "1964-01"})],
   portes=4, places=5, reservoir=50, remarques=IND)
mg(L, "Valiant", "A-body 1967", "1", "1967-01", "1976-12",
   [("2.8 Slant Six 116", "SLANT6-2.8", 210, {"fin": "1969-12"}), ("3.2 Slant Six 127", "SLANT6-3.2", 251, {"debut": "1970-01"}), ("3.7 Slant Six 147", "SLANT6-3.7", 291),
    ("5.2 V8 233", "LA-5.2", 461, {"debut": "1968-01"})], portes=4, places=5, reservoir=68, remarques=IND)
mg(L, "Barracuda", "A-body 1964", "1", "1964-04", "1969-12",
   [("3.7 Slant Six 147", "SLANT6-3.7", 291), ("4.5 V8 182", "LA-4.5", 353), ("Formula S 4.5 V8 238", "LA-4.5", 380, {"debut": "1965-01"}), ("5.6 V8 279", "LA-5.6", 461, {"debut": "1968-01"}),
    ("6.3 V8 284", "B-6.3", 542, {"debut": "1967-01"})], portes=2, places=4, reservoir=68, remarques="Fastback, coupé et cabriolet sur base Valiant ; " + IND)
mg(L, "'Cuda", "E-body", "1", "1970-01", "1971-12",
   [("5.6 V8 279", "LA-5.6", 461), ("6.3 V8 340", "B-6.3", 576), ("AAR 5.6 V8 Six Pack 294", "LA-5.6", 461, {"fin": "1970-12"}), ("7.2 V8 Six Pack 395", "RB-7.2", 664),
    ("7.0 V8 Hemi 431", "HEMI-7.0", 664)], portes=2, places=4, reservoir=68, remarques="Barracuda / 'Cuda E-body, coupé et cabriolet ; " + IND)
mg(L, "'Cuda", "E-body", "2", "1972-01", "1974-12", [("5.2 V8 152", "LA-5.2", 346), ("5.6 V8 243", "LA-5.6", 393, {"fin": "1973-12"}), ("5.9 V8 248", "LA-5.9", 393, {"debut": "1974-01"})],
   portes=2, places=4, reservoir=68, remarques="Puissances nettes ; " + IND)
mg(L, "Duster", "A-body 1970", "1", "1970-01", "1976-12",
   [("3.2 Slant Six 127", "SLANT6-3.2", 251), ("3.7 Slant Six 147", "SLANT6-3.7", 291), ("5.2 V8 233", "LA-5.2", 461), ("340 5.6 V8 279", "LA-5.6", 461, {"fin": "1973-12"}),
    ("360 5.9 V8 248", "LA-5.9", 393, {"debut": "1974-01"})], portes=2, places=5, reservoir=60, remarques="Coupé sur base Valiant ; puissances nettes à partir de 1972 ; " + IND)
mg(L, "Volaré", "F-body", "1", "1976-01", "1980-12", [("3.7 Slant Six 101", "SLANT6-3.7", 230), ("5.2 V8 147", "LA-5.2", 339), ("5.9 V8 177", "LA-5.9", 380)],
   portes=4, places=5, reservoir=68, remarques="Berline, coupé et break ; " + IND)

# ---------------------------------------------------------------- muscle cars
mg(L, "GTX", "B-body 1967", "1", "1967-01", "1971-12", [("7.2 V8 380", "RB-7.2", 651), ("7.0 V8 Hemi 431", "HEMI-7.0", 664), ("7.2 V8 Six Pack 395", "RB-7.2", 664, {"debut": "1969-01"})],
   portes=2, places=5, reservoir=72, remarques=IND)
mg(L, "Road Runner", "B-body 1968", "1", "1968-01", "1971-12", [("6.3 V8 340", "B-6.3", 576), ("7.0 V8 Hemi 431", "HEMI-7.0", 664), ("7.2 V8 Six Pack 395", "RB-7.2", 664, {"debut": "1969-03"})],
   portes=2, places=5, reservoir=72, remarques=IND)
mg(L, "Road Runner", "B-body 1972", "1", "1972-01", "1974-12", [("5.2 V8 152", "LA-5.2", 346, {"debut": "1973-01"}), ("6.6 V8 258", "B-6.6", 461), ("7.2 V8 284", "RB-7.2", 508)],
   portes=2, places=5, reservoir=72, remarques="Puissances nettes ; " + IND)
mg(L, "Road Runner", "1975", "1", "1975-01", "1980-12", [("5.2 V8 152", "LA-5.2", 346), ("5.9 V8 177", "LA-5.9", 380)], portes=2, places=5, reservoir=68,
   remarques="Finition sur Fury puis Volaré ; " + IND)
mg(L, "Superbird", "B-body 1970", "1", "1970-01", "1970-12",
   [("7.2 V8 380", "RB-7.2", 651), ("7.2 V8 Six Pack 395", "RB-7.2", 664), ("7.0 V8 Hemi 431", "HEMI-7.0", 664)], portes=2, places=5, reservoir=72,
   remarques="Série d'homologation NASCAR (environ 1 900 ex.) ; " + IND)

# ---------------------------------------------------------------- traction (années 1980-2000)
mg(L, "Horizon", "L-body", "1", "1978-01", "1990-12",
   [("1.7 71", "VW-1.7", 122, {"fin": "1983-12"}), ("2.2 85", "K-2.2", 151, {"debut": "1981-01"}), ("2.2 97", "K-2.2", 163, {"debut": "1987-01"}), ("1.6 65", "SIMCA-1.6", 118, {"debut": "1983-01", "fin": "1986-12"})],
   portes=5, places=5, reservoir=49, remarques="Jumelle américaine de la Simca / Talbot Horizon ; " + IND)
mg(L, "Reliant", "K-body", "1", "1981-01", "1989-12",
   [("2.2 85", "K-2.2", 151), ("2.2 97", "K-2.2", 163, {"debut": "1985-01"}), ("2.6 93", "MITSU-2.6", 179, {"fin": "1985-12"}), ("2.5 101", "K-2.5", 180, {"debut": "1986-01"})],
   portes=4, places=6, reservoir=53, remarques="Berline, coupé et break ; " + IND)
mg(L, "Voyager", "S", "1", "1984-01", "1990-12",
   [("2.2 97", "K-2.2", 163), ("2.6 105", "MITSU-2.6", 193, {"fin": "1987-12"}), ("2.5 101", "K-2.5", 180, {"debut": "1987-01"}), ("2.5 Turbo 152", "K-2.5T", 285, {"debut": "1989-01"}),
    ("3.0 V6 144", "MITSU-3.0", 233, {"debut": "1987-01"}), ("3.3 V6 152", "EGA-3.3", 251, {"debut": "1990-01"})],
   portes=4, places=7, reservoir=57, remarques="Voyager et Grand Voyager ; " + IND)
mg(L, "Voyager", "AS", "1", "1991-01", "1995-12", [("2.5 101", "K-2.5", 180), ("3.0 V6 144", "MITSU-3.0", 233), ("3.3 V6 152", "EGA-3.3", 251), ("3.8 V6 164", "EGH-3.8", 291, {"debut": "1994-01"})],
   portes=4, places=7, reservoir=76, remarques=IND)
mg(L, "Voyager", "NS", "1", "1996-01", "2000-12", [("2.4 152", "NEON-2.4", 226), ("3.0 V6 152", "MITSU-3.0", 239), ("3.3 V6 160", "EGA-3.3", 275), ("3.8 V6 182", "EGH-3.8", 312)],
   portes=4, places=7, reservoir=76, remarques="Repris sous la marque Chrysler en 2001 ; " + IND)
mg(L, "Acclaim", "AA", "1", "1989-01", "1995-12", [("2.5 101", "K-2.5", 180), ("2.5 Turbo 152", "K-2.5T", 285, {"fin": "1990-12"}), ("3.0 V6 143", "MITSU-3.0", 233)],
   portes=4, places=5, reservoir=61, remarques=IND)
mg(L, "Laser", "D20", "1", "1990-01", "1994-12", [("1.8 93", "MITSU-1.8", 142), ("2.0 136", "4G63-2.0", 176), ("RS 2.0 Turbo 193", "4G63T-2.0", 275)],
   portes=3, places=4, reservoir=60, remarques="Jumelle des Mitsubishi Eclipse et Eagle Talon ; " + IND)
mg(L, "Neon", "PL", "1", "1995-01", "1999-12", [("2.0 134", "NEON-2.0", 176), ("2.0 DOHC 152", "NEON-2.0", 180)], portes=4, places=5, reservoir=47, remarques="Berline et coupé ; " + IND)
mg(L, "Neon", "PL", "2", "2000-01", "2001-12", [("2.0 134", "NEON-2.0", 176)], portes=4, places=5, reservoir=47, remarques="Deuxième génération ; " + IND)
mg(L, "Breeze", "JA", "1", "1996-01", "2000-12", [("2.0 134", "NEON-2.0", 176), ("2.4 152", "NEON-2.4", 226, {"debut": "1997-01"})], portes=4, places=5, reservoir=60, remarques=IND)
mg(L, "Prowler", "PR", "1", "1997-01", "2002-12", [("3.5 V6 217", "EGJ-3.5", 300, {"fin": "1998-12"}), ("3.5 V6 257", "EGJ-3.5", 346, {"debut": "1999-01"})],
   portes=2, places=2, reservoir=45, remarques="Roadster ; vendu sous la marque Chrysler en 2001-2002 ; " + IND)

MOT = Motorisations("Plymouth", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Plymouth": L}
MOTEURS = MOT.moteurs()
