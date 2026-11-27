"""Glas : générations, phases, motorisations (marché européen) et moteurs liés.
Hans Glas GmbH (Dingolfing, 1955-1968, reprise par BMW) : Goggomobil T et TS (microvoitures deux-temps), Isar T 600 / T 700, 1004,
1300 GT, 1700 et 2600 / 3000 V8 (« Glaserati »). Premiers moteurs à arbre à cames entraîné par courroie crantée (1004).
Deux-temps : distribution « aucune », huile « à choisir » (mélange). Puissances en ch DIN. Données indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
B = "COURROIE"


def dt(l, rpm, nmrpm):
    return f("ATM", E_, l, "AUCUNE", 2, rpm, nmrpm, "CHOISIR", 0.0, 3000)


FAMILLES = {
    "GLAS-2T-0.25": dt(0.25, 5400, 3500), "GLAS-2T-0.3": dt(0.3, 5000, 3500), "GLAS-2T-0.4": dt(0.4, 5000, 3500),
    "GLAS-ISAR-0.6": f("ATM", E_, 0.58, "NC", 2, 4900, 3500, "20W50", 2.5, 5000, a="PLAT"),
    "GLAS-ISAR-0.7": f("ATM", E_, 0.69, "NC", 2, 5000, 3500, "20W50", 2.5, 5000, a="PLAT"),
    "GLAS-1.0": f("ATM", E_, 1.0, B, 4, 5000, 3000, "20W50", 3.5, 5000),
    "GLAS-1.3": f("ATM", E_, 1.3, B, 4, 5800, 4000, "20W50", 3.5, 5000),
    "GLAS-1.7": f("ATM", E_, 1.7, B, 4, 5300, 3500, "20W50", 4.0, 5000),
    "GLAS-V8-2.6": f("ATM", E_, 2.6, B, 8, 5600, 3600, "20W50", 6.0, 5000, a="V"),
    "GLAS-V8-3.0": f("ATM", E_, 3.0, B, 8, 5100, 3900, "20W50", 6.0, 5000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Glas", lambda fam: "Glas")
L = []
IND = "données indicatives, à vérifier"

mg(L, "Goggomobil T 250", "T", "1", "1955-01", "1969-06", [("250 2T 14", "GLAS-2T-0.25", 19), ("300 2T 15", "GLAS-2T-0.3", 22, {"debut": "1957-01"}),
                                                          ("400 2T 20", "GLAS-2T-0.4", 30, {"debut": "1957-01"})], portes=2, places=4, reservoir=21,
   remarques="Microvoiture T 250 / T 300 / T 400, bicylindre deux-temps arrière ; " + IND)
mg(L, "Goggomobil TS", "TS", "1", "1957-01", "1969-06", [("250 2T 14", "GLAS-2T-0.25", 19), ("300 2T 15", "GLAS-2T-0.3", 22), ("400 2T 20", "GLAS-2T-0.4", 30)],
   portes=2, places=4, reservoir=21, remarques="Coupé TS 250 / 300 / 400 ; " + IND)
mg(L, "Isar", "T", "1", "1958-09", "1965-12", [("T 600 0.6 20", "GLAS-ISAR-0.6", 40), ("T 700 0.7 30", "GLAS-ISAR-0.7", 50)], portes=2, places=4, reservoir=30,
   remarques="Petite berline et break, bicylindre à plat quatre-temps ; " + IND)
mg(L, "1004", "1004", "1", "1962-01", "1967-12", [("1.0 42", "GLAS-1.0", 73), ("TS 1.0 64", "GLAS-1.0", 80, {"debut": "1963-01"})], portes=2, places=4, reservoir=40,
   remarques="Berline, coupé et cabriolet, premier arbre à cames par courroie crantée en série ; " + IND)
mg(L, "1300 GT", "GT", "1", "1964-01", "1967-12", [("1.3 75", "GLAS-1.3", 105), ("1.3 85", "GLAS-1.3", 107)], portes=2, places=2, reservoir=40,
   remarques="Coupé et cabriolet Frua (devenu BMW 1600 GT) ; " + IND)
mg(L, "1700", "1700", "1", "1964-01", "1967-12", [("1.7 80", "GLAS-1.7", 132), ("TS 1.7 100", "GLAS-1.7", 140)], portes=4, places=5, reservoir=50,
   remarques="Berline Frua (devenue BMW 1800 SA en Afrique du Sud) ; " + IND)
mg(L, "2600 V8", "V8", "1", "1966-01", "1968-12", [("2.6 V8 140", "GLAS-V8-2.6", 206), ("3000 3.0 V8 160", "GLAS-V8-3.0", 240, {"debut": "1967-09"})],
   portes=2, places=4, reservoir=70, remarques="Coupé Frua « Glaserati », poursuivi comme BMW-Glas 3000 V8 ; " + IND)

MOT = Motorisations("Glas", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Glas": L}
MOTEURS = MOT.moteurs()
