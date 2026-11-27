"""Federal : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Federal Motor Truck Company (Detroit) : Model 94 (tracteur 6x4, 1942-1945) et Model 604 (tracteur militaire, 1942-1945).
Six cylindres Hercules (RXC repris de diamond_t.py). Puissances brutes converties en ch (× 1,014).
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .diamond_t import FAMILLES as FAMILLES_DIAMOND

FAMILLES = {"HERCULES-RXC-8.7": FAMILLES_DIAMOND["HERCULES-RXC-8.7"],
            "HERCULES-HXD-14.0": f("ATM", "ESS", 14.0, "NC", 6, 2200, 1200, "SAE30", 16.0, 3000)}
mg = SaisieMoteurs(FAMILLES, "Hercules", lambda fam: "Hercules")
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Model 94", "94", "1", "1942-01", "1945-12", [("14.0 L6 205", "HERCULES-HXD-14.0", 800)], portes=2, places=2, reservoir=300, remarques="Tracteur militaire 6x4 (94x43) ; " + IND)
mg(L, "Model 604", "604", "1", "1942-01", "1945-12", [("8.7 L6 133", "HERCULES-RXC-8.7", 450)], portes=2, places=2, reservoir=230, remarques="Tracteur militaire ; " + IND)

MOT = Motorisations("Federal", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Federal": L}
MOTEURS = MOT.moteurs()
