"""DKW : générations, phases, motorisations (marché européen) et moteurs liés.
Avant-guerre (Zschopau / Zwickau) : F1, F5, F7, F8 (bicylindres deux-temps) et Sonderklasse (V4) ; après-guerre (Ingolstadt /
Düsseldorf, Auto Union) : F89 Meisterklasse, F91 Sonderklasse, F93, Junior, F12, F102 et Munga. Moteurs deux-temps : distribution
« aucune », huile « à choisir » (mélange). Trois cylindres 1.0 du Munga repris d'auto_union.py (même famille). Puissances en ch DIN.
Données indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .auto_union import FAMILLES as FAMILLES_AU

E_ = "ESS"


def dt(l, n, rpm, nmrpm, a="EN_LIGNE"):
    return f("ATM", E_, l, "AUCUNE", n, rpm, nmrpm, "CHOISIR", 0.0, 5000, a=a)


DKW = {
    "DKW-2T-0.5": dt(0.49, 2, 3500, 2500), "DKW-2T-0.6": dt(0.58, 2, 3500, 2500), "DKW-2T-0.7": dt(0.69, 2, 3500, 2500), "DKW-V4-2T-1.05": dt(1.05, 4, 3500, 2500, a="V"),
    "DKW-2T-0.9": dt(0.9, 3, 4000, 2500), "DKW-2T-0.75": dt(0.74, 3, 4300, 3000), "DKW-2T-0.8": dt(0.8, 3, 4300, 3000),
    "DKW-2T-1.2": dt(1.18, 3, 4500, 2500),
}
AU = {"AU-2T-1.0": FAMILLES_AU["AU-2T-1.0"]}
FAMILLES = {**DKW, **AU}
mg = SaisieMoteurs(FAMILLES, "DKW", lambda fam: "Auto Union" if fam in AU else "DKW")
L = []
IND = "deux-temps ; données indicatives (marque ancienne), à vérifier"

mg(L, "F1", "F1", "1", "1931-01", "1932-12", [("0.5 15", "DKW-2T-0.5", 35)], portes=2, places=2, reservoir=25, remarques="Première traction DKW, roadster et berline ; " + IND)
mg(L, "F5", "F5", "1", "1935-01", "1937-12", [("0.6 18", "DKW-2T-0.6", 45), ("0.7 20", "DKW-2T-0.7", 50)], portes=2, places=4, reservoir=30,
   remarques="Reichsklasse (0.6) et Meisterklasse (0.7), berline, cabriolet, roadster ; " + IND)
mg(L, "F7", "F7", "1", "1937-01", "1938-12", [("0.6 18", "DKW-2T-0.6", 45), ("0.7 20", "DKW-2T-0.7", 50)], portes=2, places=4, reservoir=30, remarques="Berline et cabriolet ; " + IND)
mg(L, "F8", "F8", "1", "1939-01", "1942-12", [("0.6 18", "DKW-2T-0.6", 45), ("0.7 20", "DKW-2T-0.7", 50)], portes=2, places=4, reservoir=30, remarques="Berline et cabriolet ; " + IND)
mg(L, "Sonderklasse", "Sonderklasse", "1", "1937-01", "1940-12", [("1.05 V4 32", "DKW-V4-2T-1.05", 75)], portes=4, places=4, reservoir=40,
   remarques="Propulsion, V4 deux-temps à pompes de charge ; " + IND)
mg(L, "F89 Meisterklasse", "F89", "1", "1950-01", "1954-12", [("0.7 23", "DKW-2T-0.7", 55)], portes=2, places=4, reservoir=30, remarques="Berline et cabriolet ; " + IND)
mg(L, "F91 Sonderklasse", "F91", "1", "1953-01", "1955-12", [("0.9 34", "DKW-2T-0.9", 72)], portes=2, places=4, reservoir=35, remarques="Trois cylindres « 3=6 » ; " + IND)
mg(L, "F93", "F93", "1", "1955-01", "1957-12", [("0.9 38", "DKW-2T-0.9", 72), ("0.9 40", "DKW-2T-0.9", 75, {"debut": "1957-01"})], portes=2, places=5, reservoir=35,
   remarques="Berline, coupé et break (F94 4 portes) ; " + IND)
mg(L, "Junior", "Junior", "1", "1959-01", "1963-12", [("0.75 34", "DKW-2T-0.75", 64), ("de Luxe 0.8 34", "DKW-2T-0.8", 69, {"debut": "1961-08"})],
   portes=2, places=4, reservoir=40, remarques="Berline compacte ; " + IND)
mg(L, "F12", "F12", "1", "1963-01", "1965-12", [("0.9 40", "DKW-2T-0.9", 75), ("0.9 45", "DKW-2T-0.9", 78, {"debut": "1964-01"})], portes=2, places=4, reservoir=40,
   remarques="Berline et roadster ; " + IND)
mg(L, "F102", "F102", "1", "1963-08", "1966-12", [("1.2 60", "DKW-2T-1.2", 108)], portes=4, places=5, reservoir=52,
   remarques="Dernière DKW, base de l'Audi F103 (1965) ; " + IND)
mg(L, "Munga", "Munga", "1", "1956-01", "1968-12", [("0.9 40", "DKW-2T-0.9", 75, {"fin": "1958-12"}), ("1.0 44", "AU-2T-1.0", 83, {"debut": "1959-01"})],
   portes=4, places=4, reservoir=45, remarques="Tout-terrain militaire 4x4 (Bundeswehr), version civile ; " + IND)

MOT = Motorisations("DKW", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"DKW": L}
MOTEURS = MOT.moteurs()
