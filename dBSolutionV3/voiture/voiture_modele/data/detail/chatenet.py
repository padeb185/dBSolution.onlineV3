"""Chatenet : générations, phases, motorisations (marché européen) et moteurs liés.
Voitures sans permis françaises (quadricycles légers, 45 km/h) : CH26 et CH46.
Bicylindres diesel Lombardini (repris de bellier.py) et Kubota (repris d'aixam.py), mêmes familles et couples. Données indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .bellier import FAMILLES as FAMILLES_BELLIER
from .aixam import FAMILLES as FAMILLES_AIXAM

FAMILLES = {"LOMBARDINI-LDW502": FAMILLES_BELLIER["LOMBARDINI-LDW502"], "KUBOTA-Z482": FAMILLES_AIXAM["KUBOTA-Z482"]}
mg = SaisieMoteurs(FAMILLES, "Chatenet", lambda fam: "Kubota" if fam.startswith("KUBOTA") else "Lombardini")
L = []
VSP = "Voiture sans permis (quadricycle léger, 45 km/h) ; données indicatives, à vérifier"

mg(L, "CH26", "CH26", "1", "2008-01", "2016-12", [("Diesel 0.5 5", "LOMBARDINI-LDW502", 20)], portes=2, places=2, reservoir=16, remarques=VSP)
mg(L, "CH46", "CH46", "1", "2016-01", "2021-12", [("Diesel 0.5 7", "KUBOTA-Z482", 23)], portes=2, places=2, reservoir=16, remarques=VSP)

MOT = Motorisations("Chatenet", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Chatenet": L}
MOTEURS = MOT.moteurs()
