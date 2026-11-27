"""GEM (Global Electric Motorcars, groupe Polaris) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Véhicules électriques de quartier (vitesse limitée à 25 mph) : e2, e4 et e6. Puissance et batterie indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique

FAMILLES = {"GEM-EV": electrique()}
mg = SaisieMoteurs(FAMILLES, "GEM", lambda fam: "GEM")
L = []
NEV = "véhicule électrique de quartier (NEV) ; puissance, couple et batterie indicatifs ; marché nord-américain"

mg(L, "e2", "e2", "1", "1998-01", None, [("Électrique 7", "GEM-EV", 100, {"batterie": 9})], portes=2, places=2, reservoir=0, remarques="Biplace ; " + NEV)
mg(L, "e4", "e4", "1", "1998-01", None, [("Électrique 7", "GEM-EV", 100, {"batterie": 9})], portes=4, places=4, reservoir=0, remarques="Quatre places ; " + NEV)
mg(L, "e6", "e6", "1", "2012-01", None, [("Électrique 7", "GEM-EV", 100, {"batterie": 9})], portes=4, places=6, reservoir=0, remarques="Six places ; " + NEV)

MOT = Motorisations("GEM", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"GEM": L}
MOTEURS = MOT.moteurs()
