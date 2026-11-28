"""Nagant (Fabrique d'armes Nagant, Liège, 1900-1928) : générations, phases, motorisations (marché européen) et moteurs liés.
Gobron-Nagant (licence Gobron-Brillié à pistons opposés, code repris de gobron_brillie.py), Type C et 10/12 HP ; reprise par Imperia (1928).
Puissances en ch. Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .gobron_brillie import FAMILLES as FAMILLES_GB

FAMILLES = {
    "GOBRON-OP-2.3": FAMILLES_GB["GOBRON-OP-2.3"],
    "NAGANT-L4-2.1": f("ATM", "ESS", 2.1, "NC", 4, 2000, 1200, "SAE30", 4.0, 1000),
    "NAGANT-L4-1.5": f("ATM", "ESS", 1.5, "NC", 4, 2800, 1600, "SAE30", 3.5, 2000),
}
mg = SaisieMoteurs(FAMILLES, "Nagant", lambda fam: "Gobron-Brillié" if fam.startswith("GOBRON") else "Nagant")
L = []
IND = "données indicatives (marque ancienne), à vérifier"
mg(L, "Gobron-Nagant", "Gobron-Nagant", "1", "1900-01", "1903-12", [("2.3 10", "GOBRON-OP-2.3", 70)], portes=0, places=2, reservoir=40, remarques="Licence Gobron-Brillié ; " + IND)
mg(L, "Type C", "Type C", "1", "1910-01", "1914-12", [("2.1 20", "NAGANT-L4-2.1", 90)], portes=4, places=5, reservoir=50, remarques=IND)
mg(L, "Nagant 10/12 HP", "10/12", "1", "1920-01", "1928-12", [("1.5 22", "NAGANT-L4-1.5", 75)], portes=4, places=4, reservoir=45, remarques=IND)

MOT = Motorisations("Nagant", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Nagant": L}
MOTEURS = MOT.moteurs()
