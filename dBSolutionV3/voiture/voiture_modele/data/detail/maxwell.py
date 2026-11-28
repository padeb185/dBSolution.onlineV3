"""Maxwell (Maxwell-Briscoe puis Maxwell Motor Company, 1904-1925) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Model LC (bicylindre à plat), Model 25 et « Good Maxwell » ; racheté par Walter Chrysler (Chrysler Corporation, 1925).
Puissances brutes converties en ch (× 1,014). Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "MAXWELL-B2-1.8": f("ATM", "ESS", 1.8, "NC", 2, 1400, 900, "SAE30", 2.0, 1000, a="PLAT"),
    "MAXWELL-L4-3.0": f("ATM", "ESS", 3.0, "NC", 4, 2400, 1200, "SAE30", 4.0, 2000),
}
mg = SaisieMoteurs(FAMILLES, "Maxwell")
L = []
IND = "marché nord-américain ; données indicatives (marque ancienne), à vérifier"
mg(L, "Model LC", "LC", "1", "1904-01", "1906-12", [("1.8 8", "MAXWELL-B2-1.8", 45)], portes=0, places=2, reservoir=30, remarques="Runabout à bicylindre à plat ; " + IND)
mg(L, "Model 25", "25", "1", "1914-01", "1922-12", [("3.0 25", "MAXWELL-L4-3.0", 125)], portes=4, places=5, reservoir=50, remarques=IND)
mg(L, "Good Maxwell", "Good Maxwell", "1", "1922-01", "1925-12", [("3.0 34", "MAXWELL-L4-3.0", 135)], portes=4, places=5, reservoir=50, remarques="Devenue Chrysler 4 / Plymouth ; " + IND)

MOT = Motorisations("Maxwell", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Maxwell": L}
MOTEURS = MOT.moteurs()
