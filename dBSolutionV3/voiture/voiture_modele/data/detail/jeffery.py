"""Jeffery (Thomas B. Jeffery Company, Kenosha, 1914-1917) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Successeur de Rambler, racheté par Charles Nash (devenu Nash Motors en 1917) : Model 93 (quatre cylindres), Six et camion
Jeffery Quad 4x4 (puis Nash Quad). Puissances brutes converties en ch (× 1,014).
Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "JEFFERY-L4-3.2": f("ATM", E_, 3.2, "NC", 4, 2400, 1200, "SAE30", 4.0, 2000),
    "JEFFERY-L6-4.3": f("ATM", E_, 4.3, "NC", 6, 2400, 1200, "SAE30", 5.0, 2000),
    "BUDA-L4-5.0": f("ATM", E_, 5.0, "NC", 4, 1800, 1000, "SAE30", 6.0, 2000),
}
mg = SaisieMoteurs(FAMILLES, "Jeffery", lambda fam: "Buda" if fam.startswith("BUDA") else "Jeffery")
L = []
IND = "marché nord-américain ; données indicatives (marque ancienne), à vérifier"

mg(L, "Model 93", "Model 93", "1", "1914-01", "1916-12", [("3.2 41", "JEFFERY-L4-3.2", 150)], portes=4, places=5, reservoir=60, remarques=IND)
mg(L, "Six", "Six", "1", "1914-01", "1917-12", [("4.3 L6 49", "JEFFERY-L6-4.3", 190)], portes=4, places=7, reservoir=70, remarques=IND)
mg(L, "Quad", "Quad", "1", "1913-01", "1917-12", [("5.0 37", "BUDA-L4-5.0", 200)], portes=2, places=2, reservoir=75,
   remarques="Camion à quatre roues motrices et directrices, très utilisé pendant la Grande Guerre ; " + IND)

MOT = Motorisations("Jeffery", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Jeffery": L}
MOTEURS = MOT.moteurs()
