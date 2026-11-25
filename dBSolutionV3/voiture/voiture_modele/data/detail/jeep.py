"""Jeep : générations, phases, motorisations et moteurs liés.
Marque américaine : marché nord-américain par défaut (hp convertis en ch ×1,014) pour Willys MB, CJ, Jeepster, Gladiator,
Wagoneer/Grand Wagoneer, Cherokee (XJ, KJ/KK « Liberty », KL, hybride 2026), Grand Cherokee, Wrangler, Commander, Compass MK,
Patriot, Wagoneer S et Recon. Modèles conçus et produits en Europe : Renegade, Compass MP et Compass (2025), Avenger
(marché européen, puissances en ch). Wrangler, Grand Cherokee et Gladiator ne sont plus importés en Europe depuis 2024-2025.
Moteurs repris de chrysler.py (motoriste « Chrysler », OM642 « Mercedes-Benz »), dodge.py (« Dodge »), fiat.py (« Fiat ») et
peugeot.py (« Peugeot ») avec leurs codes ; moteurs AMC/Willys et propres au motoriste « Jeep ». Données anciennes indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .chrysler import FAMILLES as FAMILLES_CHRYSLER, mot as motoriste_chrysler
from .dodge import FAMILLES as FAMILLES_DODGE
from .fiat import FAMILLES as FAMILLES_FIAT
from .peugeot import FAMILLES as FAMILLES_PEUGEOT

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

CHRYSLER = {k: FAMILLES_CHRYSLER[k] for k in ("PENTASTAR-3.6", "POWERTECH-4.7", "HEMI-5.7", "HEMI-6.1", "HEMI-6.4", "EGH-3.8",
                                              "TIGERSHARK-2.4", "WORLD-2.0", "WORLD-2.4", "VM-2.8CRD", "VM-3.0CRD", "CHR-MB-OM642-3.0")}
DODGE = {k: FAMILLES_DODGE[k] for k in ("EKG-3.7", "GME-2.0T", "GSE-1.3-PHEV", "HURRICANE-3.0TT")}
FIAT = {k: FAMILLES_FIAT[k] for k in ("ETORQ-1.6", "MULTIAIR-1.4T", "FIREFLY-1.0T", "FIREFLY-1.3T", "FIREFLY-1.5-HYB", "MJ-1.6", "MJ-2.0",
                                      "EB2", "EB2-MHEV", "e-CMP")}
PEUGEOT = {k: FAMILLES_PEUGEOT[k] for k in ("EP6-PHEV", "STLA-M")}
PROPRES = {
    "GO-DEVIL-2.2": f("ATM", E_, 2.2, C, 4, 4000, 2000, "20W50", 4.7, 3000),
    "HURRICANE-F-2.2": f("ATM", E_, 2.2, C, 4, 4000, 2000, "20W50", 4.7, 3000),
    "TORNADO-3.8": f("ATM", E_, 3.8, C, 6, 4000, 1750, "20W50", 5.7, 5000),
    "AMC-5.4V8": f("ATM", E_, 5.4, C, 8, 4700, 2600, "20W50", 4.7, 5000, a="V"),
    "AMC-2.5": f("ATM", E_, 2.5, C, 4, 5250, 3250, "10W30", 3.8, 5000),
    "AMC-4.2": f("ATM", E_, 4.2, C, 6, 3200, 1800, "10W30", 5.7, 5000),
    "AMC-4.0": f("ATM", E_, 4.0, C, 6, 4600, 3000, "10W30", 5.7, 5000),
    "AMC-5.0V8": f("ATM", E_, 5.0, C, 8, 4200, 2500, "10W30", 4.7, 5000, a="V"),
    "AMC-5.9V8": f("ATM", E_, 5.9, C, 8, 4000, 2000, "10W30", 4.7, 5000, a="V"),
    "GM-2.8V6": f("ATM", E_, 2.8, C, 6, 4800, 2400, "10W30", 3.8, 5000, a="V"),
    "MAGNUM-5.2": f("ATM", E_, 5.2, C, 8, 4400, 3200, "5W30", 4.7, 10000, a="V"),
    "MAGNUM-5.9": f("ATM", E_, 5.9, C, 8, 4050, 3050, "5W30", 4.7, 10000, a="V"),
    "HEMI-6.2SC": f("TURBO", E_, 6.2, C, 8, 6000, 4800, "0W40", 6.6, 10000, a="V"),
    "GME-2.0T-PHEV": f("HYB_E", E_, 2.0, C, 4, 5250, 3000, "0W20", 5.5, 10000),
    "STLA-1.6T-HEV": f("HYB_TE", E_, 1.6, C, 4, 5500, 1750, "0W20", 4.7, 10000),
    "JEEP-EV": electrique(),
}
FAMILLES = {**CHRYSLER, **DODGE, **FIAT, **PEUGEOT, **PROPRES}


def motoriste(fam):
    if fam in CHRYSLER:
        return motoriste_chrysler(fam)
    if fam in DODGE:
        return "Dodge"
    if fam in FIAT:
        return "Fiat"
    return "Peugeot" if fam in PEUGEOT else "Jeep"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


NA = "Marché nord-américain (hp convertis en ch)"
EU = "Marché européen"
mg = SaisieMoteurs(FAMILLES, "Jeep", motoriste)
L = []

# ---------------------------------------------------------------- historiques
mg(L, "Willys MB / GPW", "MB", "1", "1941-11", "1945-09", [("Go Devil 2.2 61", "GO-DEVIL-2.2", 142)], portes=2, places=4, reservoir=57,
   remarques="Véhicule militaire Willys MB et Ford GPW ; données indicatives")
mg(L, "Jeepster", "VJ", "1", "1948-04", "1950-12", [("Go Devil 2.2 64", "GO-DEVIL-2.2", 142)], portes=2, places=4, reservoir=40,
   remarques=NA + " ; Willys-Overland ; données indicatives")
mg(L, "CJ-5", "CJ-5", "1", "1954-10", "1983-12",
   [("Hurricane 2.2 76", "HURRICANE-F-2.2", 155, {"fin": "1971-12"}), ("4.2 I6 112", "AMC-4.2", 264, {"debut": "1972-01"}),
    ("5.0 V8 152", "AMC-5.0V8", 332, {"debut": "1972-01", "fin": "1981-12"}), ("2.5 I4 83", "AMC-2.5", 169, {"debut": "1980-01"})],
   portes=2, places=4, reservoir=45, remarques=NA + " ; données indicatives (2.5 « Iron Duke » GM en 1980-1983)")
mg(L, "CJ-7", "CJ-7", "1", "1976-03", "1986-12",
   [("4.2 I6 112", "AMC-4.2", 264), ("5.0 V8 152", "AMC-5.0V8", 332, {"fin": "1981-12"}), ("2.5 I4 106", "AMC-2.5", 179, {"debut": "1983-01"})],
   portes=2, places=4, reservoir=57, remarques=NA + " ; données indicatives")
mg(L, "Gladiator (1963-72)", "SJ", "1", "1962-11", "1971-12",
   [("Tornado 3.8 I6 142", "TORNADO-3.8", 285, {"fin": "1965-12"}), ("5.4 V8 254", "AMC-5.4V8", 461, {"debut": "1965-01"})], portes=2, places=3,
   reservoir=55, remarques=NA + " ; pick-up, devenu J-Series en 1971 ; données indicatives")
mg(L, "Wagoneer", "SJ", "1", "1962-11", "1983-12",
   [("Tornado 3.8 I6 142", "TORNADO-3.8", 285, {"fin": "1965-12"}), ("5.4 V8 254", "AMC-5.4V8", 461, {"debut": "1965-01", "fin": "1968-12"}),
    ("5.9 V8 177", "AMC-5.9V8", 386, {"debut": "1971-01"})], portes=5, places=6, reservoir=83, remarques=NA + " ; données indicatives")
mg(L, "Grand Wagoneer", "SJ", "1", "1984-01", "1991-12", [("5.9 V8 146", "AMC-5.9V8", 380)], portes=5, places=6, reservoir=76,
   remarques=NA + " ; ancien Wagoneer haut de gamme ; données indicatives")

# ---------------------------------------------------------------- Cherokee
mg(L, "Cherokee", "XJ", "1", "1983-09", "2001-06",
   [("2.5 I4 119", "AMC-2.5", 183, {"fin": "1990-12"}), ("2.8 V6 117", "GM-2.8V6", 203, {"fin": "1986-12"}), ("4.0 I6 175", "AMC-4.0", 298, {"debut": "1987-01", "fin": "1990-12"}),
    ("2.5 I4 132", "AMC-2.5", 202, {"debut": "1991-01"}), ("4.0 I6 193", "AMC-4.0", 305, {"debut": "1991-01"})], reservoir=76,
   remarques=NA + " ; restylage 1997 ; en Europe aussi en 2.1 TD Renault et 2.5 TD VM")
mg(L, "Cherokee", "KJ", "1", "2001-07", "2007-12",
   [("2.4 152", "TIGERSHARK-2.4", 217), ("3.7 V6 213", "EKG-3.7", 319), ("2.8 CRD 162", "VM-2.8CRD", 400, {"debut": "2005-01", "fin": "2006-12"})],
   reservoir=74, remarques=NA + " ; vendu sous le nom Liberty en Amérique du Nord")
mg(L, "Cherokee", "KK", "1", "2008-01", "2012-12", [("3.7 V6 213", "EKG-3.7", 319)], reservoir=74,
   remarques=NA + " ; Liberty en Amérique du Nord ; en Europe aussi en 2.8 CRD")
mg(L, "Cherokee", "KL", "1", "2013-10", "2018-06", [("2.4 187", "TIGERSHARK-2.4", 237), ("3.2 V6 275", "PENTASTAR-3.6", 323)], reservoir=60,
   remarques=NA + " ; V6 Pentastar 3,2 l ; en Europe aussi en 2.0 et 2.2 Multijet")
mg(L, "Cherokee", "KL", "2", "2018-07", "2023-02",
   [("2.4 182", "TIGERSHARK-2.4", 233), ("3.2 V6 275", "PENTASTAR-3.6", 323), ("2.0T 274", "GME-2.0T", 400)], reservoir=60,
   remarques=NA + " ; restylage ; production arrêtée en 2023")
mg(L, "Cherokee", "KM", "1", "2026-01", None, [("1.6T Hybrid 213", "STLA-1.6T-HEV", 312)], reservoir=55,
   remarques=NA + " ; nouvelle génération exclusivement hybride (plateforme STLA Large) ; date et données indicatives")

# ---------------------------------------------------------------- Grand Cherokee
mg(L, "Grand Cherokee", "ZJ", "1", "1992-04", "1998-09",
   [("4.0 I6 193", "AMC-4.0", 305), ("5.2 V8 223", "MAGNUM-5.2", 386), ("5.9 V8 248", "MAGNUM-5.9", 468, {"debut": "1998-01"})], reservoir=87,
   remarques=NA + " ; en Europe aussi en 2.5 TD VM")
mg(L, "Grand Cherokee", "WJ", "1", "1998-10", "2004-09",
   [("4.0 I6 198", "AMC-4.0", 312), ("4.7 V8 238", "POWERTECH-4.7", 407), ("4.7 V8 HO 269", "POWERTECH-4.7", 447, {"debut": "2001-10"})], reservoir=78,
   remarques=NA + " ; en Europe aussi en 3.1 TD VM puis 2.7 CRD Mercedes")
mg(L, "Grand Cherokee", "WK", "1", "2004-10", "2010-06",
   [("3.7 V6 213", "EKG-3.7", 319), ("4.7 V8 238", "POWERTECH-4.7", 407), ("5.7 V8 331", "HEMI-5.7", 500, {"fin": "2008-12"}),
    ("5.7 V8 362", "HEMI-5.7", 527, {"debut": "2009-01"}), ("3.0 CRD 218", "CHR-MB-OM642-3.0", 510, {"debut": "2006-06", "fin": "2008-12"}),
    ("SRT8 6.1 V8 431", "HEMI-6.1", 569, {"debut": "2005-10"})], reservoir=78, remarques=NA + " ; restylage 2008")
mg(L, "Grand Cherokee", "WK2", "1", "2010-07", "2013-12",
   [("3.6 V6 294", "PENTASTAR-3.6", 353), ("5.7 V8 365", "HEMI-5.7", 529), ("SRT8 6.4 V8 476", "HEMI-6.4", 637, {"debut": "2011-06"})], reservoir=93,
   remarques=NA + " ; en Europe aussi en 3.0 CRD")
mg(L, "Grand Cherokee", "WK2", "2", "2014-01", "2021-12",
   [("3.6 V6 294", "PENTASTAR-3.6", 353), ("5.7 V8 365", "HEMI-5.7", 529), ("3.0 EcoDiesel 243", "VM-3.0CRD", 570, {"fin": "2019-12"}),
    ("SRT 6.4 V8 481", "HEMI-6.4", 637), ("Trackhawk 6.2 V8 SC 717", "HEMI-6.2SC", 868, {"debut": "2017-10"})], reservoir=93, remarques=NA + " ; restylages 2014 et 2017")
mg(L, "Grand Cherokee", "WL", "1", "2021-06", "2025-08",
   [("3.6 V6 297", "PENTASTAR-3.6", 353), ("5.7 V8 362", "HEMI-5.7", 529, {"fin": "2023-12"}),
    ("4xe 2.0T PHEV 380", "GME-2.0T-PHEV", 637, {"debut": "2022-01", "batterie": 17})], reservoir=87,
   remarques=NA + " ; Grand Cherokee L à 3 rangées ; en Europe uniquement 4xe (importation arrêtée en 2024-2025) ; 4xe arrêté en 2025")
mg(L, "Grand Cherokee", "WL", "2", "2025-09", None, [("3.6 V6 297", "PENTASTAR-3.6", 353), ("2.0T 329", "GME-2.0T", 450)], reservoir=87,
   remarques=NA + " ; restylage (millésime 2026), nouveau 2.0T Hurricane 4 ; données indicatives")

# ---------------------------------------------------------------- Wrangler / Gladiator / Commander
mg(L, "Wrangler", "YJ", "1", "1986-05", "1995-12",
   [("2.5 I4 119", "AMC-2.5", 183), ("4.2 I6 114", "AMC-4.2", 285, {"fin": "1990-12"}), ("4.0 I6 183", "AMC-4.0", 298, {"debut": "1991-01"})],
   portes=2, places=4, reservoir=57, remarques=NA)
mg(L, "Wrangler", "TJ", "1", "1996-01", "2006-12",
   [("2.5 I4 122", "AMC-2.5", 190, {"fin": "2002-12"}), ("4.0 I6 184", "AMC-4.0", 298, {"fin": "1999-12"}), ("4.0 I6 193", "AMC-4.0", 319, {"debut": "2000-01"}),
    ("2.4 152", "TIGERSHARK-2.4", 217, {"debut": "2003-01"})], portes=2, places=4, reservoir=72,
   remarques=NA + " ; Unlimited (2004) ; en Europe aussi en 2.8 CRD (2005)")
mg(L, "Wrangler", "JK", "1", "2006-08", "2018-06",
   [("3.8 V6 205", "EGH-3.8", 321, {"fin": "2011-12"}), ("3.6 V6 289", "PENTASTAR-3.6", 353, {"debut": "2012-01"})], portes=4, places=5, reservoir=70,
   remarques=NA + " ; 2 et 4 portes (Unlimited) ; en Europe aussi en 2.8 CRD")
mg(L, "Wrangler", "JL", "1", "2017-11", "2023-12",
   [("3.6 V6 289", "PENTASTAR-3.6", 353), ("2.0T 274", "GME-2.0T", 400), ("3.0 EcoDiesel 264", "VM-3.0CRD", 599, {"debut": "2020-01", "fin": "2023-06"}),
    ("4xe 2.0T PHEV 380", "GME-2.0T-PHEV", 637, {"debut": "2021-01", "batterie": 17}), ("Rubicon 392 6.4 V8 477", "HEMI-6.4", 637, {"debut": "2021-01"})],
   portes=4, places=5, reservoir=81, remarques=NA + " ; 2 et 4 portes ; en Europe 2.0T, 2.2 Multijet et 4xe")
mg(L, "Wrangler", "JL", "2", "2024-01", None,
   [("3.6 V6 289", "PENTASTAR-3.6", 353), ("2.0T 274", "GME-2.0T", 400), ("4xe 2.0T PHEV 380", "GME-2.0T-PHEV", 637, {"batterie": 17, "fin": "2025-12"}),
    ("Rubicon 392 6.4 V8 477", "HEMI-6.4", 637, {"fin": "2024-12"})], portes=4, places=5, reservoir=81,
   remarques=NA + " ; restylage ; vente européenne arrêtée en 2025 ; 4xe abandonné fin 2025")
mg(L, "Gladiator", "JT", "1", "2019-04", None,
   [("3.6 V6 289", "PENTASTAR-3.6", 353), ("3.0 EcoDiesel 264", "VM-3.0CRD", 599, {"debut": "2021-01", "fin": "2023-06"})], portes=4, places=5, reservoir=83,
   remarques=NA + " ; pick-up ; en Europe 3.0 V6 Multijet (2021-2024)")
mg(L, "Commander", "XK", "1", "2005-09", "2010-06",
   [("3.7 V6 213", "EKG-3.7", 319), ("4.7 V8 238", "POWERTECH-4.7", 407), ("5.7 V8 335", "HEMI-5.7", 508, {"fin": "2008-12"}),
    ("5.7 V8 362", "HEMI-5.7", 527, {"debut": "2009-01"})], places=7, reservoir=78, remarques=NA + " ; en Europe aussi en 3.0 CRD")

# ---------------------------------------------------------------- compacts nord-américains
mg(L, "Compass", "MK", "1", "2006-08", "2016-12", [("2.0 160", "WORLD-2.0", 190), ("2.4 174", "WORLD-2.4", 224)], reservoir=51,
   remarques=NA + " ; restylage 2011 ; en Europe aussi en 2.0 CRD (moteur Volkswagen) et 2.2 CRD")
mg(L, "Patriot", "MK74", "1", "2006-12", "2017-12", [("2.0 160", "WORLD-2.0", 190), ("2.4 174", "WORLD-2.4", 224)], reservoir=51,
   remarques=NA + " ; en Europe aussi en 2.0 CRD et 2.2 CRD")

# ---------------------------------------------------------------- modèles européens
mg(L, "Renegade", "BU", "1", "2014-09", "2018-06",
   [("1.6 E-Torq 110", "ETORQ-1.6", 152), ("1.4 MultiAir 140", "MULTIAIR-1.4T", 230), ("1.4 MultiAir 4x4 170", "MULTIAIR-1.4T", 250),
    ("1.6 Multijet 120", "MJ-1.6", 320), ("2.0 Multijet 4x4 140", "MJ-2.0", 350), ("2.0 Multijet 4x4 170", "MJ-2.0", 350)], reservoir=48,
   remarques=EU + " ; produit à Melfi (Italie)")
mg(L, "Renegade", "BU", "2", "2018-07", "2025-10",
   [("1.0 T3 120", "FIREFLY-1.0T", 190), ("1.3 T4 150", "FIREFLY-1.3T", 270), ("1.3 T4 4x4 180", "FIREFLY-1.3T", 270, {"fin": "2020-12"}),
    ("1.6 Multijet 130", "MJ-1.6", 320), ("2.0 Multijet 4x4 140", "MJ-2.0", 350, {"fin": "2020-12"}),
    ("4xe 1.3 PHEV 190", "GSE-1.3-PHEV", 270, {"debut": "2020-06", "batterie": 11}), ("4xe 1.3 PHEV 240", "GSE-1.3-PHEV", 270, {"debut": "2020-06", "batterie": 11}),
    ("e-Hybrid 1.5 130", "FIREFLY-1.5-HYB", 240, {"debut": "2022-07"})], reservoir=48,
   remarques=EU + " ; restylage ; production arrêtée à Melfi en octobre 2025")
mg(L, "Compass", "MP", "1", "2017-09", "2020-12",
   [("1.4 MultiAir 140", "MULTIAIR-1.4T", 230), ("1.4 MultiAir 4x4 170", "MULTIAIR-1.4T", 250), ("1.6 Multijet 120", "MJ-1.6", 320),
    ("2.0 Multijet 4x4 140", "MJ-2.0", 350), ("2.0 Multijet 4x4 170", "MJ-2.0", 350)], reservoir=60, remarques=EU + " ; produit au Brésil, au Mexique puis à Melfi")
mg(L, "Compass", "MP", "2", "2021-01", "2025-04",
   [("1.3 T4 130", "FIREFLY-1.3T", 270), ("1.3 T4 150", "FIREFLY-1.3T", 270), ("1.6 Multijet 130", "MJ-1.6", 320, {"fin": "2023-12"}),
    ("4xe 1.3 PHEV 190", "GSE-1.3-PHEV", 270, {"batterie": 11}), ("4xe 1.3 PHEV 240", "GSE-1.3-PHEV", 270, {"batterie": 11}),
    ("e-Hybrid 1.5 130", "FIREFLY-1.5-HYB", 240, {"debut": "2022-06"})], reservoir=55, remarques=EU + " ; restylage")
mg(L, "Compass", "J4U", "1", "2025-05", None,
   [("e-Hybrid 1.2 145", "EB2-MHEV", 230), ("Hybrid Plug-in 1.6 195", "EP6-PHEV", 360, {"debut": "2026-01", "batterie": 18}),
    ("Électrique 213", "STLA-M", 345, el(74)), ("Électrique Long Range 231", "STLA-M", 345, el(97, debut="2026-01")),
    ("Électrique 4xe 375", "STLA-M", 577, el(97, debut="2026-06"))], reservoir=55,
   remarques=EU + " ; 3e génération sur STLA Medium, produite à Melfi ; dates des versions PHEV et 4xe indicatives")
mg(L, "Avenger", "Avenger", "1", "2023-03", None,
   [("Électrique 156", "e-CMP", 260, el(54)), ("1.2 Turbo 100", "EB2", 205), ("e-Hybrid 1.2 100", "EB2-MHEV", 205, {"debut": "2024-03"}),
    ("4xe 1.2 Hybrid 136", "EB2-MHEV", 230, {"debut": "2024-10"})], reservoir=44, remarques=EU + " ; SUV urbain (base e-CMP) produit à Tychy (Pologne)")

# ---------------------------------------------------------------- Wagoneer / électriques
mg(L, "Wagoneer", "WS", "1", "2021-03", None,
   [("5.7 V8 eTorque 397", "HEMI-5.7", 549, {"fin": "2022-12"}), ("3.0 Hurricane 426", "HURRICANE-3.0TT", 635, {"debut": "2022-09"})], places=8, reservoir=100,
   remarques=NA + " ; vendu sous la marque Wagoneer jusqu'en 2024")
mg(L, "Grand Wagoneer", "WS", "1", "2021-03", None,
   [("6.4 V8 478", "HEMI-6.4", 617, {"fin": "2022-12"}), ("3.0 Hurricane HO 517", "HURRICANE-3.0TT", 678, {"debut": "2022-09"})], places=8, reservoir=100,
   remarques=NA + " ; restylage millésime 2026")
mg(L, "Wagoneer S", "KM", "1", "2024-09", None, [("AWD 608", "JEEP-EV", 841, el(100))], reservoir=0,
   remarques=NA + " ; SUV électrique STLA Large produit à Toluca ; lancement européen annoncé puis repoussé")
mg(L, "Recon", "KR", "1", "2026-06", None, [("AWD 659", "JEEP-EV", 840, el(100))], reservoir=0,
   remarques=NA + " ; électrique Trail Rated à portes amovibles (STLA Large), produit à Toluca ; Europe prévue début 2027")

MOT = Motorisations("Jeep", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Jeep": L}
MOTEURS = MOT.moteurs()
