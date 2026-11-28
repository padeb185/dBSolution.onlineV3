"""Lotec (Kolbermoor, Bavière) : générations, phases, motorisations (marché européen) et moteurs liés.
Sirius (2000-2001), supercar à V12 Mercedes-Benz 6.0 biturbo, exemplaire unique ou quasi unique ; C1000 (prototype, 1995) non repris.
Puissance en ch. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "LOTEC-V12-6.0TT": f("TURBO", "ESS", 6.0, "CHAINE", 12, 6500, 4000, "10W40", 10.0, 10000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Mercedes-Benz")
L = []
mg(L, "Sirius", "Sirius", "1", "2000-01", "2001-12", [("6.0 V12 Biturbo 1000", "LOTEC-V12-6.0TT", 1320)], portes=2, places=2, reservoir=100,
   remarques="Supercar à moteur central, V12 Mercedes M120 biturbo ; exemplaire unique ; données indicatives")

MOT = Motorisations("Mercedes-Benz", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Lotec": L}
MOTEURS = MOT.moteurs()
