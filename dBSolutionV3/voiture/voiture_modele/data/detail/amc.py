"""AMC (American Motors Corporation) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Marlin, Ambassador, Rebel, AMX, Javelin, Hornet, Gremlin, Matador, Pacer, Concord, Spirit et Eagle. Marque absorbée par Chrysler
en 1987-1988 (Jeep et Eagle reprises par Chrysler).
Moteurs AMC 2.5 / 4.2 / V8 304 / 327 / 360 repris de jeep.py, GM Iron Duke 2.5 d'oldsmobile.py, Audi 2.0 de porsche.py
(mêmes familles) ; six cylindres 199 / 232 et V8 287 / 290 / 343 / 390 / 401 ajoutés.
Puissances SAE converties en ch (× 1,014) ; jusqu'en 1971 puissances brutes (SAE gross). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .jeep import FAMILLES as FAMILLES_JEEP
from .oldsmobile import FAMILLES as FAMILLES_OLDS
from .porsche import FAMILLES as FAMILLES_PORSCHE

E_ = "ESS"
C = "CHAINE"


def v8(l, rpm, nmrpm):
    return f("ATM", E_, l, C, 8, rpm, nmrpm, "10W30", 4.7, 5000, a="V")


AMC = {
    "AMC-3.3": f("ATM", E_, 3.3, C, 6, 4400, 1600, "10W30", 5.7, 5000),
    "AMC-3.8": f("ATM", E_, 3.8, C, 6, 4300, 1600, "10W30", 5.7, 5000),
    "AMC-4.7V8": v8(4.7, 4700, 2600), "AMC-4.8V8": v8(4.8, 4700, 2600), "AMC-5.6V8": v8(5.6, 4800, 3200), "AMC-6.4V8": v8(6.4, 4600, 3200),
    "AMC-6.6V8": v8(6.6, 4600, 3200),
    **{k: FAMILLES_JEEP[k] for k in ("AMC-2.5", "AMC-4.2", "AMC-5.0V8", "AMC-5.4V8", "AMC-5.9V8")},
}
GM = {"IRON-DUKE-2.5": FAMILLES_OLDS["IRON-DUKE-2.5"]}
AUDI = {"EA831-2.0": FAMILLES_PORSCHE["EA831-2.0"]}
FAMILLES = {**AMC, **GM, **AUDI}


def motoriste(fam):
    if fam in GM:
        return "Pontiac"
    if fam in AUDI:
        return "Audi"
    return "AMC"


mg = SaisieMoteurs(FAMILLES, "AMC", motoriste)
L = []
NA = "Marché nord-américain"
IND = NA + " ; données indicatives"

mg(L, "Marlin", "Marlin", "1", "1965-01", "1967-12", [("3.8 I6 157", "AMC-3.8", 325), ("4.7 V8 201", "AMC-4.7V8", 386), ("5.4 V8 274", "AMC-5.4V8", 488)],
   portes=2, places=6, reservoir=72, remarques="Fastback (Rambler Marlin en 1965-1966) ; " + IND)
mg(L, "Ambassador", "1965", "1", "1965-01", "1970-12",
   [("3.8 I6 157", "AMC-3.8", 325), ("4.8 V8 203", "AMC-4.8V8", 386, {"debut": "1966-01"}), ("5.4 V8 274", "AMC-5.4V8", 488, {"fin": "1966-12"}),
    ("5.6 V8 284", "AMC-5.6V8", 495, {"debut": "1967-01"}), ("6.4 V8 320", "AMC-6.4V8", 576, {"debut": "1968-01"})], portes=4, places=6, reservoir=79,
   remarques="Rambler Ambassador jusqu'en 1965 ; " + IND)
mg(L, "Ambassador", "1971", "1", "1971-01", "1974-12",
   [("5.0 V8 152", "AMC-5.0V8", 332), ("5.9 V8 177", "AMC-5.9V8", 386), ("6.6 V8 259", "AMC-6.6V8", 434)], portes=4, places=6, reservoir=83,
   remarques="Puissances nettes à partir de 1972 ; " + IND)
mg(L, "Rebel", "Rebel", "1", "1967-01", "1970-12",
   [("3.3 I6 130", "AMC-3.3", 251), ("3.8 I6 157", "AMC-3.8", 325), ("4.8 V8 203", "AMC-4.8V8", 386), ("5.6 V8 284", "AMC-5.6V8", 495),
    ("Machine 6.4 V8 345", "AMC-6.4V8", 583, {"debut": "1970-01"})], portes=4, places=6, reservoir=72, remarques="Dont The Machine (1970) ; " + IND)
mg(L, "AMX", "AMX", "1", "1968-02", "1970-12",
   [("4.8 V8 228", "AMC-4.8V8", 407, {"fin": "1969-12"}), ("5.6 V8 284", "AMC-5.6V8", 495, {"fin": "1969-12"}), ("6.4 V8 320", "AMC-6.4V8", 576, {"fin": "1969-12"}),
    ("5.9 V8 294", "AMC-5.9V8", 529, {"debut": "1970-01"}), ("6.4 V8 330", "AMC-6.4V8", 583, {"debut": "1970-01"})], portes=2, places=2, reservoir=72,
   remarques="Coupé biplace ; " + IND)
mg(L, "Javelin", "Javelin", "1", "1968-01", "1970-12",
   [("3.8 I6 147", "AMC-3.8", 325), ("4.8 V8 228", "AMC-4.8V8", 407), ("5.6 V8 284", "AMC-5.6V8", 495), ("6.4 V8 320", "AMC-6.4V8", 576, {"debut": "1969-01"})],
   portes=2, places=4, reservoir=72, remarques="Pony car ; " + IND)
mg(L, "Javelin", "Javelin", "2", "1971-01", "1974-12",
   [("4.2 I6 112", "AMC-4.2", 264), ("5.0 V8 152", "AMC-5.0V8", 332), ("5.9 V8 177", "AMC-5.9V8", 386), ("AMX 6.6 V8 259", "AMC-6.6V8", 434, {"fin": "1974-12"})],
   portes=2, places=4, reservoir=79, remarques="Dont Javelin AMX ; puissances nettes à partir de 1972 ; " + IND)
mg(L, "Hornet", "Hornet", "1", "1970-01", "1977-12",
   [("3.3 I6 130", "AMC-3.3", 251, {"fin": "1971-12"}), ("3.8 I6 101", "AMC-3.8", 251), ("4.2 I6 112", "AMC-4.2", 264, {"debut": "1971-01"}),
    ("5.0 V8 152", "AMC-5.0V8", 332), ("SC/360 5.9 V8 248", "AMC-5.9V8", 495, {"debut": "1971-01", "fin": "1971-12"})], portes=4, places=5, reservoir=60,
   remarques="Berline, coupé, break Sportabout ; " + IND)
mg(L, "Gremlin", "Gremlin", "1", "1970-04", "1978-12",
   [("3.3 I6 130", "AMC-3.3", 251, {"fin": "1971-12"}), ("3.8 I6 101", "AMC-3.8", 251), ("4.2 I6 112", "AMC-4.2", 264, {"debut": "1972-01"}),
    ("5.0 V8 152", "AMC-5.0V8", 332, {"debut": "1972-01", "fin": "1976-12"}), ("2.0 81", "EA831-2.0", 140, {"debut": "1977-01"})], portes=2, places=4, reservoir=48,
   remarques="Compacte à arrière tronqué ; 2.0 d'origine Audi (1977-1978) ; " + IND)
mg(L, "Matador", "Matador", "1", "1971-01", "1978-12",
   [("3.8 I6 101", "AMC-3.8", 251), ("4.2 I6 112", "AMC-4.2", 264), ("5.0 V8 152", "AMC-5.0V8", 332), ("5.9 V8 177", "AMC-5.9V8", 386),
    ("6.6 V8 259", "AMC-6.6V8", 434, {"fin": "1975-12"})], portes=4, places=6, reservoir=79, remarques="Berline, break et coupé (1974) ; " + IND)
mg(L, "Pacer", "Pacer", "1", "1975-03", "1980-12", [("3.8 I6 101", "AMC-3.8", 251), ("4.2 I6 112", "AMC-4.2", 264), ("5.0 V8 127", "AMC-5.0V8", 332, {"debut": "1978-01", "fin": "1979-12"})],
   portes=2, places=4, reservoir=83, remarques="Compacte très vitrée, coupé et break ; " + IND)
mg(L, "Concord", "Concord", "1", "1978-01", "1983-12",
   [("2.0 81", "EA831-2.0", 140, {"fin": "1979-12"}), ("2.5 91", "IRON-DUKE-2.5", 182, {"debut": "1980-01"}), ("4.2 I6 112", "AMC-4.2", 264),
    ("5.0 V8 127", "AMC-5.0V8", 332, {"fin": "1979-12"})], portes=4, places=5, reservoir=83, remarques="Berline, coupé, break ; " + IND)
mg(L, "Spirit", "Spirit", "1", "1979-01", "1983-12",
   [("2.0 81", "EA831-2.0", 140, {"fin": "1979-12"}), ("2.5 91", "IRON-DUKE-2.5", 182, {"debut": "1980-01"}), ("4.2 I6 112", "AMC-4.2", 264),
    ("AMX 5.0 V8 127", "AMC-5.0V8", 332, {"fin": "1980-12"})], portes=2, places=4, reservoir=79, remarques="Liftback et coupé, dont AMX ; " + IND)
mg(L, "Eagle", "Eagle", "1", "1980-01", "1988-12", [("4.2 I6 112", "AMC-4.2", 264), ("2.5 91", "IRON-DUKE-2.5", 182, {"debut": "1981-01", "fin": "1983-12"})],
   portes=5, places=5, reservoir=83, remarques="Berline, coupé et break à transmission intégrale (dont SX/4 et Kammback) ; " + IND)

MOT = Motorisations("AMC", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"AMC": L}
MOTEURS = MOT.moteurs()
