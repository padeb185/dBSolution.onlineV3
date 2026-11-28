"""Innocenti (Milan-Lambrate) : générations, phases, motorisations (marché italien) et moteurs liés.
Licence BMC / British Leyland : A40, 950 / S Spider, Coupé C, IM3 / I4 / I5 (ADO16), Mini (ADO15, dont Cooper), Regent (Allegro) ;
Mini Bertone (90 / 120, Mille, De Tomaso) ; Mini 3 Cilindri et Turbo De Tomaso à moteurs Daihatsu ; ère Fiat : Koral (Yugo), Elba (Duna
Weekend) et Mille (Uno Mille brésilienne). Prototype 186 GT non repris. Moteurs BMC série A / B, Daihatsu et Fiat ajoutés.
Puissances en ch DIN. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"
FAMILLES = {
    "BMC-A-0.85": f("ATM", E_, 0.85, C, 4, 5500, 2900, "20W50", 4.5, 5000),
    "BMC-A-0.95": f("ATM", E_, 0.95, C, 4, 5000, 2500, "20W50", 4.5, 5000),
    "BMC-A-1.0": f("ATM", E_, 1.0, C, 4, 5500, 3000, "20W50", 4.5, 5000),
    "BMC-A-1.1": f("ATM", E_, 1.1, C, 4, 5500, 3000, "20W50", 4.5, 5000),
    "BMC-A-1.3": f("ATM", E_, 1.3, C, 4, 5800, 3000, "20W50", 4.5, 5000),
    "BMC-E-1.5": f("ATM", E_, 1.5, C, 4, 5500, 3000, "20W50", 4.5, 5000),
    "DAIHATSU-CB-1.0": f("ATM", E_, 1.0, B, 3, 5600, 3200, "10W40", 3.0, 10000),
    "DAIHATSU-CB-1.0T": f("TURBO", E_, 1.0, B, 3, 6200, 3200, "10W40", 3.0, 7500),
    "DAIHATSU-CL-1.0D": f("ATM", D, 1.0, B, 3, 4800, 3000, "15W40", 3.5, 7500),
    "FIAT-1.1": f("ATM", E_, 1.1, B, 4, 5800, 3000, "10W40", 3.5, 10000),
    "FIAT-1.4": f("ATM", E_, 1.4, B, 4, 6000, 3000, "10W40", 3.9, 10000),
    "FIAT-1.7D": f("ATM", D, 1.7, B, 4, 4600, 2500, "15W40", 4.5, 10000),
    "FIAT-FIRE-1.0": f("ATM", E_, 1.0, B, 4, 6000, 2750, "10W40", 3.0, 10000),
}


def motoriste(fam):
    return "Austin" if fam.startswith("BMC") else ("Daihatsu" if fam.startswith("DAIHATSU") else "Fiat")


mg = SaisieMoteurs(FAMILLES, "Innocenti", motoriste)
L = []
IND = "données indicatives"

mg(L, "A40", "A40", "1", "1960-01", "1967-12", [("0.95 43", "BMC-A-0.95", 70, {"fin": "1962-12"}), ("1.1 48", "BMC-A-1.1", 81, {"debut": "1963-01"})], portes=3, places=5, reservoir=35,
   remarques="Austin A40 Farina, Berlina et Combinata ; " + IND)
mg(L, "950 Spider", "Spider", "1", "1961-01", "1968-12", [("0.95 43", "BMC-A-0.95", 70, {"fin": "1963-06"}), ("S 1.1 58", "BMC-A-1.1", 81, {"debut": "1963-07"})], portes=2, places=2, reservoir=40,
   remarques="Base Austin-Healey Sprite, carrosserie Ghia ; Spider S 1100 ; Coupé C (1966-1968) ; " + IND)
mg(L, "IM3 / I4 / I5", "ADO16", "1", "1963-01", "1974-12",
   [("IM3 1.1 58", "BMC-A-1.1", 81, {"fin": "1966-12"}), ("IM3S 1.1 66", "BMC-A-1.1", 85, {"fin": "1966-12"}), ("I4 1.1 50", "BMC-A-1.1", 79, {"debut": "1967-01"}),
    ("I5 1.3 60", "BMC-A-1.3", 95, {"debut": "1970-01"})], portes=4, places=5, reservoir=45, remarques="Austin / Morris 1100 sous licence ; " + IND)
mg(L, "Mini", "ADO15", "1", "1965-01", "1975-12", [("Minor 850 0.85 34", "BMC-A-0.85", 59), ("1000 1.0 42", "BMC-A-1.0", 69, {"debut": "1970-01"})], portes=2, places=4, reservoir=25,
   remarques="Mini Minor, T (break) et Matic ; " + IND)
mg(L, "Mini Cooper", "ADO15", "1", "1966-01", "1975-12", [("Mk1 1.0 56", "BMC-A-1.0", 75, {"fin": "1971-12"}), ("1300 1.3 71", "BMC-A-1.3", 105, {"debut": "1972-01"})], portes=2, places=4, reservoir=25,
   remarques="Cooper Mk1, Mk2 et Mk3, puis Cooper 1300 ; " + IND)
mg(L, "Regent", "Regent", "1", "1974-01", "1976-12", [("1.3 60", "BMC-A-1.3", 95), ("1.5 69", "BMC-E-1.5", 112)], portes=4, places=5, reservoir=50, remarques="Austin Allegro ; " + IND)
mg(L, "Mini Bertone", "90 / 120", "1", "1974-11", "1982-12", [("90 1.0 49", "BMC-A-1.0", 72), ("120 1.3 65", "BMC-A-1.3", 98)], portes=3, places=4, reservoir=40,
   remarques="Hatchback dessinée par Bertone sur base Mini ; " + IND)
mg(L, "Mini De Tomaso", "De Tomaso", "1", "1976-01", "1987-12", [("1.3 71", "BMC-A-1.3", 105, {"fin": "1982-12"}), ("Turbo 1.0 72", "DAIHATSU-CB-1.0T", 107, {"debut": "1983-01"})],
   portes=3, places=4, reservoir=40, remarques="Version sportive, puis Turbo De Tomaso à trois cylindres Daihatsu ; " + IND)
mg(L, "Mini 3 Cilindri", "Mini 3 Cilindri", "1", "1982-01", "1993-12", [("1.0 52", "DAIHATSU-CB-1.0", 76), ("Diesel 1.0 37", "DAIHATSU-CL-1.0D", 62, {"debut": "1985-01"})],
   portes=3, places=4, reservoir=40, remarques="Mini 500 / 650 / 990, Mille ; moteurs Daihatsu ; " + IND)
mg(L, "Koral", "Koral", "1", "1991-01", "1993-12", [("1.1 55", "FIAT-1.1", 84), ("1.3 65", "FIAT-1.4", 100)], portes=3, places=5, reservoir=32,
   remarques="Zastava Koral (Yugo) rebadgée ; " + IND)
mg(L, "Elba", "Elba", "1", "1991-01", "1996-12", [("1.4 72", "FIAT-1.4", 106), ("1.7 D 60", "FIAT-1.7D", 103)], portes=5, places=5, reservoir=50,
   remarques="Fiat Duna Weekend importée du Brésil ; " + IND)
mg(L, "Mille", "Mille", "1", "1993-01", "1997-12", [("1.0 56", "FIAT-FIRE-1.0", 80)], portes=3, places=5, reservoir=45, remarques="Fiat Uno Mille brésilienne ; " + IND)

MOT = Motorisations("Innocenti", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Innocenti": L}
MOTEURS = MOT.moteurs()
