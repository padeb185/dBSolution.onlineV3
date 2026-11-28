"""Mia Electric (Cerizay, ex-Heuliez, 2011-2014) : générations, phases, motorisations (marché français) et moteurs liés.
Mia (3 places, conducteur central), Mia L (4 places, empattement long) ; portes coulissantes. Moteur électrique de 18 kW, batterie de
8 ou 12 kWh. Puissance en ch. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

FAMILLES = {
    "MIA-EV": electrique(),
}
mg = SaisieMoteurs(FAMILLES, "Mia Electric")
L = []
IND = "portes coulissantes ; données indicatives"
mg(L, "Mia", "Mia", "1", "2011-06", "2014-03", [("Électrique 8 kWh 24", "MIA-EV", 57, {"batterie": 8}), ("Électrique 12 kWh 24", "MIA-EV", 57, {"batterie": 12})], portes=2, places=3, reservoir=0,
   remarques="Trois places, conducteur central ; " + IND)
mg(L, "Mia L", "Mia", "L", "2011-06", "2014-03", [("Électrique 12 kWh 24", "MIA-EV", 57, {"batterie": 12})], portes=2, places=4, reservoir=0, remarques="Version longue 4 places ; " + IND)

MOT = Motorisations("Mia Electric", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Mia Electric": L}
MOTEURS = MOT.moteurs()
