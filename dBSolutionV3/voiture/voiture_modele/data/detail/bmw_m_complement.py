"""BMW M (compléments) : générations, phases, motorisations (marché européen) et moteurs liés.
Modèles BMW M absents de bmw.py : M635CSi (E24), M Roadster et M Coupé (Z3, E36/7 et E36/8), Z4 M Roadster et Coupé (E85 / E86)
et M3 CS Touring (G81). Moteurs repris de la table de bmw.py (mêmes familles, codes, couples et motoriste « BMW M »).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from . import bmw

AUTRES = {v[1]: v[0] for v in bmw.TABLE.values() if len(v) == 4}
mg = SaisieMoteurs(bmw.FAMILLES, bmw.M, lambda fam: AUTRES.get(fam, bmw.B))
L = []


def t(cle, nom=None, *surcharges):
    """Variante reprise de la table de bmw.py (même famille et couple) ; nom affiché facultatif."""
    v = bmw.TABLE[cle]
    return (nom or cle, v[-3], v[-1], *surcharges)


mg(L, "M635CSi", "E24", "1", "1984-02", "1989-04", [t("M635CSi 286")], portes=2, places=4, reservoir=70,
   remarques="Coupé Série 6 à six cylindres M88 de la M1 (M6 en Amérique du Nord)")
mg(L, "M Roadster", "E36/7", "1", "1997-03", "2000-12", [t("M Roadster 321")], portes=2, places=2, reservoir=51, remarques="Z3 M Roadster, S50 3.2")
mg(L, "M Roadster", "E36/7", "2", "2001-01", "2002-06", [t("M Roadster 325")], portes=2, places=2, reservoir=51, remarques="Z3 M Roadster, S54 3.2")
mg(L, "M Coupé", "E36/8", "1", "1998-03", "2000-12", [t("M Roadster 321", "M Coupé 321")], portes=3, places=2, reservoir=51,
   remarques="Z3 M Coupé « break de chasse », S50 3.2")
mg(L, "M Coupé", "E36/8", "2", "2001-01", "2002-06", [t("M Roadster 325", "M Coupé 325")], portes=3, places=2, reservoir=51, remarques="Z3 M Coupé, S54 3.2")
mg(L, "Z4 M", "E85 / E86", "1", "2006-04", "2008-12", [t("M3 343", "Z4 M 343")], portes=2, places=2, reservoir=55,
   remarques="Z4 M Roadster (E85) et Z4 M Coupé (E86), six cylindres S54 de la M3 E46")
mg(L, "M3 CS Touring", "G81", "1", "2025-03", None, [t("M3 CS 550", "M3 CS Touring 550")], portes=5, places=5, reservoir=59,
   remarques="Break M3 CS, transmission intégrale M xDrive ; série limitée")

MOT = Motorisations(bmw.M, bmw.FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"BMW M": L}
MOTEURS = MOT.moteurs()
