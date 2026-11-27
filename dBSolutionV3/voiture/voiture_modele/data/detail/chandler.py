"""Chandler : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Constructeur de Cleveland (1913-1929, repris par Hupmobile) : Six, Big Six et Royal Eight.
Puissances brutes converties en ch (× 1,014). Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "CHANDLER-L6-4.7": f("ATM", "ESS", 4.7, "NC", 6, 2400, 1200, "SAE30", 6.0, 3000),
    "CHANDLER-L6-4.8": f("ATM", "ESS", 4.8, "NC", 6, 3000, 1400, "SAE30", 6.0, 3000),
    "CHANDLER-L8-4.9": f("ATM", "ESS", 4.9, "NC", 8, 3200, 1400, "SAE30", 7.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Chandler", lambda fam: "Chandler")
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Six", "Six", "1", "1913-01", "1925-12", [("4.7 L6 46", "CHANDLER-L6-4.7", 230)], portes=4, places=5, reservoir=70, remarques="Torpédo et berline ; " + IND)
mg(L, "Big Six", "Big Six", "1", "1925-01", "1928-12", [("4.8 L6 86", "CHANDLER-L6-4.8", 290)], portes=4, places=5, reservoir=70, remarques="Berline ; " + IND)
mg(L, "Royal Eight", "Royal Eight", "1", "1928-01", "1929-12", [("4.9 L8 96", "CHANDLER-L8-4.9", 300)], portes=4, places=5, reservoir=75, remarques="Berline ; " + IND)

MOT = Motorisations("Chandler", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Chandler": L}
MOTEURS = MOT.moteurs()
