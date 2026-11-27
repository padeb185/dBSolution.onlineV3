"""Bentley : générations, phases, motorisations et moteurs liés.
3 Litre à 8 Litre (Cricklewood), Derby 3½/4¼ Litre, Mark VI, R Type, S1/S2/S3, T-Series, Mulsanne, Eight, Turbo R,
Brooklands, Continental R, Azure, Arnage, Continental GT/GTC, Flying Spur, Mulsanne (2010), Bentayga, Bacalar, Batur.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom.
Moteurs d'origine Rolls-Royce, BMW et Volkswagen/Audi rattachés au motoriste Bentley ; données anciennes indicatives
(puissances non publiées à l'époque, couples estimés). Cabriolets (GTC, Convertible) indiqués en remarque."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_, D = "ESS", "DSL"
C = "CHAINE"


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


FAMILLES = {
    "Bentley-3.0": f("ATM", E_, 3.0, "NC", 4, 3500, 2000, "20W50", 9.0, 3000),
    "Bentley-4.4": f("ATM", E_, 4.4, "NC", 4, 3500, 2000, "20W50", 12.0, 3000),
    "Bentley-4.4-Blower": f("TURBO", E_, 4.4, "NC", 4, 4200, 2500, "20W50", 12.0, 3000),
    "Bentley-6.6": f("ATM", E_, 6.6, "NC", 6, 3500, 2000, "20W50", 15.0, 3000),
    "Bentley-8.0": f("ATM", E_, 8.0, "NC", 6, 3500, 2000, "20W50", 15.0, 3000),
    "Derby-3.7": f("ATM", E_, 3.7, "NC", 6, 4500, 2500, "20W50", 7.5, 5000),
    "Derby-4.3": f("ATM", E_, 4.3, "NC", 6, 4500, 2500, "20W50", 7.5, 5000),
    "B60-4.3": f("ATM", E_, 4.3, "NC", 6, 4000, 2000, "20W50", 7.5, 5000),
    "B60-4.6": f("ATM", E_, 4.6, "NC", 6, 4000, 2000, "20W50", 7.5, 5000),
    "B60-4.9": f("ATM", E_, 4.9, "NC", 6, 4000, 2000, "20W50", 7.5, 5000),
    "L410-6.2": f("ATM", E_, 6.2, C, 8, 4500, 2500, "20W50", 8.0, 10000, a="V"),
    "L410-6.75": f("ATM", E_, 6.75, C, 8, 4000, 2000, "15W40", 8.0, 10000, a="V"),
    "L410-6.75T": f("TURBO", E_, 6.75, C, 8, 4000, 2000, "10W40", 8.0, 10000, a="V"),
    "BMW-M62-4.4": f("TURBO", E_, 4.4, C, 8, 5500, 2500, "5W30", 8.0, 15000, a="V"),
    "W12-6.0TT": f("TURBO", E_, 6.0, C, 12, 6000, 1600, "0W40", 12.0, 16000, a="W"),
    "V8-4.0TT": f("TURBO", E_, 4.0, C, 8, 6000, 2000, "0W40", 9.0, 16000, a="V"),
    "V8-4.0TT-PHEV": f("HYB_TE", E_, 4.0, C, 8, 6000, 2000, "0W40", 9.0, 16000, a="V"),
    "V6-3.0-PHEV": f("HYB_TE", E_, 3.0, C, 6, 5300, 1500, "0W30", 7.0, 16000, a="V"),
    "V6-2.9-PHEV": f("HYB_TE", E_, 2.9, C, 6, 5500, 2000, "0W30", 7.0, 16000, a="V"),
    "V8-4.0TDI": f("TURBO", D, 4.0, C, 8, 3750, 1000, "0W30", 9.0, 16000, a="V"),
}

mg = SaisieMoteurs(FAMILLES, "Bentley")
L = []

# ---------------------------------------------------------------- Cricklewood et Derby
mg(L, "3 Litre", "3 Litre", "1", "1921-09", "1929-12", [("3 Litre 70", "Bentley-3.0", 180)], portes=2, places=4, reservoir=50,
   remarques="Châssis carrossés (Tourer, Saloon) ; puissance indicative")
mg(L, "4½ Litre", "4½ Litre", "1", "1927-08", "1931-12",
   [("4½ Litre 110", "Bentley-4.4", 300), ("4½ Litre Blower 240", "Bentley-4.4-Blower", 450, {"debut": "1929-06", "fin": "1931-06"})],
   portes=2, places=4, reservoir=73, remarques="Châssis carrossés ; « Blower » à compresseur (55 ex.)")
mg(L, "6½ Litre", "6½ Litre", "1", "1926-06", "1930-12",
   [("6½ Litre 147", "Bentley-6.6", 400), ("Speed Six 180", "Bentley-6.6", 450, {"debut": "1928-01"})], portes=4, places=4,
   reservoir=91, remarques="Châssis carrossés ; Speed Six victorieuse au Mans")
mg(L, "8 Litre", "8 Litre", "1", "1930-10", "1932-12", [("8 Litre 220", "Bentley-8.0", 550)], portes=4, places=4, reservoir=110,
   remarques="Dernier modèle Cricklewood (100 ex.)")
mg(L, "3½ Litre", "Derby", "1", "1933-10", "1937-03", [("3½ Litre 110", "Derby-3.7", 240)], portes=4, places=4, reservoir=82,
   remarques="« Silent Sports Car » (base Rolls-Royce) ; carrosseries diverses")
mg(L, "4¼ Litre", "Derby", "2", "1936-03", "1939-12", [("4¼ Litre 125", "Derby-4.3", 270)], portes=4, places=4, reservoir=82,
   remarques="Carrosseries diverses ; Mark V (1939) non détaillée")
mg(L, "Mark VI", "Mark VI", "1", "1946-05", "1952-12",
   [("Mark VI 4.25 135", "B60-4.3", 290, {"fin": "1951-06"}), ("Mark VI 4.6 150", "B60-4.6", 320, {"debut": "1951-07"})], portes=4,
   places=5, reservoir=82, remarques="Première Bentley à carrosserie d'usine (Standard Steel Saloon)")
mg(L, "R Type", "R Type", "1", "1952-06", "1955-04",
   [("R Type 4.6 150", "B60-4.6", 320), ("R Type Continental 4.9 178", "B60-4.9", 350, {"debut": "1954-05"})], portes=4, places=5,
   reservoir=82, remarques="Berline ; R Type Continental fastback (1952-1955)")
mg(L, "S1", "S", "1", "1955-04", "1959-08", [("S1 4.9 178", "B60-4.9", 350)], portes=4, places=5, reservoir=82,
   remarques="Berline et Continental (jumelle Rolls-Royce Silver Cloud)")
mg(L, "S2", "S", "2", "1959-08", "1962-09", [("S2 6.2 V8 200", "L410-6.2", 450)], portes=4, places=5, reservoir=82,
   remarques="Berline et Continental ; premier V8")
mg(L, "S3", "S", "3", "1962-10", "1965-09", [("S3 6.2 V8 220", "L410-6.2", 450)], portes=4, places=5, reservoir=82,
   remarques="Berline à doubles phares et Continental")
mg(L, "T-Series", "T", "1", "1965-10", "1980-08",
   [("T1 6.2 V8 200", "L410-6.2", 450, {"fin": "1970-06"}), ("T1 6.75 V8 220", "L410-6.75", 500, {"debut": "1970-07", "fin": "1977-02"}),
    ("T2 6.75 V8 220", "L410-6.75", 500, {"debut": "1977-03"})], portes=4, places=5, reservoir=109,
   remarques="Jumelle de la Silver Shadow ; Corniche (1971)")

# ---------------------------------------------------------------- 1980-2009 (V8 L410)
mg(L, "Mulsanne", "SZ", "1", "1980-10", "1992-12",
   [("Mulsanne 6.75 220", "L410-6.75", 500), ("Mulsanne Turbo 6.75 300", "L410-6.75T", 610, {"debut": "1982-03", "fin": "1985-12"}),
    ("Mulsanne S 6.75 220", "L410-6.75", 500, {"debut": "1987-08"})], portes=4, places=5, reservoir=108,
   remarques="Berline (base Silver Spirit)")
mg(L, "Eight", "SZ", "1", "1984-07", "1992-12", [("Eight 6.75 220", "L410-6.75", 500)], portes=4, places=5, reservoir=108,
   remarques="Version d'accès de la Mulsanne")
mg(L, "Turbo R", "SZ", "2", "1985-03", "1997-12",
   [("Turbo R 6.75 300", "L410-6.75T", 610, {"fin": "1994-12"}), ("Turbo R 6.75 385", "L410-6.75T", 750, {"debut": "1995-01"})],
   portes=4, places=5, reservoir=108, remarques="Berline turbo ; Turbo RT (1997) non détaillée")
mg(L, "Brooklands", "SZ", "2", "1992-10", "1998-06", [("Brooklands 6.75 300", "L410-6.75", 500)], portes=4, places=5, reservoir=108,
   remarques="Berline (remplace Mulsanne S et Eight)")
mg(L, "Continental R", "SZ", "2", "1991-03", "2003-06",
   [("Continental R 6.75 325", "L410-6.75T", 610, {"fin": "1994-12"}), ("Continental R 6.75 385", "L410-6.75T", 750, {"debut": "1995-01"}),
    ("Continental T 6.75 420", "L410-6.75T", 875, {"debut": "1996-06"})], portes=2, places=4, reservoir=108,
   remarques="Coupé ; Continental S, SC (targa) non détaillées")
mg(L, "Azure", "SZ", "2", "1995-03", "2003-06", [("Azure 6.75 385", "L410-6.75T", 750)], portes=2, places=4, reservoir=108,
   remarques="Cabriolet (Pininfarina)")
mg(L, "Arnage", "RBS", "1", "1998-04", "2009-06",
   [("Arnage Green Label 4.4 354", "BMW-M62-4.4", 570, {"fin": "2000-12"}), ("Arnage Red Label 6.75 405", "L410-6.75T", 835, {"debut": "1999-09", "fin": "2002-08"}),
    ("Arnage T 6.75 457", "L410-6.75T", 875, {"debut": "2002-01", "fin": "2007-08"}), ("Arnage R 6.75 405", "L410-6.75T", 875, {"debut": "2002-01"}),
    ("Arnage T 6.75 507", "L410-6.75T", 1000, {"debut": "2007-09"}), ("Arnage RL 6.75 405", "L410-6.75T", 875, {"debut": "2002-01"})],
   portes=4, places=5, reservoir=96, remarques="Berline ; Green Label à V8 BMW biturbo, puis V8 Bentley ; RL = version longue")
mg(L, "Azure", "RBS", "1", "2006-03", "2010-12",
   [("Azure 6.75 456", "L410-6.75T", 875), ("Azure T 6.75 507", "L410-6.75T", 1000, {"debut": "2009-03"})], portes=2, places=4,
   reservoir=96, remarques="Cabriolet sur base Arnage")
mg(L, "Brooklands", "RBS", "1", "2008-01", "2011-06", [("Brooklands 6.75 537", "L410-6.75T", 1050)], portes=2, places=4,
   reservoir=96, remarques="Coupé (550 ex.)")
mg(L, "Mulsanne", "BY", "1", "2010-08", "2020-06",
   [("Mulsanne 6.75 512", "L410-6.75T", 1020, {"fin": "2016-06"}), ("Mulsanne 6.75 Speed 537", "L410-6.75T", 1100, {"debut": "2014-03"}),
    ("Mulsanne Extended Wheelbase 512", "L410-6.75T", 1020, {"debut": "2016-07"})],
   portes=4, places=5, reservoir=96, remarques="Berline de prestige ; restylage 2016 ; dernière utilisation du V8 6¾ litres")

# ---------------------------------------------------------------- Continental GT / Flying Spur
mg(L, "Continental GT", "3S", "1", "2003-09", "2011-06",
   [("Continental GT W12 560", "W12-6.0TT", 650), ("Continental GT Speed W12 610", "W12-6.0TT", 750, {"debut": "2007-09"}),
    ("Continental Supersports W12 630", "W12-6.0TT", 800, {"debut": "2009-12"})], portes=2, places=4, reservoir=90,
   remarques="Coupé et GTC cabriolet (2006)")
mg(L, "Continental GT", "3W", "1", "2011-01", "2018-06",
   [("Continental GT W12 575", "W12-6.0TT", 700, {"fin": "2015-06"}), ("Continental GT W12 590", "W12-6.0TT", 720, {"debut": "2015-07"}),
    ("Continental GT Speed W12 625", "W12-6.0TT", 800, {"debut": "2012-06", "fin": "2015-06"}),
    ("Continental GT Speed W12 642", "W12-6.0TT", 840, {"debut": "2015-07"}), ("Continental GT V8 507", "V8-4.0TT", 660, {"debut": "2012-03"}),
    ("Continental GT V8 S 528", "V8-4.0TT", 680, {"debut": "2014-01"}), ("Continental GT3-R V8 580", "V8-4.0TT", 700, {"debut": "2014-09", "fin": "2015-06"}),
    ("Continental Supersports W12 710", "W12-6.0TT", 1017, {"debut": "2017-03", "fin": "2018-02"})],
   portes=2, places=4, reservoir=90, remarques="Coupé et GTC cabriolet ; GT3-R (300 ex.) dérivée de la course ; restylage 2015")
mg(L, "Continental GT", "3S", "2", "2018-01", "2024-03",
   [("Continental GT W12 635", "W12-6.0TT", 900), ("Continental GT V8 550", "V8-4.0TT", 770, {"debut": "2019-06"}),
    ("Continental GT Speed W12 659", "W12-6.0TT", 900, {"debut": "2021-06"}), ("Continental GT S V8 550", "V8-4.0TT", 770, {"debut": "2022-09"})],
   portes=2, places=4, reservoir=90, remarques="3e génération (MSB) : Coupé et GTC")
mg(L, "Continental GT", "3S", "3", "2024-06", None,
   [("Continental GT Speed 782", "V8-4.0TT-PHEV", 1000, ph(26, 80)), ("Continental GT 680", "V8-4.0TT-PHEV", 930, ph(26, 80, debut="2025-04")),
    ("Continental GT Supersports 666", "V8-4.0TT", 800, {"debut": "2026-03", "reservoir": 80})], portes=2, places=4, reservoir=80,
   remarques="4e génération : V8 hybride rechargeable (Speed, Mulliner, S, Azure) ; Supersports à propulsion (2026)")
mg(L, "Flying Spur", "3S", "1", "2005-03", "2013-06",
   [("Continental Flying Spur W12 560", "W12-6.0TT", 650), ("Continental Flying Spur Speed W12 610", "W12-6.0TT", 750, {"debut": "2008-09"})],
   portes=4, places=5, reservoir=90, remarques="Berline (Continental Flying Spur)")
mg(L, "Flying Spur", "3W", "1", "2013-03", "2019-06",
   [("Flying Spur W12 625", "W12-6.0TT", 800), ("Flying Spur W12 S 635", "W12-6.0TT", 820, {"debut": "2016-09"}),
    ("Flying Spur V8 507", "V8-4.0TT", 660, {"debut": "2014-09"}), ("Flying Spur V8 S 528", "V8-4.0TT", 680, {"debut": "2016-09"})],
   portes=4, places=5, reservoir=90, remarques="Berline")
mg(L, "Flying Spur", "3S", "2", "2019-06", "2024-06",
   [("Flying Spur W12 635", "W12-6.0TT", 900), ("Flying Spur V8 550", "V8-4.0TT", 770, {"debut": "2020-09"}),
    ("Flying Spur Hybrid 544", "V6-2.9-PHEV", 750, ph(18, 80, debut="2021-09")), ("Flying Spur Speed W12 635", "W12-6.0TT", 900, {"debut": "2022-06"})],
   portes=4, places=5, reservoir=90, remarques="3e génération (MSB)")
mg(L, "Flying Spur", "3S", "3", "2024-07", None,
   [("Flying Spur Speed 782", "V8-4.0TT-PHEV", 1000, ph(26, 80)), ("Flying Spur 680", "V8-4.0TT-PHEV", 930, ph(26, 80, debut="2025-04"))],
   portes=4, places=5, reservoir=80, remarques="V8 hybride rechargeable (Speed, Mulliner, S, Azure) ; restylage 2026 non détaillé")

# ---------------------------------------------------------------- Bentayga / séries limitées
mg(L, "Bentayga", "4V", "1", "2016-01", "2020-06",
   [("Bentayga W12 608", "W12-6.0TT", 900), ("Bentayga Diesel 435", "V8-4.0TDI", 900, {"debut": "2017-01", "fin": "2018-08"}),
    ("Bentayga V8 550", "V8-4.0TT", 770, {"debut": "2018-01"}), ("Bentayga Hybrid 449", "V6-3.0-PHEV", 700, ph(17, 75, debut="2018-12")),
    ("Bentayga Speed W12 635", "W12-6.0TT", 900, {"debut": "2019-06"})], places=5, reservoir=85, remarques="SUV 4, 5 ou 7 places")
mg(L, "Bentayga", "4V", "2", "2020-07", None,
   [("Bentayga V8 550", "V8-4.0TT", 770), ("Bentayga Hybrid 449", "V6-3.0-PHEV", 700, ph(18, 80)),
    ("Bentayga Speed W12 635", "W12-6.0TT", 900, {"fin": "2024-04"}), ("Bentayga S V8 550", "V8-4.0TT", 770, {"debut": "2021-09"}),
    ("Bentayga Speed V8 650", "V8-4.0TT", 850, {"debut": "2024-09"})], places=5, reservoir=85,
   remarques="SUV restylé ; Extended Wheelbase (2022) ; fin du W12 en 2024")
mg(L, "Bacalar", "3S", "4", "2021-01", "2022-06", [("Bacalar W12 659", "W12-6.0TT", 900)], portes=2, places=2, reservoir=80,
   remarques="Barchetta Mulliner (12 ex.)")
mg(L, "Batur", "3S", "4", "2023-06", "2025-06", [("Batur W12 750", "W12-6.0TT", 1000)], portes=2, places=4, reservoir=80,
   remarques="Coupé et Convertible Mulliner (18 + 16 ex.), dernier W12")

MOT = Motorisations("Bentley", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Bentley": L}
MOTEURS = MOT.moteurs()
