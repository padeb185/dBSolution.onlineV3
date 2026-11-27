"""Germain : générations, phases, motorisations (marché européen) et moteurs liés.
Ateliers Germain (Monceau-sur-Sambre, Belgique, 1897-1914) : Daimler-Belge (sous licence Daimler / Panhard), Standard 18 HP et Chainless
(transmission par arbre). Puissances en ch. Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "GERMAIN-1.6": f("ATM", "ESS", 1.6, "NC", 2, 900, 600, "SAE30", 2.5, 1000),
    "GERMAIN-3.6": f("ATM", "ESS", 3.6, "NC", 4, 1400, 900, "SAE30", 5.0, 2000),
    "GERMAIN-4.1": f("ATM", "ESS", 4.1, "NC", 4, 1600, 1000, "SAE30", 5.5, 2000),
}
mg = SaisieMoteurs(FAMILLES, "Germain", lambda fam: "Germain")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Daimler-Belge", "Daimler-Belge", "1", "1898-01", "1901-12", [("1.6 6", "GERMAIN-1.6", 50)], portes=0, places=4, reservoir=25, remarques="Tonneau sous licence ; " + IND)
mg(L, "Standard 18 HP", "18 HP", "1", "1904-01", "1909-12", [("3.6 18", "GERMAIN-3.6", 110)], portes=4, places=5, reservoir=60, remarques="Torpédo ; " + IND)
mg(L, "Chainless", "Chainless", "1", "1906-01", "1914-12", [("4.1 24", "GERMAIN-4.1", 130)], portes=4, places=5, reservoir=65, remarques="Torpédo à transmission par arbre ; " + IND)

MOT = Motorisations("Germain", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Germain": L}
MOTEURS = MOT.moteurs()
