"""Rolls-Royce : générations, phases, motorisations (marché européen) et moteurs liés.
Silver Ghost, 20 HP, Phantom (I à VIII), 20/25 et 25/30, Silver Wraith, Silver Dawn, Silver Cloud, Silver Shadow, Corniche,
Camargue, Silver Spirit / Silver Spur, Silver Seraph, Ghost, Wraith, Dawn, Cullinan et Spectre.
Moteurs Rolls-Royce B60 et V8 L410 repris de bentley.py, V12 BMW M73 de bmw.py (mêmes codes) ; six cylindres et V12 d'avant-guerre,
V12 6.75 (Phantom VII) et V12 biturbo 6.6 / 6.75 (BMW) ajoutés. Rolls-Royce n'a longtemps pas publié ses puissances
(« suffisante ») : valeurs d'époque estimées, données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .bentley import FAMILLES as FAMILLES_BENTLEY
from .bmw import FAMILLES as FAMILLES_BMW

E_ = "ESS"
C, SV = "CHAINE", "NC"

RR = {
    "RR-L6-7.0": f("ATM", E_, 7.0, SV, 6, 1750, 1000, "SAE30", 8.0, 2000),
    "RR-L6-3.1": f("ATM", E_, 3.1, SV, 6, 3000, 1500, "SAE30", 6.0, 3000),
    "RR-L6-3.7": f("ATM", E_, 3.7, SV, 6, 3200, 1600, "SAE30", 6.0, 3000),
    "RR-L6-4.3": f("ATM", E_, 4.3, SV, 6, 3500, 1600, "SAE30", 6.0, 3000),
    "RR-L6-7.7": f("ATM", E_, 7.7, SV, 6, 2750, 1400, "SAE30", 9.0, 3000),
    "RR-L8-5.7": f("ATM", E_, 5.7, SV, 8, 4000, 2000, "SAE30", 8.0, 3000),
    "RR-V12-7.3": f("ATM", E_, 7.3, SV, 12, 3500, 1800, "SAE30", 12.0, 3000, a="V"),
    "RR-V12-6.75": f("ATM", E_, 6.75, C, 12, 5350, 3500, "5W30", 9.5, 15000, a="V"),
    "RR-V12-6.6TT": f("TURBO", E_, 6.6, C, 12, 5250, 1500, "5W30", 9.5, 15000, a="V"),
    "RR-V12-6.75TT": f("TURBO", E_, 6.75, C, 12, 5000, 1700, "5W30", 9.5, 15000, a="V"),
    "RR-EV": electrique(),
}
BENTLEY = {k: FAMILLES_BENTLEY[k] for k in ("B60-4.3", "B60-4.6", "B60-4.9", "L410-6.2", "L410-6.75", "L410-6.75T")}
BMW = {"M73-5.4": FAMILLES_BMW["M73-5.4"]}
FAMILLES = {**RR, **BENTLEY, **BMW}


def motoriste(fam):
    return "BMW" if fam in BMW else "Rolls-Royce"


mg = SaisieMoteurs(FAMILLES, "Rolls-Royce", motoriste)
L = []
IND = "données indicatives"

# ---------------------------------------------------------------- avant-guerre
mg(L, "Silver Ghost", "40/50 HP", "1", "1906-11", "1926-12", [("7.0 L6 49", "RR-L6-7.0", 300, {"fin": "1909-12"}), ("7.4 L6 81", "RR-L6-7.0", 350, {"debut": "1910-01"})],
   portes=4, places=5, reservoir=90, remarques="40/50 HP, châssis carrossé à la demande ; 7.4 rattaché à la famille 7.0 ; " + IND)
mg(L, "20 HP", "20 HP", "1", "1922-01", "1929-12", [("3.1 L6 54", "RR-L6-3.1", 180)], portes=4, places=5, reservoir=64, remarques="Rolls-Royce « baby » ; " + IND)
mg(L, "Phantom", "Phantom I", "1", "1925-05", "1929-12", [("7.7 L6 101", "RR-L6-7.7", 400)], portes=4, places=5, reservoir=91, remarques="New Phantom ; " + IND)
mg(L, "20/25", "20/25", "1", "1929-01", "1936-12", [("3.7 L6 67", "RR-L6-3.7", 220)], portes=4, places=5, reservoir=64, remarques=IND)
mg(L, "Phantom", "Phantom II", "1", "1929-09", "1935-12", [("7.7 L6 122", "RR-L6-7.7", 430)], portes=4, places=5, reservoir=91, remarques="Dont Continental ; " + IND)
mg(L, "25/30", "25/30", "1", "1936-01", "1938-12", [("4.3 L6 101", "RR-L6-4.3", 270)], portes=4, places=5, reservoir=73, remarques="Suivie de la Wraith (1938-1939) ; " + IND)
mg(L, "Phantom", "Phantom III", "1", "1936-01", "1939-12", [("7.3 V12 167", "RR-V12-7.3", 400)], portes=4, places=5, reservoir=150, remarques="Premier V12 Rolls-Royce ; " + IND)

# ---------------------------------------------------------------- après-guerre
mg(L, "Silver Wraith", "Silver Wraith", "1", "1946-01", "1959-12",
   [("4.3 L6 126", "B60-4.3", 270, {"fin": "1951-12"}), ("4.6 L6 136", "B60-4.6", 300, {"debut": "1951-01", "fin": "1955-12"}), ("4.9 L6 155", "B60-4.9", 330, {"debut": "1955-01"})],
   portes=4, places=5, reservoir=82, remarques="Châssis carrossé (Hooper, Park Ward, H.J. Mulliner) ; " + IND)
mg(L, "Silver Dawn", "Silver Dawn", "1", "1949-01", "1955-12", [("4.3 L6 126", "B60-4.3", 270, {"fin": "1951-12"}), ("4.6 L6 136", "B60-4.6", 300, {"debut": "1951-06"})],
   portes=4, places=5, reservoir=82, remarques="Jumelle de la Bentley Mk VI / R-Type ; " + IND)
mg(L, "Phantom", "Phantom IV", "1", "1950-01", "1956-12", [("5.7 L8 166", "RR-L8-5.7", 380)],
   portes=4, places=6, reservoir=91, remarques="18 exemplaires réservés aux familles royales et chefs d'État ; " + IND)
mg(L, "Silver Cloud", "Silver Cloud I", "1", "1955-04", "1959-08", [("4.9 L6 178", "B60-4.9", 350)], portes=4, places=5, reservoir=82, remarques="Jumelle de la Bentley S1 ; " + IND)
mg(L, "Silver Cloud", "Silver Cloud II", "1", "1959-08", "1962-09", [("6.2 V8 200", "L410-6.2", 450)], portes=4, places=5, reservoir=82, remarques=IND)
mg(L, "Silver Cloud", "Silver Cloud III", "1", "1962-10", "1966-09", [("6.2 V8 220", "L410-6.2", 450)], portes=4, places=5, reservoir=82, remarques=IND)
mg(L, "Phantom", "Phantom V", "1", "1959-09", "1968-12", [("6.2 V8 200", "L410-6.2", 450)], portes=4, places=7, reservoir=105, remarques="Limousine ; " + IND)
mg(L, "Phantom", "Phantom VI", "1", "1968-10", "1991-12", [("6.2 V8 220", "L410-6.2", 450, {"fin": "1978-12"}), ("6.75 V8 220", "L410-6.75", 500, {"debut": "1979-01"})],
   portes=4, places=7, reservoir=105, remarques="Limousine ; " + IND)
mg(L, "Silver Shadow", "Silver Shadow", "1", "1965-10", "1980-12", [("6.2 V8 200", "L410-6.2", 450, {"fin": "1970-06"}), ("6.75 V8 220", "L410-6.75", 500, {"debut": "1970-07"})],
   portes=4, places=5, reservoir=109, remarques="Silver Shadow I et II (1977), Silver Wraith II à empattement long ; " + IND)
mg(L, "Corniche", "Corniche", "1", "1971-03", "1995-12", [("6.75 V8 220", "L410-6.75", 500), ("Corniche S 6.75 V8 Turbo 360", "L410-6.75T", 650, {"debut": "1995-01"})],
   portes=2, places=4, reservoir=107, remarques="Coupé (jusqu'en 1982) et cabriolet ; Corniche II à IV ; " + IND)
mg(L, "Camargue", "Camargue", "1", "1975-03", "1986-12", [("6.75 V8 220", "L410-6.75", 500)], portes=2, places=4, reservoir=107, remarques="Coupé dessiné par Pininfarina ; " + IND)
mg(L, "Silver Spirit", "SZ", "1", "1980-10", "1999-12",
   [("6.75 V8 220", "L410-6.75", 500, {"fin": "1993-06"}), ("6.75 V8 240", "L410-6.75", 500, {"debut": "1993-07"}), ("Park Ward 6.75 V8 Turbo 300", "L410-6.75T", 610, {"debut": "1996-06"})],
   portes=4, places=5, reservoir=108, remarques="Silver Spirit, Silver Spur (empattement long), Silver Dawn (1994-1998) ; " + IND)
mg(L, "Silver Seraph", "Silver Seraph", "1", "1998-03", "2002-12", [("5.4 V12 326", "M73-5.4", 490)], portes=4, places=5, reservoir=95,
   remarques="V12 BMW ; dont Park Ward (empattement long)")
mg(L, "Corniche", "Corniche V", "1", "2000-01", "2002-12", [("6.75 V8 Turbo 325", "L410-6.75T", 610)], portes=2, places=4, reservoir=95, remarques="Cabriolet, environ 370 ex.")

# ---------------------------------------------------------------- ère BMW
mg(L, "Phantom", "Phantom VII", "1", "2003-01", "2012-12", [("6.75 V12 460", "RR-V12-6.75", 720)], portes=4, places=5, reservoir=100,
   remarques="Berline, EWB (empattement long), Drophead Coupé (2007) et Coupé (2008)")
mg(L, "Phantom", "Phantom VII", "2", "2013-01", "2017-12", [("6.75 V12 460", "RR-V12-6.75", 720)], portes=4, places=5, reservoir=100, remarques="Series II")
mg(L, "Phantom", "Phantom VIII", "1", "2017-12", "2022-12", [("6.75 V12 Biturbo 571", "RR-V12-6.75TT", 850)], portes=4, places=5, reservoir=100,
   remarques="Berline et EWB (empattement long) ; couple réel 900 Nm (code moteur commun avec Ghost / Cullinan)")
mg(L, "Phantom", "Phantom VIII", "2", "2023-01", None, [("6.75 V12 Biturbo 571", "RR-V12-6.75TT", 850)], portes=4, places=5, reservoir=100, remarques="Series II ; berline et EWB")
mg(L, "Ghost", "Ghost I", "1", "2009-09", "2014-08", [("6.6 V12 Biturbo 570", "RR-V12-6.6TT", 780)], portes=4, places=5, reservoir=82, remarques="Dont EWB (2011)")
mg(L, "Ghost", "Ghost I", "2", "2014-09", "2020-08", [("6.6 V12 Biturbo 570", "RR-V12-6.6TT", 780), ("Black Badge 6.6 V12 Biturbo 612", "RR-V12-6.6TT", 840, {"debut": "2016-03"})],
   portes=4, places=5, reservoir=82, remarques="Series II ; dont EWB")
mg(L, "Ghost", "Ghost II", "1", "2020-09", "2024-09",
   [("6.75 V12 Biturbo 571", "RR-V12-6.75TT", 850), ("Black Badge 6.75 V12 Biturbo 600", "RR-V12-6.75TT", 900, {"debut": "2021-10"})], portes=4, places=5, reservoir=90,
   remarques="Transmission intégrale ; dont EWB")
mg(L, "Ghost", "Ghost II", "2", "2024-10", None,
   [("6.75 V12 Biturbo 571", "RR-V12-6.75TT", 850), ("Black Badge 6.75 V12 Biturbo 600", "RR-V12-6.75TT", 900)], portes=4, places=5, reservoir=90, remarques="Series II ; dont EWB")
mg(L, "Wraith", "Wraith", "1", "2013-09", "2023-04", [("6.6 V12 Biturbo 632", "RR-V12-6.6TT", 800), ("Black Badge 6.6 V12 Biturbo 632", "RR-V12-6.6TT", 800, {"debut": "2016-03"})],
   portes=2, places=4, reservoir=83, remarques="Coupé fastback ; Black Badge : couple porté à 870 Nm")
mg(L, "Dawn", "Dawn", "1", "2015-09", "2023-04", [("6.6 V12 Biturbo 571", "RR-V12-6.6TT", 820), ("Black Badge 6.6 V12 Biturbo 601", "RR-V12-6.6TT", 840, {"debut": "2017-03"})],
   portes=2, places=4, reservoir=83, remarques="Cabriolet 4 places")
mg(L, "Cullinan", "Cullinan", "1", "2018-05", "2024-04",
   [("6.75 V12 Biturbo 571", "RR-V12-6.75TT", 850), ("Black Badge 6.75 V12 Biturbo 600", "RR-V12-6.75TT", 900, {"debut": "2019-10"})], portes=5, places=5, reservoir=100,
   remarques="SUV, transmission intégrale")
mg(L, "Cullinan", "Cullinan", "2", "2024-05", None,
   [("6.75 V12 Biturbo 571", "RR-V12-6.75TT", 850), ("Black Badge 6.75 V12 Biturbo 600", "RR-V12-6.75TT", 900)], portes=5, places=5, reservoir=100, remarques="Series II")
mg(L, "Spectre", "Spectre", "1", "2023-10", None,
   [("Électrique 584", "RR-EV", 900, {"reservoir": 0, "batterie": 102}), ("Black Badge Électrique 659", "RR-EV", 1075, {"reservoir": 0, "batterie": 102, "debut": "2025-03"})],
   portes=2, places=4, reservoir=0, remarques="Coupé électrique")

MOT = Motorisations("Rolls-Royce", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Rolls-Royce": L}
MOTEURS = MOT.moteurs()
