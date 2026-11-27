"""Detroit Electric : générations, phases, motorisations et moteurs liés.
Anderson Electric Car Company (Detroit, 1907-1939) : Model 27, Model 47 et Model 90 (coupés électriques à batteries plomb ou
Edison nickel-fer) ; Detroit Electric (relance, 2016-2017) : SP:01, roadster électrique sur base Lotus Elise.
Puissances converties en ch. Données indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique

FAMILLES = {"DETROIT-EV": electrique(km=5000), "DETROIT-SP01-EV": electrique()}
mg = SaisieMoteurs(FAMILLES, "Detroit Electric", lambda fam: "Detroit Electric")
L = []
IND = "électrique à batteries ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Model 27", "27", "1", "1911-01", "1912-12", [("Électrique 4", "DETROIT-EV", 40, {"batterie": 8})], portes=2, places=4, reservoir=0, remarques="Coupé (brougham) ; " + IND)
mg(L, "Model 47", "47", "1", "1914-01", "1916-12", [("Électrique 4", "DETROIT-EV", 40, {"batterie": 8})], portes=2, places=5, reservoir=0, remarques="Coupé ; " + IND)
mg(L, "Model 90", "90", "1", "1919-01", "1928-12", [("Électrique 5", "DETROIT-EV", 45, {"batterie": 10})], portes=2, places=5, reservoir=0, remarques="Coupé ; " + IND)
mg(L, "SP:01", "SP:01", "1", "2016-01", "2017-12", [("Électrique 37 kWh 286", "DETROIT-SP01-EV", 225, {"batterie": 37})], portes=2, places=2, reservoir=0,
   remarques="Roadster électrique sur châssis Lotus Elise, production très limitée ; données indicatives, à vérifier")

MOT = Motorisations("Detroit Electric", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Detroit Electric": L}
MOTEURS = MOT.moteurs()
