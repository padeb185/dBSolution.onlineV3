"""Bluecar (Bolloré) : générations, phases, motorisations (marché européen) et moteurs liés.
Bluecar (citadine électrique, base des services Autolib' / BlueIndy, 2011-2018) et Bluesummer (cabriolet, 2016-2019).
Batterie lithium-métal-polymère (LMP) de 30 kWh. Données indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique

FAMILLES = {"BLUECAR-EV": electrique()}
mg = SaisieMoteurs(FAMILLES, "Bolloré", lambda fam: "Bolloré")
L = []

mg(L, "Bluecar", "Bluecar", "1", "2011-10", "2018-12", [("Électrique 30 kWh 68", "BLUECAR-EV", 167, {"batterie": 30})], portes=3, places=4, reservoir=0,
   remarques="Citadine électrique (carrosserie Pininfarina, assemblage Cecomp), batterie LMP ; données indicatives")
mg(L, "Bluesummer", "Bluesummer", "1", "2016-06", "2019-12", [("Électrique 30 kWh 48", "BLUECAR-EV", 140, {"batterie": 30})], portes=2, places=4, reservoir=0,
   remarques="Cabriolet de plage électrique (assemblé par Renault à Dieppe), batterie LMP ; données indicatives")

MOT = Motorisations("Bluecar", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Bluecar": L}
MOTEURS = MOT.moteurs()
