"""Caparo : générations, phases, motorisations (marché européen) et moteurs liés.
T1 (Caparo Vehicle Technologies), biplace homologuée pour la route à moteur central, V8 3.5 atmosphérique Menard
dérivé du moteur IndyCar Nissan. Puissances bhp converties en ch (× 1,014). Dates de fin indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {"MENARD-V8-3.5": f("ATM", "ESS", 3.5, "CHAINE", 8, 10500, 9000, "5W50", 8.0, 3000, a="V")}
mg = SaisieMoteurs(FAMILLES, "Menard", lambda fam: "Menard")
L = []

mg(L, "T1", "T1", "1", "2007-07", "2015-12", [("3.5 V8 583", "MENARD-V8-3.5", 420), ("Race Extreme 3.5 V8 630", "MENARD-V8-3.5", 475, {"debut": "2010-01"})],
   portes=0, places=2, reservoir=60, remarques="Monocoque carbone-aluminium, plus de 1 000 bhp par tonne ; Race Extreme orientée circuit ; dates de fin indicatives")

MOT = Motorisations("Caparo", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Caparo": L}
MOTEURS = MOT.moteurs()
