"""Trabant (VEB Sachsenring, RDA) : générations, phases, motorisations et moteurs liés.
P50, P60, 601 (berline et Universal) et 1.1. Production arrêtée en 1991.
Bicylindres deux temps Sachsenring ajoutés ; quatre cylindres VW 1.1 (Trabant 1.1) repris de volkswagen.py (même famille).
Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .volkswagen import FAMILLES as FAMILLES_VW

E_ = "ESS"

SACHSENRING = {
    "P50-0.5-2T": f("ATM", E_, 0.5, "NC", 2, 3750, 2800, "SAE30", 2.0, 3000),
    "P60-0.6-2T": f("ATM", E_, 0.6, "NC", 2, 3900, 3000, "SAE30", 2.0, 3000),
}
VW = {"EA111-1.1": FAMILLES_VW["EA111-1.1"]}
FAMILLES = {**SACHSENRING, **VW}


def motoriste(fam):
    return "Volkswagen" if fam in VW else "Sachsenring"


mg = SaisieMoteurs(FAMILLES, "Trabant", motoriste)
L = []
IND = "données indicatives"

mg(L, "P50", "P50", "1", "1957-11", "1962-06", [("0.5 2T 18", "P50-0.5-2T", 44, {"fin": "1959-12"}), ("0.5 2T 20", "P50-0.5-2T", 47, {"debut": "1960-01"})],
   portes=2, places=4, reservoir=24, remarques="Carrosserie en Duroplast ; berline et break ; " + IND)
mg(L, "P60", "P60", "1", "1962-06", "1964-06", [("0.6 2T 23", "P60-0.6-2T", 54)], portes=2, places=4, reservoir=24, remarques=IND)
mg(L, "601", "601", "1", "1964-07", "1990-07", [("0.6 2T 26", "P60-0.6-2T", 54)], portes=2, places=4, reservoir=24,
   remarques="Berline ; environ 2,8 millions d'exemplaires ; " + IND)
mg(L, "601 Universal", "601", "2", "1965-01", "1990-07", [("Universal 0.6 2T 26", "P60-0.6-2T", 54)], portes=3, places=4, reservoir=24, remarques="Break ; " + IND)
mg(L, "1.1", "1.1", "1", "1990-05", "1991-04", [("1.1 40", "EA111-1.1", 74)], portes=2, places=4, reservoir=24,
   remarques="Moteur quatre temps VW (Polo) ; berline et Universal ; " + IND)

MOT = Motorisations("Trabant", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Trabant": L}
MOTEURS = MOT.moteurs()
