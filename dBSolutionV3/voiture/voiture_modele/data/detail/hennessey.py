"""Hennessey (Hennessey Special Vehicles, Sealy, Texas) : générations, phases, motorisations et moteurs liés.
Inclut l'ancienne marque « Hennessey Venom » (fusionnée). Venom GT (coupé et Spyder sur base Lotus Exige, V8 7.0 biturbo dérivé du
LS7) et Venom F5 (V8 6.6 biturbo « Fury » maison) : coupé, Roadster, Revolution, Revolution Roadster et F5-M Roadster (boîte manuelle,
Fury porté à 2 031 hp). Préparations sur base Ford, Chevrolet, RAM, etc. non reprises. Puissances hp converties en ch (× 1,014).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C = "CHAINE"

FAMILLES = {
    "HPE-LS7-7.0TT": f("TURBO", E_, 7.0, C, 8, 6600, 4200, "5W40", 10.5, 5000, a="V"),
    "HPE-FURY-6.6TT": f("TURBO", E_, 6.6, C, 8, 8000, 5500, "5W50", 12.0, 5000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Hennessey")
L = []

mg(L, "Venom GT", "Venom GT", "1", "2011-01", "2017-12",
   [("7.0 V8 Biturbo 1261", "HPE-LS7-7.0TT", 1566), ("Spyder 7.0 V8 Biturbo 1261", "HPE-LS7-7.0TT", 1566, {"debut": "2013-01", "places": 2}),
    ("Spyder Final Edition 7.0 V8 Biturbo 1471", "HPE-LS7-7.0TT", 1745, {"debut": "2016-09", "remarques": "Venom GT Spyder Final Edition, 3 exemplaires ; couple indicatif"})],
   portes=2, places=2, reservoir=70,
   remarques="Coupé (13 ex.) et Spyder sur châssis Lotus Exige allongé ; 435,3 km/h (non homologué) en 2014 ; données indicatives")
mg(L, "Venom F5", "Venom F5", "1", "2021-01", None,
   [("6.6 V8 Biturbo 1842", "HPE-FURY-6.6TT", 1617, {"fin": "2023-12"}), ("Revolution 6.6 V8 Biturbo 1842", "HPE-FURY-6.6TT", 1617, {"debut": "2023-01"})],
   portes=2, places=2, reservoir=60,
   remarques="Coupé (24 ex.) puis Revolution (version piste homologuée route) ; monocoque carbone, V8 « Fury » maison ; réservoir indicatif")
mg(L, "Venom F5 Roadster", "Venom F5", "R", "2022-10", None,
   [("6.6 V8 Biturbo 1842", "HPE-FURY-6.6TT", 1617), ("Revolution 6.6 V8 Biturbo 1842", "HPE-FURY-6.6TT", 1617, {"debut": "2023-08", "fin": "2024-12"}),
    ("F5-M 6.6 V8 Biturbo 2059", "HPE-FURY-6.6TT", 1959, {"debut": "2026-07", "remarques": "F5-M Roadster : boîte manuelle 6 rapports, 12 exemplaires"})],
   portes=2, places=2, reservoir=60,
   remarques="Roadster (30 ex.), Revolution Roadster (12 ex.) et F5-M Roadster manuel (12 ex.) ; réservoir indicatif")

MOT = Motorisations("Hennessey", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Hennessey": L}
MOTEURS = MOT.moteurs()
