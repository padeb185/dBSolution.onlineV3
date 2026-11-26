"""Saab : générations, phases, motorisations (marché européen) et moteurs liés.
92, 93, 95, 96, 99, 90, 900 (classique et NG), 9000, 9-3 (I et II, dont cabriolet), 9-5 (I et II) et 9-4X. Marque fermée en 2011-2012.
Moteurs Saab B/H, deux temps et V4 Ford ajoutés ; Saab B207 / V6 2.8 Turbo et Fiat 1.9 repris de cadillac.py, moteurs Opel / GM
repris d'opel.py (mêmes codes). Saab 9-3 EV (prototype) et 9-7X (Amérique du Nord) non repris. Données anciennes indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .cadillac import FAMILLES as FAMILLES_CADILLAC
from .opel import FAMILLES as FAMILLES_OPEL

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

SAAB_PROPRES = {
    "SAAB-2T-0.76": f("ATM", E_, 0.76, "NC", 2, 3800, 2500, "SAE30", 2.5, 3000),
    "SAAB-2T-0.75": f("ATM", E_, 0.75, "NC", 3, 4200, 3000, "SAE30", 2.5, 3000),
    "SAAB-2T-0.84": f("ATM", E_, 0.84, "NC", 3, 4500, 3000, "SAE30", 2.5, 3000),
    "SAAB-B-1.7": f("ATM", E_, 1.7, C, 4, 5200, 3000, "20W50", 3.5, 10000),
    "SAAB-B-1.85": f("ATM", E_, 1.85, C, 4, 5200, 3000, "20W50", 3.5, 10000),
    "SAAB-B-2.0": f("ATM", E_, 2.0, C, 4, 5200, 3500, "10W40", 3.5, 10000),
    "SAAB-B-2.0T": f("TURBO", E_, 2.0, C, 4, 5000, 3000, "10W40", 3.5, 7500),
    "SAAB-H-2.0": f("ATM", E_, 2.0, C, 4, 6000, 3500, "10W40", 4.0, 10000),
    "SAAB-H-2.0T": f("TURBO", E_, 2.0, C, 4, 5500, 2500, "5W40", 4.0, 10000),
    "SAAB-H-2.3": f("ATM", E_, 2.3, C, 4, 5700, 4300, "10W40", 4.0, 10000),
    "SAAB-H-2.3T": f("TURBO", E_, 2.3, C, 4, 5500, 2000, "5W40", 4.0, 10000),
    "SAAB-V6-3.0T": f("TURBO", E_, 3.0, B, 6, 5000, 2500, "5W40", 5.0, 15000, a="V"),
}
FORD = {"FORD-V4-1.5": f("ATM", E_, 1.5, C, 4, 4700, 2500, "20W50", 4.0, 7500, a="V")}
ISUZU = {"ISUZU-V6-3.0D": f("TURBO", D, 3.0, C, 6, 4000, 1500, "5W30", 6.5, 15000, a="V")}
CAD = {k: FAMILLES_CADILLAC[k] for k in ("SAAB-1.8T", "SAAB-2.0T", "SAAB-V6-2.8T", "FIAT-1.9TID")}
OPEL = {k: FAMILLES_OPEL[k] for k in ("X25XE-2.5V6", "X30XE-3.0V6", "ECOTEC-2.2DTI", "FAM2-1.8", "FAM1-1.6T", "A20NHT-2.0T", "Z28NET-2.8V6T", "A20DTH-2.0CDTI")}
FAMILLES = {**SAAB_PROPRES, **FORD, **ISUZU, **CAD, **OPEL}


def motoriste(fam):
    if fam in FORD:
        return "Ford"
    if fam in ISUZU:
        return "Isuzu"
    if fam == "FIAT-1.9TID":
        return "Fiat"
    if fam in OPEL:
        return "Opel"
    return "Saab"


mg = SaisieMoteurs(FAMILLES, "Saab", motoriste)
L = []
IND = "données indicatives"

# ---------------------------------------------------------------- deux temps et V4
mg(L, "92", "92", "1", "1949-12", "1956-12", [("0.76 2T 25", "SAAB-2T-0.76", 59), ("0.76 2T 28", "SAAB-2T-0.76", 62, {"debut": "1953-01"})], portes=2, places=4, reservoir=33,
   remarques="Bicylindre deux temps ; " + IND)
mg(L, "93", "93", "1", "1955-12", "1960-12", [("0.75 2T 33", "SAAB-2T-0.75", 68), ("0.75 2T 38", "SAAB-2T-0.75", 72, {"debut": "1957-01"})], portes=2, places=4, reservoir=37,
   remarques="Trois cylindres deux temps ; 93 B et 93 F ; " + IND)
mg(L, "96", "96", "1", "1960-02", "1980-01",
   [("0.84 2T 38", "SAAB-2T-0.84", 79, {"fin": "1967-12"}), ("Sport / Monte Carlo 0.84 2T 55", "SAAB-2T-0.84", 82, {"debut": "1962-01", "fin": "1967-12"}),
    ("V4 1.5 65", "FORD-V4-1.5", 116, {"debut": "1967-01"})], portes=2, places=4, reservoir=40, remarques="Deux temps puis V4 Ford ; " + IND)
mg(L, "95", "95", "1", "1959-12", "1978-12", [("0.84 2T 42", "SAAB-2T-0.84", 79, {"fin": "1967-12"}), ("V4 1.5 65", "FORD-V4-1.5", 116, {"debut": "1967-01"})],
   portes=3, places=7, reservoir=40, remarques="Break (7 places avec banquette d'appoint) ; " + IND)

# ---------------------------------------------------------------- 99 / 90 / 900 classique
mg(L, "99", "99", "1", "1968-11", "1984-06",
   [("1.7 80", "SAAB-B-1.7", 128, {"fin": "1971-12"}), ("1.85 87", "SAAB-B-1.85", 137, {"debut": "1971-01", "fin": "1972-12"}), ("2.0 100", "SAAB-B-2.0", 162, {"debut": "1972-01"}),
    ("EMS 2.0 118", "SAAB-B-2.0", 167, {"debut": "1974-01", "fin": "1978-12"}), ("Turbo 2.0 145", "SAAB-B-2.0T", 235, {"debut": "1977-09", "fin": "1980-12"})],
   portes=2, places=5, reservoir=55, remarques="2 et 4 portes, Combi Coupé ; " + IND)
mg(L, "90", "90", "1", "1984-08", "1987-12", [("2.0 100", "SAAB-B-2.0", 162)], portes=2, places=5, reservoir=63, remarques="Avant de 99, arrière de 900 ; " + IND)
mg(L, "900", "900 classique", "1", "1978-05", "1993-12",
   [("2.0 100", "SAAB-B-2.0", 162), ("i 2.0 118", "SAAB-B-2.0", 167), ("Turbo 2.0 145", "SAAB-B-2.0T", 235, {"fin": "1984-12"}), ("i 16V 2.0 128", "SAAB-H-2.0", 173, {"debut": "1985-01"}),
    ("Turbo 16 2.0 160", "SAAB-H-2.0T", 255, {"debut": "1984-09"}), ("Turbo 16 S 2.0 175", "SAAB-H-2.0T", 273, {"debut": "1988-01"}), ("i 2.1 140", "SAAB-H-2.3", 177, {"debut": "1990-01", "remarques": "2.1 B212 rattaché à la famille H"})],
   portes=3, places=5, reservoir=63, remarques="3, 4 et 5 portes, cabriolet (1986) ; " + IND)

# ---------------------------------------------------------------- 9000 / 900 NG / 9-3 I
mg(L, "9000", "9000", "1", "1984-10", "1998-12",
   [("i 2.0 16V 130", "SAAB-H-2.0", 177, {"fin": "1990-12"}), ("Turbo 2.0 16V 175", "SAAB-H-2.0T", 273), ("2.3 150", "SAAB-H-2.3", 212, {"debut": "1990-01"}),
    ("2.3 Turbo 170", "SAAB-H-2.3T", 280, {"debut": "1993-01"}), ("2.3 Turbo 200", "SAAB-H-2.3T", 330, {"debut": "1991-01"}), ("Aero 2.3 Turbo 225", "SAAB-H-2.3T", 342, {"debut": "1993-01"}),
    ("3.0 V6 210", "X30XE-3.0V6", 270, {"debut": "1995-01"})], portes=5, places=5, reservoir=66, remarques="5 portes CC/CD (berline) ; " + IND)
mg(L, "900", "900 NG", "1", "1994-01", "1998-06",
   [("2.0 133", "SAAB-H-2.0", 177), ("2.3 150", "SAAB-H-2.3", 212), ("2.0 Turbo 185", "SAAB-H-2.0T", 263), ("2.5 V6 170", "X25XE-2.5V6", 227)],
   portes=3, places=5, reservoir=68, remarques="Base GM2900 (Opel Vectra) ; 3 et 5 portes, cabriolet ; " + IND)
mg(L, "9-3", "9-3 I", "1", "1998-03", "2002-08",
   [("2.0 130", "SAAB-H-2.0", 177), ("2.0t 150", "SAAB-H-2.0T", 240), ("2.0 T 185", "SAAB-H-2.0T", 263), ("2.3 150", "SAAB-H-2.3", 212), ("Viggen 2.3 Turbo 230", "SAAB-H-2.3T", 350, {"debut": "1999-01"}),
    ("2.2 TiD 115", "ECOTEC-2.2DTI", 260), ("2.2 TiD 125", "ECOTEC-2.2DTI", 280, {"debut": "2000-01"})], portes=3, places=5, reservoir=68,
   remarques="3 et 5 portes, cabriolet ; " + IND)

# ---------------------------------------------------------------- 9-5 / 9-3 II / 9-4X
mg(L, "9-5", "9-5 I", "1", "1997-09", "2005-08",
   [("2.0t 150", "SAAB-H-2.0T", 240), ("2.3t 170", "SAAB-H-2.3T", 280), ("2.3t 185", "SAAB-H-2.3T", 280), ("2.3 T 220", "SAAB-H-2.3T", 310), ("Aero 2.3 Turbo 230", "SAAB-H-2.3T", 350),
    ("Aero 2.3 Turbo 250", "SAAB-H-2.3T", 350, {"debut": "2002-01"}), ("3.0 V6t 200", "SAAB-V6-3.0T", 310, {"fin": "2003-12"}), ("2.2 TiD 120", "ECOTEC-2.2DTI", 280, {"debut": "2002-01"}),
    ("3.0 TiD 176", "ISUZU-V6-3.0D", 350, {"debut": "2001-01"})], portes=4, places=5, reservoir=75, remarques="Berline et break ; restylage 2001 ; " + IND)
mg(L, "9-5", "9-5 I", "2", "2005-09", "2010-02",
   [("2.0t 150", "SAAB-H-2.0T", 240), ("2.3t 185", "SAAB-H-2.3T", 280), ("Aero 2.3 Turbo 260", "SAAB-H-2.3T", 350), ("1.9 TiD 150", "FIAT-1.9TID", 320)],
   portes=4, places=5, reservoir=75, remarques="Restylage ; berline et break")
mg(L, "9-3", "9-3 II", "1", "2002-09", "2007-08",
   [("1.8 122", "FAM2-1.8", 165), ("1.8t 150", "SAAB-1.8T", 240), ("2.0t 175", "SAAB-2.0T", 265), ("2.0 T 210", "SAAB-2.0T", 300), ("Aero 2.8 V6 Turbo 250", "SAAB-V6-2.8T", 350, {"debut": "2005-09"}),
    ("1.9 TiD 120", "FIAT-1.9TID", 280, {"debut": "2004-06"}), ("1.9 TiD 150", "FIAT-1.9TID", 320, {"debut": "2004-06"}), ("2.2 TiD 125", "ECOTEC-2.2DTI", 280, {"fin": "2004-12"})],
   portes=4, places=5, reservoir=58, remarques="Berline, break SportCombi et cabriolet")
mg(L, "9-3", "9-3 II", "2", "2007-09", "2014-12",
   [("1.8t 150", "SAAB-1.8T", 240), ("2.0t 175", "SAAB-2.0T", 265), ("2.0 T 210", "SAAB-2.0T", 300), ("Aero 2.8 V6 Turbo 280", "SAAB-V6-2.8T", 350), ("1.9 TiD 120", "FIAT-1.9TID", 280),
    ("1.9 TiD 150", "FIAT-1.9TID", 320), ("1.9 TTiD 180", "FIAT-1.9TID", 400)], portes=4, places=5, reservoir=58,
   remarques="Restylage ; berline, SportCombi, cabriolet et 9-3X ; série NEVS limitée en 2013-2014")
mg(L, "9-5", "9-5 II", "1", "2010-06", "2011-12",
   [("1.6 Turbo 180", "FAM1-1.6T", 230), ("2.0 Turbo 220", "A20NHT-2.0T", 350), ("Aero 2.8 V6 Turbo 300", "Z28NET-2.8V6T", 400), ("2.0 TiD 160", "A20DTH-2.0CDTI", 350),
    ("2.0 TTiD 190", "A20DTH-2.0CDTI", 400, {"debut": "2011-01"})], portes=4, places=5, reservoir=70, remarques="Base GM Epsilon II (Opel Insignia) ; break SportCombi très rare")
mg(L, "9-4X", "9-4X", "1", "2011-05", "2011-12", [("Aero 2.8 V6 Turbo 300", "Z28NET-2.8V6T", 400)], portes=5, places=5, reservoir=70,
   remarques="SUV sur base Cadillac SRX, quelques centaines d'exemplaires ; " + IND)

MOT = Motorisations("Saab", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Saab": L}
MOTEURS = MOT.moteurs()
