"""Lordstown Motors (Lordstown, Ohio) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Endurance : pick-up électrique à quatre moteurs-roues, produit en quelques dizaines d'exemplaires (2022-2023) avant la faillite de juin 2023.
Puissance en ch ; couple indicatif.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

FAMILLES = {
    "LORDSTOWN-EV": electrique(),
}
mg = SaisieMoteurs(FAMILLES, "Lordstown")
L = []
mg(L, "Endurance", "Endurance", "1", "2022-09", "2023-06", [("Électrique 446", "LORDSTOWN-EV", 600, {"batterie": 109})], portes=4, places=5, reservoir=0,
   remarques="Pick-up électrique, quatre moteurs-roues, environ 35 à 40 exemplaires livrés ; couple indicatif")

MOT = Motorisations("Lordstown", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Lordstown": L}
MOTEURS = MOT.moteurs()
