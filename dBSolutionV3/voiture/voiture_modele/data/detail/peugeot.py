"""Peugeot : générations, phases, motorisations (marché européen) et moteurs PSA liés."""
from ._outil import Motorisations, electrique, famille as f, gamme as g

E = {"reservoir": 0}  # électrique : pas de réservoir


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


L = []

# ---------------------------------------------------------------- 107 / 108
L += g("107", "PN", "1", "2005-06", "2008-12", ["1.0 68", "1.4 HDi 54"], places=4, reservoir=35,
       remarques="3 et 5 portes")
L += g("107", "PN", "2", "2009-01", "2012-03", ["1.0 68", ("1.4 HDi 54", {"fin": "2010-12"})], places=4,
       reservoir=35, remarques="3 et 5 portes")
L += g("107", "PN", "3", "2012-04", "2014-05", ["1.0 68"], places=4, reservoir=35, remarques="3 et 5 portes")
L += g("108", "P1", "1", "2014-06", "2018-05", ["1.0 VTi 68", "1.2 PureTech 82"], places=4, reservoir=35,
       remarques="3 et 5 portes, TOP! découvrable")
L += g("108", "P1", "2", "2018-06", "2021-12", ["1.0 VTi 72"], places=4, reservoir=35,
       remarques="3 et 5 portes, TOP! découvrable")

# ---------------------------------------------------------------- 205 / 206 / 207
L += g("205", "205", "1", "1983-02", "1998-12",
       ["1.0 45", "1.1 55", "1.4 75", "1.6 GTI 105", ("1.6 GTI 115", {"debut": "1987"}),
        ("1.9 GTI 130", {"debut": "1986", "fin": "1994"}), "1.8 D 60", ("1.8 TD 78", {"debut": "1988"})],
       reservoir=50, remarques="3 et 5 portes, Cabriolet CJ/CT")
L += g("206", "206", "1", "1998-09", "2003-05",
       ["1.1 60", "1.4 75", "1.6 90", "1.6 16v 110", ("2.0 S16 136", {"debut": "1999"}),
        "1.9 D 70", "2.0 HDi 90", ("1.4 HDi 68", {"debut": "2001"})],
       reservoir=50, remarques="3 et 5 portes, CC, SW (2002)")
L += g("206", "206", "2", "2003-06", "2009-01",
       ["1.1 60", "1.4 75", "1.4 16v 90", "1.6 16v 110", "2.0 GTi 138", ("2.0 RC 177", {"fin": "2006"}),
        "1.4 HDi 68", "1.6 HDi 110", "2.0 HDi 90"],
       reservoir=50, remarques="3 et 5 portes, CC, SW")
L += g("206", "206+", "1", "2009-02", "2012-12", ["1.1 60", "1.4 75", "1.4 HDi 70"], reservoir=50,
       remarques="3 et 5 portes")
L += g("207", "A7", "1", "2006-04", "2009-06",
       ["1.4 75", "1.4 VTi 95", "1.6 VTi 120", "1.6 THP 150", ("GTi 1.6 THP 175", {"debut": "2007"}),
        ("RC 1.6 THP 175", {"debut": "2007"}), "1.4 HDi 68", "1.6 HDi 90", "1.6 HDi 110"],
       reservoir=50, remarques="3 et 5 portes, CC, SW")
L += g("207", "A7", "2", "2009-07", "2014-12",
       ["1.4 75", "1.4 VTi 95", "1.6 VTi 120", "1.6 THP 156", "1.4 HDi 68", "1.6 HDi 92", "1.6 HDi 112"],
       reservoir=50, remarques="3 et 5 portes, CC, SW ; berline jusqu'en 2012")

# ---------------------------------------------------------------- 208
L += g("208", "A9", "1", "2012-03", "2015-03",
       ["1.0 VTi 68", "1.2 VTi 82", "1.4 VTi 95", "1.6 VTi 120", "1.6 THP 156",
        ("GTi 1.6 THP 200", {"debut": "2013-04"}), "1.4 HDi 68", "1.6 e-HDi 92", "1.6 e-HDi 115"],
       reservoir=50, remarques="3 et 5 portes")
L += g("208", "A9", "2", "2015-04", "2019-09",
       ["1.0 PureTech 68", "1.2 PureTech 82", "1.2 PureTech 110", "GT 1.6 THP 165", "GTi 1.6 THP 208",
        "1.6 BlueHDi 75", "1.6 BlueHDi 100", "1.6 BlueHDi 120", ("1.5 BlueHDi 100", {"debut": "2018-09"})],
       reservoir=50, remarques="3 et 5 portes")
L += g("208", "P21", "1", "2019-09", "2023-09",
       ["1.2 PureTech 75", "1.2 PureTech 100", "1.2 PureTech 130 EAT8", "1.5 BlueHDi 100",
        ("e-208 136", el(50, fin="2022-12")), ("e-208 156", el(51, debut="2023-01"))],
       reservoir=44, remarques="5 portes")
L += g("208", "P21", "2", "2023-10", None,
       ["1.2 PureTech 75", "1.2 PureTech 100", ("1.5 BlueHDi 100", {"fin": "2024-12"}),
        ("1.2 Hybrid 100 e-DCS6", {"debut": "2024-03"}), ("1.2 Hybrid 136 e-DCS6", {"debut": "2024-03"}),
        ("e-208 156", el(51)), ("e-208 GTi 281", el(54, debut="2026-06", remarques="Développée par Peugeot Sport"))],
       reservoir=44, remarques="5 portes")

# ---------------------------------------------------------------- 2008
L += g("2008", "A94", "1", "2013-04", "2016-05",
       ["1.2 VTi 82", "1.6 VTi 120", "1.4 HDi 68", "1.6 e-HDi 92", "1.6 e-HDi 115"], reservoir=50)
L += g("2008", "A94", "2", "2016-06", "2019-12",
       ["1.2 PureTech 82", "1.2 PureTech 110", "1.2 PureTech 130", "1.6 BlueHDi 75", "1.6 BlueHDi 100",
        "1.6 BlueHDi 120", ("1.5 BlueHDi 100", {"debut": "2018-09"})], reservoir=50)
L += g("2008", "P24", "1", "2019-11", "2023-08",
       ["1.2 PureTech 100", "1.2 PureTech 130", "1.2 PureTech 155 EAT8", "1.5 BlueHDi 110",
        "1.5 BlueHDi 130 EAT8", ("e-2008 136", el(50, fin="2022-12")), ("e-2008 156", el(54, debut="2023-01"))],
       reservoir=44)
L += g("2008", "P24", "2", "2023-09", None,
       ["1.2 PureTech 100", "1.2 PureTech 130 EAT8", "1.5 BlueHDi 130 EAT8",
        ("1.2 Hybrid 136 e-DCS6", {"debut": "2024-03"}), ("1.2 Hybrid 145 e-DCS6", {"debut": "2025-01"}),
        ("e-2008 156", el(54))],
       reservoir=44)

# ---------------------------------------------------------------- 308 (hors GT)
L += g("308", "T7", "1", "2007-09", "2011-02",
       ["1.4 VTi 95", "1.6 VTi 120", "1.6 THP 150", "1.6 HDi 90", "1.6 HDi 110", "2.0 HDi 136"],
       reservoir=60, remarques="Berline 3 et 5 portes, SW, CC")
L += g("308", "T7", "2", "2011-03", "2013-12",
       ["1.4 VTi 98", "1.6 VTi 120", "1.6 THP 156", "1.6 HDi 92", "1.6 e-HDi 112", "2.0 HDi 150"],
       reservoir=60, remarques="Berline 3 et 5 portes, SW, CC ; SW jusqu'en 2014")
L += g("308", "T9", "1", "2013-09", "2017-07",
       ["1.2 PureTech 110", "1.2 PureTech 130", "1.6 THP 125", "1.6 THP 156", "1.6 e-HDi 92",
        "1.6 e-HDi 115", "1.6 BlueHDi 120", "2.0 BlueHDi 150"],
       reservoir=53, remarques="Berline 5 portes et SW")
L += g("308", "T9", "2", "2017-08", "2021-05",
       ["1.2 PureTech 110", "1.2 PureTech 130", "1.5 BlueHDi 100", "1.5 BlueHDi 130",
        ("1.6 BlueHDi 120", {"fin": "2018-08"}), ("2.0 BlueHDi 150", {"fin": "2018-08"})],
       reservoir=53, remarques="Berline 5 portes et SW")
L += g("308", "P5", "1", "2021-06", "2025-04",
       ["1.2 PureTech 110", "1.2 PureTech 130 EAT8", "1.5 BlueHDi 130 EAT8",
        ("Hybrid 180 e-EAT8", {"reservoir": 40, "batterie": 12}),
        ("Hybrid 225 e-EAT8", {"reservoir": 40, "batterie": 12}),
        ("e-308 156", el(54, debut="2023-05")), ("1.2 Hybrid 136 e-DCS6", {"debut": "2024-01"})],
       reservoir=52, remarques="Berline 5 portes et SW")
L += g("308", "P5", "2", "2025-05", None,
       ["1.2 Hybrid 145 e-DCS6", "1.5 BlueHDi 130 EAT8",
        ("Plug-in Hybrid 195 e-DCS7", {"reservoir": 40, "batterie": 17}), ("e-308 156", el(54))],
       reservoir=52, remarques="Berline 5 portes et SW")

# ---------------------------------------------------------------- 308 GT / GTi
B = "Berline 5 portes et SW"
L += g("308", "T7", "1", "2008-09", "2011-02", ["GT 1.6 THP 175"], reservoir=60, remarques=B + " — dates à vérifier")
L += g("308", "T7", "2", "2011-03", "2013-12",
       ["GT 2.0 HDi 163", ("GTi 1.6 THP 200", {"debut": "2010-06", "remarques": B + " — lancée en fin de phase 1 ; dates à vérifier"})],
       reservoir=60, remarques=B + " — dates à vérifier")
L += g("308", "T9", "1", "2014-12", "2017-07",
       ["GT 1.6 THP 205", "GT 2.0 BlueHDi 180 EAT6", ("GTi 270", {"debut": "2015-09", "remarques": B + " — dates à vérifier"})],
       reservoir=53, remarques=B)
L += g("308", "T9", "2", "2017-08", "2020-07",
       ["GT 2.0 BlueHDi 180 EAT8", ("GT 1.6 PureTech 225 EAT8", {"debut": "2018-02"}),
        ("GT 1.2 PureTech 130", {"debut": "2020-08", "fin": "2021-11", "remarques": B + " — fin SW à vérifier"}),
        ("GT 1.5 BlueHDi 130", {"debut": "2020-08", "fin": "2021-11", "remarques": B + " — fin SW à vérifier"}),
        ("GTi 263", {"debut": "2019-01", "fin": "2021-05", "remarques": B + " — ex-GTi 270 (norme WLTP) ; dates à vérifier"})],
       reservoir=53, remarques=B)
L += g("308", "P5", "1", "2021-06", "2025-04",
       [("GT 1.2 PureTech 130 EAT8", {"remarques": B + " — fin de phase 1 approximative"}),
        ("GT 1.5 BlueHDi 130 EAT8", {"remarques": B + " — fin de phase 1 approximative"}),
        ("GT Hybrid 180 e-EAT8", {"reservoir": 40, "batterie": 12, "remarques": B + " — hybride rechargeable ; batterie 12,4 kWh"}),
        ("GT Hybrid 225 e-EAT8", {"reservoir": 40, "batterie": 12, "remarques": B + " — hybride rechargeable ; batterie 12,4 kWh"}),
        ("e-308 GT", {"reservoir": 0, "batterie": 54, "debut": "2023-05", "remarques": B + " — 100 % électrique ; dates à vérifier"}),
        ("GT 1.2 Hybrid 136 e-DCS6", {"debut": "2024-01", "remarques": B + " — hybride léger 48 V ; dates à vérifier"})],
       reservoir=52)
L += g("308", "P5", "2", "2025-05", None,
       [("GT Hybrid 145 e-DCS6", {"remarques": B + " — hybride léger 48 V ; date de début approximative"}),
        ("GT Plug-in Hybrid 195 e-DCS7", {"reservoir": 40, "batterie": 17, "remarques": B + " — hybride rechargeable ; date de début approximative ; batterie 17,2 kWh"}),
        ("e-308 GT", {"reservoir": 0, "batterie": 54, "remarques": B + " — 100 % électrique ; batterie et date à vérifier"})],
       reservoir=52)

# ---------------------------------------------------------------- 3008
L += g("3008", "T84", "1", "2009-05", "2013-09",
       ["1.6 VTi 120", "1.6 THP 156", "1.6 HDi 112", "2.0 HDi 150", "2.0 HDi 163",
        ("HYbrid4 2.0 HDi 200", {"debut": "2012-01"})], reservoir=60)
L += g("3008", "T84", "2", "2013-10", "2016-09",
       ["1.6 VTi 120", "1.6 THP 156", "1.6 e-HDi 115", "1.6 BlueHDi 120", "2.0 HDi 150", "2.0 BlueHDi 150",
        "HYbrid4 2.0 HDi 200"], reservoir=60)
L += g("3008", "P84", "1", "2016-10", "2020-09",
       ["1.2 PureTech 130", "1.6 THP 165", ("1.6 PureTech 180 EAT8", {"debut": "2018-09"}),
        "1.6 BlueHDi 120", ("1.5 BlueHDi 130", {"debut": "2018-09"}), "2.0 BlueHDi 150",
        "2.0 BlueHDi 180", ("Hybrid 225 e-EAT8", {"debut": "2020-01", "reservoir": 43, "batterie": 13}),
        ("Hybrid4 300 e-EAT8", {"debut": "2020-01", "reservoir": 43, "batterie": 13})],
       reservoir=53)
L += g("3008", "P84", "2", "2020-10", "2023-12",
       ["1.2 PureTech 130", "1.6 PureTech 180 EAT8", "1.5 BlueHDi 130",
        ("Hybrid 136 e-DCS6", {"debut": "2023-06"}),
        ("Hybrid 225 e-EAT8", {"reservoir": 43, "batterie": 13}),
        ("Hybrid4 300 e-EAT8", {"reservoir": 43, "batterie": 13})],
       reservoir=53)
L += g("3008", "P64", "1", "2024-01", None,
       ["1.2 Hybrid 136 e-DCS6", ("1.2 Hybrid 145 e-DCS6", {"debut": "2025-01"}),
        ("Plug-in Hybrid 195 e-DCS7", {"debut": "2024-06", "reservoir": 40, "batterie": 21}),
        ("e-3008 210", el(73)), ("e-3008 Long Range 230", el(98, debut="2024-09")),
        ("e-3008 Dual Motor 325", el(73, debut="2024-09"))],
       reservoir=55, remarques="SUV coupé")

# ---------------------------------------------------------------- 5008
L += g("5008", "T87", "1", "2009-09", "2013-09",
       ["1.6 VTi 120", "1.6 THP 156", "1.6 HDi 112", "2.0 HDi 150", "2.0 HDi 163"], places=7, reservoir=60,
       remarques="Monospace 5 ou 7 places")
L += g("5008", "T87", "2", "2013-10", "2017-02",
       ["1.6 VTi 120", "1.6 THP 156", "1.6 e-HDi 115", "1.6 BlueHDi 120", "2.0 BlueHDi 150"], places=7,
       reservoir=60, remarques="Monospace 5 ou 7 places")
L += g("5008", "P87", "1", "2017-03", "2020-09",
       ["1.2 PureTech 130", "1.6 THP 165", ("1.6 PureTech 180 EAT8", {"debut": "2018-09"}), "1.6 BlueHDi 120",
        ("1.5 BlueHDi 130", {"debut": "2018-09"}), "2.0 BlueHDi 150", "2.0 BlueHDi 180"],
       places=7, reservoir=56, remarques="SUV 7 places")
L += g("5008", "P87", "2", "2020-10", "2024-03",
       ["1.2 PureTech 130", "1.6 PureTech 180 EAT8", "1.5 BlueHDi 130", ("Hybrid 136 e-DCS6", {"debut": "2023-06"})],
       places=7, reservoir=56, remarques="SUV 7 places")
L += g("5008", "P97", "1", "2024-09", None,
       ["1.2 Hybrid 136 e-DCS6", ("1.2 Hybrid 145 e-DCS6", {"debut": "2025-01"}),
        ("Plug-in Hybrid 195 e-DCS7", {"debut": "2025-01", "reservoir": 40, "batterie": 21}),
        ("e-5008 210", el(73)), ("e-5008 Long Range 230", el(98)), ("e-5008 Dual Motor 325", el(73))],
       places=7, reservoir=55, remarques="SUV 7 places")

# ---------------------------------------------------------------- 408
L += g("408", "P54", "1", "2022-06", None,
       ["1.2 PureTech 130 EAT8", ("Hybrid 180 e-EAT8", {"reservoir": 40, "batterie": 12}),
        ("Hybrid 225 e-EAT8", {"reservoir": 40, "batterie": 12}),
        ("1.2 Hybrid 136 e-DCS6", {"debut": "2024-01"}), ("1.2 Hybrid 145 e-DCS6", {"debut": "2025-01"}),
        ("e-408 210", el(58, debut="2024-06"))],
       reservoir=52, remarques="Fastback")

# ---------------------------------------------------------------- 508
L += g("508", "W2", "1", "2011-03", "2014-10",
       ["1.6 VTi 120", "1.6 THP 156", "1.6 e-HDi 112", "2.0 HDi 140", "2.0 HDi 163", "GT 2.2 HDi 204",
        ("RXH HYbrid4 200", {"debut": "2012-03"})], reservoir=72, remarques="Berline 4 portes, SW, RXH")
L += g("508", "W2", "2", "2014-11", "2018-09",
       ["1.6 THP 165", "1.6 BlueHDi 120", "2.0 BlueHDi 150", "GT 2.0 BlueHDi 180", "RXH HYbrid4 200"],
       reservoir=72, remarques="Berline 4 portes, SW, RXH")
L += g("508", "R8", "1", "2018-10", "2023-05",
       ["1.6 PureTech 180 EAT8", "GT 1.6 PureTech 225 EAT8", "1.5 BlueHDi 130", "2.0 BlueHDi 160",
        "GT 2.0 BlueHDi 180", ("Hybrid 225 e-EAT8", {"debut": "2019-10", "reservoir": 43, "batterie": 12}),
        ("PSE Hybrid4 360", {"debut": "2020-10", "reservoir": 43, "batterie": 12})],
       reservoir=62, remarques="Fastback 5 portes et SW")
L += g("508", "R8", "2", "2023-06", None,
       ["1.2 PureTech 130 EAT8", "1.5 BlueHDi 130 EAT8",
        ("Hybrid 180 e-EAT8", {"reservoir": 43, "batterie": 12}),
        ("Hybrid 225 e-EAT8", {"reservoir": 43, "batterie": 12}),
        ("PSE Hybrid4 360", {"reservoir": 43, "batterie": 12, "fin": "2023-12"})],
       reservoir=62, remarques="Fastback 5 portes et SW")

# ---------------------------------------------------------------- Utilitaires / ludospaces
L += g("Partner", "M59", "1", "1996-07", "2008-03", ["1.4 75", "1.6 HDi 75", "1.9 D 70", "2.0 HDi 90"],
       places=2, reservoir=55, remarques="Fourgonnette ; Partner Combi 5 places")
L += g("Partner", "B9", "1", "2008-04", "2012-03", ["1.6 VTi 98", "1.6 HDi 75", "1.6 HDi 90", "1.6 HDi 110"],
       places=3, reservoir=60, remarques="Fourgon ; Tepee 5/7 places")
L += g("Partner", "B9", "2", "2012-04", "2018-06",
       ["1.6 VTi 98", "1.6 HDi 75", "1.6 BlueHDi 75", "1.6 BlueHDi 100", "1.6 BlueHDi 120",
        ("Electric 67", el(23, debut="2013-06"))], places=3, reservoir=60, remarques="Fourgon ; Tepee 5/7 places")
L += g("Partner", "K9", "1", "2018-06", "2024-05",
       ["1.2 PureTech 110", "1.5 BlueHDi 75", "1.5 BlueHDi 100", "1.5 BlueHDi 130",
        ("e-Partner 136", el(50, debut="2021-01"))], places=3, reservoir=50, remarques="Fourgon")
L += g("Partner", "K9", "2", "2024-06", None,
       ["1.5 BlueHDi 100", "1.5 BlueHDi 130", ("e-Partner 136", el(50))], places=3, reservoir=50,
       remarques="Fourgon")
L += g("Rifter", "K9", "1", "2018-06", "2024-05",
       ["1.2 PureTech 110", "1.2 PureTech 130", "1.5 BlueHDi 100", "1.5 BlueHDi 130",
        ("e-Rifter 136", el(50, debut="2021-09"))], places=5, reservoir=50, remarques="Ludospace 5 ou 7 places")
L += g("Rifter", "K9", "2", "2024-06", None,
       ["1.2 PureTech 110", "1.5 BlueHDi 100", "1.5 BlueHDi 130", ("e-Rifter 136", el(50))], places=5,
       reservoir=50, remarques="Ludospace 5 ou 7 places")
L += g("Expert", "G9", "1", "2007-01", "2016-05",
       ["1.6 HDi 90", "2.0 HDi 120", "2.0 HDi 136", "2.0 HDi 163"], portes=4, places=3, reservoir=80,
       remarques="Fourgon ; dates de phases non détaillées")
L += g("Expert", "K0", "1", "2016-06", "2024-05",
       ["1.5 BlueHDi 100", "1.5 BlueHDi 120", "1.6 BlueHDi 95", "1.6 BlueHDi 115", "2.0 BlueHDi 120",
        "2.0 BlueHDi 150", "2.0 BlueHDi 180", ("e-Expert 136", el(50, debut="2020-09")),
        ("e-Expert 136 75 kWh", el(75, debut="2020-09"))], portes=4, places=3, reservoir=69, remarques="Fourgon")
L += g("Expert", "K0", "2", "2024-06", None,
       ["2.0 BlueHDi 145", "2.0 BlueHDi 180", ("e-Expert 136", el(50)), ("e-Expert 136 75 kWh", el(75))],
       portes=4, places=3, reservoir=69, remarques="Fourgon")
L += g("Traveller", "K0", "1", "2016-06", "2024-05",
       ["1.6 BlueHDi 115", "2.0 BlueHDi 150", "2.0 BlueHDi 180", ("e-Traveller 136", el(50, debut="2020-09")),
        ("e-Traveller 136 75 kWh", el(75, debut="2020-09"))], places=8, reservoir=69,
       remarques="Minibus 5 à 9 places")
L += g("Traveller", "K0", "2", "2024-06", None,
       ["2.0 BlueHDi 145", "2.0 BlueHDi 180", ("e-Traveller 136", el(75))], places=8, reservoir=69,
       remarques="Minibus 5 à 9 places")
L += g("Boxer", "250", "1", "2006-07", "2014-05", ["2.2 HDi 100", "2.2 HDi 120", "3.0 HDi 157"],
       portes=4, places=3, reservoir=90, remarques="Grand fourgon")
L += g("Boxer", "250", "2", "2014-06", None,
       ["2.0 BlueHDi 110", "2.0 BlueHDi 130", "2.0 BlueHDi 160", "2.2 BlueHDi 140", "2.2 BlueHDi 165",
        "2.2 BlueHDi 180", ("e-Boxer 122", el(75, debut="2021-01"))],
       portes=4, places=3, reservoir=90, remarques="Grand fourgon ; restylage 2024 non détaillé")

# ---------------------------------------------------------------- Moteurs PSA (et fournisseurs)
FAMILLES = {
    # essence ancienne génération
    "XV8": f("ATM", "ESS", 1.0, "CHAINE", 4, 6000, 3000, "15W40", 4.0, 7500),
    "XW7": f("ATM", "ESS", 1.1, "CHAINE", 4, 5800, 3000, "15W40", 4.0, 7500),
    "TU1": f("ATM", "ESS", 1.1, "COURROIE", 4, 5500, 3400, "10W40", 3.2, 15000),
    "TU3": f("ATM", "ESS", 1.4, "COURROIE", 4, 5500, 3400, "10W40", 3.2, 15000),
    "ET3J4": f("ATM", "ESS", 1.4, "COURROIE", 4, 5250, 3250, "5W40", 3.2, 20000),
    "TU5": f("ATM", "ESS", 1.6, "COURROIE", 4, 5600, 3000, "10W40", 3.2, 15000),
    "TU5J4": f("ATM", "ESS", 1.6, "COURROIE", 4, 5750, 4000, "5W40", 3.2, 20000),
    "XU5J": f("ATM", "ESS", 1.6, "COURROIE", 4, 6250, 4000, "15W40", 5.0, 10000),
    "XU9J": f("ATM", "ESS", 1.9, "COURROIE", 4, 6000, 4750, "15W40", 5.0, 10000),
    "EW10J4": f("ATM", "ESS", 2.0, "COURROIE", 4, 6000, 4100, "5W40", 4.25, 20000),
    "EW10J4S": f("ATM", "ESS", 2.0, "COURROIE", 4, 7000, 4750, "5W40", 4.25, 20000),
    # essence Prince (BMW/PSA) et PureTech
    "EP3": f("ATM", "ESS", 1.4, "CHAINE", 4, 6000, 4000, "5W30", 4.25, 20000),
    "EP6": f("ATM", "ESS", 1.6, "CHAINE", 4, 6000, 4250, "5W30", 4.25, 20000),
    "EP6DT": f("TURBO", "ESS", 1.6, "CHAINE", 4, 5800, 1400, "5W30", 4.25, 20000),
    "EP6CDT": f("TURBO", "ESS", 1.6, "CHAINE", 4, 6000, 1400, "5W30", 4.25, 20000),
    "EP6DTS": f("TURBO", "ESS", 1.6, "CHAINE", 4, 6000, 1600, "5W30", 4.25, 20000),
    "EP6CDTX": f("TURBO", "ESS", 1.6, "CHAINE", 4, 5800, 1700, "5W30", 4.25, 20000),
    "EP6CDTR": f("TURBO", "ESS", 1.6, "CHAINE", 4, 6000, 3000, "5W30", 4.25, 20000),
    "EP6FDTX": f("TURBO", "ESS", 1.6, "CHAINE", 4, 6000, 1750, "0W30", 4.25, 20000),
    "EP6FDTR": f("TURBO", "ESS", 1.6, "CHAINE", 4, 6000, 1900, "0W30", 4.25, 20000),
    "EP6FADTX": f("TURBO", "ESS", 1.6, "CHAINE", 4, 5500, 1900, "0W30", 4.25, 20000),
    "EP6FADTXD": f("TURBO", "ESS", 1.6, "CHAINE", 4, 5500, 1650, "0W30", 4.25, 20000),
    "EP6-PHEV": f("HYB_TE", "ESS", 1.6, "CHAINE", 4, 6000, 1900, "0W30", 4.25, 20000),
    "EB0": f("ATM", "ESS", 1.0, "COURROIE", 3, 6000, 3000, "0W30", 3.25, 20000),
    "EB2F": f("ATM", "ESS", 1.2, "COURROIE", 3, 5750, 2750, "0W30", 3.25, 20000),
    "EB2FA": f("ATM", "ESS", 1.2, "COURROIE", 3, 5750, 2750, "0W30", 3.25, 20000),
    "EB2DT": f("TURBO", "ESS", 1.2, "COURROIE", 3, 5500, 1500, "0W30", 3.5, 20000),
    "EB2ADT": f("TURBO", "ESS", 1.2, "COURROIE", 3, 5500, 1750, "0W30", 3.5, 20000),
    "EB2DTS": f("TURBO", "ESS", 1.2, "COURROIE", 3, 5500, 1750, "0W30", 3.5, 20000),
    "EB2ADTS": f("TURBO", "ESS", 1.2, "COURROIE", 3, 5500, 1750, "0W20", 3.5, 20000),
    "EB2-MHEV": f("HYB_TE", "ESS", 1.2, "CHAINE", 3, 5500, 1750, "0W20", 3.5, 20000),
    # diesel
    "XUD7": f("ATM", "DSL", 1.8, "COURROIE", 4, 4600, 2000, "15W40", 5.0, 10000),
    "XUD7TE": f("TURBO", "DSL", 1.8, "COURROIE", 4, 4300, 2100, "15W40", 5.0, 10000),
    "DW8": f("ATM", "DSL", 1.9, "COURROIE", 4, 4600, 2500, "10W40", 4.5, 15000),
    "DV4TD": f("TURBO", "DSL", 1.4, "COURROIE", 4, 4000, 1750, "5W30", 3.75, 20000),
    "DV4C": f("TURBO", "DSL", 1.4, "COURROIE", 4, 4000, 1750, "5W30", 3.75, 20000),
    "DV6ATED4": f("TURBO", "DSL", 1.6, "COURROIE", 4, 4000, 1750, "5W30", 3.75, 20000),
    "DV6BTED4": f("TURBO", "DSL", 1.6, "COURROIE", 4, 4000, 1750, "5W30", 3.75, 20000),
    "DV6TED4": f("TURBO", "DSL", 1.6, "COURROIE", 4, 4000, 1750, "5W30", 3.75, 20000),
    "DV6D": f("TURBO", "DSL", 1.6, "COURROIE", 4, 4000, 1750, "5W30", 3.75, 20000),
    "DV6C": f("TURBO", "DSL", 1.6, "COURROIE", 4, 3600, 1750, "5W30", 3.75, 20000),
    "DV6F": f("TURBO", "DSL", 1.6, "COURROIE", 4, 3500, 1750, "0W30", 3.75, 25000),
    "DV5R": f("TURBO", "DSL", 1.5, "COURROIE", 4, 3750, 1750, "0W30", 4.25, 25000),
    "DW10TD": f("TURBO", "DSL", 2.0, "COURROIE", 4, 4000, 1900, "10W40", 4.5, 15000),
    "DW10BTED4": f("TURBO", "DSL", 2.0, "COURROIE", 4, 4000, 2000, "5W30", 4.5, 20000),
    "DW10UTED4": f("TURBO", "DSL", 2.0, "COURROIE", 4, 4000, 2000, "5W30", 4.5, 20000),
    "DW10C": f("TURBO", "DSL", 2.0, "COURROIE", 4, 3750, 2000, "5W30", 5.25, 20000),
    "DW10F": f("TURBO", "DSL", 2.0, "COURROIE", 4, 3750, 2000, "0W30", 5.25, 25000),
    "DW10-HYBRID4": f("TURBO", "DSL", 2.0, "COURROIE", 4, 3750, 1750, "5W30", 5.25, 20000),
    "DW12C": f("TURBO", "DSL", 2.2, "COURROIE", 4, 3500, 2000, "5W30", 5.25, 20000),
    "DW12RU": f("TURBO", "DSL", 2.2, "COURROIE", 4, 3500, 1750, "0W30", 6.0, 25000),
    "PUMA-2.2": f("TURBO", "DSL", 2.2, "CHAINE", 4, 3500, 1800, "5W30", 6.0, 30000),
    "F1C-3.0": f("TURBO", "DSL", 3.0, "CHAINE", 4, 3500, 1700, "5W30", 6.5, 30000),
    "1KR-FE": f("ATM", "ESS", 1.0, "CHAINE", 3, 6000, 3600, "5W30", 3.2, 15000),
    # électrique
    "E-CMP": electrique(), "STLA-M": electrique(), "E-BOXER": electrique(), "PARTNER-EV": electrique(),
}

TABLE = {
    # Toyota 1.0 (107 / 108)
    "1.0 68": ("Toyota", "1KR-FE", 68, 93), "1.0 VTi 68@TOY": ("Toyota", "1KR-FE", 68, 93),
    "1.0 VTi 72": ("Toyota", "1KR-FE", 72, 93),
    # 205
    "1.0 45": ("XV8", 45, 66), "1.1 55": ("XW7", 55, 85), "1.6 GTI 105": ("XU5J", 105, 135),
    "1.6 GTI 115": ("XU5J", 115, 133), "1.9 GTI 130": ("XU9J", 130, 161), "1.8 D 60": ("XUD7", 60, 110),
    "1.8 TD 78": ("XUD7TE", 78, 157),
    # essence TU / EW
    "1.1 60": ("TU1", 60, 94), "1.4 75": ("TU3", 75, 120), "1.4 16v 90": ("ET3J4", 90, 133),
    "1.6 90": ("TU5", 90, 135), "1.6 16v 110": ("TU5J4", 110, 147), "2.0 S16 136": ("EW10J4", 136, 190),
    "2.0 GTi 138": ("EW10J4", 138, 190), "2.0 RC 177": ("EW10J4S", 177, 202),
    # Prince / THP
    "1.4 VTi 95": ("EP3", 95, 136), "1.4 VTi 98": ("EP3", 98, 133), "1.6 VTi 98": ("EP6", 98, 152),
    "1.6 VTi 120": ("EP6", 120, 160), "1.6 THP 125": ("EP6CDT", 125, 200), "1.6 THP 150": ("EP6DT", 150, 240),
    "1.6 THP 156": ("EP6CDT", 156, 240), "1.6 THP 165": ("EP6CDT", 165, 240),
    "1.6 THP 175": ("EP6DTS", 175, 240), "1.6 THP 200": ("EP6CDTX", 200, 275),
    "1.6 THP 208": ("EP6CDTR", 208, 300), "1.6 THP 205": ("EP6FDTX", 205, 285),
    "GTi 270": ("EP6FDTR", 270, 330), "GTi 263": ("EP6FDTR", 263, 330),
    "1.6 PureTech 180 EAT8": ("EP6FADTXD", 180, 250), "1.6 PureTech 225 EAT8": ("EP6FADTX", 225, 300),
    # PureTech 3 cylindres
    "1.0 VTi 68": ("EB0", 68, 95), "1.0 PureTech 68": ("EB0", 68, 95), "1.2 VTi 82": ("EB2F", 82, 118),
    "1.2 PureTech 82": ("EB2F", 82, 118), "1.2 PureTech 75": ("EB2FA", 75, 118),
    "1.2 PureTech 100": ("EB2ADT", 100, 205), "1.2 PureTech 110": ("EB2DT", 110, 205),
    "1.2 PureTech 130": ("EB2DTS", 130, 230), "1.2 PureTech 130 EAT8": ("EB2ADTS", 130, 230),
    "1.2 PureTech 155 EAT8": ("EB2ADTS", 155, 240),
    "1.2 Hybrid 100 e-DCS6": ("EB2-MHEV", 100, 205), "1.2 Hybrid 136 e-DCS6": ("EB2-MHEV", 136, 230),
    "Hybrid 136 e-DCS6": ("EB2-MHEV", 136, 230), "1.2 Hybrid 145 e-DCS6": ("EB2-MHEV", 145, 230),
    "Hybrid 145 e-DCS6": ("EB2-MHEV", 145, 230),
    # hybrides rechargeables
    "Hybrid 180 e-EAT8": ("EP6-PHEV", 180, 360), "Hybrid 225 e-EAT8": ("EP6-PHEV", 225, 360),
    "Plug-in Hybrid 195 e-DCS7": ("EP6-PHEV", 195, 360), "Hybrid4 300 e-EAT8": ("EP6-PHEV", 300, 520),
    "Hybrid4 360": ("EP6-PHEV", 360, 520),
    "HYbrid4 2.0 HDi 200": ("DW10-HYBRID4", 200, 500), "HYbrid4 200": ("DW10-HYBRID4", 200, 500),
    # diesel
    "1.9 D 70": ("DW8", 70, 125), "1.4 HDi 54": ("DV4TD", 54, 130), "1.4 HDi 68": ("DV4TD", 68, 160),
    "1.4 HDi 70": ("DV4C", 70, 160), "1.6 HDi 75": ("DV6BTED4", 75, 185), "1.6 HDi 90": ("DV6ATED4", 90, 215),
    "1.6 HDi 110": ("DV6TED4", 110, 240), "1.6 HDi 92": ("DV6D", 92, 230), "1.6 e-HDi 92": ("DV6D", 92, 230),
    "1.6 HDi 112": ("DV6C", 112, 270), "1.6 e-HDi 112": ("DV6C", 112, 270), "1.6 e-HDi 115": ("DV6C", 115, 270),
    "1.6 BlueHDi 75": ("DV6F", 75, 233), "1.6 BlueHDi 95": ("DV6F", 95, 210), "1.6 BlueHDi 100": ("DV6F", 100, 254),
    "1.6 BlueHDi 115": ("DV6F", 115, 300), "1.6 BlueHDi 120": ("DV6F", 120, 300),
    "1.5 BlueHDi 75": ("DV5R", 75, 230), "1.5 BlueHDi 100": ("DV5R", 100, 250), "1.5 BlueHDi 110": ("DV5R", 110, 250),
    "1.5 BlueHDi 120": ("DV5R", 120, 300), "1.5 BlueHDi 130": ("DV5R", 130, 300),
    "1.5 BlueHDi 130 EAT8": ("DV5R", 130, 300),
    "2.0 HDi 90": ("DW10TD", 90, 205), "2.0 HDi 120": ("DW10UTED4", 120, 300),
    "2.0 HDi 136": ("DW10BTED4", 136, 320), "2.0 HDi 140": ("DW10C", 140, 320), "2.0 HDi 150": ("DW10C", 150, 340),
    "2.0 HDi 163": ("DW10C", 163, 340), "2.2 HDi 204": ("DW12C", 204, 450),
    "2.0 BlueHDi 110": ("DW10F", 110, 300), "2.0 BlueHDi 120": ("DW10F", 120, 340),
    "2.0 BlueHDi 130": ("DW10F", 130, 320), "2.0 BlueHDi 145": ("DW10F", 145, 370),
    "2.0 BlueHDi 150": ("DW10F", 150, 370), "2.0 BlueHDi 160": ("DW10F", 160, 400),
    "2.0 BlueHDi 180": ("DW10F", 180, 400), "2.0 BlueHDi 180 EAT6": ("DW10F", 180, 400),
    "2.0 BlueHDi 180 EAT8": ("DW10F", 180, 400),
    "2.2 BlueHDi 140": ("DW12RU", 140, 340), "2.2 BlueHDi 165": ("DW12RU", 165, 370),
    "2.2 BlueHDi 180": ("DW12RU", 180, 400),
    "2.2 HDi 100": ("Ford", "PUMA-2.2", 100, 250), "2.2 HDi 120": ("Ford", "PUMA-2.2", 120, 320),
    "3.0 HDi 157": ("FPT", "F1C-3.0", 157, 400),
    # électrique
    "e-208 136": ("E-CMP", 136, 260), "e-208 156": ("E-CMP", 156, 260), "e-208 GTi 281": ("E-CMP", 281, 345), "e-2008 136": ("E-CMP", 136, 260),
    "e-2008 156": ("E-CMP", 156, 260), "e-308 156": ("E-CMP", 156, 260), "e-308 GT": ("E-CMP", 156, 260),
    "e-Partner 136": ("E-CMP", 136, 260), "e-Rifter 136": ("E-CMP", 136, 260),
    "e-Expert 136": ("E-CMP", 136, 260), "e-Expert 136 75 kWh": ("E-CMP", 136, 260),
    "e-Traveller 136": ("E-CMP", 136, 260), "e-Traveller 136 75 kWh": ("E-CMP", 136, 260),
    "e-3008 210": ("STLA-M", 210, 345), "e-5008 210": ("STLA-M", 210, 345), "e-408 210": ("STLA-M", 210, 345),
    "e-3008 Long Range 230": ("STLA-M", 230, 345), "e-5008 Long Range 230": ("STLA-M", 230, 345),
    "e-3008 Dual Motor 325": ("STLA-M", 325, 509), "e-5008 Dual Motor 325": ("STLA-M", 325, 509),
    "e-Boxer 122": ("E-BOXER", 122, 260), "Electric 67": ("PARTNER-EV", 67, 200),
}
ERES = {"PN": "TOY", "P1": "TOY"}  # 107 / 108 : moteur Toyota

MOT = Motorisations("Peugeot", FAMILLES, TABLE, ERES)
MOT.lier(L)

DETAIL = {"Peugeot": L}
MOTEURS = MOT.moteurs()
