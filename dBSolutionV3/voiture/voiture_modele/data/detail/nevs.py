"""NEVS (National Electric Vehicle Sweden, Trollhättan) : générations, phases, motorisations et moteurs liés.
Repreneur des actifs de Saab (2012) : la 9-3 thermique 2013-2014 (vendue Saab) est dans saab.py ; ici la 9-3 électrique (série pilote pour la
Chine, 2017-2019). Projet Emily GT non produit. Puissance en ch ; données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

FAMILLES = {
    "NEVS-EV": electrique(),
}
mg = SaisieMoteurs(FAMILLES, "NEVS")
L = []
mg(L, "9-3 EV", "9-3", "1", "2017-12", "2019-12", [("Électrique 177", "NEVS-EV", 285, {"batterie": 48})], portes=4, places=5, reservoir=0,
   remarques="Berline électrique sur base Saab 9-3, série pilote (Tianjin / Trollhättan) ; données indicatives")

MOT = Motorisations("NEVS", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"NEVS": L}
MOTEURS = MOT.moteurs()
