"""Clément-Bayard : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur de Mézières et Levallois (Adolphe Clément) : AC4 (1904-1906), 4M (1908-1912) et 8 HP (1910-1914). Puissances en ch.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "CLEMENT-2.7": f("ATM", "ESS", 2.7, "NC", 4, 1400, 900, "SAE30", 4.5, 2000),
    "CLEMENT-2.0": f("ATM", "ESS", 2.0, "NC", 4, 1800, 1000, "SAE30", 4.0, 2000),
    "CLEMENT-1.1": f("ATM", "ESS", 1.1, "NC", 2, 1800, 1000, "SAE30", 2.5, 2000),
}
mg = SaisieMoteurs(FAMILLES, "Clément-Bayard", lambda fam: "Clément-Bayard")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "AC4", "AC4", "1", "1904-01", "1906-12", [("2.7 16", "CLEMENT-2.7", 90)], portes=0, places=2, reservoir=40, remarques="Voiturette ; " + IND)
mg(L, "4M", "4M", "1", "1908-01", "1912-12", [("2.0 14", "CLEMENT-2.0", 75)], portes=4, places=4, reservoir=45, remarques="Torpédo ; " + IND)
mg(L, "8 HP", "8 HP", "1", "1910-01", "1914-12", [("1.1 8", "CLEMENT-1.1", 40)], portes=2, places=2, reservoir=30, remarques="Voiturette bicylindre ; " + IND)

MOT = Motorisations("Clément-Bayard", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Clément-Bayard": L}
MOTEURS = MOT.moteurs()
