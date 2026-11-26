"""ADK : générations, phases, motorisations et moteurs liés.
Mk 2 (roadster de type Seven, années 1978-1985). Petit constructeur peu documenté : désignation, dates et moteur indicatifs
(quatre cylindres Ford Kent, comme la plupart des roadsters de ce type), à vérifier.
Moteur Ford Kent repris de caterham.py (même famille).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .caterham import FAMILLES as FAMILLES_CATERHAM

FAMILLES = {"KENT-1.6": FAMILLES_CATERHAM["KENT-1.6"]}

mg = SaisieMoteurs(FAMILLES, "ADK", lambda fam: "Ford")
L = []

mg(L, "Mk 2", "Mk 2", "1", "1978-01", "1985-12", [("1.6 84", "KENT-1.6", 130)], portes=0, places=2, reservoir=36,
   remarques="Roadster ; désignation, dates et moteur indicatifs (marque peu documentée), à vérifier")

MOT = Motorisations("ADK", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"ADK": L}
MOTEURS = MOT.moteurs()
