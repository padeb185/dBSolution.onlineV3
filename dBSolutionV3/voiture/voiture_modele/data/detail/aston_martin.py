"""Aston Martin : générations, phases, motorisations et moteurs liés.
DB2 à DB6, DBS, V8, Lagonda, Virage, DB7, V12 Vanquish, DB9, DBS V12, V8/V12 Vantage, Rapide, Vanquish, DB11,
DBS Superleggera, Vantage, DBX, DB12, Vanquish (2024), One-77, Valkyrie, Valhalla, Cygnet.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom.
V8 Mercedes-AMG (M177) et moteurs Ford/Cosworth/Toyota rattachés au motoriste Aston Martin ; données anciennes indicatives.
Versions Volante (cabriolet) et Roadster indiquées en remarque."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C = "CHAINE"


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


FAMILLES = {
    "Lagonda-2.6": f("ATM", E_, 2.6, C, 6, 5000, 3100, "20W50", 7.0, 5000),
    "Lagonda-2.9": f("ATM", E_, 2.9, C, 6, 5500, 3500, "20W50", 7.0, 5000),
    "Marek-3.7": f("ATM", E_, 3.7, C, 6, 5500, 4250, "20W50", 9.0, 5000),
    "Marek-4.0": f("ATM", E_, 4.0, C, 6, 5500, 3850, "20W50", 9.0, 5000),
    "AM-V8-5.3": f("ATM", E_, 5.3, C, 8, 5500, 4000, "20W50", 11.0, 5000, a="V"),
    "AM-V8-5.3SC": f("TURBO", E_, 5.3, C, 8, 6500, 4000, "15W50", 11.0, 8000, a="V"),
    "DB7-3.2SC": f("TURBO", E_, 3.2, C, 6, 6000, 3000, "10W40", 7.0, 10000),
    "AM-V12-5.9": f("ATM", E_, 5.9, C, 12, 6500, 5000, "0W40", 10.0, 15000, a="V"),
    "AM-V8-4.3": f("ATM", E_, 4.3, C, 8, 7300, 5000, "0W40", 8.0, 15000, a="V"),
    "AM-V8-4.7": f("ATM", E_, 4.7, C, 8, 7300, 5000, "0W40", 8.0, 15000, a="V"),
    "AM-V12-7.3": f("ATM", E_, 7.3, C, 12, 7500, 5000, "0W40", 12.0, 10000, a="V"),
    "AM-V12-5.2TT": f("TURBO", E_, 5.2, C, 12, 6500, 1500, "0W40", 10.0, 16000, a="V"),
    "AM-M177-4.0": f("TURBO", E_, 4.0, C, 8, 6000, 2000, "0W40", 9.0, 16000, a="V"),
    "Cosworth-6.5-HYB": f("HYB_E", E_, 6.5, C, 12, 10500, 7000, "0W40", 12.0, 10000, a="V"),
    "Valhalla-4.0-PHEV": f("HYB_TE", E_, 4.0, C, 8, 7200, 6000, "0W40", 9.0, 16000, a="V"),
    "Toyota-1NR-FE": f("ATM", E_, 1.33, C, 4, 6000, 3800, "0W20", 3.4, 15000),
}

mg = SaisieMoteurs(FAMILLES, "Aston Martin")
L = []

# ---------------------------------------------------------------- années 1950-1990
mg(L, "DB2", "DB2", "1", "1950-05", "1953-04",
   [("DB2 2.6 105", "Lagonda-2.6", 170), ("DB2 Vantage 2.6 125", "Lagonda-2.6", 190, {"debut": "1951-01"})],
   portes=2, places=2, reservoir=77, remarques="Coupé et Drophead Coupé")
mg(L, "DB2/4", "DB2/4", "1", "1953-10", "1957-08",
   [("DB2/4 2.6 125", "Lagonda-2.6", 190, {"fin": "1954-12"}), ("DB2/4 2.9 140", "Lagonda-2.9", 240, {"debut": "1954-10"})],
   portes=3, places=4, reservoir=77, remarques="Coupé 2+2 à hayon, Drophead ; Mk II (1955)")
mg(L, "DB Mark III", "DB Mk III", "1", "1957-03", "1959-07", [("DB Mk III 2.9 162", "Lagonda-2.9", 245)], portes=3,
   places=4, reservoir=77, remarques="Coupé 2+2 et Drophead")
mg(L, "DB4", "DB4", "1", "1958-10", "1963-06",
   [("DB4 3.7 240", "Marek-3.7", 325), ("DB4 GT 3.7 302", "Marek-3.7", 366, {"debut": "1959-10", "fin": "1963-06"}),
    ("DB4 Vantage 3.7 266", "Marek-3.7", 340, {"debut": "1961-09"})], portes=2, places=4, reservoir=86,
   remarques="Coupé (Touring Superleggera) et Convertible ; DB4 GT Zagato")
mg(L, "DB5", "DB5", "1", "1963-07", "1965-09",
   [("DB5 4.0 282", "Marek-4.0", 390), ("DB5 Vantage 4.0 314", "Marek-4.0", 390, {"debut": "1964-07"})], portes=2, places=4,
   reservoir=86, remarques="Coupé, Convertible, Shooting Brake (12 ex.)")
mg(L, "DB6", "DB6", "1", "1965-10", "1970-11",
   [("DB6 4.0 282", "Marek-4.0", 390), ("DB6 Vantage 4.0 325", "Marek-4.0", 400)], portes=2, places=4, reservoir=73,
   remarques="Coupé et Volante ; Mk II (1969)")
mg(L, "DBS", "DBS", "1", "1967-09", "1972-05",
   [("DBS 4.0 282", "Marek-4.0", 390), ("DBS Vantage 4.0 325", "Marek-4.0", 400), ("DBS V8 5.3 320", "AM-V8-5.3", 490, {"debut": "1969-09"})],
   portes=2, places=4, reservoir=95, remarques="Coupé 2+2")
mg(L, "V8", "AM V8", "1", "1972-05", "1989-12",
   [("V8 5.3 310", "AM-V8-5.3", 490), ("V8 Vantage 5.3 380", "AM-V8-5.3", 540, {"debut": "1977-02"}),
    ("V8 Volante 5.3 310", "AM-V8-5.3", 490, {"debut": "1978-06"})], portes=2, places=4, reservoir=95,
   remarques="Coupé 2+2 et Volante ; Zagato (1986)")
mg(L, "Lagonda", "Lagonda", "1", "1976-10", "1990-01", [("Lagonda 5.3 280", "AM-V8-5.3", 410)], portes=4, places=4,
   reservoir=127, remarques="Berline futuriste (William Towns)")
mg(L, "Virage", "Virage", "1", "1989-01", "2000-12",
   [("Virage 5.3 330", "AM-V8-5.3", 460, {"fin": "1995-12"}), ("V8 Vantage 5.3 550", "AM-V8-5.3SC", 745, {"debut": "1993-01"}),
    ("V8 Coupé 5.3 355", "AM-V8-5.3", 480, {"debut": "1996-01"}), ("V8 Vantage V600 600", "AM-V8-5.3SC", 820, {"debut": "1998-01"})],
   portes=2, places=4, reservoir=113, remarques="Coupé 2+2 et Volante ; V8 Vantage à double compresseur")

# ---------------------------------------------------------------- 1994-2018
mg(L, "DB7", "DB7", "1", "1994-09", "1999-03", [("DB7 3.2 335", "DB7-3.2SC", 489)], portes=2, places=4, reservoir=89,
   remarques="Coupé 2+2 et Volante (1996), 6 cylindres à compresseur")
mg(L, "DB7", "DB7", "2", "1999-03", "2003-12",
   [("DB7 Vantage 5.9 420", "AM-V12-5.9", 540), ("DB7 GT 5.9 435", "AM-V12-5.9", 556, {"debut": "2002-03"}),
    ("DB7 Zagato 5.9 440", "AM-V12-5.9", 556, {"debut": "2003-01"})], portes=2, places=4, reservoir=89, remarques="V12 ; Volante")
mg(L, "V12 Vanquish", "V12 Vanquish", "1", "2001-06", "2007-07",
   [("V12 Vanquish 460", "AM-V12-5.9", 542, {"fin": "2004-09"}), ("V12 Vanquish S 520", "AM-V12-5.9", 577, {"debut": "2004-10"})],
   portes=2, places=4, reservoir=80, remarques="Coupé 2+2 (ou 2 places)")
mg(L, "DB9", "VH", "1", "2004-01", "2012-06",
   [("DB9 5.9 450", "AM-V12-5.9", 570, {"fin": "2008-06"}), ("DB9 5.9 470", "AM-V12-5.9", 600, {"debut": "2008-07"})],
   portes=2, places=4, reservoir=85, remarques="Coupé 2+2 et Volante")
mg(L, "DB9", "VH", "2", "2012-07", "2016-07",
   [("DB9 5.9 517", "AM-V12-5.9", 620), ("DB9 GT 5.9 547", "AM-V12-5.9", 620, {"debut": "2015-06"})], portes=2, places=4,
   reservoir=78, remarques="Coupé 2+2 et Volante")
mg(L, "DBS", "VH", "1", "2007-08", "2012-06", [("DBS 5.9 517", "AM-V12-5.9", 570)], portes=2, places=4, reservoir=78,
   remarques="Coupé et Volante (2009)")
mg(L, "V8 Vantage", "VH", "1", "2005-03", "2008-03", [("V8 Vantage 4.3 385", "AM-V8-4.3", 410)], portes=2, places=2,
   reservoir=80, remarques="Coupé et Roadster (2006)")
mg(L, "V8 Vantage", "VH", "2", "2008-04", "2017-12",
   [("V8 Vantage 4.7 426", "AM-V8-4.7", 470), ("V8 Vantage S 4.7 436", "AM-V8-4.7", 490, {"debut": "2011-06"}),
    ("V8 Vantage GT 4.7 446", "AM-V8-4.7", 490, {"debut": "2015-01"})], portes=2, places=2, reservoir=80, remarques="Coupé et Roadster")
mg(L, "V12 Vantage", "VH", "1", "2009-06", "2018-12",
   [("V12 Vantage 5.9 517", "AM-V12-5.9", 570, {"fin": "2013-06"}), ("V12 Vantage S 5.9 573", "AM-V12-5.9", 620, {"debut": "2013-07"})],
   portes=2, places=2, reservoir=80, remarques="Coupé et Roadster ; V12 Zagato (2012)")
mg(L, "Rapide", "VH", "1", "2010-05", "2020-06",
   [("Rapide 5.9 477", "AM-V12-5.9", 600, {"fin": "2013-02"}), ("Rapide S 5.9 558", "AM-V12-5.9", 620, {"debut": "2013-03", "fin": "2014-12"}),
    ("Rapide S 5.9 560", "AM-V12-5.9", 630, {"debut": "2015-01"}), ("Rapide AMR 5.9 603", "AM-V12-5.9", 630, {"debut": "2018-06"})],
   portes=4, places=4, reservoir=90, remarques="Berline 4 portes ; Rapide E électrique (série limitée) non détaillée")
mg(L, "Vanquish", "VH", "1", "2012-06", "2018-07",
   [("Vanquish 5.9 573", "AM-V12-5.9", 620, {"fin": "2016-12"}), ("Vanquish S 5.9 600", "AM-V12-5.9", 630, {"debut": "2017-01"})],
   portes=2, places=4, reservoir=78, remarques="Coupé et Volante ; Zagato (2016)")
mg(L, "One-77", "One-77", "1", "2009-12", "2012-12", [("One-77 760", "AM-V12-7.3", 750)], portes=2, places=2, reservoir=80,
   remarques="Hypercar, 77 exemplaires")
mg(L, "Cygnet", "AJ10", "1", "2011-06", "2013-09", [("Cygnet 1.33 98", "Toyota-1NR-FE", 123)], portes=3, places=4,
   reservoir=32, remarques="Citadine dérivée de la Toyota iQ")

# ---------------------------------------------------------------- 2016-2026
mg(L, "DB11", "DB11", "1", "2016-10", "2018-05",
   [("DB11 V12 608", "AM-V12-5.2TT", 700), ("DB11 V8 510", "AM-M177-4.0", 675, {"debut": "2017-08"})], portes=2, places=4,
   reservoir=78, remarques="Coupé 2+2 et Volante (2018)")
mg(L, "DB11", "DB11", "2", "2018-06", "2023-05",
   [("DB11 V8 535", "AM-M177-4.0", 675, {"debut": "2021-01"}), ("DB11 V8 510", "AM-M177-4.0", 675, {"fin": "2020-12"}),
    ("DB11 AMR 639", "AM-V12-5.2TT", 700)], portes=2, places=4, reservoir=78, remarques="Coupé 2+2 et Volante")
mg(L, "DBS Superleggera", "DBS", "1", "2018-08", "2023-06",
   [("DBS Superleggera 725", "AM-V12-5.2TT", 900), ("DBS 770 Ultimate 770", "AM-V12-5.2TT", 900, {"debut": "2023-01"})],
   portes=2, places=4, reservoir=78, remarques="Coupé et Volante")
mg(L, "Vantage", "VH5", "1", "2018-05", "2024-03",
   [("Vantage V8 510", "AM-M177-4.0", 685), ("Vantage F1 Edition 535", "AM-M177-4.0", 685, {"debut": "2021-05"}),
    ("V12 Vantage 700", "AM-V12-5.2TT", 753, {"debut": "2022-03", "fin": "2023-12"})], portes=2, places=2, reservoir=73,
   remarques="Coupé et Roadster (2020)")
mg(L, "Vantage", "VH5", "2", "2024-04", None,
   [("Vantage 665", "AM-M177-4.0", 800), ("Vantage S 680", "AM-M177-4.0", 800, {"debut": "2026-01"})], portes=2, places=2,
   reservoir=73, remarques="Coupé et Roadster (2024) ; Vantage S (2026)")
mg(L, "DBX", "DBX", "1", "2020-07", "2024-03",
   [("DBX 550", "AM-M177-4.0", 700), ("DBX707 707", "AM-M177-4.0", 900, {"debut": "2022-04"})], places=5, reservoir=85,
   remarques="SUV")
mg(L, "DBX", "DBX", "2", "2024-04", None,
   [("DBX707 707", "AM-M177-4.0", 900), ("DBX S 727", "AM-M177-4.0", 900, {"debut": "2025-10"})], places=5, reservoir=85,
   remarques="SUV, nouvel intérieur ; DBX S (technologie moteur dérivée de la Valhalla)")
mg(L, "DB12", "DB12", "1", "2023-06", None,
   [("DB12 680", "AM-M177-4.0", 800), ("DB12 S 700", "AM-M177-4.0", 800, {"debut": "2026-07"})], portes=2, places=4,
   reservoir=78, remarques="Super Tourer : Coupé et Volante (2023) ; DB12 S (2026)")
mg(L, "Vanquish", "Vanquish III", "1", "2024-11", None, [("Vanquish 835", "AM-V12-5.2TT", 1000)], portes=2, places=2,
   reservoir=82, remarques="Coupé V12 et Volante (2025)")
mg(L, "Valkyrie", "Valkyrie", "1", "2021-11", "2024-12", [("Valkyrie 1155", "Cosworth-6.5-HYB", 900)], portes=2, places=2,
   reservoir=0, remarques="Hypercar hybride (V12 Cosworth atmosphérique) ; Spider (2023) ; réservoir non communiqué")
mg(L, "Valhalla", "Valhalla", "1", "2025-06", None, [("Valhalla 1079", "Valhalla-4.0-PHEV", 1100, ph(6, 69))], portes=2, places=2,
   remarques="Supercar hybride rechargeable à moteur central (V8 biturbo + 3 moteurs électriques) ; Valhalla AMR annoncée")

MOT = Motorisations("Aston Martin", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Aston Martin": L}
MOTEURS = MOT.moteurs()
