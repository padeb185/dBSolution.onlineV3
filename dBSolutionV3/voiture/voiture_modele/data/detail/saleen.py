"""Saleen : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Saleen Mustang (Fox), S351, S281, S302 et 302 (préparations Ford Mustang), S7 (dont Twin Turbo) et S1.
V8 Ford 4.6 repris de lincoln.py et Coyote 5.0 de ford.py (mêmes codes) ; V8 5.0 HO, Windsor 5.8, versions à compresseur, V8 Saleen
7.0 et 2.3 turbo du S1 ajoutés. Puissances américaines converties en ch (× 1,014). Petites séries, données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .ford import FAMILLES as FAMILLES_FORD
from .lincoln import FAMILLES as FAMILLES_LINCOLN

E_ = "ESS"
C = "CHAINE"


def v8(t, l, rpm, nmrpm, q=5.7):
    return f(t, E_, l, C, 8, rpm, nmrpm, "5W30", q, 8000, a="V")


FORD_PROPRES = {
    "FORD-HO-5.0": v8("ATM", 5.0, 4200, 3200, 4.7), "WINDSOR-5.8": v8("ATM", 5.8, 5500, 4000, 4.7),
    "MODULAR-4.6-3V": v8("ATM", 4.6, 6000, 4250), "MODULAR-4.6-SC": v8("TURBO", 4.6, 6000, 4000), "COYOTE-5.0-SC": v8("TURBO", 5.0, 6500, 4500, 9.0),
}
SALEEN = {"SALEEN-V8-7.0": v8("ATM", 7.0, 6400, 4000, 8.0), "SALEEN-V8-7.0TT": v8("TURBO", 7.0, 6300, 4800, 8.0),
          "SALEEN-2.3T": f("TURBO", E_, 2.3, C, 4, 6800, 4000, "5W30", 5.7, 8000)}
FORD = {**FORD_PROPRES, "MODULAR-4.6": FAMILLES_LINCOLN["MODULAR-4.6"], "COYOTE-5.0": FAMILLES_FORD["COYOTE-5.0"]}
FAMILLES = {**FORD, **SALEEN}


def motoriste(fam):
    return "Saleen" if fam in SALEEN else "Ford"


mg = SaisieMoteurs(FAMILLES, "Saleen", motoriste)
L = []
NA = "Marché nord-américain"
IND = NA + " ; données indicatives"

mg(L, "Mustang", "Fox", "1", "1984-01", "1993-12", [("5.0 V8 228", "FORD-HO-5.0", 407), ("SSC 5.0 V8 296", "FORD-HO-5.0", 441, {"debut": "1989-01", "fin": "1989-12"})],
   portes=2, places=4, reservoir=58, remarques="Saleen Mustang (Fox) ; SSC 1989 (161 ex.) ; " + IND)
mg(L, "S351", "SN95", "1", "1994-01", "1999-12", [("5.8 V8 376", "WINDSOR-5.8", 536)], portes=2, places=4, reservoir=60, remarques="Base Mustang SN95 ; " + IND)
mg(L, "S281", "SN95", "2", "1996-01", "2004-12", [("4.6 V8 289", "MODULAR-4.6", 430), ("SC 4.6 V8 Compresseur 431", "MODULAR-4.6-SC", 542, {"debut": "2001-01"})],
   portes=2, places=4, reservoir=60, remarques="Coupé et cabriolet ; " + IND)
mg(L, "S281", "S197", "1", "2005-01", "2009-12",
   [("4.6 V8 330", "MODULAR-4.6-3V", 441), ("SC 4.6 V8 Compresseur 472", "MODULAR-4.6-SC", 576), ("Extreme 4.6 V8 Compresseur 558", "MODULAR-4.6-SC", 678, {"debut": "2008-01"})],
   portes=2, places=4, reservoir=61, remarques="Coupé et cabriolet ; " + IND)
mg(L, "S302", "S197", "2", "2010-01", "2014-12", [("Yellow Label 5.0 V8 441", "COYOTE-5.0", 520, {"debut": "2011-01"}), ("Black Label 5.0 V8 Compresseur 629", "COYOTE-5.0-SC", 780, {"debut": "2011-01"}),
                                                   ("4.6 V8 Compresseur 472", "MODULAR-4.6-SC", 576, {"fin": "2010-12"})],
   portes=2, places=4, reservoir=61, remarques="Coupé et cabriolet ; " + IND)
mg(L, "302", "S550", "1", "2015-01", "2019-12", [("White Label 5.0 V8 462", "COYOTE-5.0", 556), ("Black Label 5.0 V8 Compresseur 740", "COYOTE-5.0-SC", 813)],
   portes=2, places=4, reservoir=61, remarques="Base Mustang S550 ; " + IND)
mg(L, "S7", "S7", "1", "2000-08", "2004-12", [("7.0 V8 558", "SALEEN-V8-7.0", 712)], portes=2, places=2, reservoir=72,
   remarques="Supercar à moteur central, châssis tubulaire ; " + IND)
mg(L, "S7", "S7 Twin Turbo", "1", "2005-01", "2009-12", [("Twin Turbo 7.0 V8 Biturbo 771", "SALEEN-V8-7.0TT", 949)], portes=2, places=2, reservoir=72,
   remarques="Dont Competition Package (2006) et S7 LM (2017) ; " + IND)
mg(L, "S1", "S1", "1", "2019-01", "2021-12", [("2.3 Turbo 456", "SALEEN-2.3T", 563)], portes=2, places=2, reservoir=55, remarques="Coupé à moteur central ; " + IND)

MOT = Motorisations("Saleen", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Saleen": L}
MOTEURS = MOT.moteurs()
