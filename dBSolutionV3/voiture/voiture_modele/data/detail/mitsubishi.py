"""Mitsubishi et Mitsubishi Evo : générations, phases, motorisations (marché européen) et moteurs liés.
Mitsubishi : 500, Colt 800, Galant, Sigma, Lancer, Colt, Starion, 3000 GT, Eclipse, Space Star, Space Wagon, Space Runner,
Carisma, Pajero, Pajero Pinin, Grandis, Outlander (dont PHEV), ASX, Eclipse Cross, i-MiEV, L200 ; modèles Renault rebadgés
(Colt 2023, ASX 2023, Grandis 2025, Eclipse Cross EV 2025). Mitsubishi Evo : Lancer Evolution I à X.
Moteurs PSA et Mitsubishi « partagés » repris de citroen.py / peugeot_classiques.py, VW d'audi.py, Renault de renault.py
(mêmes codes) ; moteurs Mitsubishi ajoutés. Puissances des modèles Renault alignées sur Renault (Mitsubishi annonce
parfois 1 à 2 ch d'écart). Données anciennes indicatives.
Lancer Evolution IV à IX (280 ch) : couple unifié à 373 Nm (code moteur commun).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .audi import FAMILLES as FAMILLES_AUDI
from .citroen import FAMILLES as FAMILLES_CITROEN
from .peugeot_classiques import FAMILLES as FAMILLES_PEUGEOT
from .renault import FAMILLES as FAMILLES_RENAULT

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

MITSU = {
    "NE19-0.5": f("ATM", E_, 0.5, "NC", 2, 5000, 3800, "20W50", 2.0, 3000),
    "3G8-0.8": f("ATM", E_, 0.8, "NC", 3, 5000, 3000, "20W50", 2.5, 3000),
    "4G32-1.6": f("ATM", E_, 1.6, C, 4, 5500, 3500, "10W40", 4.0, 10000),
    "4G13-1.3": f("ATM", E_, 1.3, B, 4, 6000, 4000, "10W40", 3.5, 10000),
    "4G15-1.5": f("ATM", E_, 1.5, B, 4, 6000, 4000, "10W40", 3.5, 10000),
    "4G92-1.6": f("ATM", E_, 1.6, B, 4, 6000, 4500, "10W40", 3.8, 10000),
    "4G93-1.8": f("ATM", E_, 1.8, B, 4, 5500, 4500, "10W40", 3.8, 10000),
    "4G93-GDI-1.8": f("ATM", E_, 1.8, B, 4, 5500, 3750, "5W30", 3.8, 10000),
    "4G63-2.0": f("ATM", E_, 2.0, B, 4, 6000, 4500, "10W40", 4.3, 10000),
    "4G63T-2.0": f("TURBO", E_, 2.0, B, 4, 6500, 3000, "10W40", 4.9, 7500),
    "4G64-2.4": f("ATM", E_, 2.4, B, 4, 5500, 4000, "10W40", 4.3, 10000),
    "4G54T-2.6": f("TURBO", E_, 2.6, C, 4, 5000, 2500, "10W40", 4.5, 7500),
    "6A12-2.0": f("ATM", E_, 2.0, B, 6, 6000, 4500, "10W40", 4.0, 10000, a="V"),
    "6A13-2.5": f("ATM", E_, 2.5, B, 6, 5750, 4500, "10W40", 4.0, 10000, a="V"),
    "6G72-3.0": f("ATM", E_, 3.0, B, 6, 5500, 4000, "10W40", 4.5, 10000, a="V"),
    "6G72TT-3.0": f("TURBO", E_, 3.0, B, 6, 6000, 2500, "10W40", 4.5, 7500, a="V"),
    "6G74-3.5": f("ATM", E_, 3.5, B, 6, 5000, 4000, "10W40", 4.9, 10000, a="V"),
    "6G75-3.8": f("ATM", E_, 3.8, B, 6, 6000, 3750, "5W30", 4.6, 10000, a="V"),
    "4A90-1.1": f("ATM", E_, 1.1, C, 3, 6000, 4000, "5W30", 3.5, 15000),
    "4A91-1.3": f("ATM", E_, 1.3, C, 4, 6000, 4000, "5W30", 3.6, 15000),
    "4G15T-1.5": f("TURBO", E_, 1.5, C, 4, 6000, 3500, "5W30", 3.5, 15000),
    "3A90-1.0": f("ATM", E_, 1.0, C, 3, 6000, 5000, "0W20", 3.6, 15000),
    "3A92-1.2": f("ATM", E_, 1.2, C, 3, 6000, 4000, "0W20", 3.6, 15000),
    "4B10-1.8": f("ATM", E_, 1.8, C, 4, 6000, 4250, "5W30", 4.2, 15000),
    "4B11-2.0": f("ATM", E_, 2.0, C, 4, 6000, 4250, "5W30", 4.3, 15000),
    "4B11T-2.0": f("TURBO", E_, 2.0, C, 4, 6500, 3500, "5W30", 4.6, 10000),
    "4B11-PHEV": f("HYB_E", E_, 2.0, C, 4, 4500, 4500, "0W20", 4.3, 15000),
    "4B12-PHEV": f("HYB_E", E_, 2.4, C, 4, 4500, 4500, "0W20", 4.3, 15000),
    "4B40-1.5T": f("TURBO", E_, 1.5, C, 4, 5500, 2000, "0W20", 4.3, 15000),
    "4D56-2.5": f("TURBO", D, 2.5, B, 4, 4000, 2000, "10W40", 5.5, 10000),
    "4M40-2.8": f("TURBO", D, 2.8, C, 4, 4000, 2000, "10W40", 6.5, 10000),
    "4M41-3.2": f("TURBO", D, 3.2, C, 4, 3800, 2000, "10W40", 7.5, 10000),
    "4N14-2.2": f("TURBO", D, 2.2, C, 4, 3500, 1750, "5W30", 7.0, 15000),
    "4N15-2.4": f("TURBO", D, 2.4, C, 4, 3500, 2500, "5W30", 7.0, 15000),
}
PARTAGES_MITSU = {k: FAMILLES_CITROEN[k] for k in ("4B12", "Y4F1-EV")} | {k: FAMILLES_PEUGEOT[k] for k in ("4A92", "4N13")}
PSA = {"DW12C": FAMILLES_CITROEN["DW12C"]}
VW = {"EA188-2.0TDI": FAMILLES_AUDI["EA188-2.0TDI"]}
RENAULT = {k: FAMILLES_RENAULT[k] for k in ("F9Q", "H4D", "H4Dt", "H5Ht-MHEV", "HR16-ETECH", "CMF-EV")}
RENAULT["HR18-ETECH"] = f("HYB_E", E_, 1.8, C, 4, 5600, 3600, "0W20", 4.5, 30000)
FAMILLES = {**MITSU, **PARTAGES_MITSU, **PSA, **VW, **RENAULT}


def motoriste(fam):
    if fam in PSA:
        return "Peugeot"
    if fam in VW:
        return "Volkswagen"
    if fam in RENAULT:
        return "Renault"
    return "Mitsubishi"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Mitsubishi", motoriste)
L, EVO = [], []
IND = "données indicatives"

# ---------------------------------------------------------------- anciennes
mg(L, "500", "A11", "1", "1960-04", "1962-12", [("0.5 21", "NE19-0.5", 34)], portes=2, places=4, reservoir=20, remarques="Marché japonais ; " + IND)
mg(L, "Colt 800", "A7", "1", "1965-11", "1971-12", [("0.8 45", "3G8-0.8", 67)], portes=2, places=4, reservoir=30, remarques="Moteur deux temps ; " + IND)

# ---------------------------------------------------------------- Galant / Sigma
mg(L, "Galant", "A112", "1", "1976-05", "1980-04", [("1.6 75", "4G32-1.6", 120), ("2.0 90", "4G63-2.0", 155)], portes=4, places=5, reservoir=55,
   remarques="Commercialisée en Europe sous Colt Galant puis Mitsubishi ; " + IND)
mg(L, "Galant", "E10", "1", "1984-01", "1987-12", [("1.6 75", "4G32-1.6", 120), ("2.0 102", "4G63-2.0", 160), ("2.0 Turbo 150", "4G63T-2.0", 220)],
   portes=4, places=5, reservoir=60, remarques=IND)
mg(L, "Galant", "E30", "1", "1988-01", "1992-12",
   [("1.8 90", "4G93-1.8", 145), ("2.0 109", "4G63-2.0", 165), ("2.0 GTI 16v 144", "4G63-2.0", 170), ("VR-4 2.0 Turbo 195", "4G63T-2.0", 275)],
   portes=4, places=5, reservoir=60, remarques="Berline et 5 portes ; " + IND)
mg(L, "Galant", "E50", "1", "1993-01", "1996-12",
   [("1.8 115", "4G93-1.8", 157), ("2.0 V6 150", "6A12-2.0", 180), ("2.5 V6 170", "6A13-2.5", 222)],
   portes=4, places=5, reservoir=60, remarques=IND)
mg(L, "Galant", "EA0", "1", "1997-01", "2003-12", [("2.0 136", "4G63-2.0", 176), ("2.5 V6 163", "6A13-2.5", 216)], portes=4, places=5, reservoir=62,
   remarques="Berline et break ; " + IND)
mg(L, "Sigma", "F10", "1", "1991-01", "1996-12", [("3.0 V6 205", "6G72-3.0", 270)], portes=4, places=5, reservoir=72, remarques="Berline et break ; " + IND)

# ---------------------------------------------------------------- Lancer
mg(L, "Lancer", "C10", "1", "1983-09", "1988-12", [("1.5 75", "4G15-1.5", 118), ("1.8 Turbo 135", "4G63T-2.0", 196, {"remarques": "1.8 4G62T rattaché au 4G63T"})],
   portes=4, places=5, reservoir=50, remarques=IND)
mg(L, "Lancer", "CB/CD", "1", "1992-01", "1996-12", [("1.3 75", "4G13-1.3", 108), ("1.6 113", "4G92-1.6", 137), ("1.8 GLX 4x4 115", "4G93-1.8", 157)],
   portes=4, places=5, reservoir=50, remarques=IND)
mg(L, "Lancer", "CS", "1", "2003-03", "2007-12", [("1.3 82", "4G13-1.3", 120), ("1.6 98", "4G92-1.6", 137), ("2.0 135", "4G63-2.0", 176)],
   portes=4, places=5, reservoir=50, remarques="Berline et break")
mg(L, "Lancer", "CY", "1", "2008-01", "2017-12",
   [("1.5 109", "4A91-1.3", 143, {"remarques": "1.5 4A91 MIVEC"}), ("1.8 143", "4B10-1.8", 178), ("2.0 DI-D 140", "EA188-2.0TDI", 320, {"fin": "2010-12"}),
    ("1.8 DI-D 116", "4N13", 300, {"debut": "2010-06"}), ("Ralliart 2.0 Turbo 240", "4B11T-2.0", 343, {"debut": "2008-09", "fin": "2012-12"})],
   portes=5, places=5, reservoir=59, remarques="Berline et Sportback ; 4A91 1.5 rattaché à la famille 1.3")

# ---------------------------------------------------------------- Colt
mg(L, "Colt", "C1A", "1", "1984-01", "1987-12", [("1.2 55", "4G13-1.3", 92), ("1.5 75", "4G15-1.5", 118), ("1.6 Turbo 125", "4G63T-2.0", 180)],
   portes=3, places=5, reservoir=40, remarques=IND)
mg(L, "Colt", "CA", "1", "1988-01", "1991-12", [("1.3 68", "4G13-1.3", 105), ("1.5 84", "4G15-1.5", 124), ("1.6 GTi 16v 125", "4G92-1.6", 140)],
   portes=3, places=5, reservoir=45, remarques=IND)
mg(L, "Colt", "CJ", "1", "1996-01", "2003-12", [("1.3 75", "4G13-1.3", 108), ("1.6 90", "4G92-1.6", 137), ("1.6 GDI 90", "4G92-1.6", 137, {"debut": "1999-01"})],
   portes=3, places=5, reservoir=50, remarques=IND)
mg(L, "Colt", "Z30", "1", "2004-06", "2008-09", [("1.1 75", "4A90-1.1", 100), ("1.3 95", "4A91-1.3", 125), ("1.5 109", "4G15-1.5", 145),
                                                 ("CZT 1.5 Turbo 150", "4G15T-1.5", 210, {"debut": "2005-01"})], portes=5, places=5, reservoir=47,
   remarques="3 et 5 portes, cabriolet CZC (2006-2009) ; partage sa base avec la Smart ForFour")
mg(L, "Colt", "Z30", "2", "2008-10", "2012-12", [("1.1 75", "4A90-1.1", 100), ("1.3 95", "4A91-1.3", 125), ("CZT 1.5 Turbo 150", "4G15T-1.5", 210)],
   portes=5, places=5, reservoir=47, remarques="Restylage")
mg(L, "Colt", "BF", "1", "2023-04", None, [("1.0 MPI 65", "H4D", 95), ("1.0 T 90", "H4Dt", 160), ("HEV 145", "HR16-ETECH", 205, {"reservoir": 39, "batterie": 1})],
   portes=5, places=5, reservoir=42, remarques="Base Renault Clio V")

# ---------------------------------------------------------------- sportives
mg(L, "Starion", "A180", "1", "1982-05", "1989-12", [("2.0 Turbo 170", "4G63T-2.0", 245), ("2.6 Turbo 156", "4G54T-2.6", 290, {"debut": "1987-01"})],
   portes=3, places=4, reservoir=75, remarques=IND)
mg(L, "3000 GT", "Z16A", "1", "1990-10", "1993-12", [("3.0 V6 Biturbo 286", "6G72TT-3.0", 427)], portes=3, places=4, reservoir=75,
   remarques="GTO au Japon ; " + IND)
mg(L, "3000 GT", "Z16A", "2", "1994-01", "2000-12", [("3.0 V6 Biturbo 286", "6G72TT-3.0", 427)], portes=3, places=4, reservoir=75, remarques=IND)
mg(L, "Eclipse", "D2", "1", "1995-01", "1999-12", [("2.0 146", "4G63-2.0", 183)], portes=3, places=4, reservoir=60, remarques="Vendue en Europe ; " + IND)

# ---------------------------------------------------------------- monospaces
mg(L, "Space Wagon", "N30", "1", "1991-01", "1998-12", [("1.8 122", "4G93-1.8", 159), ("2.0 133", "4G63-2.0", 176)], portes=5, places=7, reservoir=60, remarques=IND)
mg(L, "Space Wagon", "N80", "1", "1999-01", "2004-12", [("2.4 GDI 150", "4G64-2.4", 216)], portes=5, places=7, reservoir=60, remarques=IND)
mg(L, "Space Runner", "N10", "1", "1991-01", "1999-12", [("1.8 122", "4G93-1.8", 159)], portes=5, places=5, reservoir=55, remarques=IND)
mg(L, "Space Star", "DG0", "1", "1998-09", "2005-12",
   [("1.3 86", "4G13-1.3", 118), ("1.6 98", "4G92-1.6", 137), ("1.8 GDI 122", "4G93-GDI-1.8", 174), ("1.9 DI-D 102", "F9Q", 200, {"debut": "2001-01"})],
   portes=5, places=5, reservoir=50, remarques="Fabriquée par NedCar")
mg(L, "Space Star", "A00", "1", "2013-01", "2016-08", [("1.0 71", "3A90-1.0", 88), ("1.2 80", "3A92-1.2", 106)], portes=5, places=5, reservoir=35,
   remarques="Mirage hors Europe")
mg(L, "Space Star", "A00", "2", "2016-09", "2024-12", [("1.0 71", "3A90-1.0", 88, {"fin": "2019-12"}), ("1.2 80", "3A92-1.2", 106)], portes=5, places=5, reservoir=35,
   remarques="Restylages 2016 et 2020")
mg(L, "Carisma", "DA", "1", "1995-09", "2004-06",
   [("1.6 90", "4G92-1.6", 137), ("1.8 116", "4G93-1.8", 155), ("1.8 GDI 125", "4G93-GDI-1.8", 174, {"debut": "1997-06"}), ("1.9 TD 90", "F9Q", 176),
    ("1.9 DI-D 102", "F9Q", 200, {"debut": "2000-01"})], portes=5, places=5, reservoir=60, remarques="Berline et 5 portes, fabriquée par NedCar ; " + IND)
mg(L, "Grandis", "NA4W", "1", "2004-01", "2011-12", [("2.4 165", "4G64-2.4", 217), ("2.0 DI-D 136", "EA188-2.0TDI", 320, {"debut": "2005-06"})],
   portes=5, places=7, reservoir=65, remarques="Monospace 6 ou 7 places")
mg(L, "Grandis", "Symbioz", "1", "2025-10", None, [("1.3 MHEV 140", "H5Ht-MHEV", 260), ("HEV 160", "HR18-ETECH", 172, {"debut": "2026-01", "reservoir": 47, "batterie": 1})],
   portes=5, places=5, reservoir=48, remarques="SUV compact, base Renault Symbioz ; HEV 1.8 160 ch (couple thermique) ; " + IND)

# ---------------------------------------------------------------- 4x4 et SUV
mg(L, "Pajero", "L040", "1", "1982-05", "1990-12", [("2.6 103", "4G54T-2.6", 192, {"remarques": "2.6 atmosphérique rattaché à la famille 4G54"}), ("2.5 TD 84", "4D56-2.5", 197)],
   portes=5, places=7, reservoir=60, remarques="3 et 5 portes ; " + IND)
mg(L, "Pajero", "V20", "1", "1991-01", "1999-12",
   [("3.0 V6 150", "6G72-3.0", 237), ("3.5 V6 208", "6G74-3.5", 300, {"debut": "1994-01"}), ("2.5 TD 99", "4D56-2.5", 240), ("2.8 TD 125", "4M40-2.8", 294, {"debut": "1994-01"})],
   portes=5, places=7, reservoir=92, remarques="3 et 5 portes ; " + IND)
mg(L, "Pajero", "V60", "1", "2000-01", "2006-12",
   [("3.2 DI-D 160", "4M41-3.2", 373), ("3.5 V6 GDI 202", "6G74-3.5", 318, {"fin": "2003-06"}), ("3.8 V6 250", "6G75-3.8", 329, {"debut": "2003-07"})],
   portes=5, places=7, reservoir=90)
mg(L, "Pajero", "V80", "1", "2007-01", "2021-08", [("3.2 DI-D 170", "4M41-3.2", 381, {"fin": "2009-12"}), ("3.2 DI-D 200", "4M41-3.2", 441, {"debut": "2010-01"}),
                                                    ("3.8 V6 250", "6G75-3.8", 329, {"fin": "2012-12"})], portes=5, places=7, reservoir=88,
   remarques="3 et 5 portes ; retiré d'Europe vers 2019")
mg(L, "Pajero Pinin", "H60", "1", "1999-01", "2007-12", [("1.8 GDI 120", "4G93-GDI-1.8", 161), ("2.0 GDI 129", "4G63-2.0", 191)], portes=5, places=5, reservoir=53,
   remarques="3 et 5 portes, fabriqué par Pininfarina")
mg(L, "L200", "K30/K60", "1", "1996-01", "2005-12", [("2.5 TD 99", "4D56-2.5", 240), ("2.5 TD 115", "4D56-2.5", 240, {"debut": "2001-01"})], portes=4, places=5,
   reservoir=75, remarques="Simple, club et double cabine ; " + IND)
mg(L, "L200", "KB", "1", "2006-01", "2015-06", [("2.5 DI-D 136", "4D56-2.5", 314), ("2.5 DI-D 178", "4D56-2.5", 400, {"debut": "2010-01"})], portes=4, places=5,
   reservoir=75)
mg(L, "L200", "KL", "1", "2015-07", "2024-12", [("2.4 DI-D 154", "4N15-2.4", 380), ("2.4 DI-D 181", "4N15-2.4", 430), ("2.2 DI-D 150", "4N14-2.2", 360, {"debut": "2019-09"})],
   portes=4, places=5, reservoir=75, remarques="Restylage 2019 ; retrait progressif d'Europe")
mg(L, "Outlander", "CU", "1", "2003-01", "2006-12", [("2.0 136", "4G63-2.0", 176), ("2.4 160", "4G64-2.4", 216), ("2.0 Turbo 202", "4G63T-2.0", 303, {"debut": "2004-06"})],
   portes=5, places=5, reservoir=60)
mg(L, "Outlander", "CW", "1", "2007-01", "2012-08",
   [("2.0 DI-D 140", "EA188-2.0TDI", 320), ("2.2 DI-D 156", "DW12C", 380, {"debut": "2008-06"}), ("2.4 170", "4B12", 226), ("2.2 DI-D 177", "4N14-2.2", 380, {"debut": "2010-06"})],
   portes=5, places=7, reservoir=60, remarques="Jumeau des Peugeot 4007 et Citroën C-Crosser")
mg(L, "Outlander", "GF", "1", "2012-09", "2021-12", [("2.0 150", "4B11-2.0", 195), ("2.2 DI-D 150", "4N14-2.2", 360), ("2.4 167", "4B12", 222, {"debut": "2015-06"})],
   portes=5, places=7, reservoir=60, remarques="Restylages 2015 et 2018")
mg(L, "Outlander PHEV", "GG", "1", "2013-10", "2018-08", [("2.0 PHEV 203", "4B11-PHEV", 190, {"batterie": 12})], portes=5, places=5, reservoir=45,
   remarques="Puissance système ; couple thermique")
mg(L, "Outlander PHEV", "GG", "2", "2018-09", "2021-12", [("2.4 PHEV 224", "4B12-PHEV", 211, {"batterie": 14})], portes=5, places=5, reservoir=45,
   remarques="Puissance système ; couple thermique")
mg(L, "Outlander PHEV", "GN", "1", "2024-03", "2025-08", [("2.4 PHEV 306", "4B12-PHEV", 195, {"batterie": 20})], portes=5, places=7, reservoir=56,
   remarques="Puissance système ; couple thermique")
mg(L, "Outlander PHEV", "GN", "2", "2025-09", None, [("2.4 PHEV 306", "4B12-PHEV", 195, {"batterie": 23})], portes=5, places=7, reservoir=53,
   remarques="Mise à jour : batterie 22,7 kWh ; " + IND)
mg(L, "ASX", "GA", "1", "2010-06", "2016-08",
   [("1.6 117", "4A92", 154), ("1.8 140", "4B10-1.8", 172, {"fin": "2012-12"}), ("1.8 DI-D 116", "4N13", 300), ("1.8 DI-D 150", "4N13", 300), ("2.2 DI-D 150", "4N14-2.2", 360, {"debut": "2013-06"})],
   portes=5, places=5, reservoir=63)
mg(L, "ASX", "GA", "2", "2016-09", "2022-12", [("1.6 117", "4A92", 154), ("2.0 150", "4B11-2.0", 195), ("2.2 DI-D 150", "4N14-2.2", 360, {"fin": "2019-08"})],
   portes=5, places=5, reservoir=63, remarques="Restylages 2016 et 2019")
mg(L, "ASX", "HJB", "1", "2023-03", "2025-03", [("1.0 T 90", "H4Dt", 160), ("1.3 MHEV 140", "H5Ht-MHEV", 260), ("1.3 MHEV 160", "H5Ht-MHEV", 270),
                                                ("HEV 145", "HR16-ETECH", 205, {"batterie": 1})], portes=5, places=5, reservoir=48, remarques="Base Renault Captur")
mg(L, "ASX", "HJB", "2", "2025-04", None,
   [("1.0 T 90", "H4Dt", 160), ("1.3 MHEV 140", "H5Ht-MHEV", 260), ("1.3 MHEV 160", "H5Ht-MHEV", 270, {"fin": "2025-12"}), ("HEV 145", "HR16-ETECH", 205, {"batterie": 1, "fin": "2025-12"}),
    ("HEV 160", "HR18-ETECH", 172, {"debut": "2026-01", "batterie": 1})], portes=5, places=5, reservoir=48,
   remarques="Restylage (base Captur phase 2) ; HEV 1.8 160 ch (couple thermique) ; " + IND)
mg(L, "Eclipse Cross", "GK", "1", "2017-11", "2021-02", [("1.5 T 163", "4B40-1.5T", 250), ("2.2 DI-D 148", "4N14-2.2", 388, {"debut": "2018-09", "fin": "2019-12"})],
   portes=5, places=5, reservoir=63)
mg(L, "Eclipse Cross", "GK", "2", "2021-03", "2024-12", [("2.4 PHEV 188", "4B12-PHEV", 199, {"reservoir": 43, "batterie": 14})], portes=5, places=5, reservoir=43,
   remarques="Restylage, uniquement hybride rechargeable en Europe ; puissance système")
mg(L, "Eclipse Cross", "RHN", "1", "2025-10", None, [("Comfort Range 170", "CMF-EV", 280, el(60)), ("Long Range 220", "CMF-EV", 300, el(87))], portes=5, places=5,
   reservoir=0, remarques="Électrique, base Renault Scénic E-Tech ; " + IND)
mg(L, "i-MiEV", "HA", "1", "2010-12", "2017-12", [("Électrique 67", "Y4F1-EV", 180, el(16))], portes=5, places=4, reservoir=0,
   remarques="Jumeau des Peugeot iOn et Citroën C-Zero")

# ---------------------------------------------------------------- Mitsubishi Evo
mg(EVO, "Lancer Evolution", "I", "1", "1992-10", "1994-01", [("2.0 Turbo 250", "4G63T-2.0", 309)], portes=4, places=5, reservoir=50, remarques="Marché japonais ; " + IND)
mg(EVO, "Lancer Evolution", "II", "1", "1994-01", "1995-01", [("2.0 Turbo 260", "4G63T-2.0", 309)], portes=4, places=5, reservoir=50, remarques=IND)
mg(EVO, "Lancer Evolution", "III", "1", "1995-02", "1996-07", [("2.0 Turbo 270", "4G63T-2.0", 309)], portes=4, places=5, reservoir=50, remarques=IND)
mg(EVO, "Lancer Evolution", "IV", "1", "1996-08", "1998-01", [("2.0 Turbo 280", "4G63T-2.0", 373)], portes=4, places=5, reservoir=50, remarques=IND)
mg(EVO, "Lancer Evolution", "V", "1", "1998-01", "1999-01", [("2.0 Turbo 280", "4G63T-2.0", 373)], portes=4, places=5, reservoir=50, remarques=IND)
mg(EVO, "Lancer Evolution", "VI", "1", "1999-01", "2001-01", [("2.0 Turbo 280", "4G63T-2.0", 373)], portes=4, places=5, reservoir=50,
   remarques="Dont Tommi Mäkinen Edition ; " + IND)
mg(EVO, "Lancer Evolution", "VII", "1", "2001-02", "2003-01", [("2.0 Turbo 280", "4G63T-2.0", 373)], portes=4, places=5, reservoir=50, remarques=IND)
mg(EVO, "Lancer Evolution", "VIII", "1", "2003-02", "2005-02",
   [("2.0 Turbo 265", "4G63T-2.0", 355), ("FQ-300 2.0 Turbo 305", "4G63T-2.0", 407, {"debut": "2004-01"}), ("FQ-340 2.0 Turbo 345", "4G63T-2.0", 441, {"debut": "2004-06"})],
   portes=4, places=5, reservoir=55, remarques="Versions européennes et britanniques ; " + IND)
mg(EVO, "Lancer Evolution", "IX", "1", "2005-03", "2007-12",
   [("2.0 Turbo 280", "4G63T-2.0", 373), ("FQ-340 2.0 Turbo 345", "4G63T-2.0", 441), ("FQ-360 2.0 Turbo 366", "4G63T-2.0", 492)], portes=4, places=5, reservoir=55,
   remarques="Berline et break (Japon) ; " + IND)
mg(EVO, "Lancer Evolution", "X", "1", "2008-03", "2016-04",
   [("2.0 Turbo 295", "4B11T-2.0", 366), ("FQ-330 2.0 Turbo 335", "4B11T-2.0", 437, {"debut": "2008-09"}), ("FQ-400 2.0 Turbo 411", "4B11T-2.0", 525, {"debut": "2009-06", "fin": "2011-12"})],
   portes=4, places=5, reservoir=55, remarques="Retrait d'Europe vers 2014 ; " + IND)

MOT = Motorisations("Mitsubishi", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(EVO)

DETAIL = {"Mitsubishi": L, "Mitsubishi Evo": EVO}
MOTEURS = MOT.moteurs()
