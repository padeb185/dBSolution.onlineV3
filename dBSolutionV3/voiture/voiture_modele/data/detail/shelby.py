"""Shelby (Shelby American) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Cobra 260 / 289, Daytona Coupe, Cobra 427, GT350, GT500 (Shelby Mustang des années 1960 et Shelby GT350 / GT500 modernes),
Series 1 et Super Snake.
V8 Ford 289 et 5.4 à compresseur repris de ford.py, Coyote 5.0 à compresseur de saleen.py, V8 Aurora 4.0 d'oldsmobile.py
(mêmes codes) ; V8 Ford 260, FE 427 / 428, 302, Windsor 351, 5.8 compresseur, Voodoo 5.2 et Predator 5.2 ajoutés.
Puissances américaines converties en ch (× 1,014) ; jusqu'en 1971 puissances brutes. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .ford import FAMILLES as FAMILLES_FORD
from .oldsmobile import FAMILLES as FAMILLES_OLDS
from .saleen import FAMILLES as FAMILLES_SALEEN

E_ = "ESS"
C = "CHAINE"


def v8(t, l, rpm, nmrpm, q=5.7, a="V"):
    return f(t, E_, l, C, 8, rpm, nmrpm, "10W30", q, 8000, a=a)


FORD_PROPRES = {
    "FORD-V8-4.3": v8("ATM", 4.3, 5800, 4500, 4.7), "FORD-FE-7.0": v8("ATM", 7.0, 6000, 3700, 6.0), "FORD-FE-7.0-428": v8("ATM", 7.0, 5400, 3200, 6.0),
    "FORD-V8-5.0": v8("ATM", 5.0, 6000, 4200, 4.7), "WINDSOR-5.8": FAMILLES_SALEEN["WINDSOR-5.8"],
    "TRINITY-5.8S": v8("TURBO", 5.8, 6500, 4000, 7.6), "VOODOO-5.2": v8("ATM", 5.2, 7500, 4750, 9.5), "PREDATOR-5.2S": v8("TURBO", 5.2, 7300, 5000, 9.5),
}
FORD = {**FORD_PROPRES, **{k: FAMILLES_FORD[k] for k in ("FORD-V8-4.7", "MODULAR-5.4S")}, "COYOTE-5.0-SC": FAMILLES_SALEEN["COYOTE-5.0-SC"]}
OLDS = {"OLDS-AURORA-4.0": FAMILLES_OLDS["OLDS-AURORA-4.0"]}
FAMILLES = {**FORD, **OLDS}


def motoriste(fam):
    return "Oldsmobile" if fam in OLDS else "Ford"


mg = SaisieMoteurs(FAMILLES, "Shelby", motoriste)
L = []
NA = "Marché nord-américain"
IND = NA + " ; données indicatives"

mg(L, "Cobra", "Cobra 260 / 289", "1", "1962-02", "1965-12", [("260 4.3 V8 264", "FORD-V8-4.3", 365, {"fin": "1962-12"}), ("289 4.7 V8 276", "FORD-V8-4.7", 423, {"debut": "1963-01"})],
   portes=2, places=2, reservoir=68, remarques="Roadster sur base AC Ace ; " + IND)
mg(L, "Cobra", "Cobra 427", "1", "1965-01", "1967-12", [("427 7.0 V8 431", "FORD-FE-7.0", 651), ("427 S/C 7.0 V8 492", "FORD-FE-7.0", 651)], portes=2, places=2, reservoir=68,
   remarques="Châssis renforcé (Mk III), version S/C semi-compétition ; " + IND)
mg(L, "Daytona Coupe", "Daytona", "1", "1964-01", "1965-12", [("4.7 V8 390", "FORD-V8-4.7", 450)], portes=2, places=2, reservoir=140,
   remarques="Coupé de compétition, 6 exemplaires ; titre mondial GT 1965 ; " + IND)
mg(L, "GT350", "Shelby Mustang", "1", "1965-01", "1970-12",
   [("4.7 V8 306", "FORD-V8-4.7", 446, {"fin": "1967-12"}), ("5.0 V8 254", "FORD-V8-5.0", 447, {"debut": "1968-01", "fin": "1968-12"}),
    ("5.8 V8 294", "WINDSOR-5.8", 522, {"debut": "1969-01"})], portes=2, places=4, reservoir=60, remarques="Shelby Mustang ; cabriolet à partir de 1968 ; " + IND)
mg(L, "GT500", "Shelby Mustang", "2", "1967-01", "1970-12",
   [("428 7.0 V8 360", "FORD-FE-7.0-428", 569, {"fin": "1967-12"}), ("KR 428 Cobra Jet 7.0 V8 340", "FORD-FE-7.0-428", 597, {"debut": "1968-04"})],
   portes=2, places=4, reservoir=60, remarques="Shelby Mustang ; GT500KR « King of the Road » ; " + IND)
mg(L, "Series 1", "Series 1", "1", "1999-01", "2005-12", [("4.0 V8 325", "OLDS-AURORA-4.0", 393), ("4.0 V8 Compresseur 456", "OLDS-AURORA-4.0", 529, {"remarques": "Kit compresseur Shelby"})],
   portes=2, places=2, reservoir=68, remarques="Roadster conçu par Shelby, environ 250 ex. ; " + IND)
mg(L, "GT500", "S197", "1", "2007-01", "2014-12",
   [("5.4 V8 Compresseur 507", "MODULAR-5.4S", 650, {"fin": "2010-12"}), ("5.4 V8 Compresseur 558", "MODULAR-5.4S", 678, {"debut": "2011-01", "fin": "2012-12"}),
    ("5.8 V8 Compresseur 671", "TRINITY-5.8S", 856, {"debut": "2013-01"})], portes=2, places=4, reservoir=61, remarques="Ford Shelby GT500, coupé et cabriolet ; " + IND)
mg(L, "GT350", "S550", "1", "2015-09", "2020-12", [("5.2 V8 533", "VOODOO-5.2", 582), ("R 5.2 V8 533", "VOODOO-5.2", 582)], portes=2, places=4, reservoir=61,
   remarques="Ford Shelby GT350 et GT350R, V8 vilebrequin plat ; " + IND)
mg(L, "GT500", "S550", "2", "2019-09", "2022-12", [("5.2 V8 Compresseur 771", "PREDATOR-5.2S", 847)], portes=2, places=4, reservoir=61, remarques="Ford Shelby GT500 ; " + IND)
mg(L, "Super Snake", "S197", "1", "2008-01", "2014-12", [("5.4 V8 Compresseur 735", "MODULAR-5.4S", 881, {"fin": "2012-12"}), ("5.8 V8 Compresseur 862", "TRINITY-5.8S", 1047, {"debut": "2013-01"})],
   portes=2, places=4, reservoir=61, remarques="Préparation Shelby American sur base GT500 ; " + IND)
mg(L, "Super Snake", "S550 / S650", "1", "2017-01", None, [("5.0 V8 Compresseur 812", "COYOTE-5.0-SC", 942, {"fin": "2023-12"}), ("5.0 V8 Compresseur 842", "COYOTE-5.0-SC", 990, {"debut": "2024-01"})],
   portes=2, places=4, reservoir=61, remarques="Préparation Shelby American sur base Mustang GT ; " + IND)

MOT = Motorisations("Shelby", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Shelby": L}
MOTEURS = MOT.moteurs()
