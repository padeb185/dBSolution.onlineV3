"""Dodge et Dodge SRT : générations, motorisations et moteurs liés.
Marché nord-américain ; Caliber, Nitro, Avenger, Journey et Viper aussi vendus en Europe (2006-2011).
Ram 1500 jusqu'en 2010 (ensuite marque Ram). Dodge SRT : Viper, SRT-4, SRT8, SRT 392, Hellcat, Demon, Durango SRT, Ram TRX.
Puissances américaines converties en ch (×1,014). Diesels VW (2.0 CRD) avec les codes de volkswagen.py (motoriste « Volkswagen »).
Données antérieures à 2000 indicatives. Saisie : (nom, famille, couple_nm[, surcharges]) ; puissance = dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .volkswagen import FAMILLES as FAMILLES_VW

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"


def v8(t, l, rpm, nmrpm, q=6.6):
    return f(t, E_, l, C, 8, rpm, nmrpm, "5W20", q, 12000, a="V")


VW = ("EA188-2.0TDI",)
PROPRES = {
    "NEON-2.0": f("ATM", E_, 2.0, B, 4, 6500, 4500, "5W30", 4.3, 12000),
    "NEON-2.4T": f("TURBO", E_, 2.4, B, 4, 5300, 2200, "5W30", 4.3, 12000),
    "WORLD-1.8": f("ATM", E_, 1.8, C, 4, 6500, 5200, "5W20", 4.3, 12000),
    "WORLD-2.0": f("ATM", E_, 2.0, C, 4, 6300, 5100, "5W20", 4.3, 12000),
    "WORLD-2.4": f("ATM", E_, 2.4, C, 4, 6000, 4500, "5W20", 4.3, 12000),
    "WORLD-2.4T": f("TURBO", E_, 2.4, C, 4, 6000, 2000, "5W30", 4.3, 12000),
    "TIGERSHARK-2.4": f("ATM", E_, 2.4, B, 4, 6250, 4800, "0W20", 5.2, 12000),
    "MULTIAIR-1.4T": f("TURBO", E_, 1.4, B, 4, 5500, 2500, "5W40", 4.0, 12000),
    "VM-2.8CRD": f("TURBO", D, 2.8, C, 4, 3800, 2000, "5W30", 6.0, 15000),
    "EER-2.7": f("ATM", E_, 2.7, C, 6, 6400, 4000, "5W20", 5.0, 12000, a="V"),
    "EGJ-3.5": f("ATM", E_, 3.5, C, 6, 6400, 4000, "5W20", 5.0, 12000, a="V"),
    "EKG-3.7": f("ATM", E_, 3.7, C, 6, 5200, 4000, "5W20", 5.0, 12000, a="V"),
    "PENTASTAR-3.6": f("ATM", E_, 3.6, C, 6, 6350, 4800, "0W20", 5.7, 12000, a="V"),
    "POWERTECH-4.7": v8("ATM", 4.7, 5200, 3600),
    "HEMI-5.7": v8("ATM", 5.7, 5600, 4200, 6.6), "HEMI-6.1": v8("ATM", 6.1, 6200, 4800), "HEMI-6.4": v8("ATM", 6.4, 6000, 4300),
    "HELLCAT-6.2SC": v8("TURBO", 6.2, 6000, 4000, 6.6),
    "VIPER-8.0": f("ATM", E_, 8.0, C, 10, 4600, 3600, "10W30", 10.0, 12000, a="V"),
    "VIPER-8.3": f("ATM", E_, 8.3, C, 10, 5600, 4200, "10W30", 10.0, 12000, a="V"),
    "VIPER-8.4": f("ATM", E_, 8.4, C, 10, 6200, 5000, "0W40", 10.0, 12000, a="V"),
    "GME-2.0T": f("TURBO", E_, 2.0, C, 4, 5250, 2500, "0W30", 5.5, 12000),
    "GSE-1.3-PHEV": f("HYB_E", E_, 1.3, C, 4, 5750, 1850, "0W20", 3.5, 12000),
    "HURRICANE-3.0TT": f("TURBO", E_, 3.0, C, 6, 5700, 3500, "0W40", 7.0, 12000),
    "STLA-L-EV": electrique(),
}
FAMILLES = {**{k: FAMILLES_VW[k] for k in VW}, **PROPRES}

mg = SaisieMoteurs(FAMILLES, "Dodge", lambda fam: "Volkswagen" if fam in VW else "Dodge")
L, LS = [], []   # Dodge, Dodge SRT
NA = "Marché nord-américain"
EUNA = "Amérique du Nord et Europe"
IND = "données indicatives"

# ---------------------------------------------------------------- compactes / berlines
mg(L, "Neon", "PL", "1", "1995-01", "1999-12", [("2.0 SOHC 134", "NEON-2.0", 176), ("2.0 DOHC 152", "NEON-2.0", 180)], portes=4, reservoir=47,
   remarques="Aussi vendue en Europe (Chrysler Neon) ; " + IND)
mg(L, "Neon", "PL", "2", "2000-01", "2005-12", [("2.0 134", "NEON-2.0", 176), ("R/T 2.0 152", "NEON-2.0", 180, {"debut": "2001-01", "fin": "2004-12"})], portes=4, reservoir=47,
   remarques=NA + " ; SRT-4 dans « Dodge SRT »")
mg(L, "Caliber", "PM", "1", "2006-06", "2012-12",
   [("1.8 150", "WORLD-1.8", 168), ("2.0 158", "WORLD-2.0", 191), ("2.4 174", "WORLD-2.4", 224), ("2.0 CRD 140", "EA188-2.0TDI", 310)], reservoir=52,
   remarques=EUNA + " (Europe jusqu'en 2011) ; SRT4 dans « Dodge SRT »")
mg(L, "Avenger", "JS", "1", "2008-01", "2014-12", [("2.0 158", "WORLD-2.0", 190), ("2.4 174", "WORLD-2.4", 224), ("3.6 V6 287", "PENTASTAR-3.6", 353, {"debut": "2011-01"}),
                                                  ("2.0 CRD 140", "EA188-2.0TDI", 310, {"fin": "2010-12"})], portes=4, reservoir=64, remarques=EUNA + " (Europe 2008-2010)")
mg(L, "Dart", "PF", "1", "2013-01", "2016-12", [("2.0 162", "TIGERSHARK-2.4", 197), ("1.4 Turbo 162", "MULTIAIR-1.4T", 250), ("2.4 186", "TIGERSHARK-2.4", 237, {"debut": "2014-01"})],
   portes=4, reservoir=60, remarques=NA + " ; base Alfa Romeo Giulietta")
mg(L, "Charger", "LX", "1", "2006-01", "2010-12", [("2.7 V6 192", "EER-2.7", 258), ("3.5 V6 254", "EGJ-3.5", 340), ("R/T 5.7 V8 345", "HEMI-5.7", 529)], portes=4, reservoir=68,
   remarques=NA + " ; SRT8 dans « Dodge SRT »")
mg(L, "Charger", "LD", "1", "2011-01", "2023-12", [("3.6 V6 296", "PENTASTAR-3.6", 353), ("3.6 V6 304", "PENTASTAR-3.6", 359, {"debut": "2015-01"}), ("R/T 5.7 V8 375", "HEMI-5.7", 536),
                                                 ("Scat Pack 6.4 V8 492", "HEMI-6.4", 644, {"debut": "2015-01"})], portes=4, reservoir=70,
   remarques=NA + " ; restylage 2015 ; SRT dans « Dodge SRT »")
mg(L, "Challenger", "LC", "1", "2008-01", "2023-12",
   [("3.5 V6 254", "EGJ-3.5", 339, {"debut": "2009-01", "fin": "2010-12"}), ("3.6 V6 309", "PENTASTAR-3.6", 363, {"debut": "2011-01"}), ("R/T 5.7 V8 380", "HEMI-5.7", 542, {"debut": "2009-01"}),
    ("Scat Pack 6.4 V8 492", "HEMI-6.4", 644, {"debut": "2015-01"})], portes=2, places=5, reservoir=70, remarques=NA + " ; restylage 2015 ; SRT dans « Dodge SRT »")
mg(L, "Charger", "LB", "1", "2024-07", None,
   [("Daytona R/T 462", "STLA-L-EV", 548, {"batterie": 100, "fin": "2025-12"}), ("Daytona Scat Pack 680", "STLA-L-EV", 850, {"batterie": 100}),
    ("R/T Sixpack 426", "HURRICANE-3.0TT", 635, {"debut": "2026-03"}), ("Scat Pack Sixpack 558", "HURRICANE-3.0TT", 720, {"debut": "2026-01"})],
   portes=2, places=5, reservoir=0, remarques=NA + " ; coupé et berline 4 portes ; Daytona électrique, Sixpack 6 cylindres biturbo (2026)")

# ---------------------------------------------------------------- SUV / monospaces / pick-up
mg(L, "Nitro", "KA", "1", "2007-01", "2011-12", [("3.7 V6 205", "EKG-3.7", 319), ("4.0 V6 264", "EKG-3.7", 359, {"debut": "2008-01"}), ("2.8 CRD 177", "VM-2.8CRD", 460)],
   reservoir=74, remarques=EUNA + " (Europe 2007-2010)")
mg(L, "Journey", "JC", "1", "2008-06", "2020-12",
   [("2.4 174", "WORLD-2.4", 225), ("2.7 V6 187", "EER-2.7", 256, {"fin": "2010-12"}), ("3.5 V6 239", "EGJ-3.5", 305, {"fin": "2010-12"}), ("3.6 V6 287", "PENTASTAR-3.6", 353, {"debut": "2011-01"}),
    ("2.0 CRD 140", "EA188-2.0TDI", 310, {"fin": "2011-06"})], places=7, reservoir=78, remarques=EUNA + " ; en Europe vendu Fiat Freemont après 2011")
mg(L, "Grand Caravan", "RT", "1", "2008-01", "2020-12", [("3.3 V6 177", "EGJ-3.5", 278, {"fin": "2010-12"}), ("3.8 V6 200", "EGJ-3.5", 312, {"fin": "2010-12"}),
                                                        ("3.6 V6 287", "PENTASTAR-3.6", 353, {"debut": "2011-01"})], places=7, reservoir=76, remarques=NA + " ; monospace")
mg(L, "Durango", "WD", "1", "2011-01", None,
   [("3.6 V6 294", "PENTASTAR-3.6", 353), ("R/T 5.7 V8 365", "HEMI-5.7", 529), ("R/T 392 6.4 V8 482", "HEMI-6.4", 637, {"debut": "2026-03"})], places=7, reservoir=93,
   remarques=NA + " ; restylages 2014 et 2021 ; SRT dans « Dodge SRT »")
mg(L, "Hornet", "GT", "1", "2023-01", None, [("GT 2.0 Turbo 272", "GME-2.0T", 400), ("R/T 1.3 PHEV 292", "GSE-1.3-PHEV", 520, {"batterie": 15, "debut": "2024-01"})],
   reservoir=55, remarques=NA + " ; base Alfa Romeo Tonale")
mg(L, "Ram 1500", "DR", "1", "2002-01", "2008-12", [("4.7 V8 238", "POWERTECH-4.7", 407), ("5.7 Hemi V8 350", "HEMI-5.7", 508, {"debut": "2003-01"})], portes=4, reservoir=98,
   remarques=NA + " ; pick-up")
mg(L, "Ram 1500", "DS", "1", "2009-01", "2010-12", [("4.7 V8 314", "POWERTECH-4.7", 447), ("5.7 Hemi V8 395", "HEMI-5.7", 552)], portes=4, reservoir=98,
   remarques=NA + " ; vendu ensuite sous la marque Ram")

# ---------------------------------------------------------------- Dodge SRT
mg(LS, "Viper", "SR", "1", "1992-01", "1995-12", [("RT/10 8.0 V10 406", "VIPER-8.0", 630)], portes=2, places=2, reservoir=83, remarques="Roadster ; " + IND)
mg(LS, "Viper", "SR", "2", "1996-01", "2002-12", [("GTS 8.0 V10 456", "VIPER-8.0", 664), ("GTS 8.0 V10 466", "VIPER-8.0", 664, {"debut": "1999-01"})], portes=2, places=2, reservoir=83,
   remarques="GTS coupé et RT/10 ; vendue en Europe (Chrysler Viper) ; " + IND)
mg(LS, "Viper", "ZB", "1", "2003-01", "2007-12", [("SRT-10 8.3 V10 507", "VIPER-8.3", 712)], portes=2, places=2, reservoir=70, remarques="Roadster et coupé (2006)")
mg(LS, "Viper", "ZB", "2", "2008-01", "2010-12", [("SRT-10 8.4 V10 608", "VIPER-8.4", 760), ("ACR 8.4 V10 608", "VIPER-8.4", 760, {"debut": "2009-01"})], portes=2, places=2, reservoir=70,
   remarques="Vendue en Europe")
mg(LS, "Viper", "VX", "1", "2013-01", "2017-08", [("SRT Viper 8.4 V10 649", "VIPER-8.4", 814), ("ACR 8.4 V10 654", "VIPER-8.4", 813, {"debut": "2016-01"})], portes=2, places=2, reservoir=70,
   remarques="Vendue SRT Viper en 2013-2014")
mg(LS, "Neon SRT-4", "PL", "2", "2003-01", "2005-12", [("SRT-4 2.4 Turbo 218", "NEON-2.4T", 332, {"fin": "2003-12"}), ("SRT-4 2.4 Turbo 233", "NEON-2.4T", 386, {"debut": "2004-01"})],
   portes=4, reservoir=47, remarques=NA)
mg(LS, "Caliber SRT4", "PM", "1", "2008-01", "2009-12", [("SRT4 2.4 Turbo 289", "WORLD-2.4T", 359)], reservoir=52, remarques=EUNA)
mg(LS, "Charger SRT8", "LX", "1", "2006-01", "2010-12", [("SRT8 6.1 V8 431", "HEMI-6.1", 569)], portes=4, reservoir=68, remarques=NA)
mg(LS, "Charger SRT", "LD", "1", "2012-01", "2023-12",
   [("SRT8 6.4 V8 476", "HEMI-6.4", 637, {"fin": "2014-12"}), ("SRT 392 6.4 V8 492", "HEMI-6.4", 644, {"debut": "2015-01", "fin": "2018-12"}),
    ("SRT Hellcat 6.2 V8 Compresseur 717", "HELLCAT-6.2SC", 881, {"debut": "2015-01"}), ("SRT Hellcat Widebody 6.2 V8 Compresseur 717", "HELLCAT-6.2SC", 881, {"debut": "2020-01"}),
    ("SRT Hellcat Redeye 6.2 V8 Compresseur 808", "HELLCAT-6.2SC", 959, {"debut": "2021-01"})], portes=4, reservoir=70, remarques=NA)
mg(LS, "Challenger SRT", "LC", "1", "2008-01", "2023-12",
   [("SRT8 6.1 V8 431", "HEMI-6.1", 569, {"fin": "2010-12"}), ("SRT8 392 6.4 V8 476", "HEMI-6.4", 637, {"debut": "2011-01", "fin": "2014-12"}),
    ("SRT 392 6.4 V8 492", "HEMI-6.4", 644, {"debut": "2015-01"}), ("SRT Hellcat 6.2 V8 Compresseur 717", "HELLCAT-6.2SC", 881, {"debut": "2015-01"}),
    ("SRT Hellcat Redeye 6.2 V8 Compresseur 808", "HELLCAT-6.2SC", 959, {"debut": "2019-01"}), ("SRT Demon 6.2 V8 Compresseur 852", "HELLCAT-6.2SC", 1044, {"debut": "2018-01", "fin": "2018-12"}),
    ("SRT Super Stock 6.2 V8 Compresseur 818", "HELLCAT-6.2SC", 959, {"debut": "2020-01"}), ("SRT Demon 170 6.2 V8 Compresseur 1039", "HELLCAT-6.2SC", 1281, {"debut": "2023-01"})],
   portes=2, places=4, reservoir=70, remarques=NA + " ; Demon : 2 places de série, puissance avec carburant course")
mg(LS, "Durango SRT", "WD", "1", "2018-01", "2024-12", [("SRT 392 6.4 V8 482", "HEMI-6.4", 637)], places=6, reservoir=93, remarques=NA)
mg(LS, "Durango SRT Hellcat", "WD", "2", "2021-01", None, [("SRT Hellcat 6.2 V8 Compresseur 720", "HELLCAT-6.2SC", 875)], places=6, reservoir=93,
   remarques=NA + " ; millésime 2021 puis retour 2023 ; Jailbreak (2026)")
mg(LS, "Ram 1500 TRX", "DT", "1", "2021-01", "2024-12", [("TRX 6.2 V8 Compresseur 712", "HELLCAT-6.2SC", 881)], portes=4, reservoir=125,
   remarques=NA + " ; vendu sous la marque Ram")

MOT = Motorisations("Dodge", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LS)

DETAIL = {"Dodge": L, "Dodge SRT": LS}
MOTEURS = MOT.moteurs()
