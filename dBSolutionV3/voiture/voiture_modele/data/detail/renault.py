"""Renault (y compris Renault Sport) : générations, phases, motorisations (marché européen) et moteurs liés."""
from ._outil import PREFIXES, Motorisations, electrique, famille as f, gamme as g


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


L = []

# ---------------------------------------------------------------- Twingo
L += g("Twingo", "C06", "1", "1993-04", "1998-08", ["1.2 55", ("1.2 60", {"debut": "1996-07"})],
       portes=3, places=4, reservoir=40)
L += g("Twingo", "C06", "2", "1998-09", "2007-06", ["1.2 60", ("1.2 16v 75", {"debut": "2001-01"})],
       portes=3, places=4, reservoir=40, remarques="Restylages 2000 et 2004 non détaillés")
L += g("Twingo", "CN0", "1", "2007-06", "2011-12",
       ["1.2 60", "1.2 16v 75", "1.2 TCe 100", ("RS 1.6 133", {"debut": "2008-09"}), "1.5 dCi 65", "1.5 dCi 75",
        "1.5 dCi 85"], portes=3, places=4, reservoir=40)
L += g("Twingo", "CN0", "2", "2012-01", "2014-08", ["1.2 16v 75", "RS 1.6 133", "1.5 dCi 75"],
       portes=3, places=4, reservoir=40)
L += g("Twingo", "AH", "1", "2014-09", "2019-08",
       ["1.0 SCe 70", ("1.0 SCe 65", {"debut": "2018-01"}), "0.9 TCe 90", ("GT 0.9 TCe 110", {"debut": "2016-09"})],
       places=4, reservoir=35, remarques="5 portes, moteur arrière")
L += g("Twingo", "AH", "2", "2019-09", "2024-12",
       ["1.0 SCe 65", ("0.9 TCe 95", {"fin": "2020-12"}), ("Electric 82", el(22, debut="2020-11"))],
       places=4, reservoir=35, remarques="5 portes, moteur arrière")

# ---------------------------------------------------------------- Clio
L += g("Clio", "B/C/S", "1", "1998-03", "2001-05",
       ["1.2 58", "1.4 75", "1.4 16v 98", "1.6 90", ("1.6 16v 110", {"debut": "1999-09"}),
        ("RS 2.0 172", {"debut": "2000-01"}), ("V6 3.0 230", {"debut": "2001-01"}), "1.9 D 65", "1.9 dTi 80"],
       reservoir=50, remarques="Clio II — 3 et 5 portes")
L += g("Clio", "B/C/S", "2", "2001-06", "2006-09",
       ["1.2 60", "1.2 16v 75", "1.4 16v 98", "1.6 16v 110", "RS 2.0 182", ("V6 3.0 255", {"debut": "2003-06", "fin": "2005-12"}),
        "1.5 dCi 65", "1.5 dCi 80", "1.5 dCi 100"],
       reservoir=50, remarques="Clio II — 3 et 5 portes ; Clio Campus jusqu'en 2012")
L += g("Clio", "R", "1", "2005-09", "2009-04",
       ["1.2 16v 75", ("1.2 TCe 100", {"debut": "2007-06"}), "1.4 16v 98", "1.6 16v 110", "2.0 16v 140",
        ("RS 2.0 197", {"debut": "2006-06"}), "1.5 dCi 70", "1.5 dCi 85", "1.5 dCi 105"],
       reservoir=55, remarques="Clio III — 3 et 5 portes, Estate (2008)")
L += g("Clio", "R", "2", "2009-05", "2014-12",
       ["1.2 16v 75", "1.2 TCe 100", "1.6 16v 110", "RS 2.0 203", "1.5 dCi 75", "1.5 dCi 90", "1.5 dCi 105"],
       reservoir=55, remarques="Clio III — 3 et 5 portes, Estate ; berline jusqu'en 2012")
L += g("Clio", "X98", "1", "2012-11", "2016-06",
       ["1.2 16v 75", "0.9 TCe 90", "1.2 TCe 120 EDC", ("RS 1.6 TCe 200", {"debut": "2013-03"}),
        ("RS Trophy 1.6 TCe 220", {"debut": "2015-03"}), "1.5 dCi 75", "1.5 dCi 90"],
       reservoir=45, remarques="Clio IV — 5 portes et Estate")
L += g("Clio", "X98", "2", "2016-07", "2019-08",
       ["1.2 16v 75", "0.9 TCe 75", "0.9 TCe 90", "1.2 TCe 120 EDC", "RS 1.6 TCe 200", "RS Trophy 1.6 TCe 220",
        "1.5 dCi 75", "1.5 dCi 90", "1.5 dCi 110"], reservoir=45, remarques="Clio IV — 5 portes et Estate")
L += g("Clio", "BF", "1", "2019-09", "2023-05",
       ["1.0 SCe 65", "1.0 SCe 75", "1.0 TCe 90", "1.0 TCe 100", "1.3 TCe 130 EDC",
        ("1.0 TCe 100 LPG", {"remarques": "Bicarburation essence / GPL"}),
        ("E-Tech hybrid 140", {"debut": "2020-06", "reservoir": 39, "batterie": 1}),
        "1.5 Blue dCi 85", "1.5 Blue dCi 100"], reservoir=42, remarques="Clio V — 5 portes")
L += g("Clio", "BF", "2", "2023-06", "2026-03",
       ["1.0 SCe 65", "1.0 TCe 90", ("1.0 ECO-G 100", {"remarques": "Bicarburation essence / GPL"}),
        ("E-Tech full hybrid 145", {"reservoir": 39, "batterie": 1}), ("1.5 Blue dCi 100", {"fin": "2024-06"})],
       reservoir=42, remarques="Clio V — 5 portes")

# ---------------------------------------------------------------- Renault 5 / 4 E-Tech, Zoe
L += g("Zoe", "X10", "1", "2012-12", "2019-08",
       [("R240 88", el(22, fin="2016-12")), ("Q90", el(22, fin="2016-12")), ("R90", el(41, debut="2017-01")),
        ("R110", el(41, debut="2018-06"))], reservoir=0, remarques="Citadine électrique")
L += g("Zoe", "X10", "2", "2019-09", "2024-03", [("R110", el(52)), ("R135", el(52))], reservoir=0,
       remarques="Citadine électrique")
L += g("5 E-Tech", "AmpR Small", "1", "2024-10", None,
       [("Urban Range 120", el(40)), ("Comfort Range 150", el(52))], reservoir=0,
       remarques="Citadine électrique ; version sportive : Alpine A290 (marque Alpine)")
L += g("4 E-Tech", "AmpR Small", "1", "2025-06", None,
       [("Comfort Range 120", el(40)), ("Comfort Range 150", el(52))], reservoir=0, remarques="Crossover électrique")

# ---------------------------------------------------------------- Captur
L += g("Captur", "J87", "1", "2013-04", "2017-05",
       ["0.9 TCe 90", "1.2 TCe 120 EDC", "1.5 dCi 90", "1.5 dCi 110"], reservoir=45)
L += g("Captur", "J87", "2", "2017-06", "2019-12",
       ["0.9 TCe 90", ("1.2 TCe 120 EDC", {"fin": "2018-08"}), ("1.3 TCe 130", {"debut": "2018-09"}),
        ("1.3 TCe 150", {"debut": "2018-09"}), "1.5 dCi 90", "1.5 dCi 110"], reservoir=45)
L += g("Captur", "HJB", "1", "2020-01", "2024-03",
       ["1.0 TCe 90", "1.0 TCe 100", ("1.0 TCe 100 LPG", {"remarques": "Bicarburation essence / GPL"}),
        "1.3 TCe 130", "1.3 TCe 155", ("E-Tech Plug-in 160", ph(10, 39, debut="2020-06")),
        ("E-Tech hybrid 145", {"debut": "2021-06", "reservoir": 48, "batterie": 1}),
        "1.5 Blue dCi 95", "1.5 Blue dCi 115"], reservoir=48)
L += g("Captur", "HJB", "2", "2024-04", None,
       ["1.0 TCe 90", ("1.0 ECO-G 100", {"remarques": "Bicarburation essence / GPL"}), "1.3 TCe mhev 140",
        "1.3 TCe mhev 160", ("E-Tech full hybrid 145", {"batterie": 1})], reservoir=48)

# ---------------------------------------------------------------- Mégane
L += g("Mégane", "BA", "1", "1995-11", "1999-02",
       ["1.4 75", "1.6 90", "2.0 115", "2.0 16v 150", "1.9 D 65", "1.9 dTi 80", "1.9 dTi 100"],
       reservoir=60, remarques="Mégane I — berline, Coupé, Cabriolet, Classic")
L += g("Mégane", "BA", "2", "1999-03", "2002-09",
       ["1.4 16v 95", "1.6 16v 110", "2.0 16v 140", "1.9 dTi 80", "1.9 dCi 100"],
       reservoir=60, remarques="Mégane I — berline, Coupé, Cabriolet, Classic, Break")
L += g("Mégane", "M", "1", "2002-09", "2006-01",
       ["1.4 16v 80", "1.4 16v 100", "1.6 16v 115", "2.0 16v 135", ("2.0 T 165", {"debut": "2004-01"}),
        ("RS 2.0 T 225", {"debut": "2004-09"}), "1.5 dCi 80", "1.5 dCi 100", "1.9 dCi 120",
        ("2.0 dCi 150", {"debut": "2005-01"})], reservoir=60, remarques="Mégane II — 3/5 portes, berline, Grandtour, CC")
L += g("Mégane", "M", "2", "2006-02", "2008-10",
       ["1.4 16v 100", "1.6 16v 110", "2.0 16v 135", "2.0 T 165", "RS 2.0 T 225", ("RS R26 2.0 T 230", {"debut": "2007-01"}),
        "1.5 dCi 85", "1.5 dCi 105", "1.9 dCi 130", "2.0 dCi 150"],
       reservoir=60, remarques="Mégane II — 3/5 portes, berline, Grandtour, CC")
L += g("Mégane", "Z", "1", "2008-11", "2012-01",
       ["1.6 16v 110", "1.4 TCe 130", "2.0 16v 140", "2.0 TCe 180", ("RS 2.0 T 250", {"debut": "2009-12"}),
        "1.5 dCi 85", "1.5 dCi 90", "1.5 dCi 105", "1.5 dCi 110", "1.9 dCi 130", "2.0 dCi 150", "2.0 dCi 160"],
       reservoir=60, remarques="Mégane III — 5 portes, Coupé, Estate, CC")
L += g("Mégane", "Z", "2", "2012-02", "2016-01",
       ["1.6 16v 110", "1.2 TCe 115", "1.2 TCe 130", "2.0 TCe 220", "RS 2.0 T 265", ("RS 2.0 T 275", {"debut": "2014-06"}),
        "1.5 dCi 95", "1.5 dCi 110", "1.6 dCi 130"],
       reservoir=60, remarques="Mégane III — 5 portes, Coupé, Estate, CC ; restylage 2014 non détaillé")
L += g("Mégane", "B9A", "1", "2016-01", "2020-03",
       [("1.2 TCe 100", {"fin": "2018-08"}), ("1.2 TCe 130", {"fin": "2018-08"}), ("GT 1.6 TCe 205", {"fin": "2018-08"}),
        ("1.3 TCe 115", {"debut": "2018-09"}), ("1.3 TCe 140", {"debut": "2018-09"}), ("1.3 TCe 160", {"debut": "2018-09"}),
        ("RS 1.8 TCe 280", {"debut": "2018-01"}), ("RS Trophy 1.8 TCe 300", {"debut": "2018-12"}),
        "1.5 dCi 90", "1.5 dCi 110", ("1.5 Blue dCi 115", {"debut": "2018-09"}), "1.6 dCi 130", "GT 1.6 dCi 165",
        ("1.7 Blue dCi 150", {"debut": "2018-09"})],
       reservoir=47, remarques="Mégane IV — 5 portes, Grandtour, Grand Coupé")
L += g("Mégane", "B9A", "2", "2020-04", "2024-12",
       ["1.3 TCe 115", "1.3 TCe 140", "1.3 TCe 160", ("E-Tech Plug-in 160", ph(10, 39)), "RS 1.8 TCe 300",
        "1.5 Blue dCi 115"], reservoir=47, remarques="Mégane IV — 5 portes, Grandtour")
L += g("Mégane E-Tech", "BCB", "1", "2022-02", None,
       [("EV40 130", el(40)), ("EV60 130", el(60)), ("EV60 220", el(60))], reservoir=0,
       remarques="Crossover électrique")
L += g("Fluence", "L38", "1", "2010-01", "2016-12",
       ["1.6 16v 110", "2.0 16v 140", "1.5 dCi 90", "1.5 dCi 110", ("Z.E. 95", el(22, debut="2011-10", fin="2014-12"))],
       portes=4, reservoir=60, remarques="Berline 4 portes")

# ---------------------------------------------------------------- Scénic
L += g("Scénic", "JM", "1", "2003-06", "2006-09",
       ["1.4 16v 98", "1.6 16v 115", "2.0 16v 135", "1.5 dCi 85", "1.5 dCi 105", "1.9 dCi 120", "2.0 dCi 150"],
       reservoir=60, remarques="Scénic II et Grand Scénic (7 places)")
L += g("Scénic", "JM", "2", "2006-10", "2009-04",
       ["1.4 16v 98", "1.6 16v 110", "2.0 16v 135", "1.5 dCi 85", "1.5 dCi 105", "1.9 dCi 130", "2.0 dCi 150"],
       reservoir=60, remarques="Scénic II et Grand Scénic (7 places)")
L += g("Scénic", "JZ", "1", "2009-05", "2012-03",
       ["1.6 16v 110", "1.4 TCe 130", "2.0 16v 140", "1.5 dCi 110", "1.9 dCi 130", "2.0 dCi 150"],
       reservoir=60, remarques="Scénic III et Grand Scénic (7 places)")
L += g("Scénic", "JZ", "2", "2012-04", "2016-09",
       ["1.2 TCe 115", "1.2 TCe 130", "1.5 dCi 110", "1.6 dCi 130"], reservoir=60,
       remarques="Scénic III et Grand Scénic (7 places)")
L += g("Scénic", "JFA", "1", "2016-11", "2022-12",
       [("1.2 TCe 115", {"fin": "2018-08"}), ("1.2 TCe 130", {"fin": "2018-08"}), ("1.3 TCe 140", {"debut": "2018-09"}),
        ("1.3 TCe 160", {"debut": "2018-09"}), "1.5 dCi 110", "Hybrid Assist 1.5 dCi 110", "1.6 dCi 130", "1.6 dCi 160",
        ("1.7 Blue dCi 120", {"debut": "2018-09"}), ("1.7 Blue dCi 150", {"debut": "2018-09"})],
       reservoir=53, remarques="Scénic IV et Grand Scénic (7 places)")
L += g("Scénic E-Tech", "RHN", "1", "2024-01", None, [("Comfort Range 170", el(60)), ("Long Range 220", el(87))],
       reservoir=0, remarques="SUV familial électrique")

# ---------------------------------------------------------------- Laguna / Talisman / Espace
L += g("Laguna", "G", "1", "2001-03", "2005-03",
       ["1.6 16v 110", "1.8 16v 120", "2.0 16v 135", "2.0 T 165", "3.0 V6 207", "1.9 dCi 100", "1.9 dCi 120",
        "2.2 dCi 150"], reservoir=68, remarques="Laguna II — berline et Estate")
L += g("Laguna", "G", "2", "2005-04", "2007-09",
       ["1.6 16v 110", "2.0 16v 135", "2.0 T 170", "3.0 V6 207", "1.9 dCi 110", "1.9 dCi 130", "2.0 dCi 150",
        "2.0 dCi 175"], reservoir=68, remarques="Laguna II — berline et Estate")
L += g("Laguna", "T", "1", "2007-10", "2010-09",
       ["2.0 16v 140", "2.0 TCe 170", ("GT 2.0 TCe 205", {"debut": "2008-09"}), ("3.5 V6 240", {"debut": "2008-10", "remarques": "Coupé"}),
        "1.5 dCi 110", "2.0 dCi 130", "2.0 dCi 150", "2.0 dCi 175", ("3.0 dCi 235", {"debut": "2008-10"})],
       reservoir=66, remarques="Laguna III — berline, Estate, Coupé")
L += g("Laguna", "T", "2", "2010-10", "2015-12",
       ["2.0 16v 140", "2.0 TCe 170", "GT 2.0 TCe 205", "1.5 dCi 110", "2.0 dCi 130", "2.0 dCi 150", "2.0 dCi 175",
        "3.0 dCi 235"], reservoir=66, remarques="Laguna III — berline, Estate, Coupé")
L += g("Talisman", "L2M", "1", "2015-12", "2020-02",
       ["1.6 TCe 150", "GT 1.6 TCe 200", ("1.8 TCe 225", {"debut": "2018-09"}), ("1.3 TCe 160", {"debut": "2018-09"}),
        "1.5 dCi 110", "1.6 dCi 130", "1.6 dCi 160", ("1.7 Blue dCi 120", {"debut": "2018-09"}),
        ("1.7 Blue dCi 150", {"debut": "2018-09"}), ("2.0 Blue dCi 160", {"debut": "2018-09"}),
        ("2.0 Blue dCi 200", {"debut": "2018-09"})], portes=4, reservoir=52, remarques="Berline et Estate")
L += g("Talisman", "L2M", "2", "2020-03", "2022-03",
       ["1.3 TCe 160", "1.8 TCe 225", "1.7 Blue dCi 120", "1.7 Blue dCi 150", "2.0 Blue dCi 160", "2.0 Blue dCi 200"],
       portes=4, reservoir=52, remarques="Berline et Estate")
L += g("Espace", "JK", "1", "2002-11", "2010-06",
       ["2.0 16v 140", "2.0 T 170", "3.5 V6 245", "1.9 dCi 120", "2.0 dCi 150", "2.0 dCi 175", "2.2 dCi 150",
        "3.0 dCi 180"], places=7, reservoir=80, remarques="Espace IV et Grand Espace ; restylage 2006 non détaillé")
L += g("Espace", "JK", "2", "2010-07", "2014-12",
       ["2.0 dCi 130", "2.0 dCi 150", "2.0 dCi 175"], places=7, reservoir=80, remarques="Espace IV")
L += g("Espace", "RFC", "1", "2015-03", "2019-12",
       ["1.6 TCe 200", ("1.8 TCe 225", {"debut": "2017-09"}), "1.6 dCi 130", "1.6 dCi 160",
        ("2.0 Blue dCi 160", {"debut": "2018-09"}), ("2.0 Blue dCi 200", {"debut": "2018-09"})],
       places=7, reservoir=58, remarques="Espace V — 5 ou 7 places")
L += g("Espace", "RFC", "2", "2020-01", "2023-03",
       ["1.8 TCe 225", "2.0 Blue dCi 160", "2.0 Blue dCi 190", "2.0 Blue dCi 200"], places=7, reservoir=58,
       remarques="Espace V — 5 ou 7 places")
L += g("Espace", "RHN", "1", "2023-04", None, [("E-Tech full hybrid 200", {"batterie": 2})], places=7,
       reservoir=55, remarques="Espace VI — SUV 5 ou 7 places")

# ---------------------------------------------------------------- SUV
L += g("Kadjar", "HA", "1", "2015-06", "2018-08",
       ["1.2 TCe 130", "1.6 TCe 165", "1.5 dCi 110", "1.6 dCi 130"], reservoir=55)
L += g("Kadjar", "HA", "2", "2018-09", "2022-06",
       ["1.3 TCe 140", "1.3 TCe 160", "1.5 Blue dCi 115", "1.7 Blue dCi 150"], reservoir=55)
L += g("Austral", "HCB", "1", "2022-11", None,
       ["1.2 TCe mhev 130", "1.3 TCe mhev 140", "1.3 TCe mhev 160", ("E-Tech full hybrid 200", {"batterie": 2})],
       reservoir=55, remarques="SUV ; Espace et Rafale sur la même base")
L += g("Arkana", "LJL", "1", "2021-04", None,
       ["1.3 TCe mhev 140", "1.3 TCe mhev 160", ("E-Tech full hybrid 145", {"batterie": 1})], reservoir=50,
       remarques="SUV coupé ; restylage 2023 non détaillé")
L += g("Rafale", "RHN", "1", "2024-04", None,
       [("E-Tech full hybrid 200", {"batterie": 2}), ("E-Tech 4x4 300", ph(22, 55, debut="2025-03"))],
       reservoir=55, remarques="SUV coupé")
L += g("Koleos", "HY", "1", "2008-01", "2016-03", ["2.5 170", "2.0 dCi 150", "2.0 dCi 175"], reservoir=65,
       remarques="Koleos I ; restylages 2011 et 2013 non détaillés")
L += g("Koleos", "HZG", "1", "2017-06", "2019-08",
       ["1.6 dCi 130", "2.0 dCi 175"], reservoir=60, remarques="Koleos II")
L += g("Koleos", "HZG", "2", "2019-09", "2023-12",
       ["1.3 TCe 160", "1.7 Blue dCi 150", "2.0 Blue dCi 190"], reservoir=60, remarques="Koleos II")

# ---------------------------------------------------------------- Utilitaires
L += g("Kangoo", "KC", "1", "1997-10", "2003-02",
       ["1.2 60", "1.4 75", "1.9 D 55", "1.9 D 65", ("1.9 dTi 80", {"debut": "2000-01"})], places=2, reservoir=50,
       remarques="Kangoo Express et ludospace 5 places")
L += g("Kangoo", "KC", "2", "2003-03", "2009-12",
       ["1.2 16v 75", "1.6 16v 95", "1.5 dCi 57", "1.5 dCi 65", "1.5 dCi 70", "1.5 dCi 85"], places=2, reservoir=50,
       remarques="Kangoo Express et ludospace 5 places")
L += g("Kangoo", "KW", "1", "2008-02", "2013-02",
       ["1.6 90", "1.6 16v 105", "1.5 dCi 70", "1.5 dCi 85", "1.5 dCi 105", ("Z.E. 60", el(22, debut="2011-10"))],
       places=2, reservoir=60, remarques="Kangoo II — Express, Maxi, ludospace 5 à 7 places")
L += g("Kangoo", "KW", "2", "2013-03", "2021-04",
       ["1.2 TCe 115", "1.5 dCi 75", "1.5 dCi 90", "1.5 dCi 110", ("Z.E. 60", el(22, fin="2017-06")),
        ("Z.E. 33", el(33, debut="2017-07"))], places=2, reservoir=60,
       remarques="Kangoo II — Express, Maxi, ludospace 5 à 7 places")
L += g("Kangoo", "KFB", "1", "2021-05", None,
       ["1.3 TCe 100", "1.3 TCe 130", "1.5 Blue dCi 75", "1.5 Blue dCi 95", "1.5 Blue dCi 115",
        ("E-Tech Electric 122", el(45, debut="2022-06"))], places=2, reservoir=54,
       remarques="Kangoo Van et ludospace 5 à 7 places")
L += g("Trafic", "X83", "1", "2001-03", "2006-08",
       ["2.0 16v 120", "1.9 dCi 82", "1.9 dCi 100", "2.5 dCi 135"], portes=4, places=3, reservoir=90,
       remarques="Fourgon et Passenger")
L += g("Trafic", "X83", "2", "2006-09", "2014-06",
       ["2.0 dCi 90", "2.0 dCi 115", "2.0 dCi 150", "2.5 dCi 146"], portes=4, places=3, reservoir=90,
       remarques="Fourgon et Passenger")
L += g("Trafic", "X82", "1", "2014-07", "2021-08",
       ["1.6 dCi 90", "1.6 dCi 115", "1.6 dCi 120", "1.6 dCi 125", "1.6 dCi 140", ("2.0 Blue dCi 120", {"debut": "2019-06"}),
        ("2.0 Blue dCi 145", {"debut": "2019-06"}), ("2.0 Blue dCi 170", {"debut": "2019-06"})],
       portes=4, places=3, reservoir=80, remarques="Fourgon et Passenger / SpaceClass")
L += g("Trafic", "X82", "2", "2021-09", None,
       ["2.0 Blue dCi 110", "2.0 Blue dCi 130", "2.0 Blue dCi 150", "2.0 Blue dCi 170",
        ("E-Tech Electric 122", el(52, debut="2023-01"))], portes=4, places=3, reservoir=80,
       remarques="Fourgon et Passenger / SpaceClass")
L += g("Master", "X62", "1", "2010-04", "2019-06",
       ["2.3 dCi 100", "2.3 dCi 110", "2.3 dCi 125", "2.3 dCi 130", "2.3 dCi 150", "2.3 dCi 165",
        ("Z.E. 76", el(33, debut="2018-03"))], portes=4, places=3, reservoir=100, remarques="Master III — grand fourgon")
L += g("Master", "X62", "2", "2019-07", "2024-03",
       ["2.3 dCi 135", "2.3 dCi 150", "2.3 dCi 180", ("Z.E. 76", el(33))], portes=4, places=3, reservoir=100,
       remarques="Master III — grand fourgon")
L += g("Master", "X90", "1", "2024-04", None,
       ["2.0 Blue dCi 105", "2.0 Blue dCi 130", "2.0 Blue dCi 150", "2.0 Blue dCi 170",
        ("E-Tech Electric 130", el(40)), ("E-Tech Electric 143", el(87))], portes=4, places=3, reservoir=93,
       remarques="Master IV — grand fourgon")

# ---------------------------------------------------------------- Moteurs
D, E_ = "DSL", "ESS"
FAMILLES = {
    # essence atmosphérique
    "C3G": f("ATM", E_, 1.2, "CHAINE", 4, 5300, 2500, "15W40", 3.0, 10000),
    "D7F": f("ATM", E_, 1.2, "COURROIE", 4, 5250, 2500, "10W40", 3.4, 15000),
    "D4F": f("ATM", E_, 1.2, "COURROIE", 4, 5500, 4250, "5W40", 4.0, 20000),
    "K7J": f("ATM", E_, 1.4, "COURROIE", 4, 5500, 2500, "10W40", 3.4, 15000),
    "K4J": f("ATM", E_, 1.4, "COURROIE", 4, 6000, 3750, "5W40", 4.8, 20000),
    "K7M": f("ATM", E_, 1.6, "COURROIE", 4, 5250, 2500, "10W40", 3.4, 15000),
    "K4M": f("ATM", E_, 1.6, "COURROIE", 4, 6000, 4250, "5W40", 4.8, 20000),
    "F3R": f("ATM", E_, 2.0, "COURROIE", 4, 5400, 4250, "10W40", 5.0, 15000),
    "F7R": f("ATM", E_, 2.0, "COURROIE", 4, 6000, 4500, "10W40", 5.0, 15000),
    "F4R": f("ATM", E_, 2.0, "COURROIE", 4, 5500, 3750, "5W40", 5.2, 20000),
    "F4R-RS": f("ATM", E_, 2.0, "COURROIE", 4, 7250, 5400, "5W40", 5.2, 20000),
    "M4R": f("ATM", E_, 2.0, "CHAINE", 4, 6000, 3750, "5W30", 4.6, 20000),
    "H4D": f("ATM", E_, 1.0, "CHAINE", 3, 6300, 3500, "5W40", 4.1, 20000),
    "L7X": f("ATM", E_, 3.0, "COURROIE", 6, 6000, 3750, "5W40", 5.5, 20000, a="V"),
    "V4Y": f("ATM", E_, 3.5, "CHAINE", 6, 6000, 4400, "5W30", 5.0, 20000, a="V"),
    "QR25": f("ATM", E_, 2.5, "CHAINE", 4, 6000, 4400, "5W30", 4.5, 20000),
    # essence turbo
    "D4FT": f("TURBO", E_, 1.2, "COURROIE", 4, 5500, 3000, "5W40", 4.0, 20000),
    "H4Bt": f("TURBO", E_, 0.9, "CHAINE", 3, 5250, 2500, "5W40", 4.1, 20000),
    "H4Dt": f("TURBO", E_, 1.0, "CHAINE", 3, 5000, 2750, "5W30", 4.1, 30000),
    "H4Dt-LPG": f("TURBO", "LPG", 1.0, "CHAINE", 3, 5000, 2750, "5W30", 4.1, 30000),
    "H4Jt": f("TURBO", E_, 1.4, "COURROIE", 4, 5500, 2250, "5W40", 4.8, 20000),
    "H5Ft": f("TURBO", E_, 1.2, "CHAINE", 4, 5500, 2000, "5W40", 4.5, 30000),
    "H5Ht": f("TURBO", E_, 1.3, "CHAINE", 4, 5000, 1600, "5W30", 5.0, 30000),
    "H5Ht-MHEV": f("HYB_TE", E_, 1.3, "CHAINE", 4, 5000, 1600, "0W20", 5.0, 30000),
    "HR12-MHEV": f("HYB_TE", E_, 1.2, "CHAINE", 3, 5000, 1750, "0W20", 4.5, 30000),
    "HR12-ETECH": f("HYB_TE", E_, 1.2, "CHAINE", 3, 5000, 1750, "0W20", 4.5, 30000),
    "HR12-ETECH-PHEV": f("HYB_TE", E_, 1.2, "CHAINE", 3, 5000, 1750, "0W20", 4.5, 30000),
    "HR16-ETECH": f("HYB_E", E_, 1.6, "CHAINE", 4, 5600, 3600, "0W20", 4.3, 30000),
    "HR16-ETECH-PHEV": f("HYB_E", E_, 1.6, "CHAINE", 4, 5600, 3600, "0W20", 4.3, 30000),
    "F4RT": f("TURBO", E_, 2.0, "COURROIE", 4, 5000, 3250, "5W40", 5.2, 20000),
    "F4RT-RS": f("TURBO", E_, 2.0, "COURROIE", 4, 5500, 3000, "5W40", 5.2, 20000),
    "M5Mt": f("TURBO", E_, 1.6, "CHAINE", 4, 6000, 2000, "5W30", 4.8, 30000),
    "M5P": f("TURBO", E_, 1.8, "CHAINE", 4, 6000, 2400, "5W30", 5.5, 30000),
    # diesel
    "F8Q": f("ATM", D, 1.9, "COURROIE", 4, 4500, 2250, "10W40", 5.0, 10000),
    "F9Q": f("TURBO", D, 1.9, "COURROIE", 4, 4000, 2000, "5W40", 4.6, 20000),
    "K9K": f("TURBO", D, 1.5, "COURROIE", 4, 4000, 1750, "5W30", 4.5, 20000),
    "K9K-HYB": f("TURBO", D, 1.5, "COURROIE", 4, 4000, 1750, "5W30", 4.5, 20000),
    "R9M": f("TURBO", D, 1.6, "CHAINE", 4, 4000, 1750, "5W30", 5.5, 30000),
    "R9N": f("TURBO", D, 1.7, "CHAINE", 4, 3500, 1750, "0W30", 5.5, 30000),
    "M9R": f("TURBO", D, 2.0, "CHAINE", 4, 3750, 2000, "5W30", 6.3, 30000),
    "G9T": f("TURBO", D, 2.2, "COURROIE", 4, 4000, 2000, "5W30", 6.0, 20000),
    "G9U": f("TURBO", D, 2.5, "CHAINE", 4, 3500, 1500, "5W30", 6.5, 30000),
    "M9T": f("TURBO", D, 2.3, "CHAINE", 4, 3500, 1500, "5W30", 7.0, 40000),
    "P9X": f("TURBO", D, 3.0, "CHAINE", 6, 4000, 1800, "5W30", 7.0, 20000, a="V"),
    "V9X": f("TURBO", D, 3.0, "CHAINE", 6, 3750, 1750, "5W30", 6.5, 30000, a="V"),
    # électrique
    "ZOE-EV": electrique(), "ZE-EV": electrique(), "CMF-EV": electrique(), "AMPR-EV": electrique(),
}

TABLE = {
    # essence atmosphérique
    "1.2 55@C06": ("C3G", 55, 83), "1.2 55": ("D7F", 55, 93), "1.2 58": ("D7F", 58, 93), "1.2 60": ("D7F", 60, 93),
    "1.2 16v 75": ("D4F", 75, 107), "1.4 75": ("K7J", 75, 114), "1.4 16v 80": ("K4J", 80, 127),
    "1.4 16v 95": ("K4J", 95, 127), "1.4 16v 98": ("K4J", 98, 127), "1.4 16v 100": ("K4J", 100, 127),
    "1.6 90": ("K7M", 90, 128), "1.6 16v 95": ("K4M", 95, 148), "1.6 16v 105": ("K4M", 105, 148),
    "1.6 16v 110": ("K4M", 110, 151), "1.6 16v 115": ("K4M", 115, 152), "1.6 133": ("K4M", 133, 160),
    "1.8 16v 120": ("F4P", 120, 165), "2.0 16v 120": ("F4R", 120, 168), "2.0 115": ("F3R", 115, 168), "2.0 16v 150": ("F7R", 150, 190),
    "2.0 16v 135": ("F4R", 135, 191), "2.0 16v 140@F4R": ("F4R", 140, 191), "2.0 16v 140": ("M4R", 140, 195),
    "2.0 16v 140@BA": ("F4R", 140, 188), "2.0 172": ("F4R-RS", 172, 200), "2.0 182": ("F4R-RS", 182, 200),
    "2.0 197": ("F4R-RS", 197, 215), "2.0 203": ("F4R-RS", 203, 215),
    "V6 3.0 230": ("L7X", 230, 300), "V6 3.0 255": ("L7X", 255, 300), "3.0 V6 207": ("L7X", 207, 285),
    "3.5 V6 240": ("Nissan", "V4Y", 240, 330), "3.5 V6 245": ("Nissan", "V4Y", 245, 330),
    "2.5 170": ("Nissan", "QR25", 170, 226),
    "1.0 SCe 65": ("H4D", 65, 95), "1.0 SCe 70": ("H4D", 70, 91), "1.0 SCe 75": ("H4D", 75, 95),
    # essence turbo
    "1.2 TCe 100": ("D4FT", 100, 145), "0.9 TCe 75": ("H4Bt", 75, 120), "0.9 TCe 90": ("H4Bt", 90, 135),
    "0.9 TCe 95": ("H4Bt", 95, 135), "0.9 TCe 110": ("H4Bt", 110, 170),
    "1.0 TCe 90": ("H4Dt", 90, 160), "1.0 TCe 100": ("H4Dt", 100, 160),
    "1.0 TCe 100 LPG": ("H4Dt-LPG", 100, 170), "1.0 ECO-G 100": ("H4Dt-LPG", 100, 170),
    "1.4 TCe 130": ("H4Jt", 130, 190),
    "1.2 TCe 100": ("D4FT", 100, 145), "1.2 TCe 100@B9A": ("H5Ft", 100, 175),
    "1.2 TCe 115": ("H5Ft", 115, 190), "1.2 TCe 120 EDC": ("H5Ft", 120, 190), "1.2 TCe 130": ("H5Ft", 130, 205),
    "1.3 TCe 100": ("H5Ht", 100, 200), "1.3 TCe 115": ("H5Ht", 115, 220), "1.3 TCe 130": ("H5Ht", 130, 240),
    "1.3 TCe 130 EDC": ("H5Ht", 130, 240), "1.3 TCe 140": ("H5Ht", 140, 240), "1.3 TCe 150": ("H5Ht", 150, 250),
    "1.3 TCe 155": ("H5Ht", 155, 270), "1.3 TCe 160": ("H5Ht", 160, 270),
    "1.3 TCe mhev 140": ("H5Ht-MHEV", 140, 260), "1.3 TCe mhev 160": ("H5Ht-MHEV", 160, 270),
    "1.2 TCe mhev 130": ("HR12-MHEV", 130, 230), "E-Tech full hybrid 200": ("HR12-ETECH", 200, 410),
    "E-Tech 4x4 300": ("HR12-ETECH-PHEV", 300, 520),
    "E-Tech hybrid 140": ("HR16-ETECH", 140, 205), "E-Tech hybrid 145": ("HR16-ETECH", 145, 205),
    "E-Tech full hybrid 145": ("HR16-ETECH", 145, 205), "E-Tech Plug-in 160": ("HR16-ETECH-PHEV", 160, 205),
    "2.0 T 165": ("F4RT", 165, 270), "2.0 T 170": ("F4RT", 170, 270), "2.0 TCe 170": ("F4RT", 170, 270),
    "2.0 TCe 180": ("F4RT", 180, 300), "2.0 TCe 205": ("F4RT", 205, 300), "2.0 TCe 220": ("F4RT-RS", 220, 340),
    "2.0 T 225": ("F4RT-RS", 225, 300), "R26 2.0 T 230": ("F4RT-RS", 230, 310), "2.0 T 250": ("F4RT-RS", 250, 340),
    "2.0 T 265": ("F4RT-RS", 265, 360), "2.0 T 275": ("F4RT-RS", 275, 360),
    "1.6 TCe 150": ("M5Mt", 150, 220), "1.6 TCe 165": ("M5Mt", 165, 240), "1.6 TCe 200": ("M5Mt", 200, 260),
    "1.6 TCe 205": ("M5Mt", 205, 280), "Trophy 1.6 TCe 220": ("M5Mt", 220, 280),
    "1.8 TCe 225": ("M5P", 225, 300), "1.8 TCe 280": ("M5P", 280, 390), "Trophy 1.8 TCe 300": ("M5P", 300, 400),
    "1.8 TCe 300": ("M5P", 300, 400),
    # diesel
    "1.9 D 55": ("F8Q", 55, 118), "1.9 D 65": ("F8Q", 65, 120), "1.9 dTi 80": ("F9Q", 80, 160),
    "1.9 dTi 100": ("F9Q", 100, 200), "1.9 dCi 82": ("F9Q", 82, 180), "1.9 dCi 100": ("F9Q", 100, 200),
    "1.9 dCi 110": ("F9Q", 110, 240), "1.9 dCi 120": ("F9Q", 120, 300), "1.9 dCi 130": ("F9Q", 130, 300),
    "1.5 dCi 57": ("K9K", 57, 140), "1.5 dCi 65": ("K9K", 65, 160), "1.5 dCi 70": ("K9K", 70, 160),
    "1.5 dCi 75": ("K9K", 75, 180), "1.5 dCi 80": ("K9K", 80, 185), "1.5 dCi 85": ("K9K", 85, 200),
    "1.5 dCi 90": ("K9K", 90, 220), "1.5 dCi 95": ("K9K", 95, 240), "1.5 dCi 100": ("K9K", 100, 200),
    "1.5 dCi 105": ("K9K", 105, 240), "1.5 dCi 110": ("K9K", 110, 260),
    "1.5 Blue dCi 75": ("K9K", 75, 230), "1.5 Blue dCi 85": ("K9K", 85, 220), "1.5 Blue dCi 95": ("K9K", 95, 240),
    "1.5 Blue dCi 100": ("K9K", 100, 260), "1.5 Blue dCi 115": ("K9K", 115, 260),
    "Hybrid Assist 1.5 dCi 110": ("K9K-HYB", 110, 260),
    "1.6 dCi 90": ("R9M", 90, 260), "1.6 dCi 115": ("R9M", 115, 300), "1.6 dCi 120": ("R9M", 120, 320),
    "1.6 dCi 125": ("R9M", 125, 320), "1.6 dCi 130": ("R9M", 130, 320), "1.6 dCi 140": ("R9M", 140, 340),
    "1.6 dCi 160": ("R9M", 160, 380), "1.6 dCi 165": ("R9M", 165, 380),
    "1.7 Blue dCi 120": ("R9N", 120, 300), "1.7 Blue dCi 150": ("R9N", 150, 340),
    "2.0 dCi 90": ("M9R", 90, 240), "2.0 dCi 115": ("M9R", 115, 290), "2.0 dCi 130": ("M9R", 130, 320),
    "2.0 dCi 150": ("M9R", 150, 340), "2.0 dCi 160": ("M9R", 160, 380), "2.0 dCi 175": ("M9R", 175, 360),
    "2.0 Blue dCi 105": ("M9R", 105, 320), "2.0 Blue dCi 110": ("M9R", 110, 300),
    "2.0 Blue dCi 120": ("M9R", 120, 320), "2.0 Blue dCi 130": ("M9R", 130, 330),
    "2.0 Blue dCi 145": ("M9R", 145, 350), "2.0 Blue dCi 150": ("M9R", 150, 370),
    "2.0 Blue dCi 160": ("M9R", 160, 360), "2.0 Blue dCi 170": ("M9R", 170, 380),
    "2.0 Blue dCi 190": ("M9R", 190, 400), "2.0 Blue dCi 200": ("M9R", 200, 400),
    "2.2 dCi 150": ("G9T", 150, 320), "2.5 dCi 135": ("G9U", 135, 300), "2.5 dCi 146": ("G9U", 146, 320),
    "2.3 dCi 100": ("M9T", 100, 285), "2.3 dCi 110": ("M9T", 110, 285), "2.3 dCi 125": ("M9T", 125, 310),
    "2.3 dCi 130": ("M9T", 130, 330), "2.3 dCi 135": ("M9T", 135, 360), "2.3 dCi 150": ("M9T", 150, 350),
    "2.3 dCi 165": ("M9T", 165, 360), "2.3 dCi 180": ("M9T", 180, 400),
    "3.0 dCi 180": ("Isuzu", "P9X", 180, 400), "3.0 dCi 235": ("Nissan", "V9X", 235, 450),
    # électrique
    "R240 88": ("ZOE-EV", 88, 220), "Q90": ("ZOE-EV", 88, 220), "R90": ("ZOE-EV", 92, 220),
    "R110": ("ZOE-EV", 108, 225), "R135": ("ZOE-EV", 135, 245),
    "Electric 82": ("ZE-EV", 82, 160), "Z.E. 60": ("ZE-EV", 60, 226), "Z.E. 33": ("ZE-EV", 60, 225),
    "Z.E. 76": ("ZE-EV", 76, 225), "Z.E. 95": ("ZE-EV", 95, 226),
    "EV40 130": ("CMF-EV", 130, 250), "EV60 130": ("CMF-EV", 130, 250), "EV60 220": ("CMF-EV", 220, 300),
    "Comfort Range 170": ("CMF-EV", 170, 280), "Long Range 220": ("CMF-EV", 220, 300),
    "E-Tech Electric 122": ("CMF-EV", 122, 245), "E-Tech Electric 130": ("CMF-EV", 130, 300),
    "E-Tech Electric 143": ("CMF-EV", 143, 300),
    "Urban Range 120": ("AMPR-EV", 120, 225), "Comfort Range 150": ("AMPR-EV", 150, 245),
    "Comfort Range 120": ("AMPR-EV", 120, 225),
}
FAMILLES["F4P"] = f("ATM", E_, 1.8, "COURROIE", 4, 5750, 3750, "5W40", 5.2, 20000)

ERES = {"C06": "C06", "BA": "BA", "G": "F4R", "JM": "F4R", "JK": "F4R", "B9A": "B9A"}

MOT = Motorisations("Renault", FAMILLES, TABLE, ERES, prefixes=PREFIXES + ("RS ",))
MOT.lier(L)

DETAIL = {"Renault": L}
MOTEURS = MOT.moteurs()
