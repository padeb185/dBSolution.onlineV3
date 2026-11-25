"""Lexus et Lexus F : générations, phases, motorisations (marché européen) et moteurs liés.
Lexus : LS, GS, IS, SC, ES, RX, NX, UX, CT, RC, LC, LBX, LM, RZ ; modèles hors Europe signalés (marché nord-américain, hp
convertis en ch ×1,014). Lexus F : IS F, LFA, RC F, GS F, IS 500 F Sport Performance.
Moteurs : familles et codes de toyota.py (motoriste « Toyota ») ; familles Lexus ajoutées au même motoriste. Pour les hybrides,
le couple est celui du moteur thermique (convention de toyota.py). Données anciennes indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .toyota import FAMILLES as FAMILLES_TOYOTA

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

AJOUTS = {
    "1UZ-FE": f("ATM", E_, 4.0, B, 8, 5400, 4000, "5W30", 5.5, 15000, a="V"),
    "3UZ-FE": f("ATM", E_, 4.3, B, 8, 5600, 3400, "5W30", 5.5, 15000, a="V"),
    "1UR-FSE": f("ATM", E_, 4.6, C, 8, 6400, 4100, "0W20", 7.0, 15000, a="V"),
    "2UR-FSE-HYB": f("HYB_TE", E_, 5.0, C, 8, 6400, 4000, "0W20", 7.0, 15000, a="V"),
    "2UR-GSE": f("ATM", E_, 5.0, C, 8, 7100, 4800, "0W20", 8.0, 15000, a="V"),
    "1LR-GUE": f("ATM", E_, 4.8, C, 10, 8700, 6800, "0W40", 10.0, 10000, a="V"),
    "1G-FE": f("ATM", E_, 2.0, B, 6, 6200, 4400, "5W30", 5.0, 15000),
    "2JZ-GE": f("ATM", E_, 3.0, B, 6, 5800, 3800, "5W30", 5.5, 15000),
    "1MZ-FE": f("ATM", E_, 3.0, B, 6, 5800, 4400, "5W30", 4.7, 15000, a="V"),
    "3MZ-FE-HYB": f("HYB_TE", E_, 3.3, B, 6, 5600, 4400, "5W30", 4.7, 15000, a="V"),
    "4GR-FSE": f("ATM", E_, 2.5, C, 6, 6400, 4800, "0W20", 6.0, 15000, a="V"),
    "3GR-FSE": f("ATM", E_, 3.0, C, 6, 6200, 3600, "0W20", 6.0, 15000, a="V"),
    "2GR-FSE": f("ATM", E_, 3.5, C, 6, 6400, 4800, "0W20", 6.0, 15000, a="V"),
    "2GR-FSE-HYB": f("HYB_TE", E_, 3.5, C, 6, 6400, 4800, "0W20", 6.0, 15000, a="V"),
    "2GR-FXE": f("HYB_TE", E_, 3.5, C, 6, 6000, 4600, "0W20", 6.0, 15000, a="V"),
    "8GR-FXS": f("HYB_TE", E_, 3.5, C, 6, 6600, 5100, "0W20", 6.0, 15000, a="V"),
    "V35A-FTS": f("TURBO", E_, 3.5, C, 6, 6000, 1600, "0W20", 6.5, 15000, a="V"),
    "8AR-FTS": f("TURBO", E_, 2.0, C, 4, 5800, 1650, "0W20", 5.0, 15000),
    "T24A-FTS": f("TURBO", E_, 2.4, C, 4, 6000, 1700, "0W20", 5.5, 15000),
    "T24A-FTS-HEV": f("HYB_TE", E_, 2.4, C, 4, 6000, 2000, "0W20", 5.5, 15000),
    "LEXUS-EV": electrique(),
}
TOYOTA = ("2ZR-FXE", "A25A-FXS", "A25A-PHEV", "M20A-FXS", "M15A-FXE", "2AR-FXE", "2AD-FTV", "2AD-FHV", "1GR-FE", "eTNGA-EV")
FAMILLES = {**{k: FAMILLES_TOYOTA[k] for k in TOYOTA}, **AJOUTS}


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


NA = "Marché nord-américain (hp convertis en ch)"
mg = SaisieMoteurs(FAMILLES, "Toyota")
L = []

# ---------------------------------------------------------------- berlines
mg(L, "LS", "XF10", "1", "1989-09", "1994-10", [("LS 400 4.0 V8 245", "1UZ-FE", 350)], portes=4, places=5, reservoir=85, remarques="Restylage 1993 ; données indicatives")
mg(L, "LS", "XF20", "1", "1994-11", "2000-08", [("LS 400 4.0 V8 264", "1UZ-FE", 366, {"fin": "1997-08"}), ("LS 400 4.0 V8 VVT-i 290", "1UZ-FE", 407, {"debut": "1997-09"})],
   portes=4, places=5, reservoir=85, remarques="Données indicatives")
mg(L, "LS", "XF30", "1", "2000-10", "2006-08", [("LS 430 4.3 V8 282", "3UZ-FE", 417)], portes=4, places=5, reservoir=84)
mg(L, "LS", "XF40", "1", "2006-09", "2017-06",
   [("LS 460 4.6 V8 380", "1UR-FSE", 493), ("LS 600h 5.0 V8 Hybride 445", "2UR-FSE-HYB", 520, {"debut": "2007-06"})], portes=4, places=5, reservoir=84,
   remarques="Empattement long ; restylages 2009 et 2012")
mg(L, "LS", "XF50", "1", "2017-11", None, [("LS 500h 3.5 V6 Hybride 359", "8GR-FXS", 350), ("LS 500 3.5 V6 Biturbo 421", "V35A-FTS", 600, {"debut": "2018-01"})],
   portes=4, places=5, reservoir=82, remarques="En Europe uniquement LS 500h ; restylage 2020")
mg(L, "GS", "S140", "1", "1993-03", "1997-12", [("GS 300 3.0 I6 212", "2JZ-GE", 284)], portes=4, places=5, reservoir=78, remarques="Données indicatives")
mg(L, "GS", "S160", "1", "1997-09", "2005-03", [("GS 300 3.0 I6 222", "2JZ-GE", 298), ("GS 430 4.3 V8 283", "3UZ-FE", 417, {"debut": "2000-09"})], portes=4, places=5,
   reservoir=75, remarques="Données indicatives")
mg(L, "GS", "S190", "1", "2005-04", "2011-12",
   [("GS 300 3.0 V6 249", "3GR-FSE", 310), ("GS 430 4.3 V8 283", "3UZ-FE", 417, {"fin": "2007-12"}), ("GS 460 4.6 V8 347", "1UR-FSE", 460, {"debut": "2008-01"}),
    ("GS 450h 3.5 V6 Hybride 345", "2GR-FSE-HYB", 368, {"debut": "2006-04"})], portes=4, places=5, reservoir=71)
mg(L, "GS", "L10", "1", "2012-03", "2020-08",
   [("GS 250 2.5 V6 209", "4GR-FSE", 253, {"fin": "2015-12"}), ("GS 300h 2.5 Hybride 223", "2AR-FXE", 221, {"debut": "2013-09"}),
    ("GS 450h 3.5 V6 Hybride 345", "2GR-FSE-HYB", 352), ("GS 200t 2.0 Turbo 245", "8AR-FTS", 350, {"debut": "2016-01"})], portes=4, places=5, reservoir=66,
   remarques="Restylage 2015 ; version F dans Lexus F")
mg(L, "IS", "XE10", "1", "1999-03", "2005-09", [("IS 200 2.0 I6 155", "1G-FE", 195), ("IS 300 3.0 I6 214", "2JZ-GE", 298, {"debut": "2001-01"})], portes=4, places=5,
   reservoir=70, remarques="Berline et SportCross (2001)")
mg(L, "IS", "XE20", "1", "2005-10", "2013-06",
   [("IS 250 2.5 V6 208", "4GR-FSE", 252), ("IS 220d 2.2 D-4D 177", "2AD-FHV", 400), ("IS 200d 2.2 D-4D 150", "2AD-FTV", 340, {"debut": "2010-06"})], portes=4,
   places=5, reservoir=65, remarques="IS 250 C cabriolet (2009) ; IS 350 hors Europe ; version F dans Lexus F")
mg(L, "IS", "XE30", "1", "2013-06", "2020-08",
   [("IS 250 2.5 V6 208", "4GR-FSE", 252, {"fin": "2015-12"}), ("IS 300h 2.5 Hybride 223", "2AR-FXE", 221), ("IS 200t 2.0 Turbo 245", "8AR-FTS", 350, {"debut": "2015-09"})],
   portes=4, places=5, reservoir=66, remarques="Restylage 2016")
mg(L, "IS", "XE30", "2", "2020-09", "2025-12", [("IS 300h 2.5 Hybride 223", "2AR-FXE", 221)], portes=4, places=5, reservoir=66,
   remarques="Second restylage ; retirée d'Europe ; date de fin indicative")
mg(L, "ES", "XZ10", "1", "2018-12", None, [("ES 300h 2.5 Hybride 218", "A25A-FXS", 221)], portes=4, places=5, reservoir=50,
   remarques="Première ES vendue en Europe ; restylage 2022 ; nouvelle génération annoncée")
mg(L, "CT", "A10", "1", "2011-01", "2020-12", [("CT 200h 1.8 Hybride 136", "2ZR-FXE", 142)], portes=5, places=5, reservoir=45, remarques="Restylages 2014 et 2017")

# ---------------------------------------------------------------- coupés
mg(L, "SC", "Z30", "1", "1991-06", "2000-07", [("SC 400 4.0 V8 264", "1UZ-FE", 366), ("SC 300 3.0 I6 228", "2JZ-GE", 298)], portes=2, places=4, reservoir=78,
   remarques=NA + " et Japon (Toyota Soarer) ; données indicatives")
mg(L, "SC", "Z40", "1", "2001-01", "2010-07", [("SC 430 4.3 V8 286", "3UZ-FE", 419)], portes=2, places=4, reservoir=75, remarques="Coupé-cabriolet")
mg(L, "RC", "XC10", "1", "2014-10", "2025-12",
   [("RC 300h 2.5 Hybride 223", "2AR-FXE", 221), ("RC 200t 2.0 Turbo 245", "8AR-FTS", 350, {"debut": "2015-09", "fin": "2018-12"})], portes=2, places=4, reservoir=66,
   remarques="Restylage 2018 ; version F dans Lexus F ; date de fin indicative")
mg(L, "LC", "Z100", "1", "2017-03", None, [("LC 500h 3.5 V6 Hybride 359", "8GR-FXS", 350), ("LC 500 5.0 V8 477", "2UR-GSE", 540)], portes=2, places=4, reservoir=82,
   remarques="Coupé et cabriolet (2020)")

# ---------------------------------------------------------------- SUV
mg(L, "RX", "XU10", "1", "1998-01", "2003-06", [("RX 300 3.0 V6 204", "1MZ-FE", 283)], places=5, reservoir=65, remarques="Toyota Harrier au Japon ; données indicatives")
mg(L, "RX", "XU30", "1", "2003-03", "2009-02",
   [("RX 300 3.0 V6 204", "1MZ-FE", 283, {"fin": "2005-12"}), ("RX 400h 3.3 V6 Hybride 272", "3MZ-FE-HYB", 288, {"debut": "2005-04"}),
    ("RX 350 3.5 V6 276", "1GR-FE", 342, {"debut": "2006-01"})], places=5, reservoir=72, remarques="Premier SUV hybride ; RX 350 rattaché à la famille 3.5 V6 Toyota")
mg(L, "RX", "AL10", "1", "2009-03", "2015-10", [("RX 450h 3.5 V6 Hybride 299", "2GR-FXE", 317), ("RX 350 3.5 V6 277", "1GR-FE", 346)], places=5, reservoir=65,
   remarques="Restylage 2012")
mg(L, "RX", "AL20", "1", "2015-11", "2022-06",
   [("RX 450h 3.5 V6 Hybride 313", "2GR-FXE", 335), ("RX 200t 2.0 Turbo 238", "8AR-FTS", 350, {"fin": "2017-12"}),
    ("RX 450hL 3.5 V6 Hybride 313", "2GR-FXE", 335, {"debut": "2018-01"})], places=5, reservoir=65, remarques="RX L 7 places (2018) ; restylage 2019")
mg(L, "RX", "ALA10", "1", "2022-11", None,
   [("RX 350h 2.5 Hybride 250", "A25A-FXS", 239), ("RX 450h+ 2.5 PHEV 309", "A25A-PHEV", 227, {"batterie": 18}),
    ("RX 500h 2.4 Turbo Hybride 371", "T24A-FTS-HEV", 460)], places=5, reservoir=65)
mg(L, "NX", "AZ10", "1", "2014-10", "2021-09",
   [("NX 300h 2.5 Hybride 197", "2AR-FXE", 206), ("NX 200t 2.0 Turbo 238", "8AR-FTS", 350, {"fin": "2017-06"})], places=5, reservoir=56, remarques="Restylage 2017")
mg(L, "NX", "AZ20", "1", "2021-10", None,
   [("NX 350h 2.5 Hybride 244", "A25A-FXS", 239), ("NX 450h+ 2.5 PHEV 309", "A25A-PHEV", 227, {"batterie": 18})], places=5, reservoir=55)
mg(L, "UX", "MZAA10", "1", "2019-01", "2023-12",
   [("UX 250h 2.0 Hybride 184", "M20A-FXS", 190), ("UX 300e 204", "LEXUS-EV", 300, el(54, debut="2020-09"))], places=5, reservoir=43)
mg(L, "UX", "MZAA10", "2", "2024-01", None,
   [("UX 300h 2.0 Hybride 199", "M20A-FXS", 190), ("UX 300e 204", "LEXUS-EV", 300, el(73, fin="2025-06"))], places=5, reservoir=47,
   remarques="Mise à jour (UX 300h, batterie UX 300e 72,8 kWh)")
mg(L, "LBX", "MAYH10", "1", "2023-12", None, [("LBX 1.5 Hybride 136", "M15A-FXE", 185)], places=5, reservoir=36,
   remarques="SUV urbain (plateforme TNGA-B) ; LBX Morizo RR non reprise")
mg(L, "LM", "AW10", "1", "2023-11", None, [("LM 350h 2.5 Hybride 250", "A25A-FXS", 239)], places=4, reservoir=60, remarques="Monospace de luxe, 4 ou 6 places")
mg(L, "RZ", "XEBM15", "1", "2023-03", "2025-06", [("RZ 450e 313", "eTNGA-EV", 435, el(71))], places=5, reservoir=0, remarques="Électrique (plateforme e-TNGA)")
mg(L, "RZ", "XEBM15", "2", "2025-07", None,
   [("RZ 350e 224", "eTNGA-EV", 268, el(71)), ("RZ 500e 381", "eTNGA-EV", 435, el(75)), ("RZ 550e F Sport 408", "eTNGA-EV", 435, el(75))], places=5, reservoir=0,
   remarques="Mise à jour ; couples et dates indicatifs")

# ---------------------------------------------------------------- Lexus F
LF = []
mg(LF, "IS F", "XE20", "1", "2008-01", "2014-12", [("IS F 5.0 V8 423", "2UR-GSE", 505)], portes=4, places=5, reservoir=64)
mg(LF, "LFA", "LFA", "1", "2010-12", "2012-12", [("4.8 V10 560", "1LR-GUE", 480)], portes=2, places=2, reservoir=73, remarques="500 exemplaires, LFA Nürburgring Package")
mg(LF, "RC F", "XC10", "1", "2014-10", "2019-03", [("RC F 5.0 V8 477", "2UR-GSE", 530)], portes=2, places=4, reservoir=66)
mg(LF, "RC F", "XC10", "2", "2019-04", "2025-12", [("RC F 5.0 V8 464", "2UR-GSE", 520), ("RC F Track Edition 5.0 V8 464", "2UR-GSE", 520)], portes=2, places=4,
   reservoir=66, remarques="Restylage ; date de fin indicative")
mg(LF, "GS F", "L10", "1", "2015-10", "2020-08", [("GS F 5.0 V8 477", "2UR-GSE", 530)], portes=4, places=5, reservoir=66)
mg(LF, "IS 500 F Sport Performance", "XE30", "2", "2021-10", None, [("5.0 V8 479", "2UR-GSE", 535)], portes=4, places=5, reservoir=66, remarques=NA)

MOT = Motorisations("Toyota", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LF)

DETAIL = {"Lexus": L, "Lexus F": LF}
MOTEURS = MOT.moteurs()
