"""Citroën : générations, phases, motorisations (marché européen). Moteurs PSA partagés avec Peugeot."""
from . import peugeot as psa
from ._outil import PREFIXES, Motorisations, electrique, famille as f, gamme as g


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


L = []

# ---------------------------------------------------------------- Classiques
L += g("Traction Avant", "11", "1", "1934-04", "1957-07",
       [("7 CV 1.6 36", {"fin": "1941-12"}), "11 CV 1.9 46", ("11 CV 1.9 56", {"debut": "1953-01"}),
        ("15-Six 2.9 77", {"debut": "1938-06", "fin": "1955-12"})], portes=4, reservoir=50,
       remarques="Berline 7, 11 et 15 CV, Familiale, Commerciale")
L += g("2CV", "2CV", "1", "1948-10", "1960-12", ["375 9", ("425 12", {"debut": "1954-10"})], portes=4, places=4,
       reservoir=20, remarques="Berline et fourgonnette AU/AZU")
L += g("2CV", "2CV", "2", "1961-01", "1970-02", ["425 18"], portes=4, places=4, reservoir=20,
       remarques="2CV AZ / AZAM, fourgonnette AZU")
L += g("2CV", "2CV", "3", "1970-03", "1990-07", ["2CV4 435 24", "2CV6 602 29"], portes=4, places=4, reservoir=20,
       remarques="2CV4 et 2CV6 (Charleston, Spécial, Dolly), fourgonnette AK")
L += g("Dyane", "AY", "1", "1967-08", "1984-12", [("425 21", {"fin": "1968-12"}), "Dyane 4 435 26", "Dyane 6 602 32"],
       places=4, reservoir=25)
L += g("Méhari", "AY-CA", "1", "1968-05", "1987-12", ["602 29"], portes=0, places=4, reservoir=25,
       remarques="Carrosserie ABS sans portes ; Méhari 4x4 (1979-1983)")
L += g("Ami", "AM6", "1", "1961-04", "1969-03", ["602 22", ("602 25", {"debut": "1964-01"})], portes=4, places=4,
       reservoir=25, remarques="Ami 6 berline et Break")
L += g("Ami", "AM8", "1", "1969-03", "1978-12", ["602 32", ("Super 1.0 54", {"debut": "1973-01", "fin": "1976-12"})],
       portes=4, places=4, reservoir=25, remarques="Ami 8 berline et Break ; Ami Super à moteur GS")
L += g("DS", "DS", "1", "1955-10", "1967-08",
       ["DS19 1.9 75", ("ID19 1.9 66", {"debut": "1957-05"}), ("DS19 1.9 83", {"debut": "1961-01"}),
        ("DS21 2.2 109", {"debut": "1965-09"})], portes=4, reservoir=65, remarques="DS / ID berline, Break, Cabriolet")
L += g("DS", "DS", "2", "1967-09", "1975-04",
       ["ID19 1.9 66", "DS20 2.0 91", ("DS20 2.0 103", {"debut": "1969-09"}), "DS21 2.2 109",
        ("DS21 2.2 125", {"debut": "1969-09"}), ("DS23 2.3 115", {"debut": "1972-09"}), ("DS23 2.3 130", {"debut": "1972-09"})],
       portes=4, reservoir=65, remarques="Phares directionnels ; berline, Break")
L += g("SM", "S", "1", "1970-03", "1975-07", ["2.7 V6 170", ("2.7 V6 178", {"debut": "1972-07"}),
       ("3.0 V6 180", {"debut": "1973-01"})], portes=2, places=4, reservoir=90, remarques="Coupé à moteur Maserati")
L += g("GS", "G", "1", "1970-10", "1979-08", ["1.0 55", ("1.2 60", {"debut": "1972-09"}), ("1.1 57", {"debut": "1976-09"}),
       ("1.2 65", {"debut": "1977-01"})], portes=4, reservoir=43, remarques="GS berline et Break")
L += g("GS", "G", "2", "1979-09", "1986-07", ["1.1 57", "1.2 65", "1.3 65"], reservoir=43,
       remarques="GSA berline 5 portes et Break")
L += g("CX", "MA", "1", "1974-09", "1985-06",
       ["2.0 102", "2.2 112", ("2.4 115", {"debut": "1976-09"}), ("GTi 2.4 128", {"debut": "1977-07"}),
        ("2.2 D 66", {"debut": "1975-09"}), ("2.5 D 75", {"debut": "1978-07"}), ("2.5 TD 95", {"debut": "1983-09"})],
       reservoir=68, remarques="Berline, Break, Familiale, Prestige")
L += g("CX", "MA", "2", "1985-07", "1991-06",
       ["2.0 106", "GTi 2.5 138", "GTi Turbo 2.5 168", "2.5 D 75", "2.5 TD 95", ("2.5 TD 120", {"debut": "1987-09"})],
       reservoir=68, remarques="Berline, Break, Familiale, Prestige")
L += g("Visa", "VD", "1", "1978-10", "1981-06", ["652 36", "1.1 57"], reservoir=40, remarques="5 portes")
L += g("Visa", "VD", "2", "1981-07", "1988-07",
       ["652 34", "1.1 50", "1.1 57", ("GT 1.4 80", {"debut": "1982-09"}), ("GTi 1.6 105", {"debut": "1984-09"}),
        ("GTi 1.6 115", {"debut": "1985-09"}), ("1.7 D 60", {"debut": "1984-01"})], reservoir=40,
       remarques="5 portes, Décapotable, 1000 Pistes")
L += g("LNA", "LN", "1", "1976-09", "1986-06", [("602 32", {"fin": "1979-12"}), ("652 36", {"debut": "1978-09"}),
       ("1.1 50", {"debut": "1982-09"})], portes=3, places=4, reservoir=40, remarques="LN puis LNA, base Peugeot 104 coupé")
L += g("BX", "XB", "1", "1982-10", "1986-06",
       ["1.1 55", "1.4 62", "1.4 72", "1.6 90", ("1.9 105", {"debut": "1984-01"}), ("1.9 D 65", {"debut": "1983-09"})],
       reservoir=52, remarques="Berline 5 portes et Break (1985)")
L += g("BX", "XB", "2", "1986-07", "1994-06",
       ["1.4 72", "1.6 94", "GTi 1.9 125", ("1.9 16v 160", {"debut": "1987-09"}), "1.7 D 60", "1.9 D 71",
        ("1.8 TD 90", {"debut": "1988-09"}), ("1.9 TD 90", {"debut": "1992-01"})], reservoir=52,
       remarques="Berline 5 portes et Break ; 4x4")
L += g("AX", "ZA", "1", "1986-10", "1991-06", ["1.0 45", "1.1 55", "1.4 65", ("GT 1.4 85", {"debut": "1987-09"}),
       ("1.4 D 53", {"debut": "1988-09"})], reservoir=36, remarques="3 et 5 portes")
L += g("AX", "ZA", "2", "1991-07", "1998-06", ["1.0 50", "1.1 60", "1.4 75", ("GTi 1.4 100", {"fin": "1996-12"}),
       "1.5 D 57"], reservoir=36, remarques="3 et 5 portes")
L += g("ZX", "N2", "1", "1991-03", "1994-06",
       ["1.1 60", "1.4 75", "1.6 88", "1.9 122", ("2.0 16v 155", {"debut": "1992-09"}), "1.9 D 68",
        ("1.9 TD 90", {"debut": "1992-09"})], reservoir=56, remarques="3 et 5 portes")
L += g("ZX", "N2", "2", "1994-07", "1998-02",
       ["1.4 75", "1.6 90", "1.8 103", "2.0 123", "2.0 16v 150", ("2.0 16v 167", {"fin": "1996-06"}), "1.9 D 70",
        "1.9 TD 90"], reservoir=56, remarques="3 et 5 portes, Break (1994)")
L += g("Xantia", "X", "1", "1993-03", "1997-12",
       ["1.6 88", "1.8 103", ("1.8 16v 112", {"debut": "1995-09"}), "2.0 123", "2.0 16v 155", ("2.0 Turbo CT 150", {"debut": "1995-09"}),
        "1.9 D 75", "1.9 TD 90", ("2.1 TD 110", {"debut": "1995-01"})], reservoir=65,
       remarques="Xantia I — berline 5 portes et Break (1995)")
L += g("Xantia", "X", "2", "1998-01", "2001-12",
       ["1.8 16v 110", "2.0 16v 132", "2.0 Turbo CT 150", "3.0 V6 190", "1.9 TD 90", "2.0 HDi 90", "2.0 HDi 110",
        "2.1 TD 110"], reservoir=65, remarques="Xantia II — berline et Break ; Activa")
L += g("XM", "Y", "1", "1989-05", "1994-06",
       ["2.0 122", "2.0 Turbo CT 145", "3.0 V6 170", ("3.0 V6 24v 200", {"debut": "1990-09"}), "2.1 D 82",
        ("2.1 TD 110", {"debut": "1990-09"})], reservoir=80, remarques="XM I — berline et Break (1991)")
L += g("XM", "Y", "2", "1994-07", "2000-06",
       ["2.0 16v 135", "2.0 Turbo CT 150", "3.0 V6 167", ("3.0 V6 190", {"debut": "1997-09"}), "2.1 TD 110",
        ("2.5 TD 130", {"debut": "1995-09"})], reservoir=80, remarques="XM II — berline et Break")
L += g("Evasion", "U6", "1", "1994-06", "2002-07",
       ["1.8 99", "2.0 123", "2.0 16v 132", "2.0 Turbo CT 147", "1.9 TD 90", ("2.0 HDi 109", {"debut": "1999-09"})],
       places=7, reservoir=80, remarques="Monospace 5 à 8 places (Synergie hors de France)")
L += g("C8", "EA", "1", "2002-07", "2014-06",
       ["2.0 16v 136", "2.0 16v 143", "2.2 16v 158", "3.0 V6 204", "2.0 HDi 109", "2.0 HDi 120", "2.0 HDi 136",
        "2.0 HDi 163", "2.2 HDi 128", "2.2 HDi 170"], places=7, reservoir=80,
       remarques="Monospace 5 à 8 places ; restylage 2008 non détaillé")
L += g("C6", "C6", "1", "2005-11", "2012-12",
       ["3.0 V6 211", "3.0 V6 215", "2.7 HDi V6 204", ("2.2 HDi 170", {"debut": "2009-01"}),
        ("3.0 HDi V6 240", {"debut": "2009-06"})], portes=4, reservoir=72, remarques="Grande berline")
L += g("C-Crosser", "VU", "1", "2007-07", "2012-12", ["2.2 HDi 156", "2.4 16v 170"], reservoir=60,
       remarques="SUV 5 ou 7 places, base Mitsubishi Outlander")
L += g("C-Zero", "C-Zero", "1", "2010-10", "2020-12", [("Électrique 67", el(16))], places=4, reservoir=0,
       remarques="Citadine électrique, base Mitsubishi i-MiEV")
L += g("C-Elysée", "DD", "1", "2012-11", "2017-03",
       ["1.2 VTi 72", "1.6 VTi 115", "1.6 HDi 92", ("1.6 BlueHDi 100", {"debut": "2015-09"})], portes=4, reservoir=50,
       remarques="Berline 4 portes")
L += g("C-Elysée", "DD", "2", "2017-04", "2021-12",
       ["1.2 PureTech 82", "1.6 VTi 115", "1.6 BlueHDi 100", ("1.5 BlueHDi 100", {"debut": "2019-01"})], portes=4,
       reservoir=50, remarques="Berline 4 portes")
L += g("Nemo", "AA", "1", "2008-01", "2017-12", ["1.4 73", "1.3 HDi 75", ("1.3 HDi 80", {"debut": "2010-01"})],
       places=2, reservoir=45, remarques="Fourgonnette et Multispace, base Fiat Fiorino")

# ---------------------------------------------------------------- Ami / C1 / C2 / Saxo
L += g("Ami", "AMI", "1", "2020-03", None, [("Électrique 8", el(6))], portes=2, places=2, reservoir=0,
       remarques="Quadricycle léger électrique (45 km/h)")
L += g("Saxo", "S0", "1", "1996-05", "1999-09",
       ["1.0 50", "1.1 60", "1.4 75", "1.6 90", "VTS 1.6 16v 120", "1.5 D 57"], reservoir=45, remarques="3 et 5 portes")
L += g("Saxo", "S0", "2", "1999-10", "2004-03",
       ["1.1 60", "1.4 75", "1.6 100", "VTS 1.6 16v 120", "1.5 D 57"], reservoir=45, remarques="3 et 5 portes")
L += g("C1", "PM", "1", "2005-06", "2008-12", ["1.0 68", "1.4 HDi 54"], places=4, reservoir=35, remarques="3 et 5 portes")
L += g("C1", "PM", "2", "2009-01", "2012-03", ["1.0 68", ("1.4 HDi 54", {"fin": "2010-12"})], places=4, reservoir=35,
       remarques="3 et 5 portes")
L += g("C1", "PM", "3", "2012-04", "2014-05", ["1.0 68"], places=4, reservoir=35, remarques="3 et 5 portes")
L += g("C1", "PS", "1", "2014-06", "2018-05", ["1.0 VTi 68", "1.2 PureTech 82"], places=4, reservoir=35,
       remarques="3 et 5 portes, Airscape découvrable")
L += g("C1", "PS", "2", "2018-06", "2022-06", ["1.0 VTi 72"], places=4, reservoir=35,
       remarques="3 et 5 portes, Airscape découvrable")
L += g("C2", "JM", "1", "2003-09", "2009-12",
       ["1.1 60", "1.4 75", "1.4 16v 90", "1.6 16v 110", ("VTS 1.6 16v 125", {"debut": "2004-03"}), "1.4 HDi 68",
        "1.6 HDi 110"], portes=3, places=4, reservoir=41, remarques="3 portes ; restylage 2008 non détaillé")

# ---------------------------------------------------------------- C3
L += g("C3", "FC", "1", "2002-04", "2005-09",
       ["1.1 60", "1.4 75", "1.4 16v 90", "1.6 16v 110", "1.4 HDi 68", "1.4 HDi 90"], reservoir=47,
       remarques="C3 I — 5 portes, Pluriel (2003)")
L += g("C3", "FC", "2", "2005-10", "2009-11",
       ["1.1 60", "1.4 75", "1.4 16v 90", "1.6 16v 110", "1.4 HDi 68", "1.4 HDi 90", "1.6 HDi 110"], reservoir=47,
       remarques="C3 I — 5 portes, Pluriel")
L += g("C3", "SC", "1", "2009-11", "2013-03",
       ["1.1 60", "1.4 75", "1.4 VTi 95", "1.6 VTi 120", "1.4 HDi 68", "1.6 HDi 90", "1.6 HDi 110",
        ("1.6 e-HDi 92", {"debut": "2010-09"}), ("1.6 e-HDi 115", {"debut": "2010-09"})], reservoir=50,
       remarques="C3 II — 5 portes")
L += g("C3", "SC", "2", "2013-04", "2016-12",
       ["1.0 VTi 68", "1.2 VTi 82", "1.6 VTi 120", "1.4 HDi 70", "1.6 e-HDi 92", ("1.6 BlueHDi 75", {"debut": "2014-09"}),
        ("1.6 BlueHDi 100", {"debut": "2014-09"})], reservoir=50, remarques="C3 II — 5 portes")
L += g("C3", "SX", "1", "2016-11", "2020-05",
       ["1.2 PureTech 68", "1.2 PureTech 82", "1.2 PureTech 110", "1.6 BlueHDi 75", "1.6 BlueHDi 100",
        ("1.5 BlueHDi 100", {"debut": "2019-01"})], reservoir=45, remarques="C3 III — 5 portes")
L += g("C3", "SX", "2", "2020-06", "2024-03",
       ["1.2 PureTech 83", "1.2 PureTech 110", "1.5 BlueHDi 100"], reservoir=45, remarques="C3 III — 5 portes")
L += g("C3", "CC24", "1", "2024-04", None,
       ["1.2 PureTech 100", ("1.2 Hybrid 110 e-DCS6", {"debut": "2025-01"}), ("ë-C3 113", el(44))], reservoir=44,
       remarques="C3 IV — 5 portes (plateforme Smart Car)")
L += g("C3 Aircross", "A88", "1", "2017-10", "2021-05",
       ["1.2 PureTech 82", "1.2 PureTech 110", "1.2 PureTech 130 EAT6", "1.6 BlueHDi 100", "1.6 BlueHDi 120",
        ("1.5 BlueHDi 100", {"debut": "2019-01"}), ("1.5 BlueHDi 120", {"debut": "2019-01"})], reservoir=45)
L += g("C3 Aircross", "A88", "2", "2021-06", "2024-06",
       ["1.2 PureTech 110", "1.2 PureTech 130 EAT6", "1.5 BlueHDi 110", "1.5 BlueHDi 120"], reservoir=45)
L += g("C3 Aircross", "CC24", "1", "2024-10", None,
       ["1.2 PureTech 100", "1.2 Hybrid 145 e-DCS6", ("ë-C3 Aircross 113", el(44))], reservoir=44,
       remarques="SUV 5 ou 7 places")

# ---------------------------------------------------------------- Xsara / C4
L += g("Xsara", "N6", "1", "1997-09", "2000-09",
       ["1.4 75", "1.6 90", "1.8 16v 110", "2.0 16v 136", "VTS 2.0 16v 167", "1.9 D 70", "2.0 HDi 90"],
       reservoir=54, remarques="Berline, Coupé, Break")
L += g("Xsara", "N6", "2", "2000-10", "2006-02",
       ["1.4 75", "1.6 16v 110", "2.0 16v 136", "VTS 2.0 16v 136", "1.9 D 70", "2.0 HDi 90", "1.4 HDi 68",
        "1.6 HDi 110"], reservoir=54, remarques="Berline, Coupé, Break")
L += g("Xsara Picasso", "N68", "1", "1999-12", "2004-03",
       ["1.6 95", "1.8 16v 115", "2.0 16v 136", "2.0 HDi 90"], reservoir=55, remarques="Monospace")
L += g("Xsara Picasso", "N68", "2", "2004-04", "2010-12",
       ["1.6 16v 110", "1.8 16v 117", "2.0 16v 136", "2.0 HDi 90", "1.6 HDi 90", "1.6 HDi 110"], reservoir=55,
       remarques="Monospace")
L += g("C4", "L", "1", "2004-11", "2008-07",
       ["1.4 16v 90", "1.6 16v 110", "2.0 16v 138", "VTS 2.0 16v 180", "1.6 HDi 90", "1.6 HDi 110", "2.0 HDi 138"],
       reservoir=60, remarques="C4 I — 5 portes et Coupé")
L += g("C4", "L", "2", "2008-08", "2010-10",
       ["1.4 VTi 95", "1.6 VTi 120", "1.6 THP 140", "1.6 THP 150", "2.0 16v 143", "1.6 HDi 90", "1.6 HDi 110",
        "2.0 HDi 136"], reservoir=60, remarques="C4 I — 5 portes et Coupé")
L += g("C4", "B7", "1", "2010-11", "2015-04",
       ["1.4 VTi 95", "1.6 VTi 120", "1.6 THP 155", "1.6 HDi 90", "1.6 HDi 110", "1.6 e-HDi 112", "2.0 HDi 150",
        "2.0 HDi 163"], reservoir=60, remarques="C4 II — 5 portes")
L += g("C4", "B7", "2", "2015-05", "2018-09",
       ["1.2 PureTech 110", "1.2 PureTech 130", "1.6 THP 165", "1.6 BlueHDi 100", "1.6 BlueHDi 120",
        "2.0 BlueHDi 150"], reservoir=60, remarques="C4 II — 5 portes")
L += g("C4", "C41", "1", "2020-10", "2024-04",
       ["1.2 PureTech 100", "1.2 PureTech 130 EAT8", "1.2 PureTech 155 EAT8", "1.5 BlueHDi 110", "1.5 BlueHDi 130 EAT8",
        ("ë-C4 136", el(50, fin="2022-12")), ("ë-C4 156", el(54, debut="2023-01"))],
       reservoir=50, remarques="C4 III — 5 portes et C4 X berline (2022)")
L += g("C4", "C41", "2", "2024-05", None,
       ["1.2 PureTech 100", "1.2 Hybrid 136 e-DCS6", "1.2 Hybrid 145 e-DCS6", "1.5 BlueHDi 130 EAT8", ("ë-C4 156", el(54))],
       reservoir=50, remarques="C4 III — 5 portes et C4 X")
L += g("C4 Cactus", "E3", "1", "2014-09", "2018-03",
       ["1.2 PureTech 75", "1.2 PureTech 82", "1.2 PureTech 110", "1.6 e-HDi 92", "1.6 BlueHDi 100"], reservoir=50)
L += g("C4 Cactus", "E3", "2", "2018-04", "2020-09",
       ["1.2 PureTech 82", "1.2 PureTech 110", "1.2 PureTech 130", "1.6 BlueHDi 100", "1.5 BlueHDi 100",
        "1.5 BlueHDi 120"], reservoir=50, remarques="Berline compacte")
L += g("C4 Picasso", "U", "1", "2006-10", "2010-07",
       ["1.8 16v 125", "2.0 16v 143", "1.6 HDi 110", "2.0 HDi 138"], places=7, reservoir=60,
       remarques="C4 Picasso et Grand C4 Picasso (7 places)")
L += g("C4 Picasso", "U", "2", "2010-08", "2013-05",
       ["1.6 VTi 120", "1.6 THP 155", "1.6 HDi 110", "1.6 e-HDi 112", "2.0 HDi 150", "2.0 HDi 163"], places=7,
       reservoir=60, remarques="C4 Picasso et Grand C4 Picasso (7 places)")
L += g("C4 Picasso", "B78", "1", "2013-06", "2016-08",
       ["1.6 VTi 120", "1.6 THP 155", "1.6 THP 165", "1.6 e-HDi 92", "1.6 e-HDi 115", "1.6 BlueHDi 120",
        "2.0 BlueHDi 150"], places=7, reservoir=57, remarques="C4 Picasso et Grand C4 Picasso (7 places)")
L += g("C4 Picasso", "B78", "2", "2016-09", "2018-08",
       ["1.2 PureTech 130", "1.6 THP 165", "1.6 BlueHDi 100", "1.6 BlueHDi 120", "2.0 BlueHDi 150"], places=7,
       reservoir=57, remarques="C4 Picasso et Grand C4 Picasso (7 places)")
L += g("C4 Picasso", "B78", "3", "2018-09", "2022-06",
       ["1.2 PureTech 130", "1.5 BlueHDi 130", "2.0 BlueHDi 160"], places=7, reservoir=57,
       remarques="Rebaptisé C4 SpaceTourer et Grand C4 SpaceTourer")

# ---------------------------------------------------------------- C5
L += g("C5", "DC", "1", "2001-03", "2004-08",
       ["1.8 16v 115", "2.0 16v 136", "3.0 V6 207", "2.0 HDi 90", "2.0 HDi 110", "2.2 HDi 133"], reservoir=68,
       remarques="C5 I — berline et Break")
L += g("C5", "DC", "2", "2004-09", "2008-01",
       ["1.8 16v 125", "2.0 16v 140", "3.0 V6 210", "1.6 HDi 110", "2.0 HDi 136", "2.2 HDi 170"], reservoir=68,
       remarques="C5 I restylée (parfois appelée C5 II) — berline et Break")
L += g("C5", "RD", "1", "2008-02", "2010-12",
       ["1.6 VTi 120", "1.6 THP 155", "1.8 16v 125", "2.0 16v 140", "3.0 V6 215", "1.6 HDi 110", "2.0 HDi 136",
        "2.0 HDi 140", "2.2 HDi 170", "2.7 HDi V6 204", ("2.0 HDi 163", {"debut": "2009-09"}),
        ("3.0 HDi V6 240", {"debut": "2009-09"})],
       reservoir=71, remarques="C5 II (parfois appelée C5 III) — berline et Tourer (break)")
L += g("C5", "RD", "2", "2011-01", "2017-12",
       ["1.6 VTi 120", "1.6 THP 155", "2.0 16v 140", "1.6 e-HDi 115", "2.0 HDi 140", "2.0 HDi 163", "2.2 HDi 204",
        "3.0 HDi V6 240", ("2.0 BlueHDi 150", {"debut": "2014-09"}), ("2.0 BlueHDi 180", {"debut": "2014-09"})],
       reservoir=71, remarques="C5 II — berline et Tourer ; motorisations e-HDi puis BlueHDi, date de phase approximative")
L += g("C5 Aircross", "C84", "1", "2018-11", "2022-02",
       ["1.2 PureTech 130", "1.6 PureTech 180 EAT8", "1.5 BlueHDi 130", "2.0 BlueHDi 180",
        ("Hybrid 225 e-EAT8", ph(13, 43, debut="2020-06"))], reservoir=53)
L += g("C5 Aircross", "C84", "2", "2022-03", "2025-06",
       ["1.2 PureTech 130", "1.5 BlueHDi 130", ("Hybrid 136 e-DCS6", {"debut": "2023-06"}),
        ("Hybrid 180 e-EAT8", ph(13, 43)), ("Hybrid 225 e-EAT8", ph(13, 43))], reservoir=53)
L += g("C5 Aircross", "C87", "1", "2025-11", None,
       ["1.2 Hybrid 145 e-DCS6", ("Plug-in Hybrid 195 e-DCS7", ph(21, 40)), ("ë-C5 Aircross 210", el(73)),
        ("ë-C5 Aircross 230", el(97))], reservoir=55, remarques="SUV (plateforme STLA Medium)")
L += g("C5 X", "E43", "1", "2022-01", None,
       ["1.2 PureTech 130 EAT8", "1.6 PureTech 180 EAT8", ("Hybrid 225 e-EAT8", ph(13, 40)),
        ("1.2 Hybrid 136 e-DCS6", {"debut": "2023-09"})], reservoir=52, remarques="Berline surélevée")

# ---------------------------------------------------------------- Utilitaires / ludospaces
L += g("Berlingo", "M", "1", "1996-07", "2002-08", ["1.1 60", "1.4 75", "1.9 D 70", "2.0 HDi 90"], places=2,
       reservoir=55, remarques="Fourgonnette et Multispace 5 places")
L += g("Berlingo", "M", "2", "2002-09", "2008-03",
       ["1.4 75", "1.6 16v 110", "1.9 D 70", "2.0 HDi 90", "1.6 HDi 75", "1.6 HDi 90"], places=2, reservoir=55,
       remarques="Fourgonnette et Multispace 5 places")
L += g("Berlingo", "B9", "1", "2008-04", "2012-03",
       ["1.6 VTi 98", "1.6 HDi 75", "1.6 HDi 90", "1.6 HDi 110"], places=3, reservoir=60,
       remarques="Fourgon et Multispace 5 à 7 places")
L += g("Berlingo", "B9", "2", "2012-04", "2018-06",
       ["1.6 VTi 98", "1.6 HDi 75", "1.6 BlueHDi 75", "1.6 BlueHDi 100", "1.6 BlueHDi 120",
        ("Electric 67", el(23, debut="2013-06"))], places=3, reservoir=60, remarques="Fourgon et Multispace 5 à 7 places")
L += g("Berlingo", "K9", "1", "2018-06", "2024-05",
       ["1.2 PureTech 110", "1.2 PureTech 130", "1.5 BlueHDi 75", "1.5 BlueHDi 100", "1.5 BlueHDi 130",
        ("ë-Berlingo 136", el(50, debut="2021-06"))], places=5, reservoir=50, remarques="Van et ludospace 5 ou 7 places")
L += g("Berlingo", "K9", "2", "2024-06", None,
       ["1.2 PureTech 110", "1.5 BlueHDi 100", "1.5 BlueHDi 130", ("ë-Berlingo 136", el(50))], places=5, reservoir=50,
       remarques="Van et ludospace 5 ou 7 places")
L += g("Jumpy", "G9", "1", "2007-01", "2016-05", ["1.6 HDi 90", "2.0 HDi 120", "2.0 HDi 136", "2.0 HDi 163"],
       portes=4, places=3, reservoir=80, remarques="Fourgon ; Jumpy Combi / SpaceTourer")
L += g("Jumpy", "K0", "1", "2016-06", "2024-05",
       ["1.5 BlueHDi 100", "1.5 BlueHDi 120", "1.6 BlueHDi 95", "1.6 BlueHDi 115", "2.0 BlueHDi 120", "2.0 BlueHDi 150",
        "2.0 BlueHDi 180", ("ë-Jumpy 136", el(50, debut="2020-09")), ("ë-Jumpy 136 75 kWh", el(75, debut="2020-09"))],
       portes=4, places=3, reservoir=69, remarques="Fourgon")
L += g("Jumpy", "K0", "2", "2024-06", None,
       ["2.0 BlueHDi 145", "2.0 BlueHDi 180", ("ë-Jumpy 136", el(50)), ("ë-Jumpy 136 75 kWh", el(75))],
       portes=4, places=3, reservoir=69, remarques="Fourgon")
L += g("SpaceTourer", "K0", "1", "2016-06", "2024-05",
       ["1.6 BlueHDi 115", "2.0 BlueHDi 150", "2.0 BlueHDi 180", ("ë-SpaceTourer 136", el(50, debut="2020-09")),
        ("ë-SpaceTourer 136 75 kWh", el(75, debut="2020-09"))], places=8, reservoir=69, remarques="Minibus 5 à 9 places")
L += g("SpaceTourer", "K0", "2", "2024-06", None,
       ["2.0 BlueHDi 145", "2.0 BlueHDi 180", ("ë-SpaceTourer 136", el(75))], places=8, reservoir=69,
       remarques="Minibus 5 à 9 places")
L += g("Jumper", "250", "1", "2006-07", "2014-05", ["2.2 HDi 100", "2.2 HDi 120", "3.0 HDi 157"],
       portes=4, places=3, reservoir=90, remarques="Grand fourgon")
L += g("Jumper", "250", "2", "2014-06", None,
       ["2.0 BlueHDi 110", "2.0 BlueHDi 130", "2.0 BlueHDi 160", "2.2 BlueHDi 140", "2.2 BlueHDi 165", "2.2 BlueHDi 180",
        ("ë-Jumper 122", el(75, debut="2021-01"))], portes=4, places=3, reservoir=90,
       remarques="Grand fourgon ; restylage 2024 non détaillé")

# ---------------------------------------------------------------- Moteurs (PSA, partagés avec Peugeot)
FAMILLES = dict(psa.FAMILLES, **{
    # classiques
    "CIT-7C": f("ATM", "ESS", 1.6, "NC", 4, 3800, 2000, "20W50", 4.0, 3000),
    "CIT-11": f("ATM", "ESS", 1.9, "NC", 4, 3800, 2000, "20W50", 4.5, 3000),
    "CIT-15SIX": f("ATM", "ESS", 2.9, "NC", 6, 3800, 2000, "20W50", 6.0, 3000),
    "2CV-375": f("ATM", "ESS", 0.4, "NC", 2, 3500, 2000, "20W50", 2.0, 5000, a="PLAT"),
    "2CV-425": f("ATM", "ESS", 0.4, "NC", 2, 5000, 3500, "20W50", 2.0, 5000, a="PLAT"),
    "2CV-435": f("ATM", "ESS", 0.4, "NC", 2, 6750, 4000, "20W50", 2.0, 5000, a="PLAT"),
    "2CV-602": f("ATM", "ESS", 0.6, "NC", 2, 5750, 3500, "20W50", 2.2, 5000, a="PLAT"),
    "VISA-652": f("ATM", "ESS", 0.65, "NC", 2, 5500, 3500, "20W50", 2.5, 7500, a="PLAT"),
    "GS-1.0": f("ATM", "ESS", 1.0, "COURROIE", 4, 6500, 3500, "20W50", 4.5, 7500, a="PLAT"),
    "GS-1.1": f("ATM", "ESS", 1.1, "COURROIE", 4, 5750, 3500, "20W50", 4.5, 7500, a="PLAT"),
    "GS-1.2": f("ATM", "ESS", 1.2, "COURROIE", 4, 5750, 3250, "20W50", 4.5, 7500, a="PLAT"),
    "GS-1.3": f("ATM", "ESS", 1.3, "COURROIE", 4, 5500, 3500, "20W50", 4.5, 7500, a="PLAT"),
    "CIT-M-1.9": f("ATM", "ESS", 1.9, "CHAINE", 4, 5000, 3000, "20W50", 4.5, 5000),
    "CIT-M-2.0": f("ATM", "ESS", 2.0, "CHAINE", 4, 5500, 3000, "20W50", 4.5, 5000),
    "CIT-M-2.2": f("ATM", "ESS", 2.2, "CHAINE", 4, 5500, 3500, "20W50", 4.5, 5000),
    "CIT-M-2.3": f("ATM", "ESS", 2.3, "CHAINE", 4, 5750, 4000, "20W50", 4.5, 5000),
    "CIT-M-2.5": f("ATM", "ESS", 2.5, "CHAINE", 4, 5000, 4000, "15W40", 5.0, 7500),
    "CIT-M-2.5T": f("TURBO", "ESS", 2.5, "CHAINE", 4, 5000, 3250, "15W40", 5.0, 7500),
    "CIT-M-2.2D": f("ATM", "DSL", 2.2, "CHAINE", 4, 4500, 2500, "15W40", 5.0, 7500),
    "CIT-M-2.5D": f("ATM", "DSL", 2.5, "CHAINE", 4, 4250, 2000, "15W40", 5.0, 7500),
    "CIT-M-2.5TD": f("TURBO", "DSL", 2.5, "CHAINE", 4, 3900, 2000, "15W40", 5.0, 7500),
    "J6R": f("ATM", "ESS", 2.0, "COURROIE", 4, 5500, 3500, "15W40", 5.0, 10000),
    "C114-2.7": f("ATM", "ESS", 2.7, "CHAINE", 6, 5500, 4000, "20W50", 6.0, 5000, a="V"),
    "C114-3.0": f("ATM", "ESS", 3.0, "CHAINE", 6, 5750, 4000, "20W50", 6.0, 5000, a="V"),
    "XY": f("ATM", "ESS", 1.4, "CHAINE", 4, 5500, 3000, "15W40", 4.0, 7500),
    "TUD3": f("ATM", "DSL", 1.4, "COURROIE", 4, 5000, 2500, "10W40", 3.5, 10000),
    "XU7": f("ATM", "ESS", 1.8, "COURROIE", 4, 5500, 3000, "15W40", 5.0, 10000),
    "XU9J4": f("ATM", "ESS", 1.9, "COURROIE", 4, 6500, 5000, "10W40", 5.0, 10000),
    "XU10": f("ATM", "ESS", 2.0, "COURROIE", 4, 5500, 3500, "15W40", 5.0, 10000),
    "XU10J4": f("ATM", "ESS", 2.0, "COURROIE", 4, 6500, 3500, "10W40", 5.0, 10000),
    "XU10J2TE": f("TURBO", "ESS", 2.0, "COURROIE", 4, 5300, 2500, "10W40", 5.0, 10000),
    "XUD9": f("ATM", "DSL", 1.9, "COURROIE", 4, 4600, 2000, "15W40", 5.0, 10000),
    "XUD9TE": f("TURBO", "DSL", 1.9, "COURROIE", 4, 4000, 2250, "15W40", 5.0, 10000),
    "XUD11": f("ATM", "DSL", 2.1, "COURROIE", 4, 4500, 2000, "15W40", 5.0, 10000),
    "XUD11BTE": f("TURBO", "DSL", 2.1, "COURROIE", 4, 4300, 2000, "15W40", 5.0, 10000),
    "DK5ATE": f("TURBO", "DSL", 2.5, "COURROIE", 4, 4300, 2000, "15W40", 6.0, 10000),
    "PRV-ZPJ": f("ATM", "ESS", 3.0, "COURROIE", 6, 5600, 4600, "15W40", 5.5, 10000, a="V"),
    "PRV-ZPJ4": f("ATM", "ESS", 3.0, "COURROIE", 6, 6000, 3600, "10W40", 5.5, 10000, a="V"),
    "EW12J4": f("ATM", "ESS", 2.2, "COURROIE", 4, 5650, 3900, "5W40", 4.25, 20000),
    "DT17": f("TURBO", "DSL", 2.7, "COURROIE", 6, 4000, 1900, "5W30", 6.0, 20000, a="V"),
    "EC5": f("ATM", "ESS", 1.6, "COURROIE", 4, 6050, 4000, "5W30", 4.25, 20000),
    "4B12": f("ATM", "ESS", 2.4, "CHAINE", 4, 6000, 4100, "5W30", 4.6, 15000),
    "Y4F1-EV": electrique(),
    "FIRE-1.4": f("ATM", "ESS", 1.4, "COURROIE", 4, 6000, 3000, "10W40", 3.0, 15000),
    "MJT-1.3": f("TURBO", "DSL", 1.3, "CHAINE", 4, 4000, 1750, "5W30", 3.9, 30000),
    "TU9": f("ATM", "ESS", 1.0, "COURROIE", 4, 5500, 3000, "10W40", 3.0, 15000),
    "TUD5": f("ATM", "DSL", 1.5, "COURROIE", 4, 5000, 2250, "10W40", 3.5, 10000),
    "EW7J4": f("ATM", "ESS", 1.8, "COURROIE", 4, 5500, 4000, "5W40", 4.25, 20000),
    "EW7A": f("ATM", "ESS", 1.8, "COURROIE", 4, 6000, 3750, "5W30", 4.25, 20000),
    "EW10A": f("ATM", "ESS", 2.0, "COURROIE", 4, 6000, 4000, "5W30", 4.25, 20000),
    "ES9": f("ATM", "ESS", 3.0, "COURROIE", 6, 6000, 3750, "5W40", 5.0, 20000, a="V"),
    "DV4TED4": f("TURBO", "DSL", 1.4, "COURROIE", 4, 4000, 1750, "5W30", 3.75, 20000),
    "DW10ATED": f("TURBO", "DSL", 2.0, "COURROIE", 4, 4000, 1750, "5W30", 4.5, 20000),
    "DW12TED4": f("TURBO", "DSL", 2.2, "COURROIE", 4, 4000, 2000, "5W30", 4.75, 20000),
    "DT20C": f("TURBO", "DSL", 3.0, "COURROIE", 6, 4000, 1600, "5W30", 6.0, 20000, a="V"),
    "STLA-SMART-EV": electrique(), "AMI-EV": electrique(),
})
TABLE = dict(psa.TABLE, **{
    # classiques
    "7 CV 1.6 36": ("CIT-7C", 36, 98), "11 CV 1.9 46": ("CIT-11", 46, 118), "11 CV 1.9 56": ("CIT-11", 56, 125),
    "15-Six 2.9 77": ("CIT-15SIX", 77, 186),
    "375 9": ("2CV-375", 9, 20), "425 12": ("2CV-425", 12, 24), "425 18": ("2CV-425", 18, 28),
    "425 21": ("2CV-425", 21, 29), "2CV4 435 24": ("2CV-435", 24, 30), "Dyane 4 435 26": ("2CV-435", 26, 31),
    "2CV6 602 29": ("2CV-602", 29, 40), "602 22": ("2CV-602", 22, 40), "602 25": ("2CV-602", 25, 42),
    "602 29": ("2CV-602", 29, 40), "602 32": ("2CV-602", 32, 42), "Dyane 6 602 32": ("2CV-602", 32, 42),
    "652 34": ("VISA-652", 34, 49), "652 36": ("VISA-652", 36, 52),
    "Super 1.0 54": ("GS-1.0", 54, 69), "1.0 55": ("GS-1.0", 55, 72), "1.1 57": ("GS-1.1", 57, 80),
    "1.2 60": ("GS-1.2", 60, 88), "1.2 65": ("GS-1.2", 65, 89), "1.3 65": ("GS-1.3", 65, 98),
    "1.1 57@VD": ("XW7", 57, 85), "1.1 50": ("XW7", 50, 79),
    "DS19 1.9 75": ("CIT-M-1.9", 75, 137), "ID19 1.9 66": ("CIT-M-1.9", 66, 127), "DS19 1.9 83": ("CIT-M-1.9", 83, 145),
    "DS20 2.0 91": ("CIT-M-2.0", 91, 147), "DS20 2.0 103": ("CIT-M-2.0", 103, 152),
    "DS21 2.2 109": ("CIT-M-2.2", 109, 172), "DS21 2.2 125": ("CIT-M-2.2", 125, 178),
    "DS23 2.3 115": ("CIT-M-2.3", 115, 181), "DS23 2.3 130": ("CIT-M-2.3", 130, 196),
    "2.0 102": ("CIT-M-2.0", 102, 162), "2.2 112": ("CIT-M-2.2", 112, 177), "2.4 115": ("CIT-M-2.3", 115, 186),
    "2.4 128": ("CIT-M-2.3", 128, 197), "2.0 106": ("J6R", 106, 165), "2.5 138": ("CIT-M-2.5", 138, 211),
    "Turbo 2.5 168": ("CIT-M-2.5T", 168, 294), "2.2 D 66": ("CIT-M-2.2D", 66, 125),
    "2.5 D 75": ("CIT-M-2.5D", 75, 152), "2.5 TD 95": ("CIT-M-2.5TD", 95, 216), "2.5 TD 120": ("CIT-M-2.5TD", 120, 255),
    "2.7 V6 170": ("Maserati", "C114-2.7", 170, 230), "2.7 V6 178": ("Maserati", "C114-2.7", 178, 233),
    "3.0 V6 180": ("Maserati", "C114-3.0", 180, 247),
    "1.4 80": ("XY", 80, 112), "1.6 105": ("XU5J", 105, 135), "1.6 115": ("XU5J", 115, 133), "1.7 D 60": ("XUD7", 60, 110),
    "1.4 62": ("XY", 62, 108), "1.4 72": ("XY", 72, 110), "1.6 90@XU": ("XU5J", 90, 135), "1.6 94": ("XU5J", 94, 135),
    "1.6 88": ("XU5J", 88, 132), "1.9 105": ("XU9J", 105, 162), "1.9 125": ("XU9J", 125, 175),
    "1.9 122": ("XU9J", 122, 160), "1.9 16v 160": ("XU9J4", 160, 180),
    "1.0 45@TU": ("TU9", 45, 72), "1.0 50": ("TU9", 50, 74), "1.1 55@TU": ("TU1", 55, 86), "1.4 65": ("TU3", 65, 108),
    "1.4 85": ("TU3", 85, 116), "1.4 100": ("TU3", 100, 120), "1.4 D 53": ("TUD3", 53, 84),
    "1.8 103": ("XU7", 103, 153), "1.8 99": ("XU7", 99, 147), "2.0 123": ("XU10", 123, 176), "2.0 122": ("XU10", 122, 176),
    "2.0 16v 150": ("XU10J4", 150, 180), "2.0 16v 155": ("XU10J4", 155, 183), "2.0 16v 167": ("XU10J4", 167, 193),
    "2.0 16v 132": ("XU10J4", 132, 180), "2.0 16v 135": ("XU10J4", 135, 180), "2.0 16v 136@XU": ("XU10J4", 136, 190),
    "1.8 16v 112": ("XU7JP4", 112, 155),
    "2.0 Turbo CT 145": ("XU10J2TE", 145, 255), "2.0 Turbo CT 147": ("XU10J2TE", 147, 235),
    "2.0 Turbo CT 150": ("XU10J2TE", 150, 235), "3.0 V6 190": ("ES9", 190, 267),
    "3.0 V6 170": ("PRV-ZPJ", 170, 240), "3.0 V6 167": ("PRV-ZPJ", 167, 240), "3.0 V6 24v 200": ("PRV-ZPJ4", 200, 260),
    "1.9 D 65": ("XUD9", 65, 120), "1.9 D 68": ("XUD9", 68, 120), "1.9 D 70@XU": ("XUD9", 70, 125),
    "1.9 D 71": ("XUD9", 71, 120), "1.9 D 75": ("XUD9", 75, 125), "1.8 TD 90": ("XUD7TE", 90, 175),
    "1.9 TD 90": ("XUD9TE", 90, 196), "2.1 D 82": ("XUD11", 82, 147), "2.1 TD 110": ("XUD11BTE", 110, 250),
    "2.5 TD 130": ("DK5ATE", 130, 285), "2.0 HDi 109": ("DW10ATED", 109, 250),
    "2.2 16v 158": ("EW12J4", 158, 217), "3.0 V6 204": ("ES9", 204, 285), "2.2 HDi 128": ("DW12TED4", 128, 314),
    "3.0 V6 211": ("ES9", 211, 300), "2.7 HDi V6 204": ("DT17", 204, 440), "2.2 HDi 156": ("DW12C", 156, 380),
    "2.4 16v 170": ("Mitsubishi", "4B12", 170, 226), "Électrique 67": ("Mitsubishi", "Y4F1-EV", 67, 180),
    "1.2 VTi 72": ("EB2F", 72, 110), "1.6 VTi 115": ("EC5", 115, 150),
    "1.4 73": ("Fiat", "FIRE-1.4", 73, 118), "1.3 HDi 75": ("Fiat", "MJT-1.3", 75, 190),
    "1.3 HDi 80": ("Fiat", "MJT-1.3", 80, 200),
    "1.0 50": ("TU9", 50, 76), "1.6 95": ("TU5", 95, 135), "1.6 100": ("TU5", 100, 135),
    "1.6 16v 120": ("TU5J4", 120, 145), "1.6 16v 125": ("TU5J4", 125, 143), "1.5 D 57": ("TUD5", 57, 95),
    "1.8 16v 110": ("XU7JP4", 110, 155),
    "1.8 16v 115": ("EW7J4", 115, 160), "1.8 16v 117": ("EW7J4", 117, 160), "1.8 16v 125": ("EW7A", 125, 170),
    "2.0 16v 136": ("EW10J4", 136, 190), "2.0 16v 138": ("EW10J4", 138, 190), "2.0 16v 140": ("EW10A", 140, 200),
    "2.0 16v 143": ("EW10A", 143, 204), "2.0 16v 180": ("EW10J4S", 180, 202),
    "3.0 V6 207": ("ES9", 207, 285), "3.0 V6 210": ("ES9", 210, 300), "3.0 V6 215": ("ES9", 215, 300),
    "1.2 PureTech 68": ("EB2F", 68, 116), "1.2 PureTech 83": ("EB2FA", 83, 118),
    "1.2 PureTech 130 EAT6": ("EB2DTS", 130, 230), "1.2 Hybrid 110 e-DCS6": ("EB2-MHEV", 110, 205),
    "1.6 THP 140": ("EP6DT", 140, 240), "1.6 THP 155": ("EP6CDT", 155, 240),
    "1.4 HDi 90": ("DV4TED4", 90, 200), "2.0 HDi 110": ("DW10ATED", 110, 250), "2.0 HDi 138": ("DW10BTED4", 138, 320),
    "2.2 HDi 133": ("DW12TED4", 133, 314), "2.2 HDi 170": ("DW12C", 170, 370), "3.0 HDi V6 240": ("DT20C", 240, 450),
    "ë-C4 136": ("E-CMP", 136, 260), "ë-C4 156": ("E-CMP", 156, 260), "ë-Berlingo 136": ("E-CMP", 136, 260),
    "ë-Jumpy 136": ("E-CMP", 136, 260), "ë-Jumpy 136 75 kWh": ("E-CMP", 136, 260),
    "ë-SpaceTourer 136": ("E-CMP", 136, 260), "ë-SpaceTourer 136 75 kWh": ("E-CMP", 136, 260),
    "ë-Jumper 122": ("E-BOXER", 122, 260), "ë-C3 113": ("STLA-SMART-EV", 113, 125),
    "ë-C3 Aircross 113": ("STLA-SMART-EV", 113, 125), "ë-C5 Aircross 210": ("STLA-M", 210, 345),
    "ë-C5 Aircross 230": ("STLA-M", 230, 345), "Électrique 8": ("AMI-EV", 8, 40),
})
FAMILLES["XU7JP4"] = f("ATM", "ESS", 1.8, "COURROIE", 4, 5500, 4250, "10W40", 4.5, 15000)

ERES = {"PM": "TOY", "PS": "TOY", "ZA": "TU", "VD": "VD", "N2": "XU", "XB": "XU", "X": "XU", "Y": "XU", "U6": "XU",
        ("N6", "1"): "XU"}
MOT = Motorisations("Peugeot", FAMILLES, TABLE, ERES, prefixes=PREFIXES + ("VTS ",))
MOT.lier(L)

DETAIL = {"Citroën": L}
MOTEURS = MOT.moteurs()
