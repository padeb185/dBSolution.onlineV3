"""Faraday Future : générations, phases, motorisations (marché nord-américain) et moteurs liés.
FF 91 2.0 (Futurist Alliance, Futurist), crossover électrique de luxe assemblé à Hanford (Californie) : trois moteurs, 1 050 hp,
1 977 Nm, batterie 142 kWh. Production depuis mars 2023, livraisons depuis mai 2023, en très petit nombre.
Puissance convertie en ch (× 1,014).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique

FAMILLES = {"FF-TRI-EV": electrique()}
mg = SaisieMoteurs(FAMILLES, "Faraday Future", lambda fam: "Faraday Future")
L = []

mg(L, "FF 91", "FF 91 2.0", "1", "2023-05", None, [("Électrique 142 kWh 1065", "FF-TRI-EV", 1977, {"batterie": 142})], portes=5, places=4, reservoir=0,
   remarques="Futurist Alliance (série limitée) et Futurist ; trois moteurs, transmission intégrale ; livraisons très limitées ; marché nord-américain")

MOT = Motorisations("Faraday Future", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Faraday Future": L}
MOTEURS = MOT.moteurs()
