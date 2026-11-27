"""Dangel : générations, phases, motorisations (marché européen) et moteurs liés.
Préparateur alsacien de transmissions 4x4 pour PSA : Peugeot 504 4x4 (pick-up et break), 505 4x4 (break) et Partner 4x4.
Moteurs Peugeot repris de peugeot_classiques.py et peugeot.py (mêmes familles, couples et motoriste). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from . import peugeot, peugeot_classiques

FAMILLES = {**{k: peugeot_classiques.FAMILLES[k] for k in ("XN1", "XD3", "XD3T")},
            **{k: peugeot.FAMILLES[k] for k in ("DW8", "DW10TD", "DV6ATED4", "DV6TED4", "DV6F", "DV5R")}}
mg = SaisieMoteurs(FAMILLES, "Peugeot", lambda fam: "Peugeot")
L = []


def pc(nom, *surcharges):
    fam, _, nm = peugeot_classiques.TABLE[nom]
    return (nom, fam, nm, *surcharges)


def pg(nom, *surcharges):
    fam, _, nm = peugeot.TABLE[nom]
    return (nom, fam, nm, *surcharges)


IND = "transformation 4x4 Dangel ; données indicatives"
mg(L, "Peugeot 504 4x4", "504", "1", "1981-01", "1990-12", [pc("2.0 96"), pc("2.5 D 76")], portes=4, places=5, reservoir=70,
   remarques="Pick-up et break, transmission intégrale permanente ; " + IND)
mg(L, "Peugeot 505 4x4", "505", "1", "1986-01", "1992-12", [pc("2.0 110"), pc("2.5 D 76"), pc("2.5 TD 110")], portes=5, places=7, reservoir=70,
   remarques="Break et familiale ; " + IND)
mg(L, "Partner 4x4", "M59", "1", "1999-01", "2008-03", [pg("1.9 D 70"), pg("2.0 HDi 90")], portes=4, places=5, reservoir=55, remarques="Partner et Partner Combi ; " + IND)
mg(L, "Partner 4x4", "B9", "1", "2008-04", "2018-06", [pg("1.6 HDi 90"), pg("1.6 HDi 110"), pg("1.6 BlueHDi 120", {"debut": "2014-01"})], portes=4, places=5,
   reservoir=60, remarques="Partner Tepee 4x4 ; " + IND)
mg(L, "Partner 4x4", "K9", "1", "2018-06", None, [pg("1.5 BlueHDi 130")], portes=4, places=5, reservoir=50, remarques="Partner et Rifter 4x4 ; " + IND)

MOT = Motorisations("Dangel", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Dangel": L}
MOTEURS = MOT.moteurs()
