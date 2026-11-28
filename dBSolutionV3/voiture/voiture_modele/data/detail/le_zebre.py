"""Le Zèbre (Puteaux, 1909-1931) : générations, phases, motorisations (marché français) et moteurs liés.
Fondée par Jules Salomon et Jacques Bizet (Salomon créera ensuite la Citroën Type A) : Type A (monocylindre), Type D et Type Z.
Puissances en ch. Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "ZEBRE-1C-0.6": f("ATM", "ESS", 0.6, "NC", 1, 1800, 1200, "SAE30", 1.5, 1000),
    "ZEBRE-L4-1.0": f("ATM", "ESS", 1.0, "NC", 4, 2400, 1500, "SAE30", 2.5, 2000),
    "ZEBRE-L4-1.0Z": f("ATM", "ESS", 1.0, "NC", 4, 3000, 1800, "SAE30", 2.5, 2000),
}
mg = SaisieMoteurs(FAMILLES, "Le Zèbre")
L = []
IND = "données indicatives (marque ancienne), à vérifier"
mg(L, "Type A", "Type A", "1", "1909-01", "1912-12", [("0.6 6", "ZEBRE-1C-0.6", 25)], portes=0, places=2, reservoir=20, remarques="Voiturette monocylindre 5 CV ; " + IND)
mg(L, "Type D", "Type D", "1", "1914-01", "1920-12", [("1.0 12", "ZEBRE-L4-1.0", 45)], portes=2, places=2, reservoir=30, remarques=IND)
mg(L, "Type Z", "Type Z", "1", "1924-01", "1931-12", [("1.0 20", "ZEBRE-L4-1.0Z", 55)], portes=4, places=4, reservoir=35, remarques="Torpédo 7 CV ; " + IND)

MOT = Motorisations("Le Zèbre", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Le Zèbre": L}
MOTEURS = MOT.moteurs()
