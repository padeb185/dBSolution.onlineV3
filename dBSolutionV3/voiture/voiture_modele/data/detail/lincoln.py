"""Lincoln : générations, phases, motorisations (marché nord-américain, hp convertis en ch ×1,014) et moteurs liés.
Model L, Model K, Zephyr (1936), Continental, Cosmopolitan, Capri, Premiere, Mark III, Mark V, Versailles, Mark VII, Mark VIII,
Town Car, LS, Blackwood, Navigator, Aviator, Zephyr/MKZ, MKC, MKX/Nautilus, Corsair.
Moteurs Ford repris de ford.py et ginetta.py (motoriste « Ford », mêmes codes) ; V8 et V12 anciens au motoriste « Lincoln » ;
V8 3.9 de la LS au motoriste « Jaguar ». Données anciennes indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .ford import FAMILLES as FAMILLES_FORD
from .ginetta import FAMILLES as FAMILLES_GINETTA

E_ = "ESS"
C = "CHAINE"

LINCOLN = {
    "LINCOLN-V8-5.9": f("ATM", E_, 5.9, C, 8, 2800, 1400, "20W50", 7.0, 3000, a="V"),
    "LINCOLN-V8-6.3": f("ATM", E_, 6.3, C, 8, 3400, 1600, "20W50", 7.0, 3000, a="V"),
    "LINCOLN-V12-7.3": f("ATM", E_, 7.3, C, 12, 3400, 1600, "20W50", 8.0, 3000, a="V"),
    "LINCOLN-V12-4.4": f("ATM", E_, 4.4, C, 12, 3900, 2000, "20W50", 7.0, 3000, a="V"),
    "LINCOLN-V12-4.8": f("ATM", E_, 4.8, C, 12, 3600, 2000, "20W50", 7.0, 3000, a="V"),
    "LINCOLN-V8-5.5": f("ATM", E_, 5.5, C, 8, 3600, 2000, "20W50", 5.7, 3000, a="V"),
    "LINCOLN-Y-5.2": f("ATM", E_, 5.2, C, 8, 4400, 2600, "20W50", 5.7, 3000, a="V"),
    "LINCOLN-Y-6.0": f("ATM", E_, 6.0, C, 8, 4600, 3000, "20W50", 5.7, 3000, a="V"),
    "FORD-MEL-7.0": f("ATM", E_, 7.0, C, 8, 4600, 3100, "20W50", 5.7, 3000, a="V"),
    "FORD-MEL-7.6": f("ATM", E_, 7.6, C, 8, 4600, 2800, "20W50", 5.7, 3000, a="V"),
    "FORD-385-7.5": f("ATM", E_, 7.5, C, 8, 4600, 2800, "20W50", 5.7, 5000, a="V"),
    "FORD-335-6.6": f("ATM", E_, 6.6, C, 8, 3600, 1800, "10W40", 5.7, 5000, a="V"),
    "FORD-WINDSOR-5.8": f("ATM", E_, 5.8, C, 8, 3200, 1600, "10W40", 4.7, 5000, a="V"),
    "FORD-WINDSOR-5.0": f("ATM", E_, 5.0, C, 8, 4200, 2000, "10W40", 4.7, 5000, a="V"),
    "MODULAR-4.6": f("ATM", E_, 4.6, C, 8, 4750, 3500, "5W20", 5.7, 8000, a="V"),
    "MODULAR-4.6-DOHC": f("ATM", E_, 4.6, C, 8, 5750, 4500, "5W30", 5.7, 8000, a="V"),
    "MODULAR-5.4": f("ATM", E_, 5.4, C, 8, 5000, 3750, "5W20", 6.6, 8000, a="V"),
    "ECOBOOST-V6-3.0-PHEV": f("HYB_E", E_, 3.0, C, 6, 5500, 3000, "5W30", 5.7, 10000, a="V"),
    "ECOBOOST-2.0-HEV": f("HYB_TE", E_, 2.0, C, 4, 5500, 3000, "5W30", 5.4, 10000),
}
JAGUAR = {"AJ-V8-3.9": f("ATM", E_, 3.9, C, 8, 6100, 4300, "5W30", 6.0, 8000, a="V")}
FORD = {**{k: FAMILLES_FORD[k] for k in ("DURATEC-V6-3.0", "DURATEC-2.5-HEV", "DURATEC-2.5-PHEV", "ECOBOOST-2.0", "ECOBOOST-2.3", "ECOBOOST-V6-2.7",
                                         "ECOBOOST-V6-3.0", "ECOBOOST-V6-3.5")},
        **{k: FAMILLES_GINETTA[k] for k in ("CYCLONE-3.5", "CYCLONE-3.7")}}
FAMILLES = {**LINCOLN, **JAGUAR, **FORD}


def motoriste(fam):
    return "Ford" if fam in FORD else ("Jaguar" if fam in JAGUAR else "Lincoln")


NA = "Marché nord-américain (hp convertis en ch)"
mg = SaisieMoteurs(FAMILLES, "Lincoln", motoriste)
L = []

# ---------------------------------------------------------------- avant-guerre et années 1950
mg(L, "Model L Series", "Model L", "1", "1920-09", "1930-12", [("5.9 V8 82", "LINCOLN-V8-5.9", 271)], portes=4, places=5, reservoir=80,
   remarques=NA + " ; données indicatives")
mg(L, "Model K Series", "Model K", "1", "1931-01", "1940-12",
   [("6.3 V8 122", "LINCOLN-V8-6.3", 312, {"fin": "1932-12"}), ("7.3 V12 152", "LINCOLN-V12-7.3", 397)], portes=4, places=5, reservoir=95,
   remarques=NA + " ; données indicatives")
mg(L, "Zephyr", "Zephyr", "1", "1935-11", "1942-02", [("4.4 V12 112", "LINCOLN-V12-4.4", 244)], portes=4, places=5, reservoir=72, remarques=NA + " ; données indicatives")
mg(L, "Continental", "Continental", "1", "1939-10", "1948-12", [("4.8 V12 132", "LINCOLN-V12-4.8", 271)], portes=2, places=5, reservoir=72,
   remarques=NA + " ; coupé et cabriolet ; données indicatives")
mg(L, "Cosmopolitan", "Cosmopolitan", "1", "1948-04", "1954-12", [("5.5 V8 154", "LINCOLN-V8-5.5", 359)], portes=4, places=5, reservoir=72,
   remarques=NA + " ; V8 à soupapes latérales puis 5.2 culbutés (1952) ; données indicatives")
mg(L, "Capri", "Capri", "1", "1952-01", "1955-12", [("5.2 V8 162", "LINCOLN-Y-5.2", 386, {"fin": "1953-12"}), ("5.2 V8 208", "LINCOLN-Y-5.2", 414, {"debut": "1954-01"})],
   portes=4, places=5, reservoir=76, remarques=NA + " ; données indicatives")
mg(L, "Capri", "Capri", "2", "1956-01", "1959-12", [("6.0 V8 289", "LINCOLN-Y-6.0", 549, {"fin": "1956-12"}), ("7.0 V8 304", "FORD-MEL-7.0", 637, {"debut": "1957-01"})],
   portes=4, places=5, reservoir=76, remarques=NA + " ; données indicatives")
mg(L, "Premiere", "Premiere", "1", "1956-01", "1960-12",
   [("6.0 V8 289", "LINCOLN-Y-6.0", 549, {"fin": "1956-12"}), ("7.0 V8 304", "FORD-MEL-7.0", 637, {"debut": "1957-01"})], portes=4, places=5, reservoir=76,
   remarques=NA + " ; données indicatives")
mg(L, "Continental", "1961", "1", "1961-01", "1969-12", [("7.0 V8 304", "FORD-MEL-7.0", 637, {"fin": "1965-12"}), ("7.6 V8 345", "FORD-MEL-7.6", 655, {"debut": "1966-01"})],
   portes=4, places=6, reservoir=91, remarques=NA + " ; portes antagonistes ; données indicatives")

# ---------------------------------------------------------------- années 1970-1990
mg(L, "Mark III", "Mark III", "1", "1968-04", "1971-12", [("7.5 V8 370", "FORD-385-7.5", 678)], portes=2, places=5, reservoir=95, remarques=NA + " ; données indicatives")
mg(L, "Mark V", "Mark V", "1", "1976-10", "1979-12", [("6.6 V8 182", "FORD-335-6.6", 400), ("7.5 V8 211", "FORD-385-7.5", 488, {"fin": "1978-12"})], portes=2, places=5,
   reservoir=91, remarques=NA + " ; 7.5 hors Californie jusqu'en 1978 ; données indicatives")
mg(L, "Versailles", "Versailles", "1", "1977-05", "1980-12", [("5.8 V8 137", "FORD-WINDSOR-5.8", 373, {"fin": "1979-12"}), ("5.0 V8 132", "FORD-WINDSOR-5.0", 312, {"debut": "1980-01"})],
   portes=4, places=5, reservoir=73, remarques=NA + " ; données indicatives")
mg(L, "Mark VII", "Mark VII", "1", "1983-10", "1992-12", [("5.0 V8 142", "FORD-WINDSOR-5.0", 339, {"fin": "1985-12"}), ("LSC 5.0 V8 HO 228", "FORD-WINDSOR-5.0", 407, {"debut": "1986-01"})],
   portes=2, places=5, reservoir=83, remarques=NA + " ; 2.4 turbodiesel BMW (1984-1985) non repris ; données indicatives")
mg(L, "Mark VIII", "Mark VIII", "1", "1992-10", "1998-12", [("4.6 V8 DOHC 284", "MODULAR-4.6-DOHC", 386), ("LSC 4.6 V8 DOHC 294", "MODULAR-4.6-DOHC", 393, {"debut": "1996-10"})],
   portes=2, places=5, reservoir=68, remarques=NA)
mg(L, "Town Car", "Panther", "1", "1980-10", "1989-12", [("5.0 V8 152", "FORD-WINDSOR-5.0", 366)], portes=4, places=6, reservoir=68, remarques=NA + " ; données indicatives")
mg(L, "Town Car", "Panther", "2", "1990-01", "1997-12", [("4.6 V8 193", "MODULAR-4.6", 373), ("4.6 V8 213", "MODULAR-4.6", 380)], portes=4, places=6, reservoir=76, remarques=NA)
mg(L, "Town Car", "Panther", "3", "1998-01", "2011-08", [("4.6 V8 203", "MODULAR-4.6", 386, {"fin": "2002-12"}), ("4.6 V8 223", "MODULAR-4.6", 393, {"fin": "2002-12"}),
                                                         ("4.6 V8 242", "MODULAR-4.6", 389, {"debut": "2003-01"})], portes=4, places=6, reservoir=72,
   remarques=NA + " ; empattement long Signature L")
mg(L, "LS", "DEW98", "1", "1999-06", "2006-04",
   [("3.0 V6 213", "DURATEC-V6-3.0", 278, {"fin": "2002-12"}), ("3.0 V6 235", "DURATEC-V6-3.0", 297, {"debut": "2003-01"}), ("3.9 V8 256", "AJ-V8-3.9", 362, {"fin": "2002-12"}),
    ("3.9 V8 284", "AJ-V8-3.9", 389, {"debut": "2003-01"})], portes=4, places=5, reservoir=68, remarques=NA + " ; plateforme partagée avec la Jaguar S-Type")
mg(L, "Blackwood", "Blackwood", "1", "2001-07", "2002-12", [("5.4 V8 304", "MODULAR-5.4", 482)], portes=4, places=5, reservoir=114, remarques=NA + " ; pick-up de luxe")

# ---------------------------------------------------------------- SUV
mg(L, "Navigator", "U173", "1", "1997-07", "2002-12",
   [("5.4 V8 233", "MODULAR-5.4", 441, {"fin": "1998-12"}), ("5.4 V8 264", "MODULAR-5.4", 468, {"debut": "1999-01", "fin": "2000-12"}),
    ("5.4 V8 DOHC 304", "MODULAR-5.4", 481, {"debut": "2001-01"})], places=7, reservoir=114, remarques=NA)
mg(L, "Navigator", "U228", "1", "2003-01", "2006-12", [("5.4 V8 304", "MODULAR-5.4", 481)], places=7, reservoir=106, remarques=NA)
mg(L, "Navigator", "U326", "1", "2007-01", "2017-06", [("5.4 V8 304", "MODULAR-5.4", 495, {"fin": "2014-12"}), ("3.5 V6 EcoBoost 385", "ECOBOOST-V6-3.5", 624, {"debut": "2015-01"})],
   places=8, reservoir=106, remarques=NA + " ; Navigator L")
mg(L, "Navigator", "U554", "1", "2017-10", None, [("3.5 V6 EcoBoost 456", "ECOBOOST-V6-3.5", 691, {"fin": "2021-12"}), ("3.5 V6 EcoBoost 446", "ECOBOOST-V6-3.5", 691, {"debut": "2022-01"})],
   places=8, reservoir=89, remarques=NA + " ; restylage 2022 ; nouvelle génération annoncée")
mg(L, "Aviator", "UN152", "1", "2002-06", "2005-12", [("4.6 V8 DOHC 306", "MODULAR-4.6-DOHC", 407)], places=7, reservoir=86, remarques=NA)
mg(L, "Aviator", "U611", "1", "2019-06", None,
   [("3.0 V6 EcoBoost 406", "ECOBOOST-V6-3.0", 563), ("Grand Touring 3.0 V6 PHEV 501", "ECOBOOST-V6-3.0-PHEV", 854, {"fin": "2023-12", "batterie": 13})],
   places=7, reservoir=76, remarques=NA + " ; restylage 2025")
mg(L, "MKC", "MKC", "1", "2014-06", "2019-06", [("2.0 EcoBoost 248", "ECOBOOST-2.0", 373), ("2.3 EcoBoost 289", "ECOBOOST-2.3", 413)], reservoir=59,
   remarques=NA + " ; base Ford Escape")
mg(L, "Corsair", "CX483", "1", "2019-09", None,
   [("2.0 EcoBoost 254", "ECOBOOST-2.0", 373), ("2.3 EcoBoost 299", "ECOBOOST-2.3", 420, {"fin": "2022-12"}),
    ("Grand Touring 2.5 PHEV 270", "DURATEC-2.5-PHEV", 210, {"debut": "2020-10", "batterie": 14})], reservoir=56, remarques=NA + " ; restylage 2023")
mg(L, "Nautilus", "U540", "1", "2015-06", "2023-06",
   [("MKX 3.7 V6 307", "CYCLONE-3.7", 380, {"fin": "2018-12"}), ("2.7 V6 EcoBoost 340", "ECOBOOST-V6-2.7", 515), ("2.0 EcoBoost 254", "ECOBOOST-2.0", 373, {"debut": "2019-01"})],
   reservoir=68, remarques=NA + " ; MKX jusqu'en 2018, renommé Nautilus en 2019")
mg(L, "Nautilus", "U540 (2024)", "1", "2023-10", None, [("2.0 EcoBoost 254", "ECOBOOST-2.0", 373), ("2.0 Hybrid 314", "ECOBOOST-2.0-HEV", 400)], reservoir=68,
   remarques=NA + " ; seconde génération produite en Chine")

# ---------------------------------------------------------------- berlines récentes
mg(L, "Zephyr (nouvelle génération)", "CD338", "1", "2005-09", "2012-08",
   [("Zephyr 3.0 V6 224", "DURATEC-V6-3.0", 278, {"fin": "2006-12"}), ("MKZ 3.5 V6 267", "CYCLONE-3.5", 337, {"debut": "2007-01"}),
    ("MKZ Hybrid 2.5 194", "DURATEC-2.5-HEV", 184, {"debut": "2010-06"})], portes=4, places=5, reservoir=66, remarques=NA + " ; Zephyr puis MKZ (2007)")
mg(L, "Zephyr (nouvelle génération)", "CD533", "1", "2012-09", "2020-12",
   [("MKZ 2.0 EcoBoost 243", "ECOBOOST-2.0", 366), ("MKZ 3.7 V6 304", "CYCLONE-3.7", 380, {"fin": "2016-12"}), ("MKZ Hybrid 2.0 191", "DURATEC-2.5-HEV", 175),
    ("MKZ 3.0 V6 EcoBoost 406", "ECOBOOST-V6-3.0", 542, {"debut": "2017-01"})], portes=4, places=5, reservoir=68,
   remarques=NA + " ; MKZ ; Zephyr (Chine, depuis 2022) non repris")
mg(L, "Continental", "D544", "1", "2016-09", "2020-12",
   [("3.7 V6 309", "CYCLONE-3.7", 380), ("2.7 V6 EcoBoost 340", "ECOBOOST-V6-2.7", 515), ("3.0 V6 EcoBoost 406", "ECOBOOST-V6-3.0", 542)], portes=4, places=5,
   reservoir=68, remarques=NA + " ; Coach Door Edition (2019)")

MOT = Motorisations("Lincoln", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Lincoln": L}
MOTEURS = MOT.moteurs()
