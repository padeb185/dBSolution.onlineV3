"""Haynes-Apperson : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Constructeur de Kokomo (Indiana), 1898-1904, issu de la voiture d'Elwood Haynes et des frères Apperson (1894) ; scission en 1904
entre Haynes et Apperson (voir apperson.py). Bicylindre à plat. Puissances brutes converties en ch (× 1,014).
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {"HA-B2-2.6": f("ATM", "ESS", 2.6, "NC", 2, 1000, 700, "SAE30", 2.0, 1000, a="PLAT")}
mg = SaisieMoteurs(FAMILLES, "Haynes-Apperson")
L = []
IND = "désignations, cylindrée et dates indicatives (marque ancienne), à vérifier"

mg(L, "Runabout", "Runabout", "1", "1898-01", "1904-12", [("2.6 6", "HA-B2-2.6", 50, {"fin": "1901-12"}), ("2.6 12", "HA-B2-2.6", 90, {"debut": "1902-01"})],
   portes=0, places=2, reservoir=30, remarques="Voiturette à bicylindre à plat, transmission par chaîne ; " + IND)
mg(L, "Surrey", "Surrey", "1", "1901-01", "1904-12", [("2.6 12", "HA-B2-2.6", 90)], portes=0, places=4, reservoir=35, remarques="Quatre places ; " + IND)

MOT = Motorisations("Haynes-Apperson", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Haynes-Apperson": L}
MOTEURS = MOT.moteurs()
