"""Mercury (Ford Motor Company, 1938-2011) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Eight, Monterey, Montclair, Medalist, Turnpike Cruiser, S-55, Comet, Cyclone, Cougar, Marquis, Grand Marquis, Monarch, Zephyr, Capri,
Lynx, Topaz, Tracer, Sable, Mystique, Villager, Mountaineer, Marauder, Montego, Milan et Mariner. Marque arrêtée en 2011.
Moteurs Ford repris de lincoln.py, edsel.py, shelby.py et ford.py (mêmes codes) ; autres familles Ford, Nissan et Mazda ajoutées.
Puissances brutes jusqu'en 1971, nettes ensuite, converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .lincoln import FAMILLES as FAMILLES_LINCOLN
from .edsel import FAMILLES as FAMILLES_EDSEL
from .shelby import FAMILLES as FAMILLES_SHELBY
from .ford import FAMILLES as FAMILLES_FORD

E_, D, C, B = "ESS", "DSL", "CHAINE", "COURROIE"


def v8(l, rpm, nmrpm, q=4.7):
    return f("ATM", E_, l, C, 8, rpm, nmrpm, "10W30", q, 5000, a="V")


REPRIS = {
    **{k: FAMILLES_LINCOLN[k] for k in ("FORD-WINDSOR-5.0", "FORD-WINDSOR-5.8", "MODULAR-4.6", "MODULAR-4.6-DOHC", "FORD-385-7.5", "FORD-MEL-7.0", "LINCOLN-Y-6.0")},
    **{k: FAMILLES_EDSEL[k] for k in ("FORD-Y-4.8", "FORD-MEL-6.7")},
    **{k: FAMILLES_SHELBY[k] for k in ("FORD-FE-7.0", "FORD-FE-7.0-428")},
    **{k: FAMILLES_FORD[k] for k in ("DURATEC-V6-3.0", "DURATEC-HE-2.3", "ZETEC-2.0", "DURATEC-V6-2.5", "PINTO-2.0", "DURATEC-2.5-HEV")},
}
NOUVEAUX = {
    "MERC-FLATHEAD-3.9": f("ATM", E_, 3.9, "NC", 8, 3600, 2000, "SAE30", 4.7, 3000, a="V"),
    "MERC-FLATHEAD-4.2": f("ATM", E_, 4.2, "NC", 8, 3600, 2000, "SAE30", 4.7, 3000, a="V"),
    "FORD-Y-4.2": v8(4.2, 4400, 2800), "FORD-Y-5.1": v8(5.1, 4600, 2600), "FORD-FE-6.4": v8(6.4, 4600, 2800, 4.7),
    "FORD-385-7.0": v8(7.0, 4600, 2800, 4.7), "FORD-WINDSOR-4.7": v8(4.7, 4400, 2400),
    "FORD-I6-2.4": f("ATM", E_, 2.4, C, 6, 4200, 2000, "10W30", 3.8, 5000), "FORD-I6-2.8": f("ATM", E_, 2.8, C, 6, 4400, 2400, "10W30", 3.8, 5000),
    "FORD-I6-3.3": f("ATM", E_, 3.3, C, 6, 3800, 1600, "10W30", 4.3, 5000), "FORD-I6-4.1": f("ATM", E_, 4.1, C, 6, 3600, 1600, "10W30", 4.7, 5000),
    "FORD-LIMA-2.3": f("ATM", E_, 2.3, B, 4, 4600, 2600, "10W30", 4.3, 7500), "FORD-LIMA-2.3T": f("TURBO", E_, 2.3, B, 4, 5200, 3000, "10W30", 4.3, 5000),
    "FORD-HSC-2.3": f("ATM", E_, 2.3, C, 4, 4400, 2600, "10W30", 4.3, 7500),
    "FORD-COLOGNE-2.8": f("ATM", E_, 2.8, C, 6, 4600, 3200, "10W30", 4.3, 7500, a="V"),
    "FORD-ESSEX-3.8": f("ATM", E_, 3.8, C, 6, 4200, 2600, "5W30", 4.3, 7500, a="V"),
    "FORD-VULCAN-3.0": f("ATM", E_, 3.0, C, 6, 4800, 3250, "5W30", 4.3, 7500, a="V"),
    "FORD-COLOGNE-4.0": f("ATM", E_, 4.0, C, 6, 5250, 3000, "5W30", 4.7, 7500, a="V"),
    "FORD-CVH-1.6": f("ATM", E_, 1.6, B, 4, 5200, 3000, "10W30", 3.8, 7500), "FORD-CVH-1.9": f("ATM", E_, 1.9, B, 4, 4800, 3500, "10W30", 3.8, 7500),
    "FORD-SPI-2.0": f("ATM", E_, 2.0, B, 4, 5000, 3750, "5W30", 4.0, 7500),
    "DURATEC-3.5": f("ATM", E_, 3.5, C, 6, 6250, 4500, "5W20", 5.2, 12000, a="V"),
    "DURATEC-HE-2.5": f("ATM", E_, 2.5, C, 4, 6000, 4500, "5W20", 5.0, 12000),
    "DURATEC-2.3-HEV": f("HYB_E", E_, 2.3, C, 4, 6000, 4250, "5W20", 5.0, 12000),
    "MAZDA-B6-1.6": f("ATM", E_, 1.6, B, 4, 5200, 4000, "10W30", 3.6, 7500), "MAZDA-B6T-1.6": f("TURBO", E_, 1.6, B, 4, 6000, 4000, "10W30", 3.6, 5000),
    "MAZDA-BP-1.8": f("ATM", E_, 1.8, B, 4, 6500, 4500, "10W30", 3.8, 7500),
    "NISSAN-VG30-3.0": f("ATM", E_, 3.0, B, 6, 4800, 4000, "10W30", 4.0, 7500, a="V"), "NISSAN-VG33-3.3": f("ATM", E_, 3.3, B, 6, 4800, 2800, "10W30", 4.0, 7500, a="V"),
}
FAMILLES = {**REPRIS, **NOUVEAUX}
mg = SaisieMoteurs(FAMILLES, "Ford", lambda fam: "Nissan" if fam.startswith("NISSAN") else ("Mazda" if fam.startswith("MAZDA") else "Ford"))
L = []
IND = "marché nord-américain ; données indicatives"

# ---------------------------------------------------------------- 1939-1960
mg(L, "Mercury Eight", "Eight", "1", "1938-11", "1951-12", [("3.9 V8 96", "MERC-FLATHEAD-3.9", 244, {"fin": "1948-12"}), ("4.2 V8 112", "MERC-FLATHEAD-4.2", 271, {"debut": "1949-01"})],
   portes=4, places=6, reservoir=64, remarques="Première Mercury ; V8 à soupapes latérales ; coupé 1949-1951 rendu célèbre par les customs ; " + IND)
mg(L, "Monterey", "1950", "1", "1950-01", "1956-12", [("4.2 V8 127", "MERC-FLATHEAD-4.2", 276, {"fin": "1953-12"}), ("4.2 V8 163", "FORD-Y-4.2", 325, {"debut": "1954-01", "fin": "1954-12"}),
                                                       ("4.8 V8 200", "FORD-Y-4.8", 393, {"debut": "1955-01"})], portes=4, places=6, reservoir=76, remarques=IND)
mg(L, "Monterey", "1957", "1", "1957-01", "1960-12", [("6.0 V8 294", "LINCOLN-Y-6.0", 515)], portes=4, places=6, reservoir=76, remarques=IND)
mg(L, "Monterey", "1961", "1", "1961-01", "1968-12", [("6.4 V8 304", "FORD-FE-6.4", 583)], portes=4, places=6, reservoir=76, remarques=IND)
mg(L, "Monterey", "1969", "1", "1969-01", "1974-12", [("6.4 V8 269", "FORD-FE-6.4", 550, {"fin": "1971-12"}), ("7.0 V8 365", "FORD-385-7.0", 651, {"fin": "1971-12"}),
                                                       ("7.0 V8 205", "FORD-385-7.0", 434, {"debut": "1972-01"})], portes=4, places=6, reservoir=91, remarques="Puissances nettes dès 1972 ; " + IND)
mg(L, "Montclair", "1955", "1", "1955-01", "1960-12", [("4.8 V8 200", "FORD-Y-4.8", 393, {"fin": "1956-12"}), ("6.0 V8 294", "LINCOLN-Y-6.0", 515, {"debut": "1957-01", "fin": "1958-12"}),
                                                         ("7.0 V8 355", "FORD-MEL-7.0", 651, {"debut": "1959-01"})], portes=4, places=6, reservoir=76, remarques=IND)
mg(L, "Medalist", "1956", "1", "1956-01", "1958-12", [("5.1 V8 213", "FORD-Y-5.1", 441)], portes=4, places=6, reservoir=76, remarques="Entrée de gamme ; " + IND)
mg(L, "Turnpike Cruiser", "1957", "1", "1957-01", "1958-12", [("6.0 V8 294", "LINCOLN-Y-6.0", 515, {"fin": "1957-12"}), ("7.0 V8 365", "FORD-MEL-7.0", 651, {"debut": "1958-01"})],
   portes=4, places=6, reservoir=76, remarques="Lunette arrière rétractable ; " + IND)

# ---------------------------------------------------------------- années 1960-1970
mg(L, "S-55", "1962", "1", "1962-01", "1967-12", [("6.4 V8 304", "FORD-FE-6.4", 583), ("7.0 V8 431", "FORD-FE-7.0", 651, {"debut": "1963-01"})], portes=2, places=5, reservoir=76,
   remarques="Coupé et cabriolet sportifs ; " + IND)
mg(L, "Comet", "1960", "1", "1960-03", "1969-12", [("2.4 L6 91", "FORD-I6-2.4", 183, {"fin": "1962-12"}), ("2.8 L6 102", "FORD-I6-2.8", 210), ("4.7 V8 203", "FORD-WINDSOR-4.7", 393, {"debut": "1964-01"})],
   portes=4, places=5, reservoir=53, remarques="Compacte, puis intermédiaire (1966) ; " + IND)
mg(L, "Comet", "1971", "1", "1971-01", "1977-12", [("3.3 L6 83", "FORD-I6-3.3", 205), ("4.1 L6 89", "FORD-I6-4.1", 244), ("5.0 V8 140", "FORD-WINDSOR-5.0", 339)], portes=4, places=5, reservoir=60,
   remarques="Jumelle de la Ford Maverick ; " + IND)
mg(L, "Cyclone", "1964", "1", "1964-01", "1971-12", [("4.7 V8 213", "FORD-WINDSOR-4.7", 407), ("7.0 V8 CJ 340", "FORD-FE-7.0-428", 597, {"debut": "1968-01", "fin": "1969-12"}),
                                                       ("7.0 V8 CJ 375", "FORD-385-7.0", 610, {"debut": "1970-01"})], portes=2, places=5, reservoir=76, remarques="Coupé intermédiaire sportif (muscle car) ; " + IND)
mg(L, "Cougar", "1967", "1", "1967-01", "1973-12", [("4.7 V8 203", "FORD-WINDSOR-4.7", 393, {"fin": "1968-12"}), ("6.4 V8 325", "FORD-FE-6.4", 576, {"fin": "1970-12"}),
                                                     ("5.8 V8 294", "FORD-WINDSOR-5.8", 515, {"debut": "1969-01"}), ("Eliminator 7.0 V8 CJ 340", "FORD-FE-7.0-428", 597, {"debut": "1969-01", "fin": "1970-12"})],
   portes=2, places=4, reservoir=76, remarques="Pony car haut de gamme (base Mustang), coupé et cabriolet, dont XR-7 ; " + IND)
mg(L, "Cougar", "1974", "1", "1974-01", "1982-12", [("5.8 V8 150", "FORD-WINDSOR-5.8", 386), ("5.0 V8 132", "FORD-WINDSOR-5.0", 312, {"debut": "1977-01"})], portes=2, places=5, reservoir=80,
   remarques="Cougar XR-7 personnel-luxe ; " + IND)
mg(L, "Cougar", "1983", "1", "1983-01", "1988-12", [("3.8 V6 122", "FORD-ESSEX-3.8", 271), ("5.0 V8 157", "FORD-WINDSOR-5.0", 339, {"debut": "1984-01"})], portes=2, places=5, reservoir=78,
   remarques="Plateforme Fox ; " + IND)
mg(L, "Cougar", "1989", "1", "1989-01", "1997-12", [("3.8 V6 142", "FORD-ESSEX-3.8", 292), ("5.0 V8 203", "FORD-WINDSOR-5.0", 373, {"debut": "1991-01", "fin": "1993-12"}),
                                                     ("4.6 V8 208", "MODULAR-4.6", 359, {"debut": "1994-01"})], portes=2, places=5, reservoir=72, remarques="Plateforme MN12 (Thunderbird) ; " + IND)
mg(L, "Cougar", "1999", "1", "1998-09", "2002-12", [("2.0 127", "ZETEC-2.0", 176), ("2.5 V6 172", "DURATEC-V6-2.5", 224)], portes=3, places=4, reservoir=61,
   remarques="Coupé à traction (vendu Ford Cougar en Europe) ; " + IND)
mg(L, "Marquis", "1967", "1", "1967-01", "1978-12", [("6.4 V8 274", "FORD-FE-6.4", 576, {"fin": "1968-12"}), ("7.0 V8 365", "FORD-385-7.0", 651, {"debut": "1969-01", "fin": "1971-12"}),
                                                      ("7.5 V8 208", "FORD-385-7.5", 481, {"debut": "1972-01"})], portes=4, places=6, reservoir=91, remarques="Grande berline et break Colony Park ; " + IND)
mg(L, "Marquis", "1983", "1", "1983-01", "1986-12", [("2.3 90", "FORD-LIMA-2.3", 165), ("3.8 V6 122", "FORD-ESSEX-3.8", 271)], portes=4, places=5, reservoir=60, remarques="Intermédiaire plateforme Fox ; " + IND)
mg(L, "Grand Marquis", "1975", "1", "1975-01", "1978-12", [("7.5 V8 220", "FORD-385-7.5", 481)], portes=4, places=6, reservoir=91, remarques="Finition haut de gamme de la Marquis ; " + IND)
mg(L, "Grand Marquis", "Panther", "1", "1979-01", "1991-12", [("5.0 V8 131", "FORD-WINDSOR-5.0", 325), ("5.0 V8 152", "FORD-WINDSOR-5.0", 366, {"debut": "1986-01"}), ("5.8 V8 152", "FORD-WINDSOR-5.8", 366, {"fin": "1982-12"})],
   portes=4, places=6, reservoir=76, remarques=IND)
mg(L, "Grand Marquis", "Panther", "2", "1992-01", "2011-01", [("4.6 V8 193", "MODULAR-4.6", 373, {"fin": "1997-12"}), ("4.6 V8 203", "MODULAR-4.6", 386, {"debut": "1998-01", "fin": "2002-12"}),
                                                                ("4.6 V8 227", "MODULAR-4.6", 390, {"debut": "2003-01"})], portes=4, places=6, reservoir=72,
   remarques="Dernière Mercury produite le 4 janvier 2011 ; " + IND)
mg(L, "Monarch", "1975", "1", "1975-01", "1980-12", [("4.1 L6 74", "FORD-I6-4.1", 237), ("5.0 V8 135", "FORD-WINDSOR-5.0", 332)], portes=4, places=5, reservoir=72,
   remarques="Jumelle de la Ford Granada (Amérique du Nord) ; " + IND)
mg(L, "Zephyr", "Fox", "1", "1978-01", "1983-12", [("2.3 89", "FORD-LIMA-2.3", 160), ("3.3 L6 86", "FORD-I6-3.3", 210), ("5.0 V8 140", "FORD-WINDSOR-5.0", 339, {"fin": "1981-12"}),
                                                   ("3.8 V6 113", "FORD-ESSEX-3.8", 237, {"debut": "1982-01"})], portes=4, places=5, reservoir=60, remarques="Jumelle de la Ford Fairmont ; " + IND)

# ---------------------------------------------------------------- Capri
mg(L, "Capri", "Capri I-II", "1", "1970-04", "1977-12", [("2.0 101", "PINTO-2.0", 162, {"fin": "1974-12"}), ("2.8 V6 111", "FORD-COLOGNE-2.8", 197, {"debut": "1972-01"})], portes=2, places=4, reservoir=58,
   remarques="Ford Capri allemande importée et vendue par Mercury ; " + IND)
mg(L, "Capri", "Fox", "1", "1979-01", "1986-12", [("2.3 89", "FORD-LIMA-2.3", 160), ("2.3 Turbo 133", "FORD-LIMA-2.3T", 183, {"fin": "1981-12"}), ("3.8 V6 107", "FORD-ESSEX-3.8", 237, {"debut": "1983-01"}),
                                                  ("5.0 V8 142", "FORD-WINDSOR-5.0", 339, {"fin": "1982-12"}), ("5.0 V8 HO 213", "FORD-WINDSOR-5.0", 386, {"debut": "1983-01"})],
   portes=3, places=4, reservoir=58, remarques="Jumelle de la Mustang (Fox), dont RS ; " + IND)
mg(L, "Capri", "SA30", "1", "1991-01", "1994-12", [("1.6 101", "MAZDA-B6-1.6", 129), ("XR2 1.6 Turbo 134", "MAZDA-B6T-1.6", 197)], portes=2, places=4, reservoir=45,
   remarques="Cabriolet Ford Capri australien ; " + IND)

# ---------------------------------------------------------------- compactes et intermédiaires 1981-2000
mg(L, "Lynx", "Lynx", "1", "1981-01", "1987-12", [("1.6 70", "FORD-CVH-1.6", 119, {"fin": "1984-12"}), ("1.9 88", "FORD-CVH-1.9", 146, {"debut": "1985-01"})], portes=3, places=5, reservoir=43,
   remarques="Jumelle de l'Escort nord-américaine ; " + IND)
mg(L, "Topaz", "Topaz", "1", "1984-01", "1994-12", [("2.3 87", "FORD-HSC-2.3", 163), ("XR5 3.0 V6 132", "FORD-VULCAN-3.0", 217, {"debut": "1992-01"})], portes=4, places=5, reservoir=58,
   remarques="Jumelle de la Ford Tempo ; " + IND)
mg(L, "Tracer", "Tracer", "1", "1987-01", "1989-12", [("1.6 83", "MAZDA-B6-1.6", 125)], portes=5, places=5, reservoir=45, remarques="Base Mazda 323 (Ford Laser) ; " + IND)
mg(L, "Tracer", "Tracer", "2", "1991-01", "1999-12", [("1.9 89", "FORD-CVH-1.9", 155, {"fin": "1996-12"}), ("LTS 1.8 129", "MAZDA-BP-1.8", 155, {"fin": "1996-12"}), ("2.0 111", "FORD-SPI-2.0", 169, {"debut": "1997-01"})],
   portes=4, places=5, reservoir=48, remarques="Jumelle de l'Escort, berline et break ; " + IND)
mg(L, "Sable", "Sable", "1", "1986-01", "1995-12", [("3.0 V6 142", "FORD-VULCAN-3.0", 217), ("3.8 V6 142", "FORD-ESSEX-3.8", 292, {"debut": "1988-01"})], portes=4, places=6, reservoir=60,
   remarques="Jumelle de la Ford Taurus, berline et break ; " + IND)
mg(L, "Sable", "Sable", "2", "1996-01", "2005-12", [("3.0 V6 147", "FORD-VULCAN-3.0", 251), ("3.0 V6 Duratec 203", "DURATEC-V6-3.0", 271)], portes=4, places=6, reservoir=68, remarques=IND)
mg(L, "Sable", "Sable", "3", "2007-09", "2009-12", [("3.5 V6 267", "DURATEC-3.5", 337)], portes=4, places=5, reservoir=72, remarques="Ex-Montego ; " + IND)
mg(L, "Mystique", "CDW27", "1", "1994-09", "2000-12", [("2.0 127", "ZETEC-2.0", 176), ("2.5 V6 172", "DURATEC-V6-2.5", 224)], portes=4, places=5, reservoir=55,
   remarques="Jumelle de la Ford Contour (base Mondeo) ; " + IND)

# ---------------------------------------------------------------- SUV, monospaces et dernières berlines
mg(L, "Villager", "Villager", "1", "1993-01", "2002-12", [("3.0 V6 153", "NISSAN-VG30-3.0", 237, {"fin": "1998-12"}), ("3.3 V6 172", "NISSAN-VG33-3.3", 271, {"debut": "1999-01"})],
   portes=5, places=7, reservoir=76, remarques="Monospace coproduit avec Nissan (Quest) ; " + IND)
mg(L, "Mountaineer", "Mountaineer", "1", "1996-09", "2010-12", [("4.0 V6 208", "FORD-COLOGNE-4.0", 346, {"debut": "1998-01"}), ("5.0 V8 218", "FORD-WINDSOR-5.0", 390, {"fin": "2001-12"}),
                                                                 ("4.6 V8 243", "MODULAR-4.6", 382, {"debut": "2002-01"})], portes=5, places=7, reservoir=85,
   remarques="Jumeau du Ford Explorer ; " + IND)
mg(L, "Marauder", "Panther", "M", "2002-09", "2004-12", [("4.6 V8 DOHC 306", "MODULAR-4.6-DOHC", 407)], portes=4, places=5, reservoir=72, remarques="Berline sportive sur base Grand Marquis ; " + IND)
mg(L, "Montego", "D3", "1", "2004-09", "2007-08", [("3.0 V6 206", "DURATEC-V6-3.0", 281)], portes=4, places=5, reservoir=72, remarques="Jumelle de la Ford Five Hundred ; " + IND)
mg(L, "Milan", "CD3", "1", "2005-09", "2011-01", [("2.3 162", "DURATEC-HE-2.3", 212, {"fin": "2009-08"}), ("3.0 V6 224", "DURATEC-V6-3.0", 278, {"fin": "2009-08"}),
                                                  ("2.5 177", "DURATEC-HE-2.5", 232, {"debut": "2009-09"}), ("3.0 V6 243", "DURATEC-V6-3.0", 302, {"debut": "2009-09"}),
                                                  ("Hybrid 2.5 194", "DURATEC-2.5-HEV", 184, {"debut": "2009-09"})], portes=4, places=5, reservoir=66,
   remarques="Jumelle de la Ford Fusion ; " + IND)
mg(L, "Mariner", "Mariner", "1", "2004-09", "2010-12", [("2.3 155", "DURATEC-HE-2.3", 204, {"fin": "2008-12"}), ("3.0 V6 203", "DURATEC-V6-3.0", 271, {"fin": "2008-12"}),
                                                         ("Hybrid 2.3 157", "DURATEC-2.3-HEV", 175, {"debut": "2006-01", "fin": "2008-12"}), ("2.5 173", "DURATEC-HE-2.5", 232, {"debut": "2009-01"}),
                                                         ("3.0 V6 243", "DURATEC-V6-3.0", 302, {"debut": "2009-01"}), ("Hybrid 2.5 179", "DURATEC-2.5-HEV", 184, {"debut": "2009-01"})],
   portes=5, places=5, reservoir=62, remarques="Jumeau du Ford Escape ; " + IND)

MOT = Motorisations("Ford", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Mercury": L}
MOTEURS = MOT.moteurs()
