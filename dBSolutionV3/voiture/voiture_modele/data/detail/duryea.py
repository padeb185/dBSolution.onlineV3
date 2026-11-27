"""Duryea : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Frères Charles et Frank Duryea (Springfield, Massachusetts) : Motor Wagon (première automobile américaine à essence, 1893-1896)
puis Duryea Power Company (Reading) : Phaeton (tricylindre, 1900-1913). Puissances brutes converties en ch (× 1,014).
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "DURYEA-1.3": f("ATM", "ESS", 1.3, "NC", 1, 700, 500, "SAE30", 1.5, 1000),
    "DURYEA-L3-2.6": f("ATM", "ESS", 2.6, "NC", 3, 1200, 800, "SAE30", 3.5, 2000),
}
mg = SaisieMoteurs(FAMILLES, "Duryea", lambda fam: "Duryea")
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Motor Wagon", "Motor Wagon", "1", "1893-01", "1896-12", [("1.3 4", "DURYEA-1.3", 40)], portes=0, places=2, reservoir=10,
   remarques="Buggy à moteur monocylindre, vainqueur de la course de Chicago (1895) ; " + IND)
mg(L, "Phaeton", "Phaeton", "1", "1900-01", "1913-12", [("2.6 L3 12", "DURYEA-L3-2.6", 90)], portes=0, places=3, reservoir=30,
   remarques="Tricylindre transversal, direction par levier ; " + IND)

MOT = Motorisations("Duryea", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Duryea": L}
MOTEURS = MOT.moteurs()
