"""Subaru et Subaru STI : générations, phases, motorisations (marché européen) et moteurs liés.
Subaru : 360, Leone, Justy, SVX, Legacy, Outback, Impreza, Forester, XV / Crosstrek, Levorg, Tribeca, Trezia, BRZ, WRX (Amérique
du Nord), Solterra, Uncharted et E-Outback. Subaru STI : Impreza WRX STI (GC8, 22B, GDB, GRB), WRX STI (VA), S209 et Type RA.
Moteurs boxer Subaru (EA, EJ, EZ, FB, FA, EE diesel) ajoutés ; FA20 / FA24 (BRZ), moteurs de la Trezia et plateforme électrique
e-TNGA repris de toyota.py (mêmes codes). Données anciennes indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .toyota import FAMILLES as FAMILLES_TOYOTA

E_, D = "ESS", "DSL"
C, B, P = "CHAINE", "COURROIE", "PLAT"


def bx(t, l, rpm, nmrpm, d=B, c=E_, n=4, q=4.5):
    return f(t, c, l, d, n, rpm, nmrpm, "5W30", q, 15000, a=P)


SUBARU = {
    "EK31-0.36": f("ATM", E_, 0.36, "NC", 2, 4500, 3000, "SAE30", 2.0, 3000),
    "EA71-1.6": bx("ATM", 1.6, 5200, 3600, d="NC"), "EA81-1.8": bx("ATM", 1.8, 5200, 3600, d="NC"), "EA82-1.8": bx("ATM", 1.8, 5600, 3600),
    "EA82-1.8T": bx("TURBO", 1.8, 5200, 2800),
    "EF-1.2": f("ATM", E_, 1.2, B, 3, 5600, 3600, "10W40", 3.0, 10000),
    "EG33-3.3": bx("ATM", 3.3, 5400, 4400, n=6, q=5.5),
    "EJ16-1.6": bx("ATM", 1.6, 6000, 4000), "EJ18-1.8": bx("ATM", 1.8, 5600, 4000), "EJ20-2.0": bx("ATM", 2.0, 6000, 4000),
    "EJ22-2.2": bx("ATM", 2.2, 5600, 4400), "EJ25-2.5": bx("ATM", 2.5, 5600, 4000), "EJ20T-2.0": bx("TURBO", 2.0, 6000, 3600), "EJ25T-2.5": bx("TURBO", 2.5, 6000, 3600),
    "EZ30-3.0": bx("ATM", 3.0, 6600, 4200, d=C, n=6, q=6.0), "EZ36-3.6": bx("ATM", 3.6, 6000, 4400, d=C, n=6, q=6.0),
    "FB16-1.6": bx("ATM", 1.6, 6200, 4000, d=C), "FB20-2.0": bx("ATM", 2.0, 6200, 4200, d=C), "FB25-2.5": bx("ATM", 2.5, 5800, 4000, d=C),
    "FB20-EBOXER": bx("HYB_TE", 2.0, 5600, 4000, d=C), "FA16DIT-1.6T": bx("TURBO", 1.6, 4800, 1800, d=C), "FA20DIT-2.0T": bx("TURBO", 2.0, 5600, 2000, d=C),
    "FA24DIT-2.4T": bx("TURBO", 2.4, 5600, 2000, d=C),
    "EE20-2.0D": bx("TURBO", 2.0, 3600, 1800, d=C, c=D, q=5.0),
}
TOYOTA = {k: FAMILLES_TOYOTA[k] for k in ("FA20", "FA24", "1NR-FE", "1ND-TV", "eTNGA-EV")}
FAMILLES = {**SUBARU, **TOYOTA}


def motoriste(fam):
    return "Toyota" if fam in ("1NR-FE", "1ND-TV", "eTNGA-EV") else "Subaru"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Subaru", motoriste)
L, STI = [], []
IND = "données indicatives"

# ---------------------------------------------------------------- anciennes
mg(L, "360", "K111", "1", "1958-03", "1971-05", [("0.36 2T 16", "EK31-0.36", 30)], portes=2, places=4, reservoir=25, remarques="Kei car, bicylindre deux temps ; " + IND)
mg(L, "Leone", "A10", "1", "1971-10", "1979-06", [("1.4 80", "EA71-1.6", 108, {"remarques": "EA63 1.4 rattaché à la famille EA71"}), ("1.6 85", "EA71-1.6", 123)],
   portes=4, places=5, reservoir=50, remarques="Berline, coupé, break 4WD ; " + IND)
mg(L, "Leone", "AB", "1", "1979-06", "1984-06", [("1.6 72", "EA71-1.6", 117), ("1.8 82", "EA81-1.8", 137)], portes=4, places=5, reservoir=50, remarques="1600 / 1800 4WD ; " + IND)
mg(L, "Leone", "AA", "1", "1984-07", "1994-12", [("1.8 90", "EA82-1.8", 141), ("1.8 Turbo 136", "EA82-1.8T", 196)], portes=4, places=5, reservoir=60,
   remarques="1.8 4WD berline, break, coupé ; " + IND)
mg(L, "Justy", "KA", "1", "1984-02", "1994-12", [("1.2 67", "EF-1.2", 96)], portes=5, places=5, reservoir=35, remarques="3 et 5 portes, 4WD à la demande ; " + IND)
mg(L, "SVX", "CX", "1", "1991-09", "1996-12", [("3.3 H6 230", "EG33-3.3", 309)], portes=2, places=4, reservoir=70, remarques="Coupé GT, vitres « avion » ; " + IND)

# ---------------------------------------------------------------- Legacy / Outback
mg(L, "Legacy", "BC", "1", "1989-02", "1994-09", [("1.8 103", "EJ18-1.8", 147), ("2.0 116", "EJ20-2.0", 172), ("2.2 136", "EJ22-2.2", 186), ("Turbo 2.0 200", "EJ20T-2.0", 260)],
   portes=4, places=5, reservoir=60, remarques="Berline et break ; " + IND)
mg(L, "Legacy", "BD", "1", "1994-10", "1998-12", [("2.0 115", "EJ20-2.0", 172), ("2.2 128", "EJ22-2.2", 186), ("2.5 150", "EJ25-2.5", 223)], portes=4, places=5, reservoir=60,
   remarques="Berline et break ; " + IND)
mg(L, "Legacy", "BE", "1", "1998-12", "2003-08", [("2.0 125", "EJ20-2.0", 184), ("2.5 156", "EJ25-2.5", 223), ("3.0 H6 209", "EZ30-3.0", 282, {"debut": "2000-09"})],
   portes=4, places=5, reservoir=64, remarques="Berline et break ; " + IND)
mg(L, "Legacy", "BL", "1", "2003-09", "2009-08",
   [("2.0 137", "EJ20-2.0", 187), ("2.5 165", "EJ25-2.5", 227), ("2.0 Turbo 245", "EJ20T-2.0", 343, {"fin": "2006-12"}), ("3.0 H6 245", "EZ30-3.0", 297), ("2.0 D 150", "EE20-2.0D", 350, {"debut": "2008-03"})],
   portes=4, places=5, reservoir=64, remarques="Berline et break")
mg(L, "Legacy", "BM", "1", "2009-09", "2014-12", [("2.0 150", "FB20-2.0", 196), ("2.5 167", "EJ25-2.5", 229), ("2.0 D 150", "EE20-2.0D", 350)], portes=4, places=5, reservoir=65,
   remarques="Berline et break ; retiré d'Europe")
mg(L, "Outback", "BG", "1", "1995-09", "1999-12", [("2.5 150", "EJ25-2.5", 223)], portes=5, places=5, reservoir=60, remarques="Legacy Outback ; " + IND)
mg(L, "Outback", "BE", "2", "2000-01", "2003-08", [("2.5 156", "EJ25-2.5", 223), ("3.0 H6 209", "EZ30-3.0", 282)], portes=5, places=5, reservoir=64, remarques=IND)
mg(L, "Outback", "BP", "1", "2003-09", "2009-08", [("2.5 165", "EJ25-2.5", 227), ("3.0 H6 245", "EZ30-3.0", 297), ("2.0 D 150", "EE20-2.0D", 350, {"debut": "2008-03"})],
   portes=5, places=5, reservoir=64)
mg(L, "Outback", "BR", "1", "2009-09", "2014-12", [("2.5 167", "EJ25-2.5", 229), ("3.6 H6 260", "EZ36-3.6", 335), ("2.0 D 150", "EE20-2.0D", 350)], portes=5, places=5, reservoir=65)
mg(L, "Outback", "BS", "1", "2015-01", "2020-12", [("2.5 175", "FB25-2.5", 235), ("2.0 D 150", "EE20-2.0D", 350, {"fin": "2018-12"})], portes=5, places=5, reservoir=60)
mg(L, "Outback", "BT", "1", "2021-01", "2025-12", [("2.5 169", "FB25-2.5", 252)], portes=5, places=5, reservoir=63, remarques="Retiré d'Europe fin 2025")
mg(L, "E-Outback", "e-SGP", "1", "2026-07", None, [("AWD 343", "eTNGA-EV", 338, el(75))], portes=5, places=5, reservoir=0,
   remarques="Électrique (Trailseeker hors Europe), base Toyota bZ4X Touring ; " + IND)

# ---------------------------------------------------------------- Impreza / WRX
mg(L, "Impreza", "GC", "1", "1993-01", "2000-12",
   [("1.6 90", "EJ16-1.6", 130), ("1.8 103", "EJ18-1.8", 147), ("2.0 115", "EJ20-2.0", 172), ("GT 2.0 Turbo 211", "EJ20T-2.0", 290), ("GT 2.0 Turbo 218", "EJ20T-2.0", 294, {"debut": "1998-09"})],
   portes=4, places=5, reservoir=50, remarques="Berline, 5 portes et coupé ; WRX STI dans Subaru STI ; " + IND)
mg(L, "Impreza", "GD", "1", "2001-01", "2007-12",
   [("1.5 100", "EJ16-1.6", 140, {"debut": "2005-09", "remarques": "EJ15 rattaché à la famille 1.6"}), ("1.6 95", "EJ16-1.6", 143), ("2.0 125", "EJ20-2.0", 184), ("WRX 2.0 Turbo 218", "EJ20T-2.0", 294, {"fin": "2005-08"}),
    ("WRX 2.5 Turbo 230", "EJ25T-2.5", 320, {"debut": "2005-09"})], portes=4, places=5, reservoir=60, remarques="Berline et break ; " + IND)
mg(L, "Impreza", "GE", "1", "2008-01", "2011-12", [("1.5 107", "EJ16-1.6", 142), ("2.0 150", "EJ20-2.0", 196), ("WRX 2.5 Turbo 230", "EJ25T-2.5", 320), ("2.0 D 150", "EE20-2.0D", 350, {"debut": "2009-01"})],
   portes=5, places=5, reservoir=64, remarques="5 portes et berline")
mg(L, "Impreza", "GJ", "1", "2012-01", "2016-12", [("1.6 114", "FB16-1.6", 150), ("2.0 150", "FB20-2.0", 196)], portes=5, places=5, reservoir=55)
mg(L, "Impreza", "GT", "1", "2017-01", "2022-12", [("1.6 114", "FB16-1.6", 150), ("2.0 156", "FB20-2.0", 196), ("e-Boxer 2.0 150", "FB20-EBOXER", 194, {"debut": "2020-01"})],
   portes=5, places=5, reservoir=50)
mg(L, "Impreza", "GU", "1", "2023-03", None, [("e-Boxer 2.0 136", "FB20-EBOXER", 182)], portes=5, places=5, reservoir=48, remarques="Fin de production pour l'Europe annoncée")
mg(L, "WRX", "VA", "1", "2014-01", "2021-12", [("2.0 Turbo 272", "FA20DIT-2.0T", 350)], portes=4, places=5, reservoir=60, remarques="Amérique du Nord (Europe : WRX STI seulement) ; " + IND)
mg(L, "WRX", "VB", "1", "2022-01", None, [("2.4 Turbo 275", "FA24DIT-2.4T", 350)], portes=4, places=5, reservoir=63, remarques="Amérique du Nord ; " + IND)
mg(L, "Levorg", "VM", "1", "2015-06", "2020-12", [("1.6 Turbo 170", "FA16DIT-1.6T", 250)], portes=5, places=5, reservoir=60, remarques="Break")
mg(L, "BRZ", "ZC6", "1", "2012-06", "2020-12", [("2.0 D-4S 200", "FA20", 205)], portes=2, places=4, reservoir=50, remarques="Coupé propulsion (jumeau Toyota GT86)")
mg(L, "BRZ", "ZD8", "1", "2022-01", "2024-12", [("2.4 234", "FA24", 250)], portes=2, places=4, reservoir=50, remarques="Jumeau Toyota GR86 ; vendu peu de temps en Europe")

# ---------------------------------------------------------------- SUV
mg(L, "Forester", "SF", "1", "1997-09", "2002-06", [("2.0 122", "EJ20-2.0", 184), ("2.0 Turbo 170", "EJ20T-2.0", 240)], portes=5, places=5, reservoir=60, remarques=IND)
mg(L, "Forester", "SG", "1", "2002-07", "2008-02", [("2.0 125", "EJ20-2.0", 184), ("2.5 Turbo 230", "EJ25T-2.5", 320, {"debut": "2004-01"})], portes=5, places=5, reservoir=60, remarques=IND)
mg(L, "Forester", "SH", "1", "2008-03", "2012-12", [("2.0 150", "EJ20-2.0", 196), ("2.0 D 147", "EE20-2.0D", 350, {"debut": "2008-09"}), ("2.5 Turbo 230", "EJ25T-2.5", 320)],
   portes=5, places=5, reservoir=64)
mg(L, "Forester", "SJ", "1", "2013-01", "2018-08", [("2.0 150", "FB20-2.0", 196), ("2.0 Turbo 240", "FA20DIT-2.0T", 350), ("2.0 D 147", "EE20-2.0D", 350)], portes=5, places=5, reservoir=60)
mg(L, "Forester", "SK", "1", "2018-09", "2024-12", [("e-Boxer 2.0 150", "FB20-EBOXER", 194), ("2.0 156", "FB20-2.0", 196)], portes=5, places=5, reservoir=48)
mg(L, "Forester", "SL", "1", "2025-03", None, [("e-Boxer 2.0 136", "FB20-EBOXER", 182)], portes=5, places=5, reservoir=48, remarques="Fin de production pour l'Europe annoncée")
mg(L, "XV", "GP", "1", "2012-03", "2017-12", [("1.6 114", "FB16-1.6", 150), ("2.0 150", "FB20-2.0", 196), ("2.0 D 147", "EE20-2.0D", 350)], portes=5, places=5, reservoir=60)
mg(L, "XV", "GT", "2", "2018-01", "2022-12", [("1.6 114", "FB16-1.6", 150), ("2.0 156", "FB20-2.0", 196), ("e-Boxer 2.0 150", "FB20-EBOXER", 194, {"debut": "2019-09"})],
   portes=5, places=5, reservoir=48)
mg(L, "Crosstrek", "GU", "2", "2023-03", None, [("e-Boxer 2.0 136", "FB20-EBOXER", 182)], portes=5, places=5, reservoir=48, remarques="Successeur du XV ; fin de production pour l'Europe annoncée")
mg(L, "Tribeca", "WX", "1", "2006-01", "2014-12", [("3.0 H6 245", "EZ30-3.0", 297, {"fin": "2007-12"}), ("3.6 H6 258", "EZ36-3.6", 335, {"debut": "2008-01"})], portes=5, places=7, reservoir=64,
   remarques="B9 Tribeca ; vendu en Europe jusqu'en 2010")
mg(L, "Trezia", "P120", "1", "2011-01", "2016-12", [("1.3 99", "1NR-FE", 125), ("1.4 D 90", "1ND-TV", 190)], portes=5, places=5, reservoir=42, remarques="Jumelle de la Toyota Verso-S")
mg(L, "Solterra", "e-SGP", "1", "2022-11", "2025-12", [("AWD 218", "eTNGA-EV", 337, el(71))], portes=5, places=5, reservoir=0, remarques="Jumeau du Toyota bZ4X")
mg(L, "Solterra", "e-SGP", "2", "2026-01", None, [("AWD 343", "eTNGA-EV", 338, el(73))], portes=5, places=5, reservoir=0, remarques="Restylage")
mg(L, "Uncharted", "e-SGP", "U", "2026-03", None, [("FWD 167", "eTNGA-EV", 268, el(58)), ("AWD 343", "eTNGA-EV", 338, el(75))], portes=5, places=5, reservoir=0,
   remarques="SUV compact électrique, jumeau du Toyota C-HR+")

# ---------------------------------------------------------------- Subaru STI
mg(STI, "Impreza WRX STI", "GC8", "1", "1994-01", "2000-12", [("2.0 Turbo 280", "EJ20T-2.0", 350), ("22B 2.2 Turbo 280", "EJ22-2.2", 363, {"debut": "1998-03", "fin": "1998-12", "remarques": "22B STi (424 ex.), EJ22 turbo"})],
   portes=4, places=5, reservoir=50, remarques="Surtout marché japonais (importations) ; " + IND)
mg(STI, "Impreza WRX STI", "GDB", "1", "2001-01", "2007-12", [("2.0 Turbo 265", "EJ20T-2.0", 343, {"fin": "2004-12"}), ("2.5 Turbo 280", "EJ25T-2.5", 392, {"debut": "2005-01"})],
   portes=4, places=5, reservoir=60, remarques="Versions européennes ; " + IND)
mg(STI, "Impreza WRX STI", "GRB", "1", "2008-01", "2014-06", [("2.5 Turbo 300", "EJ25T-2.5", 407)], portes=5, places=5, reservoir=60, remarques="5 portes puis berline (GVB, 2011)")
mg(STI, "WRX STI", "VA", "1", "2014-07", "2018-12", [("2.5 Turbo 300", "EJ25T-2.5", 407)], portes=4, places=5, reservoir=60, remarques="Dernière STI vendue en Europe")
mg(STI, "WRX STI", "VA", "2", "2018-01", "2021-12", [("Type RA 2.5 Turbo 314", "EJ25T-2.5", 393), ("S209 2.5 Turbo 346", "EJ25T-2.5", 447, {"debut": "2019-01", "fin": "2019-12"})],
   portes=4, places=5, reservoir=60, remarques="Séries spéciales Amérique du Nord ; " + IND)

MOT = Motorisations("Subaru", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(STI)

DETAIL = {"Subaru": L, "Subaru STI": STI}
MOTEURS = MOT.moteurs()
