"""Artega : générations, phases, motorisations (marché européen) et moteurs liés.
GT (coupé à moteur central, V6 Volkswagen 3.6 FSI, 2009-2012) et Karo / Karo-Isetta (micro-citadine électrique L7e, 2020-2022).
V6 3.6 repris de volkswagen.py (même famille et couple). Les concepts Scalo, SE et Scalo Superelletra ne sont pas repris.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique
from .volkswagen import FAMILLES as FAMILLES_VW

VW = {"VR6-3.6": FAMILLES_VW["VR6-3.6"]}
FAMILLES = {**VW, "ARTEGA-KARO-EV": electrique()}


def motoriste(fam):
    return "Volkswagen" if fam in VW else "Artega"


mg = SaisieMoteurs(FAMILLES, "Artega", motoriste)
L = []

mg(L, "GT", "GT", "1", "2009-01", "2012-12", [("3.6 VR6 300", "VR6-3.6", 350)], portes=2, places=2, reservoir=60,
   remarques="Coupé à moteur central arrière, environ 150 exemplaires ; données indicatives")
mg(L, "Karo", "Karo-Isetta", "1", "2020-04", "2022-12", [("Électrique 8 kWh 20", "ARTEGA-KARO-EV", 110, {"batterie": 8}),
                                                          ("Électrique 14.4 kWh 20", "ARTEGA-KARO-EV", 110, {"batterie": 14.4})],
   portes=1, places=2, reservoir=0, remarques="Micro-citadine L7e inspirée de l'Isetta, 15 kW, 90 km/h, jusqu'à 215 km avec la grande batterie ; "
                                              "petite batterie et dates indicatives ; reprise par Electric Brands (Evetta)")

MOT = Motorisations("Artega", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Artega": L}
MOTEURS = MOT.moteurs()
