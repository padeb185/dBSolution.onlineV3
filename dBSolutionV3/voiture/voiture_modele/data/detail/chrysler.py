"""Chrysler : générations, motorisations et moteurs liés.
Amérique du Nord ; vendue aussi en Europe de 1988 à 2012 (Voyager, Neon, Stratus, Sebring, PT Cruiser, Crossfire, 300M, 300C…),
puis remplacée par Lancia sur ce marché. Puissances américaines converties en ch (×1,014).
Diesel 2.0 CRD : code de volkswagen.py (motoriste « Volkswagen ») ; diesels et V6 Mercedes au motoriste « Mercedes-Benz » (codes propres).
Données antérieures à 2000 indicatives. Saisie : (nom, famille, couple_nm[, surcharges]) ; puissance = dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .volkswagen import FAMILLES as FAMILLES_VW

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

VW = ("EA188-2.0TDI",)
MB = {
    "CHR-MB-M112-3.2": f("ATM", E_, 3.2, C, 6, 5700, 3000, "5W30", 8.0, 15000, a="V"),
    "CHR-MB-M112-3.2SC": f("TURBO", E_, 3.2, C, 6, 6100, 3500, "5W30", 8.0, 15000, a="V"),
    "CHR-MB-OM646-2.2": f("TURBO", D, 2.2, C, 4, 4000, 1600, "5W30", 6.5, 20000),
    "CHR-MB-OM642-3.0": f("TURBO", D, 3.0, C, 6, 4000, 1600, "5W30", 8.0, 20000, a="V"),
}
PROPRES = {
    "K-2.5": f("ATM", E_, 2.5, B, 4, 4800, 2800, "10W30", 4.3, 7500),
    "K-2.5T": f("TURBO", E_, 2.5, B, 4, 4800, 2400, "10W30", 4.3, 7500),
    "MITSU-3.0": f("ATM", E_, 3.0, B, 6, 5000, 2800, "10W30", 4.3, 7500, a="V"),
    "EGA-3.3": f("ATM", E_, 3.3, C, 6, 5000, 3200, "5W30", 4.3, 12000, a="V"),
    "EGH-3.8": f("ATM", E_, 3.8, C, 6, 5000, 3200, "5W30", 4.3, 12000, a="V"),
    "NEON-1.6": f("ATM", E_, 1.6, B, 4, 5800, 4300, "5W30", 4.3, 12000),
    "NEON-2.0": f("ATM", E_, 2.0, B, 4, 6000, 4500, "5W30", 4.3, 12000),
    "NEON-2.4": f("ATM", E_, 2.4, B, 4, 5600, 4000, "5W30", 4.3, 12000),
    "NEON-2.4T": f("TURBO", E_, 2.4, B, 4, 5200, 2800, "5W30", 4.3, 12000),
    "WORLD-2.0": f("ATM", E_, 2.0, C, 4, 6300, 5100, "5W20", 4.3, 12000),
    "WORLD-2.4": f("ATM", E_, 2.4, C, 4, 6000, 4500, "5W20", 4.3, 12000),
    "TIGERSHARK-2.4": f("ATM", E_, 2.4, B, 4, 6250, 4800, "0W20", 5.2, 12000),
    "EER-2.5": f("ATM", E_, 2.5, C, 6, 5900, 4350, "5W30", 5.0, 12000, a="V"),
    "EER-2.7": f("ATM", E_, 2.7, C, 6, 6400, 4000, "5W20", 5.0, 12000, a="V"),
    "EGJ-3.5": f("ATM", E_, 3.5, C, 6, 6400, 4000, "5W20", 5.0, 12000, a="V"),
    "PENTASTAR-3.6": f("ATM", E_, 3.6, C, 6, 6350, 4800, "0W20", 5.7, 12000, a="V"),
    "PENTASTAR-3.6-PHEV": f("HYB_E", E_, 3.6, C, 6, 5800, 4000, "0W20", 5.7, 12000, a="V"),
    "POWERTECH-4.7": f("ATM", E_, 4.7, C, 8, 5650, 3950, "5W20", 6.6, 12000, a="V"),
    "HEMI-5.7": f("ATM", E_, 5.7, C, 8, 5600, 4200, "5W20", 6.6, 12000, a="V"),
    "HEMI-6.1": f("ATM", E_, 6.1, C, 8, 6200, 4800, "5W20", 6.6, 12000, a="V"),
    "HEMI-6.4": f("ATM", E_, 6.4, C, 8, 6000, 4300, "0W40", 6.6, 12000, a="V"),
    "VM-2.5TD": f("TURBO", D, 2.5, B, 4, 4000, 2000, "10W40", 6.0, 10000),
    "VM-2.5CRD": f("TURBO", D, 2.5, C, 4, 3800, 1800, "5W30", 6.0, 15000),
    "VM-2.8CRD": f("TURBO", D, 2.8, C, 4, 3800, 1800, "5W30", 6.0, 15000),
    "VM-3.0CRD": f("TURBO", D, 3.0, C, 6, 4000, 1800, "5W30", 7.0, 15000, a="V"),
}
FAMILLES = {**{k: FAMILLES_VW[k] for k in VW}, **MB, **PROPRES}


def mot(fam):
    return "Volkswagen" if fam in VW else ("Mercedes-Benz" if fam in MB else "Chrysler")


mg = SaisieMoteurs(FAMILLES, "Chrysler", mot)
L = []
NA = "Marché nord-américain"
EUNA = "Amérique du Nord et Europe"
IND = "données indicatives"

# ---------------------------------------------------------------- années 1987-2000
mg(L, "LeBaron", "J-body", "1", "1987-01", "1995-12", [("2.5 100", "K-2.5", 182), ("2.5 Turbo 152", "K-2.5T", 285), ("3.0 V6 143", "MITSU-3.0", 233, {"debut": "1990-01"})],
   portes=2, places=4, reservoir=53, remarques=EUNA + " ; coupé et cabriolet ; " + IND)
mg(L, "Imperial", "Y-body", "1", "1990-01", "1993-12", [("3.8 V6 152", "EGH-3.8", 271)], portes=4, reservoir=61, remarques=NA + " ; " + IND)
mg(L, "New Yorker", "LH", "1", "1994-01", "1996-12", [("3.5 V6 217", "EGJ-3.5", 300)], portes=4, reservoir=68, remarques=NA + " ; " + IND)
mg(L, "Vision", "LH", "V", "1993-01", "1997-12", [("3.5 V6 217", "EGJ-3.5", 300)], portes=4, reservoir=68, remarques="Réservée à l'Europe (Eagle Vision) ; " + IND)
mg(L, "Neon", "PL", "1", "1995-01", "2002-12", [("2.0 133", "NEON-2.0", 176), ("1.6 116", "NEON-1.6", 157, {"debut": "2000-01"}), ("2.0 141", "NEON-2.0", 176, {"debut": "2000-01"})],
   portes=4, reservoir=47, remarques="Europe (Dodge Neon en Amérique du Nord) ; " + IND)
mg(L, "Stratus", "JA", "1", "1995-01", "2001-12", [("2.0 133", "NEON-2.0", 176), ("2.4 152", "NEON-2.4", 226), ("2.5 V6 165", "EER-2.5", 217)], portes=4, reservoir=60,
   remarques=EUNA + " ; berline et cabriolet ; " + IND)
mg(L, "300M", "LH", "2", "1999-01", "2004-12", [("2.7 V6 203", "EER-2.7", 258), ("3.5 V6 257", "EGJ-3.5", 346)], portes=4, reservoir=65, remarques=EUNA)

# ---------------------------------------------------------------- monospaces
mg(L, "Voyager", "GS", "1", "1996-01", "2000-12",
   [("2.0 133", "NEON-2.0", 176), ("2.4 152", "NEON-2.4", 226), ("3.3 V6 160", "EGA-3.3", 275), ("3.8 V6 168", "EGH-3.8", 305), ("2.5 TD 117", "VM-2.5TD", 270)],
   places=7, reservoir=75, remarques=EUNA + " ; Voyager et Grand Voyager (Graz) ; " + IND)
mg(L, "Voyager", "RG", "1", "2001-01", "2007-12",
   [("2.4 148", "NEON-2.4", 214), ("3.3 V6 177", "EGA-3.3", 285), ("3.8 V6 184", "EGH-3.8", 317), ("2.5 CRD 143", "VM-2.5CRD", 320), ("2.8 CRD 150", "VM-2.8CRD", 360, {"debut": "2004-01"})],
   places=7, reservoir=75, remarques=EUNA + " ; Voyager et Grand Voyager")
mg(L, "Grand Voyager", "RT", "1", "2008-01", "2015-12", [("3.8 V6 197", "EGH-3.8", 312), ("2.8 CRD 163", "VM-2.8CRD", 360), ("2.8 CRD 178", "VM-2.8CRD", 360, {"debut": "2011-01"})],
   places=7, reservoir=76, remarques="Europe ; vendu Lancia Voyager à partir de 2011 sur plusieurs marchés")
mg(L, "Town & Country", "RT", "T", "2008-01", "2016-12", [("3.8 V6 200", "EGH-3.8", 312, {"fin": "2010-12"}), ("4.0 V6 255", "EGJ-3.5", 352, {"fin": "2010-12"}),
                                                          ("3.6 V6 287", "PENTASTAR-3.6", 353, {"debut": "2011-01"})], places=7, reservoir=76, remarques=NA)
mg(L, "Pacifica", "RU", "1", "2017-01", None, [("3.6 V6 291", "PENTASTAR-3.6", 355), ("Hybrid 264", "PENTASTAR-3.6-PHEV", 355, {"batterie": 16})], places=7, reservoir=72,
   remarques=NA + " ; restylage 2021 ; Pacifica Hybrid rechargeable (réservoir 62 l)")
mg(L, "Voyager", "RU", "V", "2020-01", None, [("3.6 V6 291", "PENTASTAR-3.6", 355)], places=7, reservoir=72, remarques=NA + " ; version simplifiée de la Pacifica")
mg(L, "Aspen", "HG", "1", "2007-01", "2009-12", [("4.7 V8 307", "POWERTECH-4.7", 454), ("5.7 Hemi V8 381", "HEMI-5.7", 542)], places=8, reservoir=102, remarques=NA + " ; SUV (base Dodge Durango)")

# ---------------------------------------------------------------- années 2000-2023
mg(L, "PT Cruiser", "PT", "1", "2000-06", "2010-07",
   [("1.6 116", "NEON-1.6", 145), ("2.0 141", "NEON-2.0", 178), ("2.4 143", "NEON-2.4", 210, {"debut": "2004-01"}), ("GT 2.4 Turbo 223", "NEON-2.4T", 332, {"debut": "2003-01"}),
    ("2.2 CRD 121", "CHR-MB-OM646-2.2", 300, {"debut": "2002-01"})], reservoir=57, remarques=EUNA + " ; cabriolet (2004)")
mg(L, "Crossfire", "ZH", "1", "2003-09", "2008-12", [("3.2 V6 218", "CHR-MB-M112-3.2", 310), ("SRT-6 3.2 V6 Compresseur 335", "CHR-MB-M112-3.2SC", 420, {"debut": "2004-06", "fin": "2006-12"})],
   portes=2, places=2, reservoir=60, remarques=EUNA + " ; coupé et roadster (base Mercedes SLK R170, Karmann)")
mg(L, "Sebring", "JR", "1", "2001-01", "2006-12", [("2.0 141", "NEON-2.0", 180), ("2.4 152", "NEON-2.4", 226), ("2.7 V6 203", "EER-2.7", 258)], portes=4, reservoir=61,
   remarques=EUNA + " ; berline et cabriolet")
mg(L, "Sebring", "JS", "1", "2007-01", "2010-12", [("2.0 158", "WORLD-2.0", 190), ("2.4 174", "WORLD-2.4", 224), ("2.7 V6 192", "EER-2.7", 258), ("3.5 V6 239", "EGJ-3.5", 315),
                                                  ("2.0 CRD 140", "EA188-2.0TDI", 310)], portes=4, reservoir=64, remarques=EUNA + " ; berline et cabriolet")
mg(L, "200", "JS", "2", "2011-01", "2014-12", [("2.4 175", "WORLD-2.4", 225), ("3.6 V6 287", "PENTASTAR-3.6", 353)], portes=4, reservoir=64, remarques=NA + " ; berline et cabriolet")
mg(L, "200", "UF", "1", "2015-01", "2017-12", [("2.4 187", "TIGERSHARK-2.4", 237), ("3.6 V6 299", "PENTASTAR-3.6", 353)], portes=4, reservoir=60, remarques=NA)
mg(L, "300C", "LX", "1", "2005-01", "2010-12",
   [("2.7 V6 193", "EER-2.7", 258), ("3.5 V6 253", "EGJ-3.5", 340), ("5.7 Hemi V8 345", "HEMI-5.7", 525), ("3.0 CRD 218", "CHR-MB-OM642-3.0", 510, {"debut": "2006-01"}),
    ("SRT-8 6.1 V8 431", "HEMI-6.1", 569, {"debut": "2006-01"})], portes=4, reservoir=72, remarques=EUNA + " ; berline et Touring (break, Europe)")
mg(L, "300", "LD", "1", "2011-01", "2023-12",
   [("3.6 V6 296", "PENTASTAR-3.6", 353), ("3.6 V6 304", "PENTASTAR-3.6", 359, {"debut": "2015-01"}), ("5.7 Hemi V8 368", "HEMI-5.7", 536),
    ("SRT8 6.4 V8 476", "HEMI-6.4", 637, {"debut": "2012-01", "fin": "2014-12"}), ("300C 6.4 V8 492", "HEMI-6.4", 644, {"debut": "2023-01"}),
    ("3.0 CRD 239", "VM-3.0CRD", 550, {"fin": "2014-12"})], portes=4, reservoir=72, remarques=EUNA + " ; vendue Lancia Thema en Europe continentale ; restylage 2015")

MOT = Motorisations("Chrysler", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Chrysler": L}
MOTEURS = MOT.moteurs()
