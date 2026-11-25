"""Jaguar : générations, phases, motorisations (marché européen) et moteurs liés.
Jaguar : XK120/140/150, Mk VII-IX, Mk 1/Mk 2, Mk X/420G, S-Type (1963) et 420, E-Type, XJ (Series 1-3, XJ40, X300, X308, X350,
X351), XJ-S/XJS, XJ220, XK8 (X100), XK (X150), S-Type (X200), X-Type, XF (X250, X260), XE, F-Type, F-Pace, E-Pace, I-Pace, Type 01.
Jaguar R : XJR, XKR, XKR-S, S-Type R, XFR, XFR-S, XE SV Project 8, F-Type R, F-Type SVR, F-Pace SVR.
Production thermique arrêtée : XE/XF/F-Type mi-2024, E-Pace/I-Pace décembre 2024, F-Pace 19 décembre 2025.
Moteurs propres au motoriste « Jaguar » ; Duratorq et EcoBoost repris de ford.py (motoriste « Ford »).
Données des modèles anciens indicatives. Daimler (marque sœur) non reprise.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .ford import FAMILLES as FAMILLES_FORD

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

PROPRES = {
    # XK six en ligne et V12
    "XK-2.4": f("ATM", E_, 2.4, C, 6, 5750, 2000, "20W50", 7.5, 5000),
    "XK-2.8": f("ATM", E_, 2.8, C, 6, 6000, 3750, "20W50", 7.5, 5000),
    "XK-3.4": f("ATM", E_, 3.4, C, 6, 5500, 3000, "20W50", 7.5, 5000),
    "XK-3.8": f("ATM", E_, 3.8, C, 6, 5500, 3000, "20W50", 7.5, 5000),
    "XK-4.2": f("ATM", E_, 4.2, C, 6, 5400, 3000, "20W50", 7.5, 5000),
    "V12-5.3": f("ATM", E_, 5.3, C, 12, 5500, 3000, "20W50", 10.0, 10000, a="V"),
    "V12-6.0": f("ATM", E_, 6.0, C, 12, 5350, 3750, "10W40", 10.0, 10000, a="V"),
    # AJ6 / AJ16
    "AJ6-2.9": f("ATM", E_, 2.9, C, 6, 5600, 4000, "10W40", 7.5, 10000),
    "AJ6-3.2": f("ATM", E_, 3.2, C, 6, 5250, 4000, "10W40", 7.5, 10000),
    "AJ6-3.6": f("ATM", E_, 3.6, C, 6, 5000, 4000, "10W40", 7.5, 10000),
    "AJ6-4.0": f("ATM", E_, 4.0, C, 6, 4750, 3650, "10W40", 7.5, 10000),
    "AJ16-3.2": f("ATM", E_, 3.2, C, 6, 5100, 4500, "10W40", 7.5, 10000),
    "AJ16-4.0": f("ATM", E_, 4.0, C, 6, 4800, 4000, "10W40", 7.5, 10000),
    "AJ16-4.0S": f("TURBO", E_, 4.0, C, 6, 5000, 3050, "10W40", 7.5, 10000),
    # V8 AJ-V8 et V6
    "AJ26-3.2": f("ATM", E_, 3.2, C, 8, 6350, 4350, "5W30", 7.0, 16000, a="V"),
    "AJ26-4.0": f("ATM", E_, 4.0, C, 8, 6100, 4200, "5W30", 7.0, 16000, a="V"),
    "AJ26-4.0S": f("TURBO", E_, 4.0, C, 8, 6150, 3600, "5W30", 7.0, 16000, a="V"),
    "AJ-V8-3.5": f("ATM", E_, 3.5, C, 8, 6250, 4200, "5W30", 7.0, 16000, a="V"),
    "AJ-V8-4.2": f("ATM", E_, 4.2, C, 8, 6000, 4100, "5W30", 7.0, 16000, a="V"),
    "AJ-V8-4.2S": f("TURBO", E_, 4.2, C, 8, 6100, 3500, "5W30", 7.0, 16000, a="V"),
    "AJ133-5.0": f("ATM", E_, 5.0, C, 8, 6500, 3500, "0W20", 7.25, 16000, a="V"),
    "AJ133-5.0S": f("TURBO", E_, 5.0, C, 8, 6500, 2500, "0W20", 7.25, 16000, a="V"),
    "AJ126-3.0S": f("TURBO", E_, 3.0, C, 6, 6500, 3500, "0W20", 7.25, 16000, a="V"),
    "AJ-V6-2.0": f("ATM", E_, 2.0, C, 6, 6800, 4100, "5W30", 5.7, 16000, a="V"),
    "AJ-V6-2.5": f("ATM", E_, 2.5, C, 6, 6800, 3000, "5W30", 5.7, 16000, a="V"),
    "AJ-V6-3.0": f("ATM", E_, 3.0, C, 6, 6800, 4100, "5W30", 5.7, 16000, a="V"),
    "JRV6-3.5TT": f("TURBO", E_, 3.5, B, 6, 7000, 4500, "10W60", 9.0, 10000, a="V"),
    # diesels V6
    "AJD-V6-2.7": f("TURBO", D, 2.7, B, 6, 4000, 1900, "5W30", 6.0, 16000, a="V"),
    "AJV6D-3.0": f("TURBO", D, 3.0, B, 6, 4000, 2000, "0W30", 6.0, 16000, a="V"),
    # Ingenium
    "AJ200D": f("TURBO", D, 2.0, C, 4, 4000, 1750, "0W30", 6.0, 21000),
    "AJ200D-MHEV": f("HYB_E", D, 2.0, C, 4, 3750, 1750, "0W30", 6.0, 21000),
    "AJ300D-MHEV": f("HYB_E", D, 3.0, C, 6, 4000, 1500, "0W30", 7.0, 21000),
    "AJ200P": f("TURBO", E_, 2.0, C, 4, 5500, 1300, "0W20", 6.0, 21000),
    "AJ200P-MHEV": f("HYB_E", E_, 2.0, C, 4, 5500, 1300, "0W20", 6.0, 21000),
    "AJ200P-PHEV": f("HYB_E", E_, 2.0, C, 4, 5500, 1500, "0W20", 6.0, 21000),
    "AJ300P-MHEV": f("HYB_E", E_, 3.0, C, 6, 5500, 2000, "0W20", 7.0, 21000),
    "INGENIUM-1.5-PHEV": f("HYB_E", E_, 1.5, C, 3, 5500, 1600, "0W20", 5.0, 21000),
    "JAGUAR-EV": electrique(),
}
FORD = {k: FAMILLES_FORD[k] for k in ("DURATORQ-2.0", "DURATORQ-2.2", "ECOBOOST-2.0")}
FAMILLES = {**PROPRES, **FORD}


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Jaguar", lambda fam: "Ford" if fam in FORD else "Jaguar")
L = []

# ---------------------------------------------------------------- classiques
mg(L, "XK120", "XK120", "1", "1948-10", "1954-09", [("3.4 160", "XK-3.4", 264)], portes=2, places=2, reservoir=68,
   remarques="Roadster, coupé (1951), drophead (1953) ; données indicatives")
mg(L, "XK140", "XK140", "1", "1954-10", "1957-02", [("3.4 190", "XK-3.4", 284)], portes=2, places=2, reservoir=64, remarques="Données indicatives")
mg(L, "XK150", "XK150", "1", "1957-05", "1961-10", [("3.4 210", "XK-3.4", 292), ("3.8 S 265", "XK-3.8", 353, {"debut": "1959-10"})], portes=2, places=2,
   reservoir=64, remarques="Données indicatives")
mg(L, "Mk VII", "Mk VII", "1", "1951-10", "1961-09",
   [("Mk VII 3.4 162", "XK-3.4", 264, {"fin": "1956-12"}), ("Mk VIII 3.4 213", "XK-3.4", 292, {"debut": "1956-10", "fin": "1959-12"}),
    ("Mk IX 3.8 223", "XK-3.8", 325, {"debut": "1958-10"})], portes=4, reservoir=77, remarques="Mk VII, VIII et IX ; données indicatives")
mg(L, "Mk 2", "Mk 1", "1", "1955-09", "1959-09", [("2.4 113", "XK-2.4", 190), ("3.4 213", "XK-3.4", 292, {"debut": "1957-02"})], portes=4, reservoir=55,
   remarques="« 2.4 Litre » et « 3.4 Litre » (Mk 1) ; données indicatives")
mg(L, "Mk 2", "Mk 2", "1", "1959-10", "1969-09",
   [("2.4 122", "XK-2.4", 194), ("3.4 213", "XK-3.4", 292), ("3.8 223", "XK-3.8", 325, {"fin": "1967-09"})], portes=4, reservoir=55,
   remarques="240 et 340 à partir de 1967 ; données indicatives")
mg(L, "S-Type", "S-Type 1963", "1", "1963-10", "1968-06", [("3.4 213", "XK-3.4", 292), ("3.8 223", "XK-3.8", 325)], portes=4, reservoir=64,
   remarques="Mk 2 à suspension arrière indépendante ; dérivée en 420 (1966-1968, 4.2) ; données indicatives")
mg(L, "Mk X", "Mk X", "1", "1961-10", "1970-06",
   [("3.8 269", "XK-3.8", 353, {"fin": "1964-09"}), ("4.2 269", "XK-4.2", 384, {"debut": "1964-10"})], portes=4, reservoir=91,
   remarques="Renommée 420G en 1966 ; données indicatives")
mg(L, "E-Type", "Series 1", "1", "1961-03", "1968-08",
   [("3.8 269", "XK-3.8", 353, {"fin": "1964-09"}), ("4.2 269", "XK-4.2", 384, {"debut": "1964-10"})], portes=2, places=2, reservoir=64,
   remarques="Roadster et coupé, 2+2 (1966) ; données indicatives")
mg(L, "E-Type", "Series 2", "1", "1968-09", "1971-03", [("4.2 269", "XK-4.2", 384)], portes=2, places=2, reservoir=64, remarques="Données indicatives")
mg(L, "E-Type", "Series 3", "1", "1971-03", "1975-02", [("5.3 V12 276", "V12-5.3", 412)], portes=2, places=2, reservoir=82,
   remarques="Roadster et 2+2 ; données indicatives")

# ---------------------------------------------------------------- XJ
mg(L, "XJ", "Series 1", "1", "1968-09", "1973-08",
   [("XJ6 2.8 182", "XK-2.8", 247), ("XJ6 4.2 248", "XK-4.2", 384), ("XJ12 5.3 V12 256", "V12-5.3", 412, {"debut": "1972-07"})], portes=4, reservoir=91,
   remarques="Données indicatives")
mg(L, "XJ", "Series 2", "1", "1973-09", "1979-02",
   [("XJ6 3.4 163", "XK-3.4", 258, {"debut": "1975-04"}), ("XJ6 4.2 173", "XK-4.2", 315), ("XJ12 5.3 V12 289", "V12-5.3", 400)], portes=4, reservoir=91,
   remarques="Berline et coupé XJC (1975-1977) ; données indicatives")
mg(L, "XJ", "Series 3", "1", "1979-03", "1992-11",
   [("XJ6 3.4 163", "XK-3.4", 258, {"fin": "1987-06"}), ("XJ6 4.2 205", "XK-4.2", 314, {"fin": "1987-06"}), ("XJ12 5.3 V12 HE 299", "V12-5.3", 432)],
   portes=4, reservoir=91, remarques="XJ12 seule à partir de 1987 ; données indicatives")
mg(L, "XJ", "XJ40", "1", "1986-10", "1994-09",
   [("2.9 165", "AJ6-2.9", 239, {"fin": "1990-08"}), ("3.6 221", "AJ6-3.6", 337, {"fin": "1989-09"}), ("3.2 200", "AJ6-3.2", 298, {"debut": "1990-09"}),
    ("4.0 223", "AJ6-4.0", 377, {"debut": "1989-10"}), ("XJ12 6.0 V12 318", "V12-6.0", 478, {"debut": "1993-03"})], portes=4, reservoir=88)
mg(L, "XJ", "X300", "1", "1994-10", "1997-08",
   [("3.2 219", "AJ16-3.2", 315), ("4.0 249", "AJ16-4.0", 392), ("XJ12 6.0 V12 318", "V12-6.0", 478)], portes=4, reservoir=81, remarques="Empattement long disponible")
mg(L, "XJ", "X308", "1", "1997-09", "2003-02", [("3.2 V8 243", "AJ26-3.2", 316), ("4.0 V8 284", "AJ26-4.0", 375)], portes=4, reservoir=81)
mg(L, "XJ", "X350", "1", "2003-03", "2009-06",
   [("3.0 V6 243", "AJ-V6-3.0", 300), ("3.5 V8 262", "AJ-V8-3.5", 345), ("4.2 V8 298", "AJ-V8-4.2", 411), ("2.7d V6 207", "AJD-V6-2.7", 435, {"debut": "2005-03"}),
    ("Super V8 4.2 V8 SC 400", "AJ-V8-4.2S", 553)], portes=4, reservoir=85, remarques="Caisse aluminium ; restylage X358 (2007)")
mg(L, "XJ", "X351", "1", "2009-11", "2015-08",
   [("3.0d V6 275", "AJV6D-3.0", 600), ("5.0 V8 385", "AJ133-5.0", 515, {"fin": "2012-12"}), ("5.0 V8 SC 470", "AJ133-5.0S", 575),
    ("Supersport 5.0 V8 SC 510", "AJ133-5.0S", 625), ("3.0 V6 SC 340", "AJ126-3.0S", 450, {"debut": "2012-06"}),
    ("2.0 i4 240", "ECOBOOST-2.0", 340, {"debut": "2012-06"})], portes=4, reservoir=82, remarques="Empattement long disponible")
mg(L, "XJ", "X351", "2", "2015-09", "2019-07",
   [("3.0d V6 300", "AJV6D-3.0", 700), ("3.0 V6 SC 340", "AJ126-3.0S", 450), ("5.0 V8 SC 470", "AJ133-5.0S", 575)], portes=4, reservoir=82,
   remarques="Restylage ; production arrêtée en juillet 2019")

# ---------------------------------------------------------------- GT et sportives
mg(L, "XJ-S", "XJ-S", "1", "1975-09", "1991-04",
   [("5.3 V12 289", "V12-5.3", 400, {"fin": "1981-06"}), ("5.3 V12 HE 299", "V12-5.3", 432, {"debut": "1981-07"}),
    ("3.6 228", "AJ6-3.6", 325, {"debut": "1983-10"})], portes=2, places=4, reservoir=82, remarques="Coupé, cabriolet (1983) et convertible (1988)")
mg(L, "XJ-S", "XJS", "1", "1991-05", "1996-04",
   [("4.0 223", "AJ6-4.0", 375, {"fin": "1994-04"}), ("4.0 241", "AJ16-4.0", 382, {"debut": "1994-05"}), ("5.3 V12 280", "V12-5.3", 420, {"fin": "1993-04"}),
    ("6.0 V12 308", "V12-6.0", 481, {"debut": "1993-05"})], portes=2, places=4, reservoir=89, remarques="Restylage (XJS)")
mg(L, "XJ220", "XJ220", "1", "1992-06", "1994-06", [("3.5 V6 Biturbo 550", "JRV6-3.5TT", 642)], portes=2, places=2, reservoir=90,
   remarques="281 exemplaires")
mg(L, "XK", "X100", "1", "1996-10", "2002-06", [("XK8 4.0 V8 284", "AJ26-4.0", 375)], portes=2, places=4, reservoir=75, remarques="Coupé et cabriolet")
mg(L, "XK", "X100", "2", "2002-07", "2006-02", [("XK8 4.2 V8 298", "AJ-V8-4.2", 411)], portes=2, places=4, reservoir=75)
mg(L, "XK", "X150", "1", "2006-03", "2009-02", [("4.2 V8 298", "AJ-V8-4.2", 411)], portes=2, places=4, reservoir=71, remarques="Coupé et cabriolet, caisse aluminium")
mg(L, "XK", "X150", "2", "2009-03", "2014-07", [("5.0 V8 385", "AJ133-5.0", 515)], portes=2, places=4, reservoir=71, remarques="Restylage")
mg(L, "F-Type", "X152", "1", "2013-04", "2017-02",
   [("3.0 V6 SC 340", "AJ126-3.0S", 450), ("S 3.0 V6 SC 380", "AJ126-3.0S", 460), ("V8 S 5.0 V8 SC 495", "AJ133-5.0S", 625, {"fin": "2015-06"})],
   portes=2, places=2, reservoir=70, remarques="Cabriolet, coupé (2014) ; AWD (2015)")
mg(L, "F-Type", "X152", "2", "2017-03", "2019-12",
   [("2.0 P300 300", "AJ200P", 400, {"debut": "2017-06"}), ("3.0 V6 SC 340", "AJ126-3.0S", 450), ("S 3.0 V6 SC 380", "AJ126-3.0S", 460),
    ("400 Sport 3.0 V6 SC 400", "AJ126-3.0S", 460, {"debut": "2017-06", "fin": "2018-06"})], portes=2, places=2, reservoir=70)
mg(L, "F-Type", "X152", "3", "2020-01", "2024-06",
   [("P300 2.0 300", "AJ200P", 400), ("P380 3.0 V6 SC 380", "AJ126-3.0S", 460, {"fin": "2021-12"}), ("P450 5.0 V8 SC 450", "AJ133-5.0S", 580)],
   portes=2, places=2, reservoir=70, remarques="Restylage ; production arrêtée mi-2024 (87 731 exemplaires)")

# ---------------------------------------------------------------- berlines modernes
mg(L, "S-Type", "X200", "1", "1999-01", "2002-03", [("3.0 V6 238", "AJ-V6-3.0", 293), ("4.0 V8 281", "AJ26-4.0", 393)], portes=4, reservoir=69)
mg(L, "S-Type", "X200", "2", "2002-04", "2007-12",
   [("2.5 V6 201", "AJ-V6-2.5", 250), ("3.0 V6 238", "AJ-V6-3.0", 300), ("4.2 V8 298", "AJ-V8-4.2", 411), ("2.7d V6 207", "AJD-V6-2.7", 435, {"debut": "2004-03"})],
   portes=4, reservoir=69, remarques="Restylage (2004)")
mg(L, "X-Type", "X400", "1", "2001-06", "2009-12",
   [("2.0 V6 157", "AJ-V6-2.0", 196, {"debut": "2002-03", "fin": "2007-12"}), ("2.5 V6 196", "AJ-V6-2.5", 244), ("3.0 V6 231", "AJ-V6-3.0", 284, {"fin": "2008-06"}),
    ("2.0d 130", "DURATORQ-2.0", 330, {"debut": "2003-06"}), ("2.2d 155", "DURATORQ-2.2", 360, {"debut": "2005-06"})], portes=4, reservoir=61,
   remarques="Berline et break Estate (2004) ; restylage 2008")
mg(L, "XF", "X250", "1", "2008-03", "2011-04",
   [("3.0 V6 238", "AJ-V6-3.0", 293), ("4.2 V8 298", "AJ-V8-4.2", 411, {"fin": "2009-06"}), ("2.7d V6 207", "AJD-V6-2.7", 435, {"fin": "2009-06"}),
    ("3.0d V6 240", "AJV6D-3.0", 500, {"debut": "2009-06"}), ("3.0d S V6 275", "AJV6D-3.0", 600, {"debut": "2009-06"}),
    ("5.0 V8 385", "AJ133-5.0", 515, {"debut": "2009-06"})], portes=4, reservoir=70)
mg(L, "XF", "X250", "2", "2011-05", "2015-08",
   [("2.2d 163", "DURATORQ-2.2", 400, {"debut": "2012-06"}), ("2.2d 190", "DURATORQ-2.2", 450), ("2.2d 200", "DURATORQ-2.2", 450, {"debut": "2014-06"}),
    ("3.0d V6 240", "AJV6D-3.0", 500), ("3.0d S V6 275", "AJV6D-3.0", 600), ("2.0 i4 240", "ECOBOOST-2.0", 340, {"debut": "2012-06"}),
    ("3.0 V6 SC 340", "AJ126-3.0S", 450, {"debut": "2012-06"})], portes=4, reservoir=70, remarques="Restylage ; Sportbrake (2012)")
mg(L, "XF", "X260", "1", "2015-09", "2020-09",
   [("2.0d 163", "AJ200D", 380), ("2.0d 180", "AJ200D", 430), ("2.0d 240", "AJ200D", 500, {"debut": "2017-06"}), ("3.0d V6 300", "AJV6D-3.0", 700),
    ("P250 2.0 250", "AJ200P", 365, {"debut": "2017-06"}), ("P300 2.0 AWD 300", "AJ200P", 400, {"debut": "2018-06"}), ("S 3.0 V6 SC 380", "AJ126-3.0S", 450)],
   portes=4, reservoir=74, remarques="Sportbrake (2017)")
mg(L, "XF", "X260", "2", "2020-10", "2024-06",
   [("D200 2.0 MHEV 204", "AJ200D-MHEV", 430), ("P250 2.0 250", "AJ200P", 365), ("P300 2.0 AWD 300", "AJ200P", 400)], portes=4, reservoir=74,
   remarques="Restylage ; production arrêtée mi-2024")
mg(L, "XE", "X760", "1", "2015-04", "2019-03",
   [("2.0d 163", "AJ200D", 380), ("2.0d 180", "AJ200D", 430), ("2.0d 240", "AJ200D", 500, {"debut": "2017-06"}), ("P200 2.0 200", "AJ200P", 320, {"debut": "2017-06"}),
    ("P250 2.0 250", "AJ200P", 365, {"debut": "2017-06"}), ("P300 2.0 AWD 300", "AJ200P", 400, {"debut": "2018-06"}), ("S 3.0 V6 SC 380", "AJ126-3.0S", 450)],
   portes=4, reservoir=56)
mg(L, "XE", "X760", "2", "2019-04", "2024-06",
   [("D180 2.0 180", "AJ200D", 430, {"fin": "2020-09"}), ("D200 2.0 MHEV 204", "AJ200D-MHEV", 430, {"debut": "2020-10"}), ("P250 2.0 250", "AJ200P", 365),
    ("P300 2.0 AWD 300", "AJ200P", 400)], portes=4, reservoir=56, remarques="Restylage ; production arrêtée mi-2024")

# ---------------------------------------------------------------- SUV et électriques
mg(L, "F-Pace", "X761", "1", "2016-04", "2020-09",
   [("2.0d 163", "AJ200D", 380), ("2.0d 180", "AJ200D", 430), ("2.0d 240", "AJ200D", 500, {"debut": "2017-06"}), ("3.0d V6 300", "AJV6D-3.0", 700),
    ("P250 2.0 250", "AJ200P", 365, {"debut": "2017-06"}), ("P300 2.0 AWD 300", "AJ200P", 400, {"debut": "2018-06"}), ("S 3.0 V6 SC 380", "AJ126-3.0S", 450)],
   reservoir=66)
mg(L, "F-Pace", "X761", "2", "2020-10", "2025-12",
   [("D200 2.0 MHEV 204", "AJ200D-MHEV", 430), ("D300 3.0 MHEV 300", "AJ300D-MHEV", 650), ("P250 2.0 250", "AJ200P", 365),
    ("P400 3.0 MHEV 400", "AJ300P-MHEV", 550), ("P400e 2.0 PHEV 404", "AJ200P-PHEV", 640, {"batterie": 17})], reservoir=69,
   remarques="Restylage ; dernier exemplaire produit le 19 décembre 2025 (fin des Jaguar thermiques)")
mg(L, "E-Pace", "X540", "1", "2017-06", "2020-09",
   [("D150 2.0 150", "AJ200D", 380), ("D180 2.0 180", "AJ200D", 430), ("D240 2.0 240", "AJ200D", 500), ("P200 2.0 200", "AJ200P", 320, {"debut": "2018-06"}),
    ("P250 2.0 250", "AJ200P", 365), ("P300 2.0 AWD 300", "AJ200P", 400)], reservoir=69, remarques="Produit à Graz (Magna Steyr)")
mg(L, "E-Pace", "X540", "2", "2020-10", "2024-12",
   [("D165 2.0 MHEV 163", "AJ200D-MHEV", 380), ("D200 2.0 MHEV 204", "AJ200D-MHEV", 430), ("P200 2.0 MHEV 200", "AJ200P-MHEV", 320),
    ("P250 2.0 MHEV 249", "AJ200P-MHEV", 365), ("P300e 1.5 PHEV 309", "INGENIUM-1.5-PHEV", 540, {"batterie": 15})], reservoir=65,
   remarques="Restylage ; production arrêtée en décembre 2024")
mg(L, "I-Pace", "X590", "1", "2018-06", "2020-09", [("EV400 400", "JAGUAR-EV", 696, el(90))], reservoir=0, remarques="Produit à Graz (Magna Steyr)")
mg(L, "I-Pace", "X590", "2", "2020-10", "2024-12", [("EV400 400", "JAGUAR-EV", 696, el(90))], reservoir=0,
   remarques="Mise à jour (chargeur 11 kW, Pivi Pro) ; production arrêtée en décembre 2024")
mg(L, "Type 01", "Type 01", "1", "2027-06", None, [("Tri-moteur AWD 1030", "JAGUAR-EV", 1365, el(118))], portes=4, places=4, reservoir=0,
   remarques="GT électrique 850 V sur plateforme JEA, présentée en octobre 2026 ; premières livraisons prévues à l'été 2027, date indicative")

# ---------------------------------------------------------------- Jaguar R
LR = []
mg(LR, "XJR", "X300", "1", "1994-10", "1997-08", [("XJR 4.0 SC 326", "AJ16-4.0S", 512)], portes=4, reservoir=81)
mg(LR, "XJR", "X308", "1", "1997-09", "2003-02", [("XJR 4.0 V8 SC 370", "AJ26-4.0S", 525)], portes=4, reservoir=81)
mg(LR, "XJR", "X350", "1", "2003-03", "2009-06", [("XJR 4.2 V8 SC 400", "AJ-V8-4.2S", 553)], portes=4, reservoir=85)
mg(LR, "XJR", "X351", "1", "2013-06", "2017-06", [("XJR 5.0 V8 SC 550", "AJ133-5.0S", 680)], portes=4, reservoir=82)
mg(LR, "XJR", "X351", "2", "2017-07", "2019-07", [("XJR575 5.0 V8 SC 575", "AJ133-5.0S", 700)], portes=4, reservoir=82)
mg(LR, "XKR", "X100", "1", "1998-03", "2002-06", [("XKR 4.0 V8 SC 370", "AJ26-4.0S", 525)], portes=2, places=4, reservoir=75)
mg(LR, "XKR", "X100", "2", "2002-07", "2006-02", [("XKR 4.2 V8 SC 400", "AJ-V8-4.2S", 553)], portes=2, places=4, reservoir=75)
mg(LR, "XKR", "X150", "1", "2007-01", "2009-02", [("XKR 4.2 V8 SC 416", "AJ-V8-4.2S", 560)], portes=2, places=4, reservoir=71)
mg(LR, "XKR", "X150", "2", "2009-03", "2014-07", [("XKR 5.0 V8 SC 510", "AJ133-5.0S", 625)], portes=2, places=4, reservoir=71)
mg(LR, "XKR-S", "X150", "1", "2011-06", "2014-07", [("XKR-S 5.0 V8 SC 550", "AJ133-5.0S", 680)], portes=2, places=4, reservoir=71,
   remarques="Coupé puis cabriolet (2012) ; XKR-S GT (2013)")
mg(LR, "S-Type R", "X200", "1", "2002-04", "2007-12", [("S-Type R 4.2 V8 SC 400", "AJ-V8-4.2S", 553)], portes=4, reservoir=69)
mg(LR, "XFR", "X250", "1", "2009-06", "2015-08", [("XFR 5.0 V8 SC 510", "AJ133-5.0S", 625)], portes=4, reservoir=70)
mg(LR, "XFR-S", "X250", "1", "2013-03", "2015-08", [("XFR-S 5.0 V8 SC 550", "AJ133-5.0S", 680)], portes=4, reservoir=70, remarques="Sportbrake XFR-S (2014)")
mg(LR, "XE SV Project 8", "X760", "1", "2017-09", "2019-12", [("Project 8 5.0 V8 SC 600", "AJ133-5.0S", 700)], portes=4, reservoir=56,
   remarques="300 exemplaires, Jaguar SVO")
mg(LR, "F-Type R", "X152", "1", "2014-06", "2019-12", [("R 5.0 V8 SC 550", "AJ133-5.0S", 680)], portes=2, places=2, reservoir=70, remarques="AWD à partir de 2015")
mg(LR, "F-Type R", "X152", "3", "2020-01", "2024-06", [("R 5.0 V8 SC 575", "AJ133-5.0S", 700)], portes=2, places=2, reservoir=70,
   remarques="Restylage ; série finale R 75 (2023)")
mg(LR, "F-Type SVR", "X152", "1", "2016-06", "2019-12", [("SVR 5.0 V8 SC 575", "AJ133-5.0S", 700)], portes=2, places=2, reservoir=70)
mg(LR, "F-Pace SVR", "X761", "1", "2019-01", "2020-09", [("SVR 5.0 V8 SC 550", "AJ133-5.0S", 680)], reservoir=82)
mg(LR, "F-Pace SVR", "X761", "2", "2020-10", "2025-12", [("SVR 5.0 V8 SC 550", "AJ133-5.0S", 700)], reservoir=82,
   remarques="Restylage ; le dernier F-Pace produit (décembre 2025) est un SVR")

MOT = Motorisations("Jaguar", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LR)

DETAIL = {"Jaguar": L, "Jaguar R": LR}
MOTEURS = MOT.moteurs()
