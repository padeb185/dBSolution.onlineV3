"""Holsman : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Holsman Automobile Company (Chicago, 1902-1910) : « high wheeler » à grandes roues, transmission par câbles, bicylindre à plat
refroidi par air puis quatre cylindres. Puissances brutes converties en ch (× 1,014).
Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {"HOLSMAN-B2-1.6": f("ATM", "ESS", 1.6, "NC", 2, 1200, 800, "SAE30", 1.5, 1000, a="PLAT"),
            "HOLSMAN-L4-2.4": f("ATM", "ESS", 2.4, "NC", 4, 1500, 900, "SAE30", 3.0, 1000)}
mg = SaisieMoteurs(FAMILLES, "Holsman")
L = []
IND = "désignations, cylindrée et dates indicatives (marque ancienne), à vérifier"

mg(L, "High Wheeler", "High Wheeler", "1", "1902-01", "1910-12",
   [("1.6 10", "HOLSMAN-B2-1.6", 45, {"fin": "1906-12"}), ("1.6 14", "HOLSMAN-B2-1.6", 55, {"debut": "1907-01"}), ("2.4 26", "HOLSMAN-L4-2.4", 95, {"debut": "1908-01"})],
   portes=0, places=2, reservoir=25, remarques="Buggy à grandes roues pour routes rurales ; " + IND)

MOT = Motorisations("Holsman", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Holsman": L}
MOTEURS = MOT.moteurs()
