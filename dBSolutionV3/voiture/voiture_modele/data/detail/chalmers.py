"""Chalmers : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Constructeur de Detroit (1908-1923, repris par Maxwell puis Chrysler) : Model 30, Six-30 et Six.
Puissances brutes converties en ch (× 1,014). Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "CHALMERS-3.7": f("ATM", "ESS", 3.7, "NC", 4, 2000, 1000, "SAE30", 5.0, 2000),
    "CHALMERS-L6-3.6": f("ATM", "ESS", 3.6, "NC", 6, 2800, 1400, "SAE30", 5.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Chalmers", lambda fam: "Chalmers")
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Model 30", "30", "1", "1910-01", "1913-12", [("3.7 30", "CHALMERS-3.7", 140)], portes=4, places=5, reservoir=60, remarques="Torpédo ; " + IND)
mg(L, "Six-30", "Six-30", "1", "1916-01", "1919-12", [("3.6 L6 46", "CHALMERS-L6-3.6", 190)], portes=4, places=5, reservoir=60,
   remarques="Torpédo, six cylindres à haut régime (3 400 tr/min annoncés) ; " + IND)
mg(L, "Six", "Six", "1", "1920-01", "1923-12", [("3.6 L6 46", "CHALMERS-L6-3.6", 190)], portes=4, places=5, reservoir=60, remarques="Berline et torpédo ; " + IND)

MOT = Motorisations("Chalmers", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Chalmers": L}
MOTEURS = MOT.moteurs()
