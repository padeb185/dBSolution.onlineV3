"""Falcon : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Falcon Motorsports (Michigan) : F7, supercar à moteur central et châssis carbone-aluminium, V8 7.0 dérivé du LS7 Chevrolet
(famille reprise de chevrolet.py). Puissance SAE convertie en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET

FAMILLES = {"LS7-7.0": FAMILLES_CHEVROLET["LS7-7.0"]}
mg = SaisieMoteurs(FAMILLES, "Chevrolet", lambda fam: "Chevrolet")
L = []

mg(L, "F7", "F7", "1", "2012-01", "2017-12", [("7.0 V8 629", "LS7-7.0", 813)], portes=2, places=2, reservoir=70,
   remarques="Supercar artisanale à moteur central, V8 LS7 préparé ; production très limitée ; marché nord-américain ; données indicatives")

MOT = Motorisations("Falcon", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Falcon": L}
MOTEURS = MOT.moteurs()
