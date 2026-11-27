"""Bollinger : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Bollinger Motors (Michigan) : B4, camion électrique de classe 4 à cabine avancée (production sept. 2024, fermeture nov. 2025).
Les B1 et B2 (SUV et pick-up) sont restés à l'état de prototypes et ne sont pas repris.
Puissance SAE convertie en ch (× 1,014).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique

FAMILLES = {"DANA-B4-EV": electrique()}
mg = SaisieMoteurs(FAMILLES, "Dana", lambda fam: "Dana")
L = []

mg(L, "B4", "B4", "1", "2024-09", "2025-11", [("Électrique 158 kWh 328", "DANA-B4-EV", 915, {"batterie": 158})], portes=2, places=3, reservoir=0,
   remarques="Camion électrique classe 4 (PTAC 15 500 lb), batterie LFP 800 V, moteur arrière Dana ; assemblé par Roush ; marché nord-américain")

MOT = Motorisations("Bollinger", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Bollinger": L}
MOTEURS = MOT.moteurs()
