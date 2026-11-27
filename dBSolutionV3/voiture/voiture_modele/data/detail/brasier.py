"""Brasier (Richard-Brasier) : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur d'Ivry-Port : Type TB (1908-1910) et TC4 (1920-1926). Puissances en ch.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "BRASIER-2.4": f("ATM", "ESS", 2.4, "NC", 4, 1600, 1000, "SAE30", 4.5, 2000),
    "BRASIER-2.1": f("ATM", "ESS", 2.1, "NC", 4, 2800, 1600, "SAE30", 4.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Brasier", lambda fam: "Brasier")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Type TB", "TB", "1", "1908-01", "1910-12", [("2.4 16", "BRASIER-2.4", 90)], portes=4, places=4, reservoir=55, remarques="Torpédo ; " + IND)
mg(L, "TC4", "TC4", "1", "1920-01", "1926-12", [("2.1 30", "BRASIER-2.1", 95)], portes=4, places=4, reservoir=50, remarques="Torpédo et berline ; " + IND)

MOT = Motorisations("Brasier", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Brasier": L}
MOTEURS = MOT.moteurs()
