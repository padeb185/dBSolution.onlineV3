"""National (National Motor Vehicle Company, Indianapolis, 1900-1924) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Model 40 (victoire aux 500 Miles d'Indianapolis 1912), Highway Six et Sextet. Puissances brutes converties en ch (× 1,014).
Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "NATIONAL-L4-7.5": f("ATM", "ESS", 7.5, "NC", 4, 1800, 1000, "SAE30", 7.0, 1000),
    "NATIONAL-L6-5.4": f("ATM", "ESS", 5.4, "NC", 6, 2400, 1200, "SAE30", 6.0, 2000),
    "CONTINENTAL-L6-4.9": f("ATM", "ESS", 4.9, "NC", 6, 2600, 1400, "SAE30", 6.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "National", lambda fam: "Continental" if fam.startswith("CONTINENTAL") else "National")
L = []
IND = "marché nord-américain ; données indicatives (marque ancienne), à vérifier"
mg(L, "Model 40", "40", "1", "1911-01", "1913-12", [("7.5 41", "NATIONAL-L4-7.5", 270)], portes=4, places=5, reservoir=80, remarques=IND)
mg(L, "Highway Six", "Highway Six", "1", "1915-01", "1918-12", [("5.4 L6 56", "NATIONAL-L6-5.4", 230)], portes=4, places=5, reservoir=75, remarques=IND)
mg(L, "Sextet", "Sextet", "1", "1920-01", "1924-12", [("4.9 L6 61", "CONTINENTAL-L6-4.9", 240)], portes=4, places=5, reservoir=75, remarques=IND)

MOT = Motorisations("National", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"National": L}
MOTEURS = MOT.moteurs()
