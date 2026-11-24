"""Cadillac et Cadillac V-Series : générations, motorisations et moteurs liés.
Marché nord-américain pour les thermiques ; électriques Lyriq, Optiq et Vistiq aussi vendus en Europe ; BLS réservée à l'Europe.
Puissances converties des hp américains en ch (×1,014, arrondi). Modèles d'avant 1987 non repris ; données antérieures à 2000 indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"


def v8(t, l, rpm, nmrpm, q=7.0):
    return f(t, E_, l, C, 8, rpm, nmrpm, "5W30", q, 12000, a="V")


def v6(t, l, rpm, nmrpm, q=5.7):
    return f(t, E_, l, C, 6, rpm, nmrpm, "5W30", q, 12000, a="V")


FAMILLES = {
    "CAD-HT-4.1": v8("ATM", 4.1, 4400, 2200, 5.0), "CAD-HT-4.5": v8("ATM", 4.5, 4400, 3000, 5.0), "CAD-HT-4.9": v8("ATM", 4.9, 4400, 3000, 5.0),
    "NORTHSTAR-4.6": v8("ATM", 4.6, 5600, 4400, 7.1), "NORTHSTAR-4.4SC": v8("TURBO", 4.4, 6400, 3600, 7.1),
    "LT1-5.7": v8("ATM", 5.7, 5000, 2400, 5.7), "VORTEC-5.3": v8("ATM", 5.3, 5200, 4000, 5.7), "VORTEC-6.0": v8("ATM", 6.0, 5200, 4000, 5.7),
    "LS6-5.7": v8("ATM", 5.7, 6000, 4800, 5.7), "L92-6.2": v8("ATM", 6.2, 5700, 4300, 7.6), "L86-6.2": v8("ATM", 6.2, 5600, 4100, 7.6),
    "LSA-6.2SC": v8("TURBO", 6.2, 6100, 3800, 8.5), "LT4-6.2SC": v8("TURBO", 6.2, 6400, 3600, 9.8),
    "BLACKWING-4.2TT": v8("TURBO", 4.2, 5700, 3200, 8.0),
    "SAAB-V6-2.8T": v6("TURBO", 2.8, 5500, 1800, 5.5), "GM-V6-2.8": v6("ATM", 2.8, 6500, 3300),
    "GM-V6-3.0": v6("ATM", 3.0, 6800, 5100), "GM-V6-3.2": v6("ATM", 3.2, 6200, 3400), "GM-V6-3.6": v6("ATM", 3.6, 6800, 5200),
    "GM-V6-3.6TT": v6("TURBO", 3.6, 5800, 3500), "GM-V6-3.0TT": v6("TURBO", 3.0, 5700, 2500), "GM-V6-2.8T": v6("TURBO", 2.8, 5500, 2000),
    "GM-2.0T": f("TURBO", E_, 2.0, C, 4, 5500, 1500, "0W20", 5.0, 12000), "GM-2.5": f("ATM", E_, 2.5, C, 4, 6300, 4400, "5W30", 4.7, 12000),
    "GM-2.7T": f("TURBO", E_, 2.7, C, 4, 5600, 2000, "0W20", 6.0, 12000),
    "SAAB-1.8T": f("TURBO", E_, 1.8, C, 4, 5500, 2000, "5W30", 4.0, 15000), "SAAB-2.0T": f("TURBO", E_, 2.0, C, 4, 5300, 2000, "5W30", 4.0, 15000),
    "FIAT-1.9TID": f("TURBO", D, 1.9, B, 4, 4000, 2000, "5W30", 4.5, 20000),
    "DURAMAX-3.0": f("TURBO", D, 3.0, C, 6, 3750, 1500, "0W20", 6.6, 12000),
    "VOLTEC-1.4": f("HYB_E", E_, 1.4, C, 4, 4800, 0, "0W20", 4.0, 15000),
    "GM-2.0T-PHEV": f("HYB_E", E_, 2.0, C, 4, 5000, 1500, "0W20", 5.0, 12000),
    "ULTIUM": electrique(),
}

mg = SaisieMoteurs(FAMILLES, "Cadillac")
L, LV = [], []   # Cadillac, Cadillac V-Series
NA = "Marché nord-américain"
IND = NA + " ; données indicatives"

# ---------------------------------------------------------------- grandes berlines / coupés
mg(L, "Allanté", "Allanté", "1", "1987-01", "1993-12",
   [("4.1 V8 172", "CAD-HT-4.1", 319, {"fin": "1988-12"}), ("4.5 V8 203", "CAD-HT-4.5", 366, {"debut": "1989-01", "fin": "1992-12"}), ("Northstar 4.6 V8 299", "NORTHSTAR-4.6", 393, {"debut": "1993-01"})],
   portes=2, places=2, reservoir=83, remarques=IND + " ; cabriolet carrossé par Pininfarina")
mg(L, "Fleetwood", "D-body", "1", "1993-01", "1996-12", [("5.7 V8 264", "LT1-5.7", 447)], portes=4, places=6, reservoir=87, remarques=IND + " ; propulsion")
mg(L, "DeVille", "K-body", "1", "1994-01", "1999-12", [("4.9 V8 203", "CAD-HT-4.9", 373, {"fin": "1995-12"}), ("Northstar 4.6 V8 279", "NORTHSTAR-4.6", 407)],
   portes=4, places=6, reservoir=76, remarques=IND + " ; Concours")
mg(L, "DeVille", "G-body", "1", "2000-01", "2005-12", [("Northstar 4.6 V8 279", "NORTHSTAR-4.6", 407), ("DTS 4.6 V8 304", "NORTHSTAR-4.6", 400)], portes=4, places=6, reservoir=70, remarques=NA)
mg(L, "DTS", "G-body", "2", "2006-01", "2011-12", [("4.6 V8 279", "NORTHSTAR-4.6", 393), ("4.6 V8 296", "NORTHSTAR-4.6", 403)], portes=4, places=6, reservoir=70, remarques=NA)
mg(L, "Seville", "K-body", "1", "1992-01", "1997-12", [("SLS 4.6 V8 279", "NORTHSTAR-4.6", 407), ("STS 4.6 V8 304", "NORTHSTAR-4.6", 400)], portes=4, reservoir=76, remarques=IND)
mg(L, "Seville", "G-body", "1", "1998-01", "2004-12", [("SLS 4.6 V8 279", "NORTHSTAR-4.6", 407), ("STS 4.6 V8 304", "NORTHSTAR-4.6", 400)], portes=4, reservoir=70,
   remarques=NA + " ; aussi vendue en Europe")
mg(L, "Eldorado", "E-body", "1", "1992-01", "2002-12", [("Northstar 4.6 V8 279", "NORTHSTAR-4.6", 407), ("ETC 4.6 V8 304", "NORTHSTAR-4.6", 400)], portes=2, places=5, reservoir=76,
   remarques=IND + " ; coupé")
mg(L, "Catera", "V-body", "1", "1997-01", "2001-12", [("3.0 V6 203", "GM-V6-3.0", 260)], portes=4, reservoir=68, remarques=IND + " ; base Opel Omega B")

# ---------------------------------------------------------------- berlines « Art & Science »
mg(L, "CTS", "Sigma", "1", "2003-01", "2007-12", [("2.8 V6 213", "GM-V6-2.8", 252, {"debut": "2005-01"}), ("3.2 V6 223", "GM-V6-3.2", 295, {"fin": "2004-12"}),
                                                  ("3.6 V6 259", "GM-V6-3.6", 343, {"debut": "2004-01"})], portes=4, reservoir=66, remarques=NA + " ; aussi vendue en Europe")
mg(L, "CTS", "Sigma II", "1", "2008-01", "2013-12", [("3.0 V6 274", "GM-V6-3.0", 302, {"debut": "2010-01"}), ("3.6 V6 309", "GM-V6-3.6", 370), ("3.6 V6 322", "GM-V6-3.6", 373, {"debut": "2012-01"})],
   portes=4, reservoir=68, remarques=NA + " ; berline, coupé (2011), Sport Wagon (2010)")
mg(L, "CTS", "Alpha", "1", "2014-01", "2019-12", [("2.0 Turbo 276", "GM-2.0T", 400), ("3.6 V6 340", "GM-V6-3.6", 386), ("V-Sport 3.6 V6 Twin Turbo 426", "GM-V6-3.6TT", 583)],
   portes=4, reservoir=72, remarques=NA)
mg(L, "STS", "Sigma", "S", "2005-01", "2011-12", [("3.6 V6 259", "GM-V6-3.6", 343), ("3.6 V6 306", "GM-V6-3.6", 368, {"debut": "2008-01"}), ("4.6 V8 325", "NORTHSTAR-4.6", 427)],
   portes=4, reservoir=66, remarques=NA + " ; aussi vendue en Europe")
mg(L, "BLS", "Epsilon", "1", "2006-01", "2010-03",
   [("1.8 Turbo 150", "SAAB-1.8T", 240), ("2.0 Turbo 175", "SAAB-2.0T", 265), ("2.0 Turbo 210", "SAAB-2.0T", 300), ("2.8 V6 Turbo 255", "SAAB-V6-2.8T", 350),
    ("1.9 TiD 150", "FIAT-1.9TID", 320), ("1.9 TiD 180", "FIAT-1.9TID", 400, {"debut": "2008-01"})], portes=4, reservoir=62,
   remarques="Réservée à l'Europe (base Saab 9-3, Trollhättan) ; berline et Wagon (2007)")
mg(L, "XLR", "Y-body", "1", "2004-01", "2009-12", [("4.6 V8 325", "NORTHSTAR-4.6", 421)], portes=2, places=2, reservoir=68, remarques=NA + " ; roadster coupé-cabriolet")
mg(L, "ELR", "Voltec", "1", "2014-01", "2016-12", [("ELR 210", "VOLTEC-1.4", 400, {"batterie": 17}), ("ELR 237", "VOLTEC-1.4", 508, {"batterie": 17, "debut": "2016-01"})],
   portes=2, places=4, reservoir=35, remarques=NA + " ; coupé hybride à prolongateur d'autonomie")
mg(L, "ATS", "Alpha", "A", "2013-01", "2019-12", [("2.5 205", "GM-2.5", 259), ("2.0 Turbo 276", "GM-2.0T", 400), ("3.6 V6 325", "GM-V6-3.6", 373), ("3.6 V6 340", "GM-V6-3.6", 386)],
   portes=4, reservoir=61, remarques=NA + " ; berline et coupé ; aussi vendue en Europe")
mg(L, "XTS", "Epsilon II", "1", "2013-01", "2019-12", [("3.6 V6 309", "GM-V6-3.6", 359), ("V-Sport 3.6 V6 Twin Turbo 416", "GM-V6-3.6TT", 502, {"debut": "2014-01"})],
   portes=4, reservoir=72, remarques=NA)
mg(L, "CT6", "Omega", "1", "2016-01", "2020-12",
   [("2.0 Turbo 269", "GM-2.0T", 400), ("3.6 V6 340", "GM-V6-3.6", 386), ("3.0 V6 Twin Turbo 410", "GM-V6-3.0TT", 543),
    ("Plug-in 340", "GM-2.0T-PHEV", 586, {"batterie": 18, "debut": "2017-01", "fin": "2018-12"}), ("Platinum 4.2 V8 Twin Turbo 507", "BLACKWING-4.2TT", 773, {"debut": "2019-01"})],
   portes=4, reservoir=73, remarques=NA)
mg(L, "CT4", "Alpha", "4", "2020-01", "2026-06", [("2.0 Turbo 241", "GM-2.0T", 350), ("2.7 Turbo 314", "GM-2.7T", 515)], portes=4, reservoir=61,
   remarques=NA + " ; production arrêtée en juin 2026, sans successeur")
mg(L, "CT5", "Alpha", "5", "2020-01", "2026-12", [("2.0 Turbo 241", "GM-2.0T", 350), ("3.0 V6 Twin Turbo 340", "GM-V6-3.0TT", 542)], portes=4, reservoir=65,
   remarques=NA + " ; restylage 2025 ; fin fin 2026, nouvelle génération thermique annoncée")

# ---------------------------------------------------------------- SUV thermiques
mg(L, "Escalade", "GMT400", "1", "1999-01", "2000-12", [("5.7 V8 259", "LT1-5.7", 447)], reservoir=114, remarques=IND)
mg(L, "Escalade", "GMT800", "1", "2002-01", "2006-12", [("5.3 V8 289", "VORTEC-5.3", 441), ("6.0 V8 350", "VORTEC-6.0", 515)], places=7, reservoir=98, remarques=NA + " ; ESV et EXT")
mg(L, "Escalade", "GMT900", "1", "2007-01", "2014-12", [("6.2 V8 409", "L92-6.2", 565), ("Hybrid 6.0 V8 337", "VORTEC-6.0", 498, {"debut": "2009-01", "fin": "2013-12"})],
   places=7, reservoir=98, remarques=NA + " ; ESV et EXT ; aussi vendu en Europe")
mg(L, "Escalade", "K2XL", "1", "2015-01", "2020-12", [("6.2 V8 426", "L86-6.2", 623)], places=7, reservoir=98, remarques=NA + " ; ESV")
mg(L, "Escalade", "T1XX", "1", "2021-01", None, [("6.2 V8 426", "L86-6.2", 624), ("3.0 Duramax 281", "DURAMAX-3.0", 624)], places=7, reservoir=91,
   remarques=NA + " ; ESV ; restylage 2025")
mg(L, "SRX", "Sigma", "X", "2004-01", "2009-12", [("3.6 V6 259", "GM-V6-3.6", 344), ("4.6 V8 325", "NORTHSTAR-4.6", 427)], places=7, reservoir=76, remarques=NA + " ; aussi vendu en Europe")
mg(L, "SRX", "Theta", "1", "2010-01", "2016-12",
   [("3.0 V6 268", "GM-V6-3.0", 302, {"fin": "2011-12"}), ("2.8 V6 Turbo 304", "GM-V6-2.8T", 400, {"fin": "2011-12"}), ("3.6 V6 312", "GM-V6-3.6", 359, {"debut": "2012-01"})],
   reservoir=76, remarques=NA)
mg(L, "XT5", "C1XX", "1", "2017-01", None, [("2.0 Turbo 241", "GM-2.0T", 350), ("3.6 V6 314", "GM-V6-3.6", 367)], reservoir=83, remarques=NA + " ; restylage 2020")
mg(L, "XT4", "E2XX", "1", "2019-01", "2025-12", [("2.0 Turbo 241", "GM-2.0T", 350)], reservoir=61, remarques=NA + " ; aussi vendu en Europe (2019-2021) ; remplacé par l'Optiq")
mg(L, "XT6", "C1XX", "6", "2020-01", "2025-12", [("2.0 Turbo 241", "GM-2.0T", 350), ("3.6 V6 314", "GM-V6-3.6", 367)], places=7, reservoir=83, remarques=NA + " ; remplacé par le Vistiq")

# ---------------------------------------------------------------- électriques
mg(L, "Lyriq", "BEV3", "1", "2023-01", None, [("RWD 345", "ULTIUM", 440, {"batterie": 102}), ("AWD 507", "ULTIUM", 610, {"batterie": 102})], reservoir=0,
   remarques="Électrique ; vendu en Europe depuis 2024")
mg(L, "Optiq", "BEV3", "O", "2025-01", None, [("AWD 304", "ULTIUM", 480, {"batterie": 85}), ("RWD 304", "ULTIUM", 400, {"batterie": 85, "debut": "2025-09"})], reservoir=0,
   remarques="Électrique compact ; vendu en Europe depuis fin 2025 (batterie plus petite, non détaillée)")
mg(L, "Vistiq", "BEV3", "V", "2025-01", None, [("AWD 622", "ULTIUM", 880, {"batterie": 102})], places=7, reservoir=0, remarques="SUV électrique 3 rangées ; vendu en Europe")
mg(L, "Escalade IQ", "BT1", "1", "2024-07", None, [("Escalade IQ 760", "ULTIUM", 1064, {"batterie": 205}), ("Escalade IQL 760", "ULTIUM", 1064, {"batterie": 205, "debut": "2025-09"})],
   places=7, reservoir=0, remarques=NA + " ; puissance en mode Velocity Max")
mg(L, "Celestiq", "BEV3", "C", "2025-01", None, [("Celestiq 609", "ULTIUM", 875, {"batterie": 111})], portes=4, reservoir=0, remarques=NA + " ; fabrication à la main, sur commande")

# ---------------------------------------------------------------- Cadillac V-Series
mg(LV, "CTS-V", "Sigma", "1", "2004-01", "2007-12", [("CTS-V 5.7 V8 406", "LS6-5.7", 536, {"fin": "2005-12"}), ("CTS-V 6.0 V8 406", "VORTEC-6.0", 542, {"debut": "2006-01"})],
   portes=4, reservoir=68, remarques=NA)
mg(LV, "CTS-V", "Sigma II", "1", "2009-01", "2015-12", [("CTS-V 6.2 V8 Compresseur 564", "LSA-6.2SC", 747)], portes=4, reservoir=68, remarques=NA + " ; berline, coupé, Wagon")
mg(LV, "CTS-V", "Alpha", "1", "2016-01", "2019-12", [("CTS-V 6.2 V8 Compresseur 649", "LT4-6.2SC", 855)], portes=4, reservoir=72, remarques=NA)
mg(LV, "STS-V", "Sigma", "S", "2006-01", "2009-12", [("STS-V 4.4 V8 Compresseur 476", "NORTHSTAR-4.4SC", 597)], portes=4, reservoir=66, remarques=NA)
mg(LV, "XLR-V", "Y-body", "1", "2006-01", "2009-12", [("XLR-V 4.4 V8 Compresseur 449", "NORTHSTAR-4.4SC", 583)], portes=2, places=2, reservoir=68, remarques=NA)
mg(LV, "ATS-V", "Alpha", "A", "2016-01", "2019-12", [("ATS-V 3.6 V6 Twin Turbo 470", "GM-V6-3.6TT", 603)], portes=4, reservoir=61, remarques=NA + " ; berline et coupé")
mg(LV, "CT4-V", "Alpha", "4", "2020-01", "2026-06", [("CT4-V 2.7 Turbo 330", "GM-2.7T", 515), ("Blackwing 3.6 V6 Twin Turbo 479", "GM-V6-3.6TT", 603, {"debut": "2022-01"})],
   portes=4, reservoir=61, remarques=NA)
mg(LV, "CT5-V", "Alpha", "5", "2020-01", "2026-12", [("CT5-V 3.0 V6 Twin Turbo 365", "GM-V6-3.0TT", 549), ("Blackwing 6.2 V8 Compresseur 677", "LT4-6.2SC", 893, {"debut": "2022-01"})],
   portes=4, reservoir=61, remarques=NA)
mg(LV, "Escalade-V", "T1XX", "1", "2023-01", None, [("Escalade-V 6.2 V8 Compresseur 691", "LT4-6.2SC", 885)], places=7, reservoir=91, remarques=NA + " ; ESV-V")
mg(LV, "Lyriq-V", "BEV3", "1", "2025-01", None, [("Lyriq-V 624", "ULTIUM", 880, {"batterie": 102})], reservoir=0, remarques="Électrique ; vendu en Europe depuis juin 2025")
mg(LV, "Optiq-V", "BEV3", "O", "2026-01", None, [("Optiq-V 527", "ULTIUM", 650, {"batterie": 85})], reservoir=0, remarques=NA + " ; couple indicatif")

MOT = Motorisations("Cadillac", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LV)

DETAIL = {"Cadillac": L, "Cadillac V-Series": LV}
MOTEURS = MOT.moteurs()
