"""Geely : générations, phases, motorisations (marché européen) et moteurs liés.
Gamme européenne (lancement au Royaume-Uni en octobre 2025) : EX5 (SUV électrique) et Starray EM-i (SUV hybride rechargeable).
Les modèles destinés à la Chine et aux marchés émergents (Emgrand, Coolray, Atlas, Boyue, Geometry, Panda…) ne sont pas repris.
Puissances converties en ch.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

FAMILLES = {
    "GEELY-GEA-EV": electrique(),
    "GEELY-1.5-EMI": f("HYB_E", "ESS", 1.5, "CHAINE", 4, 6000, 4500, "0W20", 4.0, 15000),
}
mg = SaisieMoteurs(FAMILLES, "Geely", lambda fam: "Geely")
L = []

mg(L, "EX5", "EX5", "1", "2025-10", None, [("Électrique 60 kWh 218", "GEELY-GEA-EV", 320, {"batterie": 60}),
                                          ("Ultra Électrique 68 kWh 218", "GEELY-GEA-EV", 320, {"batterie": 68, "debut": "2026-05"})],
   portes=5, places=5, reservoir=0, remarques="SUV électrique (Proton e.MAS 7) ; couple indicatif")
mg(L, "Starray EM-i", "Starray", "1", "2026-02", None, [("Super Hybrid 1.5 262", "GEELY-1.5-EMI", 262, {"batterie": 18}),
                                                       ("Super Hybrid Ultra 1.5 262", "GEELY-1.5-EMI", 262, {"batterie": 29})],
   portes=5, places=5, reservoir=52, remarques="SUV hybride rechargeable (193 kW cumulés), batterie 18,4 ou 28,9 kWh ; réservoir indicatif")

MOT = Motorisations("Geely", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Geely": L}
MOTEURS = MOT.moteurs()
