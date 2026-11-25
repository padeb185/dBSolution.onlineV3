"""Gordon Murray Automotive : générations, phases, motorisations et moteurs liés.
T.50, T.50s Niki Lauda (circuit), T.33, T.33 Spider ; Gordon Murray Special Vehicles : S1 LM, S1, Le Mans GTR.
V12 atmosphériques Cosworth (motoriste « Cosworth »). Très petites séries : les dates des modèles pas encore livrés
(T.33, T.33 Spider, S1, Le Mans GTR) sont indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"

FAMILLES = {
    "GMA-V12-3.9": f("ATM", E_, 3.9, "NC", 12, 11500, 9000, "10W60", 9.0, 15000, a="V"),
    "GMA-V12-4.0": f("ATM", E_, 4.0, "NC", 12, 11500, 9000, "10W60", 9.0, 15000, a="V"),
    "GMA-V12-4.2": f("ATM", E_, 4.2, "NC", 12, 11000, 4000, "10W60", 9.0, 15000, a="V"),
    "GMA-V12-4.3": f("ATM", E_, 4.3, "NC", 12, 11500, 9000, "10W60", 9.0, 15000, a="V"),
}

mg = SaisieMoteurs(FAMILLES, "Cosworth")
L = []

mg(L, "T.50", "T.50", "1", "2023-01", "2025-06", [("3.9 V12 663", "GMA-V12-3.9", 467)], portes=2, places=3, reservoir=60,
   remarques="100 exemplaires, conduite centrale, ventilateur aérodynamique, boîte manuelle 6 ; dates indicatives")
mg(L, "T.50s Niki Lauda", "T.50s", "1", "2025-09", None, [("3.9 V12 735", "GMA-V12-3.9", 485)], portes=2, places=1, reservoir=60,
   remarques="Version circuit non homologuée, 25 exemplaires ; boîte séquentielle 6 à palettes")
mg(L, "T.33", "T.33", "1", "2026-12", None, [("3.9 V12 615", "GMA-V12-3.9", 451)], portes=2, places=2, reservoir=65,
   remarques="Production annoncée pour fin 2026 après plusieurs reports ; date indicative")
mg(L, "T.33 Spider", "T.33 Spider", "1", "2027-06", None, [("3.9 V12 617", "GMA-V12-3.9", 451)], portes=2, places=2, reservoir=65,
   remarques="Targa à toit amovible ; prototypes de validation en 2026 ; date indicative")
mg(L, "S1 LM", "S1 LM", "1", "2026-01", None, [("4.3 V12 700", "GMA-V12-4.3", 470)], portes=2, places=3, reservoir=60,
   remarques="Gordon Murray Special Vehicles, 5 exemplaires pour un seul client ; hommage à la McLaren F1 GTR ; date indicative")
mg(L, "S1", "S1", "1", "2027-06", None, [("4.2 V12 690", "GMA-V12-4.2", 500)], portes=2, places=3, reservoir=60,
   remarques="Gordon Murray Special Vehicles, 64 exemplaires, GT dérivée de la S1 LM ; date indicative")
mg(L, "Le Mans GTR", "Le Mans GTR", "1", "2027-01", None, [("4.0 V12 664", "GMA-V12-4.0", 467)], portes=2, places=3, reservoir=60,
   remarques="Gordon Murray Special Vehicles, 24 exemplaires à longue queue ; livraisons prévues en 2027, date indicative")

MOT = Motorisations("Cosworth", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Gordon Murray Automotive": L}
MOTEURS = MOT.moteurs()
