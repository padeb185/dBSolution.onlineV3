"""Bignan : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur de Courbevoie : Type 11 HP (1920-1924) et Sport 2 L (1923-1926). Puissances en ch.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "BIGNAN-1.9": f("ATM", "ESS", 1.9, "NC", 4, 2800, 1600, "SAE30", 4.0, 3000),
    "BIGNAN-2.0-DOHC": f("ATM", "ESS", 2.0, "NC", 4, 4000, 2800, "SAE30", 4.5, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Bignan", lambda fam: "Bignan")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Type 11 HP", "11 HP", "1", "1920-01", "1924-12", [("1.9 25", "BIGNAN-1.9", 85)], portes=4, places=4, reservoir=50, remarques="Torpédo ; " + IND)
mg(L, "Sport 2 L", "Sport 2 L", "1", "1923-01", "1926-12", [("2.0 70", "BIGNAN-2.0-DOHC", 130)], portes=2, places=2, reservoir=60,
   remarques="Sport à double arbre, victoires en course (Bol d'Or, Le Mans) ; " + IND)

MOT = Motorisations("Bignan", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Bignan": L}
MOTEURS = MOT.moteurs()
