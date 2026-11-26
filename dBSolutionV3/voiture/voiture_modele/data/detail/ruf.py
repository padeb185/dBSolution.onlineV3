"""RUF Automobile : générations, phases, motorisations (marché européen) et moteurs liés.
BTR, CTR Yellowbird, CTR2, Turbo R, RGT, Rt 12, CTR3, RGT-8, CTR Anniversary et SCR.
Constructeur à part entière (numéros de châssis RUF) sur base Porsche 911 ou en conception propre (CTR3, CTR Anniversary, SCR 2018).
Moteurs Porsche Mezger repris de porsche.py (mêmes codes, préparés RUF) ; moteurs RUF ajoutés. Petites séries, données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .porsche import FAMILLES as FAMILLES_PORSCHE

E_ = "ESS"
C, P = "CHAINE", "PLAT"

RUF = {
    "RUF-3.4T": f("TURBO", E_, 3.4, C, 6, 6000, 4800, "20W50", 13.0, 10000, a=P),
    "RUF-3.4TT": f("TURBO", E_, 3.4, C, 6, 5950, 5100, "20W50", 13.0, 10000, a=P),
    "RUF-3.6TT": f("TURBO", E_, 3.6, C, 6, 5800, 4800, "15W50", 11.5, 10000, a=P),
    "RUF-3.8TT": f("TURBO", E_, 3.8, C, 6, 7000, 4000, "0W40", 10.5, 10000, a=P),
    "RUF-V8-4.5": f("ATM", E_, 4.5, C, 8, 8500, 5250, "0W40", 10.0, 10000, a="V"),
    "RUF-4.0": f("ATM", E_, 4.0, C, 6, 8270, 6000, "0W40", 10.5, 10000, a=P),
}
PORSCHE = {k: FAMILLES_PORSCHE[k] for k in ("Mezger-3.6", "Mezger-3.6T")}
FAMILLES = {**RUF, **PORSCHE}


def motoriste(fam):
    return "Porsche" if fam in PORSCHE else "RUF"


mg = SaisieMoteurs(FAMILLES, "RUF", motoriste)
L = []
IND = "données indicatives"

mg(L, "BTR", "930", "1", "1983-01", "1989-12", [("3.4 Turbo 379", "RUF-3.4T", 480)], portes=2, places=4, reservoir=85,
   remarques="Base Porsche 911 (G), boîte 5 rapports RUF ; " + IND)
mg(L, "CTR", "CTR Yellowbird", "1", "1987-01", "1989-12", [("Yellowbird 3.4 Biturbo 476", "RUF-3.4TT", 553)], portes=2, places=2, reservoir=85,
   remarques="« Yellowbird », 29 exemplaires (plus des conversions) ; " + IND)
mg(L, "CTR2", "993", "1", "1995-01", "1997-12", [("3.6 Biturbo 527", "RUF-3.6TT", 685)], portes=2, places=2, reservoir=74,
   remarques="Base Porsche 993, propulsion puis 4x4 ; " + IND)
mg(L, "Turbo R", "993", "2", "1998-01", "2000-12", [("3.6 Biturbo 497", "RUF-3.6TT", 650)], portes=2, places=2, reservoir=74, remarques="Base Porsche 993 Turbo ; " + IND)
mg(L, "RGT", "996", "1", "2000-01", "2008-12", [("3.6 390", "Mezger-3.6", 375)], portes=2, places=2, reservoir=89,
   remarques="Base Porsche 996 / 997, moteur atmosphérique Mezger préparé ; " + IND)
mg(L, "Rt 12", "997", "1", "2004-01", "2012-12", [("3.6 Biturbo 659", "Mezger-3.6T", 880)], portes=2, places=2, reservoir=67, remarques="Base Porsche 997 ; " + IND)
mg(L, "CTR3", "CTR3", "1", "2007-09", "2012-12", [("3.8 Biturbo 710", "RUF-3.8TT", 890), ("Clubsport 3.8 Biturbo 788", "RUF-3.8TT", 980, {"debut": "2012-03"})],
   portes=2, places=2, reservoir=90, remarques="Conception propre à moteur central arrière ; " + IND)
mg(L, "RGT-8", "997", "2", "2010-03", "2013-12", [("4.5 V8 558", "RUF-V8-4.5", 500)], portes=2, places=2, reservoir=67,
   remarques="Base Porsche 997, premier V8 de conception RUF ; " + IND)
mg(L, "CTR", "CTR Anniversary", "1", "2017-03", "2022-12", [("Anniversary 3.6 Biturbo 720", "RUF-3.6TT", 880)], portes=2, places=2, reservoir=90,
   remarques="Châssis carbone propre (monocoque RUF), 30 exemplaires ; " + IND)
mg(L, "SCR", "SCR", "1", "2018-03", None, [("4.0 517", "RUF-4.0", 470)], portes=2, places=2, reservoir=90,
   remarques="Monocoque carbone RUF, flat-six atmosphérique ; " + IND)

MOT = Motorisations("RUF", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Ruf": L}
MOTEURS = MOT.moteurs()
