"""Delage : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur de Levallois / Courbevoie : Type A (1906-1908), DE et DI (1923-1928), DM (1926-1930), D8 (1929-1940), D8-120 (1937-1940)
et D6 (1930-1954). Reprise par Delahaye (1935). Puissances en ch. Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "DEDION-DELAGE-0.7": f("ATM", E_, 0.7, "NC", 1, 1600, 1100, "SAE30", 1.5, 1000),
    "DELAGE-2.1": f("ATM", E_, 2.1, "NC", 4, 2800, 1600, "SAE30", 4.0, 3000),
    "DELAGE-L6-3.2": f("ATM", E_, 3.2, "NC", 6, 3200, 1800, "SAE30", 6.0, 3000),
    "DELAGE-L8-4.1": f("ATM", E_, 4.1, "NC", 8, 3500, 2000, "SAE30", 7.0, 3000),
    "DELAGE-L8-4.3": f("ATM", E_, 4.3, "NC", 8, 3800, 2200, "SAE30", 7.0, 3000),
    "DELAGE-L6-2.7": f("ATM", E_, 2.7, "NC", 6, 3600, 2000, "SAE30", 5.5, 3000),
    "DELAGE-L6-3.0": f("ATM", E_, 3.0, "NC", 6, 3800, 2200, "SAE30", 5.5, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Delage", lambda fam: "De Dion-Bouton" if fam.startswith("DEDION") else "Delage")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Type A", "A", "1", "1906-01", "1908-12", [("0.7 9", "DEDION-DELAGE-0.7", 30)], portes=0, places=2, reservoir=20, remarques="Voiturette à monocylindre De Dion ; " + IND)
mg(L, "DE", "DE", "1", "1923-01", "1928-12", [("2.1 30", "DELAGE-2.1", 100)], portes=4, places=4, reservoir=50, remarques="Torpédo 11 CV ; " + IND)
mg(L, "DI", "DI", "1", "1923-01", "1928-12", [("2.1 38", "DELAGE-2.1", 110)], portes=4, places=4, reservoir=50, remarques="Torpédo et berline, dont DIS / DISS sport ; " + IND)
mg(L, "DM", "DM", "1", "1926-01", "1930-12", [("3.2 L6 70", "DELAGE-L6-3.2", 190)], portes=4, places=5, reservoir=70, remarques="Berline, dont DMS / DMN ; " + IND)
mg(L, "D8", "D8", "1", "1929-01", "1940-12", [("4.1 L8 105", "DELAGE-L8-4.1", 270), ("D8S 4.1 L8 120", "DELAGE-L8-4.1", 290, {"debut": "1932-01"})],
   portes=4, places=5, reservoir=90, remarques="Berlines et cabriolets carrossés (Letourneur & Marchand, Chapron…) ; " + IND)
mg(L, "D8-120", "D8-120", "1", "1937-01", "1940-12", [("4.3 L8 120", "DELAGE-L8-4.3", 290)], portes=2, places=4, reservoir=90,
   remarques="Coupé et cabriolet sur châssis Delahaye ; " + IND)
mg(L, "D6", "D6", "1", "1930-01", "1954-12", [("2.7 L6 60", "DELAGE-L6-2.7", 160, {"fin": "1939-12"}), ("D6-3L 3.0 L6 90", "DELAGE-L6-3.0", 190, {"debut": "1946-01"})],
   portes=4, places=5, reservoir=70, remarques="Berline et coupé ; D6-3L d'après-guerre (moteur Delahaye) ; " + IND)

MOT = Motorisations("Delage", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Delage": L}
MOTEURS = MOT.moteurs()
