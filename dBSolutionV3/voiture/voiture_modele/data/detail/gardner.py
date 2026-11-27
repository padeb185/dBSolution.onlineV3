"""Gardner : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Gardner Motor Company (Saint-Louis, 1920-1931) : Model 5, Model 8-80 et Model 136. Moteurs Lycoming (L8 4.4 repris d'auburn.py).
Puissances brutes converties en ch (× 1,014). Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .auburn import FAMILLES as FAMILLES_AUBURN

FAMILLES = {"LYCOMING-L8-4.4": FAMILLES_AUBURN["LYCOMING-L8-4.4"],
            "LYCOMING-L4-3.2": f("ATM", "ESS", 3.2, "NC", 4, 2400, 1200, "SAE30", 4.5, 3000)}
mg = SaisieMoteurs(FAMILLES, "Lycoming", lambda fam: "Lycoming")
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Model 5", "5", "1", "1920-01", "1924-12", [("3.2 36", "LYCOMING-L4-3.2", 150)], portes=4, places=5, reservoir=55, remarques="Torpédo ; " + IND)
mg(L, "Model 8-80", "8-80", "1", "1925-01", "1926-12", [("4.4 L8 66", "LYCOMING-L8-4.4", 220)], portes=4, places=5, reservoir=65, remarques="Berline huit cylindres ; " + IND)
mg(L, "Model 136", "136", "1", "1929-01", "1931-12", [("4.4 L8 86", "LYCOMING-L8-4.4", 245)], portes=4, places=5, reservoir=70, remarques="Berline ; " + IND)

MOT = Motorisations("Gardner", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Gardner": L}
MOTEURS = MOT.moteurs()
