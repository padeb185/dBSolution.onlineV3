"""Decauville : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur de Corbeil (matériel ferroviaire) : Voiturelle (1898-1902) et Type 10 HP (1902-1905). Puissances en ch.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "DECAUVILLE-0.5": f("ATM", "ESS", 0.5, "NC", 2, 1500, 1000, "SAE30", 1.0, 1000),
    "DECAUVILLE-1.6": f("ATM", "ESS", 1.6, "NC", 2, 1400, 900, "SAE30", 2.5, 2000),
}
mg = SaisieMoteurs(FAMILLES, "Decauville", lambda fam: "Decauville")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Voiturelle", "Voiturelle", "1", "1898-01", "1902-12", [("0.5 4", "DECAUVILLE-0.5", 20)], portes=0, places=2, reservoir=10,
   remarques="Voiturette à bicylindre arrière (De Dion) ; " + IND)
mg(L, "Type 10 HP", "10 HP", "1", "1902-01", "1905-12", [("1.6 10", "DECAUVILLE-1.6", 55)], portes=0, places=4, reservoir=40, remarques="Tonneau ; " + IND)

MOT = Motorisations("Decauville", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Decauville": L}
MOTEURS = MOT.moteurs()
