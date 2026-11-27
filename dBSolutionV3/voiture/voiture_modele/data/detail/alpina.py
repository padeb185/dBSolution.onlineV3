"""Alpina (Buchloe ; BMW Alpina depuis 2026) : générations, motorisations (marché européen) et moteurs liés.
Modèles sur base BMW (la génération reprend le code BMW). Moteurs BMW retravaillés par Alpina, au motoriste « Alpina ».
La production Bovensiepen s'est arrêtée fin 2025 ; le premier modèle BMW Alpina (base Série 7 restylée) n'est pas encore repris.
Modèles d avant 1988 dans alpina_classiques.py. Données de production indicatives (petites séries).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_, D = "ESS", "DSL"
C = "CHAINE"


def a6(t, carb, l, rpm, nmrpm, huile, q, km=15000):
    return f(t, carb, l, C, 6, rpm, nmrpm, huile, q, km)


def a8(t, l, rpm, nmrpm, huile, q, km=15000):
    return f(t, E_, l, C, 8, rpm, nmrpm, huile, q, km, a="V")


FAMILLES = {
    "ALPINA-M30-3.5": a6("ATM", E_, 3.5, 5800, 4000, "10W40", 5.75, 10000),
    "ALPINA-M30-3.5BT": a6("TURBO", E_, 3.5, 6000, 4000, "10W40", 5.75, 10000),
    "ALPINA-S52-3.2": a6("ATM", E_, 3.2, 5800, 4400, "10W60", 6.5, 10000),
    "ALPINA-M54-3.3": a6("ATM", E_, 3.3, 5900, 4500, "10W60", 6.5),
    "ALPINA-S54-3.4": a6("ATM", E_, 3.4, 6800, 4700, "10W60", 6.5),
    "ALPINA-N54-3.0BT": a6("TURBO", E_, 3.0, 5500, 3800, "5W30", 6.5),
    "ALPINA-N55-3.0BT": a6("TURBO", E_, 3.0, 5500, 3000, "5W30", 6.5),
    "ALPINA-S58-3.0BT": a6("TURBO", E_, 3.0, 5500, 2500, "0W30", 6.5),
    "ALPINA-M62-4.6": a8("ATM", 4.6, 5700, 3800, "10W60", 7.5),
    "ALPINA-M62-4.8": a8("ATM", 4.8, 5800, 3800, "10W60", 7.5),
    "ALPINA-N62-4.4K": a8("TURBO", 4.4, 5500, 4250, "5W30", 8.0),
    "ALPINA-N63-4.4BT": a8("TURBO", 4.4, 5500, 2800, "0W30", 9.0),
    "ALPINA-M73-5.7": f("ATM", E_, 5.7, C, 12, 5300, 4100, "10W60", 9.0, 15000, a="V"),
    "ALPINA-M47-2.0D": f("TURBO", D, 2.0, C, 4, 4000, 2000, "5W30", 5.25, 20000),
    "ALPINA-N57-3.0D": a6("TURBO", D, 3.0, 4000, 1500, "5W30", 7.0, 20000),
    "ALPINA-B57-3.0D": a6("TURBO", D, 3.0, 4200, 1750, "0W30", 7.0, 20000),
}

mg = SaisieMoteurs(FAMILLES, "Alpina")
L = []
IND = "Données indicatives"

# ---------------------------------------------------------------- années 1988-2005
mg(L, "B10", "E34", "1", "1988-01", "1996-06",
   [("B10 3.5 254", "ALPINA-M30-3.5", 320, {"fin": "1992-12"}), ("B10 BiTurbo 360", "ALPINA-M30-3.5BT", 520, {"debut": "1989-01", "fin": "1994-12"})],
   portes=4, reservoir=80, remarques=IND + " ; berline et Touring")
mg(L, "B3", "E36", "1", "1993-06", "1999-12", [("B3 3.0 250", "ALPINA-S52-3.2", 320, {"fin": "1995-12"}), ("B3 3.2 265", "ALPINA-S52-3.2", 330, {"debut": "1996-01"})],
   portes=4, reservoir=65, remarques=IND + " ; berline, coupé, cabriolet, Touring")
mg(L, "B8", "E36", "1", "1995-01", "1998-12", [("B8 4.6 333", "ALPINA-M62-4.6", 470)], portes=4, reservoir=65, remarques=IND + " ; V8 dans la Série 3")
mg(L, "B10", "E39", "1", "1997-01", "2004-03",
   [("B10 3.3 280", "ALPINA-M54-3.3", 315, {"debut": "1999-01"}), ("B10 V8 4.6 340", "ALPINA-M62-4.6", 470), ("B10 V8 S 4.8 375", "ALPINA-M62-4.8", 510, {"debut": "2002-01"})],
   portes=4, reservoir=70, remarques=IND + " ; berline et Touring")
mg(L, "B12", "E38", "1", "1995-01", "2001-12", [("B12 5.7 387", "ALPINA-M73-5.7", 560), ("B12 6.0 430", "ALPINA-M73-5.7", 600, {"debut": "1999-01"})],
   portes=4, reservoir=95, remarques=IND)
mg(L, "B3", "E46", "1", "1999-09", "2006-12", [("B3 3.3 280", "ALPINA-M54-3.3", 315), ("B3 S 3.4 305", "ALPINA-S54-3.4", 355, {"debut": "2002-09"})],
   portes=4, reservoir=63, remarques=IND + " ; berline, coupé, cabriolet, Touring")
mg(L, "Roadster", "E85", "1", "2003-01", "2005-12", [("Roadster V8 4.8 375", "ALPINA-M62-4.8", 500)], portes=2, places=2, reservoir=55,
   remarques="Base BMW Z8 (555 ex.)")
mg(L, "Roadster S", "E85 Z4", "1", "2004-09", "2006-12", [("Roadster S 3.4 300", "ALPINA-S54-3.4", 355)], portes=2, places=2, reservoir=55, remarques="Base BMW Z4")

# ---------------------------------------------------------------- 2005-2015
mg(L, "B5", "E60", "1", "2005-01", "2010-06", [("B5 4.4 Compresseur 500", "ALPINA-N62-4.4K", 700), ("B5 S 4.4 Compresseur 530", "ALPINA-N62-4.4K", 725, {"debut": "2007-09"})],
   portes=4, reservoir=70, remarques="Berline et Touring")
mg(L, "B6", "E63", "1", "2005-09", "2010-12", [("B6 4.4 Compresseur 500", "ALPINA-N62-4.4K", 700), ("B6 S 4.4 Compresseur 530", "ALPINA-N62-4.4K", 725, {"debut": "2008-01"})],
   portes=2, places=4, reservoir=70, remarques="Coupé et cabriolet")
mg(L, "B7", "E65", "1", "2003-09", "2008-12", [("B7 4.4 Compresseur 500", "ALPINA-N62-4.4K", 700)], portes=4, reservoir=88)
mg(L, "B3", "E90", "1", "2007-09", "2012-12",
   [("B3 BiTurbo 360", "ALPINA-N54-3.0BT", 500), ("B3 BiTurbo 370", "ALPINA-N54-3.0BT", 500, {"debut": "2010-01"}), ("B3 S BiTurbo 400", "ALPINA-N54-3.0BT", 540, {"debut": "2010-09"})],
   portes=4, reservoir=63, remarques="Berline, coupé, cabriolet, Touring")
mg(L, "D3", "E90", "1", "2005-09", "2012-12", [("D3 2.0 200", "ALPINA-M47-2.0D", 410), ("D3 Bi-Turbo 214", "ALPINA-M47-2.0D", 450, {"debut": "2008-09"})],
   portes=4, reservoir=60, remarques="Berline, coupé, Touring")
mg(L, "B7", "F01", "1", "2009-09", "2015-06", [("B7 BiTurbo 507", "ALPINA-N63-4.4BT", 700, {"fin": "2012-06"}), ("B7 BiTurbo 540", "ALPINA-N63-4.4BT", 730, {"debut": "2012-07"})],
   portes=4, reservoir=80, remarques="Normal et Lang, Allrad")
mg(L, "B5", "F10", "1", "2010-09", "2017-02",
   [("B5 BiTurbo 507", "ALPINA-N63-4.4BT", 700, {"fin": "2012-06"}), ("B5 BiTurbo 540", "ALPINA-N63-4.4BT", 730, {"debut": "2012-07", "fin": "2014-12"}),
    ("B5 BiTurbo Edition 50 600", "ALPINA-N63-4.4BT", 800, {"debut": "2015-01"})], portes=4, reservoir=70, remarques="Berline et Touring")
mg(L, "D5", "F10", "1", "2012-09", "2017-02", [("D5 BiTurbo 350", "ALPINA-N57-3.0D", 700)], portes=4, reservoir=70)
mg(L, "B6", "F12", "1", "2011-09", "2018-06", [("B6 BiTurbo 540", "ALPINA-N63-4.4BT", 730), ("B6 BiTurbo 600", "ALPINA-N63-4.4BT", 800, {"debut": "2015-01"})],
   portes=2, places=4, reservoir=70, remarques="Coupé, cabriolet, Gran Coupé")
mg(L, "B3", "F30", "1", "2013-03", "2019-06", [("B3 BiTurbo 410", "ALPINA-N55-3.0BT", 600), ("B3 S BiTurbo 440", "ALPINA-N55-3.0BT", 660, {"debut": "2017-03"})],
   portes=4, reservoir=60, remarques="Berline et Touring, Allrad")
mg(L, "D3", "F30", "1", "2013-09", "2019-06", [("D3 BiTurbo 350", "ALPINA-N57-3.0D", 700)], portes=4, reservoir=57, remarques="Berline et Touring")
mg(L, "B4", "F32", "1", "2014-09", "2020-06", [("B4 BiTurbo 410", "ALPINA-N55-3.0BT", 600), ("B4 S BiTurbo 440", "ALPINA-N55-3.0BT", 660, {"debut": "2017-03"})],
   portes=2, places=4, reservoir=60, remarques="Coupé et cabriolet")
mg(L, "D4", "F32", "1", "2017-03", "2020-06", [("D4 S 388", "ALPINA-B57-3.0D", 800)], portes=2, places=4, reservoir=57, remarques="Coupé et cabriolet")

# ---------------------------------------------------------------- 2016-2025
mg(L, "B7", "G11", "1", "2016-09", "2022-12", [("B7 BiTurbo 608", "ALPINA-N63-4.4BT", 800)], portes=4, reservoir=78, remarques="Normal et Lang, Allrad ; restylage 2019")
mg(L, "B5", "G30", "1", "2017-03", "2023-12", [("B5 BiTurbo 608", "ALPINA-N63-4.4BT", 800, {"fin": "2020-06"}), ("B5 GT 634", "ALPINA-N63-4.4BT", 850, {"debut": "2022-09"}),
                                                ("B5 BiTurbo 621", "ALPINA-N63-4.4BT", 800, {"debut": "2020-07"})], portes=4, reservoir=68, remarques="Berline et Touring")
mg(L, "D5", "G30", "1", "2017-09", "2023-12", [("D5 S 388", "ALPINA-B57-3.0D", 800, {"fin": "2020-06"}), ("D5 S 408", "ALPINA-B57-3.0D", 800, {"debut": "2020-07"})],
   portes=4, reservoir=68)
mg(L, "XD3", "G01", "1", "2018-03", "2024-06", [("XD3 BiTurbo 388", "ALPINA-B57-3.0D", 770), ("XD3 333", "ALPINA-B57-3.0D", 730, {"debut": "2020-07"})], reservoir=68,
   remarques="Base BMW X3")
mg(L, "XD4", "G02", "1", "2018-03", "2024-06", [("XD4 BiTurbo 388", "ALPINA-B57-3.0D", 770)], reservoir=68, remarques="Base BMW X4")
mg(L, "B3", "G20", "1", "2019-09", "2022-05", [("B3 462", "ALPINA-S58-3.0BT", 700)], portes=4, reservoir=59, remarques="Berline et Touring, Allrad")
mg(L, "B3", "G20", "2", "2022-06", "2025-11", [("B3 495", "ALPINA-S58-3.0BT", 730), ("B3 GT 529", "ALPINA-S58-3.0BT", 730, {"debut": "2024-06"})], portes=4, reservoir=59,
   remarques="Restylage ; dernière B3 GT Touring produite en novembre 2025")
mg(L, "D3 S", "G20", "1", "2020-03", "2025-06", [("D3 S 355", "ALPINA-B57-3.0D", 730)], portes=4, reservoir=59, remarques="Berline et Touring (micro-hybride)")
mg(L, "B4 Gran Coupé", "G26", "1", "2022-01", "2025-11", [("B4 495", "ALPINA-S58-3.0BT", 730), ("B4 GT 529", "ALPINA-S58-3.0BT", 730, {"debut": "2024-06"})],
   reservoir=59, remarques="Gran Coupé 5 portes")
mg(L, "B8 Gran Coupé", "G16", "1", "2021-09", "2025-12", [("B8 621", "ALPINA-N63-4.4BT", 800), ("B8 GT 634", "ALPINA-N63-4.4BT", 850, {"debut": "2025-01"})],
   reservoir=68, remarques="B8 GT limitée à 99 ex.")
mg(L, "XB7", "G07", "1", "2020-03", "2026-06", [("XB7 621", "ALPINA-N63-4.4BT", 800, {"fin": "2022-06"}), ("XB7 631", "ALPINA-N63-4.4BT", 800, {"debut": "2022-07"})],
   places=7, reservoir=83, remarques="Base BMW X7 ; XB7 Manufaktur (120 ex., Amérique du Nord) en 2026 ; fin indicative")

MOT = Motorisations("Alpina", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Alpina": L}
MOTEURS = MOT.moteurs()
