"""Mahindra (Mahindra & Mahindra, Mumbai) : générations, phases, motorisations (marché indien) et moteurs liés.
Bolero, KUV100, TUV300, XUV500, Bolero Neo, Scorpio-N, XUV 3XO, Thar ROXX, XUV 7XO et électriques BE 6 / XEV 9S (plateforme INGLO).
Ventes européennes limitées et ponctuelles (XUV500, KUV100) : marché indien de référence. Puissances en ch. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

FAMILLES = {
    "MAH-M2DICR-2.5D": f("TURBO", "DSL", 2.5, "COURROIE", 4, 3200, 1400, "15W40", 6.0, 10000),
    "MAH-MHAWK-2.2D": f("TURBO", "DSL", 2.2, "CHAINE", 4, 3750, 1600, "5W30", 6.5, 10000),
    "MAH-MHAWK100-1.5D": f("TURBO", "DSL", 1.5, "CHAINE", 3, 3750, 1600, "5W30", 5.5, 10000),
    "MAH-MFALCON-1.2": f("ATM", "ESS", 1.2, "CHAINE", 3, 5500, 3500, "5W30", 3.5, 10000),
    "MAH-MSTALLION-1.2T": f("TURBO", "ESS", 1.2, "CHAINE", 3, 5000, 1500, "5W30", 4.0, 10000),
    "MAH-MSTALLION-2.0T": f("TURBO", "ESS", 2.0, "CHAINE", 4, 5000, 1750, "5W30", 5.5, 10000),
    "MAH-1.5D": f("TURBO", "DSL", 1.5, "CHAINE", 4, 3750, 1500, "5W30", 5.0, 10000),
    "MAH-INGLO-EV": electrique(),
}
mg = SaisieMoteurs(FAMILLES, "Mahindra")
L = []
IND = "marché indien ; données indicatives"
mg(L, "Bolero Classic", "Bolero", "1", "2000-01", "2020-03", [("Diesel 2.5 63", "MAH-M2DICR-2.5D", 195)], portes=5, places=7, reservoir=60, remarques="Tout-terrain utilitaire ; " + IND)
mg(L, "XUV500", "XUV500", "1", "2011-09", "2021-06", [("2.2 mHawk 140", "MAH-MHAWK-2.2D", 330), ("2.2 mHawk 155", "MAH-MHAWK-2.2D", 360, {"debut": "2018-04"})], portes=5, places=7, reservoir=70,
   remarques="Vendu aussi en Italie et en Espagne ; " + IND)
mg(L, "TUV300", "TUV300", "1", "2015-09", "2020-03", [("Diesel 1.5 mHawk100 100", "MAH-MHAWK100-1.5D", 240)], portes=5, places=7, reservoir=60, remarques=IND)
mg(L, "KUV100", "KUV100", "1", "2016-01", "2022-04", [("1.2 mFalcon 82", "MAH-MFALCON-1.2", 115), ("Diesel 1.2 78", "MAH-MHAWK100-1.5D", 190, {"fin": "2020-03"})], portes=5, places=5, reservoir=35,
   remarques="Diesel 1.2 rattaché à la famille mHawk ; " + IND)
mg(L, "Bolero Neo", "Bolero Neo", "1", "2021-07", None, [("Diesel 1.5 mHawk100 100", "MAH-MHAWK100-1.5D", 260)], portes=5, places=7, reservoir=50, remarques="Ex-TUV300 restylé ; " + IND)
mg(L, "Scorpio-N", "Scorpio-N", "1", "2022-06", None, [("2.0 mStallion 203", "MAH-MSTALLION-2.0T", 380), ("Diesel 2.2 mHawk 132", "MAH-MHAWK-2.2D", 300), ("Diesel 2.2 mHawk 175", "MAH-MHAWK-2.2D", 400)],
   portes=5, places=7, reservoir=57, remarques=IND)
mg(L, "XUV 3XO", "XUV 3XO", "1", "2024-04", None, [("1.2 TCMPFi 111", "MAH-MSTALLION-1.2T", 200), ("1.2 TGDi 131", "MAH-MSTALLION-1.2T", 230), ("Diesel 1.5 117", "MAH-1.5D", 300)],
   portes=5, places=5, reservoir=42, remarques="Ex-XUV300 restylé ; " + IND)
mg(L, "Thar ROXX", "Thar ROXX", "1", "2024-08", None, [("2.0 mStallion 177", "MAH-MSTALLION-2.0T", 380), ("Diesel 2.2 mHawk 175", "MAH-MHAWK-2.2D", 400)], portes=5, places=5, reservoir=57,
   remarques="Thar 5 portes ; " + IND)
mg(L, "XUV 7XO", "XUV 7XO", "1", "2026-01", None, [("2.0 mStallion 203", "MAH-MSTALLION-2.0T", 380), ("Diesel 2.2 mHawk 185", "MAH-MHAWK-2.2D", 450)], portes=5, places=7, reservoir=60,
   remarques="Successeur du XUV700 ; " + IND)
mg(L, "BE6", "BE 6", "1", "2025-01", None, [("Électrique 59 kWh 231", "MAH-INGLO-EV", 380, {"batterie": 59}), ("Électrique 79 kWh 286", "MAH-INGLO-EV", 380, {"batterie": 79})], portes=5, places=5, reservoir=0,
   remarques="SUV coupé électrique (plateforme INGLO) ; " + IND)
mg(L, "BE6 Formula E", "BE 6", "F", "2025-08", None, [("Électrique 79 kWh 286", "MAH-INGLO-EV", 380, {"batterie": 79})], portes=5, places=5, reservoir=0, remarques="Série spéciale Formula E ; " + IND)
mg(L, "XEV 9S", "XEV 9S", "1", "2025-11", None, [("Électrique 59 kWh 231", "MAH-INGLO-EV", 380, {"batterie": 59}), ("Électrique 79 kWh 286", "MAH-INGLO-EV", 380, {"batterie": 79})], portes=5, places=7, reservoir=0,
   remarques="SUV électrique 7 places ; " + IND)

MOT = Motorisations("Mahindra", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Mahindra": L}
MOTEURS = MOT.moteurs()
