"""Chevrolet, Chevrolet Corvette et Chevrolet Camaro ZL1 : générations, motorisations et moteurs liés.
Chevrolet Europe (2005-2015, ex-Daewoo) : Matiz, Spark, Aveo, Lacetti, Epica, Captiva, Cruze, Orlando, Malibu, Volt, Trax.
Amérique du Nord : Bel Air, Nova (classiques), Camaro, Impala, Malibu, Cruze, Spark, Trax, Equinox, Blazer, Traverse, Tahoe,
Suburban, Colorado, Silverado, Bolt, Equinox EV, Blazer EV, Silverado EV. Corvette (C1 à C8) dans « Chevrolet Corvette ».
Puissances américaines converties en ch (×1,014). Moteurs ex-Daewoo : familles et codes de daewoo.py (motoriste « Daewoo »).
Données antérieures à 1990 indicatives. Saisie : (nom, famille, couple_nm[, surcharges]) ; puissance = dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .daewoo import FAMILLES as FAMILLES_DAEWOO

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"


def v8(t, l, rpm, nmrpm, q=5.7, km=12000):
    return f(t, E_, l, C, 8, rpm, nmrpm, "5W30", q, km, a="V")


DAEWOO = ("F8CV-0.8", "SOHC-1.0", "SOHC-1.2", "SOHC-1.4", "ETEC-1.4", "ETEC-1.6", "FAM2-1.8", "FAM2-2.0")
PROPRES = {
    # --- petites cylindrées GM Korea / Europe
    "B10D-1.0": f("ATM", E_, 1.0, C, 4, 6400, 4800, "5W30", 3.75, 15000),
    "B12D-1.2": f("ATM", E_, 1.2, C, 4, 6400, 4800, "5W30", 3.75, 15000),
    "ECOTEC-1.4T": f("TURBO", E_, 1.4, B, 4, 4900, 1850, "5W30", 4.0, 15000),
    "ECOTEC-1.6": f("ATM", E_, 1.6, B, 4, 6400, 4200, "5W30", 4.5, 15000),
    "ECOTEC-1.8": f("ATM", E_, 1.8, B, 4, 6200, 3800, "5W30", 4.5, 15000),
    "GM-1.5T": f("TURBO", E_, 1.5, C, 4, 5600, 2000, "0W20", 4.0, 12000),
    "GM-1.2T": f("TURBO", E_, 1.2, C, 3, 5000, 2500, "0W20", 3.8, 12000),
    "GM-2.0T": f("TURBO", E_, 2.0, C, 4, 5500, 3000, "0W20", 5.0, 12000),
    "GM-2.4": f("ATM", E_, 2.4, C, 4, 5600, 4600, "5W30", 4.7, 15000),
    "GM-2.5": f("ATM", E_, 2.5, C, 4, 6300, 4400, "0W20", 4.7, 12000),
    "GM-2.7T": f("TURBO", E_, 2.7, C, 4, 5600, 2000, "0W20", 6.0, 12000),
    "GM-2.5T": f("TURBO", E_, 2.5, C, 4, 5600, 2000, "0W20", 5.2, 12000),
    "GM-3.2-V6": f("ATM", E_, 3.2, C, 6, 6600, 3200, "5W30", 5.7, 15000, a="V"),
    "GM-3.6-V6": f("ATM", E_, 3.6, C, 6, 6800, 5200, "5W30", 5.7, 12000, a="V"),
    "XK6-2.0": f("ATM", E_, 2.0, C, 6, 6400, 4600, "5W30", 6.0, 15000),
    "XK6-2.5": f("ATM", E_, 2.5, C, 6, 5800, 4000, "5W30", 6.0, 15000),
    "VCDI-1.3": f("TURBO", D, 1.3, C, 4, 4000, 1750, "5W30", 3.2, 20000),
    "VCDI-1.7": f("TURBO", D, 1.7, C, 4, 4000, 2000, "5W30", 4.5, 20000),
    "VCDI-2.0": f("TURBO", D, 2.0, B, 4, 3800, 2000, "5W30", 5.6, 20000),
    "VCDI-2.2": f("TURBO", D, 2.2, C, 4, 3800, 2000, "5W30", 5.6, 20000),
    "DURAMAX-2.8": f("TURBO", D, 2.8, C, 4, 3400, 2000, "5W30", 6.0, 12000),
    "DURAMAX-3.0": f("TURBO", D, 3.0, C, 6, 3750, 1500, "0W20", 6.6, 12000),
    "VOLTEC-1.4": f("HYB_E", E_, 1.4, C, 4, 4800, 0, "0W20", 4.0, 15000),
    "VOLTEC-1.5": f("HYB_E", E_, 1.5, C, 4, 5600, 0, "0W20", 4.0, 15000),
    # --- V8 small-block / big-block
    "SBC-4.3": v8("ATM", 4.3, 4400, 2800, 4.7, 5000), "SBC-4.6": v8("ATM", 4.6, 4800, 3000, 4.7, 5000), "SBC-5.4": v8("ATM", 5.4, 5000, 3200, 4.7, 5000),
    "SBC-5.7": v8("ATM", 5.7, 5000, 3200, 4.7, 5000), "BBC-7.0": v8("ATM", 7.0, 5400, 3600, 5.7, 5000), "BBC-7.4": v8("ATM", 7.4, 4800, 3200, 5.7, 5000),
    "L98-5.7": v8("ATM", 5.7, 4300, 3200, 4.7), "LT1-5.7": v8("ATM", 5.7, 5000, 2400, 4.7), "LT5-5.7": v8("ATM", 5.7, 6200, 4800, 11.0),
    "LS1-5.7": v8("ATM", 5.7, 5600, 4000), "LS6-5.7": v8("ATM", 5.7, 6000, 4800), "LS2-6.0": v8("ATM", 6.0, 6000, 4400), "LS3-6.2": v8("ATM", 6.2, 5900, 4600),
    "LS7-7.0": v8("ATM", 7.0, 6300, 4800, 7.6), "LS9-6.2SC": v8("TURBO", 6.2, 6500, 3800, 10.5), "LSA-6.2SC": v8("TURBO", 6.2, 6100, 3800, 9.5),
    "LT1-6.2": v8("ATM", 6.2, 6000, 4600, 7.6), "LT2-6.2": v8("ATM", 6.2, 6450, 5150, 7.6), "LT4-6.2SC": v8("TURBO", 6.2, 6400, 3600, 9.8),
    "LT5-6.2SC": v8("TURBO", 6.2, 6300, 4400, 9.8), "LT6-5.5": v8("ATM", 5.5, 8400, 6300, 9.8), "LT7-5.5TT": v8("TURBO", 5.5, 7000, 6000, 9.8),
    "L84-5.3": v8("ATM", 5.3, 5600, 4100, 7.6), "L87-6.2": v8("ATM", 6.2, 5600, 4100, 7.6), "L83-5.3": v8("ATM", 5.3, 5600, 4100, 7.6),
    "LT2-ERAY": v8("HYB_TE", 6.2, 6450, 5150, 7.6),
    "STOVEBOLT-3.9": f("ATM", E_, 3.9, C, 6, 4000, 2400, "20W50", 4.7, 5000),
    "CHEVY-I6-4.1": f("ATM", E_, 4.1, C, 6, 4200, 1600, "20W50", 4.7, 5000),
    # --- électriques
    "GM-EV-BOLT": electrique(), "ULTIUM": electrique(),
}
FAMILLES = {**{k: FAMILLES_DAEWOO[k] for k in DAEWOO}, **PROPRES}


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Chevrolet", lambda fam: "Daewoo" if fam in DAEWOO else "Chevrolet")
L, LC, LZ = [], [], []   # Chevrolet, Chevrolet Corvette, Chevrolet Camaro ZL1
EU = "Marché européen (ex-Daewoo) ; retrait de Chevrolet d'Europe fin 2015"
NA = "Marché nord-américain"
IND = "données indicatives"

# ---------------------------------------------------------------- Chevrolet Europe
mg(L, "Matiz", "M200", "1", "2005-03", "2010-12", [("0.8 52", "F8CV-0.8", 69), ("1.0 67", "SOHC-1.0", 91)], reservoir=35, remarques=EU)
mg(L, "Spark", "M300", "1", "2010-01", "2015-12", [("1.0 68", "B10D-1.0", 93), ("1.2 82", "B12D-1.2", 111)], reservoir=35, remarques=EU + " ; vendue aussi en Amérique du Nord (2013-2015)")
mg(L, "Aveo", "T250", "1", "2005-03", "2011-06", [("1.2 72", "SOHC-1.2", 104), ("1.2 84", "B12D-1.2", 114, {"debut": "2008-01"}), ("1.4 94", "ETEC-1.4", 130), ("1.4 101", "ETEC-1.4", 131, {"debut": "2008-01"})],
   reservoir=45, remarques=EU + " ; ex-Daewoo Kalos ; 3 et 5 portes, berline")
mg(L, "Aveo", "T300", "1", "2011-07", "2015-12",
   [("1.2 70", "B12D-1.2", 110), ("1.2 86", "B12D-1.2", 115), ("1.4 100", "ETEC-1.4", 130), ("1.6 115", "ECOTEC-1.6", 155), ("1.3 VCDi 75", "VCDI-1.3", 190), ("1.3 VCDi 95", "VCDI-1.3", 210)],
   reservoir=46, remarques=EU + " ; 5 portes et berline")
mg(L, "Lacetti", "J200", "1", "2005-01", "2011-06", [("1.4 95", "ETEC-1.4", 131), ("1.6 109", "ETEC-1.6", 150), ("1.8 122", "FAM2-1.8", 165), ("2.0 VCDi 121", "VCDI-2.0", 280, {"debut": "2007-01"})],
   reservoir=60, remarques=EU + " ; berline Nubira et SW")
mg(L, "Epica", "V250", "1", "2006-06", "2011-06", [("2.0 144", "XK6-2.0", 195), ("2.5 156", "XK6-2.5", 237), ("2.0 VCDi 150", "VCDI-2.0", 320, {"debut": "2007-06"})], portes=4, reservoir=65,
   remarques=EU)
mg(L, "Captiva", "C100", "1", "2006-06", "2011-03", [("2.4 136", "GM-2.4", 220), ("3.2 V6 230", "GM-3.2-V6", 297), ("2.0 VCDi 127", "VCDI-2.0", 295), ("2.0 VCDi 150", "VCDI-2.0", 320, {"debut": "2008-01"})],
   places=7, reservoir=65, remarques=EU + " ; 5 ou 7 places")
mg(L, "Captiva", "C140", "1", "2011-04", "2015-12", [("2.4 167", "GM-2.4", 230), ("2.2 VCDi 163", "VCDI-2.2", 350), ("2.2 VCDi 184", "VCDI-2.2", 400)], places=7, reservoir=65,
   remarques=EU + " ; restylage")
mg(L, "Cruze", "J300", "1", "2009-05", "2015-12",
   [("1.6 113", "ECOTEC-1.6", 153, {"fin": "2011-12"}), ("1.6 124", "ECOTEC-1.6", 154, {"debut": "2012-01"}), ("1.8 141", "ECOTEC-1.8", 176), ("1.4 Turbo 140", "ECOTEC-1.4T", 200, {"debut": "2011-09"}),
    ("2.0 VCDi 150", "VCDI-2.0", 320), ("2.0 VCDi 163", "VCDI-2.0", 360, {"debut": "2011-01"}), ("1.7 VCDi 130", "VCDI-1.7", 300, {"debut": "2012-06"})], portes=4, reservoir=60,
   remarques=EU + " ; berline, 5 portes, SW (2012)")
mg(L, "Orlando", "J309", "1", "2011-01", "2015-12", [("1.8 141", "ECOTEC-1.8", 176), ("1.4 Turbo 140", "ECOTEC-1.4T", 200, {"debut": "2012-06"}), ("2.0 VCDi 131", "VCDI-2.0", 315),
                                                     ("2.0 VCDi 163", "VCDI-2.0", 360), ("1.7 VCDi 130", "VCDI-1.7", 300, {"debut": "2013-01"})], places=7, reservoir=64, remarques=EU + " ; monospace 7 places")
mg(L, "Malibu", "V300", "1", "2012-03", "2015-12", [("2.4 167", "GM-2.4", 225), ("2.0 VCDi 160", "VCDI-2.0", 350)], portes=4, reservoir=70, remarques=EU)
mg(L, "Volt", "Voltec", "1", "2011-01", "2015-12", [("Volt 150", "VOLTEC-1.4", 370, {"batterie": 16})], places=4, reservoir=35,
   remarques="Hybride à prolongateur d'autonomie ; Amérique du Nord et Europe (jumelle Opel Ampera)")
mg(L, "Volt", "Voltec", "2", "2016-01", "2019-02", [("Volt 151", "VOLTEC-1.5", 398, {"batterie": 18})], places=5, reservoir=34, remarques=NA)
mg(L, "Trax", "Gamma II", "1", "2013-03", "2015-12", [("1.6 115", "ECOTEC-1.6", 155), ("1.4 Turbo 140", "ECOTEC-1.4T", 200), ("1.7 VCDi 130", "VCDI-1.7", 300)], reservoir=53,
   remarques=EU + " ; jumeau Opel Mokka")

# ---------------------------------------------------------------- Amérique du Nord : voitures
mg(L, "Bel Air", "Tri-Five", "1", "1953-01", "1957-12", [("3.9 I6 117", "STOVEBOLT-3.9", 271), ("4.3 V8 164", "SBC-4.3", 348, {"debut": "1955-01"}),
                                                          ("4.6 V8 223", "SBC-4.6", 393, {"debut": "1957-01"})], portes=4, reservoir=60, remarques=NA + " ; " + IND)
mg(L, "Nova", "X-body", "1", "1968-01", "1974-12", [("4.1 I6 142", "CHEVY-I6-4.1", 312), ("5.7 V8 SS 304", "SBC-5.7", 515)], portes=4, reservoir=60, remarques=NA + " ; " + IND)
mg(L, "Camaro", "5e gén.", "1", "2010-01", "2015-12", [("3.6 V6 309", "GM-3.6-V6", 370), ("SS 6.2 V8 432", "LS3-6.2", 569)], portes=2, places=4, reservoir=72,
   remarques=NA + " ; aussi vendue en Europe ; ZL1 dans « Chevrolet Camaro ZL1 »")
mg(L, "Camaro", "6e gén.", "1", "2016-01", "2023-12", [("2.0 Turbo 279", "GM-2.0T", 400), ("3.6 V6 340", "GM-3.6-V6", 386), ("SS 6.2 V8 461", "LT1-6.2", 617)],
   portes=2, places=4, reservoir=72, remarques=NA + " ; aussi vendue en Europe ; fin de production décembre 2023")
mg(L, "Impala", "10e gén.", "1", "2014-01", "2020-02", [("2.5 199", "GM-2.5", 254), ("3.6 V6 309", "GM-3.6-V6", 359)], portes=4, reservoir=70, remarques=NA)
mg(L, "Malibu", "9e gén.", "1", "2016-01", "2024-11", [("1.5 Turbo 165", "GM-1.5T", 250), ("2.0 Turbo 253", "GM-2.0T", 353, {"fin": "2022-12"})], portes=4, reservoir=60,
   remarques=NA + " ; fin de production novembre 2024")
mg(L, "Cruze", "J400", "1", "2016-01", "2019-03", [("1.4 Turbo 155", "ECOTEC-1.4T", 240), ("1.6 Diesel 139", "VCDI-1.7", 325, {"debut": "2017-01"})], portes=4, reservoir=52, remarques=NA)
mg(L, "Spark", "M400", "1", "2016-01", "2022-08", [("1.4 99", "ETEC-1.4", 127)], reservoir=34, remarques=NA)
mg(L, "Bolt EV", "BEV2", "1", "2017-01", "2023-12", [("Bolt EV 203", "GM-EV-BOLT", 360, el(60)), ("Bolt EV 65 kWh 203", "GM-EV-BOLT", 360, el(65, debut="2020-01")),
                                                     ("Bolt EUV 203", "GM-EV-BOLT", 360, el(65, debut="2022-01"))], reservoir=0, remarques=NA + " ; vendue Opel Ampera-e en Europe")
mg(L, "Bolt", "BEV2", "2", "2026-01", "2027-06", [("Bolt 213", "ULTIUM", 229, el(65))], reservoir=0,
   remarques=NA + " ; série limitée (Fairfax, Kansas) ; fin de production prévue mi-2027")

# ---------------------------------------------------------------- Amérique du Nord : SUV / pick-up
mg(L, "Trax", "GB", "2", "2024-01", None, [("1.2 Turbo 139", "GM-1.2T", 236)], reservoir=50, remarques=NA + " ; produit en Corée du Sud")
mg(L, "Equinox", "D2XX", "1", "2018-01", "2024-06", [("1.5 Turbo 172", "GM-1.5T", 275), ("2.0 Turbo 256", "GM-2.0T", 353, {"fin": "2020-12"}), ("1.6 Diesel 139", "VCDI-1.7", 325, {"fin": "2019-12"})],
   reservoir=56, remarques=NA)
mg(L, "Equinox", "D2UX", "1", "2024-07", None, [("1.5 Turbo 177", "GM-1.5T", 275)], reservoir=56, remarques=NA + " ; 4e génération (millésime 2025)")
mg(L, "Equinox EV", "BEV3", "E", "2024-01", None, [("FWD 216", "ULTIUM", 328, el(85)), ("AWD 304", "ULTIUM", 437, el(85))], reservoir=0, remarques=NA)
mg(L, "Blazer", "C1XX", "B", "2019-01", None, [("2.5 196", "GM-2.5", 255, {"fin": "2022-12"}), ("2.0 Turbo 233", "GM-2.0T", 350), ("3.6 V6 312", "GM-3.6-V6", 365)], reservoir=82,
   remarques=NA + " ; restylage 2023")
mg(L, "Blazer EV", "BEV3", "B", "2024-01", None, [("RWD 345", "ULTIUM", 440, el(85)), ("AWD 293", "ULTIUM", 441, el(85)), ("SS 624", "ULTIUM", 880, el(102, debut="2025-01"))],
   reservoir=0, remarques=NA)
mg(L, "Traverse", "C1XX", "T", "2018-01", "2023-12", [("3.6 V6 314", "GM-3.6-V6", 361), ("2.0 Turbo 260", "GM-2.0T", 400, {"fin": "2020-12"})], places=8, reservoir=73, remarques=NA)
mg(L, "Traverse", "C1XX", "2", "2024-01", None, [("2.5 Turbo 333", "GM-2.5T", 441)], places=8, reservoir=82, remarques=NA + " ; 3e génération")
mg(L, "Tahoe", "T1XX", "1", "2021-01", None, [("5.3 V8 360", "L84-5.3", 519), ("6.2 V8 426", "L87-6.2", 623), ("3.0 Duramax 309", "DURAMAX-3.0", 678)], places=8, reservoir=91,
   remarques=NA + " ; restylage 2025 ; générations antérieures non détaillées")
mg(L, "Suburban", "T1XX", "S", "2021-01", None, [("5.3 V8 360", "L84-5.3", 519), ("6.2 V8 426", "L87-6.2", 623), ("3.0 Duramax 309", "DURAMAX-3.0", 678)], places=8, reservoir=106,
   remarques=NA + " ; restylage 2025")
mg(L, "Colorado", "GMT700", "2", "2015-01", "2022-12", [("2.5 203", "GM-2.5", 259), ("3.6 V6 312", "GM-3.6-V6", 373), ("2.8 Duramax 184", "DURAMAX-2.8", 500, {"debut": "2016-01"})],
   portes=4, reservoir=79, remarques=NA)
mg(L, "Colorado", "31XX", "1", "2023-01", None, [("2.7 Turbo 240", "GM-2.7T", 352), ("2.7 Turbo 314", "GM-2.7T", 583)], portes=4, reservoir=80, remarques=NA + " ; ZR2")
mg(L, "Silverado", "T1XX", "P", "2019-01", None,
   [("2.7 Turbo 314", "GM-2.7T", 583), ("5.3 V8 360", "L84-5.3", 519), ("6.2 V8 426", "L87-6.2", 623), ("3.0 Duramax 309", "DURAMAX-3.0", 678)], portes=4, reservoir=91,
   remarques=NA + " ; 1500 ; restylage 2022 ; générations antérieures non détaillées")
mg(L, "Silverado EV", "BT1", "1", "2024-01", None, [("WT 517", "ULTIUM", 834, el(200)), ("RST 765", "ULTIUM", 1063, el(200))], portes=4, reservoir=0, remarques=NA + " ; " + IND)

# ---------------------------------------------------------------- Chevrolet Corvette
mg(LC, "Corvette", "C1", "1", "1953-06", "1962-12", [("3.9 I6 152", "STOVEBOLT-3.9", 290, {"fin": "1955-12"}), ("4.3 V8 198", "SBC-4.3", 351, {"debut": "1955-01", "fin": "1956-12"}),
                                                    ("4.6 V8 223", "SBC-4.6", 366, {"debut": "1957-01", "fin": "1961-12"}), ("5.4 V8 365", "SBC-5.4", 475, {"debut": "1962-01"})],
   portes=2, places=2, reservoir=64, remarques="Roadster ; " + IND)
mg(LC, "Corvette", "C2", "1", "1963-01", "1967-12", [("Sting Ray 5.4 V8 304", "SBC-5.4", 488), ("Sting Ray 7.0 V8 441", "BBC-7.0", 624, {"debut": "1966-01"})],
   portes=2, places=2, reservoir=76, remarques="Coupé et cabriolet ; " + IND)
mg(LC, "Corvette", "C3", "1", "1968-01", "1982-12", [("5.7 V8 304", "SBC-5.7", 488, {"fin": "1972-12"}), ("7.4 V8 395", "BBC-7.4", 610, {"fin": "1974-12"}),
                                                    ("5.7 V8 208", "SBC-5.7", 380, {"debut": "1975-01"})], portes=2, places=2, reservoir=76, remarques="Coupé T-top et cabriolet ; " + IND)
mg(LC, "Corvette", "C4", "1", "1984-01", "1996-12", [("5.7 V8 248", "L98-5.7", 461, {"fin": "1991-12"}), ("5.7 V8 LT1 304", "LT1-5.7", 461, {"debut": "1992-01"}),
                                                    ("Grand Sport 5.7 V8 LT4 335", "LT1-5.7", 461, {"debut": "1996-01"}), ("ZR-1 5.7 V8 LT5 380", "LT5-5.7", 502, {"debut": "1990-01", "fin": "1995-12"})],
   portes=2, places=2, reservoir=76, remarques="Coupé et cabriolet ; " + IND)
mg(LC, "Corvette", "C5", "1", "1997-01", "2004-12", [("5.7 V8 350", "LS1-5.7", 475), ("Z06 5.7 V8 390", "LS6-5.7", 522, {"debut": "2001-01", "fin": "2001-12"}),
                                                    ("Z06 5.7 V8 411", "LS6-5.7", 542, {"debut": "2002-01"})], portes=2, places=2, reservoir=72, remarques="Coupé, cabriolet, hardtop")
mg(LC, "Corvette", "C6", "1", "2005-01", "2013-12",
   [("6.0 V8 405", "LS2-6.0", 542, {"fin": "2007-12"}), ("6.2 V8 437", "LS3-6.2", 575, {"debut": "2008-01"}), ("Z06 7.0 V8 512", "LS7-7.0", 637, {"debut": "2006-01"}),
    ("ZR1 6.2 V8 Compresseur 647", "LS9-6.2SC", 819, {"debut": "2009-01"})], portes=2, places=2, reservoir=68, remarques="Coupé et cabriolet ; aussi vendue en Europe")
mg(LC, "Corvette", "C7", "1", "2014-01", "2019-12", [("Stingray 6.2 V8 466", "LT1-6.2", 630), ("Z06 6.2 V8 Compresseur 659", "LT4-6.2SC", 881, {"debut": "2015-01"}),
                                                    ("ZR1 6.2 V8 Compresseur 766", "LT5-6.2SC", 969, {"debut": "2019-01"})], portes=2, places=2, reservoir=70, remarques="Coupé et cabriolet ; aussi vendue en Europe")
mg(LC, "Corvette", "C8", "1", "2020-01", None,
   [("Stingray 6.2 V8 502", "LT2-6.2", 637), ("Z06 5.5 V8 680", "LT6-5.5", 625, {"debut": "2023-01"}), ("E-Ray 664", "LT2-ERAY", 806, {"debut": "2024-01", "batterie": 2}),
    ("ZR1 5.5 V8 Biturbo 1079", "LT7-5.5TT", 1123, {"debut": "2025-01"}), ("ZR1X 5.5 V8 Biturbo Hybrid 1270", "LT7-5.5TT", 1123, {"debut": "2026-01"})],
   portes=2, places=2, reservoir=70, remarques="Moteur central ; coupé targa et cabriolet ; vendue en Europe ; ZR1X : puissance cumulée, " + IND)

# ---------------------------------------------------------------- Chevrolet Camaro ZL1
mg(LZ, "Camaro ZL1", "5e gén.", "1", "2012-01", "2015-12", [("ZL1 6.2 V8 Compresseur 588", "LSA-6.2SC", 754)], portes=2, places=4, reservoir=72, remarques=NA + " ; coupé et cabriolet")
mg(LZ, "Camaro ZL1", "6e gén.", "1", "2017-01", "2023-12", [("ZL1 6.2 V8 Compresseur 659", "LT4-6.2SC", 881), ("ZL1 1LE 6.2 V8 Compresseur 659", "LT4-6.2SC", 881, {"debut": "2018-01"})],
   portes=2, places=4, reservoir=72, remarques=NA + " ; coupé et cabriolet")

MOT = Motorisations("Chevrolet", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LC)
MOT.lier(LZ)

DETAIL = {"Chevrolet": L, "Chevrolet Corvette": LC, "Chevrolet Camaro ZL1": LZ}
MOTEURS = MOT.moteurs()
