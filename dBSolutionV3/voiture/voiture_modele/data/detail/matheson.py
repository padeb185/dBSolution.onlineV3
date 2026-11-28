"""Matheson (Wilkes-Barre, Pennsylvanie, 1903-1912) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Model 50 (quatre cylindres à arbre à cames en tête) et Silent Six. Puissances brutes converties en ch (× 1,014).
Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "MATHESON-L4-7.6": f("ATM", "ESS", 7.6, "NC", 4, 1500, 900, "SAE30", 7.0, 1000),
    "MATHESON-L6-8.0": f("ATM", "ESS", 8.0, "NC", 6, 1800, 1000, "SAE30", 8.0, 1000),
}
mg = SaisieMoteurs(FAMILLES, "Matheson")
L = []
IND = "marché nord-américain ; données indicatives (marque ancienne), à vérifier"
mg(L, "Model 50", "50", "1", "1906-01", "1909-12", [("7.6 51", "MATHESON-L4-7.6", 280)], portes=4, places=5, reservoir=80, remarques=IND)
mg(L, "Silent Six", "Silent Six", "1", "1910-01", "1912-12", [("8.0 L6 49", "MATHESON-L6-8.0", 270)], portes=4, places=7, reservoir=90, remarques=IND)

MOT = Motorisations("Matheson", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Matheson": L}
MOTEURS = MOT.moteurs()
