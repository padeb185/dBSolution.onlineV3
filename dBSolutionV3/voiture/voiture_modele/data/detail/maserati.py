"""Maserati : générations, phases, motorisations (marché européen) et moteurs liés.
A6 1500, A6G 2000, 3500 GT, 5000 GT, Mistral, Quattroporte (I, IV, V, VI), Mexico, Ghibli (I, II, M157), Indy, Bora, Merak,
Khamsin, Kyalami, Biturbo, 228, Karif, Shamal, 3200 GT, Coupé/Spyder, GranSport, MC12, GranTurismo, GranCabrio, Levante,
Grecale, MC20, MCPura, GT2 Stradale.
Moteurs Maserati au motoriste « Maserati » ; moteurs construits par Ferrari (F136, F154, F160, F140) au motoriste « Ferrari » ;
diesel VM repris de chrysler.py (« Chrysler ») ; V6 C114 repris de ligier.py. Données anciennes indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .chrysler import FAMILLES as FAMILLES_CHRYSLER
from .ligier import FAMILLES as FAMILLES_LIGIER

E_ = "ESS"
C, B = "CHAINE", "COURROIE"

MASERATI = {
    "MASERATI-I6-1.5": f("ATM", E_, 1.5, C, 6, 5500, 3500, "20W50", 6.0, 3000),
    "MASERATI-I6-2.0": f("ATM", E_, 2.0, C, 6, 6000, 4000, "20W50", 6.0, 3000),
    "MASERATI-I6-3.5": f("ATM", E_, 3.5, C, 6, 5500, 4000, "20W50", 9.0, 5000),
    "MASERATI-I6-4.0": f("ATM", E_, 4.0, C, 6, 5500, 4000, "20W50", 9.0, 5000),
    "MASERATI-V8-4.2": f("ATM", E_, 4.2, C, 8, 5500, 4000, "20W50", 11.0, 5000, a="V"),
    "MASERATI-V8-4.7": f("ATM", E_, 4.7, C, 8, 5500, 4000, "20W50", 11.0, 5000, a="V"),
    "MASERATI-V8-4.9": f("ATM", E_, 4.9, C, 8, 5500, 4000, "20W50", 11.0, 5000, a="V"),
    "MASERATI-V8-5.0": f("ATM", E_, 5.0, C, 8, 6000, 4500, "20W50", 11.0, 5000, a="V"),
    "MASERATI-V6-2.0": f("ATM", E_, 2.0, C, 6, 7000, 5000, "20W50", 7.0, 5000, a="V"),
    "MASERATI-V6-2.0BT": f("TURBO", E_, 2.0, C, 6, 6000, 4000, "10W40", 7.0, 7500, a="V"),
    "MASERATI-V6-2.5BT": f("TURBO", E_, 2.5, C, 6, 5500, 3000, "10W40", 7.0, 7500, a="V"),
    "MASERATI-V6-2.8BT": f("TURBO", E_, 2.8, C, 6, 6000, 3500, "10W40", 7.0, 7500, a="V"),
    "MASERATI-V8-3.2BT": f("TURBO", E_, 3.2, C, 8, 6250, 4500, "10W60", 9.0, 7500, a="V"),
    "NETTUNO-3.0": f("TURBO", E_, 3.0, C, 6, 7500, 3000, "0W40", 7.0, 15000, a="V"),
    "GME-2.0T-MHEV": f("HYB_E", E_, 2.0, C, 4, 5750, 2250, "0W30", 5.5, 15000),
    "FOLGORE-EV": electrique(),
}
FERRARI = {
    "F136-4.2": f("ATM", E_, 4.2, C, 8, 7000, 4500, "10W60", 9.0, 15000, a="V"),
    "F136-4.7": f("ATM", E_, 4.7, C, 8, 7000, 4750, "10W60", 9.0, 15000, a="V"),
    "F154-3.8": f("TURBO", E_, 3.8, C, 8, 6500, 2250, "5W40", 9.0, 15000, a="V"),
    "F160-3.0TT": f("TURBO", E_, 3.0, C, 6, 5750, 1750, "5W40", 7.0, 15000, a="V"),
    "F140-6.0": f("ATM", E_, 6.0, C, 12, 7500, 5500, "10W60", 15.0, 10000, a="V"),
}
AUTRES = {"VM-3.0CRD": FAMILLES_CHRYSLER["VM-3.0CRD"], **{k: FAMILLES_LIGIER[k] for k in ("MASERATI-C114-2.7", "MASERATI-C114-3.0")}}
FAMILLES = {**MASERATI, **FERRARI, **AUTRES}


def motoriste(fam):
    if fam in FERRARI:
        return "Ferrari"
    if fam == "VM-3.0CRD":
        return "Chrysler"
    return "Maserati"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Maserati", motoriste)
L = []

# ---------------------------------------------------------------- années 1940-1970
mg(L, "A6 1500", "A6", "1", "1947-03", "1950-12", [("1.5 I6 66", "MASERATI-I6-1.5", 98)], portes=2, places=2, reservoir=80,
   remarques="Première Maserati de route, carrosserie Pinin Farina ; données indicatives")
mg(L, "A6G 2000", "A6G", "1", "1950-01", "1957-12", [("2.0 I6 101", "MASERATI-I6-2.0", 147, {"fin": "1953-12"}), ("A6G/54 2.0 I6 152", "MASERATI-I6-2.0", 170, {"debut": "1954-01"})],
   portes=2, places=2, reservoir=80, remarques="Carrosseries Frua, Zagato, Allemano ; données indicatives")
mg(L, "3500 GT", "3500 GT", "1", "1957-03", "1964-12", [("3.5 I6 223", "MASERATI-I6-3.5", 340), ("3500 GTi 3.5 I6 238", "MASERATI-I6-3.5", 350, {"debut": "1961-01"})],
   portes=2, places=4, reservoir=80, remarques="Coupé Touring et Spyder Vignale ; Sebring dérivée ; données indicatives")
mg(L, "5000 GT", "5000 GT", "1", "1959-10", "1965-12", [("5.0 V8 345", "MASERATI-V8-5.0", 490)], portes=2, places=4, reservoir=95,
   remarques="34 exemplaires ; données indicatives")
mg(L, "Mistral", "Mistral", "1", "1963-10", "1970-12", [("3.7 I6 248", "MASERATI-I6-3.5", 343), ("4.0 I6 258", "MASERATI-I6-4.0", 363, {"debut": "1966-01"})],
   portes=2, places=2, reservoir=90, remarques="Coupé et Spyder ; données indicatives (3.7 rattaché à la famille 3.5)")
mg(L, "Quattroporte I", "AM107", "1", "1963-10", "1969-12", [("4.1 V8 264", "MASERATI-V8-4.2", 363), ("4.7 V8 294", "MASERATI-V8-4.7", 392, {"debut": "1966-01"})],
   portes=4, places=5, reservoir=105, remarques="Données indicatives")
mg(L, "Mexico", "AM112", "1", "1966-10", "1972-12", [("4.2 V8 264", "MASERATI-V8-4.2", 363), ("4.7 V8 294", "MASERATI-V8-4.7", 392)], portes=2, places=4,
   reservoir=95, remarques="Données indicatives")
mg(L, "Ghibli I", "AM115", "1", "1967-03", "1973-12", [("4.7 V8 314", "MASERATI-V8-4.7", 397), ("SS 4.9 V8 340", "MASERATI-V8-4.9", 481, {"debut": "1970-01"})],
   portes=2, places=2, reservoir=100, remarques="Coupé Giugiaro et Spyder ; données indicatives")
mg(L, "Indy", "AM116", "1", "1969-01", "1975-12",
   [("4.2 V8 264", "MASERATI-V8-4.2", 363, {"fin": "1971-12"}), ("4.7 V8 294", "MASERATI-V8-4.7", 392, {"debut": "1970-01"}), ("4.9 V8 324", "MASERATI-V8-4.9", 470, {"debut": "1973-01"})],
   portes=2, places=4, reservoir=100, remarques="Données indicatives")
mg(L, "Bora", "AM117", "1", "1971-03", "1978-12", [("4.7 V8 314", "MASERATI-V8-4.7", 461), ("4.9 V8 324", "MASERATI-V8-4.9", 470, {"debut": "1975-01"})],
   portes=2, places=2, reservoir=100, remarques="Moteur central ; données indicatives")
mg(L, "Merak", "AM122", "1", "1972-10", "1983-12",
   [("3.0 V6 193", "MASERATI-C114-3.0", 255), ("SS 3.0 V6 223", "MASERATI-C114-3.0", 270, {"debut": "1975-01"}), ("2000 GT 2.0 V6 172", "MASERATI-V6-2.0", 186, {"debut": "1977-01"})],
   portes=2, places=4, reservoir=90, remarques="V6 de la Citroën SM ; données indicatives")
mg(L, "Khamsin", "AM120", "1", "1974-01", "1982-12", [("4.9 V8 324", "MASERATI-V8-4.9", 481)], portes=2, places=4, reservoir=100, remarques="Données indicatives")
mg(L, "Kyalami", "AM129", "1", "1976-01", "1983-12", [("4.2 V8 269", "MASERATI-V8-4.2", 393), ("4.9 V8 284", "MASERATI-V8-4.9", 409, {"debut": "1978-01"})],
   portes=2, places=4, reservoir=100, remarques="Données indicatives")

# ---------------------------------------------------------------- ère biturbo
mg(L, "Biturbo", "AM331", "1", "1981-12", "1994-12",
   [("2.0 V6 Biturbo 180", "MASERATI-V6-2.0BT", 255), ("2.5 V6 Biturbo 185", "MASERATI-V6-2.5BT", 280, {"debut": "1983-01", "fin": "1989-12"}),
    ("2.8 V6 Biturbo 225", "MASERATI-V6-2.8BT", 335, {"debut": "1988-01"})], portes=2, places=4, reservoir=80,
   remarques="Coupé, berline 4 portes (425/430) et Spyder ; nombreuses déclinaisons ; données indicatives")
mg(L, "228", "AM334", "1", "1986-01", "1991-12", [("2.8 V6 Biturbo 250", "MASERATI-V6-2.8BT", 373)], portes=2, places=4, reservoir=80, remarques="Données indicatives")
mg(L, "Karif", "AM337", "1", "1988-01", "1993-12", [("2.8 V6 Biturbo 285", "MASERATI-V6-2.8BT", 433)], portes=2, places=2, reservoir=80, remarques="Données indicatives")
mg(L, "Shamal", "AM339", "1", "1990-01", "1996-12", [("3.2 V8 Biturbo 326", "MASERATI-V8-3.2BT", 431)], portes=2, places=4, reservoir=80, remarques="369 exemplaires")
mg(L, "Ghibli II", "AM336", "1", "1992-04", "1997-12", [("2.0 V6 Biturbo 306", "MASERATI-V6-2.0BT", 373), ("2.8 V6 Biturbo 284", "MASERATI-V6-2.8BT", 413)],
   portes=2, places=4, reservoir=80, remarques="2.0 pour l'Italie ; Ghibli Cup (330 ch) non détaillée")
mg(L, "Quattroporte IV", "AM337", "1", "1994-01", "2001-12",
   [("2.0 V6 Biturbo 287", "MASERATI-V6-2.0BT", 362), ("2.8 V6 Biturbo 284", "MASERATI-V6-2.8BT", 413, {"fin": "1998-12"}), ("3.2 V8 Biturbo 336", "MASERATI-V8-3.2BT", 450, {"debut": "1996-01"})],
   portes=4, places=5, reservoir=80, remarques="Evoluzione (1998)")
mg(L, "3200 GT", "M338", "1", "1998-10", "2002-06", [("3.2 V8 Biturbo 370", "MASERATI-V8-3.2BT", 491)], portes=2, places=4, reservoir=90, remarques="Coupé Giugiaro")

# ---------------------------------------------------------------- ère Ferrari/Fiat
mg(L, "Maserati Coupé", "M138", "1", "2002-03", "2007-12", [("4.2 V8 390", "F136-4.2", 451)], portes=2, places=4, reservoir=88, remarques="V8 F136 construit par Ferrari")
mg(L, "Maserati Spyder", "M138", "1", "2001-10", "2007-12", [("4.2 V8 390", "F136-4.2", 451)], portes=2, places=2, reservoir=88)
mg(L, "GranSport", "M138", "1", "2004-01", "2007-12", [("4.2 V8 400", "F136-4.2", 451)], portes=2, places=4, reservoir=88, remarques="Coupé et Spyder")
mg(L, "MC12", "MC12", "1", "2004-06", "2005-12", [("6.0 V12 632", "F140-6.0", 652)], portes=2, places=2, reservoir=115, remarques="50 exemplaires, base Ferrari Enzo")
mg(L, "Quattroporte V", "M139", "1", "2004-01", "2012-12",
   [("4.2 V8 400", "F136-4.2", 451), ("S 4.7 V8 430", "F136-4.7", 490, {"debut": "2008-03"}), ("Sport GT S 4.7 V8 440", "F136-4.7", 490, {"debut": "2009-01"})], portes=4,
   places=5, reservoir=90, remarques="Boîte robotisée DuoSelect puis automatique (2007) ; restylage 2008")
mg(L, "GranTurismo", "M145", "1", "2007-09", "2019-11",
   [("4.2 V8 405", "F136-4.2", 460, {"fin": "2012-12"}), ("S 4.7 V8 440", "F136-4.7", 490), ("MC Stradale 4.7 V8 450", "F136-4.7", 510, {"debut": "2010-10"}),
    ("Sport 4.7 V8 460", "F136-4.7", 520, {"debut": "2012-06"})], portes=2, places=4, reservoir=86, remarques="Restylage 2017")
mg(L, "GranCabrio", "M145", "1", "2010-01", "2019-11", [("4.7 V8 440", "F136-4.7", 490), ("Sport 4.7 V8 450", "F136-4.7", 510, {"debut": "2011-06"}),
                                                      ("MC 4.7 V8 460", "F136-4.7", 520, {"debut": "2013-01"})], portes=2, places=4, reservoir=86)
mg(L, "Quattroporte VI", "M156", "1", "2013-01", "2024-03",
   [("3.0 V6 Biturbo 350", "F160-3.0TT", 500), ("S 3.0 V6 Biturbo 410", "F160-3.0TT", 550), ("S Q4 3.0 V6 Biturbo 430", "F160-3.0TT", 580, {"debut": "2016-06"}),
    ("GTS 3.8 V8 Biturbo 530", "F154-3.8", 650), ("Trofeo 3.8 V8 Biturbo 580", "F154-3.8", 730, {"debut": "2021-01"}),
    ("Diesel 3.0 V6 275", "VM-3.0CRD", 600, {"debut": "2013-10", "fin": "2021-12"})], portes=4, places=5, reservoir=80, remarques="Restylage 2016")
mg(L, "Ghibli (M157)", "M157", "1", "2013-10", "2024-03",
   [("3.0 V6 Biturbo 350", "F160-3.0TT", 500), ("S 3.0 V6 Biturbo 410", "F160-3.0TT", 550), ("S Q4 3.0 V6 Biturbo 430", "F160-3.0TT", 580, {"debut": "2016-06"}),
    ("Diesel 3.0 V6 250", "VM-3.0CRD", 570, {"fin": "2021-12"}), ("Diesel 3.0 V6 275", "VM-3.0CRD", 600, {"fin": "2021-12"}),
    ("Hybrid 2.0 330", "GME-2.0T-MHEV", 450, {"debut": "2020-09"}), ("Trofeo 3.8 V8 Biturbo 580", "F154-3.8", 730, {"debut": "2021-01"})], portes=4, places=5,
   reservoir=80, remarques="Restylages 2017 et 2020")
mg(L, "Levante", "M161", "1", "2016-03", "2024-03",
   [("3.0 V6 Biturbo 350", "F160-3.0TT", 500), ("S 3.0 V6 Biturbo 430", "F160-3.0TT", 580), ("Diesel 3.0 V6 250", "VM-3.0CRD", 570, {"fin": "2021-12"}),
    ("Diesel 3.0 V6 275", "VM-3.0CRD", 600, {"fin": "2021-12"}), ("GTS 3.8 V8 Biturbo 530", "F154-3.8", 650, {"debut": "2019-01"}),
    ("Trofeo 3.8 V8 Biturbo 580", "F154-3.8", 730, {"debut": "2019-01"}), ("Hybrid 2.0 330", "GME-2.0T-MHEV", 450, {"debut": "2021-06"})], reservoir=80,
   remarques="SUV ; restylage 2021 ; production arrêtée en 2024, date de fin indicative")

# ---------------------------------------------------------------- nouvelle génération
mg(L, "MC20", "M240", "1", "2020-12", "2025-06", [("3.0 V6 Nettuno 630", "NETTUNO-3.0", 730)], portes=2, places=2, reservoir=60,
   remarques="Coupé à moteur central, V6 Nettuno à préchambre ; MC20 Cielo dans un modèle séparé")
mg(L, "MC20 Cielo", "M240", "1", "2022-06", "2025-06", [("3.0 V6 Nettuno 630", "NETTUNO-3.0", 730)], portes=2, places=2, reservoir=60, remarques="Spider")
mg(L, "MCPura", "M240", "2", "2025-07", None, [("3.0 V6 Nettuno 630", "NETTUNO-3.0", 730)], portes=2, places=2, reservoir=60,
   remarques="Évolution de la MC20 ; date indicative")
mg(L, "MCPura Cielo", "M240", "2", "2025-07", None, [("3.0 V6 Nettuno 630", "NETTUNO-3.0", 730)], portes=2, places=2, reservoir=60, remarques="Spider ; date indicative")
mg(L, "GT2 Stradale", "M240", "1", "2024-06", None, [("3.0 V6 Nettuno 640", "NETTUNO-3.0", 720)], portes=2, places=2, reservoir=60,
   remarques="Version route dérivée de la MC20 GT2 ; 914 exemplaires")
mg(L, "Grecale", "M182", "1", "2022-05", None,
   [("GT 2.0 MHEV 300", "GME-2.0T-MHEV", 450), ("Modena 2.0 MHEV 330", "GME-2.0T-MHEV", 450), ("Trofeo 3.0 V6 Nettuno 530", "NETTUNO-3.0", 620),
    ("Folgore 557", "FOLGORE-EV", 820, el(105, debut="2024-03"))], reservoir=64, remarques="SUV compact (base Giorgio de l'Alfa Romeo Stelvio)")
mg(L, "GranTurismo", "M189", "1", "2023-03", None,
   [("Modena 3.0 V6 Nettuno 490", "NETTUNO-3.0", 600), ("Trofeo 3.0 V6 Nettuno 550", "NETTUNO-3.0", 650), ("Folgore 761", "FOLGORE-EV", 1350, el(93))],
   portes=2, places=4, reservoir=70, remarques="Deuxième génération ; Folgore électrique 800 V")
mg(L, "GranCabrio", "M189", "1", "2024-03", None, [("Trofeo 3.0 V6 Nettuno 550", "NETTUNO-3.0", 650), ("Folgore 761", "FOLGORE-EV", 1350, el(93, debut="2024-09"))],
   portes=2, places=4, reservoir=70)

MOT = Motorisations("Maserati", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Maserati": L}
MOTEURS = MOT.moteurs()
