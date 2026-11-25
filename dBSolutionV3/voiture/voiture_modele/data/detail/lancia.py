"""Lancia : générations, phases, motorisations (marché européen) et moteurs liés.
Lancia : Lambda, Augusta, Aprilia, Ardea, Aurelia, Appia, Flaminia, Flavia/2000, Fulvia, Beta, Gamma (1976 et 2026), Delta
(I, II, III), Prisma, Y10, Thema (1984 et 2011), Dedra, Kappa, Hyena, Ypsilon (840, 843, 846, 2024), Lybra, Thesis, Phedra, Musa,
Voyager, Flavia (2012). Lancia HF : Fulvia HF, Stratos HF, 037 Rally, Delta HF Turbo, Delta S4, Delta HF 4WD et Integrale,
Ypsilon HF, Gamma HF Integrale.
Moteurs Lancia au motoriste « Lancia » ; moteurs Fiat/Alfa Romeo (Fiat), Chrysler, Peugeot et Ferrari repris des modules
correspondants avec leurs codes. Données des modèles anciens indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .alfa_romeo import FAMILLES as FAMILLES_ALFA
from .chrysler import FAMILLES as FAMILLES_CHRYSLER
from .fiat import FAMILLES as FAMILLES_FIAT
from .peugeot import FAMILLES as FAMILLES_PEUGEOT

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

PROPRES = {
    # V4 et V6 Lancia
    "LANCIA-V4-2.1": f("ATM", E_, 2.1, C, 4, 3250, 2000, "20W50", 5.0, 3000, a="V"),
    "LANCIA-V4-1.2": f("ATM", E_, 1.2, C, 4, 4000, 2500, "20W50", 4.0, 3000, a="V"),
    "LANCIA-V4-1.4": f("ATM", E_, 1.4, C, 4, 4300, 2700, "20W50", 4.0, 3000, a="V"),
    "LANCIA-V4-0.9": f("ATM", E_, 0.9, C, 4, 4600, 2800, "20W50", 3.5, 3000, a="V"),
    "LANCIA-V4-1.1": f("ATM", E_, 1.1, C, 4, 4800, 3000, "20W50", 3.5, 5000, a="V"),
    "FULVIA-V4-1.2": f("ATM", E_, 1.2, C, 4, 6000, 4500, "20W50", 4.0, 5000, a="V"),
    "FULVIA-V4-1.3": f("ATM", E_, 1.3, C, 4, 6000, 5000, "20W50", 4.0, 5000, a="V"),
    "FULVIA-V4-1.6": f("ATM", E_, 1.6, C, 4, 6200, 4500, "20W50", 4.0, 5000, a="V"),
    "AURELIA-V6-2.0": f("ATM", E_, 2.0, C, 6, 5000, 3500, "20W50", 6.0, 3000, a="V"),
    "AURELIA-V6-2.5": f("ATM", E_, 2.5, C, 6, 5000, 3500, "20W50", 6.0, 3000, a="V"),
    "FLAMINIA-V6-2.5": f("ATM", E_, 2.5, C, 6, 5400, 3500, "20W50", 6.5, 5000, a="V"),
    "FLAMINIA-V6-2.8": f("ATM", E_, 2.8, C, 6, 5400, 3500, "20W50", 6.5, 5000, a="V"),
    # flat-4
    "FLAVIA-B4-1.5": f("ATM", E_, 1.5, C, 4, 5200, 3000, "20W50", 4.5, 5000, a="PLAT"),
    "FLAVIA-B4-1.8": f("ATM", E_, 1.8, C, 4, 5200, 3500, "20W50", 4.5, 5000, a="PLAT"),
    "FLAVIA-B4-2.0": f("ATM", E_, 2.0, C, 4, 5400, 3500, "20W50", 4.5, 5000, a="PLAT"),
    "GAMMA-B4-2.0": f("ATM", E_, 2.0, B, 4, 5500, 3500, "10W40", 5.0, 10000, a="PLAT"),
    "GAMMA-B4-2.5": f("ATM", E_, 2.5, B, 4, 5400, 3000, "10W40", 5.0, 10000, a="PLAT"),
    # Fiat Twin Cam (versions Lancia)
    "FTC-1.3": f("ATM", E_, 1.3, B, 4, 6000, 3300, "10W40", 4.0, 10000),
    "FTC-1.5": f("ATM", E_, 1.5, B, 4, 5800, 3500, "10W40", 4.0, 10000),
    "FTC-1.8": f("ATM", E_, 1.8, B, 4, 6000, 4000, "10W40", 4.0, 10000),
    "FTC-2.0SC": f("TURBO", E_, 2.0, B, 4, 5500, 3500, "10W40", 4.5, 10000),
    "FTC-1.6T": f("TURBO", E_, 1.6, B, 4, 5500, 3700, "10W40", 4.0, 10000),
    "FTC-2.0T-16V": f("TURBO", E_, 2.0, B, 4, 5750, 3000, "10W40", 5.0, 10000),
    "LANCIA-1.8-S4": f("TURBO", E_, 1.8, B, 4, 6750, 4500, "10W60", 6.0, 5000),
    "FTC-2.0SC-037": f("TURBO", E_, 2.0, B, 4, 7000, 5000, "10W60", 6.0, 5000),
    # moteurs d'emprunt sans famille ailleurs
    "PRV-2.8": f("ATM", E_, 2.8, C, 6, 5750, 3000, "15W40", 5.5, 10000, a="V"),
    "FERRARI-F105L-2.9": f("ATM", E_, 2.9, B, 8, 6750, 4500, "10W60", 9.0, 10000, a="V"),
    "DINO-V6-2.4": f("ATM", E_, 2.4, C, 6, 7000, 4000, "20W50", 8.0, 5000, a="V"),
    "PSA-ES9-3.0": f("ATM", E_, 3.0, B, 6, 6000, 3750, "5W40", 5.0, 20000, a="V"),
}
FIAT = {**{k: FAMILLES_FIAT[k] for k in ("FTC-1.4", "FTC-1.6", "FTC-2.0", "FTC-2.0T", "TWINCAM-1.6", "TWINCAM-1.8", "PRATOLA-2.0-20V",
                                        "PRATOLA-2.0-20VT", "PRATOLA-2.4-20V", "FIRE-1.0", "FIRE-1.1", "FIRE-1.2", "FIRE-1.2-16V", "FIRE-1.4",
                                        "FIRE-1.4-16V", "F128-1.3T", "TJET-1.4", "TWINAIR-0.9", "FIREFLY-1.0-HYB", "TD-1.9", "TD-2.5", "JTD-1.9",
                                        "JTD-2.4", "MJ-1.3", "MJ-1.6", "MJ-2.0", "EB2", "EB2-MHEV", "e-CMP")},
        **{k: FAMILLES_ALFA[k] for k in ("BUSSO-3.0", "BUSSO-3.0-24V", "BUSSO-3.2-24V", "TBI-1.75")}}
CHRYSLER = {k: FAMILLES_CHRYSLER[k] for k in ("PENTASTAR-3.6", "VM-2.8CRD", "VM-3.0CRD", "WORLD-2.4")}
PEUGEOT = {k: FAMILLES_PEUGEOT[k] for k in ("EW10J4", "DW10TD", "DW10C", "DW12C", "STLA-M")}
FAMILLES = {**PROPRES, **FIAT, **CHRYSLER, **PEUGEOT}


def motoriste(fam):
    if fam in FIAT:
        return "Fiat" if fam not in ("BUSSO-3.0", "BUSSO-3.0-24V", "BUSSO-3.2-24V", "TBI-1.75") else "Alfa Romeo"
    if fam in CHRYSLER:
        return "Chrysler"
    if fam in PEUGEOT or fam in ("PRV-2.8", "PSA-ES9-3.0"):
        return "Peugeot"
    if fam in ("FERRARI-F105L-2.9", "DINO-V6-2.4"):
        return "Ferrari"
    return "Lancia"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Lancia", motoriste)
L = []

# ---------------------------------------------------------------- avant-guerre et années 1950
mg(L, "Lambda", "Lambda", "1", "1922-11", "1931-12", [("2.1 V4 50", "LANCIA-V4-2.1", 120)], portes=4, places=4, reservoir=60,
   remarques="Caisse autoporteuse et suspension avant indépendante ; 2,1 l puis 2,4 et 2,6 l ; données indicatives")
mg(L, "Augusta", "Augusta", "1", "1933-01", "1936-12", [("1.2 V4 35", "LANCIA-V4-1.2", 75)], portes=4, places=4, reservoir=40, remarques="Données indicatives")
mg(L, "Aprilia", "Aprilia", "1", "1937-02", "1949-12", [("1.35 V4 48", "LANCIA-V4-1.4", 88)], portes=4, places=4, reservoir=50,
   remarques="1,35 l puis 1,5 l (1939) ; données indicatives")
mg(L, "Ardea", "Ardea", "1", "1939-01", "1953-12", [("0.9 V4 29", "LANCIA-V4-0.9", 54)], portes=4, places=4, reservoir=33, remarques="Données indicatives")
mg(L, "Aurelia", "B10-B20", "1", "1950-05", "1958-12",
   [("B10 2.0 V6 56", "AURELIA-V6-2.0", 122, {"fin": "1953-12"}), ("B20 GT 2.5 V6 118", "AURELIA-V6-2.5", 182, {"debut": "1953-01"})], portes=4, places=4,
   reservoir=50, remarques="Premier V6 de série ; berline, coupé B20 GT, spider B24 ; données indicatives")
mg(L, "Appia", "Appia", "1", "1953-04", "1963-12", [("1.1 V4 38", "LANCIA-V4-1.1", 74)], portes=4, places=4, reservoir=38, remarques="Données indicatives")
mg(L, "Flaminia", "Flaminia", "1", "1957-04", "1970-12",
   [("2.5 V6 102", "FLAMINIA-V6-2.5", 186, {"fin": "1962-12"}), ("2.8 V6 129", "FLAMINIA-V6-2.8", 220, {"debut": "1963-01"})], portes=4, places=5,
   reservoir=57, remarques="Berline, coupé Pininfarina, GT Touring, Sport Zagato ; données indicatives")
mg(L, "Flavia", "Flavia", "1", "1961-01", "1974-12",
   [("1.5 78", "FLAVIA-B4-1.5", 113, {"fin": "1966-12"}), ("1.8 92", "FLAVIA-B4-1.8", 147, {"debut": "1963-01", "fin": "1970-12"}),
    ("2.0 115", "FLAVIA-B4-2.0", 172, {"debut": "1969-01"})], portes=4, places=5, reservoir=48,
   remarques="Traction avant, flat-4 ; devenue Lancia 2000 (1971-1974) ; données indicatives")
mg(L, "Fulvia", "Fulvia", "1", "1963-12", "1976-06",
   [("1.1 V4 58", "LANCIA-V4-1.1", 87, {"fin": "1969-12"}), ("Coupé 1.2 V4 80", "FULVIA-V4-1.2", 102, {"debut": "1965-03", "fin": "1967-12"}),
    ("1.3 V4 87", "FULVIA-V4-1.3", 114, {"debut": "1967-01"})], portes=4, places=4, reservoir=38,
   remarques="Berline, coupé et Sport Zagato ; versions HF dans Lancia HF ; données indicatives")

# ---------------------------------------------------------------- années 1970-1980
mg(L, "Beta", "828", "1", "1972-11", "1984-12",
   [("1.3 82", "FTC-1.3", 107, {"debut": "1975-01"}), ("1.4 90", "FTC-1.4", 115, {"fin": "1975-12"}), ("1.6 100", "FTC-1.6", 132, {"debut": "1975-01"}),
    ("1.8 110", "FTC-1.8", 147, {"fin": "1975-12"}), ("2.0 119", "FTC-2.0", 176, {"debut": "1975-01"}), ("VX 2.0 Volumex 135", "FTC-2.0SC", 206, {"debut": "1983-01"})],
   portes=4, places=5, reservoir=50, remarques="Berline, Coupé, HPE, Spider, Montecarlo (2.0, 1975-1981) ; données indicatives")
mg(L, "Gamma", "830", "1", "1976-10", "1984-12", [("2.0 115", "GAMMA-B4-2.0", 172, {"debut": "1977-01"}), ("2.5 140", "GAMMA-B4-2.5", 208)], portes=4,
   places=5, reservoir=63, remarques="Berline et coupé Pininfarina, flat-4 ; données indicatives")
mg(L, "Delta", "831", "1", "1979-09", "1994-02",
   [("1.3 75", "FTC-1.3", 106, {"fin": "1986-06"}), ("1.5 85", "FTC-1.5", 123, {"fin": "1986-06"}), ("1.6 GT 105", "FTC-1.6", 136, {"debut": "1982-01"}),
    ("1.9 TD 80", "TD-1.9", 172, {"debut": "1986-06"})], reservoir=45, remarques="Voiture européenne de l'année 1980 ; versions HF dans Lancia HF ; données indicatives")
mg(L, "Prisma", "831 AB", "1", "1982-12", "1989-12",
   [("1.3 78", "FTC-1.3", 106), ("1.5 85", "FTC-1.5", 123), ("1.6 105", "FTC-1.6", 136, {"debut": "1984-01"}), ("1.9 TD 80", "TD-1.9", 172, {"debut": "1986-06"})],
   portes=4, places=5, reservoir=45, remarques="Version tricorps de la Delta ; Prisma 4WD (1986) ; données indicatives")
mg(L, "Y10", "156", "1", "1985-03", "1995-12",
   [("Fire 1.0 45", "FIRE-1.0", 80), ("1.1 i.e. 56", "FIRE-1.1", 86, {"debut": "1989-01"}), ("Turbo 1.05 85", "F128-1.3T", 118, {"fin": "1989-12"}),
    ("GT i.e. 1.3 78", "FIRE-1.4", 105, {"debut": "1989-01"})], portes=3, places=4, reservoir=47,
   remarques="Autobianchi Y10 en Italie ; Y10 4WD ; données indicatives (1.3 rattaché à la famille 1.4 Fire)")
mg(L, "Thema", "834", "1", "1984-10", "1994-06",
   [("2.0 i.e. 120", "FTC-2.0", 167), ("2.0 Turbo 165", "FTC-2.0T", 285), ("2.8 V6 150", "PRV-2.8", 230, {"fin": "1992-12"}),
    ("8.32 2.9 V8 215", "FERRARI-F105L-2.9", 285, {"debut": "1986-12", "fin": "1992-12"}), ("2.5 TD 118", "TD-2.5", 255),
    ("3.0 V6 175", "BUSSO-3.0", 245, {"debut": "1992-06"})], portes=4, places=5, reservoir=70,
   remarques="Berline et break (1986) ; Thema 8.32 à V8 Ferrari ; données indicatives")

# ---------------------------------------------------------------- années 1990-2000
mg(L, "Dedra", "835", "1", "1989-04", "1999-12",
   [("1.6 90", "FTC-1.6", 128), ("1.8 i.e. 105", "FTC-1.8", 150), ("2.0 i.e. 113", "FTC-2.0", 162), ("2.0 Turbo 162", "FTC-2.0T", 270, {"debut": "1990-06"}),
    ("1.9 TD 90", "TD-1.9", 186)], portes=4, places=5, reservoir=63, remarques="Berline et SW (1994) ; données indicatives")
mg(L, "Delta", "836", "1", "1993-10", "1999-12",
   [("1.6 75", "FTC-1.6", 127), ("1.8 16V 113", "TWINCAM-1.8", 154, {"debut": "1996-01"}), ("HF Turbo 2.0 186", "FTC-2.0T", 290),
    ("1.9 TD 90", "TD-1.9", 186)], reservoir=63, remarques="Nouvelle Delta (base Fiat Tipo) ; données indicatives")
mg(L, "Kappa", "838", "1", "1994-09", "2001-10",
   [("2.0 20V 146", "PRATOLA-2.0-20V", 186), ("2.0 20V Turbo 205", "PRATOLA-2.0-20VT", 300), ("2.4 20V 175", "PRATOLA-2.4-20V", 221),
    ("3.0 V6 204", "BUSSO-3.0-24V", 263), ("2.4 TDS 124", "TD-2.5", 260, {"fin": "1997-12"}), ("2.4 JTD 136", "JTD-2.4", 304, {"debut": "1997-09"})],
   portes=4, places=5, reservoir=70, remarques="Berline, coupé (1997) et SW (1996)")
mg(L, "Hyena", "Hyena", "1", "1992-10", "1993-12", [("2.0 16V Turbo 250", "FTC-2.0T-16V", 314)], portes=2, places=2, reservoir=57,
   remarques="Coupé Zagato sur base Delta HF Integrale, 24 exemplaires ; données indicatives")
mg(L, "Ypsilon", "840", "1", "1995-10", "2003-08",
   [("1.1 54", "FIRE-1.1", 86), ("1.2 60", "FIRE-1.2", 102), ("1.2 16V 86", "FIRE-1.2-16V", 113, {"debut": "1997-01"}), ("1.4 12V 80", "FIRE-1.4", 112, {"fin": "2000-12"})],
   portes=3, places=4, reservoir=47, remarques="« Y » ; restylage 2000")
mg(L, "Lybra", "839", "1", "1999-07", "2005-10",
   [("1.6 16V 103", "TWINCAM-1.6", 144), ("1.8 16V 131", "TWINCAM-1.8", 164), ("2.0 20V 150", "PRATOLA-2.0-20V", 186), ("1.9 JTD 105", "JTD-1.9", 255),
    ("1.9 JTD 115", "JTD-1.9", 255), ("2.4 JTD 136", "JTD-2.4", 304), ("2.4 JTD 150", "JTD-2.4", 310, {"debut": "2002-06"})], portes=4, places=5,
   reservoir=63, remarques="Berline et SW")
mg(L, "Thesis", "841", "1", "2002-06", "2009-07",
   [("2.0 20V Turbo 185", "PRATOLA-2.0-20VT", 265), ("2.4 20V 170", "PRATOLA-2.4-20V", 221), ("3.0 V6 215", "BUSSO-3.0-24V", 263),
    ("3.2 V6 230", "BUSSO-3.2-24V", 289), ("2.4 JTD 150", "JTD-2.4", 310), ("2.4 Multijet 175", "JTD-2.4", 385, {"debut": "2003-06"}),
    ("2.4 Multijet 185", "JTD-2.4", 385, {"debut": "2006-06"})], portes=4, places=5, reservoir=75)
mg(L, "Phedra", "179", "1", "2002-06", "2010-12",
   [("2.0 16V 136", "EW10J4", 190), ("3.0 V6 204", "PSA-ES9-3.0", 285), ("2.0 JTD 109", "DW10TD", 250), ("2.0 JTD 136", "DW10C", 320, {"debut": "2006-06"}),
    ("2.2 JTD 128", "DW12C", 314), ("2.2 Multijet 170", "DW12C", 370, {"debut": "2006-06"})], places=7, reservoir=80,
   remarques="Monospace Eurovan (moteurs PSA)")
mg(L, "Ypsilon", "843", "1", "2003-09", "2011-06",
   [("1.2 60", "FIRE-1.2", 102), ("1.4 77", "FIRE-1.4", 115), ("1.4 16V 95", "FIRE-1.4-16V", 128), ("1.3 Multijet 70", "MJ-1.3", 180),
    ("1.3 Multijet 90", "MJ-1.3", 200, {"debut": "2006-06"})], portes=3, places=4, reservoir=47, remarques="Restylage 2006")
mg(L, "Musa", "350", "1", "2004-10", "2012-09",
   [("1.4 77", "FIRE-1.4", 115), ("1.4 16V 95", "FIRE-1.4-16V", 128), ("1.3 Multijet 70", "MJ-1.3", 180), ("1.3 Multijet 90", "MJ-1.3", 200),
    ("1.9 Multijet 100", "JTD-1.9", 200, {"fin": "2007-12"}), ("1.6 Multijet 120", "MJ-1.6", 300, {"debut": "2008-01"})], reservoir=47,
   remarques="Monospace (base Fiat Idea) ; restylage 2007")
mg(L, "Delta", "844", "1", "2008-06", "2014-08",
   [("1.4 T-Jet 120", "TJET-1.4", 206), ("1.4 T-Jet 150", "TJET-1.4", 230), ("1.8 Di TBi 200", "TBI-1.75", 320, {"debut": "2009-06"}),
    ("1.6 Multijet 120", "MJ-1.6", 300), ("1.9 Multijet Twin Turbo 190", "JTD-1.9", 400), ("2.0 Multijet 165", "MJ-2.0", 360, {"debut": "2010-06"})],
   reservoir=57, remarques="Vendue aussi sous le nom Chrysler Delta au Royaume-Uni")
mg(L, "Ypsilon", "846", "1", "2011-06", "2024-03",
   [("1.2 69", "FIRE-1.2", 102), ("0.9 TwinAir 85", "TWINAIR-0.9", 145), ("1.3 Multijet 95", "MJ-1.3", 200, {"fin": "2018-12"}),
    ("1.0 Hybrid 70", "FIREFLY-1.0-HYB", 92, {"debut": "2020-01"})], portes=5, places=4, reservoir=40,
   remarques="Vendue en Italie seule à partir de 2017 ; restylages 2015 et 2021")
mg(L, "Thema", "LX", "1", "2011-09", "2014-12", [("3.0 V6 Multijet 190", "VM-3.0CRD", 440), ("3.0 V6 Multijet 239", "VM-3.0CRD", 550), ("3.6 V6 286", "PENTASTAR-3.6", 340)],
   portes=4, places=5, reservoir=72, remarques="Chrysler 300 rebadgée")
mg(L, "Voyager", "RT", "1", "2011-09", "2015-12", [("2.8 CRD 163", "VM-2.8CRD", 360), ("2.8 CRD 178", "VM-2.8CRD", 360, {"debut": "2013-01"}),
                                                  ("3.6 V6 283", "PENTASTAR-3.6", 353)], places=7, reservoir=76, remarques="Chrysler Grand Voyager rebadgé")
mg(L, "Flavia", "JS", "1", "2012-03", "2014-12", [("2.4 170", "WORLD-2.4", 220)], portes=2, places=4, reservoir=64, remarques="Cabriolet, Chrysler 200 rebadgé")

# ---------------------------------------------------------------- renouveau
mg(L, "Ypsilon", "V5", "1", "2024-03", None,
   [("Elettrica 156", "e-CMP", 260, el(51)), ("Hybrid 1.2 100", "EB2-MHEV", 205, {"debut": "2024-09", "fin": "2025-06"}),
    ("HF Line Hybrid 1.2 110", "EB2-MHEV", 205, {"debut": "2025-06"})], portes=5, places=5, reservoir=44,
   remarques="Plateforme e-CMP ; version HF électrique dans Lancia HF")
mg(L, "Gamma", "STLA M", "1", "2026-10", None,
   [("LX Hybrid 1.2 145", "EB2-MHEV", 230), ("LX Elettrica 230", "STLA-M", 345, el(97))], reservoir=55,
   remarques="Berline-SUV de 4,67 m sur STLA Medium produite à Melfi ; commandes ouvertes en octobre 2026 ; versions intermédiaires et données indicatives")

# ---------------------------------------------------------------- Lancia HF
LH = []
mg(LH, "Fulvia HF", "Fulvia", "1", "1966-03", "1969-12",
   [("Coupé HF 1.2 V4 88", "FULVIA-V4-1.2", 108, {"fin": "1967-12"}), ("Coupé HF 1.3 V4 101", "FULVIA-V4-1.3", 114, {"debut": "1967-01"})], portes=2, places=4,
   reservoir=38, remarques="Coupé allégé ; données indicatives")
mg(LH, "Fulvia HF 1.6", "Fulvia", "1", "1969-01", "1972-12", [("HF 1.6 V4 115", "FULVIA-V4-1.6", 157)], portes=2, places=4, reservoir=38,
   remarques="« Fanalone » ; championne du monde des rallyes 1972 ; données indicatives")
mg(LH, "Stratos HF", "Stratos", "1", "1973-10", "1978-12", [("Stradale 2.4 V6 190", "DINO-V6-2.4", 226)], portes=2, places=2, reservoir=80,
   remarques="Version route d'homologation (environ 492 exemplaires), V6 Ferrari Dino ; données indicatives")
mg(LH, "Stratos HF Rally", "Stratos", "1", "1974-01", "1978-12", [("Rallye 2.4 V6 280", "DINO-V6-2.4", 280)], portes=2, places=2, reservoir=80,
   remarques="Voiture de rallye Groupe 4 non homologuée route ; données indicatives")
mg(LH, "037 Rally", "037", "1", "1982-04", "1983-12", [("Stradale 2.0 Volumex 205", "FTC-2.0SC-037", 226)], portes=2, places=2, reservoir=70,
   remarques="Version route d'homologation Groupe B (environ 200 exemplaires) ; données indicatives")
mg(LH, "Delta HF Turbo", "831", "1", "1983-01", "1992-12", [("HF Turbo 1.6 130", "FTC-1.6T", 191, {"fin": "1986-06"}), ("HF Turbo i.e. 1.6 140", "FTC-1.6T", 191, {"debut": "1986-06"})],
   reservoir=45, remarques="Données indicatives")
mg(LH, "Delta S4", "S4", "1", "1985-11", "1986-12", [("Stradale 1.8 Turbo-Compresseur 250", "LANCIA-1.8-S4", 291)], portes=3, places=2, reservoir=70,
   remarques="Version route d'homologation Groupe B (environ 200 exemplaires) ; données indicatives")
mg(LH, "Delta HF 4WD", "831", "1", "1986-06", "1987-12", [("HF 4WD 2.0 Turbo 165", "FTC-2.0T", 285)], reservoir=45, remarques="Données indicatives")
mg(LH, "Delta HF Integrale", "831", "1", "1987-11", "1989-12", [("Integrale 8V 2.0 Turbo 185", "FTC-2.0T", 304)], reservoir=45,
   remarques="Six titres constructeurs WRC (1987-1992) ; données indicatives")
mg(LH, "Delta HF Integrale 16V", "831", "1", "1989-05", "1991-12", [("Integrale 16V 2.0 Turbo 200", "FTC-2.0T-16V", 298)], reservoir=45, remarques="Données indicatives")
mg(LH, "Delta HF Integrale", "831", "2", "1991-10", "1994-12",
   [("Evoluzione 2.0 16V Turbo 210", "FTC-2.0T-16V", 300), ("Evoluzione II 2.0 16V Turbo 215", "FTC-2.0T-16V", 314, {"debut": "1993-06"})], reservoir=45,
   remarques="Evoluzione et Evoluzione II ; données indicatives")
mg(LH, "Ypsilon HF", "V5", "1", "2025-09", None, [("HF Elettrica 280", "e-CMP", 345, el(54))], portes=5, places=5, reservoir=0,
   remarques="Différentiel Torsen, freins Alcon")
mg(LH, "Gamma HF Integrale", "STLA M", "1", "2026-10", None, [("HF Integrale AWD 375", "STLA-M", 577, el(97))], reservoir=0,
   remarques="Électrique bimoteur ; commandes ouvertes en octobre 2026 ; couple et batterie indicatifs")

MOT = Motorisations("Lancia", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LH)

DETAIL = {"Lancia": L, "Lancia HF": LH}
MOTEURS = MOT.moteurs()
