"""Brossel : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur bruxellois de camions et d'autobus (1933-1967), souvent à moteurs Leyland. Puissances en ch.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

D = "DSL"
FAMILLES = {
    "LEYLAND-O600-9.8": f("ATM", D, 9.8, "NC", 6, 2000, 1200, "15W40", 18.0, 10000),
    "LEYLAND-O400-6.5": f("ATM", D, 6.5, "NC", 6, 2400, 1400, "15W40", 14.0, 10000),
}
mg = SaisieMoteurs(FAMILLES, "Leyland", lambda fam: "Leyland")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Camion", "Camion", "1", "1933-01", "1967-12", [("6.5 Diesel 100", "LEYLAND-O400-6.5", 350), ("9.8 Diesel 125", "LEYLAND-O600-9.8", 480, {"debut": "1949-01"})],
   portes=2, places=2, reservoir=150, remarques="Camions porteurs et tracteurs ; " + IND)
mg(L, "BL 55", "BL 55", "1", "1949-01", "1962-12", [("9.8 Diesel 125", "LEYLAND-O600-9.8", 480)], portes=2, places=80, reservoir=200,
   remarques="Autobus (notamment STIB et SNCV) ; " + IND)

MOT = Motorisations("Brossel", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Brossel": L}
MOTEURS = MOT.moteurs()
