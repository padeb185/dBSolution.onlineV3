"""Volkswagen : modèles anciens et intermédiaires (Coccinelle, Transporter T1 à T4, Polo I à III, Passat B1 à B4,
Jetta I/II, Vento, Bora, Jetta V, Scirocco I/II, Corrado, New Beetle, Sharan I) et moteurs liés."""
from . import volkswagen as vw
from ._outil import PREFIXES, Motorisations, famille as f, gamme as g

L = []
# ---------------------------------------------------------------- Coccinelle / Transporter T1-T4
L += g("Coccinelle", "Type 1", "1", "1945-08", "1953-02", ["1.1 25"], portes=2, places=4, reservoir=40,
       remarques="Berline et Cabriolet (Käfer)")
L += g("Coccinelle", "Type 1", "2", "1953-03", "1960-07", ["1.2 30"], portes=2, places=4, reservoir=40)
L += g("Coccinelle", "Type 1", "3", "1960-08", "1966-07", ["1.2 34"], portes=2, places=4, reservoir=40)
L += g("Coccinelle", "Type 1", "4", "1966-08", "1979-12",
       ["1.3 40", ("1.3 44", {"debut": "1970-08"}), "1.5 44", ("1302 1.6 50", {"debut": "1970-08", "fin": "1972-07"}),
        ("1303 1.6 50", {"debut": "1972-08", "fin": "1975-07"})], portes=2, places=4, reservoir=40,
       remarques="1300, 1500, 1302, 1303 ; Cabriolet jusqu'en 1980")
L += g("Coccinelle", "Type 1", "5", "1978-01", "2003-07", ["1.6 44", ("1.6 50", {"debut": "1993-01"})], portes=2, places=4,
       reservoir=40, remarques="Production mexicaine (importations limitées en Europe)")
L += g("Transporter", "T1", "1", "1950-03", "1967-07", ["1.1 25", "1.2 30", ("1.2 34", {"debut": "1959-01"}),
       ("1.5 42", {"debut": "1963-01"})], portes=3, places=8, reservoir=40, remarques="Combi, Fourgon, Pick-up, Samba")
L += g("Transporter", "T2", "1", "1967-08", "1972-07", ["1.6 47", ("1.7 66", {"debut": "1971-08"})], portes=3, places=8,
       reservoir=60, remarques="T2a — Combi, Fourgon, Westfalia")
L += g("Transporter", "T2", "2", "1972-08", "1979-07", ["1.6 50", "1.8 68", ("2.0 70", {"debut": "1975-08"})], portes=3,
       places=8, reservoir=56, remarques="T2b — Combi, Fourgon, Westfalia")
L += g("Transporter", "T3", "1", "1979-05", "1985-08",
       ["1.6 50", "2.0 70", ("1.6 D 50", {"debut": "1981-01"}), ("1.9 60", {"debut": "1982-09"}), ("1.9 78", {"debut": "1982-09"})],
       portes=4, places=8, reservoir=60, remarques="Combi, Caravelle, Multivan, Westfalia")
L += g("Transporter", "T3", "2", "1985-09", "1992-07",
       ["1.9 60", "1.9 78", "2.1 95", "2.1 112", "1.6 TD 70", "1.7 D 57"], portes=4, places=8, reservoir=60,
       remarques="Combi, Caravelle, Multivan, Westfalia ; Syncro")
L += g("Transporter", "T4", "1", "1990-09", "1996-08",
       ["1.8 67", "2.0 84", "2.5 110", "1.9 D 61", "1.9 TD 68", "2.4 D 78", ("2.5 TDI 102", {"debut": "1995-09"})],
       portes=4, places=3, reservoir=80, remarques="Fourgon, Caravelle, Multivan, California")
L += g("Transporter", "T4", "2", "1996-09", "2003-04",
       ["2.0 84", "2.5 115", "VR6 2.8 140", ("VR6 2.8 204", {"debut": "2000-09"}), "1.9 TD 68", "2.4 D 78", "2.5 TDI 88",
        "2.5 TDI 102", ("2.5 TDI 150", {"debut": "1998-09"})], portes=4, places=3, reservoir=80,
       remarques="Fourgon, Caravelle (nez long), Multivan, California")

# ---------------------------------------------------------------- Polo I à III
L += g("Polo", "86", "1", "1975-03", "1981-09", ["0.9 40", "1.1 50", "1.1 60", ("1.3 60", {"debut": "1979-01"})],
       portes=3, places=4, reservoir=36, remarques="Polo I et Derby (berline)")
L += g("Polo", "86C", "1", "1981-10", "1990-08",
       ["1.05 40", "1.3 55", ("1.3 75", {"debut": "1983-01"}), ("G40 1.3 115", {"debut": "1987-01"}), ("1.3 D 45", {"debut": "1986-01"})],
       portes=3, places=4, reservoir=40, remarques="Polo II, Coupé, Classic/Derby")
L += g("Polo", "86C", "2", "1990-09", "1994-09",
       ["1.05 45", "1.3 55", "G40 1.3 115", "1.4 D 48"], portes=3, places=4, reservoir=42,
       remarques="Polo II restylée, Coupé, Classic")
L += g("Polo", "6N", "1", "1994-09", "1999-09",
       ["1.0 45", "1.0 50", "1.3 55", "1.4 60", "1.6 75", "1.4 16v 100", ("GTI 1.6 120", {"debut": "1998-01"}), "1.9 D 64",
        ("1.7 SDI 60", {"debut": "1996-09"}), ("1.9 SDI 64", {"debut": "1996-09"}), ("1.9 TDI 90", {"debut": "1996-09"})],
       reservoir=45, remarques="Polo III 3/5 portes, Classic, Variant")
L += g("Polo", "6N", "2", "1999-10", "2001-10",
       ["1.0 50", "1.4 60", "1.4 16v 75", "1.4 16v 100", "GTI 1.6 125", "1.4 TDI 75", "1.9 SDI 64"], reservoir=45,
       remarques="Polo 6N2 3/5 portes")

# ---------------------------------------------------------------- Passat B1 à B4
L += g("Passat", "B1", "1", "1973-05", "1980-08",
       ["1.3 55", "1.3 60", "1.5 75", "1.5 85", ("1.6 75", {"debut": "1975-08"}), ("1.6 85", {"debut": "1975-08"}),
        ("GLI 1.6 110", {"debut": "1977-01"}), ("1.5 D 50", {"debut": "1978-01"})], portes=4, reservoir=45,
       remarques="Berline 2/4 portes, 3/5 portes, Variant")
L += g("Passat", "B2", "1", "1980-09", "1988-03",
       ["1.3 60", "1.6 75", "1.8 90", "1.9 115", ("2.2 136", {"debut": "1984-01"}), "1.6 D 54", "1.6 TD 70"],
       portes=4, reservoir=60, remarques="Passat, Santana (berline), Variant ; restylage 1985 non détaillé")
L += g("Passat", "B3", "1", "1988-04", "1993-09",
       ["1.6 72", "1.8 90", "1.8 16v 136", "G60 1.8 160", "2.0 16v 136", ("VR6 2.8 174", {"debut": "1991-09"}),
        "1.6 TD 80", "1.9 D 68", ("1.9 TD 75", {"debut": "1991-09"}), ("1.9 TDI 90", {"debut": "1991-09"})],
       portes=4, reservoir=70, remarques="Berline et Variant")
L += g("Passat", "B4", "1", "1993-10", "1996-10",
       ["1.6 75", "1.8 75", "1.8 90", "2.0 115", "2.0 16v 150", "VR6 2.8 174", "1.9 D 64", "1.9 TD 75", "1.9 TDI 90",
        ("1.9 TDI 110", {"debut": "1995-09"})], portes=4, reservoir=70, remarques="Berline et Variant")

# ---------------------------------------------------------------- Jetta / Vento / Bora
L += g("Jetta", "A1", "1", "1979-08", "1984-01", ["1.1 50", "1.3 60", "1.5 70", "1.6 75", "GLI 1.6 110", "1.6 D 54"],
       portes=4, reservoir=40, remarques="Jetta I — berline 2/4 portes")
L += g("Jetta", "A2", "1", "1984-02", "1992-01",
       ["1.3 55", "1.6 72", "1.8 90", "GT 1.8 112", ("GT 16v 1.8 139", {"debut": "1987-01"}), "1.6 D 54", "1.6 TD 70"],
       portes=4, reservoir=55, remarques="Jetta II — berline 2/4 portes")
L += g("Vento", "1H2", "1", "1992-01", "1998-08",
       ["1.4 60", "1.6 75", "1.8 75", "1.8 90", "2.0 115", "VR6 2.8 174", "1.9 D 64", "1.9 TD 75", "1.9 TDI 90",
        ("1.9 TDI 110", {"debut": "1996-09"})], portes=4, reservoir=55, remarques="Berline 4 portes (Golf III)")
L += g("Bora", "1J2", "1", "1998-10", "2005-06",
       ["1.4 16v 75", "1.6 100", "1.6 105", ("1.6 FSI 110", {"debut": "2002-01"}), "1.8T 150", "2.0 115", "2.3 V5 150",
        ("2.3 V5 170", {"debut": "2000-10"}), "1.9 SDI 68", "1.9 TDI 90", "1.9 TDI 100", "1.9 TDI 110", "1.9 TDI 115",
        "1.9 TDI 130", ("1.9 TDI 150", {"debut": "2000-10"})], portes=4, reservoir=55,
       remarques="Berline 4 portes et Variant (Golf IV)")
L += g("Jetta", "1K2", "1", "2005-08", "2010-10",
       ["1.6 102", "1.6 FSI 115", "1.4 TSI 122", "1.4 TSI 140", "1.4 TSI 170", "2.0 FSI 150", "2.0 TFSI 200",
        "1.9 TDI 105", "2.0 TDI 140", "2.0 TDI 170"], portes=4, reservoir=55, remarques="Jetta V — berline 4 portes (Golf V)")

# ---------------------------------------------------------------- Scirocco I/II, Corrado, New Beetle, Sharan I
L += g("Scirocco", "53", "1", "1974-03", "1981-03",
       ["1.1 50", "1.5 70", "1.5 85", ("1.6 75", {"debut": "1975-08"}), ("1.6 85", {"debut": "1975-08"}),
        ("GTI 1.6 110", {"debut": "1976-08"})], portes=3, places=4, reservoir=40, remarques="Scirocco I — coupé")
L += g("Scirocco", "53B", "1", "1981-04", "1992-09",
       ["1.3 60", "1.6 75", "1.6 85", "1.8 90", "GTI 1.8 112", ("GT 16v 1.8 139", {"debut": "1985-09"})], portes=3, places=4,
       reservoir=40, remarques="Scirocco II — coupé")
L += g("Corrado", "50", "1", "1988-09", "1995-07",
       ["G60 1.8 160", "16v 1.8 136", ("2.0 115", {"debut": "1993-01"}), ("2.0 16v 136", {"debut": "1992-09"}),
        ("VR6 2.8 174", {"debut": "1991-09"}), ("VR6 2.9 190", {"debut": "1992-01"})], portes=3, places=4, reservoir=55,
       remarques="Coupé")
L += g("New Beetle", "9C", "1", "1997-10", "2005-04",
       ["1.4 75", "1.6 102", "2.0 115", "1.8T 150", ("2.3 V5 170", {"debut": "2000-09"}), ("RSi 3.2 225", {"debut": "2001-10", "fin": "2003-12"}),
        "1.9 TDI 90", "1.9 TDI 100", ("1.9 TDI 105", {"debut": "2003-01"})], portes=3, places=4, reservoir=55,
       remarques="Coupé 3 portes et Cabriolet (2003)")
L += g("New Beetle", "9C", "2", "2005-05", "2010-07",
       ["1.4 75", "1.6 102", "2.0 115", "1.8T 150", "1.9 TDI 105"], portes=3, places=4, reservoir=55,
       remarques="Coupé 3 portes et Cabriolet")
L += g("Sharan", "7M", "1", "1995-05", "2000-04",
       ["2.0 115", ("1.8T 150", {"debut": "1997-09"}), "2.8 VR6 174", "1.9 TDI 90", "1.9 TDI 110"], places=7, reservoir=70,
       remarques="Monospace 5 à 7 places (jumeau Ford Galaxy / Seat Alhambra)")
L += g("Sharan", "7M", "2", "2000-05", "2010-03",
       ["2.0 115", "1.8T 150", "2.8 VR6 204", "1.9 TDI 115", "1.9 TDI 130", ("2.0 TDI 140", {"debut": "2005-09"})],
       places=7, reservoir=70, remarques="Monospace 5 à 7 places ; restylage 2004 non détaillé")

# ---------------------------------------------------------------- Moteurs
D, E_ = "DSL", "ESS"
FAMILLES = dict(vw.FAMILLES, **{
    "BOXER-1.1": f("ATM", E_, 1.1, "NC", 4, 3300, 2000, "20W50", 2.5, 5000, a="PLAT"),
    "BOXER-1.2": f("ATM", E_, 1.2, "NC", 4, 3600, 2000, "20W50", 2.5, 5000, a="PLAT"),
    "BOXER-1.3": f("ATM", E_, 1.3, "NC", 4, 4000, 2600, "20W50", 2.5, 5000, a="PLAT"),
    "BOXER-1.5": f("ATM", E_, 1.5, "NC", 4, 4000, 2600, "20W50", 2.5, 5000, a="PLAT"),
    "BOXER-1.6": f("ATM", E_, 1.6, "NC", 4, 4000, 2800, "20W50", 2.5, 5000, a="PLAT"),
    "TYPE4-1.7": f("ATM", E_, 1.7, "NC", 4, 4800, 3200, "20W50", 3.5, 5000, a="PLAT"),
    "TYPE4-1.8": f("ATM", E_, 1.8, "NC", 4, 4200, 3000, "20W50", 3.5, 5000, a="PLAT"),
    "TYPE4-2.0": f("ATM", E_, 2.0, "NC", 4, 4200, 3000, "20W50", 3.5, 5000, a="PLAT"),
    "WBX-1.9": f("ATM", E_, 1.9, "NC", 4, 4600, 2600, "15W40", 4.0, 7500, a="PLAT"),
    "WBX-2.1": f("ATM", E_, 2.1, "NC", 4, 4800, 2800, "15W40", 4.0, 7500, a="PLAT"),
    "EA111-0.9": f("ATM", E_, 0.9, "COURROIE", 4, 5900, 3500, "15W40", 3.0, 7500),
    "EA111-1.05": f("ATM", E_, 1.05, "COURROIE", 4, 5300, 3000, "15W40", 3.0, 7500),
    "EA111-1.3G40": f("TURBO", E_, 1.3, "COURROIE", 4, 6000, 3600, "15W40", 3.5, 7500),
    "EA827-1.3": f("ATM", E_, 1.3, "COURROIE", 4, 5600, 3500, "15W40", 3.5, 7500),
    "EA827-1.7D": f("ATM", D, 1.7, "COURROIE", 4, 4500, 2800, "15W40", 4.0, 7500),
    "EA827-1.3D": f("ATM", D, 1.3, "COURROIE", 4, 4800, 2800, "15W40", 3.5, 7500),
    "EA827-1.4D": f("ATM", D, 1.4, "COURROIE", 4, 4800, 2800, "15W40", 3.5, 7500),
    "R5-1.9": f("ATM", E_, 1.9, "COURROIE", 5, 5600, 3200, "15W40", 4.5, 7500),
    "R5-2.2": f("ATM", E_, 2.2, "COURROIE", 5, 5700, 3500, "15W40", 4.5, 7500),
    "R5-2.5": f("ATM", E_, 2.5, "COURROIE", 5, 4500, 2200, "15W40", 6.0, 15000),
    "R5-2.4D": f("ATM", D, 2.4, "COURROIE", 5, 3700, 1800, "15W40", 6.0, 7500),
})
TABLE = dict(vw.TABLE, **{
    "1.1 25": ("BOXER-1.1", 25, 67), "1.2 30": ("BOXER-1.2", 30, 76), "1.2 34": ("BOXER-1.2", 34, 82),
    "1.3 40": ("BOXER-1.3", 40, 89), "1.3 44": ("BOXER-1.3", 44, 86), "1.5 44": ("BOXER-1.5", 44, 102),
    "1.5 42": ("BOXER-1.5", 42, 102), "1302 1.6 50": ("BOXER-1.6", 50, 106), "1303 1.6 50": ("BOXER-1.6", 50, 106),
    "1.6 44": ("BOXER-1.6", 44, 98), "1.6 50": ("BOXER-1.6", 50, 106), "1.6 47": ("BOXER-1.6", 47, 103),
    "1.7 66": ("TYPE4-1.7", 66, 113), "1.8 68": ("TYPE4-1.8", 68, 127), "2.0 70": ("TYPE4-2.0", 70, 140),
    "1.9 60": ("WBX-1.9", 60, 125), "1.9 78": ("WBX-1.9", 78, 141), "2.1 95": ("WBX-2.1", 95, 160),
    "2.1 112": ("WBX-2.1", 112, 174), "1.6 D 50": ("EA827-1.6D", 50, 103), "1.7 D 57": ("EA827-1.7D", 57, 103),
    "1.8 67": ("EA827-1.8-8v", 67, 140), "2.0 84": ("EA827-2.0", 84, 159), "2.5 110": ("R5-2.5", 110, 190),
    "2.5 115": ("R5-2.5", 115, 200), "VR6 2.8 140": ("VR6-2.8", 140, 240), "VR6 2.8 204": ("VR6-2.8", 204, 265),
    "1.9 D 61": ("EA827-1.9D", 61, 127), "1.9 TD 68": ("EA827-1.9TD", 68, 140), "2.4 D 78": ("R5-2.4D", 78, 164),
    "2.5 TDI 88": ("R5-2.5TDI", 88, 195), "2.5 TDI 102": ("R5-2.5TDI", 102, 250), "2.5 TDI 150": ("R5-2.5TDI", 150, 295),
    "0.9 40": ("EA111-0.9", 40, 61), "1.1 60": ("EA111-1.1", 60, 83), "1.05 40": ("EA111-1.05", 40, 74),
    "1.05 45": ("EA111-1.05", 45, 76), "1.3 75": ("EA111-1.3", 75, 100), "G40 1.3 115": ("EA111-1.3G40", 115, 148),
    "1.3 D 45": ("EA827-1.3D", 45, 76), "1.4 D 48": ("EA827-1.4D", 48, 82), "1.0 45": ("EA111-1.0", 45, 74),
    "1.6 120": ("EA111-1.6", 120, 148), "1.3 55@OLD": ("EA827-1.3", 55, 96), "1.3 60@OLD": ("EA827-1.3", 60, 100),
    "1.5 75": ("EA827-1.5", 75, 118), "1.5 85": ("EA827-1.5", 85, 121), "1.6 85": ("EA827-1.6", 85, 127),
    "1.9 115": ("Audi", "R5-1.9", 115, 154), "2.2 136": ("Audi", "R5-2.2", 136, 186),
    "1.8 16v 136": ("EA827-1.8-16v", 136, 162), "16v 1.8 136": ("EA827-1.8-16v", 136, 162),
    "2.0 16v 136": ("EA827-2.0-16v", 136, 180), "1.9 D 68": ("EA827-1.9D", 68, 127), "VR6 2.8 174@P": ("VR6-2.8", 174, 235),
    "2.8 VR6 174": ("VR6-2.8", 174, 235), "2.8 VR6 204": ("VR6-2.8", 204, 265), "RSi 3.2 225": ("VR6-3.2", 225, 320),
    "1.9 D 64": ("EA827-1.9D", 64, 124),
})
ERES = {"B1": "OLD", "B2": "OLD", "A1": "OLD", "53": "OLD", "53B": "OLD", "1K2": "A", "7M": "A"}

MOT = Motorisations("Volkswagen", FAMILLES, TABLE, ERES, prefixes=PREFIXES + ("GLI ",))
MOT.lier(L)

DETAIL = {"Volkswagen": L}
MOTEURS = MOT.moteurs()
