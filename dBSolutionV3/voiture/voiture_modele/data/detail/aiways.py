"""Aiways : générations, motorisations (marché européen) et moteurs liés.
U5 (SUV) et U6 (SUV coupé), électriques sur la même plateforme. Le concept U7 ion n'a pas été produit.
La commercialisation en Europe s'est arrêtée (date de fin indicative).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique

FAMILLES = {"AIWAYS-EV": electrique()}


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Aiways")
L = []

mg(L, "U5", "MAS", "1", "2020-08", "2021-08", [("Standard 204", "AIWAYS-EV", 310, el(63)), ("Premium 204", "AIWAYS-EV", 310, el(63))], reservoir=0,
   remarques="SUV électrique, traction ; vente directe en Europe")
mg(L, "U5", "MAS", "2", "2021-09", "2025-12", [("Standard 204", "AIWAYS-EV", 310, el(63)), ("Premium 204", "AIWAYS-EV", 310, el(63))], reservoir=0,
   remarques="Restylage (équipements) ; fin de commercialisation indicative")
mg(L, "U6", "MAS", "C", "2022-12", "2025-12", [("U6 218", "AIWAYS-EV", 315, el(63))], reservoir=0,
   remarques="SUV coupé électrique (base U5) ; fin de commercialisation indicative")

MOT = Motorisations("Aiways", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Aiways": L}
MOTEURS = MOT.moteurs()
