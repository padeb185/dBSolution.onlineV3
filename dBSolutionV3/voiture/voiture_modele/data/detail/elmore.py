"""Elmore : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Elmore Manufacturing (Clyde, Ohio, groupe GM en 1909) : voitures à moteurs deux-temps, Model 30 et Model 46. Moteurs deux-temps :
distribution « aucune », huile « à choisir » (mélange). Puissances brutes converties en ch (× 1,014).
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "ELMORE-2T-4.0": f("ATM", "ESS", 4.0, "AUCUNE", 4, 1600, 1000, "CHOISIR", 0.0, 2000),
    "ELMORE-2T-5.4": f("ATM", "ESS", 5.4, "AUCUNE", 4, 1600, 1000, "CHOISIR", 0.0, 2000),
}
mg = SaisieMoteurs(FAMILLES, "Elmore", lambda fam: "Elmore")
L = []
IND = "deux-temps ; marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Model 30", "30", "1", "1908-01", "1912-12", [("4.0 2T 30", "ELMORE-2T-4.0", 150)], portes=4, places=5, reservoir=60, remarques="Torpédo ; " + IND)
mg(L, "Model 46", "46", "1", "1910-01", "1912-12", [("5.4 2T 47", "ELMORE-2T-5.4", 220)], portes=4, places=5, reservoir=70, remarques="Torpédo ; " + IND)

MOT = Motorisations("Elmore", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Elmore": L}
MOTEURS = MOT.moteurs()
