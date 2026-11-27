"""Cartercar : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Constructeur de Pontiac (Michigan, groupe GM à partir de 1909) à transmission par friction : Model R et Model 5.
Puissances brutes converties en ch (× 1,014). Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {"CARTERCAR-4.5": f("ATM", "ESS", 4.5, "NC", 4, 1800, 1000, "SAE30", 5.0, 2000)}
mg = SaisieMoteurs(FAMILLES, "Cartercar", lambda fam: "Cartercar")
L = []
IND = "transmission par friction ; marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Model R", "R", "1", "1909-01", "1910-12", [("4.5 30", "CARTERCAR-4.5", 150)], portes=4, places=5, reservoir=55, remarques="Torpédo ; " + IND)
mg(L, "Model 5", "5", "1", "1912-01", "1915-12", [("4.5 30", "CARTERCAR-4.5", 150)], portes=4, places=5, reservoir=55, remarques="Torpédo ; " + IND)

MOT = Motorisations("Cartercar", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Cartercar": L}
MOTEURS = MOT.moteurs()
