"""Gutbrod : générations, phases, motorisations (marché européen) et moteurs liés.
Gutbrod (Plochingen) : Superior (1950-1954), petite voiture à traction avant et bicylindre deux-temps, injection directe (Bosch) dès 1952.
Deux-temps : distribution « aucune », huile « à choisir » (mélange). Puissances en ch DIN. Données indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {"GUTBROD-2T-0.66": f("ATM", "ESS", 0.66, "AUCUNE", 2, 4000, 2800, "CHOISIR", 0.0, 3000)}
mg = SaisieMoteurs(FAMILLES, "Gutbrod", lambda fam: "Gutbrod")
L = []

mg(L, "Superior", "Superior", "1", "1950-01", "1954-12", [("0.66 2T 20", "GUTBROD-2T-0.66", 42), ("Injection 0.66 2T 30", "GUTBROD-2T-0.66", 48, {"debut": "1952-01"})],
   portes=2, places=4, reservoir=30, remarques="Berline, cabriolet et break ; une des premières injections directes d'essence en série ; données indicatives, à vérifier")

MOT = Motorisations("Gutbrod", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Gutbrod": L}
MOTEURS = MOT.moteurs()
