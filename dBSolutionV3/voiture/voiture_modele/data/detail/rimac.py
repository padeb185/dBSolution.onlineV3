"""Rimac : générations, phases, motorisations (marché européen) et moteurs liés.
Concept One, Concept S et Nevera (dont Nevera R). Le C_Two (2018) est le prototype du Nevera ; le Concept One Alpha était un prototype.
Moteurs électriques Rimac (quatre moteurs, un par roue). Séries très limitées, données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique

FAMILLES = {"RIMAC-EV": electrique()}

mg = SaisieMoteurs(FAMILLES, "Rimac")
L = []


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg(L, "Concept One", "Concept One", "1", "2013-01", "2014-12", [("Électrique 1088", "RIMAC-EV", 1600, el(82))], portes=2, places=2, reservoir=0,
   remarques="Supercar électrique à quatre moteurs, 8 exemplaires ; données indicatives")
mg(L, "Concept S", "Concept S", "1", "2016-03", "2017-12", [("Électrique 1384", "RIMAC-EV", 1800, el(82))], portes=2, places=2, reservoir=0,
   remarques="Version piste du Concept One, très petite série ; données indicatives")
mg(L, "Nevera", "Nevera", "1", "2021-06", None,
   [("Électrique 1914", "RIMAC-EV", 2360, el(120)), ("R Électrique 2107", "RIMAC-EV", 2360, el(108, debut="2024-06"))], portes=2, places=2, reservoir=0,
   remarques="Hypercar électrique (prototype C_Two en 2018), 150 ex. ; Nevera R (40 ex.) et Time Attack ; données indicatives")

MOT = Motorisations("Rimac", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Rimac": L}
MOTEURS = MOT.moteurs()
