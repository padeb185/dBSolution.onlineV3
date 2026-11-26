"""TVR : générations, phases, motorisations (marché européen) et moteurs liés.
Grantura, Griffith 200 / 400, Tuscan V8 / V6, Vixen, série M (1600M, 2500M, 3000M, Turbo), Tasmin / 350i, série S, Griffith,
Chimaera, Cerbera, Tuscan (1999), Tamora, T350 et Sagaris. Production arrêtée en 2006-2007.
Moteurs BMC de mg.py, Coventry Climax de morgan.py, Ford Kent de caterham.py, V8 289 de ford.py, Triumph 2.5 de triumph.py, V8 Rover
de land_rover.py / ginetta.py (mêmes codes) ; V6 Ford Essex et Cologne, V8 Rover préparés TVR, AJP8 et Speed Six ajoutés.
Le nouveau Griffith (V8 Cosworth), annoncé en 2017, n'est pas entré en production : il n'est pas repris. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .caterham import FAMILLES as FAMILLES_CATERHAM
from .ford import FAMILLES as FAMILLES_FORD
from .ginetta import FAMILLES as FAMILLES_GINETTA
from .land_rover import FAMILLES as FAMILLES_LR
from .mg import FAMILLES as FAMILLES_MG
from .morgan import FAMILLES as FAMILLES_MORGAN
from .triumph import FAMILLES as FAMILLES_TRIUMPH

E_ = "ESS"
C, B = "CHAINE", "COURROIE"


def v(l, n, rpm, nmrpm, t="ATM", d=C, q=5.5, a="V"):
    return f(t, E_, l, d, n, rpm, nmrpm, "10W40", q, 10000, a=a)


FORD_PROPRES = {"FORD-ESSEX-3.0": v(3.0, 6, 5000, 3000), "FORD-ESSEX-3.0T": v(3.0, 6, 5500, 3500, t="TURBO"),
                "FORD-COLOGNE-2.8": v(2.8, 6, 5700, 4300), "FORD-COLOGNE-2.9": v(2.9, 6, 5500, 3000)}
TVR = {"TVR-V8-4.3": v(4.3, 8, 6000, 4000), "TVR-V8-4.5": v(4.5, 8, 5500, 4000), "TVR-V8-5.0": v(5.0, 8, 5500, 4000),
       "AJP8-4.2": v(4.2, 8, 6500, 4500, q=9.0), "AJP8-4.5": v(4.5, 8, 6750, 5500, q=9.0),
       "SPEED6-3.6": v(3.6, 6, 7200, 5250, q=9.0, a="EN_LIGNE"), "SPEED6-4.0": v(4.0, 6, 7000, 5500, q=9.0, a="EN_LIGNE")}
REPRIS = {**{k: FAMILLES_MG[k] for k in ("BMC-B-1.6", "BMC-B-1.8")}, "CLIMAX-1.1": FAMILLES_MORGAN["CLIMAX-1.1"], "KENT-1.6": FAMILLES_CATERHAM["KENT-1.6"],
          "FORD-V8-4.7": FAMILLES_FORD["FORD-V8-4.7"], "TRIUMPH-L6-2.5": FAMILLES_TRIUMPH["TRIUMPH-L6-2.5"],
          "ROVER-V8-3.5": FAMILLES_LR["ROVER-V8-3.5"], "ROVER-V8-4.0": FAMILLES_LR["ROVER-V8-4.0"], "ROVER-V8-3.9": FAMILLES_GINETTA["ROVER-V8-3.9"]}
FAMILLES = {**FORD_PROPRES, **TVR, **REPRIS}
MOTORISTES = {"BMC-B-1.6": "BMC", "BMC-B-1.8": "BMC", "CLIMAX-1.1": "Coventry Climax", "TRIUMPH-L6-2.5": "Triumph",
              "ROVER-V8-3.5": "Rover", "ROVER-V8-4.0": "Rover", "ROVER-V8-3.9": "Rover"}


def motoriste(fam):
    if fam in TVR:
        return "TVR"
    return MOTORISTES.get(fam, "Ford")


mg = SaisieMoteurs(FAMILLES, "TVR", motoriste)
L = []
IND = "données indicatives"

mg(L, "Grantura", "Grantura", "1", "1958-01", "1967-12",
   [("1.1 84", "CLIMAX-1.1", 105, {"fin": "1960-12"}), ("1.6 81", "BMC-B-1.6", 118, {"debut": "1960-01", "fin": "1962-12"}), ("1.8 96", "BMC-B-1.8", 149, {"debut": "1962-09"})],
   portes=2, places=2, reservoir=45, remarques="Mk I à Mk IV, moteurs Climax, MG et Ford ; " + IND)
mg(L, "Griffith", "Griffith 200 / 400", "1", "1963-01", "1967-12", [("4.7 V8 275", "FORD-V8-4.7", 423)], portes=2, places=2, reservoir=55, remarques="V8 Ford 289 ; " + IND)
mg(L, "Tuscan", "Tuscan (1967)", "1", "1967-01", "1971-12", [("V8 4.7 V8 275", "FORD-V8-4.7", 423), ("V6 3.0 V6 130", "FORD-ESSEX-3.0", 236, {"debut": "1969-01"})],
   portes=2, places=2, reservoir=55, remarques=IND)
mg(L, "Vixen", "Vixen", "1", "1967-01", "1973-12", [("1.6 88", "KENT-1.6", 130)], portes=2, places=2, reservoir=45, remarques="S1 à S4 ; " + IND)
mg(L, "M", "M", "1", "1972-01", "1979-12",
   [("1600M 1.6 88", "KENT-1.6", 130), ("2500M 2.5 L6 107", "TRIUMPH-L6-2.5", 189), ("3000M 3.0 V6 140", "FORD-ESSEX-3.0", 236),
    ("Turbo 3.0 V6 Turbo 233", "FORD-ESSEX-3.0T", 373, {"debut": "1975-01"})], portes=2, places=2, reservoir=55,
   remarques="Série M : coupé, Taimar (hayon) et cabriolet ; " + IND)
mg(L, "Tasmin", "Tasmin", "1", "1980-01", "1991-12",
   [("280i 2.8 V6 162", "FORD-COLOGNE-2.8", 220), ("350i 3.5 V8 193", "ROVER-V8-3.5", 298, {"debut": "1983-01"}), ("390SE 3.9 V8 279", "ROVER-V8-3.9", 366, {"debut": "1985-01"})],
   portes=2, places=2, reservoir=64, remarques="Tasmin, 280i, 350i, 390SE / 400SE / 450SE ; " + IND)
mg(L, "S", "S", "1", "1986-10", "1994-12", [("2.8 V6 162", "FORD-COLOGNE-2.8", 220, {"fin": "1988-12"}), ("2.9 V6 172", "FORD-COLOGNE-2.9", 233, {"debut": "1989-01"})],
   portes=2, places=2, reservoir=55, remarques="S, S2, S3, S4C ; " + IND)
mg(L, "Griffith", "Griffith (1991)", "1", "1991-01", "2002-12",
   [("4.0 V8 243", "ROVER-V8-4.0", 373), ("4.3 V8 284", "TVR-V8-4.3", 414, {"fin": "1993-12"}), ("500 5.0 V8 345", "TVR-V8-5.0", 475, {"debut": "1993-06"})],
   portes=2, places=2, reservoir=57, remarques="Roadster ; " + IND)
mg(L, "Chimaera", "Chimaera", "1", "1992-01", "2003-12",
   [("4.0 V8 243", "ROVER-V8-4.0", 373), ("4.5 V8 289", "TVR-V8-4.5", 427, {"debut": "1996-01"}), ("500 5.0 V8 345", "TVR-V8-5.0", 475, {"debut": "1994-01"})],
   portes=2, places=2, reservoir=57, remarques="Roadster ; " + IND)
mg(L, "Cerbera", "Cerbera", "1", "1996-01", "2006-12",
   [("4.2 V8 365", "AJP8-4.2", 434), ("4.5 V8 426", "AJP8-4.5", 515, {"debut": "1997-01"}), ("Speed Six 4.0 355", "SPEED6-4.0", 434, {"debut": "1997-09"})],
   portes=2, places=4, reservoir=65, remarques="Coupé 2+2 ; " + IND)
mg(L, "Tuscan", "Tuscan (1999)", "1", "1999-01", "2006-12",
   [("Speed Six 3.6 355", "SPEED6-3.6", 393), ("Speed Six 4.0 365", "SPEED6-4.0", 420), ("S 4.0 406", "SPEED6-4.0", 474, {"debut": "2001-01"})],
   portes=2, places=2, reservoir=60, remarques="Coupé targa ; Tuscan 2 (2005) ; " + IND)
mg(L, "Tamora", "Tamora", "1", "2002-01", "2006-12", [("Speed Six 3.6 355", "SPEED6-3.6", 393)], portes=2, places=2, reservoir=60, remarques="Roadster ; " + IND)
mg(L, "T350", "T350", "1", "2003-01", "2006-12", [("Speed Six 3.6 355", "SPEED6-3.6", 393)], portes=2, places=2, reservoir=60, remarques="T350C (coupé) et T350T (targa) ; " + IND)
mg(L, "Sagaris", "Sagaris", "1", "2005-01", "2006-12", [("Speed Six 4.0 412", "SPEED6-4.0", 475)], portes=2, places=2, reservoir=60, remarques="Coupé ; " + IND)

MOT = Motorisations("TVR", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"TVR": L}
MOTEURS = MOT.moteurs()
