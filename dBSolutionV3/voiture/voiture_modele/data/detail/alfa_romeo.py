"""Alfa Romeo : générations, phases, motorisations (marché européen) et moteurs liés.
Giulietta et Giulia classiques, Spider, Alfetta (et GT/GTV), Alfasud, Giulietta 116, 33, 75, 164, 155, 145/146, GTV/Spider 916,
156, 166, 147, GT, 159, Brera/Spider, 8C, MiTo, Giulietta 940, 4C, Giulia 952, Stelvio, Tonale, Junior, 33 Stradale.
Moteurs propres au motoriste « Alfa Romeo » ; moteurs FCA/Stellantis partagés (MultiAir, TwinAir, JTD/Multijet, Hybrid)
avec les familles et codes de fiat.py (motoriste « Fiat »). Avant-guerre et modèles anciens dans alfa_romeo_classiques.py.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .fiat import FAMILLES as FAMILLES_FIAT

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

PROPRES = {
    # --- double arbre classique
    "AR-TC-1.3": f("ATM", E_, 1.3, C, 4, 6000, 4000, "20W50", 6.5, 5000),
    "AR-TC-1.6": f("ATM", E_, 1.6, C, 4, 6000, 4000, "20W50", 6.5, 5000),
    "AR-TC-1.8": f("ATM", E_, 1.8, C, 4, 5500, 4000, "20W50", 6.5, 5000),
    "AR-TC-2.0": f("ATM", E_, 2.0, C, 4, 5400, 4000, "20W50", 6.5, 7500),
    "AR-TS-2.0": f("ATM", E_, 2.0, C, 4, 5800, 4000, "15W40", 6.5, 10000),
    "AR-TS-1.8": f("ATM", E_, 1.8, C, 4, 6000, 4000, "15W40", 6.5, 10000),
    "AR-TC-2.0T": f("TURBO", E_, 2.0, B, 4, 6000, 3000, "10W40", 5.0, 10000),
    "AR-TC-1.8T": f("TURBO", E_, 1.8, C, 4, 5800, 2600, "15W40", 6.5, 10000),
    # --- boxer
    "AR-BOXER-1.2": f("ATM", E_, 1.2, B, 4, 6000, 3500, "20W50", 4.0, 7500, a="PLAT"),
    "AR-BOXER-1.3": f("ATM", E_, 1.3, B, 4, 6000, 4000, "15W40", 4.0, 10000, a="PLAT"),
    "AR-BOXER-1.5": f("ATM", E_, 1.5, B, 4, 6000, 4000, "15W40", 4.0, 10000, a="PLAT"),
    "AR-BOXER-1.6": f("ATM", E_, 1.6, B, 4, 6000, 4500, "15W40", 4.0, 10000, a="PLAT"),
    "AR-BOXER-1.7": f("ATM", E_, 1.7, B, 4, 6500, 4600, "15W40", 4.0, 10000, a="PLAT"),
    # --- Busso V6
    "BUSSO-2.0T": f("TURBO", E_, 2.0, B, 6, 6000, 2500, "10W60", 6.0, 10000, a="V"),
    "BUSSO-2.5": f("ATM", E_, 2.5, B, 6, 6000, 3200, "10W60", 6.0, 10000, a="V"),
    "BUSSO-2.5-24V": f("ATM", E_, 2.5, B, 6, 6300, 5000, "10W60", 6.0, 10000, a="V"),
    "BUSSO-3.0": f("ATM", E_, 3.0, B, 6, 6200, 4500, "10W60", 6.0, 10000, a="V"),
    "BUSSO-3.0-24V": f("ATM", E_, 3.0, B, 6, 6300, 5000, "10W60", 6.0, 10000, a="V"),
    "BUSSO-3.2-24V": f("ATM", E_, 3.2, B, 6, 6200, 4800, "10W60", 6.0, 10000, a="V"),
    # --- Twin Spark 16V / JTS / TBi
    "TS16-1.4": f("ATM", E_, 1.4, B, 4, 6300, 4600, "10W40", 4.4, 20000),
    "TS16-1.6": f("ATM", E_, 1.6, B, 4, 6300, 4200, "10W40", 4.4, 20000),
    "TS16-1.8": f("ATM", E_, 1.8, B, 4, 6500, 3500, "10W40", 4.4, 20000),
    "TS16-2.0": f("ATM", E_, 2.0, B, 4, 6400, 3500, "10W40", 4.4, 20000),
    "JTS-2.0": f("ATM", E_, 2.0, B, 4, 6400, 3250, "10W40", 4.4, 20000),
    "JTS-2.2": f("ATM", E_, 2.2, C, 4, 6500, 4500, "5W40", 5.5, 20000),
    "JTS-3.2": f("ATM", E_, 3.2, C, 6, 6200, 4500, "5W40", 6.5, 20000, a="V"),
    "MPI-1.8": f("ATM", E_, 1.8, C, 4, 6500, 4500, "5W40", 5.5, 20000),
    "TBI-1.75": f("TURBO", E_, 1.75, C, 4, 5500, 1400, "5W40", 5.5, 20000),
    # --- ère Giorgio
    "GME-2.0T": f("TURBO", E_, 2.0, C, 4, 5250, 2250, "0W30", 5.5, 15000),
    "V6-2.9BT": f("TURBO", E_, 2.9, C, 6, 6500, 2500, "0W40", 7.5, 15000, a="V"),
    "V6-3.0TT-33": f("TURBO", E_, 3.0, C, 6, 7500, 3000, "0W40", 7.5, 15000, a="V"),
    "JTDM-2.2": f("TURBO", D, 2.2, C, 4, 3750, 1750, "0W30", 5.5, 20000),
    "FIREFLY-1.3-PHEV": f("HYB_E", E_, 1.3, C, 4, 5750, 1850, "0W20", 3.5, 15000),
    "F136-4.7": f("ATM", E_, 4.7, C, 8, 7000, 4750, "10W60", 9.0, 15000, a="V"),
    # --- diesel ancien (VM Motori)
    "VM-1.8TD": f("TURBO", D, 1.8, B, 3, 4200, 2400, "15W40", 5.0, 10000),
    "VM-2.0TD": f("TURBO", D, 2.0, B, 4, 4300, 2300, "15W40", 6.0, 10000),
    "VM-2.4TD": f("TURBO", D, 2.4, B, 4, 4200, 2200, "15W40", 6.5, 10000),
    "VM-2.5TD": f("TURBO", D, 2.5, B, 4, 4100, 2000, "15W40", 6.5, 10000),
}
FIAT = ("FIRE-1.4", "TJET-1.4", "MULTIAIR-1.4", "MULTIAIR-1.4T", "TWINAIR-0.9", "TD-1.9", "JTD-1.9", "JTD-2.4", "MJ-1.3", "MJ-1.6",
        "MJ-2.0", "MJ-2.4", "FIREFLY-1.5-HYB", "EB2-MHEV", "e-CMP")
FAMILLES = {**{k: FAMILLES_FIAT[k] for k in FIAT}, **PROPRES}


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Alfa Romeo", lambda fam: "Alfa Romeo" if fam in PROPRES else "Fiat")
L = []
CL = "Données indicatives (modèle ancien), à vérifier"

# ---------------------------------------------------------------- classiques
mg(L, "Giulietta", "750", "1", "1954-04", "1965-12",
   [("Berlina 1.3 53", "AR-TC-1.3", 88), ("Sprint 1.3 80", "AR-TC-1.3", 100), ("Spider 1.3 80", "AR-TC-1.3", 100, {"debut": "1955-06"}),
    ("TI 1.3 74", "AR-TC-1.3", 95, {"debut": "1957-01"})], portes=4, reservoir=40, remarques=CL)
mg(L, "Giulia", "105", "1", "1962-06", "1978-12",
   [("TI 1.6 92", "AR-TC-1.6", 118), ("Super 1.6 98", "AR-TC-1.6", 135, {"debut": "1965-01"}), ("1300 TI 82", "AR-TC-1.3", 103, {"debut": "1966-01"}),
    ("Sprint GT 1.6 106", "AR-TC-1.6", 140, {"debut": "1963-09", "fin": "1966-12"}), ("GT Junior 1300 89", "AR-TC-1.3", 137, {"debut": "1966-06"}),
    ("1750 GTV 118", "AR-TC-1.8", 186, {"debut": "1967-09", "fin": "1971-12"}), ("2000 GTV 131", "AR-TC-2.0", 182, {"debut": "1971-06", "fin": "1976-12"})],
   portes=4, reservoir=46, remarques=CL + " ; berline et coupés Bertone (GT/GTV)")
mg(L, "Spider", "105 Spider", "1", "1966-03", "1993-12",
   [("Duetto 1.6 109", "AR-TC-1.6", 140, {"fin": "1967-12"}), ("1750 Veloce 118", "AR-TC-1.8", 186, {"debut": "1967-09", "fin": "1971-12"}),
    ("1300 Junior 89", "AR-TC-1.3", 137, {"debut": "1968-06", "fin": "1977-12"}), ("2000 Veloce 131", "AR-TC-2.0", 182, {"debut": "1971-06", "fin": "1989-12"}),
    ("1.6 104", "AR-TC-1.6", 137, {"debut": "1972-01"}), ("2.0 S4 126", "AR-TC-2.0", 167, {"debut": "1990-01"})], portes=2, places=2, reservoir=46,
   remarques=CL + " ; 4 séries (Osso di seppia, Coda tronca, Aerodinamica, S4)")
mg(L, "Alfetta", "116", "1", "1972-05", "1984-12",
   [("1.6 109", "AR-TC-1.6", 142, {"debut": "1975-01"}), ("1.8 122", "AR-TC-1.8", 167), ("2.0 130", "AR-TC-2.0", 178, {"debut": "1977-01"}),
    ("2.0 TD 82", "VM-2.0TD", 162, {"debut": "1979-01"}), ("2.4 TD 95", "VM-2.4TD", 196, {"debut": "1983-01"})], portes=4, reservoir=49, remarques=CL)
mg(L, "Alfetta GT", "116 GT", "1", "1974-05", "1987-12",
   [("GT 1.6 109", "AR-TC-1.6", 142), ("GT 1.8 122", "AR-TC-1.8", 167), ("GTV 2.0 130", "AR-TC-2.0", 178, {"debut": "1976-01"}),
    ("GTV 2.0 Turbodelta 150", "AR-TC-1.8T", 230, {"debut": "1979-01", "fin": "1980-12"}), ("GTV6 2.5 160", "BUSSO-2.5", 213, {"debut": "1980-10"})],
   portes=2, places=4, reservoir=75, remarques=CL + " ; coupé Giugiaro")
mg(L, "Alfasud", "901", "1", "1972-06", "1984-12",
   [("1.2 63", "AR-BOXER-1.2", 88), ("ti 1.3 79", "AR-BOXER-1.3", 98, {"debut": "1977-01"}), ("1.5 85", "AR-BOXER-1.5", 117, {"debut": "1978-01"}),
    ("ti 1.5 95", "AR-BOXER-1.5", 128, {"debut": "1980-01"})], portes=4, reservoir=50, remarques=CL + " ; Sprint coupé")
mg(L, "Giulietta", "116", "1", "1977-11", "1985-12",
   [("1.6 109", "AR-TC-1.6", 142), ("1.8 122", "AR-TC-1.8", 167), ("2.0 130", "AR-TC-2.0", 178, {"debut": "1979-01"}), ("2.0 TD 82", "VM-2.0TD", 162, {"debut": "1983-01"})],
   portes=4, reservoir=49, remarques=CL)
mg(L, "33", "905", "1", "1983-06", "1989-12",
   [("1.3 79", "AR-BOXER-1.3", 98), ("1.5 95", "AR-BOXER-1.5", 128), ("1.5 4x4 105", "AR-BOXER-1.5", 133), ("1.7 118", "AR-BOXER-1.7", 146, {"debut": "1986-01"}),
    ("1.8 TD 73", "VM-1.8TD", 137, {"debut": "1986-01"})], reservoir=50, remarques=CL + " ; berline et Sport Wagon")
mg(L, "33", "907", "1", "1990-01", "1994-12",
   [("1.3 IE 88", "AR-BOXER-1.3", 108), ("1.5 IE 98", "AR-BOXER-1.5", 128), ("1.7 IE 110", "AR-BOXER-1.7", 146), ("16V 1.7 137", "AR-BOXER-1.7", 158),
    ("1.8 TD 84", "VM-1.8TD", 182)], reservoir=50, remarques=CL)
mg(L, "75", "162B", "1", "1985-05", "1992-12",
   [("1.6 110", "AR-TC-1.6", 146), ("1.8 120", "AR-TC-1.8", 167), ("1.8 Turbo 155", "AR-TC-1.8T", 226, {"debut": "1986-06"}),
    ("2.0 Twin Spark 148", "AR-TS-2.0", 186, {"debut": "1987-01"}), ("2.5 V6 156", "BUSSO-2.5", 206), ("3.0 V6 188", "BUSSO-3.0", 250, {"debut": "1987-01"}),
    ("2.0 TD 95", "VM-2.0TD", 186)], portes=4, reservoir=49, remarques=CL)
mg(L, "164", "164", "1", "1987-09", "1998-12",
   [("2.0 Twin Spark 148", "AR-TS-2.0", 186), ("2.0 V6 Turbo 205", "BUSSO-2.0T", 271, {"debut": "1991-01"}), ("3.0 V6 192", "BUSSO-3.0", 245),
    ("3.0 V6 24V 210", "BUSSO-3.0-24V", 260, {"debut": "1992-01"}), ("Q4 3.0 V6 24V 232", "BUSSO-3.0-24V", 285, {"debut": "1993-09"}),
    ("2.5 TD 117", "VM-2.5TD", 255)], portes=4, reservoir=70, remarques="Berline ; restylage 1992")
mg(L, "155", "167", "1", "1992-01", "1997-12",
   [("1.8 Twin Spark 126", "AR-TS-1.8", 165), ("2.0 Twin Spark 143", "AR-TS-2.0", 187), ("2.5 V6 165", "BUSSO-2.5", 216),
    ("Q4 2.0 Turbo 190", "AR-TC-2.0T", 298), ("1.8 TS 16V 140", "TS16-1.8", 165, {"debut": "1995-06"}), ("2.0 TS 16V 150", "TS16-2.0", 187, {"debut": "1995-06"}),
    ("1.9 TD 90", "TD-1.9", 186), ("2.5 TD 125", "VM-2.5TD", 294)], portes=4, reservoir=63)

# ---------------------------------------------------------------- années 90-2000
for m, p in (("145", 3), ("146", 5)):
    mg(L, m, "930", "1", "1994-07", "2001-01",
       [("1.3 90", "AR-BOXER-1.3", 115, {"fin": "1997-03"}), ("1.6 103", "AR-BOXER-1.6", 137, {"fin": "1997-03"}),
        ("1.4 TS 16V 103", "TS16-1.4", 124, {"debut": "1997-04"}), ("1.6 TS 16V 120", "TS16-1.6", 144, {"debut": "1997-04"}),
        ("1.8 TS 16V 140", "TS16-1.8", 165), ("2.0 TS 16V 150", "TS16-2.0", 186), ("1.9 TD 90", "TD-1.9", 186), ("1.9 JTD 105", "JTD-1.9", 255, {"debut": "1999-01"})],
       portes=p, reservoir=51, remarques="Quadrifoglio (145) et ti (146) en 2.0 TS")
mg(L, "GTV", "916", "1", "1995-01", "2005-12",
   [("2.0 TS 16V 150", "TS16-2.0", 186), ("2.0 V6 Turbo 200", "BUSSO-2.0T", 271, {"fin": "2000-12"}), ("3.0 V6 220", "BUSSO-3.0-24V", 270, {"fin": "2002-12"}),
    ("2.0 JTS 165", "JTS-2.0", 206, {"debut": "2003-01"}), ("3.2 V6 240", "BUSSO-3.2-24V", 289, {"debut": "2003-01"})], portes=2, places=4, reservoir=70,
   remarques="Coupé ; Spider 916 dans le modèle Spider")
mg(L, "Spider", "916", "1", "1995-01", "2005-12",
   [("1.8 TS 16V 144", "TS16-1.8", 169, {"fin": "1998-12"}), ("2.0 TS 16V 150", "TS16-2.0", 186), ("3.0 V6 192", "BUSSO-3.0", 260, {"fin": "1998-12"}),
    ("3.0 V6 24V 220", "BUSSO-3.0-24V", 270, {"debut": "1999-01", "fin": "2002-12"}), ("2.0 JTS 165", "JTS-2.0", 206, {"debut": "2003-01"}),
    ("3.2 V6 240", "BUSSO-3.2-24V", 289, {"debut": "2003-01"})], portes=2, places=2, reservoir=70, remarques="Roadster")
mg(L, "156", "932", "1", "1997-09", "2003-08",
   [("1.6 TS 16V 120", "TS16-1.6", 144), ("1.8 TS 16V 144", "TS16-1.8", 169), ("2.0 TS 16V 155", "TS16-2.0", 187), ("2.5 V6 190", "BUSSO-2.5-24V", 222),
    ("GTA 3.2 V6 250", "BUSSO-3.2-24V", 300, {"debut": "2002-01"}), ("2.0 JTS 165", "JTS-2.0", 206, {"debut": "2002-09"}),
    ("1.9 JTD 105", "JTD-1.9", 255), ("1.9 JTD 115", "JTD-1.9", 275, {"debut": "2000-09"}), ("2.4 JTD 136", "JTD-2.4", 304), ("2.4 JTD 150", "JTD-2.4", 310, {"debut": "2001-01"})],
   portes=4, reservoir=63, remarques="Berline et Sportwagon (2000)")
mg(L, "156", "932", "2", "2003-09", "2007-12",
   [("1.6 TS 16V 120", "TS16-1.6", 146), ("1.8 TS 16V 140", "TS16-1.8", 163), ("2.0 JTS 165", "JTS-2.0", 206), ("GTA 3.2 V6 250", "BUSSO-3.2-24V", 300),
    ("1.9 JTD 115", "JTD-1.9", 275), ("1.9 JTD 140", "JTD-1.9", 305), ("1.9 JTDm 150", "JTD-1.9", 305, {"debut": "2005-01"}),
    ("2.4 JTD 175", "JTD-2.4", 385)], portes=4, reservoir=63, remarques="Restylage Giugiaro ; Crosswagon Q4")
mg(L, "166", "936", "1", "1998-09", "2007-06",
   [("2.0 TS 16V 155", "TS16-2.0", 187, {"fin": "2003-06"}), ("2.5 V6 188", "BUSSO-2.5-24V", 222, {"fin": "2003-06"}), ("3.0 V6 220", "BUSSO-3.0-24V", 265),
    ("3.2 V6 240", "BUSSO-3.2-24V", 289, {"debut": "2003-09"}), ("2.4 JTD 136", "JTD-2.4", 304, {"fin": "2001-06"}), ("2.4 JTD 150", "JTD-2.4", 310, {"debut": "2001-06", "fin": "2003-06"}),
    ("2.4 JTDm 175", "JTD-2.4", 385, {"debut": "2003-09"}), ("2.4 JTDm 185", "JTD-2.4", 385, {"debut": "2005-06"})], portes=4, reservoir=70,
   remarques="Grande berline ; restylage 2003")
mg(L, "147", "937", "1", "2000-10", "2010-03",
   [("1.6 TS 16V 105", "TS16-1.6", 140), ("1.6 TS 16V 120", "TS16-1.6", 146), ("2.0 TS 16V 150", "TS16-2.0", 181), ("GTA 3.2 V6 250", "BUSSO-3.2-24V", 300, {"debut": "2002-09", "fin": "2005-12"}),
    ("1.9 JTD 115", "JTD-1.9", 275), ("1.9 JTD 120", "JTD-1.9", 280, {"debut": "2005-01"}), ("1.9 JTD 150", "JTD-1.9", 305, {"debut": "2005-01"}),
    ("1.9 JTD 170", "JTD-1.9", 330, {"debut": "2006-06"})], reservoir=60, remarques="3 et 5 portes ; restylage 2004")
mg(L, "GT", "937", "1", "2003-09", "2010-12",
   [("1.8 TS 16V 140", "TS16-1.8", 163), ("2.0 JTS 165", "JTS-2.0", 206), ("3.2 V6 240", "BUSSO-3.2-24V", 289), ("1.9 JTD 150", "JTD-1.9", 305),
    ("1.9 JTD 170", "JTD-1.9", 330, {"debut": "2006-06"})], portes=2, places=4, reservoir=63, remarques="Coupé Bertone")
mg(L, "159", "939", "1", "2005-11", "2011-12",
   [("1.8 MPI 140", "MPI-1.8", 175), ("1.75 TBi 200", "TBI-1.75", 320, {"debut": "2009-06"}), ("2.2 JTS 185", "JTS-2.2", 230), ("3.2 JTS V6 260", "JTS-3.2", 322),
    ("1.9 JTDm 120", "JTD-1.9", 280), ("1.9 JTDm 150", "JTD-1.9", 320), ("2.0 JTDm 170", "MJ-2.0", 360, {"debut": "2009-06"}),
    ("2.4 JTDm 200", "MJ-2.4", 400), ("2.4 JTDm 210", "MJ-2.4", 400, {"debut": "2008-06"})], portes=4, reservoir=70, remarques="Berline et Sportwagon ; Q4")
mg(L, "Brera", "939", "1", "2005-09", "2010-12",
   [("1.75 TBi 200", "TBI-1.75", 320, {"debut": "2009-06"}), ("2.2 JTS 185", "JTS-2.2", 230), ("3.2 JTS V6 260", "JTS-3.2", 322),
    ("2.0 JTDm 170", "MJ-2.0", 360, {"debut": "2009-06"}), ("2.4 JTDm 200", "MJ-2.4", 400), ("2.4 JTDm 210", "MJ-2.4", 400, {"debut": "2008-06"})],
   portes=2, places=4, reservoir=70, remarques="Coupé ; Spider (2006) dérivé")
mg(L, "8C Competizione", "8C", "1", "2007-01", "2010-12", [("8C 4.7 V8 450", "F136-4.7", 470)], portes=2, places=2, reservoir=88, remarques="Coupé et Spider (1000 ex.)")

# ---------------------------------------------------------------- années 2010
mg(L, "MiTo", "955", "1", "2008-06", "2013-09",
   [("1.4 78", "FIRE-1.4", 120), ("1.4 TB 120", "TJET-1.4", 206), ("1.4 TB 155", "TJET-1.4", 230, {"fin": "2009-12"}), ("1.4 MultiAir 105", "MULTIAIR-1.4", 130, {"debut": "2009-09"}),
    ("1.4 MultiAir 135", "MULTIAIR-1.4T", 206, {"debut": "2009-09"}), ("QV 1.4 MultiAir 170", "MULTIAIR-1.4T", 250, {"debut": "2009-09"}),
    ("1.3 JTDm 90", "MJ-1.3", 200), ("1.3 JTDm 95", "MJ-1.3", 200, {"debut": "2011-06"}), ("1.6 JTDm 120", "MJ-1.6", 320)], portes=3, reservoir=45)
mg(L, "MiTo", "955", "2", "2013-10", "2018-12",
   [("1.4 78", "FIRE-1.4", 120), ("0.9 TwinAir 85", "TWINAIR-0.9", 145), ("0.9 TwinAir 105", "TWINAIR-0.9", 145), ("1.4 MultiAir 140", "MULTIAIR-1.4T", 230),
    ("QV 1.4 MultiAir 170", "MULTIAIR-1.4T", 250), ("1.3 JTDm 85", "MJ-1.3", 200), ("1.3 JTDm 95", "MJ-1.3", 200)], portes=3, reservoir=45, remarques="Restylage")
mg(L, "Giulietta", "940", "1", "2010-04", "2016-03",
   [("1.4 TB 105", "TJET-1.4", 206), ("1.4 TB 120", "TJET-1.4", 206), ("1.4 MultiAir 170", "MULTIAIR-1.4T", 250), ("QV 1.75 TBi 235", "TBI-1.75", 340),
    ("1.6 JTDm 105", "MJ-1.6", 320), ("2.0 JTDm 140", "MJ-2.0", 350), ("2.0 JTDm 170", "MJ-2.0", 350), ("2.0 JTDm 175", "MJ-2.0", 350, {"debut": "2013-06"})],
   reservoir=60, remarques="Compacte 5 portes")
mg(L, "Giulietta", "940", "2", "2016-04", "2020-12",
   [("1.4 TB 120", "TJET-1.4", 215), ("1.4 MultiAir 150", "MULTIAIR-1.4T", 250), ("Veloce 1.75 TBi 240", "TBI-1.75", 340), ("1.6 JTDm 120", "MJ-1.6", 320),
    ("2.0 JTDm 150", "MJ-2.0", 380), ("Veloce 2.0 JTDm 175", "MJ-2.0", 350)], reservoir=60, remarques="Restylage")
mg(L, "4C", "960", "1", "2013-09", "2020-12", [("4C 1.75 TBi 240", "TBI-1.75", 350)], portes=2, places=2, reservoir=40, remarques="Coupé et Spider (2015), carbone")
mg(L, "Giulia", "952", "1", "2016-04", "2022-12",
   [("2.0 T 200", "GME-2.0T", 330), ("Veloce 2.0 T 280", "GME-2.0T", 400), ("Quadrifoglio 2.9 V6 510", "V6-2.9BT", 600),
    ("GTA 2.9 V6 540", "V6-2.9BT", 600, {"debut": "2020-09", "fin": "2021-12"}), ("2.2 JTDm 136", "JTDM-2.2", 380), ("2.2 JTDm 150", "JTDM-2.2", 450),
    ("2.2 JTDm 160", "JTDM-2.2", 450, {"debut": "2019-01"}), ("2.2 JTDm 180", "JTDM-2.2", 450), ("2.2 JTDm 190", "JTDM-2.2", 450, {"debut": "2019-01"}),
    ("Veloce 2.2 JTDm 210", "JTDM-2.2", 470)], portes=4, reservoir=58, remarques="Plateforme Giorgio ; Q4")
mg(L, "Giulia", "952", "2", "2023-01", None,
   [("2.0 T 280", "GME-2.0T", 400), ("Quadrifoglio 2.9 V6 520", "V6-2.9BT", 600), ("2.2 JTDm 160", "JTDM-2.2", 450), ("2.2 JTDm 210", "JTDM-2.2", 470)],
   portes=4, reservoir=58, remarques="Restylage (phares 3+3) ; prolongée jusqu'à la nouvelle génération (2027)")
mg(L, "Stelvio", "949", "1", "2017-03", "2022-12",
   [("2.0 T 200", "GME-2.0T", 330), ("Veloce 2.0 T 280", "GME-2.0T", 400), ("Quadrifoglio 2.9 V6 510", "V6-2.9BT", 600, {"debut": "2018-01"}),
    ("2.2 JTDm 160", "JTDM-2.2", 450), ("2.2 JTDm 190", "JTDM-2.2", 450), ("Veloce 2.2 JTDm 210", "JTDM-2.2", 470)], reservoir=64, remarques="SUV Giorgio ; Q4")
mg(L, "Stelvio", "949", "2", "2023-01", None,
   [("2.0 T 280", "GME-2.0T", 400), ("Quadrifoglio 2.9 V6 520", "V6-2.9BT", 600), ("2.2 JTDm 160", "JTDM-2.2", 450), ("2.2 JTDm 210", "JTDM-2.2", 470)],
   reservoir=64, remarques="Restylage ; prolongé jusqu'à la nouvelle génération (2027)")

# ---------------------------------------------------------------- gamme actuelle
mg(L, "Tonale", "965", "1", "2022-06", "2025-09",
   [("1.5 Hybrid 130", "FIREFLY-1.5-HYB", 240), ("1.5 Hybrid 160", "FIREFLY-1.5-HYB", 240), ("1.6 JTDm 130", "MJ-1.6", 320),
    ("Plug-in Hybrid Q4 280", "FIREFLY-1.3-PHEV", 270, ph(15, 42, debut="2023-01"))], reservoir=55, remarques="SUV compact")
mg(L, "Tonale", "965", "2", "2025-10", None,
   [("1.5 Hybrid 160", "FIREFLY-1.5-HYB", 240), ("Plug-in Hybrid Q4 280", "FIREFLY-1.3-PHEV", 270, ph(15, 42)), ("1.6 JTDm 130", "MJ-1.6", 320, {"debut": "2026-01"})],
   reservoir=55, remarques="Restylage")
mg(L, "Junior", "STLA-S", "1", "2024-06", None,
   [("Ibrida 136", "EB2-MHEV", 230, {"fin": "2025-06"}), ("Ibrida 145", "EB2-MHEV", 230, {"debut": "2025-07"}), ("Ibrida Q4 145", "EB2-MHEV", 230, {"debut": "2025-03"}),
    ("Elettrica 156", "e-CMP", 260, el(54)), ("Veloce Elettrica 280", "e-CMP", 345, el(54))], reservoir=44,
   remarques="SUV urbain (présenté sous le nom Milano) ; Ibrida 136 ch + boost électrique (145 ch)")
mg(L, "33 Stradale", "33S", "1", "2024-01", "2026-06", [("3.0 V6 Biturbo 620", "V6-3.0TT-33", 720)], portes=2, places=2, reservoir=70,
   remarques="Série limitée (33 ex.), version électrique non reprise ; dates indicatives")

MOT = Motorisations("Alfa Romeo", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Alfa Romeo": L}
MOTEURS = MOT.moteurs()
