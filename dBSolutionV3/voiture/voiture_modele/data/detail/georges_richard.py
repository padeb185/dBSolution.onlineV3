"""Georges Richard : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur d'Ivry-Port (1897-1905, devenu Unic) : Type C (voiturette dérivée de la Vivinus belge) et Poney. Puissances en ch.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "GRICHARD-0.7": f("ATM", "ESS", 0.7, "NC", 1, 1500, 1000, "SAE30", 1.0, 1000),
    "GRICHARD-1.3": f("ATM", "ESS", 1.3, "NC", 2, 1400, 900, "SAE30", 2.0, 1000),
}
mg = SaisieMoteurs(FAMILLES, "Georges Richard", lambda fam: "Georges Richard")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Type C", "C", "1", "1899-01", "1902-12", [("0.7 5", "GRICHARD-0.7", 25)], portes=0, places=2, reservoir=10, remarques="Voiturette sous licence Vivinus ; " + IND)
mg(L, "Poney", "Poney", "1", "1901-01", "1903-12", [("1.3 8", "GRICHARD-1.3", 40)], portes=0, places=2, reservoir=15, remarques="Voiturette bicylindre ; " + IND)

MOT = Motorisations("Georges Richard", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Georges Richard": L}
MOTEURS = MOT.moteurs()
