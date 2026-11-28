"""Hongqi (FAW) : générations, phases, motorisations (marché européen) et moteurs liés.
Historique (Chine) : CA72 et CA770, limousines officielles à V8. Europe (depuis fin 2022, Norvège, Pays-Bas, Allemagne, France…) :
E-HS9 (SUV électrique), EH7 (berline) et EHS7 (SUV) sur plateforme électrique Tiangong. Modèles chinois (H5, H7, H9, L5, HS5, HS7…)
non repris ; EHS5 (2026) et dérivé de la Leapmotor B10 non repris faute de données européennes définitives.
Puissances en ch ; couples des électriques indicatifs.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

FAMILLES = {
    "HONGQI-V8-5.6": f("ATM", "ESS", 5.6, "CHAINE", 8, 4400, 2800, "20W50", 6.0, 5000, a="V"),
    "HONGQI-EV": electrique(),
}
mg = SaisieMoteurs(FAMILLES, "Hongqi")
L = []
IND = "données indicatives"

mg(L, "CA72", "CA72", "1", "1958-08", "1965-12", [("5.6 V8 200", "HONGQI-V8-5.6", 400)], portes=4, places=5, reservoir=90,
   remarques="Première limousine Hongqi (« Drapeau rouge »), marché chinois ; " + IND)
mg(L, "CA770", "CA770", "1", "1965-01", "1981-12", [("5.6 V8 220", "HONGQI-V8-5.6", 420)], portes=4, places=7, reservoir=90,
   remarques="Limousine officielle, marché chinois ; " + IND)
mg(L, "E-HS9", "E-HS9", "1", "2022-12", "2026-02",
   [("Électrique 99 kWh 435", "HONGQI-EV", 600, {"batterie": 99}), ("Électrique 120 kWh 551", "HONGQI-EV", 750, {"batterie": 120, "debut": "2023-09"})],
   portes=5, places=6, reservoir=0, remarques="Grand SUV électrique à deux moteurs, 6 ou 7 places ; couple de la version 99 kWh indicatif")
mg(L, "EH7", "EH7", "1", "2025-01", None,
   [("Électrique 85 kWh 344", "HONGQI-EV", 450, {"batterie": 85}), ("Long Range Électrique 111 kWh 344", "HONGQI-EV", 450, {"batterie": 111}),
    ("AWD Électrique 111 kWh 619", "HONGQI-EV", 750, {"batterie": 111})],
   portes=4, places=5, reservoir=0, remarques="Berline électrique (plateforme Tiangong), propulsion ou transmission intégrale ; couples indicatifs")
mg(L, "EHS7", "EHS7", "1", "2025-08", None,
   [("Électrique 85 kWh 343", "HONGQI-EV", 450, {"batterie": 85}), ("Long Range Électrique 111 kWh 343", "HONGQI-EV", 450, {"batterie": 111}),
    ("AWD Électrique 111 kWh 619", "HONGQI-EV", 750, {"batterie": 111})],
   portes=5, places=5, reservoir=0, remarques="SUV électrique dérivé de l'EH7 ; couples indicatifs")

MOT = Motorisations("Hongqi", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Hongqi": L}
MOTEURS = MOT.moteurs()
