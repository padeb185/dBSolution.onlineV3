"""Columbia : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Pope Manufacturing / Electric Vehicle Company (Hartford) : Electric Runabout (1897-1907) et Mark XLVI (1905-1907) ;
Columbia Motors (Detroit) : Six (1916-1924, six cylindres Continental repris d'auburn.py). Puissances brutes converties en ch (× 1,014).
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .auburn import FAMILLES as FAMILLES_AUBURN

CONTINENTAL = {"CONTINENTAL-L6-3.7": FAMILLES_AUBURN["CONTINENTAL-L6-3.7"]}
FAMILLES = {**CONTINENTAL, "COLUMBIA-EV": electrique(km=5000), "COLUMBIA-6.4": f("ATM", "ESS", 6.4, "NC", 4, 1400, 900, "SAE30", 6.0, 2000)}
mg = SaisieMoteurs(FAMILLES, "Columbia", lambda fam: "Continental" if fam in CONTINENTAL else "Columbia")
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Electric Runabout", "Electric", "1", "1897-01", "1907-12", [("Électrique 2", "COLUMBIA-EV", 20, {"batterie": 3})], portes=0, places=2, reservoir=0,
   remarques="Voiturette électrique à batteries plomb ; " + IND)
mg(L, "Mark XLVI", "Mark XLVI", "1", "1905-01", "1907-12", [("6.4 41", "COLUMBIA-6.4", 210)], portes=4, places=5, reservoir=70, remarques="Torpédo ; " + IND)
mg(L, "Six", "Six", "1", "1916-01", "1924-12", [("3.7 L6 41", "CONTINENTAL-L6-3.7", 190)], portes=4, places=5, reservoir=60, remarques="Berline, six cylindres Continental ; " + IND)

MOT = Motorisations("Columbia", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Columbia": L}
MOTEURS = MOT.moteurs()
