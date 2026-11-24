"""DeLorean (DeLorean Motor Company, Dunmurry, Irlande du Nord) : modèle, motorisation et moteur lié.
DMC-12 (1981-1983, environ 9 000 ex.). Le concept électrique Alpha5 (2022) n'a pas été produit.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {"PRV-2.85": f("ATM", "ESS", 2.85, "CHAINE", 6, 5500, 2750, "10W40", 5.5, 10000, a="V")}

mg = SaisieMoteurs(FAMILLES, "DeLorean")
L = []

mg(L, "DMC-12", "DMC-12", "1", "1981-01", "1983-12", [("DMC-12 2.85 V6 132", "PRV-2.85", 208)], portes=2, places=2, reservoir=51,
   remarques="Coupé à portes papillon, carrosserie inox ; V6 PRV (Peugeot-Renault-Volvo) ; version nord-américaine, données indicatives")

MOT = Motorisations("DeLorean", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"DeLorean": L}
MOTEURS = MOT.moteurs()
