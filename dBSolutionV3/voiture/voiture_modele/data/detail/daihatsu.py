"""Daihatsu : générations, motorisations (marché européen, jusqu'au retrait de 2013) et moteurs liés.
Cuore, Charade, Applause, Sirion, YRV, Move, Gran Move, Copen, Terios, Feroza, Rocky, Materia, Trevis.
Modèles réservés au Japon (Cast, kei-cars récentes) non repris. Données indicatives (marque retirée d'Europe en 2013).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

FAMILLES = {
    "ED-0.85": f("ATM", E_, 0.85, B, 3, 5500, 3200, "10W40", 2.6, 10000),
    "CB-1.0": f("ATM", E_, 1.0, B, 3, 5600, 3200, "10W40", 3.0, 10000),
    "CL-1.0TD": f("TURBO", D, 1.0, B, 3, 4800, 2500, "15W40", 3.5, 7500),
    "EJ-1.0": f("ATM", E_, 1.0, C, 3, 6000, 3600, "5W30", 3.0, 15000),
    "1KR-1.0": f("ATM", E_, 1.0, C, 3, 6000, 3600, "0W20", 3.0, 15000),
    "HC-1.3": f("ATM", E_, 1.3, B, 4, 6500, 5000, "10W40", 3.2, 10000),
    "K3-1.3": f("ATM", E_, 1.3, C, 4, 6000, 4400, "5W30", 3.2, 15000),
    "K3-1.3T": f("TURBO", E_, 1.3, C, 4, 6400, 3200, "5W30", 3.2, 10000),
    "JB-0.66T": f("TURBO", E_, 0.66, B, 4, 6000, 3200, "5W30", 3.0, 10000),
    "HD-1.6": f("ATM", E_, 1.6, B, 4, 5700, 4800, "10W40", 3.5, 10000),
    "3SZ-1.5": f("ATM", E_, 1.5, C, 4, 6000, 4400, "5W30", 3.6, 15000),
    "1NR-1.33": f("ATM", E_, 1.33, C, 4, 6000, 4000, "0W20", 3.4, 15000),
    "DL-2.8TD": f("TURBO", D, 2.8, B, 4, 3600, 2200, "15W40", 6.0, 7500),
}

mg = SaisieMoteurs(FAMILLES, "Daihatsu")
L = []
IND = "Données indicatives"

mg(L, "Cuore", "L201", "1", "1990-01", "1995-06", [("0.85 42", "ED-0.85", 66)], portes=3, places=4, reservoir=30, remarques=IND + " ; 3 et 5 portes")
mg(L, "Cuore", "L501", "1", "1995-07", "1998-08", [("0.85 42", "ED-0.85", 66)], portes=3, places=4, reservoir=30, remarques=IND)
mg(L, "Cuore", "L701", "1", "1998-09", "2003-06", [("1.0 56", "EJ-1.0", 88)], portes=3, places=4, reservoir=36, remarques=IND)
mg(L, "Cuore", "L251", "1", "2003-07", "2007-06", [("1.0 58", "EJ-1.0", 91)], portes=3, places=4, reservoir=36, remarques=IND)
mg(L, "Cuore", "L276", "1", "2007-07", "2012-12", [("1.0 70", "1KR-1.0", 94)], places=4, reservoir=36, remarques=IND)
mg(L, "Charade", "G100", "1", "1987-01", "1993-06", [("1.0 52", "CB-1.0", 75), ("1.0 TD 46", "CL-1.0TD", 91), ("1.3 16V 75", "HC-1.3", 103, {"debut": "1988-01"})],
   portes=3, reservoir=40, remarques=IND + " ; 3 et 5 portes")
mg(L, "Charade", "G200", "1", "1993-01", "2000-12", [("1.3 16V 84", "HC-1.3", 105), ("1.5 16V 90", "HC-1.3", 120), ("GTti 1.6 105", "HD-1.6", 138)],
   portes=3, reservoir=40, remarques=IND + " ; 3 et 5 portes, berline")
mg(L, "Charade", "XP90", "1", "2011-03", "2013-01", [("1.33 99", "1NR-1.33", 125)], reservoir=42, remarques=IND + " ; Toyota Yaris rebadgée")
mg(L, "Applause", "A101", "1", "1989-01", "2000-12", [("1.6 16V 90", "HD-1.6", 128), ("1.6 16V 105", "HD-1.6", 135, {"debut": "1992-01"})], reservoir=50,
   remarques=IND + " ; liftback 5 portes")
mg(L, "Sirion", "M100", "1", "1998-09", "2004-12", [("1.0 56", "EJ-1.0", 88), ("1.3 102", "K3-1.3", 122, {"debut": "2002-01"})], reservoir=40, remarques=IND)
mg(L, "Sirion", "M300", "1", "2005-01", "2012-12", [("1.0 70", "1KR-1.0", 94), ("1.3 87", "K3-1.3", 120), ("1.5 103", "3SZ-1.5", 132, {"debut": "2007-01"})],
   reservoir=40, remarques=IND + " ; jumelle Subaru Justy")
mg(L, "YRV", "M201", "1", "2001-01", "2005-12", [("1.3 87", "K3-1.3", 120), ("Turbo 1.3 140", "K3-1.3T", 177)], reservoir=40, remarques=IND)
mg(L, "Move", "L601", "1", "1995-09", "1998-12", [("0.85 42", "ED-0.85", 66)], places=4, reservoir=36, remarques=IND + " ; monospace urbain")
mg(L, "Move", "L901", "1", "1999-01", "2002-12", [("1.0 56", "EJ-1.0", 88)], places=4, reservoir=36, remarques=IND)
mg(L, "Gran Move", "G303", "1", "1996-09", "2002-12", [("1.5 90", "HC-1.3", 120), ("1.6 91", "HD-1.6", 130, {"debut": "1999-01"})], reservoir=50, remarques=IND)
mg(L, "Copen", "L880", "1", "2003-01", "2012-12", [("0.66 Turbo 68", "JB-0.66T", 110, {"fin": "2006-12"}), ("1.3 87", "K3-1.3", 120, {"debut": "2006-01"})],
   portes=2, places=2, reservoir=40, remarques=IND + " ; roadster à toit rigide escamotable")
mg(L, "Terios", "J100", "1", "1997-06", "2006-03", [("1.3 83", "HC-1.3", 107, {"fin": "2000-12"}), ("1.3 86", "K3-1.3", 120, {"debut": "2001-01"})], reservoir=46,
   remarques=IND + " ; mini-SUV 4x4")
mg(L, "Terios", "J200", "1", "2006-04", "2013-01", [("1.5 105", "3SZ-1.5", 140)], reservoir=50, remarques=IND + " ; 2WD et 4WD")
mg(L, "Feroza", "F300", "1", "1989-01", "1998-12", [("1.6 95", "HD-1.6", 128)], portes=3, places=4, reservoir=60, remarques=IND + " ; 4x4 découvrable")
mg(L, "Rocky", "F70", "1", "1984-01", "1993-12", [("2.8 TD 101", "DL-2.8TD", 220)], portes=3, places=4, reservoir=60, remarques=IND + " ; 4x4 court et long")
mg(L, "Materia", "M400", "1", "2007-01", "2011-12", [("1.5 103", "3SZ-1.5", 132)], reservoir=40, remarques=IND + " ; monospace compact")
mg(L, "Trevis", "L651", "1", "2006-01", "2010-12", [("1.0 58", "EJ-1.0", 91)], places=4, reservoir=36, remarques=IND + " ; citadine néo-rétro")

MOT = Motorisations("Daihatsu", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Daihatsu": L}
MOTEURS = MOT.moteurs()
