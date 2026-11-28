"""Marmon (Nordyke & Marmon, Indianapolis, 1902-1933) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Wasp (vainqueur des premiers 500 Miles d'Indianapolis, 1911), Model 34 (six cylindres en aluminium), Roosevelt (huit cylindres, 1929-1930)
et Sixteen (V16, 1931-1933). Puissances brutes converties en ch (× 1,014). Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "MARMON-L6-7.8": f("ATM", "ESS", 7.8, "NC", 6, 2000, 1200, "SAE30", 8.0, 1000),
    "MARMON-L6-5.6": f("ATM", "ESS", 5.6, "NC", 6, 2300, 1200, "SAE30", 6.0, 2000),
    "MARMON-L8-3.3": f("ATM", "ESS", 3.3, "NC", 8, 3400, 1600, "SAE30", 5.0, 3000),
    "MARMON-V16-8.0": f("ATM", "ESS", 8.0, "NC", 16, 3400, 1600, "SAE30", 9.0, 3000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Marmon")
L = []
IND = "marché nord-américain ; données indicatives (marque ancienne), à vérifier"
mg(L, "Wasp", "Wasp", "1", "1911-01", "1911-12", [("7.8 L6 112", "MARMON-L6-7.8", 400)], portes=0, places=1, reservoir=100, remarques="Monoplace de course, premier rétroviseur ; " + IND)
mg(L, "Model 34", "34", "1", "1916-01", "1924-12", [("5.6 L6 75", "MARMON-L6-5.6", 280)], portes=4, places=5, reservoir=80, remarques="Moteur et carrosserie en aluminium ; " + IND)
mg(L, "Roosevelt", "Roosevelt", "1", "1929-01", "1930-12", [("3.3 L8 73", "MARMON-L8-3.3", 200)], portes=4, places=5, reservoir=60, remarques="Première huit cylindres à moins de 1 000 dollars ; " + IND)
mg(L, "Sixteen", "Sixteen", "1", "1931-01", "1933-12", [("8.0 V16 203", "MARMON-V16-8.0", 560)], portes=4, places=5, reservoir=100, remarques="V16 en aluminium, environ 390 exemplaires ; " + IND)

MOT = Motorisations("Marmon", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Marmon": L}
MOTEURS = MOT.moteurs()
