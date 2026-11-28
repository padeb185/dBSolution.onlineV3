"""Marquette (Buick, 1929-1930) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Marque compagne de Buick, une seule année-modèle (Series 30, six cylindres Oldsmobile / Buick). Puissances brutes converties en ch (× 1,014).
Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "MARQUETTE-L6-3.5": f("ATM", "ESS", 3.5, "NC", 6, 3000, 1400, "SAE30", 5.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Buick")
L = []
mg(L, "Series 30", "30", "1", "1929-06", "1930-12", [("3.5 L6 68", "MARQUETTE-L6-3.5", 210)], portes=4, places=5, reservoir=55, remarques="Marché nord-américain ; données indicatives")

MOT = Motorisations("Buick", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Marquette": L}
MOTEURS = MOT.moteurs()
