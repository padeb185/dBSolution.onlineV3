"""Aixam : générations, phases, motorisations (marché européen) et moteurs liés.
Voitures sans permis (quadricycles légers) : 400 / 500 (années 1990-2000), City, Crossline, Coupé, Crossover, Minauto et e-Aixam
(versions électriques). Bicylindres diesel Kubota (bridés à 45 km/h) et moteurs électriques ajoutés. Données indicatives.
Utilitaires Mega non repris.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

D = "DSL"
B = "COURROIE"

FAMILLES = {
    "KUBOTA-Z402": f("ATM", D, 0.4, B, 2, 3200, 2400, "10W40", 1.8, 5000),
    "KUBOTA-Z482": f("ATM", D, 0.48, B, 2, 3200, 2400, "10W40", 2.0, 5000),
    "AIXAM-EV": electrique(),
}


def motoriste(fam):
    return "Aixam" if fam == "AIXAM-EV" else "Kubota"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Aixam", motoriste)
L = []
VSP = "Voiture sans permis (quadricycle léger, 45 km/h)"

mg(L, "500", "400 / 500", "1", "1996-01", "2005-12", [("400 Diesel 0.4 5", "KUBOTA-Z402", 20), ("500 Diesel 0.5 7", "KUBOTA-Z482", 23, {"debut": "1999-01"})],
   portes=2, places=2, reservoir=16, remarques=VSP + " ; 400, 500, 500.4, 500.5 ; données indicatives")
mg(L, "City", "City", "1", "2008-01", None, [("Diesel 0.5 7", "KUBOTA-Z482", 23), ("e-City 8", "AIXAM-EV", 50, el(8, debut="2015-01"))], portes=2, places=2, reservoir=16,
   remarques=VSP + " ; plusieurs restylages ; e-City électrique")
mg(L, "Crossline", "Crossline", "1", "2008-01", None, [("Diesel 0.5 7", "KUBOTA-Z482", 23)], portes=2, places=2, reservoir=16, remarques=VSP + " ; style SUV")
mg(L, "Coupé", "Coupé", "1", "2014-01", None, [("Diesel 0.5 7", "KUBOTA-Z482", 23), ("e-Coupé 8", "AIXAM-EV", 50, el(8, debut="2016-01"))], portes=2, places=2, reservoir=16,
   remarques=VSP + " ; dont GTI et e-Coupé")
mg(L, "Crossover", "Crossover", "1", "2015-01", None, [("Diesel 0.5 7", "KUBOTA-Z482", 23), ("e-Crossover 8", "AIXAM-EV", 50, el(8, debut="2018-01"))], portes=2, places=2,
   reservoir=16, remarques=VSP + " ; dont GTR")
mg(L, "Minauto", "Minauto", "1", "2016-01", None, [("Diesel 0.5 7", "KUBOTA-Z482", 23), ("e-Minauto 8", "AIXAM-EV", 50, el(8, debut="2022-01"))], portes=2, places=2,
   reservoir=16, remarques=VSP + " ; version d'entrée de gamme")
mg(L, "e-Aixam", "e-Aixam", "1", "2015-01", "2019-12", [("Électrique 8", "AIXAM-EV", 50, el(8))], portes=2, places=2, reservoir=0,
   remarques=VSP + " ; premières versions électriques (ensuite e-City / e-Coupé / e-Crossover)")

MOT = Motorisations("Aixam", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Aixam": L}
MOTEURS = MOT.moteurs()
