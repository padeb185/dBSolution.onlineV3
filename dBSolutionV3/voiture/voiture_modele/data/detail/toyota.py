"""Toyota et Toyota GR : générations, phases, motorisations (marché européen) et moteurs liés.
Citadines (Aygo, iQ, Yaris), compactes (Corolla, Auris, C-HR), familiales (Carina E, Avensis, Verso, Prius, Camry),
SUV et 4x4 (RAV4, Land Cruiser, Hilux, Highlander, bZ4X, C-HR+, Urban Cruiser), sportives (Celica, MR2, Supra, GT86)
et GR (GR Yaris, GR86) ; toutes les Supra (A40 à A90) dans Toyota. Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ;
la puissance est le dernier nombre du nom. Utilitaires (Proace) non couverts ; données anciennes indicatives."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

E_, D = "ESS", "DSL"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


C, B = "CHAINE", "COURROIE"
FAMILLES = {
    # --- essence 3 et 4 cylindres
    "1KR-FE": f("ATM", E_, 1.0, C, 3, 6000, 4800, "0W20", 3.2, 15000),
    "1SZ-FE": f("ATM", E_, 1.0, C, 4, 6000, 4100, "5W30", 3.4, 15000),
    "2SZ-FE": f("ATM", E_, 1.3, C, 4, 6000, 4200, "5W30", 3.7, 15000),
    "2NZ-FE": f("ATM", E_, 1.3, C, 4, 6000, 4400, "5W30", 3.7, 15000),
    "1NZ-FE": f("ATM", E_, 1.5, C, 4, 6000, 4200, "5W30", 3.7, 15000),
    "1NR-FE": f("ATM", E_, 1.33, C, 4, 6000, 3800, "0W20", 3.4, 15000),
    "2NR-FKE": f("ATM", E_, 1.5, C, 4, 6000, 4400, "0W20", 3.4, 15000),
    "8NR-FTS": f("TURBO", E_, 1.2, C, 4, 5200, 1500, "0W20", 4.2, 15000),
    "M15A-FKS": f("ATM", E_, 1.5, C, 3, 6600, 4800, "0W16", 3.6, 15000),
    "4E-FE": f("ATM", E_, 1.3, B, 4, 5400, 4400, "10W40", 3.2, 15000),
    "4A-FE": f("ATM", E_, 1.6, B, 4, 6000, 4800, "10W40", 3.3, 15000),
    "4A-GE": f("ATM", E_, 1.6, B, 4, 6600, 5000, "10W40", 3.5, 10000),
    "7A-FE": f("ATM", E_, 1.8, B, 4, 5600, 2800, "10W40", 3.4, 15000),
    "3S-FE": f("ATM", E_, 2.0, B, 4, 5600, 4400, "10W40", 3.9, 15000),
    "3S-GE": f("ATM", E_, 2.0, B, 4, 7000, 4800, "10W40", 4.1, 15000),
    "3S-GTE": f("TURBO", E_, 2.0, B, 4, 6000, 4000, "10W40", 4.2, 10000),
    "4ZZ-FE": f("ATM", E_, 1.4, C, 4, 6000, 4400, "5W30", 3.7, 15000),
    "3ZZ-FE": f("ATM", E_, 1.6, C, 4, 6000, 3800, "5W30", 3.7, 15000),
    "1ZZ-FE": f("ATM", E_, 1.8, C, 4, 6000, 4200, "5W30", 3.7, 15000),
    "2ZZ-GE": f("ATM", E_, 1.8, C, 4, 7800, 6800, "5W30", 4.2, 15000),
    "1ZR-FAE": f("ATM", E_, 1.6, C, 4, 6400, 4400, "0W20", 4.2, 15000),
    "2ZR-FE": f("ATM", E_, 1.8, C, 4, 6000, 4400, "0W20", 4.2, 15000),
    "2ZR-FAE": f("ATM", E_, 1.8, C, 4, 6400, 4400, "0W20", 4.2, 15000),
    "2ZR-FE-SC": f("TURBO", E_, 1.8, C, 4, 6800, 5000, "0W20", 4.2, 15000),
    "3ZR-FAE": f("ATM", E_, 2.0, C, 4, 6200, 4400, "0W20", 4.2, 15000),
    "1AZ-FE": f("ATM", E_, 2.0, C, 4, 6000, 4000, "5W30", 4.2, 15000),
    "2AZ-FE": f("ATM", E_, 2.4, C, 4, 6000, 4000, "5W30", 4.2, 15000),
    "2TZ-FE": f("ATM", E_, 2.4, B, 4, 5000, 4000, "10W40", 4.3, 15000),
    "G16E-GTS": f("TURBO", E_, 1.6, C, 3, 6500, 3000, "0W20", 4.5, 15000),
    "FA20": f("ATM", E_, 2.0, C, 4, 7000, 6400, "0W20", 5.4, 15000, a="PLAT"),
    "FA24": f("ATM", E_, 2.4, C, 4, 7000, 3700, "0W20", 5.0, 15000, a="PLAT"),
    # --- hybrides
    "1NZ-FXE": f("HYB_E", E_, 1.5, C, 4, 4800, 3600, "0W20", 3.7, 15000),
    "2ZR-FXE": f("HYB_E", E_, 1.8, C, 4, 5200, 3600, "0W20", 4.2, 15000),
    "M15A-FXE": f("HYB_E", E_, 1.5, C, 3, 5500, 3600, "0W16", 3.6, 15000),
    "M20A-FXS": f("HYB_E", E_, 2.0, C, 4, 6000, 4400, "0W16", 4.5, 15000),
    "M20A-PHEV": f("HYB_E", E_, 2.0, C, 4, 6000, 4400, "0W16", 4.5, 15000),
    "2AR-FXE": f("HYB_E", E_, 2.5, C, 4, 5700, 4500, "0W20", 4.4, 15000),
    "A25A-FXS": f("HYB_E", E_, 2.5, C, 4, 5700, 3600, "0W16", 4.5, 15000),
    "A25A-PHEV": f("HYB_E", E_, 2.5, C, 4, 6000, 3600, "0W16", 4.5, 15000),
    # --- 6 et 8 cylindres essence
    "7M-GE": f("ATM", E_, 3.0, B, 6, 6000, 4800, "10W40", 4.9, 10000),
    "7M-GTE": f("TURBO", E_, 3.0, B, 6, 5600, 3200, "10W40", 4.9, 10000),
    "4M-E": f("ATM", E_, 2.6, B, 6, 5000, 4000, "10W40", 4.9, 10000),
    "5M-GE": f("ATM", E_, 2.8, B, 6, 5600, 4400, "10W40", 4.9, 10000),
    "2JZ-GTE": f("TURBO", E_, 3.0, B, 6, 5600, 4000, "10W40", 5.5, 10000),
    "5VZ-FE": f("ATM", E_, 3.4, B, 6, 4800, 3600, "10W40", 5.2, 15000, a="V"),
    "1GR-FE": f("ATM", E_, 4.0, C, 6, 5600, 4400, "5W30", 5.7, 15000, a="V"),
    "2UZ-FE": f("ATM", E_, 4.7, B, 8, 4800, 3400, "5W30", 6.4, 15000, a="V"),
    "2F": f("ATM", E_, 4.2, "NC", 6, 3600, 1800, "15W40", 7.6, 5000),
    "1FZ-FE": f("ATM", E_, 4.5, C, 6, 4600, 3200, "10W40", 7.6, 10000),
    "B48": f("TURBO", E_, 2.0, C, 4, 5000, 1550, "0W20", 5.25, 15000),
    "B58": f("TURBO", E_, 3.0, C, 6, 5800, 1600, "0W20", 6.5, 15000),
    # --- diesel
    "2C": f("ATM", D, 2.0, B, 4, 4700, 3000, "15W40", 4.5, 10000),
    "2C-T": f("TURBO", D, 2.0, B, 4, 4000, 2200, "15W40", 4.5, 10000),
    "1WZ": f("TURBO", D, 1.9, B, 4, 4600, 2500, "5W40", 4.3, 15000),
    "DV4": f("TURBO", D, 1.4, B, 4, 4000, 1750, "5W40", 3.75, 15000),
    "1ND-TV": f("TURBO", D, 1.4, C, 4, 3800, 1800, "5W30", 4.2, 15000),
    "1WW": f("TURBO", D, 1.6, C, 4, 4000, 1750, "0W30", 5.2, 15000),
    "2WW": f("TURBO", D, 2.0, C, 4, 4000, 1750, "0W30", 5.2, 15000),
    "1CD-FTV": f("TURBO", D, 2.0, B, 4, 3600, 1800, "5W30", 6.3, 15000),
    "1AD-FTV": f("TURBO", D, 2.0, C, 4, 3600, 1800, "5W30", 5.9, 15000),
    "2AD-FTV": f("TURBO", D, 2.2, C, 4, 3600, 2000, "5W30", 5.9, 15000),
    "2AD-FHV": f("TURBO", D, 2.2, C, 4, 3600, 2000, "5W30", 5.9, 15000),
    "2L": f("ATM", D, 2.4, B, 4, 4200, 2400, "15W40", 5.5, 10000),
    "2KD-FTV": f("TURBO", D, 2.5, B, 4, 3600, 1600, "5W30", 6.9, 10000),
    "1KD-FTV": f("TURBO", D, 3.0, B, 4, 3400, 1600, "5W30", 6.9, 10000),
    "1KZ-TE": f("TURBO", D, 3.0, B, 4, 3600, 2000, "15W40", 6.4, 10000),
    "2GD-FTV": f("TURBO", D, 2.4, C, 4, 3400, 1600, "0W30", 7.5, 15000),
    "1GD-FTV": f("TURBO", D, 2.8, C, 4, 3400, 1600, "0W30", 7.5, 15000),
    "1GD-MHEV": f("TURBO", D, 2.8, C, 4, 3400, 1600, "0W30", 7.5, 15000),
    "3B": f("ATM", D, 3.4, "NC", 4, 3500, 2200, "15W40", 6.5, 5000),
    "2H": f("ATM", D, 4.0, "NC", 6, 3500, 2000, "15W40", 7.5, 5000),
    "12H-T": f("TURBO", D, 4.0, "NC", 6, 3500, 1800, "15W40", 7.5, 5000),
    "1HD-T": f("TURBO", D, 4.2, "NC", 6, 3600, 1800, "15W40", 8.0, 10000),
    "1HD-FTE": f("TURBO", D, 4.2, "NC", 6, 3400, 1200, "15W40", 8.0, 10000),
    "1VD-FTV": f("TURBO", D, 4.5, C, 8, 3600, 1600, "5W30", 9.0, 10000, a="V"),
    # --- électriques et hydrogène
    "eTNGA-EV": electrique(), "Suzuki-EV": electrique(), "Hilux-EV": electrique(),
    "FCEV": f("ELEC", "H2", 0.0, "AUCUNE", 0, 0, 0, "CHOISIR", 0.0, 15000, a="SANS"),
}

mg = SaisieMoteurs(FAMILLES, "Toyota")
L = []   # Toyota
LG = []  # Toyota GR

# ---------------------------------------------------------------- Aygo / iQ
mg(L, "Aygo", "AB10", "1", "2005-07", "2008-12", [("1.0 VVT-i 68", "1KR-FE", 93), ("1.4 D-4D 54", "DV4", 130)],
   portes=5, places=4, reservoir=35, remarques="3 et 5 portes (jumelle C1 / 107)")
mg(L, "Aygo", "AB10", "2", "2009-01", "2014-05", [("1.0 VVT-i 68", "1KR-FE", 93, {"fin": "2012-03"}),
   ("1.0 VVT-i 69", "1KR-FE", 95, {"debut": "2012-04"})], portes=5, places=4, reservoir=35,
   remarques="Restylages 2009 et 2012")
mg(L, "Aygo", "AB40", "1", "2014-06", "2018-06", [("1.0 VVT-i 69", "1KR-FE", 95)], portes=5, places=4, reservoir=35)
mg(L, "Aygo", "AB40", "2", "2018-07", "2022-03", [("1.0 VVT-i 72", "1KR-FE", 93)], portes=5, places=4, reservoir=35)
mg(L, "Aygo X", "AB70", "1", "2022-01", "2025-12", [("1.0 VVT-i 72", "1KR-FE", 93)], portes=5, places=4, reservoir=35,
   remarques="Crossover urbain")
mg(L, "Aygo X", "AB70", "2", "2026-01", None, [("1.5 Hybrid 116", "M15A-FXE", 141)], portes=5, places=4, reservoir=36,
   remarques="Restylage : full hybride (moteur de la Yaris)")
mg(L, "iQ", "AJ10", "1", "2009-01", "2015-12",
   [("1.0 VVT-i 68", "1KR-FE", 93), ("1.33 Dual VVT-i 98", "1NR-FE", 123, {"debut": "2009-07"}),
    ("1.4 D-4D 90", "1ND-TV", 190, {"fin": "2011-12"})], portes=3, places=4, reservoir=32, remarques="Micro-citadine 3+1")

# ---------------------------------------------------------------- Yaris / Yaris Cross / Urban Cruiser
mg(L, "Yaris", "XP10", "1", "1999-04", "2003-02",
   [("1.0 VVT-i 68", "1SZ-FE", 90), ("1.3 VVT-i 86", "2NZ-FE", 123, {"debut": "1999-10"}),
    ("1.5 T-Sport 106", "1NZ-FE", 144, {"debut": "2001-09"})], reservoir=45, remarques="3 et 5 portes ; Yaris Verso (1999-2005)")
mg(L, "Yaris", "XP10", "2", "2003-03", "2005-08",
   [("1.0 VVT-i 65", "1SZ-FE", 90), ("1.3 VVT-i 87", "2NZ-FE", 123), ("1.5 T-Sport 106", "1NZ-FE", 144),
    ("1.4 D-4D 75", "1ND-TV", 180)], reservoir=45, remarques="3 et 5 portes")
mg(L, "Yaris", "XP90", "1", "2005-09", "2008-12",
   [("1.0 VVT-i 69", "1KR-FE", 95), ("1.3 VVT-i 87", "2SZ-FE", 121), ("1.4 D-4D 90", "1ND-TV", 190),
    ("1.8 TS 133", "2ZR-FE", 173, {"debut": "2007-03"})], reservoir=42, remarques="3 et 5 portes")
mg(L, "Yaris", "XP90", "2", "2009-01", "2011-08",
   [("1.0 VVT-i 69", "1KR-FE", 95), ("1.33 Dual VVT-i 101", "1NR-FE", 132), ("1.4 D-4D 90", "1ND-TV", 190),
    ("1.8 TS 133", "2ZR-FE", 173)], reservoir=42, remarques="3 et 5 portes")
mg(L, "Yaris", "XP130", "1", "2011-09", "2014-07",
   [("1.0 VVT-i 69", "1KR-FE", 95), ("1.33 Dual VVT-i 99", "1NR-FE", 125), ("1.4 D-4D 90", "1ND-TV", 190),
    ("1.5 Hybrid 100", "1NZ-FXE", 111, {"debut": "2012-06"})], reservoir=42, remarques="3 et 5 portes")
mg(L, "Yaris", "XP130", "2", "2014-08", "2017-03",
   [("1.0 VVT-i 69", "1KR-FE", 95), ("1.33 Dual VVT-i 99", "1NR-FE", 125), ("1.4 D-4D 90", "1ND-TV", 190),
    ("1.5 Hybrid 100", "1NZ-FXE", 111)], reservoir=42, remarques="3 et 5 portes")
mg(L, "Yaris", "XP130", "3", "2017-04", "2020-06",
   [("1.0 VVT-i 72", "1KR-FE", 93), ("1.5 Dual VVT-iE 111", "2NR-FKE", 136), ("1.5 Hybrid 100", "1NZ-FXE", 111),
    ("GRMN 212", "2ZR-FE-SC", 250, {"debut": "2018-03", "fin": "2018-12"})], reservoir=42,
   remarques="3 et 5 portes ; GRMN à compresseur (400 ex.)")
mg(L, "Yaris", "XP210", "1", "2020-07", "2024-03",
   [("1.0 VVT-i 72", "1KR-FE", 93), ("1.5 VVT-iE 125", "M15A-FKS", 153), ("1.5 Hybrid 116", "M15A-FXE", 141)],
   reservoir=40, remarques="5 portes (TNGA-B)")
mg(L, "Yaris", "XP210", "2", "2024-04", None,
   [("1.5 Hybrid 116", "M15A-FXE", 141), ("1.5 Hybrid 130", "M15A-FXE", 185)], reservoir=36, remarques="Restylage")
mg(L, "Yaris Cross", "XP210", "1", "2021-08", "2024-03",
   [("1.5 Hybrid 116", "M15A-FXE", 141), ("1.5 Hybrid AWD-i 116", "M15A-FXE", 141), ("1.5 VVT-iE 125", "M15A-FKS", 153)],
   reservoir=36, remarques="SUV urbain")
mg(L, "Yaris Cross", "XP210", "2", "2024-04", None,
   [("1.5 Hybrid 116", "M15A-FXE", 141), ("1.5 Hybrid 130", "M15A-FXE", 185), ("1.5 Hybrid AWD-i 116", "M15A-FXE", 141)],
   reservoir=36, remarques="SUV urbain restylé")
mg(L, "Urban Cruiser", "XP110", "1", "2009-03", "2014-12",
   [("1.33 Dual VVT-i 101", "1NR-FE", 132), ("1.4 D-4D AWD 90", "1ND-TV", 190)], reservoir=42, remarques="Mini-SUV")
mg(L, "Urban Cruiser", "eVitara", "1", "2025-11", None,
   [("Urban Cruiser 144", "Suzuki-EV", 189, el(49)), ("Urban Cruiser 174", "Suzuki-EV", 193, el(61)),
    ("Urban Cruiser AWD 184", "Suzuki-EV", 307, el(61))], reservoir=0,
   remarques="SUV urbain électrique (jumeau du Suzuki e Vitara)")

# ---------------------------------------------------------------- Corolla / Auris
mg(L, "Corolla", "E100", "1", "1992-05", "1997-04",
   [("1.3 XLi 75", "4E-FE", 110), ("1.6 GLi 114", "4A-FE", 145), ("1.6 GTi 16v 114", "4A-FE", 145),
    ("2.0 D 72", "2C", 131)], reservoir=50, remarques="Berline, Liftback, 3 et 5 portes, Break")
mg(L, "Corolla", "E110", "1", "1997-05", "2001-12",
   [("1.3 86", "4E-FE", 117, {"fin": "1999-12"}), ("1.6 G6 110", "4A-FE", 145, {"fin": "1999-12"}),
    ("1.4 VVT-i 97", "4ZZ-FE", 130, {"debut": "2000-01"}), ("1.6 VVT-i 110", "3ZZ-FE", 150, {"debut": "2000-01"}),
    ("1.9 D 69", "1WZ", 120, {"fin": "1999-12"}), ("2.0 D-4D 90", "1CD-FTV", 215, {"debut": "2000-01"})],
   reservoir=50, remarques="Berline, Liftback, 3 et 5 portes, Break")
mg(L, "Corolla", "E120", "1", "2002-01", "2004-05",
   [("1.4 VVT-i 97", "4ZZ-FE", 130), ("1.6 VVT-i 110", "3ZZ-FE", 150), ("1.8 TS 192", "2ZZ-GE", 180),
    ("2.0 D-4D 90", "1CD-FTV", 215), ("2.0 D-4D 116", "1CD-FTV", 280, {"debut": "2002-09"})], reservoir=55,
   remarques="Berline, 3 et 5 portes, Break ; Corolla Verso")
mg(L, "Corolla", "E120", "2", "2004-06", "2007-01",
   [("1.4 VVT-i 97", "4ZZ-FE", 130), ("1.6 VVT-i 110", "3ZZ-FE", 150), ("1.4 D-4D 90", "1ND-TV", 190),
    ("2.0 D-4D 116", "1CD-FTV", 280)], reservoir=55, remarques="Berline, 3 et 5 portes, Break")
mg(L, "Corolla", "E150", "1", "2007-02", "2013-08",
   [("1.33 Dual VVT-i 101", "1NR-FE", 132, {"debut": "2009-04"}), ("1.6 Dual VVT-i 132", "1ZR-FAE", 160),
    ("1.4 D-4D 90", "1ND-TV", 190), ("2.0 D-4D 126", "1AD-FTV", 300)], portes=4, reservoir=55, remarques="Berline")
mg(L, "Corolla", "E170", "1", "2013-09", "2018-12",
   [("1.33 Dual VVT-i 99", "1NR-FE", 125), ("1.6 Valvematic 132", "1ZR-FAE", 160), ("1.4 D-4D 90", "1ND-TV", 190)],
   portes=4, reservoir=55, remarques="Berline")
mg(L, "Corolla", "E210", "1", "2019-01", "2022-12",
   [("1.2 T 116", "8NR-FTS", 185, {"fin": "2020-12"}), ("1.8 Hybrid 122", "2ZR-FXE", 142), ("2.0 Hybrid 180", "M20A-FXS", 190)],
   reservoir=43, remarques="5 portes, Touring Sports, berline")
mg(L, "Corolla", "E210", "2", "2023-01", None,
   [("1.8 Hybrid 140", "2ZR-FXE", 142), ("2.0 Hybrid 196", "M20A-FXS", 190)], reservoir=43,
   remarques="5 portes, Touring Sports, berline (5e génération hybride)")
mg(L, "Corolla Cross", "XG10", "1", "2022-10", None,
   [("2.0 Hybrid 197", "M20A-FXS", 190), ("2.0 Hybrid AWD-i 197", "M20A-FXS", 190)], reservoir=36, remarques="SUV compact")
mg(L, "Auris", "E150", "1", "2007-02", "2010-03",
   [("1.33 Dual VVT-i 101", "1NR-FE", 132, {"debut": "2009-04"}), ("1.4 VVT-i 97", "4ZZ-FE", 130),
    ("1.6 VVT-i 124", "1ZR-FAE", 157), ("1.6 Valvematic 132", "1ZR-FAE", 160, {"debut": "2009-04"}),
    ("1.4 D-4D 90", "1ND-TV", 190), ("2.0 D-4D 126", "1AD-FTV", 300), ("2.2 D-CAT 177", "2AD-FHV", 400)], reservoir=55,
   remarques="3 et 5 portes")
mg(L, "Auris", "E150", "2", "2010-04", "2012-10",
   [("1.33 Dual VVT-i 99", "1NR-FE", 125), ("1.6 Valvematic 132", "1ZR-FAE", 160), ("1.8 HSD 136", "2ZR-FXE", 142),
    ("1.4 D-4D 90", "1ND-TV", 190), ("2.0 D-4D 126", "1AD-FTV", 300)], reservoir=55, remarques="3 et 5 portes ; hybride HSD")
mg(L, "Auris", "E180", "1", "2012-11", "2015-06",
   [("1.33 Dual VVT-i 99", "1NR-FE", 125), ("1.6 Valvematic 132", "1ZR-FAE", 160), ("1.8 Hybrid 136", "2ZR-FXE", 142),
    ("1.4 D-4D 90", "1ND-TV", 190), ("2.0 D-4D 124", "1AD-FTV", 300)], reservoir=50, remarques="5 portes, Touring Sports (2013)")
mg(L, "Auris", "E180", "2", "2015-07", "2018-12",
   [("1.2 T 116", "8NR-FTS", 185), ("1.33 Dual VVT-i 99", "1NR-FE", 125), ("1.8 Hybrid 136", "2ZR-FXE", 142),
    ("1.4 D-4D 90", "1ND-TV", 190), ("1.6 D-4D 112", "1WW", 270)], reservoir=50, remarques="5 portes, Touring Sports")

# ---------------------------------------------------------------- C-HR / C-HR+
mg(L, "C-HR", "AX10", "1", "2016-12", "2019-09",
   [("1.2 T 116", "8NR-FTS", 185), ("1.8 Hybrid 122", "2ZR-FXE", 142)], reservoir=43, remarques="SUV coupé")
mg(L, "C-HR", "AX10", "2", "2019-10", "2023-09",
   [("1.8 Hybrid 122", "2ZR-FXE", 142), ("2.0 Hybrid 184", "M20A-FXS", 190)], reservoir=43, remarques="SUV coupé restylé")
mg(L, "C-HR", "AX20", "1", "2023-10", None,
   [("1.8 Hybrid 140", "2ZR-FXE", 142), ("2.0 Hybrid 197", "M20A-FXS", 190), ("2.0 Hybrid AWD-i 197", "M20A-FXS", 190),
    ("2.0 Plug-in Hybrid 223", "M20A-PHEV", 208, ph(14, 43, debut="2024-03"))], reservoir=43, remarques="SUV coupé")
mg(L, "C-HR+", "C-HR+", "1", "2026-01", None,
   [("C-HR+ 167", "eTNGA-EV", 268, el(58)), ("C-HR+ 224", "eTNGA-EV", 268, el(77)),
    ("C-HR+ AWD 343", "eTNGA-EV", 338, el(77))], reservoir=0, remarques="SUV compact électrique (e-TNGA)")

# ---------------------------------------------------------------- Prius / familiales
mg(L, "Prius", "NHW11", "1", "2000-09", "2003-12", [("1.5 Hybrid 72", "1NZ-FXE", 115)], portes=4, reservoir=50,
   remarques="1re génération en Europe (berline) ; puissance thermique")
mg(L, "Prius", "NHW20", "1", "2004-01", "2009-05", [("1.5 Hybrid 110", "1NZ-FXE", 115)], reservoir=45, remarques="Liftback")
mg(L, "Prius", "ZVW30", "1", "2009-06", "2015-12",
   [("1.8 Hybrid 136", "2ZR-FXE", 142), ("1.8 Plug-in 136", "2ZR-FXE", 142, ph(4, 45, debut="2012-06"))], reservoir=45,
   remarques="Liftback ; Prius Plug-in (ZVW35)")
mg(L, "Prius", "ZVW50", "1", "2016-01", "2022-12",
   [("1.8 Hybrid 122", "2ZR-FXE", 142), ("1.8 Plug-in 122", "2ZR-FXE", 142, ph(9, 43, debut="2017-03")),
    ("1.8 Hybrid AWD-i 122", "2ZR-FXE", 142, {"debut": "2019-03"})], reservoir=43, remarques="Liftback ; Prius Plug-in")
mg(L, "Prius", "XW60", "1", "2023-06", None, [("2.0 Plug-in Hybrid 223", "M20A-PHEV", 208, ph(14, 40))], reservoir=40,
   remarques="Uniquement hybride rechargeable en Europe")
mg(L, "Prius+", "ZVW40", "1", "2012-06", "2021-06", [("1.8 Hybrid 136", "2ZR-FXE", 142)], places=7, reservoir=45,
   remarques="Monospace 7 places")
mg(L, "Carina E", "T190", "1", "1992-04", "1997-09",
   [("1.6 XLi 107", "4A-FE", 145), ("2.0 GLi 133", "3S-FE", 178), ("2.0 GTi 175", "3S-GE", 186), ("2.0 D 73", "2C", 132),
    ("2.0 TD 83", "2C-T", 170, {"debut": "1996-01"})], portes=4, reservoir=60, remarques="Berline, Liftback, Break")
mg(L, "Avensis", "T220", "1", "1997-09", "2003-01",
   [("1.6 VVT-i 110", "3ZZ-FE", 150), ("1.8 VVT-i 129", "1ZZ-FE", 170), ("2.0 VVT-i 150", "1AZ-FE", 200, {"debut": "2000-09"}),
    ("2.0 TD 90", "2C-T", 205, {"fin": "1999-12"}), ("2.0 D-4D 110", "1CD-FTV", 250, {"debut": "2000-01"})], portes=4,
   reservoir=60, remarques="Berline, Liftback, Break ; Avensis Verso (2001)")
mg(L, "Avensis", "T250", "1", "2003-01", "2008-10",
   [("1.6 VVT-i 110", "3ZZ-FE", 150), ("1.8 VVT-i 129", "1ZZ-FE", 170), ("2.0 VVT-i 147", "1AZ-FE", 196),
    ("2.4 VVT-i 163", "2AZ-FE", 224), ("2.0 D-4D 116", "1CD-FTV", 280), ("2.0 D-4D 126", "1AD-FTV", 300, {"debut": "2006-06"}),
    ("2.2 D-4D 150", "2AD-FTV", 340, {"debut": "2005-09"}), ("2.2 D-CAT 177", "2AD-FHV", 400, {"debut": "2005-09"})],
   portes=4, reservoir=60, remarques="Berline, Liftback, Break")
mg(L, "Avensis", "T270", "1", "2009-01", "2015-06",
   [("1.6 Valvematic 132", "1ZR-FAE", 160), ("1.8 Valvematic 147", "2ZR-FAE", 180), ("2.0 Valvematic 152", "3ZR-FAE", 196),
    ("2.0 D-4D 126", "1AD-FTV", 300), ("2.2 D-4D 150", "2AD-FTV", 340), ("2.2 D-CAT 177", "2AD-FHV", 400)], portes=4,
   reservoir=60, remarques="Berline et Touring Sports ; restylage 2012 non détaillé")
mg(L, "Avensis", "T270", "2", "2015-07", "2018-09",
   [("1.6 Valvematic 132", "1ZR-FAE", 160), ("1.8 Valvematic 147", "2ZR-FAE", 180), ("1.6 D-4D 112", "1WW", 270),
    ("2.0 D-4D 143", "2WW", 320)], portes=4, reservoir=60, remarques="Berline et Touring Sports")
mg(L, "Corolla Verso", "AR10", "1", "2004-04", "2009-03",
   [("1.6 VVT-i 110", "3ZZ-FE", 150), ("1.8 VVT-i 129", "1ZZ-FE", 170), ("2.0 D-4D 116", "1CD-FTV", 280),
    ("2.2 D-4D 136", "2AD-FTV", 310, {"debut": "2005-09"}), ("2.2 D-CAT 177", "2AD-FHV", 400, {"debut": "2006-01"})],
   places=7, reservoir=60, remarques="Monospace 7 places")
mg(L, "Verso", "R20", "1", "2009-04", "2018-09",
   [("1.6 Valvematic 132", "1ZR-FAE", 160), ("1.8 Valvematic 147", "2ZR-FAE", 180), ("2.0 D-4D 126", "1AD-FTV", 300, {"fin": "2014-02"}),
    ("2.2 D-4D 150", "2AD-FTV", 340, {"fin": "2014-02"}), ("2.2 D-CAT 177", "2AD-FHV", 400, {"fin": "2012-12"}),
    ("1.6 D-4D 112", "1WW", 270, {"debut": "2014-03"})], places=7, reservoir=60, remarques="Monospace 5 ou 7 places ; restylage 2013")
mg(L, "Verso-S", "P120", "1", "2011-01", "2015-12",
   [("1.33 Dual VVT-i 99", "1NR-FE", 125), ("1.4 D-4D 90", "1ND-TV", 190)], reservoir=42, remarques="Mini-monospace")
mg(L, "Previa", "XR10", "1", "1990-06", "2000-06", [("2.4 132", "2TZ-FE", 204)], places=7, reservoir=75,
   remarques="Monospace à moteur central couché")
mg(L, "Previa", "XR30", "1", "2000-07", "2006-06",
   [("2.4 VVT-i 156", "2AZ-FE", 224), ("2.0 D-4D 116", "1CD-FTV", 280, {"debut": "2001-09"})], places=7, reservoir=65,
   remarques="Monospace 7 ou 8 places")
mg(L, "Camry", "XV70", "1", "2019-03", "2024-12", [("2.5 Hybrid 218", "A25A-FXS", 221)], portes=4, reservoir=50,
   remarques="Retour en Europe (berline hybride)")
mg(L, "Camry", "XV80", "1", "2025-01", None, [("2.5 Hybrid 230", "A25A-FXS", 221)], portes=4, reservoir=50,
   remarques="Berline hybride")

# ---------------------------------------------------------------- sportives
mg(L, "Celica", "T180", "1", "1989-10", "1993-09",
   [("2.0 GTi 156", "3S-GE", 186), ("2.0 GT-Four 208", "3S-GTE", 275)], portes=3, places=4, reservoir=60,
   remarques="Liftback, Coupé, Cabriolet")
mg(L, "Celica", "T200", "1", "1993-11", "1999-08",
   [("1.8 116", "7A-FE", 156), ("2.0 GT 175", "3S-GE", 186), ("2.0 GT-Four 242", "3S-GTE", 304, {"debut": "1994-03", "fin": "1997-12"})],
   portes=3, places=4, reservoir=60, remarques="Liftback et Cabriolet")
mg(L, "Celica", "T230", "1", "1999-09", "2006-03",
   [("1.8 VVT-i 143", "1ZZ-FE", 169), ("1.8 TS 192", "2ZZ-GE", 180)], portes=3, places=4, reservoir=55, remarques="Coupé 3 portes")
mg(L, "MR2", "W10", "1", "1984-06", "1989-10", [("1.6 Twin Cam 124", "4A-GE", 142)], portes=2, places=2, reservoir=41,
   remarques="Coupé et T-Bar à moteur central")
mg(L, "MR2", "W20", "1", "1989-11", "1999-12", [("2.0 GTi 156", "3S-GE", 186, {"fin": "1993-12"}),
   ("2.0 GTi 175", "3S-GE", 186, {"debut": "1994-01"})], portes=2, places=2, reservoir=54, remarques="Coupé et T-Bar")
mg(L, "MR2", "W30", "1", "2000-01", "2007-07", [("1.8 VVT-i 140", "1ZZ-FE", 170)], portes=2, places=2, reservoir=48,
   remarques="MR2 Roadster")
mg(L, "Supra", "A40", "1", "1978-04", "1981-06", [("Celica Supra 2.6i 110", "4M-E", 186)], portes=3, places=4, reservoir=61,
   remarques="Celica Supra (MA46), liftback dérivé de la Celica ; données indicatives")
mg(L, "Supra", "A60", "1", "1981-07", "1986-01", [("Celica Supra 2.8i 170", "5M-GE", 236)], portes=3, places=4, reservoir=61,
   remarques="Celica Supra (MA61) ; données indicatives")
mg(L, "Supra", "A70", "1", "1986-02", "1993-04",
   [("3.0i 204", "7M-GE", 254), ("3.0i Turbo 235", "7M-GTE", 324, {"debut": "1987-01"})], portes=3, places=4, reservoir=70,
   remarques="Liftback (Targa en option)")
mg(L, "Supra", "A80", "1", "1993-05", "2002-08", [("3.0 Biturbo 330", "2JZ-GTE", 441)], portes=3, places=4, reservoir=70,
   remarques="Coupé (Targa en option)")
mg(L, "GT86", "ZN6", "1", "2012-06", "2016-08", [("2.0 D-4S 200", "FA20", 205)], portes=2, places=4, reservoir=50,
   remarques="Coupé propulsion (jumeau Subaru BRZ)")
mg(L, "GT86", "ZN6", "2", "2016-09", "2021-12", [("2.0 D-4S 200", "FA20", 205)], portes=2, places=4, reservoir=50)

# ---------------------------------------------------------------- RAV4 / SUV
mg(L, "RAV4", "XA10", "1", "1994-06", "2000-05", [("2.0 129", "3S-FE", 178)], portes=3, reservoir=58,
   remarques="3 et 5 portes, Cabriolet")
mg(L, "RAV4", "XA20", "1", "2000-06", "2005-11",
   [("1.8 VVT-i 125", "1ZZ-FE", 161), ("2.0 VVT-i 150", "1AZ-FE", 200), ("2.0 D-4D 116", "1CD-FTV", 280, {"debut": "2001-06"})],
   reservoir=57, remarques="3 et 5 portes")
mg(L, "RAV4", "XA30", "1", "2006-01", "2012-12",
   [("2.0 VVT-i 152", "1AZ-FE", 194), ("2.0 Valvematic 158", "3ZR-FAE", 198, {"debut": "2009-01"}),
    ("2.2 D-4D 136", "2AD-FTV", 310), ("2.2 D-4D 150", "2AD-FTV", 340, {"debut": "2009-01"}),
    ("2.2 D-CAT 177", "2AD-FHV", 400), ("2.0 D-4D 126", "1AD-FTV", 300, {"debut": "2010-06"})], reservoir=60)
mg(L, "RAV4", "XA40", "1", "2013-01", "2015-12",
   [("2.0 Valvematic 151", "3ZR-FAE", 195), ("2.0 D-4D 124", "1AD-FTV", 300), ("2.2 D-4D 150", "2AD-FTV", 340)], reservoir=60)
mg(L, "RAV4", "XA40", "2", "2016-01", "2018-12",
   [("2.0 Valvematic 152", "3ZR-FAE", 196), ("2.5 Hybrid 197", "2AR-FXE", 206), ("2.0 D-4D 143", "2WW", 320)], reservoir=60)
mg(L, "RAV4", "XA50", "1", "2019-01", "2025-12",
   [("2.5 Hybrid 218", "A25A-FXS", 221), ("2.5 Hybrid AWD-i 222", "A25A-FXS", 221),
    ("2.5 Plug-in Hybrid 306", "A25A-PHEV", 227, ph(18, 55, debut="2020-09"))], reservoir=55)
mg(L, "RAV4", "XA60", "1", "2026-01", None,
   [("2.5 Hybrid 185", "A25A-FXS", 221), ("2.5 Hybrid AWD-i 194", "A25A-FXS", 221),
    ("2.5 Plug-in Hybrid AWD-i 309", "A25A-PHEV", 227, ph(23, 55, debut="2026-04")),
    ("2.5 Plug-in Hybrid 272", "A25A-PHEV", 227, ph(23, 55, debut="2026-09"))], reservoir=55,
   remarques="6e génération, uniquement hybride et hybride rechargeable ; logiciel Arene")
mg(L, "Highlander", "XU70", "1", "2021-01", None, [("2.5 Hybrid AWD-i 248", "A25A-FXS", 239)], places=7, reservoir=65,
   remarques="SUV 7 places hybride")
mg(L, "bZ4X", "XEAM10", "1", "2022-04", "2025-03",
   [("bZ4X FWD 204", "eTNGA-EV", 266, el(71)), ("bZ4X AWD 218", "eTNGA-EV", 337, el(73))], reservoir=0,
   remarques="SUV électrique (e-TNGA)")
mg(L, "bZ4X", "XEAM10", "2", "2025-04", None,
   [("bZ4X 167", "eTNGA-EV", 268, el(58)), ("bZ4X 224", "eTNGA-EV", 268, el(73)), ("bZ4X AWD 343", "eTNGA-EV", 338, el(73))],
   reservoir=0, remarques="Restylage technique (batteries, puissances) ; appelé « bZ » dans certains pays")
mg(L, "Mirai", "JPD10", "1", "2015-09", "2020-12", [("Mirai 154", "FCEV", 335)], portes=4, places=4, reservoir=0,
   remarques="Berline à pile à combustible (hydrogène 5 kg)")
mg(L, "Mirai", "JPD20", "1", "2021-01", None, [("Mirai 182", "FCEV", 300)], portes=4, places=5, reservoir=0,
   remarques="Berline à pile à combustible (hydrogène 5,6 kg)")

# ---------------------------------------------------------------- Land Cruiser / Hilux
mg(L, "Land Cruiser", "J40", "1", "1960-08", "1984-12",
   [("FJ40 4.2 135", "2F", 284, {"debut": "1975-01"}), ("BJ40 3.4 D 90", "3B", 216, {"debut": "1979-01"}),
    ("HJ47 4.0 D 103", "2H", 245, {"debut": "1980-01"})], portes=3, places=6, reservoir=70,
   remarques="4x4 court et long ; motorisations antérieures (F 3.9, B 3.0 D) non détaillées")
mg(L, "Land Cruiser", "J60", "1", "1980-08", "1990-01",
   [("FJ60 4.2 135", "2F", 284), ("HJ60 4.0 D 103", "2H", 245), ("HJ61 4.0 TD 136", "12H-T", 315, {"debut": "1985-01"})],
   places=7, reservoir=90, remarques="Station wagon")
mg(L, "Land Cruiser", "J70", "1", "1984-11", "2006-12",
   [("BJ70 3.4 D 90", "3B", 216, {"fin": "1990-12"}), ("LJ70 2.4 TD 86", "2L", 188, {"fin": "1996-12"}),
    ("KZJ70 3.0 TD 125", "1KZ-TE", 287, {"debut": "1993-01", "fin": "1996-12"}),
    ("KDJ 3.0 D-4D 163", "1KD-FTV", 343, {"debut": "2001-01"})], portes=3, places=6, reservoir=90,
   remarques="4x4 utilitaire court et long ; commercialisation européenne limitée après 1996")
mg(L, "Land Cruiser", "J80", "1", "1990-01", "1997-12",
   [("HDJ80 4.2 TD 167", "1HD-T", 360), ("FZJ80 4.5 205", "1FZ-FE", 362, {"debut": "1992-08"})], places=7, reservoir=95,
   remarques="Grand station wagon")
mg(L, "Land Cruiser", "J90", "1", "1996-05", "2002-09",
   [("KZJ90 3.0 TD 125", "1KZ-TE", 287), ("VZJ90 3.4 V6 178", "5VZ-FE", 303)], portes=3, places=7, reservoir=87,
   remarques="3 et 5 portes")
mg(L, "Land Cruiser", "J120", "1", "2002-10", "2009-11",
   [("3.0 D-4D 163", "1KD-FTV", 343, {"fin": "2006-08"}), ("3.0 D-4D 173", "1KD-FTV", 410, {"debut": "2006-09"}),
    ("4.0 V6 249", "1GR-FE", 380)], portes=3, places=7, reservoir=87, remarques="3 et 5 portes")
mg(L, "Land Cruiser", "J150", "1", "2009-11", "2017-09",
   [("3.0 D-4D 173", "1KD-FTV", 410, {"fin": "2013-08"}), ("3.0 D-4D 190", "1KD-FTV", 420, {"debut": "2013-09"}),
    ("4.0 V6 282", "1GR-FE", 385), ("2.8 D-4D 177", "1GD-FTV", 450, {"debut": "2015-09"})], portes=3, places=7, reservoir=87,
   remarques="3 et 5 portes")
mg(L, "Land Cruiser", "J150", "2", "2017-10", "2024-03",
   [("2.8 D-4D 177", "1GD-FTV", 450, {"fin": "2020-09"}), ("2.8 D-4D 204", "1GD-FTV", 500, {"debut": "2020-10"})],
   portes=3, places=7, reservoir=87, remarques="3 et 5 portes")
mg(L, "Land Cruiser", "J250", "1", "2024-04", None,
   [("2.8 D-4D 204", "1GD-FTV", 500), ("2.8 D-4D Hybrid 48V 204", "1GD-MHEV", 500, {"debut": "2025-06"})], places=7,
   reservoir=80, remarques="5 portes, 5 ou 7 places")
mg(L, "Land Cruiser V8", "J100", "1", "1998-03", "2007-12",
   [("4.2 TD 204", "1HD-FTE", 430), ("4.7 V8 235", "2UZ-FE", 434)], places=8, reservoir=96, remarques="Land Cruiser 100")
mg(L, "Land Cruiser V8", "J200", "1", "2008-01", "2021-12", [("4.5 D-4D V8 286", "1VD-FTV", 650)], places=8, reservoir=93,
   remarques="Land Cruiser 200")
mg(L, "Hilux", "N140", "1", "1997-09", "2005-08",
   [("2.4 D 79", "2L", 158, {"fin": "2001-12"}), ("2.5 D-4D 102", "2KD-FTV", 260, {"debut": "2002-01"})], portes=4,
   reservoir=65, remarques="Pick-up simple, extra et double cabine")
mg(L, "Hilux", "AN10", "1", "2005-09", "2015-12",
   [("2.5 D-4D 102", "2KD-FTV", 260, {"fin": "2008-12"}), ("2.5 D-4D 120", "2KD-FTV", 325, {"debut": "2009-01"}),
    ("2.5 D-4D 144", "2KD-FTV", 343, {"debut": "2011-09"}), ("3.0 D-4D 171", "1KD-FTV", 343)], portes=4, reservoir=80,
   remarques="Pick-up ; restylages 2008 et 2011")
mg(L, "Hilux", "AN120", "1", "2016-01", "2020-09", [("2.4 D-4D 150", "2GD-FTV", 400)], portes=4, reservoir=80,
   remarques="Pick-up simple, extra et double cabine")
mg(L, "Hilux", "AN120", "2", "2020-10", "2025-12",
   [("2.4 D-4D 150", "2GD-FTV", 400), ("2.8 D-4D 204", "1GD-FTV", 500), ("2.8 D-4D Hybrid 48V 204", "1GD-MHEV", 500, {"debut": "2023-06"})],
   portes=4, reservoir=80, remarques="Pick-up ; GR Sport")
mg(L, "Hilux", "AN220", "1", "2026-01", None,
   [("2.8 D-4D Hybrid 48V 204", "1GD-MHEV", 500), ("Hilux Électrique 196", "Hilux-EV", 268, el(59))], portes=4, reservoir=80,
   remarques="9e génération (code indicatif) : diesel 48 V et électrique ; puissance et couple de la version électrique indicatifs")

# ---------------------------------------------------------------- Toyota GR
mg(LG, "GR Yaris", "GXPA16", "1", "2020-09", "2024-03", [("GR Yaris 261", "G16E-GTS", 360)], portes=3, places=4,
   reservoir=50, remarques="3 portes à transmission intégrale GR-Four")
mg(LG, "GR Yaris", "GXPA16", "2", "2024-04", None, [("GR Yaris 280", "G16E-GTS", 390)], portes=3, places=4, reservoir=50,
   remarques="Évolution : boîte manuelle ou automatique 8 rapports")
mg(L, "Supra", "A90", "1", "2019-03", None,
   [("GR Supra 3.0 340", "B58", 500), ("GR Supra 2.0 258", "B48", 400, {"debut": "2020-03", "fin": "2024-12"})],
   portes=2, places=2, reservoir=52, remarques="GR Supra, coupé (base BMW Z4 G29) ; boîte manuelle en option (2022)")
mg(LG, "GR86", "ZN8", "1", "2022-04", "2024-12", [("GR86 2.4 234", "FA24", 250)], portes=2, places=4, reservoir=50,
   remarques="Coupé propulsion (jumeau Subaru BRZ) ; vendu deux ans en Europe")

MOT = Motorisations("Toyota", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LG)

DETAIL = {"Toyota": L, "Toyota GR": LG}
MOTEURS = MOT.moteurs()
