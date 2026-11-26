"""Polestar : générations, phases, motorisations (marché européen) et moteurs liés.
Polestar 1 (hybride rechargeable), Polestar 2, Polestar 3, Polestar 4 et Polestar 5.
Moteurs repris de volvo.py (mêmes codes : 2.0 T8 hybride rechargeable, plateformes électriques CMA, SPA2 et SEA) ; plateforme
aluminium du Polestar 5 ajoutée. Polestar 6 (reporté), Polestar 7 (2028), nouveau Polestar 2 (2027) et nouvelle variante break / SUV
du Polestar 4 (fin 2026) non repris faute de données définitives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique
from .volvo import FAMILLES as FAMILLES_VOLVO

VOLVO = {k: FAMILLES_VOLVO[k] for k in ("B4204T-PHEV", "EV-CMA", "EV-SPA2", "EV-SEA")}
PROPRES = {"PPA-EV": electrique()}
FAMILLES = {**VOLVO, **PROPRES}


def motoriste(fam):
    return "Volvo" if fam in VOLVO else "Polestar"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Polestar", motoriste)
L = []

mg(L, "Polestar 1", "Polestar 1", "1", "2019-10", "2021-12", [("T8 2.0 Hybride rechargeable 609", "B4204T-PHEV", 1000, {"batterie": 34})], portes=2, places=4,
   reservoir=60, remarques="Coupé GT hybride rechargeable (puissance système), environ 1 500 ex.")
mg(L, "Polestar 2", "Polestar 2", "1", "2020-07", "2023-12",
   [("Long Range Dual Motor 408", "EV-CMA", 660, el(78)), ("Long Range Single Motor 231", "EV-CMA", 330, el(78, debut="2021-06")),
    ("Standard Range Single Motor 224", "EV-CMA", 330, el(69, debut="2021-06"))], portes=5, places=5, reservoir=0,
   remarques="Fastback électrique ; pack Performance sur la Dual Motor")
mg(L, "Polestar 2", "Polestar 2", "2", "2024-01", None,
   [("Standard Range Single Motor 272", "EV-CMA", 490, el(69)), ("Long Range Single Motor 299", "EV-CMA", 490, el(82)), ("Long Range Dual Motor 421", "EV-CMA", 740, el(82)),
    ("Long Range Dual Motor Performance 476", "EV-CMA", 740, el(82))], portes=5, places=5, reservoir=0,
   remarques="Mise à jour : propulsion sur les Single Motor ; successeur annoncé pour 2027")
mg(L, "Polestar 3", "Polestar 3", "1", "2024-06", None,
   [("Long Range Dual Motor 489", "EV-SPA2", 840, el(111)), ("Long Range Dual Motor Performance 517", "EV-SPA2", 910, el(111)),
    ("Long Range Single Motor 299", "EV-SPA2", 490, el(111, debut="2025-03"))], portes=5, places=5, reservoir=0,
   remarques="SUV électrique (base Volvo EX90) ; mise à jour 800 V annoncée pour 2026")
mg(L, "Polestar 4", "Polestar 4", "1", "2024-04", None,
   [("Long Range Single Motor 272", "EV-SEA", 343, el(100)), ("Long Range Dual Motor 544", "EV-SEA", 686, el(100)), ("Standard Range Single Motor 272", "EV-SEA", 343, el(77, debut="2025-03"))],
   portes=5, places=5, reservoir=0, remarques="SUV coupé électrique sans lunette arrière (plateforme Geely SEA) ; renommé Polestar 4 Coupé avec l'arrivée de la nouvelle variante")
mg(L, "Polestar 5", "Polestar 5", "1", "2026-07", None,
   [("Dual Motor 748", "PPA-EV", 812, el(112)), ("Performance 884", "PPA-EV", 1015, el(112))], portes=4, places=4, reservoir=0,
   remarques="GT quatre portes à plateforme aluminium collée, architecture 800 V ; données indicatives")

MOT = Motorisations("Polestar", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Polestar": L}
MOTEURS = MOT.moteurs()
