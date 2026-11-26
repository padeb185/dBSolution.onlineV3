"""Avanti : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Avanti II (Avanti Motor Corporation, South Bend, 1965-1991) et Avanti Convertible (1985-1991), suite de la Studebaker Avanti
(voir studebaker.py). V8 Chevrolet small-block repris de chevrolet.py (mêmes familles et couples) ; 5.0 et 6.6 ajoutés.
Puissances SAE converties en ch (× 1,014) ; jusqu'en 1971 puissances brutes. Données indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET


def v8(l, rpm, nmrpm):
    return f("ATM", "ESS", l, "CHAINE", 8, rpm, nmrpm, "10W30", 4.7, 5000, a="V")


FAMILLES = {**{k: FAMILLES_CHEVROLET[k] for k in ("SBC-5.4", "SBC-5.7")}, "SBC-5.0": v8(5.0, 4200, 2400), "SBC-6.6": v8(6.6, 3800, 2400)}
mg = SaisieMoteurs(FAMILLES, "Chevrolet", lambda fam: "Chevrolet")
L = []
IND = "marché nord-américain ; données indicatives, à vérifier"

mg(L, "Avanti II", "Avanti II", "1", "1965-01", "1982-12",
   [("5.4 V8 304", "SBC-5.4", 488, {"fin": "1969-12"}), ("5.7 V8 304", "SBC-5.7", 515, {"debut": "1970-01", "fin": "1972-12"}),
    ("6.6 V8 183", "SBC-6.6", 400, {"debut": "1973-01", "fin": "1976-12"}), ("5.7 V8 183", "SBC-5.7", 366, {"debut": "1977-01", "fin": "1980-12"}),
    ("5.0 V8 157", "SBC-5.0", 325, {"debut": "1981-01"})], portes=2, places=4, reservoir=79,
   remarques="Coupé en polyester construit par Avanti Motor Corporation (Newman & Altman) ; " + IND)
mg(L, "Avanti II", "Avanti II", "2", "1983-01", "1991-12", [("5.0 V8 172", "SBC-5.0", 345)], portes=2, places=4, reservoir=79,
   remarques="Périodes Blake (1983-1985) puis Kelly (1987-1991), dont coupé allongé et berline 4 portes (1989) ; pas de production en 1986 ; " + IND)
mg(L, "Avanti Convertible", "Convertible", "1", "1985-01", "1991-12", [("5.0 V8 172", "SBC-5.0", 345)], portes=2, places=4, reservoir=79,
   remarques="Cabriolet ; " + IND)

MOT = Motorisations("Avanti", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Avanti": L}
MOTEURS = MOT.moteurs()
