"""Delaunay-Belleville : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur de Saint-Denis (chaudières marines) : HB4 (1908-1912), SMT (« Sa Majesté le Tsar », 1909-1914) et VL8 (1931-1936).
Puissances en ch. Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "DELAUNAY-2.6": f("ATM", E_, 2.6, "NC", 4, 1600, 1000, "SAE30", 4.5, 2000),
    "DELAUNAY-L6-11.9": f("ATM", E_, 11.9, "NC", 6, 1500, 900, "SAE30", 10.0, 2000),
    "DELAUNAY-L8-4.4": f("ATM", E_, 4.4, "NC", 8, 3200, 1600, "SAE30", 7.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Delaunay-Belleville", lambda fam: "Delaunay-Belleville")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "HB4", "HB4", "1", "1908-01", "1912-12", [("2.6 16", "DELAUNAY-2.6", 90)], portes=4, places=4, reservoir=55, remarques="Torpédo, radiateur rond caractéristique ; " + IND)
mg(L, "SMT", "SMT", "1", "1909-01", "1914-12", [("11.9 L6 70", "DELAUNAY-L6-11.9", 450)], portes=4, places=6, reservoir=100,
   remarques="Limousine de prestige (cour de Russie) ; " + IND)
mg(L, "VL8", "VL8", "1", "1931-01", "1936-12", [("4.4 L8 90", "DELAUNAY-L8-4.4", 250)], portes=4, places=5, reservoir=80, remarques="Berline huit cylindres ; " + IND)

MOT = Motorisations("Delaunay-Belleville", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Delaunay-Belleville": L}
MOTEURS = MOT.moteurs()
