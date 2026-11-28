"""Knox (Knox Automobile Company, Springfield, Massachusetts, 1900-1914) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Waterless (monocylindre refroidi par air à ailettes « porcupine ») et Model 40 (quatre cylindres). Puissances brutes converties en ch (× 1,014).
Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "KNOX-1C-1.6": f("ATM", "ESS", 1.6, "NC", 1, 1200, 800, "SAE30", 1.5, 1000),
    "KNOX-L4-6.0": f("ATM", "ESS", 6.0, "NC", 4, 1800, 1000, "SAE30", 6.0, 2000),
}
mg = SaisieMoteurs(FAMILLES, "Knox")
L = []
IND = "marché nord-américain ; données indicatives (marque ancienne), à vérifier"
mg(L, "Waterless", "Waterless", "1", "1900-01", "1904-12", [("1.6 8", "KNOX-1C-1.6", 40)], portes=0, places=2, reservoir=20, remarques="Runabout à refroidissement par air ; " + IND)
mg(L, "Model 40", "Model 40", "1", "1910-01", "1914-12", [("6.0 41", "KNOX-L4-6.0", 200)], portes=4, places=5, reservoir=70, remarques=IND)

MOT = Motorisations("Knox", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Knox": L}
MOTEURS = MOT.moteurs()
