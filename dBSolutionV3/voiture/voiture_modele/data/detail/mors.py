"""Mors (Émile et Louis Mors, Paris, 1895-1925) : générations, phases, motorisations (marché français) et moteurs liés.
Type C, Dauphin (course, Paris-Vienne 1902), 14/19 HP et modèles à moteur sans soupapes Knight ; usine reprise par André Citroën (1919).
Puissances en ch. Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "MORS-2C-1.8": f("ATM", "ESS", 1.8, "NC", 2, 1000, 700, "SAE30", 2.5, 1000, a="V"),
    "MORS-L4-9.2": f("ATM", "ESS", 9.2, "NC", 4, 1200, 900, "SAE30", 8.0, 500),
    "MORS-L4-2.8": f("ATM", "ESS", 2.8, "NC", 4, 1600, 1000, "SAE30", 4.0, 1000),
    "MORS-KNIGHT-L4-4.4": f("ATM", "ESS", 4.4, "NC", 4, 2000, 1200, "SAE30", 6.0, 2000),
}
mg = SaisieMoteurs(FAMILLES, "Mors")
L = []
IND = "données indicatives (marque ancienne), à vérifier"
mg(L, "Type C", "Type C", "1", "1899-01", "1901-12", [("1.8 6", "MORS-2C-1.8", 40)], portes=0, places=4, reservoir=30, remarques="Tonneau à bicylindre en V ; " + IND)
mg(L, "Dauphin", "Dauphin", "1", "1902-01", "1902-12", [("9.2 60", "MORS-L4-9.2", 330)], portes=0, places=2, reservoir=80, remarques="Voiture de course ; " + IND)
mg(L, "14/19 HP", "14/19", "1", "1908-01", "1912-12", [("2.8 19", "MORS-L4-2.8", 90)], portes=4, places=4, reservoir=50, remarques=IND)
mg(L, "Sans-soupapes", "Knight", "1", "1912-01", "1925-12", [("4.4 Knight 30", "MORS-KNIGHT-L4-4.4", 160)], portes=4, places=4, reservoir=60, remarques="Moteur sans soupapes Knight ; " + IND)

MOT = Motorisations("Mors", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Mors": L}
MOTEURS = MOT.moteurs()
