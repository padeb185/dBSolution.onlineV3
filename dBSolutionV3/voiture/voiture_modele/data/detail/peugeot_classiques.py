"""Peugeot : modèles anciens et intermédiaires (201 à 1007, 4007/4008, RCZ, iOn, Bipper).
Moteurs PSA partagés avec Peugeot / Citroën (motoriste « Peugeot »)."""
from . import citroen
from ._outil import PREFIXES, Motorisations, electrique, famille as f, gamme as g


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


L = []
L += g("201", "201", "1", "1929-10", "1931-12", ["1.1 23"], portes=4, reservoir=30,
       remarques="Berline, Torpédo, Coupé, Cabriolet, utilitaires")
L += g("201", "201", "2", "1932-01", "1937-12", ["1.1 23", ("1.3 28", {"debut": "1932-10"})], portes=4, reservoir=30,
       remarques="201 C / 201 D / 201 M ; suspension avant à roues indépendantes (1931)")
L += g("202", "202", "1", "1938-02", "1942-06", ["1.1 30"], portes=4, reservoir=35,
       remarques="Berline, Découvrable, Cabriolet, Commerciale")
L += g("202", "202", "2", "1945-01", "1949-08", ["1.1 30"], portes=4, reservoir=35,
       remarques="Production reprise après-guerre ; utilitaire 202 U")
L += g("203", "203", "1", "1948-10", "1954-09", ["1.3 42"], portes=4, reservoir=40,
       remarques="Berline, Familiale, Commerciale, Cabriolet, Coupé")
L += g("203", "203", "2", "1954-10", "1960-02", ["1.3 45"], portes=4, reservoir=40,
       remarques="203 C ; Berline, Familiale, Commerciale")
L += g("204", "204", "1", "1965-04", "1969-08", ["1.1 53", ("1.3 D 40", {"debut": "1968-09"})], portes=4, reservoir=42,
       remarques="Berline, Break, Coupé, Cabriolet")
L += g("204", "204", "2", "1969-09", "1976-07", ["1.1 58", "1.3 D 45"], portes=4, reservoir=42,
       remarques="Berline et Break ; Coupé et Cabriolet jusqu'en 1970")
L += g("104", "104", "1", "1972-10", "1988-06",
       ["954 46", "1.1 57", ("1.1 50", {"debut": "1976-01"}), ("1.4 ZS 80", {"debut": "1979-01", "fin": "1983-12"})],
       reservoir=40, remarques="Berline 4/5 portes et Coupé")
L += g("304", "304", "1", "1969-09", "1980-10", ["1.3 65", ("1.3 S 75", {"debut": "1972-01"})], portes=4, reservoir=45,
       remarques="Berline, Break, Coupé, Cabriolet")
L += g("305", "581", "1", "1977-11", "1982-08", ["1.3 65", "1.5 74", "1.5 85", ("1.5 D 49", {"debut": "1980-01"})],
       portes=4, reservoir=50, remarques="Berline et Break (1980)")
L += g("305", "581", "2", "1982-09", "1989-12", ["1.5 74", "1.6 94", "1.9 105", "1.9 D 65"], portes=4, reservoir=50,
       remarques="Berline et Break ; GTX 1.9")
L += g("505", "551A", "1", "1979-05", "1992-12",
       ["2.0 96", "2.0 110", "GTi 2.2 130", ("Turbo Injection 2.2 160", {"debut": "1983-09"}),
        ("Turbo Injection 2.2 200", {"debut": "1986-09", "fin": "1988-12"}), "2.5 D 76", ("2.5 TD 110", {"debut": "1984-09"})],
       portes=4, reservoir=70, remarques="Berline, Break, Familiale 8 places ; restylage 1986 non détaillé")
L += g("309", "10C", "1", "1985-09", "1989-07",
       ["1.1 55", "1.3 64", "1.6 80", "1.6 92", ("GTI 1.9 130", {"debut": "1987-01"}), "1.8 D 60", "1.9 D 65"],
       reservoir=55, remarques="3 et 5 portes")
L += g("309", "10C", "2", "1989-08", "1993-12",
       ["1.1 60", "1.4 75", "1.6 88", "1.9 122", "GTI 1.9 130", "GTI 16 1.9 160", "1.9 D 65", ("1.8 TD 90", {"debut": "1991-01"})],
       reservoir=55, remarques="3 et 5 portes")
L += g("405", "15B", "1", "1987-07", "1992-07",
       ["1.4 70", "1.6 92", "1.9 110", "Mi16 1.9 160", "1.9 D 70", ("1.8 TD 90", {"debut": "1988-09"})],
       portes=4, reservoir=70, remarques="Berline et Break (1988) ; Mi16 x4")
L += g("405", "15B", "2", "1992-08", "1997-12",
       ["1.6 90", "1.8 103", "2.0 123", "2.0 16v 155", ("T16 2.0 Turbo 200", {"debut": "1993-01", "fin": "1995-12"}), "1.9 D 70",
        "1.9 TD 90"], portes=4, reservoir=70, remarques="Berline et Break")
L += g("605", "Z6", "1", "1989-09", "1994-08",
       ["2.0 122", "2.0 Turbo 147", "3.0 V6 170", ("3.0 V6 24v 200", {"debut": "1990-09"}), "2.1 TD 110",
        ("2.5 TD 129", {"debut": "1994-01"})], portes=4, reservoir=80)
L += g("605", "Z6", "2", "1994-09", "1999-09", ["2.0 16v 135", "2.0 Turbo 147", "3.0 V6 190", "2.1 TD 110", "2.5 TD 129"],
       portes=4, reservoir=80)
L += g("106", "S1", "1", "1991-09", "1996-04",
       ["1.0 45", "1.1 60", "1.4 75", "XSi 1.4 100", ("Rallye 1.3 100", {"debut": "1993-09"}), "1.5 D 57"],
       reservoir=45, remarques="3 et 5 portes")
L += g("106", "S2", "2", "1996-05", "2003-12",
       ["1.0 50", "1.1 60", "1.4 75", "1.6 90", "GTi 1.6 16v 120", ("Rallye 1.6 103", {"fin": "1998-12"}), "1.5 D 57"],
       reservoir=45, remarques="3 et 5 portes ; 106 électrique (1995-2003)")
L += g("306", "N3", "1", "1993-03", "1997-03",
       ["1.1 60", "1.4 75", "1.6 89", "1.8 101", "2.0 123", "S16 2.0 16v 150", ("S16 2.0 16v 155", {"debut": "1996-01"}),
        "1.9 D 68", "1.9 TD 90"], reservoir=60, remarques="3 et 5 portes, berline, Cabriolet (1994), Break (1997)")
L += g("306", "N3", "2", "1997-04", "2002-08",
       ["1.4 75", "1.6 90", "1.8 16v 110", "2.0 16v 132", "2.0 16v 135", "GTi-6 2.0 16v 167", "1.9 D 70", "2.0 HDi 90"],
       reservoir=60, remarques="3 et 5 portes, berline, Break, Cabriolet")
L += g("806", "U6", "1", "1994-06", "2002-07",
       ["1.8 99", "2.0 123", "2.0 16v 132", "2.0 Turbo 147", "1.9 TD 90", "2.1 TD 110", ("2.0 HDi 109", {"debut": "1999-09"})],
       places=7, reservoir=80, remarques="Monospace 5 à 8 places")
L += g("406", "D8", "1", "1995-11", "1999-04",
       ["1.6 90", "1.8 101", "1.8 16v 110", "2.0 16v 135", "2.0 Turbo 147", ("3.0 V6 190", {"debut": "1996-09"}),
        "1.9 TD 90", "2.1 TD 110", ("2.0 HDi 90", {"debut": "1998-09"}), ("2.0 HDi 110", {"debut": "1998-09"})],
       portes=4, reservoir=70, remarques="Berline, Break (1996), Coupé (1997)")
L += g("406", "D8", "2", "1999-05", "2004-12",
       ["1.8 16v 117", "2.0 16v 136", "2.2 16v 158", "3.0 V6 207", ("3.0 V6 210", {"debut": "2000-09"}), "2.0 HDi 90",
        "2.0 HDi 110", "2.2 HDi 133"], portes=4, reservoir=70, remarques="Berline, Break, Coupé")
L += g("607", "9D", "1", "2000-01", "2004-12",
       ["2.2 16v 158", "3.0 V6 207", "3.0 V6 210", "2.0 HDi 107", "2.2 HDi 133"], portes=4, reservoir=80)
L += g("607", "9D", "2", "2005-01", "2010-12", ["2.2 16v 158", "3.0 V6 211", "2.2 HDi 170", "2.7 HDi V6 204"], portes=4,
       reservoir=80)
L += g("307", "T5", "1", "2001-04", "2005-05",
       ["1.4 75", "1.4 16v 90", "1.6 16v 110", "2.0 16v 136", "2.0 16v 138", ("2.0 16v 177", {"debut": "2003-09"}),
        "1.4 HDi 68", "1.6 HDi 90", "1.6 HDi 110", "2.0 HDi 90", "2.0 HDi 107", "2.0 HDi 136"],
       reservoir=60, remarques="3/5 portes, Break et SW (2002), CC (2003)")
L += g("307", "T6", "2", "2005-06", "2008-12",
       ["1.4 16v 90", "1.6 16v 110", "2.0 16v 140", "2.0 16v 177", "1.6 HDi 90", "1.6 HDi 110", "2.0 HDi 136"],
       reservoir=60, remarques="3/5 portes, Break, SW, CC (jusqu'en 2009)")
L += g("807", "EB", "1", "2002-07", "2014-06",
       ["2.0 16v 136", "2.0 16v 143", "2.2 16v 158", "3.0 V6 204", "2.0 HDi 109", "2.0 HDi 120", "2.0 HDi 136",
        "2.0 HDi 163", "2.2 HDi 128", "2.2 HDi 170"], places=7, reservoir=80,
       remarques="Monospace 5 à 8 places ; restylage 2008 non détaillé")
L += g("407", "6D", "1", "2004-05", "2008-09",
       ["1.8 16v 117", "2.0 16v 136", "2.2 16v 158", "3.0 V6 211", "1.6 HDi 110", "2.0 HDi 136", "2.2 HDi 170",
        ("2.7 HDi V6 204", {"debut": "2005-09"})], portes=4, reservoir=66, remarques="Berline, SW, Coupé (2005)")
L += g("407", "6D", "2", "2008-10", "2011-12",
       ["1.8 16v 125", "2.0 16v 140", "2.2 16v 163", "3.0 V6 211", "1.6 HDi 110", "2.0 HDi 140", "2.0 HDi 163",
        "2.2 HDi 170", "2.7 HDi V6 204", "3.0 HDi V6 240"], portes=4, reservoir=66, remarques="Berline, SW, Coupé")
L += g("1007", "KM", "1", "2005-04", "2009-12", ["1.4 75", "1.4 16v 90", "1.6 16v 110", "1.4 HDi 68", "1.6 HDi 110"],
       portes=3, places=4, reservoir=40, remarques="Portes latérales coulissantes électriques")
L += g("4007", "4007", "1", "2007-07", "2012-12", ["2.2 HDi 156", "2.4 16v 170"], places=7, reservoir=60,
       remarques="SUV 5 ou 7 places, base Mitsubishi Outlander")
L += g("4008", "4008", "1", "2012-05", "2017-12", ["1.6 117", "1.6 HDi 115", "1.8 HDi 150"], reservoir=60,
       remarques="SUV, base Mitsubishi ASX")
L += g("RCZ", "T75", "1", "2010-04", "2013-03", ["1.6 THP 156", "1.6 THP 200", "2.0 HDi 163"], portes=2, places=4,
       reservoir=55, remarques="Coupé")
L += g("RCZ", "T75", "2", "2013-04", "2015-09", ["1.6 THP 156", "1.6 THP 200", ("R 1.6 THP 270", {"debut": "2013-11"}),
       "2.0 HDi 163"], portes=2, places=4, reservoir=55, remarques="Coupé")
L += g("iOn", "iOn", "1", "2010-12", "2020-12", [("Électrique 67", el(16))], places=4, reservoir=0,
       remarques="Citadine électrique, base Mitsubishi i-MiEV")
L += g("Bipper", "AA", "1", "2008-01", "2017-12", ["1.4 73", "1.3 HDi 75", ("1.3 HDi 80", {"debut": "2010-01"})],
       places=2, reservoir=45, remarques="Fourgonnette et Tepee, base Fiat Fiorino")

# ---------------------------------------------------------------- Moteurs
FAMILLES = dict(citroen.FAMILLES, **{
    "PEU-201-1.1": f("ATM", "ESS", 1.1, "NC", 4, 3500, 2000, "20W50", 4.0, 3000),
    "PEU-201-1.3": f("ATM", "ESS", 1.3, "NC", 4, 3500, 2000, "20W50", 4.0, 3000),
    "PEU-202": f("ATM", "ESS", 1.1, "NC", 4, 4000, 2500, "20W50", 4.0, 3000),
    "PEU-203": f("ATM", "ESS", 1.3, "NC", 4, 4500, 2500, "20W50", 4.0, 3000),
    "XK": f("ATM", "ESS", 1.1, "CHAINE", 4, 5800, 3500, "20W50", 3.5, 5000),
    "XL4D": f("ATM", "DSL", 1.3, "CHAINE", 4, 5000, 3000, "20W50", 4.0, 5000),
    "XL3": f("ATM", "ESS", 1.3, "CHAINE", 4, 6000, 3750, "15W40", 4.0, 7500),
    "XR5": f("ATM", "ESS", 1.5, "CHAINE", 4, 6000, 3000, "15W40", 4.0, 7500),
    "XID": f("ATM", "DSL", 1.5, "CHAINE", 4, 5000, 2500, "15W40", 4.0, 7500),
    "POISSY-1.1": f("ATM", "ESS", 1.1, "CHAINE", 4, 5800, 3000, "15W40", 3.5, 7500),
    "POISSY-1.3": f("ATM", "ESS", 1.3, "CHAINE", 4, 5800, 3200, "15W40", 3.5, 7500),
    "TU2J2": f("ATM", "ESS", 1.3, "COURROIE", 4, 7200, 5400, "10W40", 3.2, 10000),
    "XU10J4TE": f("TURBO", "ESS", 2.0, "COURROIE", 4, 5000, 2600, "10W40", 5.0, 10000),
    "XN1": f("ATM", "ESS", 2.0, "CHAINE", 4, 5200, 3000, "15W40", 4.5, 7500),
    "ZEJ": f("ATM", "ESS", 2.2, "CHAINE", 4, 5750, 3500, "15W40", 4.5, 7500),
    "N9TE": f("TURBO", "ESS", 2.2, "CHAINE", 4, 5200, 3000, "15W40", 4.5, 7500),
    "XD3": f("ATM", "DSL", 2.5, "CHAINE", 4, 4500, 2000, "15W40", 5.5, 7500),
    "XD3T": f("TURBO", "DSL", 2.5, "CHAINE", 4, 4150, 2000, "15W40", 5.5, 7500),
    "4A92": f("ATM", "ESS", 1.6, "CHAINE", 4, 6000, 4000, "5W30", 4.2, 15000),
    "4N13": f("TURBO", "DSL", 1.8, "CHAINE", 4, 4000, 2000, "5W30", 4.9, 15000),
})
TABLE = dict(citroen.TABLE, **{
    "1.1 23": ("PEU-201-1.1", 23, 60), "1.3 28": ("PEU-201-1.3", 28, 75), "1.1 30": ("PEU-202", 30, 72),
    "1.3 42": ("PEU-203", 42, 80), "1.3 45": ("PEU-203", 45, 83), "1.1 53": ("XK", 53, 82), "1.1 58": ("XK", 58, 88),
    "1.3 D 40": ("XL4D", 40, 72), "1.3 D 45": ("XL4D", 45, 75),
    "954 46": ("XV8", 46, 66), "1.1 57": ("XW7", 57, 85), "1.4 ZS 80": ("XY", 80, 112),
    "1.3 65": ("XL3", 65, 98), "1.3 S 75": ("XL3", 75, 99), "1.5 74": ("XR5", 74, 117), "1.5 85": ("XR5", 85, 119),
    "1.5 D 49": ("XID", 49, 87), "1.9 D 65": ("XUD9", 65, 120),
    "2.0 96": ("XN1", 96, 162), "2.0 110": ("XN1", 110, 170), "2.2 130": ("ZEJ", 130, 184),
    "Turbo Injection 2.2 160": ("N9TE", 160, 235), "Turbo Injection 2.2 200": ("N9TE", 200, 290),
    "2.5 D 76": ("XD3", 76, 150), "2.5 TD 110": ("XD3T", 110, 235),
    "1.1 55": ("POISSY-1.1", 55, 86), "1.3 64": ("POISSY-1.3", 64, 102), "1.6 80": ("XU5J", 80, 132),
    "1.6 92": ("XU5J", 92, 135), "1.9 130": ("XU9J", 130, 161), "GTI 16 1.9 160": ("XU9J4", 160, 180),
    "1.4 70": ("TU3", 70, 110), "1.9 110": ("XU9J", 110, 162), "Mi16 1.9 160": ("XU9J4", 160, 180),
    "T16 2.0 Turbo 200": ("XU10J4TE", 200, 288), "2.0 Turbo 147": ("XU10J2TE", 147, 235),
    "2.5 TD 129": ("DK5ATE", 129, 285),
    "1.0 45": ("TU9", 45, 72), "XSi 1.4 100": ("TU3", 100, 120), "Rallye 1.3 100": ("TU2J2", 100, 112),
    "Rallye 1.6 103": ("TU5", 103, 135), "1.6 16v 120": ("TU5J4", 120, 145),
    "1.6 89": ("XU5J", 89, 135), "1.8 101": ("XU7", 101, 153), "S16 2.0 16v 150": ("XU10J4", 150, 180),
    "S16 2.0 16v 155": ("XU10J4", 155, 183), "GTi-6 2.0 16v 167": ("XU10J4", 167, 193),
    "2.0 HDi 107": ("DW10ATED", 107, 250), "2.0 16v 177": ("EW10J4S", 177, 202), "2.2 16v 163": ("EW12J4", 163, 220),
    "1.6 117": ("Mitsubishi", "4A92", 117, 154), "1.6 HDi 115": ("DV6C", 115, 270),
    "1.8 HDi 150": ("Mitsubishi", "4N13", 150, 300), "R 1.6 THP 270": ("EP6FDTR", 270, 330),
})
TABLE = {k: v for k, v in TABLE.items() if not (len(v) == 4 and v[0] == "Citroën")}  # pas de moteurs Citroën d'avant PSA

ERES = {"15B": "XU", "Z6": "XU", "U6": "XU", ("N3", "1"): "XU", ("D8", "1"): "XU", "10C": "XU", "581": "XU", "S1": "TU"}
MOT = Motorisations("Peugeot", FAMILLES, TABLE, ERES, prefixes=PREFIXES + ("GTI ", "XSi "))
MOT.lier(L)

DETAIL = {"Peugeot": L}
MOTEURS = MOT.moteurs()
