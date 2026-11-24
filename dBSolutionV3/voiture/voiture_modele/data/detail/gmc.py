"""GMC : générations, motorisations (marché nord-américain — GMC n'est pas vendu en Europe) et moteurs liés.
Syclone / Typhoon, Envoy, Sierra 1500, Sierra HD, Canyon, Yukon / Yukon XL, Acadia, Terrain, Savana, Hummer EV, Sierra EV.
Moteurs GM : familles et codes de chevrolet.py (motoriste « Chevrolet ») et familles ajoutées ici au même motoriste.
Puissances américaines converties en ch (×1,014). Générations antérieures à 2007 non reprises, sauf Syclone/Typhoon et Envoy.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET

E_, D = "ESS", "DSL"
C = "CHAINE"


def v8(t, carb, l, rpm, nmrpm, q, km=12000):
    return f(t, carb, l, C, 8, rpm, nmrpm, "5W30" if carb == E_ else "15W40", q, km, a="V")


CHEVROLET = ("L84-5.3", "L87-6.2", "L83-5.3", "LS3-6.2", "DURAMAX-3.0", "DURAMAX-2.8", "GM-2.7T", "GM-1.5T", "GM-2.0T", "GM-2.5T", "GM-2.5",
             "GM-3.6-V6", "GM-2.4", "VCDI-1.7", "ULTIUM")
AJOUTS = {
    "LB4-4.3T": f("TURBO", E_, 4.3, C, 6, 4400, 3600, "5W30", 4.7, 7500, a="V"),
    "LV3-4.3": f("ATM", E_, 4.3, C, 6, 5300, 3900, "5W30", 5.7, 12000, a="V"),
    "LY2-4.8": v8("ATM", E_, 4.8, 5600, 4600, 5.7), "LMG-5.3": v8("ATM", E_, 5.3, 5200, 4000, 5.7), "L92-6.2": v8("ATM", E_, 6.2, 5700, 4300, 5.7),
    "L96-6.0": v8("ATM", E_, 6.0, 5400, 4200, 5.7), "L8T-6.6": v8("ATM", E_, 6.6, 5200, 4000, 7.6), "L5P-6.6D": v8("TURBO", D, 6.6, 2800, 1600, 9.5, 12000),
    "LL8-4.2": f("ATM", E_, 4.2, C, 6, 6000, 4600, "5W30", 6.6, 12000),
    "LLV-2.9": f("ATM", E_, 2.9, C, 4, 5600, 2800, "5W30", 4.7, 12000),
    "LLR-3.7": f("ATM", E_, 3.7, C, 5, 5600, 4600, "5W30", 5.7, 12000),
    "LF1-3.0": f("ATM", E_, 3.0, C, 6, 7000, 5100, "5W30", 5.7, 12000, a="V"),
}
FAMILLES = {**{k: FAMILLES_CHEVROLET[k] for k in CHEVROLET}, **AJOUTS}


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Chevrolet")
L = []
NA = "Marché nord-américain"

mg(L, "Syclone", "GMT325", "S", "1991-01", "1991-12", [("Syclone 4.3 V6 Turbo 284", "LB4-4.3T", 475)], portes=2, places=2, reservoir=76,
   remarques=NA + " ; pick-up sportif (base S-15) ; données indicatives")
mg(L, "Typhoon", "GMT325", "T", "1992-01", "1993-12", [("Typhoon 4.3 V6 Turbo 284", "LB4-4.3T", 475)], places=4, reservoir=76,
   remarques=NA + " ; SUV sportif (base Jimmy) ; données indicatives")
mg(L, "Envoy", "GMT360", "1", "2002-01", "2009-12", [("4.2 I6 279", "LL8-4.2", 373), ("4.2 I6 295", "LL8-4.2", 373, {"debut": "2006-01"}), ("5.3 V8 294", "LMG-5.3", 441, {"debut": "2005-01"})],
   reservoir=83, remarques=NA + " ; Envoy XL 7 places (2002-2006) ; données indicatives")

# ---------------------------------------------------------------- pick-up
mg(L, "Sierra 1500", "GMT900", "1", "2007-01", "2013-12", [("4.8 V8 306", "LY2-4.8", 413), ("5.3 V8 319", "LMG-5.3", 454), ("Denali 6.2 V8 409", "L92-6.2", 565)],
   portes=4, reservoir=98, remarques=NA)
mg(L, "Sierra 1500", "K2XX", "1", "2014-01", "2018-12", [("4.3 V6 289", "LV3-4.3", 413), ("5.3 V8 360", "L83-5.3", 519), ("Denali 6.2 V8 426", "L87-6.2", 623)], portes=4, reservoir=98,
   remarques=NA)
mg(L, "Sierra 1500", "T1XX", "1", "2019-01", None,
   [("2.7 Turbo 314", "GM-2.7T", 583), ("5.3 V8 360", "L84-5.3", 519), ("6.2 V8 426", "L87-6.2", 623), ("3.0 Duramax 309", "DURAMAX-3.0", 678)], portes=4, reservoir=91,
   remarques=NA + " ; AT4, Denali ; restylage 2022")
mg(L, "Sierra HD", "T1XX", "H", "2020-01", None,
   [("2500HD 6.6 V8 407", "L8T-6.6", 631), ("2500HD 6.6 Duramax 451", "L5P-6.6D", 1234, {"fin": "2023-12"}), ("2500HD 6.6 Duramax 477", "L5P-6.6D", 1322, {"debut": "2024-01"})],
   portes=4, reservoir=136, remarques=NA + " ; 2500HD et 3500HD")
mg(L, "Canyon", "GMT355", "1", "2004-01", "2012-12", [("2.9 187", "LLV-2.9", 258, {"debut": "2007-01"}), ("3.7 I5 245", "LLR-3.7", 325, {"debut": "2007-01"}),
                                                     ("5.3 V8 304", "LMG-5.3", 434, {"debut": "2009-01"})], portes=4, reservoir=74, remarques=NA + " ; données indicatives")
mg(L, "Canyon", "GMT700", "2", "2015-01", "2022-12", [("2.5 203", "GM-2.5", 259), ("3.6 V6 312", "GM-3.6-V6", 373), ("2.8 Duramax 184", "DURAMAX-2.8", 500, {"debut": "2016-01"})],
   portes=4, reservoir=79, remarques=NA)
mg(L, "Canyon", "31XX", "1", "2023-01", None, [("2.7 Turbo 314", "GM-2.7T", 583)], portes=4, reservoir=80, remarques=NA + " ; AT4X")
mg(L, "Sierra EV", "BT1", "S", "2024-07", None, [("Denali Edition 1 765", "ULTIUM", 1064, el(205)), ("Elevation 517", "ULTIUM", 834, el(200, debut="2025-06"))], portes=4, reservoir=0,
   remarques=NA + " ; puissance Max Power ; données indicatives")
mg(L, "Hummer EV", "BT1", "H", "2022-01", None,
   [("Pickup Edition 1 1014", "ULTIUM", 1500, el(213)), ("Pickup EV3X 842", "ULTIUM", 1300, el(213, debut="2023-01")), ("Pickup EV2X 578", "ULTIUM", 830, el(160, debut="2023-06")),
    ("SUV EV3X 842", "ULTIUM", 1300, el(170, debut="2024-01")), ("SUV EV2X 578", "ULTIUM", 830, el(170, debut="2024-01"))],
   portes=4, reservoir=0, remarques=NA + " ; pick-up et SUV ; couples à la roue non repris (couple moteur indicatif)")

# ---------------------------------------------------------------- SUV / van
mg(L, "Yukon", "GMT900", "1", "2007-01", "2014-12", [("5.3 V8 324", "LMG-5.3", 454), ("Denali 6.2 V8 409", "L92-6.2", 565)], places=8, reservoir=98, remarques=NA + " ; Yukon et Yukon XL")
mg(L, "Yukon", "K2XL", "1", "2015-01", "2020-12", [("5.3 V8 360", "L83-5.3", 519), ("Denali 6.2 V8 426", "L87-6.2", 623)], places=8, reservoir=98, remarques=NA + " ; Yukon et Yukon XL")
mg(L, "Yukon", "T1XX", "Y", "2021-01", None, [("5.3 V8 360", "L84-5.3", 519), ("6.2 V8 426", "L87-6.2", 623), ("3.0 Duramax 309", "DURAMAX-3.0", 678)], places=8, reservoir=91,
   remarques=NA + " ; Yukon et Yukon XL ; restylage 2025")
mg(L, "Acadia", "Lambda", "1", "2007-01", "2016-12", [("3.6 V6 279", "GM-3.6-V6", 366), ("3.6 V6 292", "GM-3.6-V6", 360, {"debut": "2009-01"})], places=8, reservoir=83, remarques=NA)
mg(L, "Acadia", "C1XX", "1", "2017-01", "2023-12", [("2.5 196", "GM-2.5", 255), ("2.0 Turbo 233", "GM-2.0T", 350, {"debut": "2020-01"}), ("3.6 V6 314", "GM-3.6-V6", 367)],
   places=7, reservoir=73, remarques=NA)
mg(L, "Acadia", "C1XX", "2", "2024-01", None, [("2.5 Turbo 333", "GM-2.5T", 441)], places=7, reservoir=82, remarques=NA + " ; 3e génération")
mg(L, "Terrain", "Theta", "1", "2010-01", "2017-12", [("2.4 185", "GM-2.4", 232), ("3.0 V6 268", "LF1-3.0", 302, {"fin": "2012-12"}), ("3.6 V6 306", "GM-3.6-V6", 366, {"debut": "2013-01"})],
   reservoir=70, remarques=NA)
mg(L, "Terrain", "D2XX", "1", "2018-01", "2024-06", [("1.5 Turbo 172", "GM-1.5T", 275), ("2.0 Turbo 256", "GM-2.0T", 353, {"fin": "2019-12"}), ("1.6 Diesel 139", "VCDI-1.7", 325, {"fin": "2019-12"})],
   reservoir=56, remarques=NA)
mg(L, "Terrain", "D2UX", "1", "2024-07", None, [("1.5 Turbo 177", "GM-1.5T", 275)], reservoir=56, remarques=NA + " ; 3e génération (millésime 2025)")
mg(L, "Savana", "GMT610", "1", "2003-01", None,
   [("4.3 V6 280", "LV3-4.3", 404, {"debut": "2018-01"}), ("4.8 V8 289", "LY2-4.8", 400, {"fin": "2017-12"}), ("6.0 V8 347", "L96-6.0", 508, {"fin": "2019-12"}),
    ("6.6 V8 406", "L8T-6.6", 630, {"debut": "2020-01"}), ("2.8 Duramax 184", "DURAMAX-2.8", 500, {"debut": "2017-01"})], places=8, reservoir=117,
   remarques=NA + " ; van de transport de personnes (jusqu'à 15 places) ; données indicatives")

MOT = Motorisations("Chevrolet", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"GMC": L}
MOTEURS = MOT.moteurs()
