"""Checker : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Checker Motors (Kalamazoo) : taxis Model A (1922-1927), A8 (1956-1958), Marathon (1961-1982) et limousine Aerobus (1962-1977).
Six cylindres Buda et Continental, puis six cylindres et V8 Chevrolet (familles reprises de studebaker.py, chevrolet.py, avanti.py et
auburn.py). Puissances SAE converties en ch (× 1,014) ; jusqu'en 1971 puissances brutes. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .auburn import FAMILLES as FAMILLES_AUBURN
from .avanti import FAMILLES as FAMILLES_AVANTI
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET
from .studebaker import FAMILLES as FAMILLES_STUDEBAKER

BUDA = {"BUDA-L4-3.7": f("ATM", "ESS", 3.7, "NC", 4, 2000, 1000, "SAE30", 5.0, 2000)}
CONTINENTAL = {"CONTINENTAL-L6-3.7": FAMILLES_AUBURN["CONTINENTAL-L6-3.7"]}
CHEVROLET = {
    "CHEVY-I6-3.8": FAMILLES_STUDEBAKER["CHEVY-I6-3.8"],
    "CHEVY-I6-4.1": FAMILLES_CHEVROLET["CHEVY-I6-4.1"],
    "SBC-4.6": FAMILLES_CHEVROLET["SBC-4.6"],
    "SBC-5.4": FAMILLES_CHEVROLET["SBC-5.4"],
    "SBC-5.7": FAMILLES_CHEVROLET["SBC-5.7"],
    "SBC-5.0": FAMILLES_AVANTI["SBC-5.0"],
}
FAMILLES = {**BUDA, **CONTINENTAL, **CHEVROLET}


def motoriste(fam):
    if fam in BUDA:
        return "Buda"
    if fam in CONTINENTAL:
        return "Continental"
    return "Chevrolet"


mg = SaisieMoteurs(FAMILLES, "Checker", motoriste)
L = []
NA = "marché nord-américain ; données indicatives"
V8_CHEVROLET = [("5.4 V8 254", "SBC-5.4", 441, {"debut": "1965-01", "fin": "1968-12"}), ("5.7 V8 253", "SBC-5.7", 468, {"debut": "1969-01", "fin": "1971-12"}),
                ("5.7 V8 147", "SBC-5.7", 339, {"debut": "1972-01", "fin": "1979-12"})]

mg(L, "Model A", "A", "1", "1922-01", "1927-12", [("3.7 22", "BUDA-L4-3.7", 160)], portes=4, places=7, reservoir=60, remarques="Taxi, quatre cylindres Buda ; " + NA)
mg(L, "Model A8", "A8", "1", "1956-01", "1958-12", [("3.7 L6 81", "CONTINENTAL-L6-3.7", 258)], portes=4, places=8, reservoir=68,
   remarques="Taxi, six cylindres Continental à soupapes latérales ; " + NA)
mg(L, "Marathon", "A11 / A12", "1", "1961-01", "1982-12",
   [("3.7 L6 81", "CONTINENTAL-L6-3.7", 258, {"fin": "1964-12"}), ("3.8 L6 142", "CHEVY-I6-3.8", 298, {"debut": "1965-01", "fin": "1967-12"}),
    ("4.6 V8 198", "SBC-4.6", 386, {"debut": "1965-01", "fin": "1967-12"}), *V8_CHEVROLET,
    ("4.1 I6 157", "CHEVY-I6-4.1", 319, {"debut": "1968-01", "fin": "1979-12"}), ("5.0 V8 157", "SBC-5.0", 325, {"debut": "1980-01"})],
   portes=4, places=8, reservoir=87, remarques="Taxi (A11) et berline civile Marathon (A12), break ; strapontins ; " + NA)
mg(L, "Aerobus", "Aerobus", "1", "1962-01", "1977-12", [("5.4 V8 254", "SBC-5.4", 441, {"fin": "1968-12"}), ("5.7 V8 253", "SBC-5.7", 468, {"debut": "1969-01", "fin": "1971-12"}),
                                                       ("5.7 V8 147", "SBC-5.7", 339, {"debut": "1972-01"})],
   portes=5, places=12, reservoir=87, remarques="Limousine allongée 6 ou 8 portes (navettes d'hôtels et d'aéroports) ; " + NA)

MOT = Motorisations("Checker", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Checker": L}
MOTEURS = MOT.moteurs()
