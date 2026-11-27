"""Graham-Paige : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Graham-Paige Motors (Detroit, 1927-1930, ex-Paige-Detroit, puis Graham) : Model 610 (six cylindres) et Model 837 (huit cylindres).
Puissances brutes converties en ch (× 1,014). Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "GP-L6-3.3": f("ATM", "ESS", 3.3, "NC", 6, 3000, 1400, "SAE30", 5.0, 3000),
    "GP-L8-5.3": f("ATM", "ESS", 5.3, "NC", 8, 3200, 1600, "SAE30", 7.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Graham-Paige", lambda fam: "Graham-Paige")
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Model 610", "610", "1", "1928-01", "1929-12", [("3.3 L6 63", "GP-L6-3.3", 180)], portes=4, places=5, reservoir=60, remarques="Berline six cylindres ; " + IND)
mg(L, "Model 837", "837", "1", "1928-01", "1929-12", [("5.3 L8 122", "GP-L8-5.3", 340)], portes=4, places=7, reservoir=80, remarques="Grande berline huit cylindres ; " + IND)

MOT = Motorisations("Graham-Paige", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Graham-Paige": L}
MOTEURS = MOT.moteurs()
