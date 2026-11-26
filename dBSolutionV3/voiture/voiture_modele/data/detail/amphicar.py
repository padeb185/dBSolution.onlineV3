"""Amphicar : générations, phases, motorisations (marché européen) et moteurs liés.
770 (1961-1968), cabriolet amphibie allemand. Quatre cylindres Triumph 1147 cm³ repris de triumph.py (même famille).
Puissance en ch DIN. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .triumph import FAMILLES as FAMILLES_TRIUMPH

FAMILLES = {"TRIUMPH-SC-1.15": FAMILLES_TRIUMPH["TRIUMPH-SC-1.15"]}
mg = SaisieMoteurs(FAMILLES, "Triumph", lambda fam: "Triumph")
L = []

mg(L, "770", "770", "1", "1961-01", "1968-12", [("1.15 38", "TRIUMPH-SC-1.15", 80)], portes=2, places=4, reservoir=47,
   remarques="Cabriolet amphibie, moteur Triumph Herald 1200 en position arrière, environ 3 900 exemplaires ; données indicatives")

MOT = Motorisations("Amphicar", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Amphicar": L}
MOTEURS = MOT.moteurs()
