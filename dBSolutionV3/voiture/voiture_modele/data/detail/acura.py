"""Acura : générations, phases, motorisations (marché nord-américain — Acura n'est pas vendu en Europe) et moteurs liés.
Integra, Legend, NSX, TL, RL/RLX, TSX, RSX, CSX, ILX, TLX, MDX, RDX, ZDX, CDX, ADX.
Puissances converties des hp américains en ch (×1,014, arrondi). Moteurs Honda : familles de honda.py (motoriste « Honda »)
et familles nord-américaines ajoutées ici, au même motoriste. Saisie : (nom, famille, couple_nm[, surcharges]) ;
la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .honda import FAMILLES as FAMILLES_HONDA

E_ = "ESS"
C, B = "CHAINE", "COURROIE"

AJOUTS = {
    "D16A": f("ATM", E_, 1.6, B, 4, 6250, 5500, "10W40", 3.5, 10000),
    "B17A": f("ATM", E_, 1.7, B, 4, 7600, 7000, "10W40", 4.0, 10000),
    "B18": f("ATM", E_, 1.8, B, 4, 6300, 5200, "10W40", 4.0, 10000),
    "C25": f("ATM", E_, 2.5, B, 6, 6000, 4500, "10W40", 4.5, 10000, a="V"),
    "C27": f("ATM", E_, 2.7, B, 6, 6000, 4500, "10W40", 4.5, 10000, a="V"),
    "C35": f("ATM", E_, 3.5, B, 6, 5200, 2800, "10W40", 4.5, 10000, a="V"),
    "G25": f("ATM", E_, 2.5, B, 5, 6300, 3900, "10W40", 4.5, 10000),
    "J32": f("ATM", E_, 3.2, B, 6, 6200, 4700, "5W20", 4.5, 15000, a="V"),
    "J35": f("ATM", E_, 3.5, B, 6, 6200, 4700, "0W20", 4.5, 15000, a="V"),
    "J35-HYB": f("HYB_TE", E_, 3.5, B, 6, 6300, 4700, "0W20", 4.5, 15000, a="V"),
    "J37": f("ATM", E_, 3.7, B, 6, 6300, 5000, "5W20", 4.5, 15000, a="V"),
    "J30-T": f("TURBO", E_, 3.0, B, 6, 5500, 1400, "0W20", 5.7, 15000, a="V"),
    "K20A-USA": f("ATM", E_, 2.0, C, 4, 6500, 4000, "5W20", 4.2, 15000),
    "K23-T": f("TURBO", E_, 2.3, C, 4, 6000, 4500, "5W20", 4.2, 15000),
    "K20C-T": f("TURBO", E_, 2.0, C, 4, 6500, 1600, "0W20", 4.5, 15000),
    "R20": f("ATM", E_, 2.0, C, 4, 6500, 4300, "0W20", 3.7, 15000),
    "IMA-1.5-ILX": f("HYB_TE", E_, 1.5, C, 4, 5500, 1000, "0W20", 3.6, 15000),
    "ZDX-EV": electrique(),
}
HONDA = ("K24", "C30", "C32", "NSX-HYB-3.5", "L15-VTEC-T", "K20C1")
FAMILLES = {**{k: FAMILLES_HONDA[k] for k in HONDA}, **AJOUTS}


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Honda")
L = []
NA = "Marché nord-américain"

# ---------------------------------------------------------------- berlines / coupés
mg(L, "Integra", "DA", "1", "1986-03", "1993-12",
   [("1.6 DOHC 115", "D16A", 141, {"fin": "1989-12"}), ("1.8 RS/LS 132", "B18", 165, {"debut": "1990-01"}), ("GS-R 1.7 VTEC 162", "B17A", 157, {"debut": "1992-01"})],
   portes=3, reservoir=50, remarques=NA + " ; 3 et 5 portes ; données indicatives")
mg(L, "Integra", "DC2", "1", "1994-01", "2001-12",
   [("LS 1.8 144", "B18", 172), ("GS-R 1.8 VTEC 172", "B18", 174), ("Type R 1.8 197", "B18", 178, {"debut": "1997-06"})], portes=3, reservoir=50, remarques=NA + " ; coupé 3 portes et berline")
mg(L, "RSX", "DC5", "1", "2002-01", "2006-12",
   [("2.0 162", "K20A-USA", 191), ("Type-S 2.0 203", "K20A-USA", 191, {"fin": "2004-12"}), ("Type-S 2.0 213", "K20A-USA", 194, {"debut": "2005-01"})],
   portes=3, places=4, reservoir=50, remarques=NA + " ; vendue Honda Integra au Japon")
mg(L, "Integra", "DE4", "1", "2022-06", None,
   [("1.5 VTEC Turbo 203", "L15-VTEC-T", 260), ("Type S 2.0 VTEC Turbo 325", "K20C1", 420, {"debut": "2023-06"})], reservoir=47,
   remarques=NA + " ; liftback 5 portes ; boîte manuelle abandonnée en 2026")
mg(L, "Legend", "KA", "1", "1986-03", "1990-12", [("2.5 V6 153", "C25", 205), ("2.7 V6 162", "C27", 220, {"debut": "1988-01"})], portes=4, reservoir=68,
   remarques=NA + " ; berline et coupé ; données indicatives")
mg(L, "Legend", "KA7", "1", "1991-01", "1995-12", [("3.2 V6 203", "C32", 285), ("Type II 3.2 V6 233", "C32", 305, {"debut": "1993-01"})], portes=4, reservoir=68,
   remarques=NA + " ; données indicatives")
mg(L, "TL", "UA2", "1", "1996-01", "1998-12", [("2.5 TL 178", "G25", 230), ("3.2 TL 203", "C32", 285)], portes=4, reservoir=65, remarques=NA)
mg(L, "TL", "UA5", "1", "1999-01", "2003-12", [("3.2 V6 228", "J32", 293), ("Type-S 3.2 V6 264", "J32", 314, {"debut": "2002-01"})], portes=4, reservoir=65,
   remarques=NA + " ; coupé CL dérivé")
mg(L, "TL", "UA6", "1", "2004-01", "2008-12", [("3.2 V6 274", "J32", 323), ("Type-S 3.5 V6 290", "J35", 346, {"debut": "2007-01"})], portes=4, reservoir=65, remarques=NA)
mg(L, "TL", "UA8", "1", "2009-01", "2014-12", [("3.5 V6 284", "J35", 344), ("SH-AWD 3.7 V6 309", "J37", 369)], portes=4, reservoir=70, remarques=NA)
mg(L, "TSX", "CL9", "1", "2004-01", "2008-12", [("2.4 203", "K24", 225)], portes=4, reservoir=65, remarques=NA + " ; Honda Accord européenne")
mg(L, "TSX", "CU2", "1", "2009-01", "2014-12", [("2.4 204", "K24", 232), ("V6 3.5 284", "J35", 344, {"debut": "2010-01"})], portes=4, reservoir=70,
   remarques=NA + " ; Sport Wagon (2011)")
mg(L, "CSX", "FD", "1", "2006-01", "2011-12", [("2.0 157", "R20", 189), ("Type-S 2.0 200", "K20A-USA", 189, {"debut": "2007-01"})], portes=4, reservoir=50,
   remarques="Marché canadien (Civic berline)")
mg(L, "ILX", "DE1", "1", "2013-01", "2015-12",
   [("2.0 152", "R20", 190), ("2.4 204", "K24", 230), ("Hybrid 1.5 113", "IMA-1.5-ILX", 172)], portes=4, reservoir=50, remarques=NA)
mg(L, "ILX", "DE1", "2", "2016-01", "2022-06", [("2.4 204", "K24", 245)], portes=4, reservoir=50, remarques=NA + " ; restylages 2016 et 2019")
mg(L, "RL", "KA9", "1", "1996-01", "2004-12", [("3.5 V6 213", "C35", 305), ("3.5 V6 228", "C35", 312, {"debut": "1999-01"})], portes=4, reservoir=68, remarques=NA)
mg(L, "RL", "KB1", "1", "2005-01", "2012-12", [("3.5 V6 SH-AWD 294", "J35", 353), ("3.7 V6 SH-AWD 304", "J37", 366, {"debut": "2009-01"})], portes=4, reservoir=73,
   remarques=NA)
mg(L, "RLX", "KC2", "1", "2014-01", "2020-12", [("3.5 V6 314", "J35", 369), ("Sport Hybrid SH-AWD 382", "J35-HYB", 461)], portes=4, reservoir=70, remarques=NA)
mg(L, "TLX", "UB1", "1", "2015-01", "2020-06", [("2.4 210", "K24", 247), ("3.5 V6 294", "J35", 361)], portes=4, reservoir=65, remarques=NA + " ; restylage 2018")
mg(L, "TLX", "UB5", "1", "2020-09", "2025-07", [("2.0 Turbo 276", "K20C-T", 380), ("Type S 3.0 V6 Turbo 360", "J30-T", 480, {"debut": "2021-06"})], portes=4,
   reservoir=65, remarques=NA + " ; production arrêtée en juillet 2025")
mg(L, "NSX", "NA1", "1", "1991-01", "2005-12", [("3.0 V6 274", "C30", 284, {"fin": "1996-12"}), ("3.2 V6 294", "C32", 305, {"debut": "1997-01"})],
   portes=2, places=2, reservoir=70, remarques=NA + " ; NSX-T targa")
mg(L, "NSX", "NC1", "1", "2017-01", "2022-11", [("3.5 V6 Hybrid 581", "NSX-HYB-3.5", 646), ("Type S 3.5 V6 Hybrid 608", "NSX-HYB-3.5", 667, {"debut": "2022-01"})],
   portes=2, places=2, reservoir=59, remarques=NA)

# ---------------------------------------------------------------- SUV
mg(L, "MDX", "YD1", "1", "2001-01", "2006-12", [("3.5 V6 243", "J35", 332, {"fin": "2002-12"}), ("3.5 V6 269", "J35", 342, {"debut": "2003-01"})],
   places=7, reservoir=75, remarques=NA)
mg(L, "MDX", "YD2", "1", "2007-01", "2013-12", [("3.7 V6 304", "J37", 373)], places=7, reservoir=79, remarques=NA)
mg(L, "MDX", "YD3", "1", "2014-01", "2020-12", [("3.5 V6 294", "J35", 361), ("Sport Hybrid 325", "J35-HYB", 393, {"debut": "2017-01"})], places=7, reservoir=73,
   remarques=NA)
mg(L, "MDX", "YD4", "1", "2021-02", None, [("3.5 V6 294", "J35", 361), ("Type S 3.0 V6 Turbo 360", "J30-T", 480, {"debut": "2021-09", "fin": "2026-12"})],
   places=7, reservoir=70, remarques=NA + " ; restylage 2024 ; Type S arrêtée après le millésime 2026")
mg(L, "RDX", "TB1", "1", "2007-01", "2012-12", [("2.3 Turbo 243", "K23-T", 353)], reservoir=68, remarques=NA)
mg(L, "RDX", "TB3", "1", "2013-01", "2018-06", [("3.5 V6 277", "J35", 342), ("3.5 V6 283", "J35", 340, {"debut": "2016-01"})], reservoir=60, remarques=NA)
mg(L, "RDX", "TC1", "1", "2018-06", "2026-06", [("2.0 Turbo 276", "K20C-T", 380)], reservoir=65,
   remarques=NA + " ; restylage 2022 ; production arrêtée en 2026 (successeur hybride annoncé), date indicative")
mg(L, "ZDX", "YB1", "1", "2009-12", "2013-12", [("3.7 V6 304", "J37", 366)], reservoir=79, remarques=NA + " ; SUV coupé")
mg(L, "ZDX", "BEV3", "1", "2024-03", "2025-09", [("A-Spec RWD 363", "ZDX-EV", 437, el(102)), ("Type S AWD 507", "ZDX-EV", 738, el(102))], reservoir=0,
   remarques=NA + " ; SUV électrique sur base GM, arrêté en septembre 2025")
mg(L, "CDX", "TC", "1", "2016-07", "2022-12", [("1.5 Turbo 185", "L15-VTEC-T", 245)], reservoir=50, remarques="Marché chinois")
mg(L, "ADX", "RV", "1", "2024-12", None, [("1.5 VTEC Turbo 193", "L15-VTEC-T", 240)], reservoir=50, remarques=NA + " ; SUV compact (base HR-V américain)")

MOT = Motorisations("Honda", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Acura": L}
MOTEURS = MOT.moteurs()
