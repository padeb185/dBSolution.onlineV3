"""Ford USA (marché nord-américain) : générations, phases, motorisations et moteurs liés.
Modèles Ford nord-américains absents de ford.py (marché européen) : ancêtres (Model A 1903, N, T, A 1927, B, V8 1932-1948), Custom,
Crestline, Fairlane, Thunderbird, Galaxie, LTD, Crown Victoria, Falcon, Mustang (1964-2014), Torino, Maverick, Pinto, Granada, Fairmont,
Escort et Tempo nord-américains, Taurus, Probe, Five Hundred, Freestyle, Fusion (berline), Aerostar, Windstar / Freestar, Bronco
(1966-1996), Bronco II, Bronco Sport, Explorer (thermique), Explorer Sport Trac, Expedition, Excursion, Escape (1re et 2e gén.), Edge,
Flex, Ranger (1983-2012), F-150 et F-150 Lightning, Maverick pick-up. Mustang 2015+, Bronco 2024, Ranger T6, Kuga, GT et électriques
dans ford.py ; Super Duty, Transit et utilitaires non repris. Moteurs repris de mercury.py, ford.py, lincoln.py, shelby.py et
navistar.py (mêmes codes) ; familles manquantes ajoutées. Puissances brutes jusqu'en 1971, nettes ensuite, converties en ch (× 1,014).
Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .mercury import FAMILLES as FAMILLES_MERCURY
from .ford import FAMILLES as FAMILLES_FORD
from .lincoln import FAMILLES as FAMILLES_LINCOLN
from .shelby import FAMILLES as FAMILLES_SHELBY
from .navistar import FAMILLES as FAMILLES_NAVISTAR

E_, D, C, B = "ESS", "DSL", "CHAINE", "COURROIE"


def v8(l, rpm, nmrpm, q=5.7, t="ATM"):
    return f(t, E_, l, C, 8, rpm, nmrpm, "5W30", q, 7500, a="V")


REPRIS = {
    **FAMILLES_MERCURY,
    **{k: FAMILLES_FORD[k] for k in ("ECOBOOST-1.5", "ECOBOOST-1.5-3C", "ECOBOOST-2.0", "ECOBOOST-2.3", "ECOBOOST-V6-2.7", "ECOBOOST-V6-3.0", "ECOBOOST-V6-3.5",
                                     "COYOTE-5.0", "COLOGNE-2.9", "Lion-3.0V6")},
    **{k: FAMILLES_LINCOLN[k] for k in ("MODULAR-5.4", "AJ-V8-3.9", "ECOBOOST-V6-3.0-PHEV")},
    "PREDATOR-5.2S": FAMILLES_SHELBY["PREDATOR-5.2S"], "NAV-VT365-6.0": FAMILLES_NAVISTAR["NAV-VT365-6.0"],
}
NOUVEAUX = {
    "FORD-A1903-B2-1.7": f("ATM", E_, 1.7, "NC", 2, 1000, 700, "SAE30", 2.0, 1000, a="PLAT"),
    "FORD-N-2.4": f("ATM", E_, 2.4, "NC", 4, 1600, 900, "SAE30", 3.0, 1000),
    "FORD-T-2.9": f("ATM", E_, 2.9, "NC", 4, 1600, 900, "SAE30", 3.8, 800),
    "FORD-A-3.3": f("ATM", E_, 3.3, "NC", 4, 2200, 1000, "SAE30", 4.7, 1000),
    "FORD-FLATHEAD-3.6": f("ATM", E_, 3.6, "NC", 8, 3800, 2000, "SAE30", 4.7, 2000, a="V"),
    "FORD-FLATHEAD-2.2": f("ATM", E_, 2.2, "NC", 8, 3500, 2000, "SAE30", 4.0, 2000, a="V"),
    "FORD-I6-3.5": f("ATM", E_, 3.5, "NC", 6, 3500, 1600, "SAE30", 4.7, 3000),
    "FORD-I6-3.7F": f("ATM", E_, 3.7, "NC", 6, 3300, 1500, "SAE30", 4.7, 3000),
    "FORD-Y-3.9": v8(3.9, 4400, 2400, 4.7), "FORD-Y-4.5": v8(4.5, 4400, 2600, 4.7),
    "FORD-FE-5.8": v8(5.8, 4600, 2800, 4.7), "FORD-WINDSOR-4.3": v8(4.3, 4400, 2200, 4.7),
    "FORD-335-5.8M": v8(5.8, 3800, 2000, 4.7), "FORD-335-6.6": v8(6.6, 3800, 2000, 4.7),
    "FORD-I6-4.9": f("ATM", E_, 4.9, "NC", 6, 3400, 1800, "10W30", 5.7, 7500),
    "FORD-LIMA-2.0": f("ATM", E_, 2.0, B, 4, 4600, 2600, "10W30", 4.3, 7500),
    "FORD-LIMA-2.3SVO": f("TURBO", E_, 2.3, B, 4, 5000, 3000, "10W30", 4.3, 5000),
    "FORD-HSC-2.5": f("ATM", E_, 2.5, C, 4, 4400, 2600, "10W30", 4.3, 7500),
    "FORD-LIMA-2.5": f("ATM", E_, 2.5, B, 4, 5000, 3000, "5W30", 4.3, 7500),
    "YAMAHA-SHO-3.0": f("ATM", E_, 3.0, B, 6, 6200, 4800, "5W30", 4.7, 7500, a="V"),
    "YAMAHA-V8-3.4": f("ATM", E_, 3.4, C, 8, 6100, 4800, "5W30", 5.7, 7500, a="V"),
    "MAZDA-F2-2.2": f("ATM", E_, 2.2, B, 4, 5000, 3500, "10W30", 4.3, 7500), "MAZDA-F2-2.2T": f("TURBO", E_, 2.2, B, 4, 4300, 3500, "10W30", 4.3, 5000),
    "MAZDA-FS-2.0": f("ATM", E_, 2.0, B, 4, 5500, 4500, "10W30", 4.0, 7500), "MAZDA-KL-2.5": f("ATM", E_, 2.5, B, 6, 5600, 4800, "10W30", 4.5, 7500, a="V"),
    "FORD-ESSEX-3.9": f("ATM", E_, 3.9, C, 6, 4750, 3750, "5W30", 4.7, 7500, a="V"),
    "FORD-ESSEX-4.2": f("ATM", E_, 4.2, C, 6, 4750, 3000, "5W30", 4.7, 7500, a="V"),
    "FORD-CYCLONE-3.7": f("ATM", E_, 3.7, C, 6, 6500, 4000, "5W20", 5.7, 10000, a="V"),
    "FORD-CYCLONE-3.3": f("ATM", E_, 3.3, C, 6, 6500, 4000, "5W20", 5.7, 10000, a="V"),
    "MODULAR-4.6S": v8(4.6, 6000, 3500, 5.7, "TURBO"), "MODULAR-4.6-3V": v8(4.6, 5750, 4500, 5.7),
    "MODULAR-5.4-3V": v8(5.4, 5000, 3750, 6.6), "MODULAR-5.4S": v8(5.4, 4750, 3250, 6.6, "TURBO"),
    "FORD-BOSS-6.2": v8(6.2, 5500, 4500, 6.6), "FORD-WINDSOR-5.0-BOSS": v8(5.0, 7500, 4500, 8.0),
    "FORD-TRITON-V10-6.8": f("ATM", E_, 6.8, C, 10, 4750, 3250, "5W20", 6.6, 7500, a="V"),
    "NAV-POWERSTROKE-7.3": f("TURBO", D, 7.3, C, 8, 2600, 1600, "15W40", 14.0, 10000, a="V"),
    "ECOBOOST-V6-3.5T": FAMILLES_FORD["ECOBOOST-V6-3.5"],
    "ECOBOOST-V6-3.5-HEV": f("HYB_TE", E_, 3.5, C, 6, 6000, 3000, "5W30", 5.7, 15000, a="V"),
    "DURATEC-2.0-HEV": f("HYB_E", E_, 2.0, C, 4, 6000, 4000, "5W20", 4.7, 15000),
    "FORD-USA-EV": electrique(),
}
FAMILLES = {**REPRIS, **NOUVEAUX}


def motoriste(fam):
    if fam.startswith("NISSAN"):
        return "Nissan"
    if fam.startswith("MAZDA"):
        return "Mazda"
    if fam.startswith("YAMAHA"):
        return "Yamaha"
    if fam.startswith("NAV-"):
        return "International"
    return "Ford"


mg = SaisieMoteurs(FAMILLES, "Ford", motoriste)
L = []
IND = "marché nord-américain ; données indicatives"

# ---------------------------------------------------------------- ancêtres
mg(L, "Model A (1903)", "Model A", "1", "1903-07", "1904-12", [("1.7 8", "FORD-A1903-B2-1.7", 40)], portes=0, places=2, reservoir=20, remarques="Première Ford, bicylindre à plat ; " + IND)
mg(L, "Model N", "Model N", "1", "1906-01", "1908-12", [("2.4 15", "FORD-N-2.4", 60)], portes=0, places=2, reservoir=25, remarques="Modèles N, R et S ; " + IND)
mg(L, "Model T", "Model T", "1", "1908-10", "1927-05", [("2.9 20", "FORD-T-2.9", 113)], portes=2, places=4, reservoir=38,
   remarques="« Tin Lizzie », 15 millions d'exemplaires, chaîne d'assemblage mobile (1913) ; " + IND)
mg(L, "Model A (1927)", "Model A", "2", "1927-12", "1931-12", [("3.3 41", "FORD-A-3.3", 174)], portes=2, places=4, reservoir=38, remarques="Successeur de la Model T ; " + IND)
mg(L, "V8", "Model 18", "1", "1932-03", "1940-12",
   [("3.6 V8 66", "FORD-FLATHEAD-3.6", 176, {"fin": "1932-12"}), ("B 3.3 51", "FORD-A-3.3", 190, {"fin": "1934-12"}), ("3.6 V8 86", "FORD-FLATHEAD-3.6", 200, {"debut": "1933-01"}),
    ("V8-60 2.2 V8 61", "FORD-FLATHEAD-2.2", 128, {"debut": "1937-01"})],
   portes=2, places=5, reservoir=53, remarques="Premier V8 monobloc bon marché ; Model 18, 40, 48, 68, 78, 81A, 91A, 01A ; " + IND)
mg(L, "Super Deluxe", "1941", "1", "1941-01", "1948-12", [("3.7 L6 91", "FORD-I6-3.7F", 244), ("3.9 V8 101", "MERC-FLATHEAD-3.9", 244, {"debut": "1946-01"}),
                                                          ("3.6 V8 91", "FORD-FLATHEAD-3.6", 210, {"fin": "1942-12"})], portes=4, places=6, reservoir=64,
   remarques="Special, Deluxe et Super Deluxe ; production interrompue de 1942 à 1945 ; " + IND)
mg(L, "Custom", "Shoebox", "1", "1949-01", "1951-12", [("3.7 L6 96", "FORD-I6-3.7F", 244), ("3.9 V8 101", "MERC-FLATHEAD-3.9", 244)], portes=4, places=6, reservoir=61,
   remarques="« Shoebox », Custom et Deluxe, dont Victoria et Crestliner ; " + IND)
mg(L, "Crestline", "1952", "1", "1952-01", "1954-12", [("3.5 L6 102", "FORD-I6-3.5", 251, {"fin": "1953-12"}), ("3.9 V8 112", "MERC-FLATHEAD-3.9", 264, {"fin": "1953-12"}),
                                                       ("3.7 L6 117", "FORD-I6-3.7F", 264, {"debut": "1954-01"}), ("3.9 V8 Y 132", "FORD-Y-3.9", 290, {"debut": "1954-01"})],
   portes=4, places=6, reservoir=64, remarques="Mainline, Customline et Crestline ; premier V8 culbuté Y-block en 1954 ; " + IND)

# ---------------------------------------------------------------- 1955-1985
mg(L, "Fairlane", "1955", "1", "1955-01", "1961-12", [("4.5 V8 164", "FORD-Y-4.5", 346, {"fin": "1956-12"}), ("4.8 V8 200", "FORD-Y-4.8", 393, {"debut": "1956-01"}),
                                                      ("5.1 V8 213", "FORD-Y-5.1", 441, {"debut": "1957-01", "fin": "1959-12"}), ("5.8 V8 304", "FORD-FE-5.8", 515, {"debut": "1958-01"})],
   portes=4, places=6, reservoir=76, remarques="Grande berline, dont Crown Victoria (1955-1956) et Skyliner à toit rétractable ; " + IND)
mg(L, "Fairlane", "1962", "1", "1962-01", "1970-12", [("2.8 L6 102", "FORD-I6-2.8", 210), ("4.3 V8 166", "FORD-WINDSOR-4.3", 348), ("4.7 V8 203", "FORD-WINDSOR-4.7", 393),
                                                      ("6.4 V8 325", "FORD-FE-6.4", 576, {"debut": "1966-01"})], portes=4, places=6, reservoir=76, remarques="Intermédiaire ; " + IND)
mg(L, "Thunderbird", "1955", "1", "1955-01", "1957-12", [("4.8 V8 196", "FORD-Y-4.8", 386), ("5.1 V8 248", "FORD-Y-5.1", 454, {"debut": "1956-01"})], portes=2, places=2, reservoir=64,
   remarques="Biplace « personal car » ; " + IND)
mg(L, "Thunderbird", "1958", "1", "1958-01", "1966-12", [("5.8 V8 304", "FORD-FE-5.8", 515, {"fin": "1960-12"}), ("7.0 V8 355", "FORD-MEL-7.0", 651, {"debut": "1959-01", "fin": "1960-12"}),
                                                         ("6.4 V8 304", "FORD-FE-6.4", 583, {"debut": "1961-01"})], portes=2, places=4, reservoir=76, remarques="« Squarebird » puis « Bullet Bird » ; " + IND)
mg(L, "Thunderbird", "1967", "1", "1967-01", "1976-12", [("6.4 V8 319", "FORD-FE-6.4", 576, {"fin": "1968-12"}), ("7.0 V8 365", "FORD-385-7.0", 651, {"debut": "1968-01", "fin": "1971-12"}),
                                                         ("7.5 V8 220", "FORD-385-7.5", 481, {"debut": "1972-01"})], portes=2, places=5, reservoir=91, remarques=IND)
mg(L, "Thunderbird", "1977", "1", "1977-01", "1988-12", [("5.0 V8 132", "FORD-WINDSOR-5.0", 312), ("5.8 V8 150", "FORD-WINDSOR-5.8", 386, {"fin": "1979-12"}),
                                                         ("3.8 V6 122", "FORD-ESSEX-3.8", 271, {"debut": "1983-01"}), ("Turbo Coupe 2.3 Turbo 193", "FORD-LIMA-2.3SVO", 325, {"debut": "1983-01"})],
   portes=2, places=5, reservoir=78, remarques="Dont plateforme Fox (1980-1988) et Turbo Coupe ; " + IND)
mg(L, "Thunderbird", "MN12", "1", "1989-01", "1997-12", [("3.8 V6 142", "FORD-ESSEX-3.8", 292), ("SC 3.8 V6 Compresseur 213", "FORD-ESSEX-3.8", 427, {"fin": "1995-12"}),
                                                          ("5.0 V8 203", "FORD-WINDSOR-5.0", 373, {"debut": "1991-01", "fin": "1993-12"}), ("4.6 V8 208", "MODULAR-4.6", 359, {"debut": "1994-01"})],
   portes=2, places=5, reservoir=72, remarques="Jumelle de la Mercury Cougar ; " + IND)
mg(L, "Thunderbird", "DEW98", "1", "2001-09", "2005-12", [("3.9 V8 256", "AJ-V8-3.9", 362, {"fin": "2002-12"}), ("3.9 V8 284", "AJ-V8-3.9", 389, {"debut": "2003-01"})], portes=2, places=2, reservoir=68,
   remarques="Roadster rétro (base Lincoln LS) ; " + IND)
mg(L, "Galaxie", "1959", "1", "1959-01", "1974-12", [("5.8 V8 304", "FORD-FE-5.8", 515, {"fin": "1964-12"}), ("6.4 V8 304", "FORD-FE-6.4", 583), ("7.0 V8 431", "FORD-FE-7.0", 651, {"debut": "1963-01", "fin": "1967-12"}),
                                                      ("7.0 V8 365", "FORD-385-7.0", 651, {"debut": "1968-01", "fin": "1971-12"})], portes=4, places=6, reservoir=91,
   remarques="Grande berline, dont Galaxie 500 et 500XL ; " + IND)
mg(L, "LTD", "1965", "1", "1965-01", "1978-12", [("6.4 V8 274", "FORD-FE-6.4", 576, {"fin": "1971-12"}), ("7.0 V8 365", "FORD-385-7.0", 651, {"debut": "1968-01", "fin": "1971-12"}),
                                                  ("7.5 V8 208", "FORD-385-7.5", 481, {"debut": "1972-01"})], portes=4, places=6, reservoir=91, remarques="Version luxe de la Galaxie puis modèle à part ; " + IND)
mg(L, "LTD", "Panther", "1", "1979-01", "1991-12", [("5.0 V8 131", "FORD-WINDSOR-5.0", 325), ("5.0 V8 152", "FORD-WINDSOR-5.0", 366, {"debut": "1986-01"}), ("5.8 V8 152", "FORD-WINDSOR-5.8", 366, {"fin": "1982-12"})],
   portes=4, places=6, reservoir=76, remarques="LTD puis LTD Crown Victoria (1983) ; " + IND)
mg(L, "Crown Victoria", "Panther", "2", "1992-01", "2012-09", [("4.6 V8 193", "MODULAR-4.6", 373, {"fin": "1997-12"}), ("4.6 V8 203", "MODULAR-4.6", 386, {"debut": "1998-01", "fin": "2002-12"}),
                                                                ("4.6 V8 227", "MODULAR-4.6", 390, {"debut": "2003-01"})], portes=4, places=6, reservoir=72,
   remarques="Dont Police Interceptor et taxis ; jumelle de la Mercury Grand Marquis ; " + IND)
mg(L, "Falcon", "1960", "1", "1959-09", "1970-12", [("2.4 L6 91", "FORD-I6-2.4", 183, {"fin": "1962-12"}), ("2.8 L6 102", "FORD-I6-2.8", 210), ("3.3 L6 122", "FORD-I6-3.3", 258, {"debut": "1964-01"}),
                                                    ("4.7 V8 203", "FORD-WINDSOR-4.7", 393, {"debut": "1964-01"})], portes=4, places=6, reservoir=53,
   remarques="Compacte, base de la Mustang ; " + IND)
mg(L, "Mustang", "1964", "1", "1964-04", "1973-12",
   [("2.8 L6 102", "FORD-I6-2.8", 210, {"fin": "1965-06"}), ("3.3 L6 122", "FORD-I6-3.3", 258, {"debut": "1965-01"}), ("4.3 V8 166", "FORD-WINDSOR-4.3", 348, {"fin": "1965-06"}),
    ("4.7 V8 213", "FORD-WINDSOR-4.7", 407), ("K-Code 4.7 V8 275", "FORD-WINDSOR-4.7", 424, {"fin": "1967-12"}), ("6.4 V8 325", "FORD-FE-6.4", 576, {"debut": "1967-01", "fin": "1969-12"}),
    ("Mach 1 7.0 V8 CJ 340", "FORD-FE-7.0-428", 597, {"debut": "1968-04", "fin": "1970-12"}), ("Boss 302 5.0 V8 294", "FORD-WINDSOR-5.0-BOSS", 393, {"debut": "1969-01", "fin": "1970-12"}),
    ("Boss 429 7.0 V8 380", "FORD-385-7.0", 610, {"debut": "1969-01", "fin": "1970-12"}), ("5.8 V8 254", "FORD-WINDSOR-5.8", 481, {"debut": "1969-01"})],
   portes=2, places=4, reservoir=61, remarques="Pony car originel : coupé, fastback et cabriolet ; " + IND)
mg(L, "Mustang", "Mustang II", "1", "1973-09", "1978-12", [("2.3 89", "FORD-LIMA-2.3", 160), ("2.8 V6 107", "FORD-COLOGNE-2.8", 190), ("5.0 V8 141", "FORD-WINDSOR-5.0", 339, {"debut": "1975-01"})],
   portes=3, places=4, reservoir=49, remarques="Base Pinto ; " + IND)
mg(L, "Mustang", "Fox", "1", "1978-09", "1993-12",
   [("2.3 89", "FORD-LIMA-2.3", 160), ("2.3 Turbo 133", "FORD-LIMA-2.3T", 183, {"fin": "1981-12"}), ("SVO 2.3 Turbo 208", "FORD-LIMA-2.3SVO", 325, {"debut": "1984-01", "fin": "1986-12"}),
    ("3.8 V6 107", "FORD-ESSEX-3.8", 237, {"debut": "1983-01", "fin": "1986-12"}), ("5.0 V8 142", "FORD-WINDSOR-5.0", 339, {"fin": "1982-12"}),
    ("GT 5.0 V8 HO 213", "FORD-WINDSOR-5.0", 386, {"debut": "1983-01", "fin": "1986-12"}), ("GT 5.0 V8 HO 228", "FORD-WINDSOR-5.0", 407, {"debut": "1987-01"})],
   portes=3, places=4, reservoir=58, remarques="Plateforme Fox, coupé, hatchback et cabriolet ; " + IND)
mg(L, "Mustang", "SN95", "1", "1993-11", "2004-12",
   [("3.8 V6 147", "FORD-ESSEX-3.8", 291, {"fin": "1998-12"}), ("3.8 V6 193", "FORD-ESSEX-3.8", 305, {"debut": "1999-01"}), ("GT 5.0 V8 218", "FORD-WINDSOR-5.0", 390, {"fin": "1995-12"}),
    ("GT 4.6 V8 218", "MODULAR-4.6", 393, {"debut": "1996-01", "fin": "1998-12"}), ("GT 4.6 V8 264", "MODULAR-4.6", 410, {"debut": "1999-01"}),
    ("Cobra 4.6 V8 DOHC 309", "MODULAR-4.6-DOHC", 407, {"debut": "1999-01", "fin": "2001-12"}), ("Cobra 4.6 V8 Compresseur 395", "MODULAR-4.6S", 529, {"debut": "2003-01"})],
   portes=2, places=4, reservoir=59, remarques="Coupé et cabriolet, dont SVT Cobra ; " + IND)
mg(L, "Mustang", "S197", "1", "2004-09", "2014-12",
   [("4.0 V6 213", "FORD-COLOGNE-4.0", 346, {"fin": "2010-12"}), ("3.7 V6 309", "FORD-CYCLONE-3.7", 380, {"debut": "2011-01"}), ("GT 4.6 V8 304", "MODULAR-4.6-3V", 434, {"fin": "2009-12"}),
    ("GT 4.6 V8 319", "MODULAR-4.6-3V", 440, {"debut": "2010-01", "fin": "2010-12"}), ("GT 5.0 V8 418", "COYOTE-5.0", 529, {"debut": "2011-01", "fin": "2012-12"}),
    ("GT 5.0 V8 426", "COYOTE-5.0", 529, {"debut": "2013-01"}), ("Boss 302 5.0 V8 450", "COYOTE-5.0", 529, {"debut": "2012-01", "fin": "2013-12"})],
   portes=2, places=4, reservoir=60, remarques="Style rétro ; Shelby GT500 dans shelby.py ; " + IND)
mg(L, "Torino", "1968", "1", "1968-01", "1976-12", [("4.1 L6 157", "FORD-I6-4.1", 325), ("5.0 V8 223", "FORD-WINDSOR-5.0", 407), ("5.8 V8 254", "FORD-WINDSOR-5.8", 481),
                                                    ("Cobra 7.0 V8 CJ 375", "FORD-385-7.0", 610, {"debut": "1970-01", "fin": "1971-12"})], portes=4, places=6, reservoir=76,
   remarques="Intermédiaire, dont Torino GT, Cobra et Gran Torino ; puissances nettes dès 1972 ; " + IND)
mg(L, "Maverick", "1970", "1", "1969-04", "1977-12", [("2.8 L6 102", "FORD-I6-2.8", 210, {"fin": "1972-12"}), ("3.3 L6 83", "FORD-I6-3.3", 205), ("4.1 L6 89", "FORD-I6-4.1", 244),
                                                       ("5.0 V8 140", "FORD-WINDSOR-5.0", 339)], portes=2, places=5, reservoir=60, remarques="Compacte, jumelle de la Mercury Comet ; " + IND)
mg(L, "Pinto", "Pinto", "1", "1970-09", "1980-12", [("2.0 101", "PINTO-2.0", 162, {"fin": "1974-12"}), ("2.3 89", "FORD-LIMA-2.3", 160, {"debut": "1974-01"}),
                                                    ("2.8 V6 111", "FORD-COLOGNE-2.8", 197, {"debut": "1975-01", "fin": "1979-12"})], portes=3, places=4, reservoir=49,
   remarques="Sous-compacte (berline, hatchback Runabout, break) ; " + IND)
mg(L, "Granada", "1975", "1", "1975-01", "1982-12", [("4.1 L6 74", "FORD-I6-4.1", 237), ("5.0 V8 135", "FORD-WINDSOR-5.0", 332)], portes=4, places=5, reservoir=72,
   remarques="Granada nord-américaine, jumelle de la Mercury Monarch ; " + IND)
mg(L, "Fairmont", "Fox", "1", "1978-01", "1983-12", [("2.3 89", "FORD-LIMA-2.3", 160), ("3.3 L6 86", "FORD-I6-3.3", 210), ("5.0 V8 140", "FORD-WINDSOR-5.0", 339, {"fin": "1981-12"})],
   portes=4, places=5, reservoir=60, remarques="Jumelle de la Mercury Zephyr ; " + IND)

# ---------------------------------------------------------------- 1981-2020 berlines et coupés
mg(L, "Escort", "NA", "1", "1980-10", "1990-12", [("1.6 70", "FORD-CVH-1.6", 119, {"fin": "1984-12"}), ("1.9 88", "FORD-CVH-1.9", 146, {"debut": "1985-01"}),
                                                  ("GT 1.9 112", "FORD-CVH-1.9", 155, {"debut": "1986-01"})], portes=3, places=5, reservoir=43,
   remarques="Escort nord-américaine (différente de l'européenne) ; " + IND)
mg(L, "Escort", "NA", "2", "1990-04", "2002-12", [("1.9 89", "FORD-CVH-1.9", 155, {"fin": "1996-12"}), ("GT 1.8 129", "MAZDA-BP-1.8", 155, {"fin": "1996-12"}),
                                                  ("2.0 111", "FORD-SPI-2.0", 169, {"debut": "1997-01"}), ("ZX2 2.0 132", "ZETEC-2.0", 183, {"debut": "1997-09"})],
   portes=4, places=5, reservoir=48, remarques="Base Mazda 323 ; ZX2 coupé ; " + IND)
mg(L, "Tempo", "Tempo", "1", "1983-05", "1994-12", [("2.3 87", "FORD-HSC-2.3", 163), ("3.0 V6 132", "FORD-VULCAN-3.0", 217, {"debut": "1992-01"})], portes=4, places=5, reservoir=58,
   remarques="Jumelle de la Mercury Topaz ; " + IND)
mg(L, "Taurus", "1986", "1", "1985-12", "1995-12",
   [("2.5 91", "FORD-HSC-2.5", 176, {"fin": "1991-12"}), ("3.0 V6 142", "FORD-VULCAN-3.0", 217), ("3.8 V6 142", "FORD-ESSEX-3.8", 292, {"debut": "1988-01"}),
    ("SHO 3.0 V6 223", "YAMAHA-SHO-3.0", 271, {"debut": "1989-01"})], portes=4, places=6, reservoir=60, remarques="Berline et break, voiture la plus vendue aux États-Unis (1992-1996) ; " + IND)
mg(L, "Taurus", "1996", "1", "1995-09", "2007-10", [("3.0 V6 147", "FORD-VULCAN-3.0", 251), ("3.0 V6 Duratec 203", "DURATEC-V6-3.0", 271), ("SHO 3.4 V8 239", "YAMAHA-V8-3.4", 312, {"fin": "1999-12"})],
   portes=4, places=6, reservoir=68, remarques=IND)
mg(L, "Taurus", "D3", "1", "2007-09", "2009-12", [("3.5 V6 267", "DURATEC-3.5", 337)], portes=4, places=5, reservoir=72, remarques="Ex-Five Hundred ; " + IND)
mg(L, "Taurus", "D3", "2", "2009-06", "2019-03", [("3.5 V6 267", "DURATEC-3.5", 337, {"fin": "2012-12"}), ("3.5 V6 291", "DURATEC-3.5", 346, {"debut": "2013-01"}),
                                                   ("2.0 EcoBoost 243", "ECOBOOST-2.0", 366, {"debut": "2013-01"}), ("SHO 3.5 EcoBoost 370", "ECOBOOST-V6-3.5", 474)],
   portes=4, places=5, reservoir=72, remarques=IND)
mg(L, "Probe", "Probe", "1", "1988-05", "1992-12", [("2.2 112", "MAZDA-F2-2.2", 176), ("GT 2.2 Turbo 147", "MAZDA-F2-2.2T", 258), ("3.0 V6 142", "FORD-VULCAN-3.0", 217, {"debut": "1990-01"})],
   portes=3, places=4, reservoir=57, remarques="Coupé sur base Mazda MX-6 ; " + IND)
mg(L, "Probe", "Probe", "2", "1992-08", "1997-12", [("2.0 120", "MAZDA-FS-2.0", 172), ("GT 2.5 V6 166", "MAZDA-KL-2.5", 217)], portes=3, places=4, reservoir=58, remarques="Aussi vendu en Europe ; " + IND)
mg(L, "Five Hundred", "D3", "1", "2004-09", "2007-08", [("3.0 V6 206", "DURATEC-V6-3.0", 281)], portes=4, places=5, reservoir=72, remarques=IND)
mg(L, "Freestyle", "D3", "1", "2004-09", "2009-12", [("3.0 V6 206", "DURATEC-V6-3.0", 281, {"fin": "2007-08"}), ("3.5 V6 267", "DURATEC-3.5", 337, {"debut": "2007-09"})], portes=5, places=7, reservoir=72,
   remarques="Crossover, renommé Taurus X (2008-2009) ; " + IND)
mg(L, "Fusion", "CD3", "1", "2005-09", "2012-08", [("2.3 162", "DURATEC-HE-2.3", 212, {"fin": "2009-08"}), ("3.0 V6 224", "DURATEC-V6-3.0", 278, {"fin": "2009-08"}),
                                                   ("2.5 177", "DURATEC-HE-2.5", 232, {"debut": "2009-09"}), ("3.0 V6 243", "DURATEC-V6-3.0", 302, {"debut": "2009-09"}),
                                                   ("Sport 3.5 V6 267", "DURATEC-3.5", 337, {"debut": "2009-09"}), ("Hybrid 2.5 194", "DURATEC-2.5-HEV", 184, {"debut": "2009-09"})],
   portes=4, places=5, reservoir=66, remarques="Berline nord-américaine (différente de la Fusion européenne) ; " + IND)
mg(L, "Fusion", "CD4", "1", "2012-09", "2020-07", [("2.5 177", "DURATEC-HE-2.5", 232), ("1.5 EcoBoost 184", "ECOBOOST-1.5", 251, {"debut": "2014-01"}), ("2.0 EcoBoost 243", "ECOBOOST-2.0", 366),
                                                   ("Sport 2.7 EcoBoost 330", "ECOBOOST-V6-2.7", 542, {"debut": "2016-06"}), ("Hybrid 2.0 191", "DURATEC-2.0-HEV", 175),
                                                   ("Energi 2.0 PHEV 191", "DURATEC-2.0-HEV", 175, {"batterie": 8})], portes=4, places=5, reservoir=63,
   remarques="Jumelle de la Mondeo européenne ; " + IND)

# ---------------------------------------------------------------- monospaces, SUV, pick-up
mg(L, "Aerostar", "Aerostar", "1", "1985-08", "1997-12", [("2.3 89", "FORD-LIMA-2.3", 160, {"fin": "1986-12"}), ("3.0 V6 147", "FORD-VULCAN-3.0", 251), ("4.0 V6 157", "FORD-COLOGNE-4.0", 298, {"debut": "1990-01"})],
   portes=4, places=7, reservoir=79, remarques="Monospace à propulsion ; " + IND)
mg(L, "Windstar", "Windstar", "1", "1994-03", "2003-12", [("3.0 V6 147", "FORD-VULCAN-3.0", 251, {"fin": "1999-12"}), ("3.8 V6 203", "FORD-ESSEX-3.8", 312)], portes=4, places=7, reservoir=98, remarques=IND)
mg(L, "Freestar", "Windstar", "2", "2003-09", "2007-12", [("3.9 V6 196", "FORD-ESSEX-3.9", 319), ("4.2 V6 204", "FORD-ESSEX-4.2", 359)], portes=4, places=7, reservoir=98, remarques=IND)
mg(L, "Bronco", "1966", "1", "1965-08", "1977-12", [("2.8 L6 107", "FORD-I6-2.8", 215, {"fin": "1972-12"}), ("4.7 V8 203", "FORD-WINDSOR-4.7", 393, {"fin": "1968-12"}),
                                                    ("5.0 V8 208", "FORD-WINDSOR-5.0", 407, {"debut": "1969-01"})], portes=2, places=4, reservoir=55, remarques="Tout-terrain compact ; " + IND)
mg(L, "Bronco", "1978", "1", "1977-09", "1996-06", [("5.8 V8 158", "FORD-335-5.8M", 373, {"fin": "1979-12"}), ("6.6 V8 160", "FORD-335-6.6", 393, {"fin": "1979-12"}),
                                                    ("4.9 L6 121", "FORD-I6-4.9", 325, {"debut": "1980-01", "fin": "1986-12"}), ("4.9 L6 147", "FORD-I6-4.9", 359, {"debut": "1987-01"}),
                                                    ("5.0 V8 188", "FORD-WINDSOR-5.0", 366, {"debut": "1980-01"}), ("5.8 V8 213", "FORD-WINDSOR-5.8", 441, {"debut": "1987-01"})],
   portes=2, places=5, reservoir=121, remarques="Grand Bronco sur base F-Series ; " + IND)
mg(L, "Bronco II", "Bronco II", "1", "1983-03", "1990-12", [("2.8 V6 117", "FORD-COLOGNE-2.8", 203, {"fin": "1985-12"}), ("2.9 V6 142", "COLOGNE-2.9", 231, {"debut": "1986-01"})],
   portes=2, places=4, reservoir=87, remarques="Base Ranger ; " + IND)
mg(L, "Bronco Sport", "CX430", "1", "2020-10", None, [("1.5 EcoBoost 183", "ECOBOOST-1.5-3C", 258), ("2.0 EcoBoost 253", "ECOBOOST-2.0", 373)], portes=5, places=5, reservoir=60,
   remarques="SUV compact (base Escape / Kuga) ; " + IND)
mg(L, "Explorer", "UN46", "1", "1990-03", "2001-12", [("4.0 V6 157", "FORD-COLOGNE-4.0", 298, {"fin": "1992-12"}), ("4.0 V6 162", "FORD-COLOGNE-4.0", 305, {"debut": "1993-01"}),
                                                      ("4.0 V6 208", "FORD-COLOGNE-4.0", 346, {"debut": "1997-01"}), ("5.0 V8 218", "FORD-WINDSOR-5.0", 390, {"debut": "1996-01"})],
   portes=5, places=5, reservoir=80, remarques="Premier SUV familial à succès ; " + IND)
mg(L, "Explorer", "U152", "1", "2001-02", "2010-12", [("4.0 V6 213", "FORD-COLOGNE-4.0", 346), ("4.6 V8 243", "MODULAR-4.6", 382, {"fin": "2005-12"}), ("4.6 V8 296", "MODULAR-4.6-3V", 434, {"debut": "2006-01"})],
   portes=5, places=7, reservoir=85, remarques=IND)
mg(L, "Explorer", "U502", "1", "2010-12", "2019-03", [("3.5 V6 294", "DURATEC-3.5", 346), ("2.0 EcoBoost 243", "ECOBOOST-2.0", 366), ("2.3 EcoBoost 284", "ECOBOOST-2.3", 420, {"debut": "2016-01"}),
                                                      ("Sport 3.5 EcoBoost 370", "ECOBOOST-V6-3.5", 474, {"debut": "2013-01"})], portes=5, places=7, reservoir=70,
   remarques="Monocoque à traction / intégrale ; " + IND)
mg(L, "Explorer", "U625", "1", "2019-06", None, [("2.3 EcoBoost 304", "ECOBOOST-2.3", 420), ("ST 3.0 EcoBoost 406", "ECOBOOST-V6-3.0", 563),
                                                ("Plug-in Hybrid 3.0 457", "ECOBOOST-V6-3.0-PHEV", 825, {"batterie": 14, "fin": "2023-12", "remarques": "Version européenne hybride rechargeable (2020-2023)"})],
   portes=5, places=7, reservoir=68, remarques="Propulsion / intégrale ; vendu en Europe en hybride rechargeable ; " + IND)
mg(L, "Explorer Sport Trac", "Sport Trac", "1", "2000-07", "2010-12", [("4.0 V6 208", "FORD-COLOGNE-4.0", 346), ("4.6 V8 296", "MODULAR-4.6-3V", 434, {"debut": "2007-01"})],
   portes=4, places=5, reservoir=85, remarques="Pick-up à benne courte sur base Explorer ; " + IND)
mg(L, "Expedition", "UN93", "1", "1996-09", "2002-12", [("4.6 V8 218", "MODULAR-4.6", 393), ("5.4 V8 236", "MODULAR-5.4", 441, {"fin": "1998-12"}), ("5.4 V8 264", "MODULAR-5.4", 468, {"debut": "1999-01"})],
   portes=5, places=8, reservoir=114, remarques="Grand SUV sur base F-150 ; " + IND)
mg(L, "Expedition", "U222", "1", "2002-09", "2006-12", [("4.6 V8 235", "MODULAR-4.6", 407, {"fin": "2004-12"}), ("5.4 V8 264", "MODULAR-5.4", 468, {"fin": "2004-12"}),
                                                        ("5.4 V8 3V 304", "MODULAR-5.4-3V", 495, {"debut": "2005-01"})], portes=5, places=8, reservoir=106, remarques=IND)
mg(L, "Expedition", "U324", "1", "2006-09", "2017-09", [("5.4 V8 314", "MODULAR-5.4-3V", 495, {"fin": "2014-12"}), ("3.5 EcoBoost 370", "ECOBOOST-V6-3.5T", 569, {"debut": "2015-01"})],
   portes=5, places=8, reservoir=106, remarques="Dont Expedition EL / Max ; " + IND)
mg(L, "Expedition", "U553", "1", "2017-10", None, [("3.5 EcoBoost 380", "ECOBOOST-V6-3.5T", 637), ("Platinum 3.5 EcoBoost 406", "ECOBOOST-V6-3.5T", 678)], portes=5, places=8, reservoir=89,
   remarques="Carrosserie aluminium ; dont Expedition Max ; " + IND)
mg(L, "Excursion", "Excursion", "1", "1999-10", "2005-12", [("5.4 V8 259", "MODULAR-5.4", 474), ("6.8 V10 314", "FORD-TRITON-V10-6.8", 576), ("Diesel 7.3 V8 254", "NAV-POWERSTROKE-7.3", 712, {"fin": "2003-06"}),
                                                            ("Diesel 6.0 V8 330", "NAV-VT365-6.0", 759, {"debut": "2003-01"})], portes=5, places=8, reservoir=167,
   remarques="SUV géant sur base Super Duty ; diesels Power Stroke (Navistar) ; " + IND)
mg(L, "Escape", "ZA / ZB", "1", "2000-08", "2007-12", [("2.0 132", "ZETEC-2.0", 183, {"fin": "2004-12"}), ("2.3 155", "DURATEC-HE-2.3", 204, {"debut": "2005-01"}), ("3.0 V6 203", "DURATEC-V6-3.0", 271),
                                                       ("Hybrid 2.3 157", "DURATEC-2.3-HEV", 175, {"debut": "2004-09"})], portes=5, places=5, reservoir=62,
   remarques="Jumeau des Mazda Tribute et Mercury Mariner ; 3e génération et suivantes = Kuga (ford.py) ; " + IND)
mg(L, "Escape", "ZC / ZD", "1", "2007-09", "2012-06", [("2.5 173", "DURATEC-HE-2.5", 232, {"debut": "2008-09"}), ("2.3 155", "DURATEC-HE-2.3", 204, {"fin": "2008-08"}),
                                                       ("3.0 V6 243", "DURATEC-V6-3.0", 302, {"debut": "2008-09"}), ("Hybrid 2.5 179", "DURATEC-2.5-HEV", 184, {"debut": "2008-09"})],
   portes=5, places=5, reservoir=62, remarques=IND)
mg(L, "Edge", "CD3", "1", "2006-12", "2014-12", [("3.5 V6 269", "DURATEC-3.5", 339), ("Sport 3.7 V6 309", "FORD-CYCLONE-3.7", 380, {"debut": "2010-06"}),
                                                 ("2.0 EcoBoost 243", "ECOBOOST-2.0", 366, {"debut": "2011-06"})], portes=5, places=5, reservoir=76,
   remarques="1re génération nord-américaine ; 2e génération dans ford.py ; " + IND)
mg(L, "Flex", "D4", "1", "2008-06", "2019-11", [("3.5 V6 266", "DURATEC-3.5", 336, {"fin": "2012-12"}), ("3.5 V6 291", "DURATEC-3.5", 346, {"debut": "2013-01"}),
                                                ("3.5 EcoBoost 370", "ECOBOOST-V6-3.5", 474, {"debut": "2009-06"})], portes=5, places=7, reservoir=70, remarques="Crossover 7 places ; " + IND)
mg(L, "Ranger", "NA", "1", "1982-03", "1992-12", [("2.0 74", "FORD-LIMA-2.0", 149, {"fin": "1988-12"}), ("2.3 91", "FORD-LIMA-2.3", 165), ("2.8 V6 117", "FORD-COLOGNE-2.8", 203, {"fin": "1985-12"}),
                                                  ("2.9 V6 142", "COLOGNE-2.9", 231, {"debut": "1986-01"}), ("4.0 V6 162", "FORD-COLOGNE-4.0", 305, {"debut": "1990-01"})],
   portes=2, places=3, reservoir=64, remarques="Pick-up compact nord-américain ; " + IND)
mg(L, "Ranger", "NA", "2", "1992-08", "2012-12", [("2.3 99", "FORD-LIMA-2.3", 180, {"fin": "1997-12"}), ("2.5 121", "FORD-LIMA-2.5", 196, {"debut": "1998-01", "fin": "2000-12"}),
                                                  ("2.3 145", "DURATEC-HE-2.3", 203, {"debut": "2001-01"}), ("3.0 V6 147", "FORD-VULCAN-3.0", 251), ("4.0 V6 162", "FORD-COLOGNE-4.0", 305, {"fin": "2000-12"}),
                                                  ("4.0 V6 210", "FORD-COLOGNE-4.0", 322, {"debut": "2001-01"})], portes=2, places=3, reservoir=74,
   remarques="Ranger T6 (2012+) et P703 dans ford.py ; " + IND)
mg(L, "Maverick", "P758", "1", "2021-09", None, [("Hybrid 2.5 194", "DURATEC-2.5-HEV", 184), ("2.0 EcoBoost 253", "ECOBOOST-2.0", 373)], portes=4, places=5, reservoir=52,
   remarques="Pick-up compact monocoque ; " + IND)
mg(L, "F-150", "1975", "1", "1975-01", "1979-12", [("4.9 L6 119", "FORD-I6-4.9", 298), ("5.8 V8 163", "FORD-335-5.8M", 373), ("6.6 V8 171", "FORD-335-6.6", 400)], portes=2, places=3, reservoir=72,
   remarques="Pick-up (F-Series 6e gén.), cabine simple ou double ; " + IND)
mg(L, "F-150", "1980", "1", "1980-01", "1996-12", [("4.9 L6 122", "FORD-I6-4.9", 332, {"fin": "1986-12"}), ("4.9 L6 147", "FORD-I6-4.9", 359, {"debut": "1987-01"}),
                                                   ("5.0 V8 135", "FORD-WINDSOR-5.0", 332, {"fin": "1986-12"}), ("5.0 V8 188", "FORD-WINDSOR-5.0", 366, {"debut": "1987-01"}),
                                                   ("5.8 V8 158", "FORD-WINDSOR-5.8", 373, {"fin": "1986-12"}), ("5.8 V8 213", "FORD-WINDSOR-5.8", 441, {"debut": "1987-01"})],
   portes=2, places=3, reservoir=72, remarques="7e à 9e générations ; dont SVT Lightning 5.8 (1993-1995) ; " + IND)
mg(L, "F-150", "PN96", "1", "1996-01", "2004-12", [("4.2 V6 208", "FORD-ESSEX-4.2", 346), ("4.6 V8 223", "MODULAR-4.6", 393), ("5.4 V8 238", "MODULAR-5.4", 441, {"fin": "1998-12"}),
                                                   ("5.4 V8 264", "MODULAR-5.4", 468, {"debut": "1999-01"}), ("SVT Lightning 5.4 V8 Compresseur 385", "MODULAR-5.4S", 610, {"debut": "1999-01"})],
   portes=2, places=3, reservoir=95, remarques="10e génération ; " + IND)
mg(L, "F-150", "P221", "1", "2003-09", "2008-12", [("4.2 V6 205", "FORD-ESSEX-4.2", 353), ("4.6 V8 234", "MODULAR-4.6", 397), ("5.4 V8 3V 304", "MODULAR-5.4-3V", 495)], portes=4, places=5, reservoir=113,
   remarques="11e génération ; " + IND)
mg(L, "F-150", "P415", "1", "2008-09", "2014-12",
   [("4.6 V8 251", "MODULAR-4.6", 397, {"fin": "2010-12"}), ("4.6 V8 296", "MODULAR-4.6-3V", 434, {"fin": "2010-12"}), ("5.4 V8 314", "MODULAR-5.4-3V", 495, {"fin": "2010-12"}),
    ("3.7 V6 306", "FORD-CYCLONE-3.7", 380, {"debut": "2011-01"}), ("5.0 V8 365", "COYOTE-5.0", 515, {"debut": "2011-01"}), ("3.5 EcoBoost 370", "ECOBOOST-V6-3.5T", 569, {"debut": "2011-01"}),
    ("6.2 V8 417", "FORD-BOSS-6.2", 590, {"debut": "2011-01"}), ("SVT Raptor 6.2 V8 417", "FORD-BOSS-6.2", 590, {"debut": "2010-01"})], portes=4, places=5, reservoir=98,
   remarques="12e génération, dont SVT Raptor ; " + IND)
mg(L, "F-150", "P552", "1", "2014-09", "2020-12",
   [("3.5 V6 286", "DURATEC-3.5", 344, {"fin": "2017-12"}), ("3.3 V6 294", "FORD-CYCLONE-3.3", 359, {"debut": "2018-01"}), ("2.7 EcoBoost 330", "ECOBOOST-V6-2.7", 542),
    ("5.0 V8 390", "COYOTE-5.0", 524, {"fin": "2017-12"}), ("5.0 V8 401", "COYOTE-5.0", 542, {"debut": "2018-01"}), ("3.5 EcoBoost 380", "ECOBOOST-V6-3.5T", 637),
    ("Raptor 3.5 EcoBoost 456", "ECOBOOST-V6-3.5T", 691, {"debut": "2017-01"}), ("Diesel 3.0 V6 254", "Lion-3.0V6", 597, {"debut": "2018-01"})], portes=4, places=5, reservoir=98,
   remarques="13e génération, carrosserie aluminium ; " + IND)
mg(L, "F-150", "P702", "1", "2020-11", None,
   [("3.3 V6 294", "FORD-CYCLONE-3.3", 359, {"fin": "2023-12"}), ("2.7 EcoBoost 330", "ECOBOOST-V6-2.7", 542), ("5.0 V8 406", "COYOTE-5.0", 556), ("3.5 EcoBoost 406", "ECOBOOST-V6-3.5T", 678),
    ("PowerBoost 3.5 Hybrid 436", "ECOBOOST-V6-3.5-HEV", 773), ("Raptor 3.5 EcoBoost 456", "ECOBOOST-V6-3.5T", 691), ("Raptor R 5.2 V8 Compresseur 710", "PREDATOR-5.2S", 868, {"debut": "2022-09"})],
   portes=4, places=5, reservoir=98, remarques="14e génération ; restylage 2024 ; " + IND)
mg(L, "F-150 Lightning", "P702 EV", "1", "2022-04", "2025-12", [("Électrique 98 kWh 458", "FORD-USA-EV", 1050, {"batterie": 98}), ("Électrique 131 kWh 588", "FORD-USA-EV", 1050, {"batterie": 131})],
   portes=4, places=5, reservoir=0, remarques="Pick-up électrique à deux moteurs ; production arrêtée fin 2025 ; " + IND)

MOT = Motorisations("Ford", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Ford USA": L}
MOTEURS = MOT.moteurs()
