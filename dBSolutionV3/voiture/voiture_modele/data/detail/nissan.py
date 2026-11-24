"""Nissan et Nissan Nismo : générations, phases, motorisations (marché européen) et moteurs liés.
Micra, Note, Almera, Primera, Tiida, Pulsar, Juke, Qashqai, X-Trail, Murano, Terrano II, Pathfinder, Patrol, Navara,
Leaf, Ariya, 200SX, 300ZX, 350Z, 370Z, GT-R ; versions Nismo dans la marque « Nissan Nismo ».
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom.
Moteurs Renault (dCi, TCe, E-Tech) rattachés au motoriste Nissan ; utilitaires non couverts ; données anciennes indicatives."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


FAMILLES = {
    # --- essence
    "MA10": f("ATM", E_, 1.0, C, 4, 6000, 3600, "10W40", 2.8, 15000),
    "MA12": f("ATM", E_, 1.2, C, 4, 6000, 3600, "10W40", 2.8, 15000),
    "CG10DE": f("ATM", E_, 1.0, C, 4, 6000, 4000, "10W40", 2.7, 15000),
    "CG13DE": f("ATM", E_, 1.3, C, 4, 6000, 4000, "10W40", 2.7, 15000),
    "CR12DE": f("ATM", E_, 1.2, C, 4, 5600, 3200, "5W30", 2.9, 15000),
    "CR14DE": f("ATM", E_, 1.4, C, 4, 5200, 3200, "5W30", 2.9, 15000),
    "GA14DE": f("ATM", E_, 1.4, C, 4, 6000, 4000, "10W40", 3.2, 15000),
    "GA16DE": f("ATM", E_, 1.6, C, 4, 6000, 4000, "10W40", 3.2, 15000),
    "QG15DE": f("ATM", E_, 1.5, C, 4, 5600, 4000, "5W30", 3.2, 15000),
    "QG16DE": f("ATM", E_, 1.6, C, 4, 6000, 4000, "5W30", 3.2, 15000),
    "QG18DE": f("ATM", E_, 1.8, C, 4, 5600, 4000, "5W30", 3.2, 15000),
    "SR20DE": f("ATM", E_, 2.0, C, 4, 6400, 4800, "10W40", 3.9, 15000),
    "SR20DET": f("TURBO", E_, 2.0, C, 4, 6000, 4800, "10W40", 3.9, 10000),
    "CA18DET": f("TURBO", E_, 1.8, B, 4, 6400, 4000, "10W40", 3.9, 10000),
    "HR16DE": f("ATM", E_, 1.6, C, 4, 6000, 4400, "5W30", 4.1, 20000),
    "HR12DE": f("ATM", E_, 1.2, C, 3, 6000, 4000, "5W30", 3.0, 20000),
    "HR12DDR": f("TURBO", E_, 1.2, C, 3, 5600, 4400, "5W30", 3.0, 20000),
    "BR10": f("ATM", E_, 1.0, C, 3, 6300, 3500, "5W30", 3.0, 20000),
    "H4Bt": f("TURBO", E_, 0.9, C, 3, 5500, 2500, "5W40", 4.0, 20000),
    "HR10DET": f("TURBO", E_, 1.0, C, 3, 5000, 2000, "0W20", 4.0, 20000),
    "HRA2DDT": f("TURBO", E_, 1.2, C, 4, 4500, 2000, "5W30", 4.3, 20000),
    "HR13DDT": f("TURBO", E_, 1.3, C, 4, 5500, 1600, "0W20", 4.4, 20000),
    "HR13DDT-MHEV": f("HYB_TE", E_, 1.3, C, 4, 5500, 1600, "0W20", 4.4, 20000),
    "MR16DDT": f("TURBO", E_, 1.6, C, 4, 6000, 2000, "5W30", 4.4, 20000),
    "MR20DE": f("ATM", E_, 2.0, C, 4, 6000, 4800, "5W30", 4.4, 20000),
    "QR20DE": f("ATM", E_, 2.0, C, 4, 6000, 4000, "5W30", 4.4, 20000),
    "QR25DE": f("ATM", E_, 2.5, C, 4, 6000, 4400, "5W30", 4.6, 20000),
    "KR15DDT": f("HYB_TE", E_, 1.5, C, 3, 5000, 2400, "0W20", 4.5, 20000),
    "ePower-1.5": f("HYB_TE", E_, 1.5, C, 3, 4600, 0, "0W20", 4.5, 20000),
    "H4M-ETECH": f("HYB_E", E_, 1.6, C, 4, 5600, 3200, "0W20", 4.5, 30000),
    "VG30DETT": f("TURBO", E_, 3.0, B, 6, 6400, 3600, "10W40", 4.4, 10000, a="V"),
    "VQ35DE": f("ATM", E_, 3.5, C, 6, 6200, 4800, "5W30", 4.7, 20000, a="V"),
    "VQ35HR": f("ATM", E_, 3.5, C, 6, 6800, 4800, "5W30", 4.7, 20000, a="V"),
    "VQ37VHR": f("ATM", E_, 3.7, C, 6, 7000, 5200, "5W30", 4.7, 20000, a="V"),
    "VQ40DE": f("ATM", E_, 4.0, C, 6, 5600, 4000, "5W30", 5.0, 20000, a="V"),
    "TB48DE": f("ATM", E_, 4.8, C, 6, 4800, 3600, "10W40", 6.0, 15000),
    "VR38DETT": f("TURBO", E_, 3.8, C, 6, 6800, 3300, "0W40", 6.0, 15000, a="V"),
    "KA24E": f("ATM", E_, 2.4, C, 4, 5200, 4000, "10W40", 4.0, 15000),
    # --- diesel
    "CD20": f("ATM", D, 2.0, B, 4, 4600, 2800, "15W40", 4.5, 10000),
    "CD20T": f("TURBO", D, 2.0, B, 4, 4400, 2000, "15W40", 4.5, 10000),
    "K9K": f("TURBO", D, 1.5, B, 4, 4000, 1750, "5W30", 4.5, 20000),
    "F9Q": f("TURBO", D, 1.9, B, 4, 4000, 1900, "5W30", 5.0, 20000),
    "R9M": f("TURBO", D, 1.6, C, 4, 4000, 1750, "5W30", 5.2, 20000),
    "R9N": f("TURBO", D, 1.7, C, 4, 3750, 1750, "5W30", 5.2, 20000),
    "M9R": f("TURBO", D, 2.0, C, 4, 4000, 2000, "5W30", 6.5, 20000),
    "YD22": f("TURBO", D, 2.2, C, 4, 4000, 2000, "5W30", 5.0, 20000),
    "YD25": f("TURBO", D, 2.5, C, 4, 4000, 2000, "5W30", 6.2, 20000),
    "YS23": f("TURBO", D, 2.3, C, 4, 3750, 1500, "5W30", 6.8, 20000),
    "V9X": f("TURBO", D, 3.0, C, 6, 3750, 1500, "5W30", 7.0, 20000, a="V"),
    "TD27T": f("TURBO", D, 2.7, "NC", 4, 3600, 2000, "15W40", 6.0, 10000),
    "RD28T": f("TURBO", D, 2.8, B, 6, 4000, 2000, "15W40", 6.5, 10000),
    "ZD30": f("TURBO", D, 3.0, C, 4, 3600, 2000, "10W40", 7.0, 10000),
    "TD42": f("ATM", D, 4.2, "NC", 6, 4000, 2000, "15W40", 8.0, 10000),
    # --- électriques
    "EM57": electrique(), "AmpR-Small": electrique(), "CMF-EV": electrique(), "Ariya-EV": electrique(),
}

mg = SaisieMoteurs(FAMILLES, "Nissan")
L, LN = [], []   # Nissan, Nissan Nismo

# ---------------------------------------------------------------- Micra / Note
mg(L, "Micra", "K10", "1", "1983-01", "1992-12", [("1.0 50", "MA10", 75), ("1.2 57", "MA12", 90, {"debut": "1988-01"})], portes=3,
   reservoir=40, remarques="3 et 5 portes")
mg(L, "Micra", "K11", "1", "1992-11", "2002-12",
   [("1.0 55", "CG10DE", 79), ("1.3 75", "CG13DE", 104), ("1.4 82", "CG13DE", 117, {"debut": "2000-09"}), ("1.5 D 57", "CD20", 95, {"debut": "1998-01"})],
   portes=3, reservoir=40, remarques="3 et 5 portes, C+C (1997)")
mg(L, "Micra", "K12", "1", "2003-01", "2010-09",
   [("1.0 65", "CR12DE", 90, {"fin": "2007-12"}), ("1.2 80", "CR12DE", 110), ("1.4 88", "CR14DE", 128), ("1.6 160 SR 110", "HR16DE", 153, {"debut": "2005-06"}),
    ("1.5 dCi 65", "K9K", 160, {"fin": "2005-06"}), ("1.5 dCi 86", "K9K", 200, {"debut": "2005-07"})], portes=3, reservoir=46,
   remarques="3 et 5 portes, C+C (2005) ; restylage 2007")
mg(L, "Micra", "K13", "1", "2010-11", "2017-02", [("1.2 80", "HR12DE", 110), ("1.2 DIG-S 98", "HR12DDR", 142, {"debut": "2011-06"})],
   reservoir=41, remarques="5 portes ; restylage 2013")
mg(L, "Micra", "K14", "1", "2017-03", "2023-12",
   [("1.0 71", "BR10", 95), ("0.9 IG-T 90", "H4Bt", 140, {"fin": "2019-06"}), ("1.0 IG-T 100", "HR10DET", 160, {"debut": "2019-01"}),
    ("1.0 DIG-T 117", "HR10DET", 180, {"debut": "2019-01", "fin": "2020-12"}), ("1.5 dCi 90", "K9K", 220, {"fin": "2019-06"})],
   reservoir=41, remarques="5 portes (jumelle technique de la Clio IV)")
mg(L, "Micra", "AmpR Small", "1", "2025-11", None,
   [("Micra 122", "AmpR-Small", 225, el(40)), ("Micra 150", "AmpR-Small", 245, el(52))], reservoir=0,
   remarques="Citadine électrique (base Renault 5 E-Tech) ; version 95 ch annoncée")
mg(L, "Note", "E11", "1", "2006-03", "2013-08",
   [("1.4 88", "CR14DE", 128), ("1.6 110", "HR16DE", 153), ("1.5 dCi 86", "K9K", 200), ("1.5 dCi 90", "K9K", 200, {"debut": "2009-01"})],
   reservoir=46, remarques="Monospace compact ; restylage 2009")
mg(L, "Note", "E12", "1", "2013-09", "2017-12", [("1.2 80", "HR12DE", 110), ("1.2 DIG-S 98", "HR12DDR", 142), ("1.5 dCi 90", "K9K", 200)],
   reservoir=41, remarques="Monospace compact")

# ---------------------------------------------------------------- Almera / Primera / Tiida / Pulsar
mg(L, "Almera", "N15", "1", "1995-06", "2000-06",
   [("1.4 87", "GA14DE", 116), ("1.6 100", "GA16DE", 135), ("2.0 GTi 143", "SR20DE", 178), ("2.0 D 75", "CD20", 132)], reservoir=50,
   remarques="3 et 5 portes, berline")
mg(L, "Almera", "N16", "1", "2000-03", "2006-12",
   [("1.5 90", "QG15DE", 128), ("1.8 114", "QG18DE", 158), ("2.2 dCi 112", "YD22", 250), ("2.2 dCi 136", "YD22", 300, {"debut": "2003-01"}),
    ("1.5 dCi 82", "K9K", 185, {"debut": "2003-01"})], reservoir=60, remarques="3 et 5 portes, berline ; Almera Tino (2000)")
mg(L, "Primera", "P10", "1", "1990-06", "1996-09",
   [("1.6 102", "GA16DE", 135), ("2.0 115", "SR20DE", 162), ("2.0 GT 150", "SR20DE", 186), ("2.0 D 75", "CD20", 132)], portes=4, reservoir=60,
   remarques="Berline, 5 portes, Break")
mg(L, "Primera", "P11", "1", "1996-09", "2002-01",
   [("1.6 99", "GA16DE", 140), ("1.8 114", "QG18DE", 158, {"debut": "1999-09"}), ("2.0 115", "SR20DE", 162), ("2.0 GT 140", "SR20DE", 180),
    ("2.0 TD 90", "CD20T", 196)], portes=4, reservoir=60, remarques="Berline, 5 portes, Break")
mg(L, "Primera", "P12", "1", "2002-01", "2007-12",
   [("1.6 109", "QG16DE", 144), ("1.8 116", "QG18DE", 163), ("2.0 140", "QR20DE", 192), ("1.9 dCi 120", "F9Q", 270, {"debut": "2003-06"}),
    ("2.2 dCi 139", "YD22", 314)], portes=4, reservoir=62, remarques="Berline, 5 portes, Break")
mg(L, "Tiida", "C11", "1", "2007-03", "2012-12",
   [("1.6 110", "HR16DE", 153), ("1.8 126", "MR20DE", 173), ("1.5 dCi 105", "K9K", 240)], reservoir=52, remarques="5 portes et berline")
mg(L, "Pulsar", "C13", "1", "2014-09", "2018-12",
   [("1.2 DIG-T 115", "HRA2DDT", 190), ("1.6 DIG-T 190", "MR16DDT", 240, {"debut": "2015-09"}), ("1.5 dCi 110", "K9K", 260)], reservoir=46,
   remarques="Compacte 5 portes")

# ---------------------------------------------------------------- Juke / Qashqai / X-Trail
mg(L, "Juke", "F15", "1", "2010-10", "2014-04",
   [("1.6 94", "HR16DE", 140), ("1.6 117", "HR16DE", 158), ("1.6 DIG-T 190", "MR16DDT", 240), ("1.5 dCi 110", "K9K", 240)], reservoir=46,
   remarques="Crossover urbain")
mg(L, "Juke", "F15", "2", "2014-05", "2019-09",
   [("1.6 94", "HR16DE", 140), ("1.6 117", "HR16DE", 158), ("1.2 DIG-T 115", "HRA2DDT", 190), ("1.6 DIG-T 190", "MR16DDT", 240),
    ("1.5 dCi 110", "K9K", 260)], reservoir=46, remarques="Crossover urbain restylé")
mg(L, "Juke", "F16", "1", "2019-11", "2024-03",
   [("1.0 DIG-T 117", "HR10DET", 180, {"fin": "2021-06"}), ("1.0 DIG-T 114", "HR10DET", 200, {"debut": "2021-07"}),
    ("1.6 Hybrid 143", "H4M-ETECH", 148, {"debut": "2022-06"})], reservoir=46, remarques="Crossover urbain")
mg(L, "Juke", "F16", "2", "2024-04", None,
   [("1.0 DIG-T 114", "HR10DET", 200), ("1.6 Hybrid 143", "H4M-ETECH", 148)], reservoir=46,
   remarques="Restylage ; Juke électrique de 3e génération annoncé pour début 2027")
mg(L, "Qashqai", "J10", "1", "2007-02", "2010-02",
   [("1.6 115", "HR16DE", 156), ("2.0 141", "MR20DE", 196), ("1.5 dCi 106", "K9K", 240), ("2.0 dCi 150", "M9R", 320)], reservoir=65,
   remarques="Crossover ; Qashqai+2 7 places (2008)")
mg(L, "Qashqai", "J10", "2", "2010-03", "2013-12",
   [("1.6 117", "HR16DE", 158), ("2.0 141", "MR20DE", 196), ("1.5 dCi 110", "K9K", 240), ("1.6 dCi 130", "R9M", 320, {"debut": "2011-09"}),
    ("2.0 dCi 150", "M9R", 320)], reservoir=65, remarques="Crossover et Qashqai+2")
mg(L, "Qashqai", "J11", "1", "2014-02", "2017-06",
   [("1.2 DIG-T 115", "HRA2DDT", 190), ("1.6 DIG-T 163", "MR16DDT", 240, {"debut": "2015-06"}), ("1.5 dCi 110", "K9K", 260),
    ("1.6 dCi 130", "R9M", 320)], reservoir=55, remarques="Crossover")
mg(L, "Qashqai", "J11", "2", "2017-07", "2021-05",
   [("1.2 DIG-T 115", "HRA2DDT", 190, {"fin": "2018-12"}), ("1.3 DIG-T 140", "HR13DDT", 240, {"debut": "2018-09"}),
    ("1.3 DIG-T 160", "HR13DDT", 270, {"debut": "2018-09"}), ("1.5 dCi 115", "K9K", 260), ("1.7 dCi 150", "R9N", 340, {"debut": "2019-01"})],
   reservoir=55, remarques="Crossover restylé")
mg(L, "Qashqai", "J12", "1", "2021-06", "2024-05",
   [("1.3 DIG-T MHEV 140", "HR13DDT-MHEV", 240), ("1.3 DIG-T MHEV 158", "HR13DDT-MHEV", 270), ("e-Power 190", "ePower-1.5", 330, {"debut": "2022-08"})],
   reservoir=55, remarques="Crossover")
mg(L, "Qashqai", "J12", "2", "2024-06", None,
   [("1.3 DIG-T MHEV 140", "HR13DDT-MHEV", 240), ("1.3 DIG-T MHEV 158", "HR13DDT-MHEV", 270), ("e-Power 190", "ePower-1.5", 330, {"fin": "2025-08"}),
    ("e-Power 205", "ePower-1.5", 330, {"debut": "2025-09"})], reservoir=55, remarques="Restylage ; e-Power de 3e génération (2025)")
mg(L, "X-Trail", "T30", "1", "2001-06", "2007-05",
   [("2.0 140", "QR20DE", 192), ("2.5 165", "QR25DE", 230), ("2.2 dCi 114", "YD22", 270, {"fin": "2003-12"}), ("2.2 dCi 136", "YD22", 314, {"debut": "2004-01"})],
   reservoir=60, remarques="SUV")
mg(L, "X-Trail", "T31", "1", "2007-06", "2014-06",
   [("2.0 141", "MR20DE", 196), ("2.5 169", "QR25DE", 233), ("2.0 dCi 150", "M9R", 320), ("2.0 dCi 173", "M9R", 360)], reservoir=65, remarques="SUV")
mg(L, "X-Trail", "T32", "1", "2014-07", "2022-06",
   [("1.6 DIG-T 163", "MR16DDT", 240, {"debut": "2015-09", "fin": "2018-12"}), ("1.6 dCi 130", "R9M", 320, {"fin": "2019-06"}),
    ("2.0 dCi 177", "M9R", 380, {"debut": "2017-06", "fin": "2019-06"}), ("1.7 dCi 150", "R9N", 340, {"debut": "2019-07"}),
    ("1.3 DIG-T 160", "HR13DDT", 270, {"debut": "2019-01"})], places=7, reservoir=60, remarques="SUV 5 ou 7 places ; restylage 2017")
mg(L, "X-Trail", "T33", "1", "2022-07", None,
   [("1.5 VC-T MHEV 163", "KR15DDT", 300), ("e-Power 204", "ePower-1.5", 330), ("e-Power e-4ORCE 213", "ePower-1.5", 525)], places=7,
   reservoir=55, remarques="SUV 5 ou 7 places ; restylage 2024 non détaillé")

# ---------------------------------------------------------------- grands SUV et 4x4
mg(L, "Murano", "Z50", "1", "2003-06", "2008-12", [("3.5 V6 234", "VQ35DE", 318)], reservoir=82, remarques="SUV")
mg(L, "Murano", "Z51", "1", "2009-01", "2014-12", [("3.5 V6 256", "VQ35DE", 336), ("2.5 dCi 190", "YD25", 450, {"debut": "2010-06"})],
   reservoir=82, remarques="SUV ; CrossCabriolet non vendu en Europe")
mg(L, "Terrano II", "R20", "1", "1993-01", "2006-12",
   [("2.4 118", "KA24E", 192), ("2.7 TD 100", "TD27T", 221, {"fin": "1999-12"}), ("2.7 TDi 125", "TD27T", 278, {"debut": "2000-01", "fin": "2002-12"}),
    ("3.0 Di 154", "ZD30", 304, {"debut": "2002-09"})], portes=3, places=7, reservoir=72, remarques="4x4 3 et 5 portes (jumeau Ford Maverick)")
mg(L, "Pathfinder", "R51", "1", "2005-01", "2014-12",
   [("2.5 dCi 174", "YD25", 403, {"fin": "2010-06"}), ("2.5 dCi 190", "YD25", 450, {"debut": "2010-07"}), ("3.0 V6 dCi 231", "V9X", 550, {"debut": "2010-07"}),
    ("4.0 V6 269", "VQ40DE", 385, {"fin": "2010-06"})], places=7, reservoir=80, remarques="SUV 7 places")
mg(L, "Patrol", "Y60", "1", "1987-11", "1997-12", [("2.8 TD 115", "RD28T", 235), ("4.2 D 115", "TD42", 264)], portes=3, places=7, reservoir=95,
   remarques="4x4 court et long")
mg(L, "Patrol", "Y61", "1", "1997-12", "2010-06",
   [("2.8 TD 129", "RD28T", 285, {"fin": "2000-12"}), ("3.0 Di 158", "ZD30", 354, {"debut": "2000-01"}), ("4.8 245", "TB48DE", 420, {"debut": "2001-09"})],
   portes=3, places=7, reservoir=95, remarques="4x4 court et long")
mg(L, "Navara", "D22", "1", "1997-01", "2005-12", [("2.5 Di 103", "YD25", 230), ("2.5 Di 133", "YD25", 304, {"debut": "2001-09"})], portes=4,
   reservoir=70, remarques="Pick-up King Cab et double cabine")
mg(L, "Navara", "D40", "1", "2005-06", "2015-12",
   [("2.5 dCi 174", "YD25", 403, {"fin": "2010-06"}), ("2.5 dCi 190", "YD25", 450, {"debut": "2010-07"}), ("3.0 V6 dCi 231", "V9X", 550, {"debut": "2010-07"})],
   portes=4, reservoir=80, remarques="Pick-up")
mg(L, "Navara", "D23", "1", "2015-06", "2021-12", [("2.3 dCi 160", "YS23", 403), ("2.3 dCi 190", "YS23", 450)], portes=4, reservoir=80,
   remarques="Pick-up (base du Mercedes Classe X)")

# ---------------------------------------------------------------- électriques
mg(L, "Leaf", "ZE0", "1", "2011-03", "2017-12",
   [("Leaf 24 kWh 109", "EM57", 280, el(21, fin="2015-12")),
    ("Leaf 30 kWh 109", "EM57", 254, el(28, debut="2016-01"))], reservoir=0, remarques="Compacte électrique ; production Sunderland (2013)")
mg(L, "Leaf", "ZE1", "1", "2018-01", "2024-12",
   [("Leaf 150", "EM57", 320, el(39)), ("Leaf e+ 217", "EM57", 340, el(59, debut="2019-06"))], reservoir=0, remarques="Compacte électrique")
mg(L, "Leaf", "ZE2", "1", "2025-11", None,
   [("Leaf 177", "CMF-EV", 345, el(52)), ("Leaf 218", "CMF-EV", 355, el(75))], reservoir=0,
   remarques="3e génération, crossover électrique (plateforme CMF-EV) ; puissances et batteries indicatives")
mg(L, "Ariya", "FE0", "1", "2022-06", None,
   [("Ariya 63 kWh 218", "Ariya-EV", 300, el(63)), ("Ariya 87 kWh 242", "Ariya-EV", 300, el(87)),
    ("Ariya e-4ORCE 87 kWh 306", "Ariya-EV", 600, el(87, debut="2023-06"))], reservoir=0, remarques="SUV coupé électrique ; restylage 2025 non détaillé")

# ---------------------------------------------------------------- sportives
mg(L, "200SX", "S13", "1", "1989-01", "1994-06", [("200SX 1.8 Turbo 169", "CA18DET", 226)], portes=2, places=4, reservoir=60, remarques="Coupé")
mg(L, "200SX", "S14", "1", "1994-06", "1999-12", [("200SX 2.0 Turbo 200", "SR20DET", 265)], portes=2, places=4, reservoir=65, remarques="Coupé ; restylage 1996")
mg(L, "300ZX", "Z32", "1", "1990-01", "1996-12", [("300ZX Twin Turbo 283", "VG30DETT", 388)], portes=2, places=2, reservoir=72,
   remarques="Coupé targa 2 places")
mg(L, "350Z", "Z33", "1", "2003-03", "2009-06",
   [("350Z 280", "VQ35DE", 363, {"fin": "2005-06"}), ("350Z 300", "VQ35DE", 353, {"debut": "2005-07", "fin": "2007-03"}), ("350Z 313", "VQ35HR", 358, {"debut": "2007-04"})],
   portes=2, places=2, reservoir=80, remarques="Coupé et Roadster (2005)")
mg(L, "370Z", "Z34", "1", "2009-06", "2020-12", [("370Z 328", "VQ37VHR", 363), ("370Z 344", "VQ37VHR", 371, {"debut": "2013-01"})], portes=2,
   places=2, reservoir=72, remarques="Coupé et Roadster (2010)")
mg(L, "GT-R", "R35", "1", "2008-03", "2025-08",
   [("GT-R 480", "VR38DETT", 588, {"fin": "2010-12"}), ("GT-R 530", "VR38DETT", 612, {"debut": "2011-01", "fin": "2011-12"}),
    ("GT-R 550", "VR38DETT", 632, {"debut": "2012-01", "fin": "2016-06"}), ("GT-R 570", "VR38DETT", 637, {"debut": "2016-07"})],
   portes=2, places=4, reservoir=74, remarques="Coupé 2+2 ; vente européenne arrêtée en 2022, fin de production 2025")

# ---------------------------------------------------------------- Nissan Nismo
mg(LN, "Juke Nismo", "F15", "1", "2013-01", "2014-04", [("Juke Nismo 200", "MR16DDT", 250)], reservoir=46)
mg(LN, "Juke Nismo", "F15", "2", "2014-09", "2018-06", [("Juke Nismo RS 218", "MR16DDT", 280)], reservoir=46, remarques="Traction ou 4x4")
mg(LN, "370Z Nismo", "Z34", "1", "2013-09", "2020-12", [("370Z Nismo 344", "VQ37VHR", 371)], portes=2, places=2, reservoir=72)
mg(LN, "GT-R Nismo", "R35", "1", "2014-02", "2025-08", [("GT-R Nismo 600", "VR38DETT", 652)], portes=2, places=4, reservoir=74,
   remarques="Restylages 2017 et 2020")
mg(LN, "Ariya Nismo", "FE0", "1", "2024-06", None, [("Ariya Nismo 435", "Ariya-EV", 600, el(87))], reservoir=0,
   remarques="SUV coupé électrique e-4ORCE")

MOT = Motorisations("Nissan", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LN)

DETAIL = {"Nissan": L, "Nissan Nismo": LN}
MOTEURS = MOT.moteurs()
