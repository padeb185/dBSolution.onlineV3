"""De Dion-Bouton : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur de Puteaux : Vis-à-vis (1900-1902), Type Q et Populaire (1903-1904), Type AL (1906-1907), Type BS (1910-1912)
et Type IW (1923-1925). Monocylindres à haut régime puis quatre cylindres. Puissances en ch.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "DEDION-0.4": f("ATM", E_, 0.4, "NC", 1, 1800, 1200, "SAE30", 1.0, 1000),
    "DEDION-0.7": f("ATM", E_, 0.7, "NC", 1, 1600, 1100, "SAE30", 1.5, 1000),
    "DEDION-1.9": f("ATM", E_, 1.9, "NC", 4, 1600, 1000, "SAE30", 3.5, 2000),
    "DEDION-2.0": f("ATM", E_, 2.0, "NC", 4, 2000, 1200, "SAE30", 4.0, 2000),
    "DEDION-1.8": f("ATM", E_, 1.8, "NC", 4, 2600, 1500, "SAE30", 4.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "De Dion-Bouton", lambda fam: "De Dion-Bouton")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Vis-à-vis", "Vis-à-vis", "1", "1900-01", "1902-12", [("0.4 4", "DEDION-0.4", 18)], portes=0, places=4, reservoir=15, remarques="Monocylindre arrière ; " + IND)
mg(L, "Type Q", "Q", "1", "1903-01", "1904-12", [("0.7 6", "DEDION-0.7", 28)], portes=0, places=2, reservoir=20, remarques="Voiturette monocylindre ; " + IND)
mg(L, "Populaire", "Populaire", "1", "1903-01", "1904-12", [("0.7 6", "DEDION-0.7", 28)], portes=0, places=2, reservoir=20, remarques="Voiturette ; " + IND)
mg(L, "Type AL", "AL", "1", "1906-01", "1907-12", [("1.9 15", "DEDION-1.9", 75)], portes=4, places=4, reservoir=45, remarques="Torpédo ; " + IND)
mg(L, "Type BS", "BS", "1", "1910-01", "1912-12", [("2.0 18", "DEDION-2.0", 80)], portes=4, places=4, reservoir=50, remarques="Torpédo ; " + IND)
mg(L, "Type IW", "IW", "1", "1923-01", "1925-12", [("1.8 25", "DEDION-1.8", 80)], portes=4, places=4, reservoir=45, remarques="Torpédo ; " + IND)

MOT = Motorisations("De Dion-Bouton", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"De Dion-Bouton": L}
MOTEURS = MOT.moteurs()
