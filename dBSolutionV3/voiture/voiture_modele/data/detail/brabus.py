"""Brabus (Bottrop) : véhicules complets « supercars » Brabus, avec le modèle de base dans la génération, et moteurs liés.
Bases Mercedes-AMG (Classe G, Classe S, AMG GT 4 portes) et, depuis 2025, Bentley Continental GT et Lamborghini Urus.
Kits de préparation seuls et smart Brabus non repris. Données de production indicatives (séries très limitées).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "BRABUS-V12-6.3BT": f("TURBO", E_, 6.3, "CHAINE", 12, 5500, 2100, "5W40", 9.5, 15000, a="V"),
    "BRABUS-V8-4.0BT": f("TURBO", E_, 4.0, "CHAINE", 8, 6600, 3600, "0W40", 9.0, 15000, a="V"),
    "BRABUS-V8-4.5BT": f("TURBO", E_, 4.5, "CHAINE", 8, 6200, 2900, "0W40", 9.0, 15000, a="V"),
    "BRABUS-V8-4.5-PHEV": f("HYB_TE", E_, 4.5, "CHAINE", 8, 6200, 2500, "0W40", 9.0, 15000, a="V"),
    "BRABUS-V8-4.0-PHEV": f("HYB_TE", E_, 4.0, "CHAINE", 8, 6000, 2500, "0W40", 9.0, 15000, a="V"),
}

mg = SaisieMoteurs(FAMILLES, "Brabus")
L = []
LIM = "Série limitée ; données indicatives"

mg(L, "Rocket 900", "W222 S 65", "1", "2015-09", "2017-12", [("Rocket 900 6.3 V12 900", "BRABUS-V12-6.3BT", 1200)], portes=4, places=4, reservoir=80,
   remarques="Base Mercedes-AMG S 65 (berline, coupé et cabriolet) ; couple limité électroniquement ; " + LIM)
mg(L, "700", "W463A G 63", "1", "2018-06", "2024-03", [("700 Widestar 700", "BRABUS-V8-4.0BT", 960)], reservoir=100, remarques="Base Mercedes-AMG G 63 W463A")
mg(L, "800", "W463A G 63", "1", "2018-06", "2024-03", [("800 Widestar 800", "BRABUS-V8-4.0BT", 1000), ("XLP 800 Adventure 800", "BRABUS-V8-4.0BT", 1000, {"debut": "2021-06"})],
   reservoir=100, remarques="Base Mercedes-AMG G 63 W463A ; XLP pick-up")
mg(L, "800", "Mercedes-AMG 4.0 V8", "1", "2017-09", "2023-12",
   [("800 GLE 63 S 800", "BRABUS-V8-4.0BT", 1000, {"debut": "2020-09"}), ("800 E 63 S 800", "BRABUS-V8-4.0BT", 1000), ("800 S 63 800", "BRABUS-V8-4.0BT", 1000, {"debut": "2018-01"})],
   reservoir=80, remarques="Bases Mercedes-AMG E 63 S, S 63 et GLE 63 S")
mg(L, "900 Rocket", "W463A G 63", "1", "2021-03", "2023-12",
   [("G 900 Rocket 900", "BRABUS-V8-4.5BT", 1250), ("900 Deep Blue 900", "BRABUS-V8-4.5BT", 1250, {"debut": "2022-06"}),
    ("P 900 Rocket 900", "BRABUS-V8-4.5BT", 1250, {"debut": "2023-01"})], reservoir=100, remarques="Base Mercedes-AMG G 63 W463A (moteur 4.5 réalésé) ; " + LIM)
mg(L, "Rocket 900", "X290 AMG GT 63 S", "1", "2021-01", "2022-12", [("Rocket 900 One of 25 900", "BRABUS-V8-4.5BT", 1250)], portes=4, places=4, reservoir=80,
   remarques="Base Mercedes-AMG GT 63 S 4 portes ; 25 ex.")
mg(L, "Rocket 1000", "X290 AMG GT 63 S E Performance", "1", "2023-01", "2024-12", [("Rocket 1000 1000", "BRABUS-V8-4.5-PHEV", 1820)], portes=4, places=4,
   reservoir=80, batterie=6, remarques="Base Mercedes-AMG GT 63 S E Performance (hybride rechargeable) ; " + LIM)
mg(L, "930", "AMG E Performance", "1", "2023-06", "2025-06",
   [("930 GT 63 S E Performance 930", "BRABUS-V8-4.0-PHEV", 1500), ("930 S 63 E Performance 930", "BRABUS-V8-4.0-PHEV", 1500, {"debut": "2024-01"})],
   portes=4, places=4, reservoir=80, batterie=6, remarques="Bases Mercedes-AMG GT 63 S E Performance et S 63 E Performance")
mg(L, "800", "W465 G 63", "1", "2024-06", None,
   [("800 G 63 800", "BRABUS-V8-4.0BT", 1000), ("800 Cabrio 800", "BRABUS-V8-4.0BT", 1000, {"debut": "2025-03"}), ("800 XL Cabrio 800", "BRABUS-V8-4.0BT", 1000, {"debut": "2025-06"})],
   reservoir=100, remarques="Base Mercedes-AMG G 63 W465 (micro-hybride) ; cabriolets 2025")
mg(L, "900 Rocket Edition", "W465 G 63", "1", "2026-01", None,
   [("900 Rocket Edition 900", "BRABUS-V8-4.5BT", 1250), ("P 900 Rocket Edition 900", "BRABUS-V8-4.5BT", 1250, {"debut": "2026-10"})], reservoir=100,
   remarques="Base Mercedes-AMG G 63 W465 ; 30 ex. ; P = pick-up (888 hp annoncés)")
mg(L, "900", "Bentley Continental GT Speed", "1", "2025-11", None, [("900 Continental GT 900", "BRABUS-V8-4.0-PHEV", 1100), ("900 Superblack 900", "BRABUS-V8-4.0-PHEV", 1100)],
   portes=2, places=4, reservoir=80, batterie=26, remarques="Base Bentley Continental GT / GTC Speed (V8 hybride rechargeable) ; couple indicatif")
mg(L, "900", "Lamborghini Urus SE", "1", "2026-02", None, [("900 Superblack 900", "BRABUS-V8-4.0-PHEV", 1100), ("900 Mint 900", "BRABUS-V8-4.0-PHEV", 1100)],
   reservoir=80, batterie=26, remarques="Base Lamborghini Urus SE (V8 hybride rechargeable) ; couple indicatif")

MOT = Motorisations("Brabus", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Brabus": L}
MOTEURS = MOT.moteurs()
