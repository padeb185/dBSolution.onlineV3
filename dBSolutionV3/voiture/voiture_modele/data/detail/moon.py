"""Moon (Moon Motor Car Company, Saint-Louis, 1905-1930) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Model 30, Victory (six cylindres Continental) et Aerotype Eight. Puissances brutes converties en ch (× 1,014).
Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "MOON-L4-4.4": f("ATM", "ESS", 4.4, "NC", 4, 1800, 1000, "SAE30", 5.0, 2000),
    "CONTINENTAL-L6-3.9": f("ATM", "ESS", 3.9, "NC", 6, 2800, 1400, "SAE30", 5.0, 3000),
    "CONTINENTAL-L8-4.4": f("ATM", "ESS", 4.4, "NC", 8, 3200, 1600, "SAE30", 6.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Continental", lambda fam: "Moon" if fam.startswith("MOON") else "Continental")
L = []
IND = "marché nord-américain ; données indicatives (marque ancienne), à vérifier"
mg(L, "Model 30", "30", "1", "1906-01", "1910-12", [("4.4 30", "MOON-L4-4.4", 150)], portes=4, places=5, reservoir=60, remarques=IND)
mg(L, "Victory", "Victory", "1", "1918-01", "1925-12", [("3.9 L6 51", "CONTINENTAL-L6-3.9", 190)], portes=4, places=5, reservoir=65, remarques=IND)
mg(L, "Aerotype Eight", "Aerotype", "1", "1928-01", "1930-12", [("4.4 L8 75", "CONTINENTAL-L8-4.4", 230)], portes=4, places=5, reservoir=70, remarques=IND)

MOT = Motorisations("Continental", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Moon": L}
MOTEURS = MOT.moteurs()
