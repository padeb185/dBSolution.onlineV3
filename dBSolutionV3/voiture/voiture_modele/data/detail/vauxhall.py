"""Vauxhall (marché britannique) : générations, phases, motorisations et moteurs liés.
Vauxhall propre (1903-1980) : 5 HP, Prince Henry, 30-98, 14/40, 20/60, Cadet, Light Six, 10-4, 12-4, 14-6, 25, Wyvern, Velox, Cresta,
Victor, Viva, Ventora, Viscount, Firenza, Magnum, Chevette, Viceroy. Lotus Carlton, Signum, Monaro et VXR8 (Holden / HSV) saisis ici.
Depuis 1975-1980, les Vauxhall sont des Opel rebaptisées : leurs générations sont reprises d'opel.py (mêmes variantes, mêmes
moteurs et codes, dates alignées sur Opel sauf lancement britannique différent) sous le nom Vauxhall : Astra (Kadett D / E puis
Astra), Nova (Corsa A), Cavalier (Ascona B / C, Vectra A), Carlton (Rekord E, Omega A), Royale et Senator, Omega, Vectra, Insignia,
Corsa, Tigra, Calibra, Zafira, Meriva, Agila, Adam, Viva (Karl), Cascada, VX220 (Speedster), Frontera, Antara, Mokka, Crossland,
Grandland, Ampera ; OPC renommées VXR. Puissances en ch (bhp × 1,014). Données anciennes indicatives. Utilitaires non repris.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
import copy

from ._outil import Motorisations, SaisieMoteurs, famille as f
from . import opel
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET

E_ = "ESS"
C, B = "CHAINE", "COURROIE"

VX = {
    "VX-1C-1.0": f("ATM", E_, 1.0, "NC", 1, 1000, 800, "SAE30", 1.5, 1000),
    "VX-L4-3.0": f("ATM", E_, 3.0, "NC", 4, 2800, 1800, "SAE30", 6.0, 2000),
    "VX-L4-4.0": f("ATM", E_, 4.0, "NC", 4, 2500, 1600, "SAE30", 7.0, 2000),
    "VX-L4-4.5": f("ATM", E_, 4.5, "NC", 4, 2800, 1800, "SAE30", 8.0, 2000),
    "VX-L4-4.2": f("ATM", E_, 4.2, "NC", 4, 3300, 2000, "SAE30", 8.0, 2000),
    "VX-L4-2.3": f("ATM", E_, 2.3, "NC", 4, 2800, 1600, "SAE30", 5.0, 2000),
    "VX-L6-2.8": f("ATM", E_, 2.8, "NC", 6, 3300, 1800, "SAE30", 6.0, 2000),
    "VX-L6-2.0": f("ATM", E_, 2.0, "NC", 6, 3300, 1800, "SAE30", 5.0, 3000),
    "VX-L6-3.2": f("ATM", E_, 3.2, "NC", 6, 3600, 2000, "SAE30", 6.0, 3000),
    "VX-L6-1.5": f("ATM", E_, 1.5, "NC", 6, 3800, 2400, "SAE30", 4.5, 3000),
    "VX-L6-1.8": f("ATM", E_, 1.8, "NC", 6, 3600, 2200, "SAE30", 4.5, 3000),
    "VX-L4-1.2": f("ATM", E_, 1.2, "NC", 4, 3600, 2200, "SAE30", 3.5, 3000),
    "VX-L4-1.4": f("ATM", E_, 1.4, "NC", 4, 3600, 2200, "SAE30", 3.5, 3000),
    "VX-L4-1.5": f("ATM", E_, 1.5, C, 4, 4200, 2400, "20W50", 4.0, 5000),
    "VX-L4-1.6": f("ATM", E_, 1.6, C, 4, 4800, 2800, "20W50", 4.0, 5000),
    "VX-L6-2.3": f("ATM", E_, 2.3, C, 6, 4400, 2400, "20W50", 5.0, 5000),
    "VX-L6-2.6": f("ATM", E_, 2.6, C, 6, 4800, 2400, "20W50", 5.0, 5000),
    "VX-L6-3.3": f("ATM", E_, 3.3, C, 6, 4600, 2400, "20W50", 5.5, 5000),
    "VX-OHV-1.1": f("ATM", E_, 1.1, C, 4, 5000, 2800, "20W50", 3.0, 5000),
    "VX-OHV-1.2": f("ATM", E_, 1.2, C, 4, 5200, 3000, "20W50", 3.0, 5000),
    "VX-OHV-1.3": f("ATM", E_, 1.3, C, 4, 5400, 3000, "20W50", 3.0, 6000),
    "VX-SL-1.6": f("ATM", E_, 1.6, B, 4, 5600, 3000, "20W50", 4.0, 6000),
    "VX-SL-1.8": f("ATM", E_, 1.8, B, 4, 5200, 3000, "20W50", 4.0, 6000),
    "VX-SL-2.0": f("ATM", E_, 2.0, B, 4, 5500, 3200, "20W50", 4.0, 6000),
    "VX-SL-2.3": f("ATM", E_, 2.3, B, 4, 5000, 3000, "20W50", 4.0, 6000),
    "VX-SL-2.3-16V": f("ATM", E_, 2.3, B, 4, 5500, 4500, "20W50", 4.5, 6000),
    "LOTUS-C36GET-3.6": f("TURBO", E_, 3.6, C, 6, 5200, 4200, "10W40", 7.0, 10000),
}
GM_V8 = {k: FAMILLES_CHEVROLET[k] for k in ("LS1-5.7", "LS2-6.0", "LS3-6.2", "LSA-6.2SC")}
FAMILLES = {**opel.FAMILLES, **VX, **GM_V8}


def motoriste(fam):
    if fam in GM_V8:
        return "Chevrolet"
    if fam == "LOTUS-C36GET-3.6":
        return "Lotus"
    if fam in VX:
        return "Vauxhall"
    return opel.motoriste(fam)


mg = SaisieMoteurs(FAMILLES, "Vauxhall", motoriste)
L = []
IND = "données indicatives"

# ---------------------------------------------------------------- Vauxhall d'avant-guerre
mg(L, "5 HP", "5 HP", "1", "1903-01", "1904-12", [("1.0 5", "VX-1C-1.0", 25)], portes=0, places=2, reservoir=15,
   remarques="Première Vauxhall (Londres), monocylindre ; " + IND)
mg(L, "Prince Henry", "C-Type", "1", "1911-01", "1914-12", [("3.0 61", "VX-L4-3.0", 180), ("4.0 76", "VX-L4-4.0", 230, {"debut": "1913-01"})], portes=0, places=4, reservoir=70,
   remarques="Torpédo sportive, souvent citée comme première voiture de sport ; " + IND)
mg(L, "D-Type", "D-Type", "1", "1912-01", "1922-12", [("4.0 61", "VX-L4-4.0", 200)], portes=4, places=5, reservoir=70, remarques="Voiture d'état-major britannique de la Grande Guerre ; " + IND)
mg(L, "30-98", "30-98", "1", "1913-01", "1927-12", [("E 4.5 91", "VX-L4-4.5", 300, {"fin": "1922-12"}), ("OE 4.2 114", "VX-L4-4.2", 300, {"debut": "1923-01"})],
   portes=0, places=4, reservoir=80, remarques="Grand tourisme sportif (Velox) ; " + IND)
mg(L, "14/40", "M-Type", "1", "1922-01", "1927-12", [("2.3 41", "VX-L4-2.3", 120)], portes=4, places=5, reservoir=50, remarques=IND)
mg(L, "20/60", "R-Type", "1", "1927-01", "1930-12", [("2.8 61", "VX-L6-2.8", 170)], portes=4, places=5, reservoir=60, remarques="Première Vauxhall de l'ère General Motors (rachat 1925) ; " + IND)
mg(L, "Cadet", "VY / VX", "1", "1930-10", "1933-12", [("17 HP 2.0 49", "VX-L6-2.0", 130), ("26 HP 3.2 61", "VX-L6-3.2", 180)], portes=4, places=5, reservoir=50,
   remarques="Première voiture britannique à boîte synchronisée ; " + IND)
mg(L, "Light Six", "ASX / ASY", "1", "1933-01", "1938-12", [("12 HP 1.5 42", "VX-L6-1.5", 95), ("14 HP 1.8 49", "VX-L6-1.8", 110)], portes=4, places=5, reservoir=40, remarques=IND)
mg(L, "10-4", "H-Type", "1", "1937-10", "1940-12", [("1.2 32", "VX-L4-1.2", 72)], portes=4, places=4, reservoir=30,
   remarques="Première Vauxhall à caisse autoporteuse ; 12-4 (I-Type) 1.4 ; " + IND)
mg(L, "12-4", "I-Type", "1", "1938-01", "1940-12", [("1.4 35", "VX-L4-1.4", 82)], portes=4, places=5, reservoir=36, remarques=IND)
mg(L, "14-6", "J-Type", "1", "1938-01", "1948-12", [("1.8 49", "VX-L6-1.8", 110)], portes=4, places=5, reservoir=45, remarques="Production interrompue pendant la guerre ; " + IND)
mg(L, "25", "G-Type", "1", "1937-01", "1940-12", [("3.2 81", "VX-L6-3.2", 210)], portes=4, places=5, reservoir=60, remarques=IND)

# ---------------------------------------------------------------- années 1948-1972
mg(L, "Wyvern", "L-Type", "1", "1948-09", "1951-07", [("1.4 35", "VX-L4-1.4", 82)], portes=4, places=5, reservoir=36, remarques=IND)
mg(L, "Wyvern", "E-Type", "1", "1951-08", "1957-12", [("1.5 41", "VX-L4-1.5", 95)], portes=4, places=5, reservoir=45, remarques=IND)
mg(L, "Velox", "L-Type", "1", "1948-09", "1951-07", [("2.3 55", "VX-L6-2.3", 140)], portes=4, places=5, reservoir=36, remarques=IND)
mg(L, "Velox", "E-Type", "1", "1951-08", "1957-12", [("2.3 56", "VX-L6-2.3", 145, {"fin": "1955-07"}), ("2.3 65", "VX-L6-2.3", 160, {"debut": "1955-08"})], portes=4, places=5, reservoir=45,
   remarques=IND)
mg(L, "Cresta", "E-Type", "1", "1954-10", "1957-12", [("2.3 65", "VX-L6-2.3", 160)], portes=4, places=5, reservoir=45, remarques="Version luxe de la Velox ; " + IND)
mg(L, "Cresta", "PA", "1", "1957-10", "1962-08", [("2.3 84", "VX-L6-2.3", 167, {"fin": "1960-07"}), ("2.6 96", "VX-L6-2.6", 190, {"debut": "1960-08"})], portes=4, places=6, reservoir=50,
   remarques="Velox et Cresta PA (style américain), berline et break Friary ; " + IND)
mg(L, "Cresta", "PB", "1", "1962-10", "1965-09", [("2.6 96", "VX-L6-2.6", 190), ("3.3 117", "VX-L6-3.3", 235, {"debut": "1964-09"})], portes=4, places=6, reservoir=55,
   remarques="Velox et Cresta PB ; " + IND)
mg(L, "Cresta", "PC", "1", "1965-10", "1972-06", [("3.3 125", "VX-L6-3.3", 239)], portes=4, places=6, reservoir=64, remarques="Dont Viscount (1966-1972) ; " + IND)
mg(L, "Viscount", "PC", "1", "1966-06", "1972-06", [("3.3 125", "VX-L6-3.3", 239)], portes=4, places=6, reservoir=64, remarques="Version de luxe de la Cresta PC ; " + IND)
mg(L, "Victor", "F", "1", "1957-02", "1961-08", [("1.5 56", "VX-L4-1.5", 105)], portes=4, places=5, reservoir=36, remarques="Victor F Series I et II, berline et break ; " + IND)
mg(L, "Victor", "FB", "1", "1961-09", "1964-09", [("1.5 57", "VX-L4-1.5", 108), ("VX4/90 1.5 72", "VX-L4-1.5", 113), ("1.6 60", "VX-L4-1.6", 115, {"debut": "1963-09"})],
   portes=4, places=5, reservoir=45, remarques=IND)
mg(L, "Victor", "FC 101", "1", "1964-10", "1967-09", [("1.6 71", "VX-L4-1.6", 122), ("VX4/90 1.6 86", "VX-L4-1.6", 125)], portes=4, places=5, reservoir=55, remarques=IND)
mg(L, "Victor", "FD", "1", "1967-10", "1972-02", [("1.6 73", "VX-SL-1.6", 121), ("2.0 105", "VX-SL-2.0", 159), ("VX4/90 2.0 106", "VX-SL-2.0", 160, {"debut": "1969-10"})],
   portes=4, places=5, reservoir=55, remarques="Premier moteur Vauxhall « slant four » à arbre à cames en tête entraîné par courroie ; " + IND)
mg(L, "Victor", "FE", "1", "1972-03", "1978-12", [("1.8 78", "VX-SL-1.8", 140), ("2.3 110", "VX-SL-2.3", 189), ("VX4/90 2.3 112", "VX-SL-2.3", 190, {"fin": "1976-12"}),
                                                   ("VX 2300 2.3 110", "VX-SL-2.3", 189, {"debut": "1976-01"})],
   portes=4, places=5, reservoir=55, remarques="Victor FE puis VX 1800 / 2300 (1976) ; " + IND)
mg(L, "Ventora", "FD / FE", "1", "1968-02", "1976-12", [("3.3 125", "VX-L6-3.3", 239)], portes=4, places=5, reservoir=55, remarques="Victor à six cylindres Cresta ; " + IND)
mg(L, "Viva", "HA", "1", "1963-09", "1966-09", [("1.1 45", "VX-OHV-1.1", 76)], portes=2, places=4, reservoir=27, remarques=IND)
mg(L, "Viva", "HB", "1", "1966-09", "1970-08", [("1.2 48", "VX-OHV-1.2", 80), ("SL90 1.2 61", "VX-OHV-1.2", 86), ("1.6 84", "VX-SL-1.6", 129, {"debut": "1968-01"})],
   portes=2, places=4, reservoir=36, remarques="Berline 2 et 4 portes, break ; " + IND)
mg(L, "Viva", "HC", "1", "1970-10", "1979-07", [("1.2 50", "VX-OHV-1.2", 82, {"fin": "1971-12"}), ("1.3 54", "VX-OHV-1.3", 89, {"debut": "1971-09"}), ("1800 1.8 78", "VX-SL-1.8", 140, {"debut": "1972-03", "fin": "1973-12"})],
   portes=2, places=4, reservoir=36, remarques="Berline 2 et 4 portes, break ; " + IND)
mg(L, "Firenza", "HC", "1", "1971-05", "1975-12", [("1.3 54", "VX-OHV-1.3", 89), ("1.6 70", "VX-SL-1.6", 117, {"fin": "1972-02"}), ("2.0 96", "VX-SL-2.0", 152, {"fin": "1972-02"}),
                                                    ("1.8 78", "VX-SL-1.8", 140, {"debut": "1972-03"}), ("2.3 110", "VX-SL-2.3", 189, {"debut": "1972-03"}),
                                                    ("HP 2.3 133", "VX-SL-2.3", 196, {"debut": "1973-09", "remarques": "Firenza HP « Droopsnoot » ; " + IND})],
   portes=2, places=4, reservoir=55, remarques="Coupé de la Viva HC ; " + IND)
mg(L, "Magnum", "HC", "1", "1973-02", "1978-12", [("1.8 78", "VX-SL-1.8", 140), ("2.3 110", "VX-SL-2.3", 189)], portes=4, places=4, reservoir=55,
   remarques="Berline, coupé et break ; " + IND)
mg(L, "Chevette", "Chevette", "1", "1975-05", "1984-01", [("1.3 59", "VX-OHV-1.3", 92), ("HS 2.3 16V 137", "VX-SL-2.3-16V", 182, {"debut": "1978-01", "fin": "1980-12"})],
   portes=3, places=4, reservoir=38, remarques="3 et 5 portes, berline, break ; base GM T-Car (Opel Kadett C) ; Chevette HS homologation rallye ; " + IND)
mg(L, "Viceroy", "Viceroy", "1", "1980-02", "1982-07", [("2.5 115", "CIH6-2.5", 172)], portes=4, places=5, reservoir=70,
   remarques="Opel Commodore C vendue par Vauxhall ; " + IND)

# ---------------------------------------------------------------- Lotus Carlton, Signum, Monaro, VXR8
mg(L, "Lotus Carlton", "Carlton Mk2", "L", "1990-11", "1992-12", [("3.6 Biturbo 382", "LOTUS-C36GET-3.6", 568)], portes=4, places=5, reservoir=75,
   remarques="Préparée par Lotus (Lotus Omega en Europe continentale), six cylindres biturbo, 440 exemplaires Vauxhall ; " + IND)
mg(L, "Signum", "Signum", "1", "2003-05", "2008-09",
   [("1.8 122", "FAM2-1.8", 165), ("2.2 155", "FAM2-2.2", 220), ("3.2 V6 211", "Y32SE-3.2V6", 300, {"fin": "2005-08"}), ("2.8 V6 Turbo 230", "Z28NET-2.8V6T", 330, {"debut": "2005-09"}),
    ("1.9 CDTi 120", "FIAT-1.9TID", 280, {"debut": "2004-01"}), ("1.9 CDTi 150", "FIAT-1.9TID", 320, {"debut": "2004-01"})],
   portes=5, places=5, reservoir=61, remarques="Grande routière 5 portes sur base Vectra C ; 3.0 V6 CDTi non repris ; " + IND)
mg(L, "Monaro", "V2", "1", "2004-01", "2006-12", [("CV8 5.7 V8 335", "LS1-5.7", 465, {"fin": "2005-06"}), ("VXR 6.0 V8 406", "LS2-6.0", 542, {"debut": "2005-01"})],
   portes=2, places=4, reservoir=75, remarques="Coupé Holden Monaro importé d'Australie ; " + IND)
mg(L, "VXR8", "VE", "1", "2007-03", "2013-06", [("6.0 V8 417", "LS2-6.0", 550, {"fin": "2008-06"}), ("6.2 V8 431", "LS3-6.2", 550, {"debut": "2008-07"})],
   portes=4, places=5, reservoir=75, remarques="Berline HSV Clubsport (Holden Commodore VE) ; dont VXR8 Bathurst S ; " + IND)
mg(L, "VXR8", "VF", "1", "2013-09", "2017-12", [("GTS 6.2 V8 Compresseur 585", "LSA-6.2SC", 740)], portes=4, places=5, reservoir=71,
   remarques="HSV GTS (Holden Commodore VF), dont GTS-R ; " + IND)

# ---------------------------------------------------------------- générations reprises d'Opel
# (modèle Opel, génération Opel) -> (modèle Vauxhall, génération Vauxhall, début, fin, variantes exclues)
REPRISES = {
    ("Ascona", "Ascona B"): ("Cavalier", "Cavalier Mk1", "1975-08", "1981-08", ("400 2.4 144",)),
    ("Ascona", "Ascona C"): ("Cavalier", "Cavalier Mk2", None, None, ()),
    ("Vectra", "Vectra A"): ("Cavalier", "Cavalier Mk3", None, None, ()),
    ("Rekord", "Rekord E"): ("Carlton", "Carlton Mk1", "1978-10", "1986-08", ()),
    ("Omega", "Omega A"): ("Carlton", "Carlton Mk2", None, "1994-03", ()),
    ("Senator", "Senator A"): ("Senator", "Royale / Senator A", "1978-11", None, ()),
    ("Monza", "Monza"): ("Royale Coupé", "Royale Coupé", "1978-11", "1982-12", ()),
    ("Senator", "Senator B"): ("Senator", "Senator B", None, None, ()),
    ("Omega", "Omega B"): ("Omega", "Omega B", None, None, ()),
    ("Kadett", "Kadett D"): ("Astra", "Astra Mk1 (D)", "1980-02", None, ()),
    ("Kadett", "Kadett E"): ("Astra", "Astra Mk2 (E)", None, None, ()),
    ("Astra", "Astra F"): ("Astra", "Astra Mk3 (F)", None, None, ()),
    ("Astra", "Astra G"): ("Astra", "Astra Mk4 (G)", None, None, ()),
    ("Astra", "Astra H"): ("Astra", "Astra Mk5 (H)", None, None, ()),
    ("Astra", "Astra J"): ("Astra", "Astra Mk6 (J)", None, None, ()),
    ("Astra", "Astra K"): ("Astra", "Astra Mk7 (K)", None, None, ()),
    ("Astra", "Astra L"): ("Astra", "Astra Mk8 (L)", None, None, ()),
    ("Corsa", "Corsa A"): ("Nova", "Nova", "1983-04", None, ()),
    ("Corsa", "Corsa B"): ("Corsa", "Corsa B", None, None, ()),
    ("Corsa", "Corsa C"): ("Corsa", "Corsa C", None, None, ()),
    ("Corsa", "Corsa D"): ("Corsa", "Corsa D", None, None, ()),
    ("Corsa", "Corsa E"): ("Corsa", "Corsa E", None, None, ()),
    ("Corsa", "Corsa F"): ("Corsa", "Corsa F", None, None, ()),
    ("Tigra", "Tigra A"): ("Tigra", "Tigra A", None, None, ()),
    ("Tigra", "Tigra TwinTop"): ("Tigra", "Tigra TwinTop", None, None, ()),
    ("Calibra", "Calibra"): ("Calibra", "Calibra", None, None, ()),
    ("Vectra", "Vectra B"): ("Vectra", "Vectra B", None, None, ()),
    ("Vectra", "Vectra C"): ("Vectra", "Vectra C", None, None, ()),
    ("Insignia", "Insignia A"): ("Insignia", "Insignia A", None, None, ()),
    ("Insignia", "Insignia B"): ("Insignia", "Insignia B", None, None, ()),
    ("Zafira", "Zafira A"): ("Zafira", "Zafira A", None, None, ()),
    ("Zafira", "Zafira B"): ("Zafira", "Zafira B", None, None, ()),
    ("Zafira", "Zafira C"): ("Zafira Tourer", "Zafira Tourer", None, None, ()),
    ("Meriva", "Meriva A"): ("Meriva", "Meriva A", None, None, ()),
    ("Meriva", "Meriva B"): ("Meriva", "Meriva B", None, None, ()),
    ("Agila", "Agila A"): ("Agila", "Agila A", None, None, ()),
    ("Agila", "Agila B"): ("Agila", "Agila B", None, None, ()),
    ("Adam", "Adam"): ("Adam", "Adam", None, None, ()),
    ("Karl", "Karl"): ("Viva", "Viva (2015)", None, None, ()),
    ("Cascada", "Cascada"): ("Cascada", "Cascada", None, None, ()),
    ("Speedster", "Speedster"): ("VX220", "VX220", None, None, ()),
    ("Frontera", "Frontera A"): ("Frontera", "Frontera A", None, None, ()),
    ("Frontera", "Frontera B"): ("Frontera", "Frontera B", None, None, ()),
    ("Frontera", "Frontera (2024)"): ("Frontera", "Frontera (2024)", None, None, ()),
    ("Antara", "Antara"): ("Antara", "Antara", None, None, ()),
    ("Mokka", "Mokka A"): ("Mokka", "Mokka / Mokka X", None, None, ()),
    ("Mokka", "Mokka B"): ("Mokka", "Mokka B", None, None, ()),
    ("Crossland", "Crossland"): ("Crossland", "Crossland X / Crossland", None, None, ()),
    ("Grandland", "Grandland X"): ("Grandland", "Grandland X", None, None, ()),
    ("Grandland", "Grandland (2024)"): ("Grandland", "Grandland (2024)", None, None, ()),
    ("Ampera", "Ampera"): ("Ampera", "Ampera", None, None, ()),
    # OPC -> VXR / GSi / GSe
    ("Astra OPC", "Astra H OPC"): ("Astra VXR", "Astra H VXR", None, None, ()),
    ("Astra OPC", "Astra J OPC"): ("Astra VXR", "Astra J VXR", None, None, ()),
    ("Corsa OPC", "Corsa D OPC"): ("Corsa VXR", "Corsa D VXR", None, None, ()),
    ("Corsa OPC", "Corsa E OPC"): ("Corsa VXR", "Corsa E VXR", None, None, ()),
    ("Vectra OPC", "Vectra C OPC"): ("Vectra VXR", "Vectra C VXR", None, None, ()),
    ("Insignia OPC", "Insignia A OPC"): ("Insignia VXR", "Insignia A VXR", None, None, ()),
    ("Insignia GSi", "Insignia B GSi"): ("Insignia GSi", "Insignia B GSi", None, None, ()),
    ("Meriva OPC", "Meriva A OPC"): ("Meriva VXR", "Meriva A VXR", None, None, ()),
    ("Zafira OPC", "Zafira A OPC"): ("Zafira GSi", "Zafira A GSi", None, None, ()),
    ("Zafira OPC", "Zafira B OPC"): ("Zafira VXR", "Zafira B VXR", None, None, ()),
    ("Astra GSe", "Astra L GSe"): ("Astra GSe", "Astra L GSe", None, None, ()),
    ("Grandland GSe", "Grandland X GSe"): ("Grandland GSe", "Grandland X GSe", None, None, ()),
    ("Mokka GSE", "Mokka B GSE"): ("Mokka GSE", "Mokka B GSE", None, None, ()),
    ("Corsa GSE", "Corsa F GSE"): ("Corsa GSE", "Corsa F GSE", None, None, ()),
}


def _am(txt):
    a, m = txt.split("-")
    return int(a), int(m)


def reprendre(source):
    """Copie les générations Opel listées dans REPRISES sous leur nom Vauxhall (mêmes variantes et moteurs)."""
    for d in source:
        cle = (d["modele"], d["generation"])
        if cle not in REPRISES:
            continue
        modele, gen, debut, fin, exclues = REPRISES[cle]
        if d["variante"] in exclues:
            continue
        n = copy.deepcopy(d)
        n.pop("moteurs", None)
        if debut:
            a, m = _am(debut)
            if (n.get("annee_fin"), n.get("mois_fin") or 12) < (a, m) and n.get("annee_fin"):
                continue
            if (n.get("annee_debut"), n.get("mois_debut") or 1) < (a, m):
                n["annee_debut"], n["mois_debut"] = a, m
        if fin:
            a, m = _am(fin)
            if (n.get("annee_debut"), n.get("mois_debut") or 1) > (a, m):
                continue
            if not n.get("annee_fin") or (n["annee_fin"], n.get("mois_fin") or 12) > (a, m):
                n["annee_fin"], n["mois_fin"] = a, m
        n["modele"], n["generation"] = modele, gen
        base = f"Version Vauxhall de l'Opel {d['generation']}"
        n["remarques"] = base + (" ; " + d["remarques"] if d.get("remarques") else "")
        ancienne, nouvelle = f"{d['generation']}-{d['phase']}", f"{gen}-{d['phase']}"
        mg.eres[(gen, d["phase"])] = nouvelle
        mg.table[f"{d['variante']}@{nouvelle}"] = opel.mg.table[f"{d['variante']}@{ancienne}"]
        L.append(n)


reprendre(opel.L)
reprendre(opel.OPC)

MOT = Motorisations("Vauxhall", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Vauxhall": L}
MOTEURS = MOT.moteurs()
