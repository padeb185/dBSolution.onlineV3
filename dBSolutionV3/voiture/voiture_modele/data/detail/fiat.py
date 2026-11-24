"""Fiat : générations, phases, motorisations (marché européen) et moteurs liés.
Classiques (500, 126, 127, 128, 131, Ritmo, Uno, Panda 141), puis Cinquecento, Seicento, Tipo, Tempra, Croma,
Punto, Bravo/Brava, Marea, Stilo, Multipla, Idea, Sedici, Barchetta, Coupé, 124 Spider, Panda, 500 / 500e / 500L / 500X,
Grande Panda, 600, Doblò, Qubo, Freemont. Versions Abarth dans la marque Abarth ; utilitaires purs non couverts.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


FAMILLES = {
    # --- essence anciennes
    "F2-0.5": f("ATM", E_, 0.5, C, 2, 4600, 3000, "20W50", 2.25, 5000),
    "F2-0.6": f("ATM", E_, 0.6, C, 2, 4800, 3000, "20W50", 2.25, 5000),
    "F100-0.9": f("ATM", E_, 0.9, C, 4, 5600, 3000, "20W50", 3.5, 5000),
    "F100-1.05": f("ATM", E_, 1.05, B, 4, 5600, 3000, "20W50", 3.5, 7500),
    "F128-1.1": f("ATM", E_, 1.1, B, 4, 6000, 3000, "20W50", 4.0, 7500),
    "F128-1.3": f("ATM", E_, 1.3, B, 4, 5800, 3200, "20W50", 4.0, 7500),
    "F128-1.5": f("ATM", E_, 1.5, B, 4, 5800, 3000, "15W40", 4.0, 10000),
    "F128-1.3T": f("TURBO", E_, 1.3, B, 4, 5750, 3200, "15W40", 4.0, 10000),
    "F128-1.4T": f("TURBO", E_, 1.4, B, 4, 6000, 3500, "10W40", 4.0, 10000),
    "FTC-1.6": f("ATM", E_, 1.6, B, 4, 6000, 4000, "15W40", 4.5, 10000),
    "FTC-2.0": f("ATM", E_, 2.0, B, 4, 5600, 3600, "15W40", 4.5, 10000),
    "FTC-2.0T": f("TURBO", E_, 2.0, B, 4, 5500, 3000, "10W40", 4.5, 10000),
    "FTC-1.4": f("ATM", E_, 1.4, B, 4, 6000, 3000, "15W40", 4.0, 10000),
    # --- FIRE / Torque / Pratola Serra
    "FIRE-0.75": f("ATM", E_, 0.75, B, 4, 5250, 3000, "15W40", 3.0, 10000),
    "FIRE-1.0": f("ATM", E_, 1.0, B, 4, 5500, 3000, "15W40", 3.0, 10000),
    "FIRE-1.1": f("ATM", E_, 1.1, B, 4, 5250, 3000, "10W40", 3.0, 15000),
    "FIRE-1.2": f("ATM", E_, 1.2, B, 4, 5500, 3000, "10W40", 3.0, 15000),
    "FIRE-1.2-16V": f("ATM", E_, 1.2, B, 4, 5000, 4000, "10W40", 3.0, 15000),
    "FIRE-1.4": f("ATM", E_, 1.4, B, 4, 6000, 3000, "5W40", 3.0, 15000),
    "FIRE-1.4-16V": f("ATM", E_, 1.4, B, 4, 6000, 4500, "5W40", 3.0, 15000),
    "TJET-1.4": f("TURBO", E_, 1.4, B, 4, 5000, 2250, "5W40", 3.5, 15000),
    "MULTIAIR-1.4": f("ATM", E_, 1.4, B, 4, 6500, 4000, "5W40", 3.5, 15000),
    "MULTIAIR-1.4T": f("TURBO", E_, 1.4, B, 4, 5500, 2500, "5W40", 3.5, 15000),
    "TWINAIR-0.9": f("TURBO", E_, 0.9, C, 2, 5500, 1900, "5W40", 3.0, 15000),
    "FIREFLY-1.0-HYB": f("HYB_TE", E_, 1.0, C, 3, 6000, 3500, "0W20", 3.0, 15000),
    "FIREFLY-1.0T": f("TURBO", E_, 1.0, C, 3, 5750, 1750, "0W20", 3.5, 15000),
    "FIREFLY-1.3T": f("TURBO", E_, 1.3, C, 4, 5500, 1850, "0W20", 3.5, 15000),
    "FIREFLY-1.5-HYB": f("HYB_TE", E_, 1.5, C, 4, 5750, 1500, "0W20", 4.0, 15000),
    "ETORQ-1.6": f("ATM", E_, 1.6, C, 4, 5500, 4500, "5W40", 4.0, 15000),
    "TWINCAM-1.6": f("ATM", E_, 1.6, B, 4, 5750, 4000, "10W40", 4.0, 15000),
    "TWINCAM-1.8": f("ATM", E_, 1.8, B, 4, 6300, 4400, "10W40", 4.0, 15000),
    "PRATOLA-2.0-20V": f("ATM", E_, 2.0, B, 5, 6500, 4500, "10W40", 5.0, 15000),
    "PRATOLA-2.0-20VT": f("TURBO", E_, 2.0, B, 5, 5750, 2500, "10W40", 5.0, 15000),
    "PRATOLA-2.4-20V": f("ATM", E_, 2.4, B, 5, 6500, 3500, "10W40", 5.0, 15000),
    "GM-2.2": f("ATM", E_, 2.2, C, 4, 5600, 4000, "5W30", 4.5, 15000),
    "SUZ-M16A": f("ATM", E_, 1.6, C, 4, 6000, 4400, "5W30", 4.0, 15000),
    "PENTASTAR-3.6": f("ATM", E_, 3.6, C, 6, 6350, 4300, "5W30", 5.7, 15000, a="V"),
    # --- Stellantis
    "EB2": f("TURBO", E_, 1.2, C, 3, 5500, 1750, "0W20", 3.5, 25000),
    "EB2-MHEV": f("HYB_TE", E_, 1.2, C, 3, 5500, 1750, "0W20", 3.5, 25000),
    # --- diesel
    "D-1.7": f("ATM", D, 1.7, B, 4, 4500, 2500, "15W40", 4.5, 10000),
    "TD-1.7": f("TURBO", D, 1.7, B, 4, 4500, 2500, "15W40", 4.5, 10000),
    "D-1.9": f("ATM", D, 1.9, B, 4, 4600, 2500, "15W40", 4.5, 10000),
    "TD-1.9": f("TURBO", D, 1.9, B, 4, 4100, 2250, "15W40", 4.5, 10000),
    "TD-2.5": f("TURBO", D, 2.5, B, 4, 4100, 2250, "15W40", 5.0, 10000),
    "JTD-1.9": f("TURBO", D, 1.9, B, 4, 4000, 1750, "5W40", 4.5, 20000),
    "JTD-2.4": f("TURBO", D, 2.4, B, 5, 4000, 1750, "5W40", 5.5, 20000),
    "MJ-1.3": f("TURBO", D, 1.3, C, 4, 4000, 1750, "5W30", 3.9, 30000),
    "MJ-1.6": f("TURBO", D, 1.6, B, 4, 3750, 1750, "5W30", 4.4, 30000),
    "MJ-2.0": f("TURBO", D, 2.0, B, 4, 4000, 1750, "5W30", 4.9, 30000),
    "MJ-2.4": f("TURBO", D, 2.4, B, 5, 4000, 2000, "5W30", 5.5, 30000),
    "DV5": f("TURBO", D, 1.5, C, 4, 3750, 1750, "0W30", 3.5, 25000),
    # --- électriques
    "FIAT-500E": electrique(), "e-CMP": electrique(), "SMART-CAR-EV": electrique(),
}

mg = SaisieMoteurs(FAMILLES, "Fiat")
L = []
CL = "Données indicatives (modèle ancien), à vérifier"

# ---------------------------------------------------------------- classiques
mg(L, "500", "110", "1", "1957-07", "1975-08",
   [("Nuova 500 13", "F2-0.5", 26, {"fin": "1960-10"}), ("500 D 18", "F2-0.5", 31, {"debut": "1960-10", "fin": "1965-03"}),
    ("500 F 18", "F2-0.5", 31, {"debut": "1965-03", "fin": "1972-12"}), ("500 L 18", "F2-0.5", 31, {"debut": "1968-09", "fin": "1972-12"}),
    ("500 R 18", "F2-0.6", 37, {"debut": "1972-11"})], portes=2, places=4, reservoir=22, remarques=CL + " ; Giardiniera (break)")
mg(L, "126", "126", "1", "1972-10", "2000-09", [("126 23", "F2-0.6", 40, {"fin": "1977-12"}), ("126 650 24", "F2-0.6", 43, {"debut": "1977-06"})],
   portes=2, places=4, reservoir=21, remarques=CL + " ; produite en Pologne (Polski Fiat) jusqu'en 2000")
mg(L, "127", "127", "1", "1971-04", "1987-12", [("900 45", "F100-0.9", 64), ("1050 50", "F100-1.05", 77, {"debut": "1977-05"})],
   portes=3, places=5, reservoir=30, remarques=CL)
mg(L, "128", "128", "1", "1969-04", "1985-12", [("1100 55", "F128-1.1", 79), ("1300 60", "F128-1.3", 94, {"debut": "1971-01"})],
   portes=4, reservoir=38, remarques=CL + " ; berline, 3 portes, Familiare, Coupé")
mg(L, "131", "131", "1", "1974-10", "1984-12",
   [("1300 65", "F128-1.3", 98), ("1600 TC 96", "FTC-1.6", 127, {"debut": "1978-01"}), ("2000 TC 113", "FTC-2.0", 162, {"debut": "1978-01"}),
    ("2.5 D 72", "D-1.9", 147, {"debut": "1978-01"})], portes=4, reservoir=50, remarques=CL + " ; Mirafiori, Panorama (break)")
mg(L, "Ritmo", "138", "1", "1978-04", "1988-12",
   [("60 1.1 60", "F128-1.1", 83), ("65 1.3 65", "F128-1.3", 100), ("75 1.5 75", "F128-1.5", 118), ("1.7 D 55", "D-1.7", 103, {"debut": "1980-01"})],
   portes=5, reservoir=50, remarques=CL + " ; 3 et 5 portes, Cabrio")
mg(L, "Uno", "146", "1", "1983-01", "1989-08",
   [("45 0.9 45", "F100-0.9", 66), ("55 1.1 55", "F128-1.1", 84), ("70 1.3 68", "F128-1.3", 100), ("Turbo i.e. 105", "F128-1.3T", 147, {"debut": "1985-04"}),
    ("1.7 D 60", "D-1.7", 103)], portes=3, reservoir=42, remarques=CL + " ; 3 et 5 portes")
mg(L, "Uno", "146", "2", "1989-09", "1995-12",
   [("1.0 Fire 45", "FIRE-1.0", 80), ("1.1 i.e. 54", "FIRE-1.1", 86), ("1.4 i.e. 70", "FTC-1.4", 106), ("Turbo i.e. 1.4 116", "F128-1.4T", 161),
    ("1.7 D 60", "D-1.7", 103)], portes=3, reservoir=42, remarques=CL)
mg(L, "Panda", "141", "1", "1980-02", "1986-01", [("30 0.65 30", "F2-0.6", 43), ("45 0.9 45", "F100-0.9", 64)], portes=3, places=4, reservoir=35,
   remarques=CL)
mg(L, "Panda", "141", "2", "1986-01", "2003-09",
   [("750 Fire 34", "FIRE-0.75", 57), ("1000 Fire 45", "FIRE-1.0", 80), ("1100 i.e. 54", "FIRE-1.1", 88, {"debut": "1991-01"}),
    ("4x4 1100 50", "FIRE-1.1", 86, {"debut": "1991-01"}), ("1.3 D 37", "D-1.7", 76, {"fin": "1995-12"})], portes=3, places=4, reservoir=35,
   remarques=CL + " ; 4x4 (1983)")

# ---------------------------------------------------------------- années 90
mg(L, "Cinquecento", "170", "1", "1991-12", "1998-06", [("0.9 41", "F100-0.9", 65), ("Sporting 1.1 54", "FIRE-1.1", 86, {"debut": "1994-03"})],
   portes=3, places=4, reservoir=35)
mg(L, "Seicento", "187", "1", "1998-01", "2010-07", [("0.9 39", "F100-0.9", 65, {"fin": "2001-12"}), ("1.1 54", "FIRE-1.1", 88)], portes=3, places=4,
   reservoir=35)
mg(L, "Tipo", "160", "1", "1988-01", "1995-12",
   [("1.4 i.e. 72", "FTC-1.4", 108), ("1.6 i.e. 90", "FTC-1.6", 128), ("2.0 16V 148", "FTC-2.0", 177, {"debut": "1991-01"}),
    ("1.7 D 58", "D-1.7", 103), ("1.9 TD 92", "TD-1.9", 186)], portes=5, reservoir=55, remarques="3 et 5 portes")
mg(L, "Tempra", "159", "1", "1990-04", "1996-12",
   [("1.6 i.e. 78", "FTC-1.6", 125), ("2.0 i.e. 113", "FTC-2.0", 158), ("1.9 TD 90", "TD-1.9", 186)], portes=4, reservoir=65, remarques="Berline et SW")
mg(L, "Croma", "154", "1", "1985-10", "1996-02",
   [("2.0 i.e. 120", "FTC-2.0", 167), ("2.0 Turbo i.e. 155", "FTC-2.0T", 235), ("2.5 TD 115", "TD-2.5", 220, {"debut": "1991-01"})],
   reservoir=70, remarques="5 portes")
mg(L, "Punto", "176", "1", "1993-09", "1999-08",
   [("55 1.1 54", "FIRE-1.1", 86), ("60 1.2 60", "FIRE-1.2", 102, {"debut": "1997-01"}), ("75 1.2 73", "FIRE-1.2", 106),
    ("GT 1.4 Turbo 133", "F128-1.4T", 191), ("1.7 TD 70", "TD-1.7", 137)], portes=3, reservoir=47, remarques="3 et 5 portes, Cabrio")
mg(L, "Punto", "188", "1", "1999-09", "2003-05",
   [("1.2 60", "FIRE-1.2", 102), ("1.2 16V 80", "FIRE-1.2-16V", 114), ("HGT 1.8 130", "TWINCAM-1.8", 164),
    ("1.9 D 60", "D-1.9", 118), ("1.9 JTD 80", "JTD-1.9", 196, {"debut": "2000-01"})], portes=3, reservoir=47, remarques="3 et 5 portes")
mg(L, "Punto", "188", "2", "2003-06", "2010-12",
   [("1.2 60", "FIRE-1.2", 102), ("1.4 16V 95", "FIRE-1.4-16V", 128), ("1.3 Multijet 70", "MJ-1.3", 180),
    ("1.9 Multijet 100", "JTD-1.9", 200, {"fin": "2005-12"})], portes=3, reservoir=47, remarques="Restylage ; Punto Classic après 2005")
mg(L, "Bravo", "182", "1", "1995-09", "2001-12",
   [("1.4 80", "FIRE-1.4", 112), ("1.6 16V 103", "TWINCAM-1.6", 144), ("1.8 16V 113", "TWINCAM-1.8", 154), ("HGT 2.0 20V 147", "PRATOLA-2.0-20V", 186),
    ("1.9 TD 100", "TD-1.9", 200), ("1.9 JTD 105", "JTD-1.9", 255, {"debut": "1998-09"})], portes=3, reservoir=60, remarques="Bravo 3 portes, Brava 5 portes")
mg(L, "Marea", "185", "1", "1996-09", "2002-12",
   [("1.6 16V 103", "TWINCAM-1.6", 144), ("1.8 16V 113", "TWINCAM-1.8", 154), ("2.0 20V 147", "PRATOLA-2.0-20V", 186),
    ("1.9 JTD 105", "JTD-1.9", 255), ("2.4 JTD 130", "JTD-2.4", 304)], portes=4, reservoir=63, remarques="Berline et Weekend")
mg(L, "Barchetta", "183", "1", "1995-03", "2005-06", [("1.8 16V 130", "TWINCAM-1.8", 164)], portes=2, places=2, reservoir=50, remarques="Roadster")
mg(L, "Coupé", "175", "1", "1993-11", "2000-09",
   [("2.0 16V 139", "FTC-2.0", 180, {"fin": "1996-12"}), ("2.0 16V Turbo 190", "FTC-2.0T", 290, {"fin": "1996-12"}),
    ("1.8 16V 131", "TWINCAM-1.8", 164, {"debut": "1996-09"}), ("2.0 20V 147", "PRATOLA-2.0-20V", 186, {"debut": "1996-09"}),
    ("2.0 20V Turbo 220", "PRATOLA-2.0-20VT", 310, {"debut": "1996-09"})], portes=2, places=4, reservoir=63)
mg(L, "Multipla", "186", "1", "1998-11", "2004-05", [("1.6 16V 103", "TWINCAM-1.6", 145), ("1.9 JTD 105", "JTD-1.9", 203)], places=6, reservoir=63,
   remarques="Monospace 6 places (3+3) ; versions GNV/bipower non reprises")
mg(L, "Multipla", "186", "2", "2004-06", "2010-06", [("1.6 16V 103", "TWINCAM-1.6", 145), ("1.9 Multijet 120", "JTD-1.9", 203)], places=6,
   reservoir=63, remarques="Restylage")

# ---------------------------------------------------------------- années 2000
mg(L, "Stilo", "192", "1", "2001-10", "2007-12",
   [("1.2 16V 80", "FIRE-1.2-16V", 114), ("1.4 16V 95", "FIRE-1.4-16V", 128, {"debut": "2003-10"}), ("1.6 16V 103", "TWINCAM-1.6", 145),
    ("1.8 16V 133", "TWINCAM-1.8", 164), ("Abarth 2.4 20V 170", "PRATOLA-2.4-20V", 221), ("1.9 JTD 80", "JTD-1.9", 196),
    ("1.9 JTD 115", "JTD-1.9", 255), ("1.9 Multijet 120", "JTD-1.9", 280, {"debut": "2005-01"}), ("1.9 Multijet 150", "JTD-1.9", 305, {"debut": "2005-01"})],
   portes=5, reservoir=58, remarques="3 et 5 portes, Multiwagon")
mg(L, "Idea", "350", "1", "2003-11", "2012-12",
   [("1.2 16V 80", "FIRE-1.2-16V", 114, {"fin": "2005-12"}), ("1.4 77", "FIRE-1.4", 115), ("1.4 16V 95", "FIRE-1.4-16V", 128),
    ("1.3 Multijet 70", "MJ-1.3", 180), ("1.3 Multijet 90", "MJ-1.3", 200, {"debut": "2005-01"}), ("1.9 Multijet 100", "JTD-1.9", 200, {"fin": "2008-12"})],
   reservoir=47, remarques="Monospace compact")
mg(L, "Croma", "194", "1", "2005-04", "2011-12",
   [("1.8 16V 140", "GM-2.2", 175), ("2.2 16V 147", "GM-2.2", 203), ("1.9 Multijet 120", "JTD-1.9", 280), ("1.9 Multijet 150", "JTD-1.9", 320),
    ("2.4 Multijet 200", "MJ-2.4", 400)], reservoir=63, remarques="Break haut")
mg(L, "Sedici", "FY", "1", "2006-03", "2014-12",
   [("1.6 16V 107", "SUZ-M16A", 145, {"fin": "2009-12"}), ("1.6 16V 120", "SUZ-M16A", 156, {"debut": "2010-01"}),
    ("1.9 Multijet 120", "JTD-1.9", 280, {"fin": "2009-12"}), ("2.0 Multijet 135", "MJ-2.0", 320, {"debut": "2010-01"})], reservoir=50,
   remarques="Jumeau du Suzuki SX4")
mg(L, "Panda", "169", "1", "2003-09", "2012-01",
   [("1.1 54", "FIRE-1.1", 88), ("1.2 60", "FIRE-1.2", 102, {"fin": "2007-12"}), ("1.2 69", "FIRE-1.2", 102, {"debut": "2008-01"}),
    ("100HP 1.4 16V 100", "FIRE-1.4-16V", 131, {"debut": "2006-09", "fin": "2010-12"}), ("1.3 Multijet 70", "MJ-1.3", 145, {"fin": "2009-12"}),
    ("1.3 Multijet 75", "MJ-1.3", 145, {"debut": "2010-01"})], places=4, reservoir=35, remarques="4x4 et Cross")
mg(L, "Grande Punto", "199", "1", "2005-09", "2009-09",
   [("1.2 65", "FIRE-1.2", 102), ("1.4 77", "FIRE-1.4", 115), ("1.4 16V 95", "FIRE-1.4-16V", 125), ("1.4 T-Jet 120", "TJET-1.4", 206, {"debut": "2007-06"}),
    ("1.3 Multijet 75", "MJ-1.3", 190), ("1.3 Multijet 90", "MJ-1.3", 200), ("1.9 Multijet 130", "JTD-1.9", 280)], portes=3, reservoir=45,
   remarques="3 et 5 portes")
mg(L, "Punto Evo", "199", "2", "2009-10", "2012-08",
   [("1.2 65", "FIRE-1.2", 102), ("1.4 77", "FIRE-1.4", 115), ("1.4 MultiAir 105", "MULTIAIR-1.4", 130), ("1.4 MultiAir Turbo 135", "MULTIAIR-1.4T", 206),
    ("1.3 Multijet 75", "MJ-1.3", 190), ("1.3 Multijet 95", "MJ-1.3", 200), ("1.6 Multijet 120", "MJ-1.6", 300)], portes=3, reservoir=45,
   remarques="3 et 5 portes")
mg(L, "Punto", "199", "3", "2012-09", "2018-08",
   [("1.2 69", "FIRE-1.2", 102), ("0.9 TwinAir 85", "TWINAIR-0.9", 145, {"fin": "2016-12"}), ("1.4 77", "FIRE-1.4", 115),
    ("1.3 Multijet 75", "MJ-1.3", 190), ("1.3 Multijet 95", "MJ-1.3", 200)], portes=3, reservoir=45, remarques="3 et 5 portes")
mg(L, "Bravo", "198", "1", "2007-02", "2014-12",
   [("1.4 90", "FIRE-1.4-16V", 128), ("1.4 T-Jet 120", "TJET-1.4", 206), ("1.4 T-Jet 150", "TJET-1.4", 230),
    ("1.6 Multijet 105", "MJ-1.6", 290, {"debut": "2008-06"}), ("1.6 Multijet 120", "MJ-1.6", 300, {"debut": "2008-06"}),
    ("1.9 Multijet 150", "JTD-1.9", 305, {"fin": "2008-06"}), ("2.0 Multijet 165", "MJ-2.0", 360, {"debut": "2008-06"})], reservoir=58)

# ---------------------------------------------------------------- 500 et dérivés
mg(L, "500", "312", "1", "2007-07", "2015-06",
   [("1.2 69", "FIRE-1.2", 102), ("1.4 16V 100", "FIRE-1.4-16V", 131), ("0.9 TwinAir 85", "TWINAIR-0.9", 145, {"debut": "2010-09"}),
    ("1.3 Multijet 75", "MJ-1.3", 145, {"fin": "2010-12"}), ("1.3 Multijet 95", "MJ-1.3", 200, {"debut": "2010-01"})], portes=3, places=4,
   reservoir=35, remarques="500C cabriolet (2009)")
mg(L, "500", "312", "2", "2015-07", "2019-12",
   [("1.2 69", "FIRE-1.2", 102), ("0.9 TwinAir 85", "TWINAIR-0.9", 145), ("0.9 TwinAir 105", "TWINAIR-0.9", 145),
    ("1.3 Multijet 95", "MJ-1.3", 200, {"fin": "2017-12"})], portes=3, places=4, reservoir=35, remarques="Restylage, 500C")
mg(L, "500", "312", "3", "2020-01", "2024-07", [("1.0 Hybrid 70", "FIREFLY-1.0-HYB", 92)], portes=3, places=4, reservoir=35, remarques="Micro-hybride, 500C")
mg(L, "500", "332", "1", "2025-11", None, [("1.0 Hybrid 65", "FIREFLY-1.0-HYB", 92)], portes=3, places=4, reservoir=38,
   remarques="500 Hybrid (base 500e, Mirafiori) ; 500C et 3+1 (2026)")
mg(L, "500e", "332", "1", "2020-10", None,
   [("500e 95", "FIAT-500E", 220, el(24)), ("500e 118", "FIAT-500E", 220, el(42))], portes=3, places=4, reservoir=0,
   remarques="Électrique : berline, 500C et 3+1")
mg(L, "500L", "330", "1", "2012-09", "2017-06",
   [("1.4 95", "FIRE-1.4-16V", 127), ("0.9 TwinAir 105", "TWINAIR-0.9", 145), ("1.4 T-Jet 120", "TJET-1.4", 206),
    ("1.3 Multijet 85", "MJ-1.3", 200), ("1.6 Multijet 105", "MJ-1.6", 320), ("1.6 Multijet 120", "MJ-1.6", 320)], reservoir=50,
   remarques="Monospace ; 500L Living 7 places (2013)")
mg(L, "500L", "330", "2", "2017-07", "2022-12",
   [("1.4 95", "FIRE-1.4-16V", 127), ("1.3 Multijet 95", "MJ-1.3", 200), ("1.6 Multijet 120", "MJ-1.6", 320)], reservoir=50, remarques="Restylage, Cross")
mg(L, "500X", "334", "1", "2014-11", "2018-08",
   [("1.6 E-Torq 110", "ETORQ-1.6", 152), ("1.4 MultiAir 140", "MULTIAIR-1.4T", 230), ("1.4 MultiAir 170", "MULTIAIR-1.4T", 250),
    ("1.6 Multijet 120", "MJ-1.6", 320), ("2.0 Multijet 140", "MJ-2.0", 350)], reservoir=48, remarques="SUV urbain")
mg(L, "500X", "334", "2", "2018-09", "2024-12",
   [("1.0 FireFly Turbo 120", "FIREFLY-1.0T", 190), ("1.3 FireFly Turbo 150", "FIREFLY-1.3T", 270, {"fin": "2022-06"}),
    ("1.6 Multijet 130", "MJ-1.6", 320), ("1.5 Hybrid 130", "FIREFLY-1.5-HYB", 240, {"debut": "2022-07"})], reservoir=48, remarques="Restylage")
mg(L, "124 Spider", "348", "1", "2016-06", "2019-12", [("1.4 MultiAir Turbo 140", "MULTIAIR-1.4T", 240)], portes=2, places=2, reservoir=45,
   remarques="Roadster (base Mazda MX-5)")

# ---------------------------------------------------------------- gamme actuelle
mg(L, "Tipo", "356", "1", "2015-10", "2020-10",
   [("1.4 95", "FIRE-1.4-16V", 127), ("1.4 T-Jet 120", "TJET-1.4", 215), ("1.6 E-Torq 110", "ETORQ-1.6", 152),
    ("1.3 Multijet 95", "MJ-1.3", 200), ("1.6 Multijet 120", "MJ-1.6", 320)], portes=4, reservoir=50, remarques="Berline, 5 portes et SW")
mg(L, "Tipo", "356", "2", "2020-11", "2025-12",
   [("1.0 FireFly Turbo 100", "FIREFLY-1.0T", 190), ("1.6 Multijet 130", "MJ-1.6", 320), ("1.5 Hybrid 130", "FIREFLY-1.5-HYB", 240, {"debut": "2022-06"})],
   reservoir=50, remarques="Restylage, Cross ; fin de commercialisation à vérifier")
mg(L, "Panda", "319", "1", "2012-02", "2023-12",
   [("1.2 69", "FIRE-1.2", 102, {"fin": "2020-12"}), ("0.9 TwinAir 85", "TWINAIR-0.9", 145, {"fin": "2019-12"}),
    ("1.3 Multijet 75", "MJ-1.3", 190, {"fin": "2014-12"}), ("1.3 Multijet 95", "MJ-1.3", 200, {"debut": "2015-01", "fin": "2019-12"}),
    ("1.0 Hybrid 70", "FIREFLY-1.0-HYB", 92, {"debut": "2020-01"})], reservoir=37, remarques="4x4, Cross ; versions GPL/GNV non reprises")
mg(L, "Panda", "319", "2", "2024-01", None, [("Pandina 1.0 Hybrid 70", "FIREFLY-1.0-HYB", 92)], reservoir=37, remarques="Pandina (restylage)")
mg(L, "Grande Panda", "Smart Car", "1", "2025-01", None,
   [("1.2 Hybrid 110", "EB2-MHEV", 205), ("Électrique 113", "SMART-CAR-EV", 125, el(44)), ("1.2 Turbo 100", "EB2", 205, {"debut": "2026-01"})],
   reservoir=44, remarques="Plateforme Smart Car (Stellantis) ; dérivés SUV (Grizzly) annoncés")
mg(L, "600", "STLA-S", "1", "2023-07", None,
   [("600e 156", "e-CMP", 260, el(54)), ("1.2 Hybrid 100", "EB2-MHEV", 205, {"debut": "2024-01", "fin": "2025-06"}),
    ("1.2 Hybrid 110", "EB2-MHEV", 205, {"debut": "2025-07"}), ("1.2 Hybrid 145", "EB2-MHEV", 230, {"debut": "2025-01"}),
    ("1.2 Turbo 100", "EB2", 205, {"debut": "2026-03"})], reservoir=44, remarques="SUV urbain (base e-CMP)")

# ---------------------------------------------------------------- ludospaces / divers
mg(L, "Doblò", "119", "1", "2001-01", "2009-12", [("1.2 65", "FIRE-1.2", 102), ("1.9 JTD 100", "JTD-1.9", 200), ("1.3 Multijet 85", "MJ-1.3", 200, {"debut": "2005-06"})],
   reservoir=60, remarques="Version voiture (Panorama) ; utilitaire Cargo non repris")
mg(L, "Doblò", "263", "1", "2010-01", "2022-06",
   [("1.4 95", "FIRE-1.4", 127), ("1.6 Multijet 105", "MJ-1.6", 290), ("2.0 Multijet 135", "MJ-2.0", 320)], places=7, reservoir=60,
   remarques="5 ou 7 places")
mg(L, "Doblò", "K9", "1", "2022-07", None,
   [("1.2 PureTech 110", "EB2", 205), ("1.5 BlueHDi 100", "DV5", 250), ("1.5 BlueHDi 130", "DV5", 300), ("e-Doblò 136", "e-CMP", 260, el(50))],
   places=7, reservoir=50, remarques="Base Citroën Berlingo")
mg(L, "Qubo", "225", "1", "2008-01", "2021-12", [("1.4 73", "FIRE-1.4", 118), ("1.3 Multijet 75", "MJ-1.3", 190), ("1.3 Multijet 95", "MJ-1.3", 200)],
   reservoir=45, remarques="Ludospace (Fiorino voiture)")
mg(L, "Freemont", "JC", "1", "2011-06", "2016-12",
   [("2.0 Multijet 140", "MJ-2.0", 350), ("2.0 Multijet 170", "MJ-2.0", 350), ("3.6 V6 280", "PENTASTAR-3.6", 342, {"debut": "2012-01"})],
   places=7, reservoir=78, remarques="SUV 7 places (base Dodge Journey)")

MOT = Motorisations("Fiat", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Fiat": L}
MOTEURS = MOT.moteurs()
