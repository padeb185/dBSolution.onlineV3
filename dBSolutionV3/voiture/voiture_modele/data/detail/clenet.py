"""Clénet : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Néo-classiques de Santa Barbara (Alain Clénet) : Series I (roadster sur base Lincoln Continental Mark V, 1976-1979)
et Series II (cabriolet sur base Mercury Cougar, 1979-1982). V8 Ford repris de lincoln.py (mêmes familles, couples et motoristes).
Puissances SAE nettes converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .lincoln import FAMILLES as FAMILLES_LINCOLN, motoriste as motoriste_lincoln

FAMILLES = {k: FAMILLES_LINCOLN[k] for k in ("FORD-335-6.6", "FORD-WINDSOR-5.8")}
mg = SaisieMoteurs(FAMILLES, "Ford", motoriste_lincoln)
L = []
NA = "marché nord-américain ; données indicatives"

mg(L, "Series I", "Series I", "1", "1976-01", "1979-12", [("6.6 V8 182", "FORD-335-6.6", 400)], portes=2, places=2, reservoir=95,
   remarques="Roadster néo-classique (250 exemplaires), châssis Lincoln Continental Mark V ; " + NA)
mg(L, "Series II", "Series II", "1", "1979-01", "1982-12", [("5.8 V8 137", "FORD-WINDSOR-5.8", 373)], portes=2, places=4, reservoir=76,
   remarques="Cabriolet 4 places, base Mercury Cougar ; " + NA)

MOT = Motorisations("Clénet", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Clénet": L}
MOTEURS = MOT.moteurs()
