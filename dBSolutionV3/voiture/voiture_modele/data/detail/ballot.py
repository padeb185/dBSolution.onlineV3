"""Ballot : générations, phases, motorisations (marché européen) et moteurs liés.
2 LS (sport à double arbre, 1922-1925), 2 LT (1923-1928) et RH (huit cylindres, 1928-1932). Constructeur parisien.
Puissances en ch. Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "BALLOT-2.0-DOHC": f("ATM", E_, 2.0, "NC", 4, 5000, 3500, "SAE30", 5.0, 3000),
    "BALLOT-2.0": f("ATM", E_, 2.0, "NC", 4, 3500, 2000, "SAE30", 5.0, 3000),
    "BALLOT-L8-2.9": f("ATM", E_, 2.9, "NC", 8, 3600, 2000, "SAE30", 6.5, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Ballot", lambda fam: "Ballot")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "2 LS", "2 LS", "1", "1922-01", "1925-12", [("2.0 75", "BALLOT-2.0-DOHC", 130)], portes=2, places=2, reservoir=60, remarques="Sport à double arbre à cames en tête ; " + IND)
mg(L, "2 LT", "2 LT", "1", "1923-01", "1928-12", [("2.0 35", "BALLOT-2.0", 100)], portes=4, places=4, reservoir=55, remarques="Berline et torpédo ; " + IND)
mg(L, "RH", "RH", "1", "1928-01", "1932-12", [("2.9 L8 70", "BALLOT-L8-2.9", 160)], portes=4, places=5, reservoir=70,
   remarques="Huit cylindres en ligne (RH, RH2, RH3) ; reprise par Hispano-Suiza (1931) ; " + IND)

MOT = Motorisations("Ballot", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Ballot": L}
MOTEURS = MOT.moteurs()
