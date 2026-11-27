"""FN (Fabrique Nationale d'Herstal) : générations, phases, motorisations (marché européen) et moteurs liés.
Voitures de la FN (Herstal, 1899-1935) : Type 1900, Type 1300, 1625, Prince Baudouin et Baudouin 8 ; puis AS 24 (tricycle militaire
aéroporté à moteur deux-temps, 1959-1964). Puissances en ch. Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "FN-1.0": f("ATM", E_, 1.0, "NC", 1, 1500, 1000, "SAE30", 1.5, 1000),
    "FN-1.3": f("ATM", E_, 1.3, "NC", 4, 3000, 1800, "SAE30", 3.0, 3000),
    "FN-1.6": f("ATM", E_, 1.6, "NC", 4, 3200, 1800, "SAE30", 3.5, 3000),
    "FN-L8-3.3": f("ATM", E_, 3.3, "NC", 8, 3600, 2000, "SAE30", 6.0, 3000),
    "FN-2T-0.25": f("ATM", E_, 0.25, "AUCUNE", 2, 5300, 4000, "CHOISIR", 0.0, 3000, a="PLAT"),
}
mg = SaisieMoteurs(FAMILLES, "FN", lambda fam: "FN")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Type 1900", "1900", "1", "1900-01", "1902-12", [("1.0 6", "FN-1.0", 30)], portes=0, places=2, reservoir=15, remarques="Voiturette ; " + IND)
mg(L, "Type 1300", "1300", "1", "1923-01", "1925-12", [("1.3 22", "FN-1.3", 65)], portes=4, places=4, reservoir=40, remarques="Torpédo ; " + IND)
mg(L, "1625", "1625", "1", "1928-01", "1932-12", [("1.6 35", "FN-1.6", 85)], portes=4, places=5, reservoir=45, remarques="Berline ; " + IND)
mg(L, "Prince Baudouin", "Prince Baudouin", "1", "1934-01", "1935-12", [("3.3 L8 75", "FN-L8-3.3", 200)], portes=4, places=5, reservoir=70,
   remarques="Berline huit cylindres, dernière voiture FN ; " + IND)
mg(L, "Baudouin 8", "Baudouin 8", "1", "1934-01", "1935-12", [("3.3 L8 75", "FN-L8-3.3", 200)], portes=4, places=5, reservoir=70, remarques="Berline ; " + IND)
mg(L, "AS 24", "AS 24", "1", "1959-01", "1964-12", [("0.25 2T 15", "FN-2T-0.25", 20)], portes=0, places=4, reservoir=13,
   remarques="Tricycle militaire pliable pour parachutistes, bicylindre deux-temps ; " + IND)

MOT = Motorisations("FN", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"FN": L}
MOTEURS = MOT.moteurs()
