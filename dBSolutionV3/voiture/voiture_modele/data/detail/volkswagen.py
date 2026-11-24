"""Volkswagen : générations, phases, motorisations (marché européen) et moteurs liés."""
from ._outil import Motorisations, electrique, famille as f, gamme as g


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def ph(kwh, reservoir, **kw):  # hybride rechargeable
    return {"reservoir": reservoir, "batterie": kwh, **kw}


L = []

# ---------------------------------------------------------------- Lupo / Fox / up!
L += g("Lupo", "6X", "1", "1998-10", "2005-07",
       ["1.0 50", "1.4 60", "1.4 16v 75", ("1.4 FSI 105", {"debut": "2000-09", "fin": "2003"}),
        ("GTI 1.6 125", {"debut": "2000-10"}), ("1.2 TDI 61", {"debut": "1999-07", "remarques": "Lupo 3L"}),
        "1.4 TDI 75", "1.7 SDI 60"], portes=3, places=4, reservoir=34, remarques="3 portes")
L += g("Fox", "5Z", "1", "2005-04", "2011-12", ["1.2 55", "1.4 75", "1.4 TDI 70"], portes=3, places=4, reservoir=50,
       remarques="3 portes")
L += g("up!", "AA", "1", "2011-12", "2016-06",
       ["1.0 MPI 60", "1.0 MPI 75", ("e-up! 82", el(19, debut="2013-10"))], places=4, reservoir=35,
       remarques="3 et 5 portes")
L += g("up!", "AA", "2", "2016-07", "2023-08",
       ["1.0 MPI 60", "1.0 MPI 65", "1.0 MPI 75", ("1.0 TSI 90", {"fin": "2019-08"}),
        ("GTI 1.0 TSI 115", {"debut": "2018-01", "fin": "2021-12"}), ("e-up! 83", el(32, debut="2019-10"))],
       places=4, reservoir=35, remarques="3 et 5 portes")

# ---------------------------------------------------------------- Polo
L += g("Polo", "9N", "1", "2001-11", "2005-04",
       ["1.2 55", "1.2 65", "1.4 75", "1.4 16v 100", "1.4 FSI 86", "1.9 SDI 64", "1.4 TDI 75",
        "1.9 TDI 100", ("GTI 1.8T 150", {"debut": "2004-09"})], reservoir=45, remarques="3 et 5 portes, Classic")
L += g("Polo", "9N", "2", "2005-05", "2009-06",
       ["1.2 60", "1.2 70", "1.4 80", "1.6 105", "GTI 1.8T 150", "1.4 TDI 70", "1.4 TDI 80", "1.9 TDI 100",
        "GT 1.9 TDI 130"], reservoir=45, remarques="3 et 5 portes")
L += g("Polo", "6R", "1", "2009-06", "2014-03",
       ["1.2 60", "1.2 70", "1.4 85", "1.2 TSI 90", "1.2 TSI 105", ("GTI 1.4 TSI 180", {"debut": "2010-05"}),
        "1.2 TDI 75", "1.6 TDI 75", "1.6 TDI 90", "1.6 TDI 105"], reservoir=45, remarques="3 et 5 portes")
L += g("Polo", "6C", "1", "2014-04", "2017-06",
       ["1.0 MPI 60", "1.0 MPI 75", "1.0 TSI 95", "1.0 TSI 110", "1.2 TSI 90", "1.2 TSI 110",
        "GTI 1.8 TSI 192", "1.4 TDI 75", "1.4 TDI 90", "1.4 TDI 105"], reservoir=45, remarques="3 et 5 portes")
L += g("Polo", "AW", "1", "2017-09", "2021-05",
       ["1.0 MPI 65", "1.0 MPI 80", "1.0 TSI 95", "1.0 TSI 115", ("1.5 TSI 150", {"fin": "2020-06"}),
        ("GTI 2.0 TSI 200", {"debut": "2018-01", "fin": "2019-12"}), ("GTI 2.0 TSI 207", {"debut": "2020-01"}),
        ("1.6 TDI 80", {"fin": "2020-06"}), ("1.6 TDI 95", {"fin": "2020-06"})], reservoir=40,
       remarques="5 portes")
L += g("Polo", "AW", "2", "2021-06", None,
       ["1.0 MPI 80", "1.0 TSI 95", "1.0 TSI 110", "GTI 2.0 TSI 207"], reservoir=40, remarques="5 portes")

# ---------------------------------------------------------------- Golf
L += g("Golf", "Mk1", "1", "1974-05", "1978-07",
       ["1.1 50", "1.5 70", ("GTI 1.6 110", {"debut": "1976-06"}), ("1.5 D 50", {"debut": "1976-09"})],
       reservoir=40, remarques="Golf I — 3 et 5 portes")
L += g("Golf", "Mk1", "2", "1978-08", "1983-08",
       ["1.1 50", "1.3 60", "1.5 70", "1.6 75", "GTI 1.6 110", ("GTI 1.8 112", {"debut": "1982-09"}),
        ("1.6 D 54", {"debut": "1980-08"}), ("1.6 TD 70", {"debut": "1982-09"})],
       reservoir=40, remarques="Golf I — 3 et 5 portes, Cabriolet (1979)")
L += g("Golf", "Mk1", "3", "1983-09", "1993-06",
       ["1.6 72", "1.8 90", "1.8 98", "GTI 1.8 112"], portes=2, places=4, reservoir=40,
       remarques="Golf I Cabriolet, produit jusqu'en 1993")
L += g("Golf", "Mk2", "1", "1983-08", "1987-07",
       ["1.3 55", "1.6 75", "1.8 90", "GTI 1.8 112", ("GTI 16v 1.8 139", {"debut": "1986-01"}), "1.6 D 54",
        "1.6 TD 70"], reservoir=55, remarques="Golf II — 3 et 5 portes, Jetta II")
L += g("Golf", "Mk2", "2", "1987-08", "1992-06",
       ["1.3 55", "1.6 72", "1.8 90", "GTI 1.8 107", "GTI 16v 1.8 129", ("GTI G60 1.8 160", {"debut": "1990-01"}),
        ("Rallye G60 1.8 160", {"debut": "1989-01", "fin": "1991-12"}), "1.6 D 54", "1.6 TD 70", ("1.6 TD 80", {"debut": "1989-01"})],
       reservoir=55, remarques="Golf II — 3 et 5 portes ; Country 4x4 (1990)")
L += g("Golf", "Mk3", "1", "1991-08", "1997-12",
       ["1.4 60", "1.6 75", ("1.6 100", {"debut": "1995-09"}), "1.8 75", "1.8 90", "2.0 115", "GTI 2.0 115",
        ("GTI 2.0 16v 150", {"debut": "1992-10"}), "VR6 2.8 174", ("VR6 2.9 190", {"debut": "1994-09"}),
        "1.9 D 64", "1.9 TD 75", ("1.9 TDI 90", {"debut": "1993-09"}), ("1.9 TDI 110", {"debut": "1996-09"}),
        ("1.9 SDI 64", {"debut": "1995-09"})],
       reservoir=55, remarques="Golf III — 3 et 5 portes, Variant (1993), Cabriolet (1993)")
L += g("Golf", "Mk3", "2", "1998-01", "2002-06",
       ["1.6 75", "1.6 100", "1.8 90", "2.0 115", "1.9 TDI 90", "1.9 TDI 110"], portes=2, places=4, reservoir=55,
       remarques="Golf III Cabriolet restylé (face avant Golf IV), produit jusqu'en 2002 ; Variant jusqu'en 1999")
L += g("Golf", "Mk4", "1", "1997-10", "2003-09",
       ["1.4 16v 75", "1.6 100", "1.6 105", ("1.6 FSI 110", {"debut": "2002-01"}), "1.8T 150", "GTI 1.8T 180",
        "2.0 115", "2.3 V5 150", ("2.3 V5 170", {"debut": "2000-10"}), ("R32 3.2 241", {"debut": "2002-09"}),
        "1.9 SDI 68", "1.9 TDI 90", "1.9 TDI 100", "1.9 TDI 110", "1.9 TDI 115", "1.9 TDI 130", "1.9 TDI 150"],
       reservoir=55, remarques="3 et 5 portes, Variant, Cabriolet (Mk3 restylée)")
L += g("Golf", "Mk5", "1", "2003-10", "2008-10",
       ["1.4 80", "1.4 FSI 90", ("1.4 TSI 122", {"debut": "2007-01"}), ("1.4 TSI 140", {"debut": "2006-01"}),
        ("GT 1.4 TSI 170", {"debut": "2006-01"}), "1.6 102", "1.6 FSI 115", "2.0 FSI 150",
        ("GTI 2.0 TFSI 200", {"debut": "2004-10"}), ("GTI Edition 30 2.0 TFSI 230", {"debut": "2006-10", "fin": "2007-12"}),
        ("R32 3.2 250", {"debut": "2005-09"}), "1.9 TDI 90", "1.9 TDI 105", "2.0 SDI 75", "2.0 TDI 140",
        ("GT 2.0 TDI 170", {"debut": "2006-01"})],
       reservoir=55, remarques="3 et 5 portes, Plus, Variant (2007)")
L += g("Golf", "Mk6", "1", "2008-10", "2012-11",
       ["1.2 TSI 85", "1.2 TSI 105", "1.4 80", "1.4 TSI 122", "1.4 TSI 160", "1.6 102",
        ("GTI 2.0 TSI 210", {"debut": "2009-04"}), ("GTI Edition 35 2.0 TSI 235", {"debut": "2011-06", "fin": "2012-10"}),
        ("R 2.0 TSI 270", {"debut": "2009-10"}), "1.6 TDI 90", "1.6 TDI 105", "2.0 TDI 110", "2.0 TDI 140",
        ("GTD 2.0 TDI 170", {"debut": "2009-04"})],
       reservoir=55, remarques="3 et 5 portes, Plus, Variant, Cabriolet (2011)")
L += g("Golf", "Mk7", "1", "2012-11", "2017-02",
       ["1.2 TSI 85", "1.2 TSI 105", "1.4 TSI 122", "1.4 TSI 140", "1.4 TSI 150", ("1.0 TSI 115", {"debut": "2015-01"}),
        ("GTI 2.0 TSI 220", {"debut": "2013-04"}), ("GTI 2.0 TSI 230", {"debut": "2013-04"}),
        ("GTI Clubsport 2.0 TSI 265", {"debut": "2016-01"}), ("R 2.0 TSI 300", {"debut": "2013-11"}),
        "1.6 TDI 90", "1.6 TDI 105", ("1.6 TDI 110", {"debut": "2014-01"}), "2.0 TDI 150", ("GTD 2.0 TDI 184", {"debut": "2013-04"}),
        ("e-Golf 115", el(24, debut="2014-03")), ("GTE 204", ph(9, 40, debut="2014-08"))],
       reservoir=50, remarques="3 et 5 portes, Variant, Sportsvan")
L += g("Golf", "Mk7", "2", "2017-03", "2020-01",
       ["1.0 TSI 85", "1.0 TSI 110", ("1.4 TSI 125", {"fin": "2017-12"}), "1.5 TSI 130", "1.5 TSI 150",
        ("GTI 2.0 TSI 230", {"fin": "2018-06"}), "GTI 2.0 TSI 245", ("GTI TCR 2.0 TSI 290", {"debut": "2019-01"}),
        "R 2.0 TSI 300", ("R 2.0 TSI 310", {"debut": "2017-03", "fin": "2018-06"}), "1.6 TDI 90", "1.6 TDI 115",
        "2.0 TDI 150", "GTD 2.0 TDI 184", ("e-Golf 136", el(36)), ("GTE 204", ph(9, 40))],
       reservoir=50, remarques="3 et 5 portes, Variant, Sportsvan")
L += g("Golf", "Mk8", "1", "2020-01", "2024-03",
       ["1.0 TSI 90", "1.0 TSI 110", "1.0 eTSI 110", "1.5 TSI 130", "1.5 TSI 150", "1.5 eTSI 130", "1.5 eTSI 150",
        "2.0 TDI 115", "2.0 TDI 150", "GTD 2.0 TDI 200", "GTI 2.0 TSI 245", ("GTI Clubsport 2.0 TSI 300", {"debut": "2020-11"}),
        ("R 2.0 TSI 320", {"debut": "2020-11"}), ("R 2.0 TSI 333", {"debut": "2022-06", "remarques": "R « 20 Years »"}),
        ("eHybrid 204", ph(13, 40, debut="2020-09")), ("GTE 245", ph(13, 40, debut="2020-09"))],
       reservoir=50, remarques="5 portes et Variant")
L += g("Golf", "Mk8", "2", "2024-04", None,
       ["1.5 TSI 116", "1.5 eTSI 116", "1.5 eTSI 150", "2.0 TDI 116", "2.0 TDI 150", "GTI 2.0 TSI 265",
        ("GTI Clubsport 2.0 TSI 300", {"debut": "2024-09"}), ("R 2.0 TSI 333", {"debut": "2024-09"}),
        ("eHybrid 204", ph(20, 40)), ("GTE 272", ph(20, 40))],
       reservoir=50, remarques="5 portes et Variant (Golf 8.5)")

# ---------------------------------------------------------------- ID. (électriques MEB)
L += g("ID.3", "E1", "1", "2020-09", "2023-05",
       [("Pure 150", el(45, debut="2021-06")), ("Pro 145", el(58)), ("Pro 204", el(58)), ("Pro S 204", el(77))],
       reservoir=0, remarques="Compacte électrique")
L += g("ID.3", "E1", "2", "2023-06", None,
       [("Pure 150", el(52)), ("Pure 170", el(52, debut="2024-06")), ("Pro 204", el(59)), ("Pro S 231", el(79)),
        ("GTX 286", el(79, debut="2024-06")), ("GTX 326", el(79, debut="2024-06"))],
       reservoir=0, remarques="Compacte électrique")
L += g("ID.4", "E2", "1", "2021-03", "2023-12",
       [("Pure 148", el(52)), ("Pure 170", el(52)), ("Pro 204", el(77)), ("GTX 299", el(77))],
       reservoir=0, remarques="SUV électrique")
L += g("ID.4", "E2", "2", "2024-01", None,
       [("Pure 170", el(52)), ("Pro 286", el(77)), ("GTX 340", el(77))], reservoir=0, remarques="SUV électrique")
L += g("ID.5", "E3", "1", "2022-01", None,
       [("Pro 174", el(77, fin="2023-12")), ("Pro 204", el(77, fin="2023-12")), ("GTX 299", el(77, fin="2023-12")),
        ("Pro 286", el(77, debut="2024-01")), ("GTX 340", el(77, debut="2024-01"))],
       reservoir=0, remarques="SUV coupé électrique")
L += g("ID.7", "ED", "1", "2023-11", None,
       [("Pro 286", el(77)), ("Pro S 286", el(86, debut="2024-06")), ("GTX 340", el(86, debut="2024-06"))],
       reservoir=0, remarques="Berline et Tourer électriques")
L += g("ID. Buzz", "EB", "1", "2022-09", None,
       [("Pro 204", el(77, fin="2024-05")), ("Pro 286", el(79, debut="2024-06")), ("GTX 340", el(86, debut="2024-06"))],
       places=5, reservoir=0, remarques="Monospace électrique 5 à 7 places, Cargo")

# ---------------------------------------------------------------- SUV compacts
L += g("T-Cross", "C1", "1", "2019-04", "2024-02",
       ["1.0 TSI 95", "1.0 TSI 110", "1.5 TSI 150", ("1.6 TDI 95", {"fin": "2020-12"})], reservoir=40)
L += g("T-Cross", "C1", "2", "2024-03", None, ["1.0 TSI 95", "1.0 TSI 115", "1.5 TSI 150"], reservoir=40)
L += g("Taigo", "CS", "1", "2021-11", None, ["1.0 TSI 95", "1.0 TSI 110", "1.5 TSI 150"], reservoir=40,
       remarques="SUV coupé")
L += g("T-Roc", "A1", "1", "2017-11", "2021-12",
       ["1.0 TSI 110", "1.0 TSI 115", "1.5 TSI 150", "2.0 TSI 190", ("R 2.0 TSI 300", {"debut": "2019-09"}),
        "1.6 TDI 115", "2.0 TDI 150"], reservoir=50, remarques="Cabriolet à partir de 2020")
L += g("T-Roc", "A1", "2", "2022-01", "2025-10",
       ["1.0 TSI 110", "1.5 TSI 150", "2.0 TSI 190", "R 2.0 TSI 300", "2.0 TDI 115", "2.0 TDI 150"], reservoir=50,
       remarques="Cabriolet jusqu'en 2025")
L += g("T-Roc", "A2", "1", "2025-11", None, ["1.5 eTSI 116", "1.5 eTSI 150"], reservoir=50,
       remarques="Hybride léger ; versions supplémentaires annoncées")

# ---------------------------------------------------------------- Tiguan
L += g("Tiguan", "5N", "1", "2007-11", "2011-06",
       ["1.4 TSI 150", "2.0 TSI 170", "2.0 TSI 200", "2.0 TDI 140", "2.0 TDI 170"], reservoir=64)
L += g("Tiguan", "5N", "2", "2011-07", "2016-03",
       ["1.4 TSI 122", "1.4 TSI 160", "2.0 TSI 180", "2.0 TSI 210", "2.0 TDI 110", "2.0 TDI 140", "2.0 TDI 150",
        "2.0 TDI 177", "2.0 TDI 184"], reservoir=64)
L += g("Tiguan", "AD1", "1", "2016-04", "2020-07",
       ["1.4 TSI 125", "1.4 TSI 150", "1.5 TSI 130", "1.5 TSI 150", "2.0 TSI 180", "2.0 TSI 220",
        "1.6 TDI 115", "2.0 TDI 115", "2.0 TDI 150", "2.0 TDI 190", "2.0 TDI 240"], reservoir=58,
       remarques="Tiguan et Allspace (7 places)")
L += g("Tiguan", "AD1", "2", "2020-08", "2023-12",
       ["1.5 TSI 130", "1.5 TSI 150", "2.0 TSI 190", "2.0 TSI 245", "R 2.0 TSI 320", ("eHybrid 245", ph(13, 45)),
        "2.0 TDI 122", "2.0 TDI 150", "2.0 TDI 200"], reservoir=58, remarques="Tiguan et Allspace (7 places)")
L += g("Tiguan", "CT1", "1", "2024-01", None,
       ["1.5 eTSI 130", "1.5 eTSI 150", "2.0 TSI 204", "2.0 TSI 265", ("eHybrid 204", ph(20, 45)),
        ("eHybrid 272", ph(20, 45)), "2.0 TDI 150", "2.0 TDI 193"], reservoir=58)
L += g("Tayron", "CT2", "1", "2024-11", None,
       ["1.5 eTSI 150", "2.0 TSI 204", "2.0 TSI 265", ("eHybrid 204", ph(20, 45)), ("eHybrid 272", ph(20, 45)),
        "2.0 TDI 150", "2.0 TDI 193"], places=5, reservoir=58, remarques="SUV 5 ou 7 places (succède au Tiguan Allspace)")

# ---------------------------------------------------------------- Touran / Sharan
L += g("Touran", "1T", "1", "2003-02", "2006-09",
       ["1.6 102", "1.6 FSI 115", "2.0 FSI 150", "1.9 TDI 90", "1.9 TDI 105", "2.0 TDI 140"], places=7, reservoir=60,
       remarques="Monospace 5 ou 7 places")
L += g("Touran", "1T", "2", "2006-10", "2010-07",
       ["1.6 102", "1.4 TSI 140", "1.4 TSI 170", "2.0 EcoFuel 109", "1.9 TDI 90", "1.9 TDI 105", "2.0 TDI 140",
        "2.0 TDI 170"], places=7, reservoir=60, remarques="Monospace 5 ou 7 places")
L += g("Touran", "1T", "3", "2010-08", "2015-05",
       ["1.2 TSI 105", "1.4 TSI 140", "1.4 TSI 150", "1.6 TDI 90", "1.6 TDI 105", "2.0 TDI 140", "2.0 TDI 170"],
       places=7, reservoir=60, remarques="Monospace 5 ou 7 places")
L += g("Touran", "5T", "1", "2015-06", "2023-12",
       ["1.0 TSI 115", "1.2 TSI 110", "1.4 TSI 150", "1.5 TSI 150", "1.6 TDI 115", "2.0 TDI 150", "2.0 TDI 190"],
       places=7, reservoir=58, remarques="Monospace 5 ou 7 places")
L += g("Sharan", "7N", "1", "2010-09", "2015-05",
       ["1.4 TSI 150", "2.0 TSI 200", "2.0 TDI 115", "2.0 TDI 140", "2.0 TDI 170"], places=7, reservoir=70,
       remarques="Monospace 5 à 7 places")
L += g("Sharan", "7N", "2", "2015-06", "2022-02",
       ["1.4 TSI 150", "2.0 TSI 220", "2.0 TDI 115", "2.0 TDI 150", "2.0 TDI 184"], places=7, reservoir=70,
       remarques="Monospace 5 à 7 places")

# ---------------------------------------------------------------- Passat / Arteon
L += g("Passat", "B5", "1", "1996-10", "2000-10",
       ["1.6 101", "1.8 125", "1.8T 150", "2.8 V6 193", "1.9 TDI 90", "1.9 TDI 110", "2.5 V6 TDI 150"],
       portes=4, reservoir=62, remarques="Berline et Variant")
L += g("Passat", "B5", "2", "2000-11", "2005-03",
       ["1.6 102", "1.8T 150", "2.0 115", "2.3 V5 170", "2.8 V6 193", "4.0 W8 275", "1.9 TDI 100", "1.9 TDI 130",
        "2.0 TDI 136", "2.5 V6 TDI 163"], portes=4, reservoir=62, remarques="Berline et Variant (B5.5)")
L += g("Passat", "B6", "1", "2005-03", "2010-10",
       [("1.4 TSI 122", {"debut": "2008-01"}), "1.6 FSI 115", ("1.8 TSI 160", {"debut": "2007-01"}), "2.0 FSI 150",
        "2.0 TFSI 200", "3.2 VR6 250", ("R36 3.6 VR6 300", {"debut": "2007-12"}), "1.9 TDI 105",
        ("1.6 TDI 105", {"debut": "2009-06"}), "2.0 TDI 110", "2.0 TDI 140", "2.0 TDI 170"],
       portes=4, reservoir=70, remarques="Berline, Variant, CC (2008)")
L += g("Passat", "B7", "1", "2010-11", "2014-07",
       ["1.4 TSI 122", "1.4 TSI 150 EcoFuel", "1.8 TSI 160", "2.0 TSI 210", "3.6 VR6 300", "1.6 TDI 105",
        "2.0 TDI 140", "2.0 TDI 170", "2.0 TDI 177"], portes=4, reservoir=70, remarques="Berline, Variant, Alltrack, CC")
L += g("Passat", "B8", "1", "2014-08", "2019-07",
       ["1.4 TSI 125", "1.4 TSI 150", "1.8 TSI 180", "2.0 TSI 220", "2.0 TSI 280", ("GTE 218", ph(10, 50, debut="2015-09")),
        "1.6 TDI 120", "2.0 TDI 150", "2.0 TDI 190", "2.0 TDI 240"], portes=4, reservoir=66,
       remarques="Berline, Variant, Alltrack")
L += g("Passat", "B8", "2", "2019-08", "2023-08",
       ["1.5 TSI 150", "2.0 TSI 190", "2.0 TSI 272", ("GTE 218", ph(13, 50)), "1.6 TDI 120", "2.0 TDI 122",
        "2.0 TDI 150", "2.0 TDI 200", "2.0 TDI 240"], portes=4, reservoir=66, remarques="Berline, Variant, Alltrack")
L += g("Passat", "B9", "1", "2024-01", None,
       ["1.5 eTSI 150", "2.0 TSI 204", "2.0 TSI 265", ("eHybrid 204", ph(20, 45)), ("eHybrid 272", ph(20, 45)),
        "2.0 TDI 122", "2.0 TDI 150", "2.0 TDI 193"], reservoir=66, remarques="Variant uniquement")
L += g("Arteon", "3H", "1", "2017-06", "2020-09",
       ["1.5 TSI 150", "2.0 TSI 190", "2.0 TSI 280", "2.0 TDI 150", "2.0 TDI 190", "2.0 TDI 240"], reservoir=66,
       remarques="Fastback")
L += g("Arteon", "3H", "2", "2020-10", "2024-06",
       ["1.5 TSI 150", "2.0 TSI 190", "R 2.0 TSI 320", ("eHybrid 218", ph(13, 50)), "2.0 TDI 150", "2.0 TDI 200"],
       reservoir=66, remarques="Fastback et Shooting Brake")

# ---------------------------------------------------------------- Coupés / cabriolets
L += g("Scirocco", "13", "1", "2008-08", "2014-04",
       ["1.4 TSI 122", "1.4 TSI 160", "2.0 TSI 200", "2.0 TSI 210", ("R 2.0 TSI 265", {"debut": "2009-09"}),
        "2.0 TDI 140", "2.0 TDI 170"], portes=3, places=4, reservoir=55, remarques="Coupé 3 portes")
L += g("Scirocco", "13", "2", "2014-05", "2017-11",
       ["1.4 TSI 125", "2.0 TSI 180", "2.0 TSI 220", "R 2.0 TSI 280", "2.0 TDI 150", "2.0 TDI 184"],
       portes=3, places=4, reservoir=55, remarques="Coupé 3 portes")
L += g("Beetle", "5C", "1", "2011-10", "2019-07",
       ["1.2 TSI 105", "1.4 TSI 160", "2.0 TSI 200", "2.0 TSI 220", "1.6 TDI 105", "2.0 TDI 140", "2.0 TDI 150"],
       portes=3, places=4, reservoir=55, remarques="Coupé 3 portes et Cabriolet ; restylage 2016 non détaillé")
L += g("Eos", "1F", "1", "2006-04", "2015-05",
       ["1.4 TSI 122", "1.4 TSI 160", "1.6 FSI 115", "2.0 FSI 150", "2.0 TFSI 200", "2.0 TSI 210", "3.2 VR6 250",
        "2.0 TDI 140"], portes=2, places=4, reservoir=55, remarques="Coupé-cabriolet ; restylage 2011 non détaillé")
L += g("Jetta", "16", "1", "2010-11", "2018-10",
       ["1.2 TSI 105", "1.4 TSI 122", "1.4 TSI 150", ("Hybrid 1.4 TSI 170", {"debut": "2013-01"}), "2.0 TSI 211",
        "1.6 TDI 105", "2.0 TDI 140", "2.0 TDI 150"], portes=4, reservoir=55, remarques="Berline ; restylage 2014 non détaillé")

# ---------------------------------------------------------------- Touareg / Phaeton
L += g("Touareg", "7L", "1", "2002-10", "2010-03",
       ["3.2 V6 220", ("3.2 V6 241", {"debut": "2004-09"}), ("3.6 V6 280", {"debut": "2006-09"}), "4.2 V8 310",
        ("4.2 V8 350", {"debut": "2006-09"}), ("6.0 W12 450", {"debut": "2005-01"}), "2.5 TDI 174",
        ("3.0 TDI 225", {"debut": "2004-10"}), ("3.0 TDI 240", {"debut": "2007-11"}), "5.0 V10 TDI 313",
        ("5.0 V10 TDI 350", {"debut": "2007-11"})], reservoir=100, remarques="SUV ; restylage 2007 non détaillé")
L += g("Touareg", "7P", "1", "2010-04", "2014-10",
       ["3.6 VR6 280", "4.2 V8 360", "Hybrid 3.0 TSI 380", "3.0 TDI 204", "3.0 TDI 240", "4.2 TDI 340"],
       reservoir=85, remarques="SUV")
L += g("Touareg", "7P", "2", "2014-11", "2018-02",
       ["3.0 TDI 204", "3.0 TDI 262", "4.2 TDI 340"], reservoir=85, remarques="SUV")
L += g("Touareg", "CR", "1", "2018-03", "2023-05",
       ["3.0 TSI 340", "3.0 TDI 231", "3.0 TDI 286", ("4.0 TDI 421", {"fin": "2020-12"}),
        ("R eHybrid 462", ph(14, 75, debut="2020-09")), ("eHybrid 381", ph(14, 75, debut="2021-01"))],
       reservoir=90, remarques="SUV")
L += g("Touareg", "CR", "2", "2023-06", None,
       ["3.0 TDI 231", "3.0 TDI 286", ("eHybrid 381", ph(14, 75)), ("R eHybrid 462", ph(14, 75))],
       reservoir=90, remarques="SUV")
L += g("Phaeton", "3D", "1", "2002-05", "2016-03",
       ["3.2 V6 241", "3.6 VR6 280", "4.2 V8 335", "6.0 W12 420", ("6.0 W12 450", {"debut": "2008-01"}),
        "3.0 TDI 224", ("3.0 TDI 240", {"debut": "2010-06"}), ("3.0 TDI 262", {"debut": "2014-01"}),
        ("5.0 V10 TDI 313", {"fin": "2010-06"})], portes=4, reservoir=90,
       remarques="Berline de luxe ; restylages 2007 et 2010 non détaillés")

# ---------------------------------------------------------------- Utilitaires
L += g("Caddy", "2K", "1", "2004-03", "2010-08",
       ["1.4 75", "1.6 102", "2.0 EcoFuel 109", "1.9 SDI 69", "1.9 TDI 75", "1.9 TDI 105", "2.0 SDI 70"],
       places=2, reservoir=60, remarques="Fourgon et Combi/Life 5 à 7 places")
L += g("Caddy", "2K", "2", "2010-09", "2015-05",
       ["1.2 TSI 86", "1.2 TSI 105", "1.6 102", "2.0 EcoFuel 109", "1.6 TDI 75", "1.6 TDI 102", "2.0 TDI 110",
        "2.0 TDI 140"], places=2, reservoir=60, remarques="Fourgon et Combi/Life 5 à 7 places")
L += g("Caddy", "SA", "1", "2015-06", "2020-09",
       ["1.0 TSI 102", "1.2 TSI 84", "1.4 TSI 125", "2.0 TDI 75", "2.0 TDI 102", "2.0 TDI 122", "2.0 TDI 150"],
       places=2, reservoir=55, remarques="Fourgon et Combi/Life 5 à 7 places")
L += g("Caddy", "SB", "1", "2020-10", None,
       ["1.5 TSI 114", "2.0 TDI 75", "2.0 TDI 102", "2.0 TDI 122", ("eHybrid 150", ph(20, 32, debut="2024-06"))],
       places=2, reservoir=50, remarques="Cargo et Caddy 5 à 7 places")
L += g("Transporter", "T5", "1", "2003-04", "2009-08",
       ["2.0 115", "3.2 V6 235", "1.9 TDI 86", "1.9 TDI 105", "2.5 TDI 130", "2.5 TDI 174"],
       portes=4, places=3, reservoir=80, remarques="Fourgon, Caravelle, Multivan, California")
L += g("Transporter", "T5", "2", "2009-09", "2015-05",
       ["2.0 TSI 150", "2.0 TSI 204", "2.0 TDI 84", "2.0 TDI 102", "2.0 TDI 114", "2.0 TDI 140", "2.0 TDI 180"],
       portes=4, places=3, reservoir=80, remarques="T5.1 — Fourgon, Caravelle, Multivan, California")
L += g("Transporter", "T6", "1", "2015-06", "2019-08",
       ["2.0 TSI 150", "2.0 TSI 204", "2.0 TDI 84", "2.0 TDI 102", "2.0 TDI 114", "2.0 TDI 150", "2.0 TDI 204"],
       portes=4, places=3, reservoir=80, remarques="Fourgon, Caravelle, Multivan, California")
L += g("Transporter", "T6", "2", "2019-09", "2024-12",
       ["2.0 TDI 90", "2.0 TDI 110", "2.0 TDI 150", "2.0 TDI 199", ("ABT e-Transporter 112", el(37, debut="2020-01"))],
       portes=4, places=3, reservoir=70, remarques="T6.1 — Fourgon, Caravelle, California")
L += g("Multivan", "ST7", "1", "2022-01", None,
       ["1.5 TSI 136", "2.0 TSI 204", ("eHybrid 218", ph(13, 45)), ("2.0 TDI 150", {"debut": "2022-09"})],
       places=7, reservoir=52, remarques="Monospace 6/7 places (T7)")
L += g("Crafter", "2E", "1", "2006-04", "2011-04",
       ["2.5 TDI 88", "2.5 TDI 109", "2.5 TDI 136", "2.5 TDI 163"], portes=4, places=3, reservoir=75,
       remarques="Grand fourgon")
L += g("Crafter", "2E", "2", "2011-05", "2016-12",
       ["2.0 TDI 109", "2.0 TDI 136", "2.0 TDI 163"], portes=4, places=3, reservoir=75, remarques="Grand fourgon")
L += g("Crafter", "SY", "1", "2017-01", None,
       ["2.0 TDI 102", "2.0 TDI 122", "2.0 TDI 140", "2.0 TDI 177", ("e-Crafter 136", el(36, debut="2018-09", fin="2022-12"))],
       portes=4, places=3, reservoir=75, remarques="Grand fourgon ; restylage 2024 non détaillé")
L += g("Amarok", "2H", "1", "2010-02", "2016-08",
       ["2.0 TDI 122", "2.0 TDI 140", "2.0 TDI 163", "2.0 TDI 180"], portes=4, reservoir=80, remarques="Pick-up")
L += g("Amarok", "2H", "2", "2016-09", "2020-12",
       ["3.0 V6 TDI 163", "3.0 V6 TDI 204", "3.0 V6 TDI 224", "3.0 V6 TDI 258"], portes=4, reservoir=80,
       remarques="Pick-up")
L += g("Amarok", "AMK2", "1", "2022-11", None,
       ["2.0 TDI 170", "2.0 TDI 205", "3.0 V6 TDI 240"], portes=4, reservoir=80,
       remarques="Pick-up (base Ford Ranger)")

# ---------------------------------------------------------------- Moteurs
D, E_ = "DSL", "ESS"
FAMILLES = {
    # essence anciens (Golf I à III)
    "EA111-1.1": f("ATM", E_, 1.1, "COURROIE", 4, 5600, 3500, "15W40", 3.5, 7500),
    "EA111-1.3": f("ATM", E_, 1.3, "COURROIE", 4, 5200, 3400, "15W40", 3.5, 7500),
    "EA827-1.5": f("ATM", E_, 1.5, "COURROIE", 4, 5800, 3500, "15W40", 3.5, 7500),
    "EA827-1.6GTI": f("ATM", E_, 1.6, "COURROIE", 4, 6100, 5000, "15W40", 3.5, 7500),
    "EA827-1.8-8v": f("ATM", E_, 1.8, "COURROIE", 4, 5500, 3100, "15W40", 4.0, 7500),
    "EA827-1.8-16v": f("ATM", E_, 1.8, "COURROIE", 4, 6100, 4600, "15W40", 4.0, 7500),
    "EA827-1.8G60": f("TURBO", E_, 1.8, "COURROIE", 4, 5600, 4000, "15W40", 4.0, 7500),
    "EA827-2.0-16v": f("ATM", E_, 2.0, "COURROIE", 4, 6000, 4800, "10W40", 4.0, 15000),
    "EA827-1.5D": f("ATM", D, 1.5, "COURROIE", 4, 5000, 3000, "15W40", 3.5, 7500),
    "EA827-1.6D": f("ATM", D, 1.6, "COURROIE", 4, 4800, 2300, "15W40", 3.5, 7500),
    "EA827-1.6TD": f("TURBO", D, 1.6, "COURROIE", 4, 4500, 2600, "15W40", 3.5, 7500),
    "EA827-1.9D": f("ATM", D, 1.9, "COURROIE", 4, 4400, 2000, "15W40", 4.5, 15000),
    "EA827-1.9TD": f("TURBO", D, 1.9, "COURROIE", 4, 4200, 2400, "15W40", 4.5, 15000),
    # essence
    "EA111-1.0": f("ATM", E_, 1.0, "COURROIE", 4, 5000, 3000, "5W30", 3.2, 15000),
    "EA111-1.2": f("ATM", E_, 1.2, "CHAINE", 3, 5200, 3000, "5W30", 2.8, 15000),
    "EA111-1.4": f("ATM", E_, 1.4, "COURROIE", 4, 5000, 3800, "5W30", 3.2, 15000),
    "EA111-1.4FSI": f("ATM", E_, 1.4, "COURROIE", 4, 5200, 3750, "5W30", 3.6, 15000),
    "EA111-1.6": f("ATM", E_, 1.6, "COURROIE", 4, 5600, 3800, "5W30", 3.6, 15000),
    "EA111-1.6FSI": f("ATM", E_, 1.6, "COURROIE", 4, 6000, 4000, "5W30", 3.6, 15000),
    "EA111-1.2TSI": f("TURBO", E_, 1.2, "CHAINE", 4, 5000, 1500, "5W30", 3.6, 15000),
    "EA111-1.4TSI": f("TURBO", E_, 1.4, "CHAINE", 4, 5000, 1500, "5W30", 3.6, 15000),
    "EA111-1.4TSI-HYB": f("HYB_TE", E_, 1.4, "CHAINE", 4, 5000, 1500, "5W30", 3.6, 15000),
    "EA827-1.6": f("ATM", E_, 1.6, "COURROIE", 4, 5600, 3800, "10W40", 4.5, 15000),
    "EA827-1.8": f("ATM", E_, 1.8, "COURROIE", 4, 5800, 3500, "10W40", 4.5, 15000),
    "EA827-2.0": f("ATM", E_, 2.0, "COURROIE", 4, 5400, 2600, "10W40", 4.0, 15000),
    "EA113-1.6": f("ATM", E_, 1.6, "COURROIE", 4, 5600, 3800, "5W30", 4.5, 15000),
    "EA113-1.8T": f("TURBO", E_, 1.8, "COURROIE", 4, 5700, 1950, "5W40", 4.5, 15000),
    "EA113-2.0FSI": f("ATM", E_, 2.0, "COURROIE", 4, 6000, 3500, "5W30", 4.6, 15000),
    "EA113-2.0TFSI": f("TURBO", E_, 2.0, "COURROIE", 4, 5100, 1800, "5W30", 4.6, 15000),
    "EA113-2.0CNG": f("ATM", "CNG", 2.0, "COURROIE", 4, 5400, 3500, "5W30", 4.5, 15000),
    "EA211-1.0MPI": f("ATM", E_, 1.0, "COURROIE", 3, 6200, 3000, "0W20", 4.0, 30000),
    "EA211-1.0TSI": f("TURBO", E_, 1.0, "COURROIE", 3, 5000, 2000, "0W20", 4.0, 30000),
    "EA211-1.0eTSI": f("HYB_TE", E_, 1.0, "COURROIE", 3, 5500, 2000, "0W20", 4.0, 30000),
    "EA211-1.2TSI": f("TURBO", E_, 1.2, "COURROIE", 4, 4500, 1400, "0W30", 4.0, 30000),
    "EA211-1.4TSI": f("TURBO", E_, 1.4, "COURROIE", 4, 5000, 1500, "0W30", 4.0, 30000),
    "EA211-1.5TSI": f("TURBO", E_, 1.5, "COURROIE", 4, 5000, 1500, "0W20", 4.3, 30000),
    "EA211-1.5eTSI": f("HYB_TE", E_, 1.5, "COURROIE", 4, 5000, 1500, "0W20", 4.3, 30000),
    "EA211-1.4TSI-PHEV": f("HYB_TE", E_, 1.4, "COURROIE", 4, 5000, 1550, "0W30", 4.0, 30000),
    "EA211-1.5TSI-PHEV": f("HYB_TE", E_, 1.5, "COURROIE", 4, 5000, 1550, "0W20", 4.3, 30000),
    "EA888-1.8TSI": f("TURBO", E_, 1.8, "CHAINE", 4, 5000, 1500, "5W30", 4.6, 15000),
    "EA888-2.0TSI": f("TURBO", E_, 2.0, "CHAINE", 4, 5000, 1700, "0W20", 5.7, 30000),
    "EA390-2.3V5": f("ATM", E_, 2.3, "CHAINE", 5, 6000, 3200, "5W40", 4.5, 15000, a="VR"),
    "VR6-2.8": f("ATM", E_, 2.8, "CHAINE", 6, 5800, 3200, "5W40", 5.5, 15000, a="VR"),
    "VR6-3.2": f("ATM", E_, 3.2, "CHAINE", 6, 6250, 2800, "5W40", 5.5, 15000, a="VR"),
    "VR6-3.6": f("ATM", E_, 3.6, "CHAINE", 6, 6200, 2750, "5W30", 5.5, 15000, a="VR"),
    "V6-2.8": f("ATM", E_, 2.8, "COURROIE", 6, 6000, 3200, "5W40", 5.5, 15000, a="V"),
    "W8-4.0": f("ATM", E_, 4.0, "CHAINE", 8, 6000, 2750, "5W30", 7.0, 15000, a="W"),
    "V8-4.2": f("ATM", E_, 4.2, "CHAINE", 8, 6800, 3500, "5W30", 8.0, 15000, a="V"),
    "W12-6.0": f("ATM", E_, 6.0, "CHAINE", 12, 6000, 3000, "5W30", 10.0, 15000, a="W"),
    "EA839-3.0TSI": f("TURBO", E_, 3.0, "CHAINE", 6, 5200, 1340, "0W20", 7.0, 30000, a="V"),
    "EA839-PHEV": f("HYB_TE", E_, 3.0, "CHAINE", 6, 5300, 1500, "0W20", 7.0, 30000, a="V"),
    "EA837-3.0TSI-HYB": f("HYB_TE", E_, 3.0, "CHAINE", 6, 5500, 1000, "5W30", 7.0, 15000, a="V"),
    # diesel
    "EA180-1.7SDI": f("ATM", D, 1.7, "COURROIE", 4, 4200, 2200, "5W30", 4.3, 15000),
    "EA180-1.9SDI": f("ATM", D, 1.9, "COURROIE", 4, 4000, 2200, "5W30", 4.3, 15000),
    "EA180-1.9TDI": f("TURBO", D, 1.9, "COURROIE", 4, 4000, 1900, "5W30", 4.3, 15000),
    "EA188-1.2TDI": f("TURBO", D, 1.2, "COURROIE", 3, 4000, 1800, "5W30", 3.5, 15000),
    "EA188-1.4TDI": f("TURBO", D, 1.4, "COURROIE", 3, 4000, 2000, "5W30", 3.8, 15000),
    "EA188-2.0SDI": f("ATM", D, 2.0, "COURROIE", 4, 4200, 2200, "5W30", 4.3, 15000),
    "EA188-2.0TDI": f("TURBO", D, 2.0, "COURROIE", 4, 4000, 1750, "5W30", 4.3, 15000),
    "EA189-1.2TDI": f("TURBO", D, 1.2, "COURROIE", 3, 4200, 2000, "5W30", 4.3, 30000),
    "EA189-1.6TDI": f("TURBO", D, 1.6, "COURROIE", 4, 4400, 1500, "5W30", 4.3, 30000),
    "EA189-2.0TDI": f("TURBO", D, 2.0, "COURROIE", 4, 4200, 1750, "5W30", 4.3, 30000),
    "EA288-1.4TDI": f("TURBO", D, 1.4, "COURROIE", 3, 3500, 1750, "0W30", 4.3, 30000),
    "EA288-1.6TDI": f("TURBO", D, 1.6, "COURROIE", 4, 3500, 1750, "0W30", 4.3, 30000),
    "EA288-2.0TDI": f("TURBO", D, 2.0, "COURROIE", 4, 3500, 1750, "0W30", 4.6, 30000),
    "EA288-2.0BiTDI": f("TURBO", D, 2.0, "COURROIE", 4, 4000, 1750, "0W30", 4.6, 30000),
    "EA288evo-2.0TDI": f("TURBO", D, 2.0, "COURROIE", 4, 3500, 1750, "0W20", 5.0, 30000),
    "R5-2.5TDI": f("TURBO", D, 2.5, "CHAINE", 5, 3500, 2000, "5W30", 7.0, 15000),
    "V6-2.5TDI": f("TURBO", D, 2.5, "COURROIE", 6, 4000, 1500, "5W30", 6.5, 15000, a="V"),
    "V6-3.0TDI": f("TURBO", D, 3.0, "CHAINE", 6, 4000, 1500, "5W30", 8.0, 30000, a="V"),
    "V8-4.0TDI": f("TURBO", D, 4.0, "CHAINE", 8, 3750, 1250, "0W30", 10.0, 30000, a="V"),
    "V8-4.2TDI": f("TURBO", D, 4.2, "CHAINE", 8, 4000, 1750, "5W30", 9.0, 30000, a="V"),
    "V10-5.0TDI": f("TURBO", D, 4.9, "CHAINE", 10, 4000, 2000, "5W30", 12.0, 15000, a="V"),
    "EcoBlue-2.0": f("TURBO", D, 2.0, "COURROIE", 4, 3500, 1750, "0W30", 6.0, 30000),
    "Lion-3.0V6": f("TURBO", D, 3.0, "COURROIE", 6, 3250, 1750, "5W30", 7.0, 30000, a="V"),
    # électrique
    "EUP-EV": electrique(), "EGOLF-EV": electrique(), "MEB-EV": electrique(), "MEB-AWD": electrique(),
    "ABT-EV": electrique(), "ECRAFTER-EV": electrique(),
}

TABLE = {
    # --- Golf I à III
    "1.1 50": ("EA111-1.1", 50, 77), "1.3 55": ("EA111-1.3", 55, 96), "1.3 60": ("EA111-1.3", 60, 95),
    "1.5 70": ("EA827-1.5", 70, 112), "1.6 72": ("EA827-1.6", 72, 125), "1.6 75": ("EA827-1.6", 75, 125),
    "1.6 110": ("EA827-1.6GTI", 110, 137), "1.8 75": ("EA827-1.8-8v", 75, 140), "1.8 90": ("EA827-1.8-8v", 90, 142),
    "1.8 98": ("EA827-1.8-8v", 98, 145), "1.8 107": ("EA827-1.8-8v", 107, 157), "1.8 112": ("EA827-1.8-8v", 112, 153),
    "16v 1.8 139": ("EA827-1.8-16v", 139, 168), "16v 1.8 129": ("EA827-1.8-16v", 129, 165),
    "G60 1.8 160": ("EA827-1.8G60", 160, 225), "Rallye G60 1.8 160": ("EA827-1.8G60", 160, 225),
    "2.0 16v 150": ("EA827-2.0-16v", 150, 180), "VR6 2.8 174": ("VR6-2.8", 174, 235),
    "VR6 2.9 190": ("VR6-2.8", 190, 245),
    "1.5 D 50": ("EA827-1.5D", 50, 80), "1.6 D 54": ("EA827-1.6D", 54, 100), "1.6 TD 70": ("EA827-1.6TD", 70, 130),
    "1.6 TD 80": ("EA827-1.6TD", 80, 155), "1.9 D 64": ("EA827-1.9D", 64, 124), "1.9 TD 75": ("EA827-1.9TD", 75, 150),
    # --- essence MPI / FSI anciens
    "1.0 50": ("EA111-1.0", 50, 86), "1.2 55": ("EA111-1.2", 55, 108), "1.2 60": ("EA111-1.2", 60, 108),
    "1.2 65": ("EA111-1.2", 65, 112), "1.2 70": ("EA111-1.2", 70, 112),
    "1.4 60": ("EA111-1.4", 60, 116), "1.4 75": ("EA111-1.4", 75, 126), "1.4 80": ("EA111-1.4", 80, 132),
    "1.4 85": ("EA111-1.4", 85, 132), "1.4 16v 75": ("EA111-1.4", 75, 126), "1.4 16v 100": ("EA111-1.4", 100, 126),
    "1.4 FSI 86": ("EA111-1.4FSI", 86, 130), "1.4 FSI 90": ("EA111-1.4FSI", 90, 130),
    "1.4 FSI 105": ("EA111-1.4FSI", 105, 130), "1.6 105": ("EA111-1.6", 105, 148), "1.6 125": ("EA111-1.6", 125, 152),
    "1.6 FSI 110": ("EA111-1.6FSI", 110, 155), "1.6 FSI 115": ("EA111-1.6FSI", 115, 155),
    "1.6 100": ("EA113-1.6", 100, 145), "1.6 101": ("EA827-1.6", 101, 140), "1.6 102": ("EA113-1.6", 102, 148),
    "1.8 125": ("EA827-1.8", 125, 168), "2.0 115": ("EA827-2.0", 115, 170),
    "1.8T 150": ("EA113-1.8T", 150, 210), "1.8T 180": ("EA113-1.8T", 180, 235),
    "2.0 FSI 150": ("EA113-2.0FSI", 150, 200), "2.0 TFSI 200": ("EA113-2.0TFSI", 200, 280),
    "2.0 TFSI 230": ("EA113-2.0TFSI", 230, 300), "2.0 EcoFuel 109": ("EA113-2.0CNG", 109, 160),
    "2.3 V5 150": ("EA390-2.3V5", 150, 205), "2.3 V5 170": ("EA390-2.3V5", 170, 220),
    "2.8 V6 193": ("V6-2.8", 193, 280), "4.0 W8 275": ("W8-4.0", 275, 370),
    "3.2 241": ("VR6-3.2", 241, 320), "3.2 250": ("VR6-3.2", 250, 320), "3.2 VR6 250": ("VR6-3.2", 250, 320),
    "3.2 V6 220": ("VR6-3.2", 220, 305), "3.2 V6 235": ("VR6-3.2", 235, 315), "3.2 V6 241": ("VR6-3.2", 241, 315),
    "3.6 V6 280": ("VR6-3.6", 280, 360), "3.6 VR6 280": ("VR6-3.6", 280, 360), "3.6 VR6 300": ("VR6-3.6", 300, 350),
    "R36 3.6 VR6 300": ("VR6-3.6", 300, 350),
    "4.2 V8 310": ("V8-4.2", 310, 410), "4.2 V8 335": ("V8-4.2", 335, 430), "4.2 V8 350": ("V8-4.2", 350, 440),
    "4.2 V8 360": ("V8-4.2", 360, 445), "6.0 W12 420": ("W12-6.0", 420, 550), "6.0 W12 450": ("W12-6.0", 450, 600),
    "3.0 TSI 340": ("EA839-3.0TSI", 340, 450), "Hybrid 3.0 TSI 380": ("EA837-3.0TSI-HYB", 380, 580),
    "eHybrid 381": ("EA839-PHEV", 381, 600), "R eHybrid 462": ("EA839-PHEV", 462, 700),
    # --- TSI EA111 (par défaut) / EA211 (@M)
    "1.2 TSI 85": ("EA111-1.2TSI", 85, 160), "1.2 TSI 86": ("EA111-1.2TSI", 86, 160),
    "1.2 TSI 90": ("EA111-1.2TSI", 90, 160), "1.2 TSI 105": ("EA111-1.2TSI", 105, 175),
    "1.2 TSI 85@M": ("EA211-1.2TSI", 85, 160), "1.2 TSI 84": ("EA211-1.2TSI", 84, 160),
    "1.2 TSI 90@M": ("EA211-1.2TSI", 90, 160), "1.2 TSI 105@M": ("EA211-1.2TSI", 105, 175),
    "1.2 TSI 110": ("EA211-1.2TSI", 110, 175),
    "1.4 TSI 122": ("EA111-1.4TSI", 122, 200), "1.4 TSI 140": ("EA111-1.4TSI", 140, 220),
    "1.4 TSI 150": ("EA111-1.4TSI", 150, 240), "1.4 TSI 150 EcoFuel": ("EA111-1.4TSI", 150, 220),
    "1.4 TSI 160": ("EA111-1.4TSI", 160, 240), "1.4 TSI 170": ("EA111-1.4TSI", 170, 240),
    "1.4 TSI 180": ("EA111-1.4TSI", 180, 250), "Hybrid 1.4 TSI 170": ("EA111-1.4TSI-HYB", 170, 250),
    "1.4 TSI 122@M": ("EA211-1.4TSI", 122, 200), "1.4 TSI 125": ("EA211-1.4TSI", 125, 200),
    "1.4 TSI 140@M": ("EA211-1.4TSI", 140, 250), "1.4 TSI 150@M": ("EA211-1.4TSI", 150, 250),
    "1.0 MPI 60": ("EA211-1.0MPI", 60, 95), "1.0 MPI 65": ("EA211-1.0MPI", 65, 95),
    "1.0 MPI 75": ("EA211-1.0MPI", 75, 95), "1.0 MPI 80": ("EA211-1.0MPI", 80, 93),
    "1.0 TSI 85": ("EA211-1.0TSI", 85, 175), "1.0 TSI 90": ("EA211-1.0TSI", 90, 160),
    "1.0 TSI 95": ("EA211-1.0TSI", 95, 175), "1.0 TSI 102": ("EA211-1.0TSI", 102, 175),
    "1.0 TSI 110": ("EA211-1.0TSI", 110, 200), "1.0 TSI 115": ("EA211-1.0TSI", 115, 200),
    "1.0 eTSI 110": ("EA211-1.0eTSI", 110, 200),
    "1.5 TSI 114": ("EA211-1.5TSI", 114, 220), "1.5 TSI 116": ("EA211-1.5TSI", 116, 220),
    "1.5 TSI 130": ("EA211-1.5TSI", 130, 200), "1.5 TSI 136": ("EA211-1.5TSI", 136, 220),
    "1.5 TSI 150": ("EA211-1.5TSI", 150, 250), "1.5 eTSI 116": ("EA211-1.5eTSI", 116, 220),
    "1.5 eTSI 130": ("EA211-1.5eTSI", 130, 200), "1.5 eTSI 150": ("EA211-1.5eTSI", 150, 250),
    "GTE 204": ("EA211-1.4TSI-PHEV", 204, 350), "GTE 218": ("EA211-1.4TSI-PHEV", 218, 400),
    "GTE 245": ("EA211-1.4TSI-PHEV", 245, 400), "eHybrid 204": ("EA211-1.4TSI-PHEV", 204, 350),
    "eHybrid 218": ("EA211-1.4TSI-PHEV", 218, 350), "eHybrid 245": ("EA211-1.4TSI-PHEV", 245, 400),
    "eHybrid 204@N": ("EA211-1.5TSI-PHEV", 204, 350), "eHybrid 272": ("EA211-1.5TSI-PHEV", 272, 400),
    "GTE 272": ("EA211-1.5TSI-PHEV", 272, 400), "eHybrid 150": ("EA211-1.5TSI-PHEV", 150, 350),
    # --- EA888
    "1.8 TSI 160": ("EA888-1.8TSI", 160, 250), "1.8 TSI 180": ("EA888-1.8TSI", 180, 250),
    "1.8 TSI 192": ("EA888-1.8TSI", 192, 250),
    "2.0 TSI 170": ("EA888-2.0TSI", 170, 280), "2.0 TSI 180": ("EA888-2.0TSI", 180, 280),
    "2.0 TSI 190": ("EA888-2.0TSI", 190, 320), "2.0 TSI 200": ("EA888-2.0TSI", 200, 280),
    "2.0 TSI 204": ("EA888-2.0TSI", 204, 320), "2.0 TSI 207": ("EA888-2.0TSI", 207, 320),
    "2.0 TSI 210": ("EA888-2.0TSI", 210, 280), "2.0 TSI 211": ("EA888-2.0TSI", 211, 280),
    "2.0 TSI 220": ("EA888-2.0TSI", 220, 350), "2.0 TSI 230": ("EA888-2.0TSI", 230, 350),
    "2.0 TSI 235": ("EA888-2.0TSI", 235, 300), "2.0 TSI 245": ("EA888-2.0TSI", 245, 370),
    "2.0 TSI 265": ("EA113-2.0TFSI", 265, 350), "2.0 TSI 265@M": ("EA888-2.0TSI", 265, 370),
    "2.0 TSI 270": ("EA113-2.0TFSI", 270, 350), "2.0 TSI 272": ("EA888-2.0TSI", 272, 350),
    "2.0 TSI 280": ("EA888-2.0TSI", 280, 350), "2.0 TSI 290": ("EA888-2.0TSI", 290, 380),
    "2.0 TSI 300": ("EA888-2.0TSI", 300, 380), "2.0 TSI 310": ("EA888-2.0TSI", 310, 380),
    "2.0 TSI 320": ("EA888-2.0TSI", 320, 420), "2.0 TSI 333": ("EA888-2.0TSI", 333, 420),
    "2.0 TSI 150": ("EA888-2.0TSI", 150, 280),
    # --- diesel PD / anciens
    "1.7 SDI 60": ("EA180-1.7SDI", 60, 115), "1.9 SDI 64": ("EA180-1.9SDI", 64, 125),
    "1.9 SDI 68": ("EA180-1.9SDI", 68, 133), "1.9 SDI 69": ("EA180-1.9SDI", 69, 140),
    "1.9 TDI 75": ("EA180-1.9TDI", 75, 210), "1.9 TDI 86": ("EA180-1.9TDI", 86, 200),
    "1.9 TDI 90": ("EA180-1.9TDI", 90, 210), "1.9 TDI 100": ("EA180-1.9TDI", 100, 240),
    "1.9 TDI 105": ("EA180-1.9TDI", 105, 250), "1.9 TDI 110": ("EA180-1.9TDI", 110, 235),
    "1.9 TDI 115": ("EA180-1.9TDI", 115, 285), "1.9 TDI 130": ("EA180-1.9TDI", 130, 310),
    "1.9 TDI 150": ("EA180-1.9TDI", 150, 320),
    "1.2 TDI 61": ("EA188-1.2TDI", 61, 140), "1.4 TDI 70": ("EA188-1.4TDI", 70, 155),
    "1.4 TDI 75": ("EA188-1.4TDI", 75, 195), "1.4 TDI 80": ("EA188-1.4TDI", 80, 195),
    "2.0 SDI 70": ("EA188-2.0SDI", 70, 140), "2.0 SDI 75": ("EA188-2.0SDI", 75, 140),
    "2.5 V6 TDI 150": ("V6-2.5TDI", 150, 310), "2.5 V6 TDI 163": ("V6-2.5TDI", 163, 350),
    "2.5 TDI 88": ("R5-2.5TDI", 88, 220), "2.5 TDI 109": ("R5-2.5TDI", 109, 280), "2.5 TDI 130": ("R5-2.5TDI", 130, 340),
    "2.5 TDI 136": ("R5-2.5TDI", 136, 330), "2.5 TDI 163": ("R5-2.5TDI", 163, 350), "2.5 TDI 174": ("R5-2.5TDI", 174, 400),
    # --- 1.2/1.4/1.6 TDI : EA189 (par défaut) / EA288 (@M)
    "1.2 TDI 75": ("EA189-1.2TDI", 75, 180),
    "1.6 TDI 75": ("EA189-1.6TDI", 75, 195), "1.6 TDI 90": ("EA189-1.6TDI", 90, 230),
    "1.6 TDI 102": ("EA189-1.6TDI", 102, 250), "1.6 TDI 105": ("EA189-1.6TDI", 105, 250),
    "1.6 TDI 90@M": ("EA288-1.6TDI", 90, 230), "1.6 TDI 105@M": ("EA288-1.6TDI", 105, 250),
    "1.6 TDI 80": ("EA288-1.6TDI", 80, 230), "1.6 TDI 95": ("EA288-1.6TDI", 95, 250),
    "1.6 TDI 110": ("EA288-1.6TDI", 110, 250), "1.6 TDI 115": ("EA288-1.6TDI", 115, 250),
    "1.6 TDI 120": ("EA288-1.6TDI", 120, 250),
    "1.4 TDI 75@M": ("EA288-1.4TDI", 75, 210), "1.4 TDI 90": ("EA288-1.4TDI", 90, 230),
    "1.4 TDI 105": ("EA288-1.4TDI", 105, 250),
    # --- 2.0 TDI : EA188 PD (@A), EA189 (@B / défaut), EA288 (@M), EA288 evo (@N)
    "2.0 TDI 136@A": ("EA188-2.0TDI", 136, 320), "2.0 TDI 140@A": ("EA188-2.0TDI", 140, 320),
    "2.0 TDI 170@A": ("EA188-2.0TDI", 170, 350),
    "2.0 TDI 84": ("EA189-2.0TDI", 84, 220), "2.0 TDI 102": ("EA189-2.0TDI", 102, 250),
    "2.0 TDI 109": ("EA189-2.0TDI", 109, 250), "2.0 TDI 110": ("EA189-2.0TDI", 110, 250),
    "2.0 TDI 114": ("EA189-2.0TDI", 114, 250), "2.0 TDI 122": ("EA189-2.0TDI", 122, 340),
    "2.0 TDI 136": ("EA189-2.0TDI", 136, 340), "2.0 TDI 140": ("EA189-2.0TDI", 140, 320),
    "2.0 TDI 163": ("EA189-2.0TDI", 163, 400), "2.0 TDI 170": ("EA189-2.0TDI", 170, 350),
    "2.0 TDI 177": ("EA189-2.0TDI", 177, 380), "2.0 TDI 180": ("EA189-2.0TDI", 180, 400),
    "2.0 TDI 75": ("EA288-2.0TDI", 75, 225), "2.0 TDI 84@M": ("EA288-2.0TDI", 84, 220),
    "2.0 TDI 102@M": ("EA288-2.0TDI", 102, 250), "2.0 TDI 114@M": ("EA288-2.0TDI", 114, 250),
    "2.0 TDI 115": ("EA288-2.0TDI", 115, 300), "2.0 TDI 122@M": ("EA288-2.0TDI", 122, 320),
    "2.0 TDI 140@M": ("EA288-2.0TDI", 140, 340), "2.0 TDI 150": ("EA288-2.0TDI", 150, 340),
    "2.0 TDI 177@M": ("EA288-2.0TDI", 177, 410), "2.0 TDI 184": ("EA288-2.0TDI", 184, 380),
    "2.0 TDI 190": ("EA288-2.0TDI", 190, 400), "2.0 TDI 204": ("EA288-2.0BiTDI", 204, 450),
    "2.0 TDI 240": ("EA288-2.0BiTDI", 240, 500),
    "2.0 TDI 90": ("EA288evo-2.0TDI", 90, 220), "2.0 TDI 110@N": ("EA288evo-2.0TDI", 110, 250),
    "2.0 TDI 116": ("EA288evo-2.0TDI", 116, 300), "2.0 TDI 122@N": ("EA288evo-2.0TDI", 122, 320),
    "2.0 TDI 150@N": ("EA288evo-2.0TDI", 150, 360), "2.0 TDI 193": ("EA288evo-2.0TDI", 193, 400),
    "2.0 TDI 199": ("EA288evo-2.0TDI", 199, 450), "2.0 TDI 200": ("EA288evo-2.0TDI", 200, 400),
    "2.0 TDI 102@N": ("EA288evo-2.0TDI", 102, 280), "2.0 TDI 75@N": ("EA288evo-2.0TDI", 75, 250),
    "2.0 TDI 170@F": ("Ford", "EcoBlue-2.0", 170, 405), "2.0 TDI 205@F": ("Ford", "EcoBlue-2.0", 205, 500),
    # --- V6 / V8 / V10 TDI
    "3.0 TDI 204": ("V6-3.0TDI", 204, 450), "3.0 TDI 224": ("V6-3.0TDI", 224, 500),
    "3.0 TDI 225": ("V6-3.0TDI", 225, 500), "3.0 TDI 231": ("V6-3.0TDI", 231, 500),
    "3.0 TDI 240": ("V6-3.0TDI", 240, 550), "3.0 TDI 262": ("V6-3.0TDI", 262, 580),
    "3.0 TDI 286": ("V6-3.0TDI", 286, 600),
    "3.0 V6 TDI 163": ("V6-3.0TDI", 163, 450), "3.0 V6 TDI 204": ("V6-3.0TDI", 204, 450),
    "3.0 V6 TDI 224": ("V6-3.0TDI", 224, 500), "3.0 V6 TDI 258": ("V6-3.0TDI", 258, 580),
    "3.0 V6 TDI 240@F": ("Ford", "Lion-3.0V6", 240, 600),
    "4.0 TDI 421": ("V8-4.0TDI", 421, 900), "4.2 TDI 340": ("V8-4.2TDI", 340, 800),
    "5.0 V10 TDI 313": ("V10-5.0TDI", 313, 750), "5.0 V10 TDI 350": ("V10-5.0TDI", 350, 850),
    # --- électrique
    "e-up! 82": ("EUP-EV", 82, 210), "e-up! 83": ("EUP-EV", 83, 212),
    "e-Golf 115": ("EGOLF-EV", 115, 270), "e-Golf 136": ("EGOLF-EV", 136, 290),
    "Pure 148": ("MEB-EV", 148, 220), "Pure 150": ("MEB-EV", 150, 310), "Pure 170": ("MEB-EV", 170, 310),
    "Pro 145": ("MEB-EV", 145, 275), "Pro 174": ("MEB-EV", 174, 310), "Pro 204": ("MEB-EV", 204, 310),
    "Pro S 204": ("MEB-EV", 204, 310), "Pro S 231": ("MEB-EV", 231, 545), "Pro 286": ("MEB-EV", 286, 545),
    "Pro S 286": ("MEB-EV", 286, 545), "GTX 286": ("MEB-EV", 286, 545),
    "GTX 299": ("MEB-AWD", 299, 460), "GTX 326": ("MEB-AWD", 326, 545), "GTX 340": ("MEB-AWD", 340, 679),
    "ABT e-Transporter 112": ("ABT-EV", 112, 200), "e-Crafter 136": ("ECRAFTER-EV", 136, 290),
}

ERES = {
    # A : injecteurs-pompes (PD) ; B : EA189 / EA111 ; M : EA211 / EA288 ; N : EA288 evo ; F : moteurs Ford
    "Mk5": "A", "B6": "A", ("1T", "1"): "A", ("1T", "2"): "A", ("2K", "1"): "A", ("T5", "1"): "A", "B5": "A",
    "Mk6": "B", "6R": "B", "B7": "B", "5N": "B", "7N": "B", "5C": "B", "16": "B", "1F": "B", "2H": "B",
    ("1T", "3"): "B", ("2K", "2"): "B", ("T5", "2"): "B", ("13", "1"): "B", ("2E", "2"): "B",
    "Mk7": "M", "6C": "M", "AW": "M", "AD1": "M", "B8": "M", "5T": "M", "3H": "M", "A1": "M", "C1": "M",
    "CS": "M", "SA": "M", ("T6", "1"): "M", "SY": "M", ("Mk8", "1"): "M", "CR": "M", "ST7": "M",
    ("13", "2"): "M", ("7N", "2"): "M",
    ("Mk8", "2"): "N", "CT1": "N", "CT2": "N", "B9": "N", "SB": "N", ("T6", "2"): "N", "A2": "N",
    "AMK2": "F",
}

MOT = Motorisations("Volkswagen", FAMILLES, TABLE, ERES)
MOT.lier(L)

DETAIL = {"Volkswagen": L}
MOTEURS = MOT.moteurs()
