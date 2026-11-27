"""Equus : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Equus Automotive (Michigan) : Bass 770, coupé néo-rétro (inspiré des muscle cars) en aluminium et carbone, V8 6.2 LS9 à compresseur
(famille et couple repris de chevrolet.py). Puissance SAE convertie en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET

FAMILLES = {"LS9-6.2SC": FAMILLES_CHEVROLET["LS9-6.2SC"]}
mg = SaisieMoteurs(FAMILLES, "Chevrolet", lambda fam: "Chevrolet")
L = []

mg(L, "Bass 770", "Bass 770", "1", "2014-01", None, [("6.2 V8 Compresseur 647", "LS9-6.2SC", 819)], portes=2, places=4, reservoir=70,
   remarques="Coupé 2+2 artisanal, V8 LS9 de la Corvette ZR1 ; production limitée ; marché nord-américain ; données indicatives")

MOT = Motorisations("Equus", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Equus": L}
MOTEURS = MOT.moteurs()
