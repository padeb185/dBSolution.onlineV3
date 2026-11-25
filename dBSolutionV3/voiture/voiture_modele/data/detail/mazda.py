"""Mazda et Mazda Speed : générations, phases, motorisations (marché européen) et moteurs liés.
Mazda : R360, Familia/1000, Cosmo Sport, RX-7, RX-8, 121, 323, Mazda2, Mazda3, Mazda6, Mazda 6e, MX-5, MX-30, CX-3, CX-30,
CX-5, CX-60, CX-80, CX-6e ; modèles nord-américains (CX-50, CX-70, CX-90 : hp convertis en ch ×1,014).
Mazda Speed : Mazda3 MPS (Mazdaspeed3), Mazda6 MPS (Mazdaspeed6), MX-5 Mazdaspeed.
Moteurs Mazda au motoriste « Mazda » ; diesels PSA (peugeot.py), Ford Sigma (ford.py) et hybride Toyota (toyota.py) repris avec
leurs codes. Données anciennes indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .ford import FAMILLES as FAMILLES_FORD
from .peugeot import FAMILLES as FAMILLES_PEUGEOT
from .toyota import FAMILLES as FAMILLES_TOYOTA

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"


def rot(l, rpm, nmrpm):
    return f("WANKEL", E_, l, "AUCUNE", 2, rpm, nmrpm, "10W30", 4.5, 5000, a="ROTATIF")


MAZDA = {
    "MZ-R360": f("ATM", E_, 0.36, "NC", 2, 5300, 4000, "20W50", 1.5, 3000, a="V"),
    "MZ-PB-1.0": f("ATM", E_, 1.0, C, 4, 6000, 3500, "20W50", 3.2, 5000),
    "R-10A": rot(1.0, 7000, 5000), "R-12A": rot(1.15, 6000, 4000), "R-13B": rot(1.3, 6500, 3500),
    "R-13BT": f("WANKEL", E_, 1.3, "AUCUNE", 2, 6500, 3500, "10W30", 5.0, 5000, a="ROTATIF"),
    "R-13B-REW": f("WANKEL", E_, 1.3, "AUCUNE", 2, 6500, 5000, "10W30", 5.0, 5000, a="ROTATIF"),
    "R-RENESIS": rot(1.3, 8200, 5500),
    "R-8C-REV": f("HYB_E", E_, 0.83, "AUCUNE", 1, 4500, 4000, "0W20", 3.5, 15000, a="ROTATIF"),
    "MZ-E-1.1": f("ATM", E_, 1.1, B, 4, 6000, 3500, "10W40", 3.2, 10000),
    "MZ-E-1.3": f("ATM", E_, 1.3, B, 4, 6000, 3500, "10W40", 3.2, 10000),
    "MZ-E-1.5": f("ATM", E_, 1.5, B, 4, 5500, 3500, "10W40", 3.2, 10000),
    "MZ-B3-1.3": f("ATM", E_, 1.3, B, 4, 6000, 3500, "10W40", 3.4, 10000),
    "MZ-B6-1.6": f("ATM", E_, 1.6, B, 4, 6000, 4000, "10W40", 3.4, 10000),
    "MZ-B6-1.6T": f("TURBO", E_, 1.6, B, 4, 6000, 5000, "10W40", 3.6, 10000),
    "MZ-BP-1.8": f("ATM", E_, 1.8, B, 4, 6500, 4500, "10W40", 3.6, 10000),
    "MZ-BP-1.8T": f("TURBO", E_, 1.8, B, 4, 6000, 4500, "10W40", 3.8, 10000),
    "MZ-Z5-1.5": f("ATM", E_, 1.5, B, 4, 5500, 4000, "10W40", 3.4, 15000),
    "MZ-FP-1.8": f("ATM", E_, 1.8, B, 4, 5500, 4500, "10W40", 3.8, 15000),
    "MZ-KF-2.0V6": f("ATM", E_, 2.0, B, 6, 6000, 4500, "10W40", 4.0, 15000, a="V"),
    "MZ-PN-1.7D": f("ATM", D, 1.7, B, 4, 4500, 2500, "15W40", 4.5, 10000),
    "MZ-RF-2.0D": f("TURBO", D, 2.0, B, 4, 4000, 2000, "10W40", 5.0, 10000),
    "MZR-1.3": f("ATM", E_, 1.3, C, 4, 6000, 4000, "5W30", 3.5, 20000),
    "MZR-1.4": f("ATM", E_, 1.4, C, 4, 5700, 3500, "5W30", 3.5, 20000),
    "MZR-1.5": f("ATM", E_, 1.5, C, 4, 6000, 4500, "5W30", 3.5, 20000),
    "MZR-1.6": f("ATM", E_, 1.6, C, 4, 6000, 4000, "5W30", 4.0, 20000),
    "MZR-1.8": f("ATM", E_, 1.8, C, 4, 6000, 4500, "5W30", 4.3, 20000),
    "MZR-2.0": f("ATM", E_, 2.0, C, 4, 6500, 4500, "5W30", 4.3, 20000),
    "MZR-2.3": f("ATM", E_, 2.3, C, 4, 6500, 4500, "5W30", 4.3, 20000),
    "MZR-2.5": f("ATM", E_, 2.5, C, 4, 6000, 4000, "5W30", 4.5, 20000),
    "MZR-2.3T": f("TURBO", E_, 2.3, C, 4, 5500, 3000, "5W30", 4.6, 20000),
    "MZR-CD-2.0": f("TURBO", D, 2.0, C, 4, 3500, 2000, "5W30", 5.5, 20000),
    "MZR-CD-2.2": f("TURBO", D, 2.2, C, 4, 3500, 2000, "5W30", 5.5, 20000),
    "SKY-G-1.5": f("ATM", E_, 1.5, C, 4, 6000, 3500, "0W20", 4.0, 20000),
    "SKY-G-1.5-MHEV": f("HYB_E", E_, 1.5, C, 4, 6000, 3500, "0W20", 4.0, 20000),
    "SKY-G-2.0": f("ATM", E_, 2.0, C, 4, 6000, 4000, "0W20", 4.2, 20000),
    "SKY-G-2.0-MHEV": f("HYB_E", E_, 2.0, C, 4, 6000, 4000, "0W20", 4.2, 20000),
    "SKY-X-2.0-MHEV": f("HYB_E", E_, 2.0, C, 4, 6000, 3000, "0W20", 4.2, 20000),
    "SKY-G-2.5": f("ATM", E_, 2.5, C, 4, 6000, 4000, "0W20", 4.5, 20000),
    "SKY-G-2.5-MHEV": f("HYB_E", E_, 2.5, C, 4, 5000, 3500, "0W20", 4.5, 20000),
    "SKY-G-2.5T": f("TURBO", E_, 2.5, C, 4, 5000, 2000, "0W20", 4.8, 20000),
    "SKY-G-2.5-HEV": f("HYB_TE", E_, 2.5, C, 4, 5700, 3600, "0W16", 4.5, 20000),
    "SKY-PHEV-2.5": f("HYB_E", E_, 2.5, C, 4, 6000, 4000, "0W20", 5.0, 20000),
    "SKY-G-3.3T-MHEV": f("HYB_E", E_, 3.3, C, 6, 6000, 2000, "0W20", 6.5, 20000),
    "SKY-D-1.5": f("TURBO", D, 1.5, C, 4, 4000, 1600, "0W30", 4.5, 20000),
    "SKY-D-1.8": f("TURBO", D, 1.8, C, 4, 4000, 1600, "0W30", 4.5, 20000),
    "SKY-D-2.2": f("TURBO", D, 2.2, C, 4, 4500, 2000, "0W30", 5.5, 20000),
    "SKY-D-3.3-MHEV": f("HYB_E", D, 3.3, C, 6, 3750, 1500, "0W30", 7.0, 20000),
    "MAZDA-EV": electrique(),
}
PEUGEOT = {k: FAMILLES_PEUGEOT[k] for k in ("DV4TD", "DV6TED4", "DV6C")}
FORD = {"SIGMA-1.25": FAMILLES_FORD["SIGMA-1.25"]}
TOYOTA = {"M15A-FXE": FAMILLES_TOYOTA["M15A-FXE"]}
FAMILLES = {**MAZDA, **PEUGEOT, **FORD, **TOYOTA}


def motoriste(fam):
    return "Peugeot" if fam in PEUGEOT else ("Ford" if fam in FORD else ("Toyota" if fam in TOYOTA else "Mazda"))


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


NA = "Marché nord-américain (hp convertis en ch)"
mg = SaisieMoteurs(FAMILLES, "Mazda", motoriste)
L = []

# ---------------------------------------------------------------- historiques
mg(L, "R360 Coupé", "R360", "1", "1960-05", "1969-12", [("0.36 V2 16", "MZ-R360", 22)], portes=2, places=4, reservoir=18, remarques="Kei-car japonaise ; données indicatives")
mg(L, "Mazda 1000 / Familia", "Familia", "1", "1963-10", "1977-12", [("1.0 52", "MZ-PB-1.0", 75)], portes=4, places=5, reservoir=40,
   remarques="Familia (Mazda 1000/1200 à l'export) ; données indicatives")
mg(L, "Cosmo Sport", "L10", "1", "1967-05", "1972-09", [("10A Rotatif 110", "R-10A", 130, {"fin": "1968-06"}), ("10A Rotatif 128", "R-10A", 140, {"debut": "1968-07"})],
   portes=2, places=2, reservoir=57, remarques="Premier moteur rotatif Mazda ; données indicatives")
mg(L, "Mazda RX-7", "SA/FB", "1", "1978-03", "1985-09", [("12A Rotatif 105", "R-12A", 144), ("12A Rotatif 115", "R-12A", 147, {"debut": "1981-01"})], portes=2, places=2,
   reservoir=55, remarques="Données indicatives")
mg(L, "Mazda RX-7", "FC", "1", "1985-10", "1992-09", [("13B Rotatif 150", "R-13B", 186), ("13B Turbo 182", "R-13BT", 249), ("13B Turbo 200", "R-13BT", 270, {"debut": "1989-04"})],
   portes=2, places=2, reservoir=63, remarques="Coupé et cabriolet ; données indicatives")
mg(L, "Mazda RX-7", "FD", "1", "1992-10", "2002-08", [("13B-REW Biturbo 239", "R-13B-REW", 294)], portes=2, places=2, reservoir=76,
   remarques="Version européenne 239 ch (1992-1995) ; versions japonaises 255 à 280 ch non détaillées")
mg(L, "Mazda RX-8", "SE3P", "1", "2003-05", "2012-06", [("Renesis 192", "R-RENESIS", 220), ("Renesis 231", "R-RENESIS", 211)], portes=4, places=4, reservoir=61,
   remarques="Portes antagonistes ; restylage 2008")

# ---------------------------------------------------------------- citadines et compactes
mg(L, "Mazda 121", "DA", "1", "1987-01", "1990-12", [("1.1 55", "MZ-B3-1.3", 85), ("1.3 64", "MZ-B3-1.3", 100)], portes=3, places=5, reservoir=38,
   remarques="Données indicatives (1.1 rattaché à la famille B 1.3)")
mg(L, "Mazda 121", "DB", "1", "1991-01", "1996-06", [("1.3 73", "MZ-B3-1.3", 104)], portes=4, places=5, reservoir=40, remarques="Berline « bulle » ; données indicatives")
mg(L, "Mazda 121", "JASM", "1", "1996-07", "2003-03", [("1.25 75", "SIGMA-1.25", 110)], portes=5, places=5, reservoir=42, remarques="Ford Fiesta rebadgée")
mg(L, "Mazda 323", "BD", "1", "1980-06", "1985-05", [("1.3 68", "MZ-E-1.3", 100), ("1.5 85", "MZ-E-1.5", 120)], portes=5, places=5, reservoir=45,
   remarques="Première 323 à traction ; données indicatives")
mg(L, "Mazda 323", "BF", "1", "1985-06", "1989-08",
   [("1.3 64", "MZ-E-1.3", 100), ("1.6 85", "MZ-B6-1.6", 125), ("1.6 Turbo 4WD 148", "MZ-B6-1.6T", 197, {"debut": "1986-06"})], portes=5, places=5, reservoir=45,
   remarques="Données indicatives")
mg(L, "Mazda 323", "BG", "1", "1989-09", "1994-08",
   [("1.3 73", "MZ-B3-1.3", 104), ("1.6 88", "MZ-B6-1.6", 132), ("1.8 16V 140", "MZ-BP-1.8", 160), ("GT-R 1.8 Turbo 185", "MZ-BP-1.8T", 240, {"debut": "1992-01"})],
   portes=5, places=5, reservoir=50, remarques="323 F à phares escamotables ; données indicatives")
mg(L, "Mazda 323", "BA", "1", "1994-09", "1998-08",
   [("1.3 75", "MZ-B3-1.3", 106), ("1.5 88", "MZ-Z5-1.5", 130), ("1.8 115", "MZ-FP-1.8", 155), ("2.0 V6 144", "MZ-KF-2.0V6", 180), ("1.7 D 55", "MZ-PN-1.7D", 105)],
   portes=5, places=5, reservoir=50, remarques="323 F/P/C ; données indicatives")
mg(L, "Mazda 323", "BJ", "1", "1998-09", "2003-09",
   [("1.4 73", "MZ-B3-1.3", 104), ("1.6 98", "MZ-B6-1.6", 145), ("1.8 114", "MZ-FP-1.8", 157), ("2.0 DiTD 90", "MZ-RF-2.0D", 220), ("2.0 DiTD 101", "MZ-RF-2.0D", 230)],
   portes=5, places=5, reservoir=55, remarques="Restylage 2000 ; données indicatives (1.4 rattaché à la famille B)")
mg(L, "Mazda2", "DY", "1", "2003-01", "2007-09",
   [("1.25 75", "MZR-1.3", 120), ("1.4 80", "MZR-1.4", 124), ("1.6 100", "MZR-1.6", 140), ("1.4 D 68", "DV4TD", 160)], portes=5, places=5, reservoir=45,
   remarques="Diesel PSA ; données indicatives")
mg(L, "Mazda2", "DE", "1", "2007-10", "2014-12",
   [("1.3 75", "MZR-1.3", 120), ("1.3 86", "MZR-1.3", 122), ("1.5 103", "MZR-1.5", 137), ("1.4 D 68", "DV4TD", 160), ("1.6 D 95", "DV6TED4", 205, {"debut": "2010-06"})],
   portes=5, places=5, reservoir=43, remarques="Restylage 2010")
mg(L, "Mazda2", "DJ", "1", "2014-12", "2020-03",
   [("1.5 Skyactiv-G 75", "SKY-G-1.5", 135), ("1.5 Skyactiv-G 90", "SKY-G-1.5", 148), ("1.5 Skyactiv-G 115", "SKY-G-1.5", 148), ("1.5 Skyactiv-D 105", "SKY-D-1.5", 270, {"fin": "2018-12"})],
   portes=5, places=5, reservoir=44)
mg(L, "Mazda2", "DJ", "2", "2020-04", "2025-12",
   [("1.5 e-Skyactiv-G 75", "SKY-G-1.5-MHEV", 135), ("1.5 e-Skyactiv-G 90", "SKY-G-1.5-MHEV", 148), ("1.5 e-Skyactiv-G 115", "SKY-G-1.5-MHEV", 148)],
   portes=5, places=5, reservoir=44, remarques="Restylages 2020 et 2023 ; date de fin indicative")
mg(L, "Mazda2", "XP21", "1", "2022-04", None, [("Hybrid 1.5 116", "M15A-FXE", 141)], portes=5, places=5, reservoir=36, remarques="Mazda2 Hybrid : Toyota Yaris rebadgée")
mg(L, "Mazda3", "BK", "1", "2003-10", "2009-03",
   [("1.4 84", "MZR-1.4", 122), ("1.6 105", "MZR-1.6", 145), ("2.0 150", "MZR-2.0", 187), ("1.6 D 109", "DV6TED4", 240), ("2.0 D 143", "MZR-CD-2.0", 360)],
   portes=5, places=5, reservoir=55, remarques="5 portes et berline ; MPS dans Mazda Speed")
mg(L, "Mazda3", "BL", "1", "2009-04", "2013-08",
   [("1.6 105", "MZR-1.6", 145), ("2.0 150", "MZR-2.0", 187), ("1.6 D 115", "DV6C", 270), ("2.2 D 150", "MZR-CD-2.2", 360), ("2.2 D 185", "MZR-CD-2.2", 400)],
   portes=5, places=5, reservoir=55)
mg(L, "Mazda3", "BM", "1", "2013-09", "2019-02",
   [("1.5 Skyactiv-G 100", "SKY-G-1.5", 150), ("2.0 Skyactiv-G 120", "SKY-G-2.0", 210), ("2.0 Skyactiv-G 165", "SKY-G-2.0", 210),
    ("1.5 Skyactiv-D 105", "SKY-D-1.5", 270, {"debut": "2016-06"}), ("2.2 Skyactiv-D 150", "SKY-D-2.2", 380)], portes=5, places=5, reservoir=51, remarques="Restylage 2016")
mg(L, "Mazda3", "BP", "1", "2019-03", None,
   [("2.0 e-Skyactiv-G 122", "SKY-G-2.0-MHEV", 213, {"fin": "2024-12"}), ("2.0 e-Skyactiv-X 180", "SKY-X-2.0-MHEV", 224, {"fin": "2021-06"}),
    ("2.0 e-Skyactiv-X 186", "SKY-X-2.0-MHEV", 240, {"debut": "2021-07"}), ("2.5 e-Skyactiv-G 140", "SKY-G-2.5-MHEV", 238, {"debut": "2024-09"}),
    ("1.8 Skyactiv-D 116", "SKY-D-1.8", 270, {"fin": "2022-12"})], portes=5, places=5, reservoir=51, remarques="5 portes et berline")
mg(L, "Mazda6", "GG", "1", "2002-06", "2007-12",
   [("1.8 120", "MZR-1.8", 165), ("2.0 141", "MZR-2.0", 181), ("2.3 166", "MZR-2.3", 207), ("2.0 D 121", "MZR-CD-2.0", 310), ("2.0 D 143", "MZR-CD-2.0", 360, {"debut": "2005-06"})],
   portes=4, places=5, reservoir=64, remarques="Berline, 5 portes et break ; MPS dans Mazda Speed")
mg(L, "Mazda6", "GH", "1", "2008-01", "2012-12",
   [("1.8 120", "MZR-1.8", 165), ("2.0 147", "MZR-2.0", 184), ("2.5 170", "MZR-2.5", 226), ("2.0 D 140", "MZR-CD-2.0", 330, {"fin": "2009-06"}),
    ("2.2 D 163", "MZR-CD-2.2", 360, {"debut": "2009-07"}), ("2.2 D 185", "MZR-CD-2.2", 400, {"debut": "2009-07"})], portes=4, places=5, reservoir=64)
mg(L, "Mazda6", "GJ/GL", "1", "2012-11", "2024-06",
   [("2.0 Skyactiv-G 145", "SKY-G-2.0", 210), ("2.0 Skyactiv-G 165", "SKY-G-2.0", 210), ("2.5 Skyactiv-G 194", "SKY-G-2.5", 258, {"debut": "2014-01"}),
    ("2.2 Skyactiv-D 150", "SKY-D-2.2", 380), ("2.2 Skyactiv-D 175", "SKY-D-2.2", 420), ("2.2 Skyactiv-D 184", "SKY-D-2.2", 445, {"debut": "2018-06"})],
   portes=4, places=5, reservoir=62, remarques="Berline et break ; restylages 2015 et 2018 ; retirée d'Europe, date de fin indicative")
mg(L, "Mazda 6e", "EZ-6", "1", "2025-06", None, [("6e 258", "MAZDA-EV", 320, el(69)), ("6e Long Range 245", "MAZDA-EV", 320, el(80))], portes=5, places=5,
   reservoir=0, remarques="Berline électrique développée avec Changan ; données indicatives")
mg(L, "Mazda MX-5", "NA", "1", "1989-05", "1998-02", [("1.6 115", "MZ-B6-1.6", 136), ("1.6 90", "MZ-B6-1.6", 130, {"debut": "1994-01"}), ("1.8 131", "MZ-BP-1.8", 155, {"debut": "1994-01"})],
   portes=2, places=2, reservoir=45, remarques="Roadster à phares escamotables ; données indicatives")
mg(L, "Mazda MX-5", "NB", "1", "1998-03", "2005-09", [("1.6 110", "MZ-B6-1.6", 134), ("1.8 140", "MZ-BP-1.8", 160), ("1.8 146", "MZ-BP-1.8", 168, {"debut": "2001-01"})],
   portes=2, places=2, reservoir=48, remarques="Restylage 2001 ; Mazdaspeed dans Mazda Speed")
mg(L, "Mazda MX-5", "NC", "1", "2005-10", "2015-07", [("1.8 126", "MZR-1.8", 167), ("2.0 160", "MZR-2.0", 188)], portes=2, places=2, reservoir=50,
   remarques="Roadster et Roadster Coupé à toit rigide ; restylages 2008 et 2012")
mg(L, "Mazda MX-5", "ND", "1", "2015-07", None,
   [("1.5 Skyactiv-G 131", "SKY-G-1.5", 150), ("2.0 Skyactiv-G 160", "SKY-G-2.0", 200, {"fin": "2018-06"}), ("2.0 Skyactiv-G 184", "SKY-G-2.0", 205, {"debut": "2018-07"})],
   portes=2, places=2, reservoir=45, remarques="Roadster et RF ; restylage 2024")

# ---------------------------------------------------------------- SUV et électriques
mg(L, "Mazda CX-3", "DK", "1", "2015-06", "2022-12",
   [("2.0 Skyactiv-G 120", "SKY-G-2.0", 210), ("2.0 Skyactiv-G 150", "SKY-G-2.0", 204), ("1.5 Skyactiv-D 105", "SKY-D-1.5", 270, {"fin": "2018-06"}),
    ("1.8 Skyactiv-D 115", "SKY-D-1.8", 270, {"debut": "2018-07"})], reservoir=48, remarques="Restylage 2018")
mg(L, "Mazda CX-30", "DM", "1", "2019-09", None,
   [("2.0 e-Skyactiv-G 122", "SKY-G-2.0-MHEV", 213, {"fin": "2024-12"}), ("2.0 e-Skyactiv-X 180", "SKY-X-2.0-MHEV", 224, {"fin": "2021-06"}),
    ("2.0 e-Skyactiv-X 186", "SKY-X-2.0-MHEV", 240, {"debut": "2021-07"}), ("2.5 e-Skyactiv-G 140", "SKY-G-2.5-MHEV", 238, {"debut": "2024-09"}),
    ("1.8 Skyactiv-D 116", "SKY-D-1.8", 270, {"fin": "2022-12"})], reservoir=51)
mg(L, "Mazda CX-5", "KE", "1", "2012-03", "2017-03",
   [("2.0 Skyactiv-G 165", "SKY-G-2.0", 210), ("2.5 Skyactiv-G 192", "SKY-G-2.5", 256, {"debut": "2014-01"}), ("2.2 Skyactiv-D 150", "SKY-D-2.2", 380),
    ("2.2 Skyactiv-D 175", "SKY-D-2.2", 420)], reservoir=56, remarques="Restylage 2015")
mg(L, "Mazda CX-5", "KF", "1", "2017-04", "2025-12",
   [("2.0 Skyactiv-G 165", "SKY-G-2.0", 210), ("2.5 Skyactiv-G 194", "SKY-G-2.5", 258), ("2.2 Skyactiv-D 150", "SKY-D-2.2", 380), ("2.2 Skyactiv-D 175", "SKY-D-2.2", 420, {"fin": "2018-12"}),
    ("2.2 Skyactiv-D 184", "SKY-D-2.2", 445, {"debut": "2019-01"})], reservoir=56, remarques="Restylage 2022 ; 2.5 Turbo hors Europe ; date de fin indicative")
mg(L, "Mazda CX-5", "KG", "1", "2026-04", None, [("2.5 e-Skyactiv-G 141", "SKY-G-2.5-MHEV", 238)], reservoir=58,
   remarques="Troisième génération, micro-hybride 24 V ; hybride Skyactiv Z attendu ensuite")
mg(L, "Mazda CX-60", "KH", "1", "2022-06", None,
   [("e-Skyactiv PHEV 2.5 327", "SKY-PHEV-2.5", 500, {"batterie": 18}), ("e-Skyactiv-D 3.3 MHEV 200", "SKY-D-3.3-MHEV", 450, {"debut": "2023-03"}),
    ("e-Skyactiv-D 3.3 MHEV AWD 254", "SKY-D-3.3-MHEV", 550, {"debut": "2023-03"})], reservoir=58, remarques="Plateforme à moteur longitudinal ; couples système")
mg(L, "Mazda CX-80", "KL", "1", "2024-09", None,
   [("e-Skyactiv PHEV 2.5 327", "SKY-PHEV-2.5", 500, {"batterie": 18}), ("e-Skyactiv-D 3.3 MHEV AWD 254", "SKY-D-3.3-MHEV", 550)], places=7, reservoir=74,
   remarques="SUV 6 ou 7 places")
mg(L, "Mazda MX-30", "DR", "1", "2020-09", None,
   [("e-Skyactiv EV 145", "MAZDA-EV", 271, el(36)), ("e-Skyactiv R-EV 170", "R-8C-REV", 260, {"debut": "2023-06", "batterie": 18})], reservoir=0,
   remarques="Portes antagonistes ; R-EV hybride rechargeable de série avec moteur rotatif générateur")
mg(L, "Mazda CX-6e", "EZ-60", "1", "2026-06", None, [("CX-6e 258", "MAZDA-EV", 320, el(78))], reservoir=0,
   remarques="SUV électrique présenté au Salon de Bruxelles 2026 ; données et date indicatives")
mg(L, "Mazda CX-50", "CX-50", "1", "2022-03", None,
   [("2.5 190", "SKY-G-2.5", 252), ("2.5 Turbo 260", "SKY-G-2.5T", 434), ("2.5 Hybrid 222", "SKY-G-2.5-HEV", 221, {"debut": "2025-01"})], reservoir=56, remarques=NA)
mg(L, "Mazda CX-70", "KK", "1", "2024-03", None,
   [("3.3 Turbo MHEV 284", "SKY-G-3.3T-MHEV", 450), ("3.3 Turbo MHEV 345", "SKY-G-3.3T-MHEV", 500), ("PHEV 2.5 328", "SKY-PHEV-2.5", 500, {"batterie": 18})],
   reservoir=74, remarques=NA)
mg(L, "Mazda CX-90", "KK", "1", "2023-04", None,
   [("3.3 Turbo MHEV 284", "SKY-G-3.3T-MHEV", 450), ("3.3 Turbo MHEV 345", "SKY-G-3.3T-MHEV", 500), ("PHEV 2.5 328", "SKY-PHEV-2.5", 500, {"batterie": 18})],
   places=8, reservoir=74, remarques=NA)

# ---------------------------------------------------------------- Mazda Speed
LS = []
mg(LS, "Mazda3 MPS", "BK", "1", "2006-10", "2009-03", [("MPS 2.3 Turbo 260", "MZR-2.3T", 380)], portes=5, places=5, reservoir=60,
   remarques="Mazdaspeed3 en Amérique du Nord")
mg(LS, "Mazda3 MPS", "BL", "1", "2009-04", "2013-08", [("MPS 2.3 Turbo 260", "MZR-2.3T", 380)], portes=5, places=5, reservoir=60)
mg(LS, "Mazda6 MPS", "GG", "1", "2005-06", "2007-12", [("MPS 2.3 Turbo AWD 260", "MZR-2.3T", 380)], portes=4, places=5, reservoir=60,
   remarques="Mazdaspeed6 en Amérique du Nord")
mg(LS, "MX-5 Mazdaspeed", "NB", "1", "2004-01", "2005-09", [("1.8 Turbo 180", "MZ-BP-1.8T", 226)], portes=2, places=2, reservoir=48,
   remarques="Marché nord-américain (hp convertis en ch) ; Roadster Turbo au Japon")

MOT = Motorisations("Mazda", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LS)

DETAIL = {"Mazda": L, "Mazda Speed": LS}
MOTEURS = MOT.moteurs()
