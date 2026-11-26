"""Ultima Sports : générations, phases, motorisations (marché européen, Royaume-Uni) et moteurs liés.
Sport, Spyder, GTR (dont GTR 720), Evolution (coupé et cabriolet) et RS. Voitures en kit ou montées usine, moteur V8 central
Chevrolet ; puissances selon la préparation choisie (versions de référence ci-dessous).
V8 Chevrolet repris de chevrolet.py (mêmes familles). Mk1 à Mk3 (1983-1992) non repris. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET

FAMILLES = {k: FAMILLES_CHEVROLET[k] for k in ("SBC-5.7", "LS3-6.2", "LS7-7.0", "LT1-6.2", "LT4-6.2SC", "LT5-6.2SC")}

mg = SaisieMoteurs(FAMILLES, "Ultima Sports", lambda fam: "Chevrolet")
L = []
IND = "voiture en kit ou montée usine ; données indicatives"

mg(L, "Sport", "Sport", "1", "1992-01", "1999-12", [("5.7 V8 355", "SBC-5.7", 475)], portes=2, places=2, reservoir=55, remarques="Coupé à moteur central ; " + IND)
mg(L, "Spyder", "Spyder", "1", "1993-01", "1999-12", [("5.7 V8 355", "SBC-5.7", 475)], portes=2, places=2, reservoir=55, remarques="Version ouverte ; " + IND)
mg(L, "GTR", "GTR", "1", "1999-01", "2015-12",
   [("5.7 V8 355", "SBC-5.7", 475, {"fin": "2006-12"}), ("6.2 V8 436", "LS3-6.2", 575, {"debut": "2007-01"}), ("7.0 V8 512", "LS7-7.0", 637, {"debut": "2007-01"}),
    ("720 6.2 V8 Compresseur 730", "LT4-6.2SC", 900, {"debut": "2010-01", "remarques": "GTR 720 (compresseur)"})], portes=2, places=2, reservoir=55, remarques="Coupé ; " + IND)
mg(L, "Evolution", "Evolution", "1", "2015-01", "2019-12",
   [("7.0 V8 512", "LS7-7.0", 637), ("6.2 V8 Compresseur 659", "LT4-6.2SC", 881), ("6.2 V8 Compresseur 1034", "LT4-6.2SC", 1200, {"remarques": "Préparation 1020 ch"})],
   portes=2, places=2, reservoir=55, remarques="Coupé et cabriolet ; " + IND)
mg(L, "RS", "RS", "1", "2019-10", None,
   [("6.2 V8 487", "LT1-6.2", 617), ("6.2 V8 Compresseur 659", "LT4-6.2SC", 881), ("6.2 V8 Compresseur 811", "LT5-6.2SC", 1000), ("6.2 V8 Compresseur 1217", "LT5-6.2SC", 1300)],
   portes=2, places=2, reservoir=55, remarques="Coupé et cabriolet ; jusqu'à 1 200 ch selon préparation ; " + IND)

MOT = Motorisations("Ultima Sports", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Ultima Sports": L}
MOTEURS = MOT.moteurs()
