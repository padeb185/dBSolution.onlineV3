"""Miesse (Bruxelles, 1894-1972) : générations, phases, motorisations (marché européen) et moteurs liés.
Voitures à vapeur (1896-1904), voitures à essence Type 10/12 HP (1904-1914), puis camions et autobus (moteurs diesel Gardner).
Vapeur : référentiel sans carburant « vapeur », saisie en essence atmosphérique. Puissances en ch.
Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "MIESSE-VAPEUR-3C": f("ATM", "ESS", 1.0, "AUCUNE", 3, 600, 300, "SAE30", 1.0, 500),
    "MIESSE-L4-2.0": f("ATM", "ESS", 2.0, "NC", 4, 1800, 1000, "SAE30", 3.0, 1000),
    "GARDNER-6LW-8.4": f("ATM", "DSL", 8.4, "NC", 6, 1700, 1100, "15W40", 18.0, 10000),
}
mg = SaisieMoteurs(FAMILLES, "Miesse", lambda fam: "Gardner" if fam.startswith("GARDNER") else "Miesse")
L = []
IND = "données indicatives (marque ancienne), à vérifier"
mg(L, "Vapeur", "Vapeur", "1", "1896-01", "1904-12", [("Vapeur 8", "MIESSE-VAPEUR-3C", 60)], portes=0, places=4, reservoir=60,
   remarques="Voiture à vapeur à trois cylindres (pas de carburant « vapeur » au référentiel) ; " + IND)
mg(L, "Type 10/12 HP", "10/12 HP", "1", "1904-01", "1914-12", [("2.0 12", "MIESSE-L4-2.0", 70)], portes=4, places=4, reservoir=50, remarques=IND)
mg(L, "Camion", "Camion", "1", "1920-01", "1972-12", [("Diesel Gardner 8.4 L6 102", "GARDNER-6LW-8.4", 480)], portes=2, places=2, reservoir=150, remarques="Camions et autobus ; " + IND)

MOT = Motorisations("Miesse", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Miesse": L}
MOTEURS = MOT.moteurs()
