"""NIO (Shanghai) : générations, phases, motorisations (marché européen) et moteurs liés.
Europe (Norvège dès 2021, puis Allemagne, Pays-Bas, Danemark, Suède) : ES8 (1re gén.), ET7, ET5 et ET5 Touring, EL6 (ES6 2e gén.), EL7 (ES7),
EL8 (ES8 2e gén.) et Firefly ; batteries échangeables (75 ou 100 kWh). Modèles chinois (EC6, EC7, ES9, ET9) non repris. Puissances en ch.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

FAMILLES = {
    "NIO-EV": electrique(),
}
mg = SaisieMoteurs(FAMILLES, "NIO")
L = []
IND = "batterie échangeable (Power Swap)"
B2 = lambda p, nm, **kw: [("Électrique 75 kWh " + str(p), "NIO-EV", nm, {"batterie": 75, **kw}), ("Électrique 100 kWh " + str(p), "NIO-EV", nm, {"batterie": 100, **kw})]
mg(L, "ES8", "ES8", "1", "2021-09", "2022-12", [("Électrique 100 kWh 544", "NIO-EV", 725, {"batterie": 100})], portes=5, places=7, reservoir=0, remarques="Lancé en Norvège ; " + IND)
mg(L, "ET7", "ET7", "1", "2022-10", None, B2(653, 850), portes=4, places=5, reservoir=0, remarques="Berline, deux moteurs (180 + 300 kW) ; " + IND)
mg(L, "ET5", "ET5", "1", "2022-10", None, B2(490, 700), portes=4, places=5, reservoir=0, remarques="Berline compacte ; " + IND)
mg(L, "ET5 Touring", "ET5", "T", "2023-06", None, B2(490, 700), portes=5, places=5, reservoir=0, remarques="Break ; " + IND)
mg(L, "EL7", "EL7", "1", "2022-10", None, B2(653, 850), portes=5, places=5, reservoir=0, remarques="ES7 en Chine ; " + IND)
mg(L, "EL6", "EL6", "1", "2023-07", None, B2(490, 700), portes=5, places=5, reservoir=0, remarques="ES6 de 2e génération en Chine ; " + IND)
mg(L, "EL8", "EL8", "1", "2024-09", None, B2(653, 850), portes=5, places=6, reservoir=0, remarques="ES8 de 2e génération en Chine ; " + IND)
mg(L, "Firefly", "Firefly", "1", "2025-04", None, [("Électrique 42 kWh 143", "NIO-EV", 200, {"batterie": 42})], portes=5, places=5, reservoir=0, remarques="Citadine électrique (marque Firefly) ; couple indicatif")

MOT = Motorisations("NIO", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"NIO": L}
MOTEURS = MOT.moteurs()
