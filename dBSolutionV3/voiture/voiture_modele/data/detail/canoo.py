"""Canoo : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Lifestyle Vehicle (LV), monospace électrique sur plate-forme « skateboard », batterie 80 kWh, moteur arrière.
Livraisons à partir de fin 2023 ; faillite (Chapter 7) le 17 janvier 2025. Puissance (paramétrable 200 à 350 hp) indicative.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique

FAMILLES = {"CANOO-EV": electrique()}
mg = SaisieMoteurs(FAMILLES, "Canoo", lambda fam: "Canoo")
L = []

mg(L, "Lifestyle Vehicle", "LV", "1", "2023-12", "2025-01", [("Électrique 80 kWh 304", "CANOO-EV", 412, {"batterie": 80})], portes=5, places=7, reservoir=0,
   remarques="Monospace électrique 5 à 7 places, propulsion ; puissance logicielle de 200 à 350 hp ; quelques centaines d'exemplaires, surtout flottes ; marché nord-américain")

MOT = Motorisations("Canoo", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Canoo": L}
MOTEURS = MOT.moteurs()
