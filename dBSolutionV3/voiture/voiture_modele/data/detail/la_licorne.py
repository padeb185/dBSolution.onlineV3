"""La Licorne (Corre-La Licorne, Neuilly / Courbevoie, 1907-1949) : générations, phases, motorisations (marché français) et moteurs liés.
Type V8 (1920-1924), BO (1928-1934), L 760 et Type 14 CV (fin des années 1930, sur bases mécaniques Citroën Traction).
Puissances en ch. Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "LICORNE-L4-1.4": f("ATM", "ESS", 1.4, "NC", 4, 2800, 1600, "SAE30", 3.5, 2000),
    "LICORNE-L4-1.2": f("ATM", "ESS", 1.2, "NC", 4, 3200, 1800, "SAE30", 3.0, 3000),
    "CITROEN-L4-1.6": f("ATM", "ESS", 1.6, "NC", 4, 3800, 2000, "SAE30", 4.0, 3000),
    "CITROEN-L4-1.9": f("ATM", "ESS", 1.9, "NC", 4, 3800, 2000, "SAE30", 4.5, 3000),
}
mg = SaisieMoteurs(FAMILLES, "La Licorne", lambda fam: "Citroën" if fam.startswith("CITROEN") else "La Licorne")
L = []
IND = "données indicatives (marque ancienne), à vérifier"
mg(L, "Type V8", "V8", "1", "1920-01", "1924-12", [("1.4 20", "LICORNE-L4-1.4", 70)], portes=2, places=4, reservoir=40, remarques="Torpédo 8 CV ; " + IND)
mg(L, "BO", "BO", "1", "1928-01", "1934-12", [("1.2 25", "LICORNE-L4-1.2", 65)], portes=4, places=4, reservoir=40, remarques=IND)
mg(L, "L 760", "L 760", "1", "1936-01", "1939-12", [("1.6 35", "CITROEN-L4-1.6", 95)], portes=4, places=4, reservoir=45, remarques="Mécanique Citroën 7 ; " + IND)
mg(L, "Type 14 CV", "14 CV", "1", "1937-01", "1940-12", [("1.9 46", "CITROEN-L4-1.9", 120)], portes=4, places=5, reservoir=50, remarques="Mécanique Citroën 11 ; " + IND)

MOT = Motorisations("La Licorne", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"La Licorne": L}
MOTEURS = MOT.moteurs()
