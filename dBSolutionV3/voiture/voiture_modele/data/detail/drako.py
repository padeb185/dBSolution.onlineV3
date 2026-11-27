"""Drako : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Drako Motors (San José) : GTE, berline électrique 4 places sur base Fisker Karma, quatre moteurs (un par roue), 25 exemplaires.
Le SUV Dragon (2 000 hp annoncés) n'est pas repris faute de livraisons confirmées. Puissance convertie en ch ; couple indicatif.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique

FAMILLES = {"DRAKO-QUAD-EV": electrique()}
mg = SaisieMoteurs(FAMILLES, "Drako", lambda fam: "Drako")
L = []

mg(L, "GTE", "GTE", "1", "2020-01", "2022-12", [("Électrique 90 kWh 1217", "DRAKO-QUAD-EV", 1200, {"batterie": 90})], portes=4, places=4, reservoir=0,
   remarques="Quatre moteurs de 225 kW avec vectorisation du couple, 25 exemplaires ; dates de production, batterie et couple indicatifs ; marché nord-américain")

MOT = Motorisations("Drako", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Drako": L}
MOTEURS = MOT.moteurs()
