"""BMW et BMW M : générations, phases (2 = LCI), motorisations (marché européen) et moteurs liés.
Familles de moteurs partagées avec Mini (N12…B48)."""
from . import mini
from ._outil import Motorisations, electrique, famille as f, gamme as g


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


L = []   # BMW
LM = []  # BMW M

# ---------------------------------------------------------------- Série 1
L += g("Série 1", "E87", "1", "2004-09", "2007-02",
       ["116i 115", "118i 129", "120i 150", ("130i 265", {"debut": "2005-09"}), "118d 122", "120d 163"],
       reservoir=51, remarques="E87 5 portes (E81 3 portes : 2007)")
L += g("Série 1", "E87", "2", "2007-03", "2011-09",
       ["116i 122", "118i 143", "120i 170", "130i 265", "116d 116", "118d 143", "120d 177", "123d 204"],
       reservoir=51, remarques="E87 5 portes, E81 3 portes")
L += g("Série 1", "E82", "1", "2007-11", "2013-10",
       ["118i 143", "120i 170", "125i 218", "135i 306", "118d 143", "120d 177", "123d 204"], portes=2, places=4,
       reservoir=53, remarques="E82 Coupé et E88 Cabriolet")
L += g("Série 1", "F20", "1", "2011-09", "2015-02",
       ["114i 102", "116i 136", "118i 170", "125i 218", ("M135i 320", {"debut": "2012-09"}), "114d 95", "116d 116",
        "118d 143", "120d 184", "125d 218"], reservoir=52, remarques="F20 5 portes, F21 3 portes")
L += g("Série 1", "F20", "2", "2015-03", "2019-06",
       ["116i 109", "118i 136", "120i 184", "125i 224", ("M140i 340", {"debut": "2016-07"}), "116d 116", "118d 150",
        "120d 190", "125d 224"], reservoir=52, remarques="F20 5 portes, F21 3 portes")
L += g("Série 1", "F40", "1", "2019-09", "2024-07",
       ["116i 109", "118i 140", ("120i 178", {"debut": "2022-03"}), ("128ti 265", {"debut": "2020-11"}), "M135i 306",
        "116d 116", "118d 150", "120d 190"], reservoir=50, remarques="Traction")
L += g("Série 1", "F70", "1", "2024-09", None,
       ["118 156", "120 170", "M135 300", "118d 150", "120d 163"], reservoir=49)

# ---------------------------------------------------------------- Série 2
L += g("Série 2", "F22", "1", "2014-01", "2017-06",
       ["218i 136", "220i 184", "228i 245", "M235i 326", "218d 143", "220d 184", "225d 218"], portes=2, places=4,
       reservoir=52, remarques="F22 Coupé et F23 Cabriolet")
L += g("Série 2", "F22", "2", "2017-07", "2021-06",
       ["218i 136", "220i 184", "230i 252", "M240i 340", "218d 150", "220d 190", "225d 224"], portes=2, places=4,
       reservoir=52, remarques="F22 Coupé et F23 Cabriolet")
L += g("Série 2", "F45", "1", "2014-10", "2018-02",
       ["216i 102", "218i 136", "220i 192", "225i 231", ("225xe 224", ph(8, 36, debut="2016-03")), "216d 116", "218d 150",
        "220d 190"], reservoir=51, remarques="Active Tourer (F45) et Gran Tourer 7 places (F46)")
L += g("Série 2", "F45", "2", "2018-03", "2021-12",
       ["216i 109", "218i 140", "220i 192", ("225xe 224", ph(10, 36)), "216d 116", "218d 150", "220d 190"], reservoir=51,
       remarques="Active Tourer (F45) et Gran Tourer 7 places (F46)")
L += g("Série 2", "F44", "1", "2020-03", None,
       ["218i 136", "218i 140", "220i 178", "M235i 306", "216d 116", "218d 150", "220d 190"], portes=4, reservoir=50,
       remarques="Gran Coupé")
L += g("Série 2", "G42", "1", "2021-10", None, ["220i 184", "230i 245", "M240i 374", "220d 190"], portes=2,
       places=4, reservoir=52, remarques="Coupé")
L += g("Série 2", "U06", "1", "2022-02", None,
       ["218i 136", "220 170", "223 218", ("225e 245", ph(14, 39)), ("230e 326", ph(14, 39)), ("216d 122", {"debut": "2023-03"}),
        "218d 150"], reservoir=45, remarques="Active Tourer")

# ---------------------------------------------------------------- Série 3
L += g("Série 3", "E21", "1", "1975-06", "1983-08",
       ["315 75", "316 90", "318 98", "318i 105", "320 109", "320/6 122", "320i 125", "323i 143"], portes=2,
       reservoir=52, remarques="Berline 2 portes ; Baur TC")
L += g("Série 3", "E30", "1", "1982-11", "1987-08",
       ["316 90", "318i 105", "320i 125", "320i 129", "323i 139", "323i 150", ("325i 171", {"debut": "1985-09"}),
        ("325e 122", {"debut": "1983-09"}), ("324d 86", {"debut": "1985-09"})], portes=4, reservoir=55,
       remarques="Berline 2 et 4 portes, Cabriolet (1985), Touring (1987)")
L += g("Série 3", "E30", "2", "1987-09", "1994-06",
       ["316i 100", "318i 113", ("318is 136", {"debut": "1989-09"}), "320i 129", "325i 170", "324td 115"], portes=4,
       reservoir=64, remarques="Berline 2 et 4 portes, Cabriolet, Touring ; 325iX")
L += g("Série 3", "E36", "1", "1990-11", "1995-08",
       ["316i 100", "318i 113", "318is 140", "320i 150", "325i 192", ("318tds 90", {"debut": "1994-09"}),
        ("325td 115", {"debut": "1991-09"}), ("325tds 143", {"debut": "1993-09"})], portes=4, reservoir=65,
       remarques="Berline, Coupé, Cabriolet, Touring, Compact")
L += g("Série 3", "E36", "2", "1995-09", "2000-08",
       ["316i 102", "318i 115", "318is 140", "320i 150", "323i 170", "328i 193", "318tds 90", "325tds 143"],
       portes=4, reservoir=65, remarques="Berline, Coupé, Cabriolet, Touring, Compact (316i, 318ti)")
L += g("Série 3", "E46", "1", "1998-05", "2001-08",
       ["316i 105", "318i 118", "320i 150", "323i 170", "328i 193", "320d 136", ("330d 184", {"debut": "1999-09"})],
       portes=4, reservoir=63, remarques="Berline, Touring, Coupé, Cabriolet, Compact")
L += g("Série 3", "E46", "2", "2001-09", "2006-12",
       ["316i 115", "318i 143", "320i 170", "325i 192", "330i 231", "318d 116", "320d 150", "330d 204"],
       portes=4, reservoir=63, remarques="Berline, Touring ; Coupé et Cabriolet jusqu'en 2006")
L += g("Série 3", "E90", "1", "2005-03", "2008-08",
       ["318i 129", "318i 143", "320i 150", "325i 218", "330i 258", ("335i 306", {"debut": "2006-09"}), "318d 122",
        ("318d 143", {"debut": "2007-03"}), "320d 163", ("320d 177", {"debut": "2007-03"}), "325d 197", "330d 231",
        ("335d 286", {"debut": "2006-09"})], portes=4, reservoir=60,
       remarques="Berline E90, Touring E91, Coupé E92, Cabriolet E93")
L += g("Série 3", "E90", "2", "2008-09", "2012-02",
       ["316i 122", "318i 143", "320i 170", "325i 218", "330i 272", "335i 306", "316d 116", "318d 143", "320d 184",
        "325d 204", "330d 245", "335d 286"], portes=4, reservoir=60,
       remarques="Berline E90, Touring E91 ; Coupé E92 et Cabriolet E93 jusqu'en 2013")
L += g("Série 3", "F30", "1", "2012-02", "2015-06",
       ["316i 136", "320i 184", "328i 245", "335i 306", ("ActiveHybrid 3 340", {"debut": "2012-09"}), "316d 116",
        "318d 143", "320d 184", "325d 218", "330d 258", "335d 313"], portes=4, reservoir=60,
       remarques="Berline F30, Touring F31, Gran Turismo F34")
L += g("Série 3", "F30", "2", "2015-07", "2019-02",
       ["318i 136", "320i 184", "330i 252", "340i 326", ("330e 252", ph(8, 41)), "316d 116", "318d 150", "320d 190",
        "325d 224", "330d 258", "335d 313"], portes=4, reservoir=57,
       remarques="Berline F30, Touring F31, Gran Turismo F34")
L += g("Série 3", "G20", "1", "2019-03", "2022-06",
       ["318i 156", "320i 184", "330i 258", "M340i 374", ("330e 292", ph(12, 40)), "316d 122", "318d 150", "320d 190",
        "330d 265", "330d 286", "M340d 340"], portes=4, reservoir=59, remarques="Berline G20, Touring G21")
L += g("Série 3", "G20", "2", "2022-07", None,
       ["318i 156", "320i 184", "330i 245", "M340i 374", ("320e 204", ph(12, 40)), ("330e 292", ph(12, 40)), "318d 150",
        "320d 190", "M340d 340"], portes=4, reservoir=59, remarques="Berline G20, Touring G21")

# ---------------------------------------------------------------- Série 4
L += g("Série 4", "F32", "1", "2013-10", "2017-02",
       ["420i 184", "428i 245", "435i 306", "418d 143", "420d 184", "425d 218", "430d 258", "435d 313"], portes=2,
       places=4, reservoir=60, remarques="Coupé F32, Cabriolet F33, Gran Coupé F36")
L += g("Série 4", "F32", "2", "2017-03", "2020-09",
       ["420i 184", "430i 252", "440i 326", "418d 150", "420d 190", "425d 224", "430d 258", "435d 313"], portes=2,
       places=4, reservoir=57, remarques="Coupé F32, Cabriolet F33, Gran Coupé F36")
L += g("Série 4", "G22", "1", "2020-10", None,
       ["420i 184", "430i 258", "430i 245", "M440i 374", "420d 190", "430d 286", "M440d 340"], portes=2, places=4,
       reservoir=59, remarques="Coupé G22, Cabriolet G23, Gran Coupé G26 ; restylage 2024 non détaillé")

# ---------------------------------------------------------------- Série 5
L += g("Série 5", "E12", "1", "1972-09", "1981-06",
       ["518 90", "520 115", "520i 125", "520/6 122", "525 145", "528i 177"], portes=4, reservoir=70)
L += g("Série 5", "E28", "1", "1981-06", "1988-01",
       ["518i 105", "520i 125", "520i 129", "525i 150", "528i 184", ("535i 218", {"debut": "1985-01"}),
        ("524td 115", {"debut": "1983-01"}), ("524d 86", {"debut": "1986-09"})], portes=4, reservoir=70)
L += g("Série 5", "E34", "1", "1988-01", "1992-08",
       ["518i 113", "520i 129", "525i 170", "530i 188", "535i 211", "524td 115"], portes=4, reservoir=80,
       remarques="Berline et Touring (1991)")
L += g("Série 5", "E34", "2", "1992-09", "1996-06",
       ["518i 115", "520i 150", "525i 192", "530i 218", "540i 286", "525td 115", "525tds 143"], portes=4,
       reservoir=80, remarques="Berline et Touring")
L += g("Série 5", "E39", "1", "1995-12", "2000-08",
       ["520i 150", "523i 170", "528i 193", "535i 235", "540i 286", ("520d 136", {"debut": "1998-09"}), "525tds 143",
        ("530d 184", {"debut": "1998-09"})], portes=4, reservoir=70, remarques="Berline et Touring (1997)")
L += g("Série 5", "E39", "2", "2000-09", "2004-05",
       ["520i 170", "525i 192", "530i 231", "535i 245", "540i 286", "520d 136", "525d 163", "530d 193"], portes=4,
       reservoir=70, remarques="Berline et Touring")
L += g("Série 5", "E60", "1", "2003-07", "2007-02",
       ["520i 170", ("523i 177", {"debut": "2005-09"}), "525i 192", ("525i 218", {"debut": "2005-09"}), "530i 231",
        ("530i 258", {"debut": "2005-09"}), "545i 333", ("550i 367", {"debut": "2005-09"}), "520d 163", "525d 177",
        "530d 218", ("530d 231", {"debut": "2005-09"}), ("535d 272", {"debut": "2004-09"})], portes=4, reservoir=70,
       remarques="Berline E60, Touring E61")
L += g("Série 5", "E60", "2", "2007-03", "2010-02",
       ["520i 170", "523i 190", "525i 218", "530i 272", "540i 306", "550i 367", "520d 177", "525d 197", "530d 235",
        "535d 286"], portes=4, reservoir=70, remarques="Berline E60, Touring E61")
L += g("Série 5", "F10", "1", "2010-03", "2013-06",
       [("520i 184", {"debut": "2011-09"}), "523i 204", "528i 258", ("528i 245", {"debut": "2011-09"}), "535i 306",
        "550i 407", ("ActiveHybrid 5 340", {"debut": "2012-03"}), ("518d 143", {"debut": "2012-03"}), "520d 184",
        "525d 204", "530d 245", "530d 258", "535d 300", "535d 313", ("M550d 381", {"debut": "2012-03"})], portes=4,
       reservoir=70, remarques="Berline F10, Touring F11, Gran Turismo F07")
L += g("Série 5", "F10", "2", "2013-07", "2017-01",
       ["520i 184", "528i 245", "535i 306", "550i 449", "518d 150", "520d 190", "525d 218", "530d 258", "535d 313",
        "M550d 381"], portes=4, reservoir=70, remarques="Berline F10, Touring F11, Gran Turismo F07")
L += g("Série 5", "G30", "1", "2017-02", "2020-06",
       ["520i 184", "530i 252", "540i 340", "M550i 462", ("530e 252", ph(9, 46)), "518d 150", "520d 190", "525d 231",
        "530d 265", "540d 320", "M550d 400"], portes=4, reservoir=68, remarques="Berline G30, Touring G31")
L += g("Série 5", "G30", "2", "2020-07", "2023-09",
       ["520i 184", "530i 252", "540i 333", "M550i 530", ("530e 292", ph(12, 40)), ("545e 394", ph(12, 46)), "518d 150",
        "520d 190", "530d 286", "540d 340"], portes=4, reservoir=68, remarques="Berline G30, Touring G31")
L += g("Série 5", "G60", "1", "2023-10", None,
       ["520i 208", "520d 197", ("530e 299", ph(19, 46)), ("550e 489", ph(19, 46, debut="2024-03"))], portes=4,
       reservoir=60, remarques="Berline G60, Touring G61 (2024)")

# ---------------------------------------------------------------- Série 6 / 7 / 8
L += g("Série 6", "E24", "1", "1976-03", "1989-04",
       ["630CS 185", "633CSi 197", ("628CSi 184", {"debut": "1979-01"}), ("635CSi 218", {"debut": "1978-07"}),
        ("M635CSi 286", {"debut": "1984-02"})], portes=2, places=4, reservoir=70, remarques="Coupé")
L += g("Série 6", "E63", "1", "2003-12", "2010-07",
       ["645Ci 333", ("630i 258", {"debut": "2004-09", "fin": "2007-08"}), ("630i 272", {"debut": "2007-09"}),
        ("650i 367", {"debut": "2005-09"}), ("635d 286", {"debut": "2007-09"})], portes=2, places=4, reservoir=70,
       remarques="Coupé E63 et Cabriolet E64 ; restylage 2007 non détaillé")
L += g("Série 6", "F12", "1", "2011-03", "2018-02",
       ["640i 320", "650i 407", ("650i 449", {"debut": "2012-09"}), "640d 313"], portes=2, places=4, reservoir=70,
       remarques="Cabriolet F12, Coupé F13, Gran Coupé F06 ; restylage 2015 non détaillé")
L += g("Série 6", "G32", "1", "2017-10", "2023-12",
       ["630i 258", "640i 340", "620d 190", "630d 265", "630d 286"], reservoir=68, remarques="Gran Turismo")
L += g("Série 7", "E23", "1", "1977-05", "1986-06",
       ["728i 184", "732i 197", "735i 218", ("745i 252", {"debut": "1980-01"})], portes=4, reservoir=85)
L += g("Série 7", "E32", "1", "1986-06", "1994-03",
       ["730i 188", "735i 211", ("750i 300", {"debut": "1987-06"}), ("730i 218", {"debut": "1992-04"}),
        ("740i 286", {"debut": "1992-04"})], portes=4, reservoir=90)
L += g("Série 7", "E38", "1", "1994-06", "2001-09",
       ["728i 193", "735i 238", "740i 286", "750i 326", ("725tds 143", {"debut": "1996-01"}), ("730d 184", {"debut": "1998-09"}),
        ("730d 193", {"debut": "2000-01"}), ("740d 245", {"debut": "1999-01"})], portes=4, reservoir=85,
       remarques="Restylage 1998 non détaillé")
L += g("Série 7", "E65", "1", "2001-11", "2005-02",
       ["735i 272", "745i 333", ("760i 445", {"debut": "2003-01"}), ("730i 231", {"debut": "2002-09"}),
        ("730d 218", {"debut": "2002-09"}), ("740d 258", {"debut": "2002-09"})], portes=4, reservoir=88,
       remarques="E65 et version longue E66")
L += g("Série 7", "E65", "2", "2005-03", "2008-10",
       ["730i 258", "740i 306", "750i 367", "760i 445", "730d 231", "745d 300"], portes=4, reservoir=88,
       remarques="E65 et version longue E66")
L += g("Série 7", "F01", "1", "2008-11", "2012-06",
       ["730i 258", "740i 326", "750i 407", ("760i 544", {"debut": "2009-09"}), ("ActiveHybrid 7 465", {"debut": "2010-03"}),
        "730d 245", "740d 306"], portes=4, reservoir=80, remarques="F01 et version longue F02")
L += g("Série 7", "F01", "2", "2012-07", "2015-06",
       ["740i 326", "750i 449", "760i 544", "730d 258", "740d 313", "750d 381"], portes=4, reservoir=80,
       remarques="F01 et version longue F02")
L += g("Série 7", "G11", "1", "2015-10", "2019-03",
       ["730i 258", "740i 326", "750i 450", ("M760i 610", {"debut": "2016-09"}), ("740e 326", ph(9, 46, debut="2016-06")),
        "725d 231", "730d 265", "740d 320", "750d 400"], portes=4, reservoir=78, remarques="G11 et version longue G12")
L += g("Série 7", "G11", "2", "2019-04", "2022-06",
       ["730i 258", "740i 333", "750i 530", "M760i 585", ("745e 394", ph(12, 46)), "730d 286", "740d 340", "750d 400"],
       portes=4, reservoir=78, remarques="G11 et version longue G12")
L += g("Série 7", "G70", "1", "2022-07", None,
       [("740i 380", {"fin": "2023-12"}), "740d 300", ("750e 489", ph(19, 69)), ("M760e 571", ph(19, 69)),
        ("760i 544", {"debut": "2022-07", "remarques": "Hors Europe / sur demande"})], portes=4, reservoir=74,
       remarques="Version longue uniquement")
L += g("Série 8", "E31", "1", "1989-09", "1999-05",
       ["850i 300", ("850Ci 326", {"debut": "1994-01"}), ("840Ci 286", {"debut": "1993-01"}), ("850CSi 380", {"debut": "1992-01", "fin": "1996-12"})],
       portes=2, places=4, reservoir=90, remarques="Coupé")
L += g("Série 8", "G15", "1", "2018-11", "2025-12",
       ["840i 340", "840i 333", "M850i 530", "M850i 523", "840d 320", "840d 340"], portes=2, places=4, reservoir=68,
       remarques="Coupé G15, Cabriolet G14, Gran Coupé G16 ; restylage 2022 non détaillé")

# ---------------------------------------------------------------- X1 / X2
L += g("X1", "E84", "1", "2009-10", "2012-06",
       ["sDrive18i 150", "xDrive28i 258", "sDrive16d 116", "sDrive18d 143", "xDrive20d 177", "xDrive23d 204"],
       reservoir=61)
L += g("X1", "E84", "2", "2012-07", "2015-06",
       ["sDrive18i 150", "sDrive20i 184", "xDrive28i 245", "sDrive16d 116", "sDrive18d 143", "xDrive20d 184",
        "xDrive25d 218"], reservoir=63)
L += g("X1", "F48", "1", "2015-10", "2019-06",
       ["sDrive18i 136", "sDrive20i 192", "xDrive25i 231", "sDrive16d 116", "sDrive18d 150", "xDrive20d 190",
        "xDrive25d 231"], reservoir=51)
L += g("X1", "F48", "2", "2019-07", "2022-09",
       ["sDrive18i 140", "sDrive20i 178", ("xDrive25e 220", ph(10, 36)), "sDrive16d 116", "sDrive18d 150",
        "xDrive20d 190", "xDrive25d 231"], reservoir=51)
L += g("X1", "U11", "1", "2022-10", None,
       ["sDrive18i 136", "sDrive20i 170", "xDrive23i 218", ("xDrive25e 245", ph(14, 45)), ("xDrive30e 326", ph(14, 45)),
        "sDrive18d 150", "xDrive20d 163", "xDrive23d 211", ("iX1 eDrive20 204", el(65, debut="2023-09")),
        ("iX1 xDrive30 313", el(65))], reservoir=54, remarques="X1 thermique, hybride et iX1 électrique")
L += g("X2", "F39", "1", "2018-03", "2023-09",
       ["sDrive18i 136", "sDrive18i 140", "sDrive20i 192", "sDrive20i 178", ("M35i 306", {"debut": "2018-11"}),
        ("xDrive25e 220", ph(10, 36, debut="2020-06")), "sDrive18d 150", "xDrive20d 190", "xDrive25d 231"],
       reservoir=51, remarques="SUV coupé")
L += g("X2", "U10", "1", "2024-03", None,
       ["sDrive20i 170", "M35i 300", "sDrive18d 150", ("iX2 eDrive20 204", el(65, debut="2024-09")), ("iX2 xDrive30 313", el(65))],
       reservoir=54, remarques="SUV coupé thermique et iX2 électrique")

# ---------------------------------------------------------------- X3 / X4
L += g("X3", "E83", "1", "2003-12", "2006-08",
       ["2.0i 150", "2.5i 192", "3.0i 231", ("2.0d 150", {"debut": "2004-09"}), "3.0d 204"], reservoir=67)
L += g("X3", "E83", "2", "2006-09", "2010-08",
       ["2.0i 150", "2.5si 218", "3.0si 272", "2.0d 150", ("2.0d 177", {"debut": "2007-09"}), "3.0d 218", "3.0sd 286"],
       reservoir=67, remarques="xDrive à partir de 2008")
L += g("X3", "F25", "1", "2010-11", "2014-03",
       [("xDrive20i 184", {"debut": "2011-09"}), "xDrive28i 258", ("xDrive28i 245", {"debut": "2011-09"}), "xDrive35i 306",
        ("sDrive18d 143", {"debut": "2011-09"}), "xDrive20d 184", "xDrive30d 258", ("xDrive35d 313", {"debut": "2011-09"})],
       reservoir=67)
L += g("X3", "F25", "2", "2014-04", "2017-10",
       ["xDrive20i 184", "xDrive28i 245", "xDrive35i 306", "sDrive18d 150", "xDrive20d 190", "xDrive30d 258",
        "xDrive35d 313"], reservoir=67)
L += g("X3", "G01", "1", "2017-11", "2021-06",
       ["xDrive20i 184", "xDrive30i 252", "M40i 360", ("xDrive30e 292", ph(12, 50, debut="2019-12")), "sDrive18d 150",
        "xDrive20d 190", "xDrive30d 265", "M40d 326"], reservoir=65, remarques="X3 et iX3 électrique (modèle à part)")
L += g("X3", "G01", "2", "2021-07", "2024-09",
       ["xDrive20i 184", "xDrive30i 245", "M40i 354", ("xDrive30e 292", ph(12, 50)), "sDrive18d 150", "xDrive20d 190",
        "xDrive30d 286", "M40d 340"], reservoir=65)
L += g("X3", "G45", "1", "2024-10", None,
       ["20 xDrive 208", ("30e xDrive 299", ph(20, 57)), "M50 xDrive 398", "20d xDrive 197"], reservoir=65)
L += g("X4", "F26", "1", "2014-04", "2018-02",
       ["xDrive20i 184", "xDrive28i 245", "xDrive35i 306", ("M40i 360", {"debut": "2016-03"}), "xDrive20d 190",
        "xDrive30d 258", "xDrive35d 313"], reservoir=67, remarques="SUV coupé")
L += g("X4", "G02", "1", "2018-03", "2021-06",
       ["xDrive20i 184", "xDrive30i 252", "M40i 360", "xDrive20d 190", "xDrive30d 265", "M40d 326"], reservoir=65,
       remarques="SUV coupé")
L += g("X4", "G02", "2", "2021-07", "2025-10",
       ["xDrive20i 184", "xDrive30i 245", "M40i 354", "xDrive20d 190", "xDrive30d 286", "M40d 340"], reservoir=65,
       remarques="SUV coupé")

# ---------------------------------------------------------------- X5 / X6 / X7 / XM
L += g("X5", "E53", "1", "1999-11", "2003-09",
       ["3.0i 231", "4.4i 286", ("4.6is 347", {"debut": "2001-09"}), ("3.0d 184", {"debut": "2001-01"})], reservoir=93)
L += g("X5", "E53", "2", "2003-10", "2006-10",
       ["3.0i 231", "4.4i 320", "4.8is 360", "3.0d 218"], reservoir=93)
L += g("X5", "E70", "1", "2007-03", "2010-03",
       ["3.0si 272", "4.8i 355", "3.0d 235", "3.0sd 286"], places=5, reservoir=85, remarques="5 ou 7 places")
L += g("X5", "E70", "2", "2010-04", "2013-10",
       ["xDrive35i 306", "xDrive50i 407", "xDrive30d 245", "xDrive30d 258", "xDrive40d 306", "xDrive40d 313",
        ("M50d 381", {"debut": "2012-03"})], places=5, reservoir=85, remarques="5 ou 7 places")
L += g("X5", "F15", "1", "2013-11", "2018-10",
       ["xDrive35i 306", "xDrive50i 450", ("xDrive40e 313", ph(9, 85, debut="2015-09")), "sDrive25d 218", "sDrive25d 231",
        "xDrive30d 258", "xDrive40d 313", "M50d 381"], places=5, reservoir=85, remarques="5 ou 7 places")
L += g("X5", "G05", "1", "2018-11", "2023-03",
       ["xDrive40i 340", "xDrive40i 333", "M50i 530", ("xDrive45e 394", ph(24, 69, debut="2019-09")), "xDrive25d 231",
        "xDrive30d 265", "xDrive30d 286", "M50d 400"], places=5, reservoir=83, remarques="5 ou 7 places")
L += g("X5", "G05", "2", "2023-04", None,
       ["xDrive40i 381", ("xDrive50e 489", ph(26, 69)), "M60i 530", "xDrive30d 298", "xDrive40d 352"], places=5,
       reservoir=83, remarques="5 ou 7 places")
L += g("X6", "E71", "1", "2008-05", "2014-06",
       ["xDrive35i 306", "xDrive50i 407", ("ActiveHybrid X6 485", {"debut": "2009-12", "fin": "2011-12"}), "xDrive30d 235",
        ("xDrive30d 245", {"debut": "2010-04"}), "xDrive35d 286", ("xDrive40d 306", {"debut": "2010-04"}),
        ("M50d 381", {"debut": "2012-03"})], places=5, reservoir=85, remarques="SUV coupé ; restylage 2012 non détaillé")
L += g("X6", "F16", "1", "2014-12", "2019-10",
       ["xDrive35i 306", "xDrive50i 450", "xDrive30d 258", "xDrive40d 313", "M50d 381"], places=5, reservoir=85,
       remarques="SUV coupé")
L += g("X6", "G06", "1", "2019-11", "2023-03",
       ["xDrive40i 340", "xDrive40i 333", "M50i 530", "xDrive30d 286", "xDrive40d 340", "M50d 400"], places=5,
       reservoir=83, remarques="SUV coupé")
L += g("X6", "G06", "2", "2023-04", None,
       ["xDrive40i 381", "M60i 530", "xDrive30d 298", "xDrive40d 352"], places=5, reservoir=83, remarques="SUV coupé")
L += g("X7", "G07", "1", "2019-03", "2022-10",
       ["xDrive40i 340", "xDrive40i 333", "M50i 530", "xDrive30d 265", "xDrive30d 286", "xDrive40d 340", "M50d 400"],
       places=7, reservoir=83, remarques="SUV 6 ou 7 places")
L += g("X7", "G07", "2", "2022-11", None,
       ["xDrive40i 381", "M60i 530", "xDrive40d 352"], places=7, reservoir=83, remarques="SUV 6 ou 7 places")

# ---------------------------------------------------------------- Z / roadsters
L += g("Z1", "E30/Z", "1", "1989-03", "1991-06", ["Z1 170"], portes=2, places=2, reservoir=58,
       remarques="Roadster à portes escamotables")
L += g("Z3", "E36/7", "1", "1995-10", "1999-03",
       ["1.8 115", "1.9 140", ("2.8 193", {"debut": "1996-09"}), ("M Roadster 321", {"debut": "1997-03"})], portes=2, places=2, reservoir=51,
       remarques="Roadster E36/7, Coupé E36/8 (1998)")
L += g("Z3", "E36/7", "2", "1999-04", "2002-12",
       ["1.9 118", "2.0 150", ("2.2i 170", {"debut": "2000-09"}), "2.8 193", ("3.0i 231", {"debut": "2000-09"}),
        ("M Roadster 325", {"debut": "2001-01"})],
       portes=2, places=2, reservoir=51, remarques="Roadster et Coupé")
L += g("Z4", "E85", "1", "2002-10", "2006-02", ["2.2i 170", "2.5i 192", "3.0i 231", ("2.0i 150", {"debut": "2005-01"})],
       portes=2, places=2, reservoir=55, remarques="Roadster E85, Coupé E86 (2006)")
L += g("Z4", "E85", "2", "2006-03", "2008-12", ["2.0i 150", "2.5i 177", "2.5si 218", "3.0si 265", "Z4 M 343"], portes=2, places=2,
       reservoir=55, remarques="Roadster E85, Coupé E86")
L += g("Z4", "E89", "1", "2009-04", "2013-02",
       ["sDrive23i 204", "sDrive30i 258", "sDrive35i 306", ("sDrive35is 340", {"debut": "2010-04"}),
        ("sDrive18i 156", {"debut": "2011-09"}), ("sDrive20i 184", {"debut": "2011-09"}), ("sDrive28i 245", {"debut": "2011-09"})],
       portes=2, places=2, reservoir=55, remarques="Roadster à toit rigide escamotable")
L += g("Z4", "E89", "2", "2013-03", "2016-08",
       ["sDrive18i 156", "sDrive20i 184", "sDrive28i 245", "sDrive35i 306", "sDrive35is 340"], portes=2, places=2,
       reservoir=55, remarques="Roadster à toit rigide escamotable")
L += g("Z4", "G29", "1", "2018-11", "2026-03", ["sDrive20i 197", "sDrive30i 258", "M40i 340"], portes=2, places=2,
       reservoir=52, remarques="Roadster ; restylage 2022 non détaillé")
L += g("Z8", "E52", "1", "2000-01", "2003-06", ["Z8 400"], portes=2, places=2, reservoir=73, remarques="Roadster")

# ---------------------------------------------------------------- i (électriques et i8)
L += g("i3", "I01", "1", "2013-11", "2017-08",
       [("i3 170", el(22, fin="2016-06")), ("i3 170 94Ah", el(33, debut="2016-07")),
        ("i3 REx 170", {"reservoir": 9, "batterie": 22, "remarques": "Prolongateur d'autonomie 2 cylindres 647 cm³"})],
       places=4, reservoir=0, remarques="Citadine électrique")
L += g("i3", "I01", "2", "2017-09", "2022-06",
       [("i3 170 94Ah", el(33, fin="2018-10")), ("i3 170 120Ah", el(42, debut="2018-11")), ("i3s 184", el(42)),
        ("i3 REx 170", {"reservoir": 9, "batterie": 33, "fin": "2018-10"})], places=4, reservoir=0,
       remarques="Citadine électrique")
L += g("i8", "I12", "1", "2014-06", "2018-03", [("i8 362", ph(7, 42))], portes=2, places=4, remarques="Coupé hybride rechargeable")
L += g("i8", "I12", "2", "2018-04", "2020-06", [("i8 374", ph(12, 30))], portes=2, places=4,
       remarques="Coupé et Roadster hybrides rechargeables")
L += g("i4", "G26", "1", "2021-11", "2024-02",
       [("eDrive35 286", el(70, debut="2022-09")), ("eDrive40 340", el(84)), ("M50 544", el(84))], reservoir=0,
       remarques="Gran Coupé électrique")
L += g("i4", "G26", "2", "2024-03", None,
       [("eDrive35 286", el(70)), ("eDrive40 340", el(84)), ("xDrive40 401", el(84)), ("M50 601", el(84))], reservoir=0,
       remarques="Gran Coupé électrique")
L += g("i5", "G60", "1", "2023-10", None,
       [("eDrive40 340", el(84)), ("xDrive40 394", el(84, debut="2024-03")), ("M60 601", el(84))], portes=4, reservoir=0,
       remarques="Berline et Touring électriques")
L += g("i7", "G70", "1", "2022-11", None,
       [("xDrive60 544", el(102)), ("eDrive50 455", el(102, debut="2023-06")), ("M70 660", el(102, debut="2023-06"))],
       portes=4, reservoir=0, remarques="Grande berline électrique")
L += g("iX", "I20", "1", "2021-11", "2025-02",
       [("xDrive40 326", el(77)), ("xDrive50 523", el(112)), ("M60 619", el(112, debut="2022-06"))], reservoir=0,
       remarques="SUV électrique")
L += g("iX", "I20", "2", "2025-03", None,
       [("xDrive45 408", el(95)), ("xDrive60 544", el(109)), ("M70 659", el(109))], reservoir=0, remarques="SUV électrique")
L += g("iX3", "G08", "1", "2021-08", "2025-06", [("iX3 286", el(80))], reservoir=0, remarques="SUV électrique (base X3 G01)")
L += g("iX3", "NA5", "1", "2025-10", None, [("50 xDrive 469", el(109))], reservoir=0,
       remarques="SUV électrique Neue Klasse ; autres versions annoncées")

# ---------------------------------------------------------------- BMW M
LM += g("M1", "E26", "1", "1978-10", "1981-07", ["M1 277"], portes=2, places=2, reservoir=116)
LM += g("1M", "E82", "1", "2011-03", "2012-06", ["1M 340"], portes=2, places=4, reservoir=53, remarques="Coupé")
LM += g("M2", "F87", "1", "2016-01", "2018-06", ["M2 370"], portes=2, places=4, reservoir=52, remarques="Coupé")
LM += g("M2", "F87", "2", "2018-07", "2021-06", ["M2 Competition 410", ("M2 CS 450", {"debut": "2020-03"})], portes=2,
        places=4, reservoir=52, remarques="Coupé")
LM += g("M2", "G87", "1", "2023-04", None, [("M2 460", {"fin": "2024-08"}), ("M2 480", {"debut": "2024-09"}),
        ("M2 CS 530", {"debut": "2025-06"})], portes=2, places=4, reservoir=52, remarques="Coupé")
LM += g("M3", "E30", "1", "1986-09", "1991-12",
        ["M3 2.3 195", "M3 2.3 200", ("M3 Evo 2.3 220", {"debut": "1988-01"}), ("M3 Sport Evo 2.5 238", {"debut": "1990-01"})],
        portes=2, places=4, reservoir=70, remarques="Coupé et Cabriolet")
LM += g("M3", "E36", "1", "1992-11", "1999-12", ["M3 3.0 286", ("M3 3.2 321", {"debut": "1995-09"})], portes=2, places=4,
        reservoir=65, remarques="Coupé, Cabriolet, Berline")
LM += g("M3", "E46", "1", "2000-06", "2006-08", ["M3 343", ("M3 CSL 360", {"debut": "2003-06", "fin": "2004-03"})],
        portes=2, places=4, reservoir=63, remarques="Coupé et Cabriolet")
LM += g("M3", "E92", "1", "2007-09", "2013-10", ["M3 420", ("M3 GTS 450", {"debut": "2010-06", "fin": "2011-06"})],
        portes=2, places=4, reservoir=63, remarques="Berline E90, Coupé E92, Cabriolet E93")
LM += g("M3", "F80", "1", "2014-03", "2018-10", ["M3 431", ("M3 Competition 450", {"debut": "2016-03"}),
        ("M3 CS 460", {"debut": "2018-01"})], portes=4, reservoir=60, remarques="Berline")
LM += g("M3", "G80", "1", "2021-03", "2024-08", ["M3 480", "M3 Competition 510", ("M3 CS 550", {"debut": "2023-03"})],
        portes=4, reservoir=59, remarques="Berline G80, Touring G81 (2022)")
LM += g("M3", "G80", "2", "2024-09", None, ["M3 Competition 530"], portes=4, reservoir=59, remarques="Berline et Touring")
LM += g("M4", "F82", "1", "2014-03", "2020-09", ["M4 431", ("M4 Competition 450", {"debut": "2016-03"}),
        ("M4 GTS 500", {"debut": "2016-01", "fin": "2016-12"}), ("M4 CS 460", {"debut": "2017-03"})], portes=2, places=4,
        reservoir=60, remarques="Coupé F82, Cabriolet F83")
LM += g("M4", "G82", "1", "2021-03", "2024-08", ["M4 480", "M4 Competition 510", ("M4 CSL 550", {"debut": "2022-07"})],
        portes=2, places=4, reservoir=59, remarques="Coupé G82, Cabriolet G83")
LM += g("M4", "G82", "2", "2024-09", None, ["M4 Competition 530", ("M4 CS 550", {"debut": "2024-09"})], portes=2,
        places=4, reservoir=59, remarques="Coupé G82, Cabriolet G83")
LM += g("M5", "E28", "1", "1985-02", "1988-01", ["M5 286"], portes=4, reservoir=70)
LM += g("M5", "E34", "1", "1988-09", "1995-12", ["M5 3.6 315", ("M5 3.8 340", {"debut": "1992-01"})], portes=4,
        reservoir=90, remarques="Berline et Touring (1992)")
LM += g("M5", "E39", "1", "1998-10", "2003-06", ["M5 400"], portes=4, reservoir=70)
LM += g("M5", "E60", "1", "2005-03", "2010-12", ["M5 507"], portes=4, reservoir=70, remarques="Berline E60, Touring E61")
LM += g("M5", "F10", "1", "2011-06", "2016-10", ["M5 560", ("M5 Competition 575", {"debut": "2013-09"}),
        ("M5 30 Jahre 600", {"debut": "2014-06", "fin": "2014-12"})], portes=4, reservoir=80)
LM += g("M5", "F90", "1", "2018-03", "2020-06", ["M5 600", "M5 Competition 625"], portes=4, reservoir=68)
LM += g("M5", "F90", "2", "2020-07", "2023-12", ["M5 Competition 625", ("M5 CS 635", {"debut": "2021-03"})], portes=4,
        reservoir=68)
LM += g("M5", "G90", "1", "2024-07", None, [("M5 727", ph(19, 60))], portes=4, reservoir=60,
        remarques="Berline G90, Touring G99 (2025) ; hybride rechargeable")
LM += g("M6", "E63", "1", "2005-04", "2010-07", ["M6 507"], portes=2, places=4, reservoir=70, remarques="Coupé et Cabriolet")
LM += g("M6", "F12", "1", "2012-06", "2018-02", ["M6 560", ("M6 Competition 575", {"debut": "2013-09"}),
        ("M6 Competition 600", {"debut": "2015-03"})], portes=2, places=4, reservoir=80,
        remarques="Cabriolet F12, Coupé F13, Gran Coupé F06")
LM += g("M8", "F92", "1", "2019-06", "2025-12", ["M8 600", "M8 Competition 625"], portes=2, places=4, reservoir=68,
        remarques="Coupé F92, Cabriolet F91, Gran Coupé F93")
LM += g("X3 M", "F97", "1", "2019-04", "2024-09", ["X3 M 480", "X3 M Competition 510"], reservoir=65)
LM += g("X4 M", "F98", "1", "2019-04", "2025-10", ["X4 M 480", "X4 M Competition 510"], reservoir=65)
LM += g("X5 M", "E70", "1", "2009-10", "2013-10", ["X5 M 555"], reservoir=85)
LM += g("X5 M", "F85", "1", "2014-12", "2018-12", ["X5 M 575"], reservoir=85)
LM += g("X5 M", "F95", "1", "2020-04", None, [("X5 M Competition 625", {"fin": "2023-03"}), ("X5 M Competition 625 mhev", {"debut": "2023-04"})],
        reservoir=83)
LM += g("X6 M", "E71", "1", "2009-10", "2014-06", ["X6 M 555"], reservoir=85)
LM += g("X6 M", "F86", "1", "2014-12", "2019-10", ["X6 M 575"], reservoir=85)
LM += g("X6 M", "F96", "1", "2020-04", None, [("X6 M Competition 625", {"fin": "2023-03"}), ("X6 M Competition 625 mhev", {"debut": "2023-04"})],
        reservoir=83)
LM += g("XM", "G09", "1", "2022-12", None, [("XM 653", ph(30, 69)), ("XM Label 748", ph(30, 69, debut="2023-09"))],
        reservoir=69, remarques="SUV hybride rechargeable")

# ---------------------------------------------------------------- Moteurs
D, E_ = "DSL", "ESS"
FAMILLES = dict(mini.FAMILLES, **{
    # anciens 4 et 6 cylindres
    "M10-1.6": f("ATM", E_, 1.6, "CHAINE", 4, 5800, 3200, "15W40", 4.0, 10000),
    "M10-1.8": f("ATM", E_, 1.8, "CHAINE", 4, 5800, 4000, "15W40", 4.0, 10000),
    "M10-2.0": f("ATM", E_, 2.0, "CHAINE", 4, 5800, 4000, "15W40", 4.25, 10000),
    "M20-2.0": f("ATM", E_, 2.0, "COURROIE", 6, 6000, 4300, "15W40", 4.3, 10000),
    "M20-2.3": f("ATM", E_, 2.3, "COURROIE", 6, 6000, 4000, "15W40", 4.3, 10000),
    "M20-2.5": f("ATM", E_, 2.5, "COURROIE", 6, 5800, 4300, "15W40", 4.3, 10000),
    "M20-2.7": f("ATM", E_, 2.7, "COURROIE", 6, 4250, 3250, "15W40", 4.3, 10000),
    "M30-2.5": f("ATM", E_, 2.5, "CHAINE", 6, 6000, 4000, "15W40", 5.75, 10000),
    "M30-2.8": f("ATM", E_, 2.8, "CHAINE", 6, 5800, 4200, "15W40", 5.75, 10000),
    "M30-3.0": f("ATM", E_, 3.0, "CHAINE", 6, 5800, 4000, "15W40", 5.75, 10000),
    "M30-3.2": f("ATM", E_, 3.2, "CHAINE", 6, 5500, 4300, "15W40", 5.75, 10000),
    "M30-3.4": f("ATM", E_, 3.4, "CHAINE", 6, 5700, 4000, "15W40", 5.75, 10000),
    "M102-3.2T": f("TURBO", E_, 3.2, "CHAINE", 6, 4900, 2200, "15W40", 5.75, 10000),
    "M40-1.6": f("ATM", E_, 1.6, "COURROIE", 4, 5500, 4250, "10W40", 4.0, 15000),
    "M40-1.8": f("ATM", E_, 1.8, "COURROIE", 4, 5500, 4250, "10W40", 4.0, 15000),
    "M42-1.8": f("ATM", E_, 1.8, "CHAINE", 4, 6000, 4600, "10W40", 5.0, 15000),
    "M43-1.6": f("ATM", E_, 1.6, "CHAINE", 4, 5500, 3900, "10W40", 4.25, 15000),
    "M43-1.8": f("ATM", E_, 1.8, "CHAINE", 4, 5500, 3900, "10W40", 4.25, 15000),
    "M43-1.9": f("ATM", E_, 1.9, "CHAINE", 4, 5500, 3900, "10W40", 4.25, 15000),
    "M44-1.9": f("ATM", E_, 1.9, "CHAINE", 4, 6000, 4300, "10W40", 5.0, 15000),
    "M50-2.0": f("ATM", E_, 2.0, "CHAINE", 6, 5900, 4700, "10W40", 6.5, 15000),
    "M50-2.5": f("ATM", E_, 2.5, "CHAINE", 6, 5900, 4700, "10W40", 6.5, 15000),
    "M52-2.0": f("ATM", E_, 2.0, "CHAINE", 6, 5900, 3500, "5W30", 6.5, 15000),
    "M52-2.5": f("ATM", E_, 2.5, "CHAINE", 6, 5500, 3950, "5W30", 6.5, 15000),
    "M52-2.8": f("ATM", E_, 2.8, "CHAINE", 6, 5300, 3950, "5W30", 6.5, 15000),
    "M54-2.2": f("ATM", E_, 2.2, "CHAINE", 6, 6100, 3500, "5W30", 6.5, 25000),
    "M54-2.5": f("ATM", E_, 2.5, "CHAINE", 6, 6000, 3500, "5W30", 6.5, 25000),
    "M54-3.0": f("ATM", E_, 3.0, "CHAINE", 6, 5900, 3500, "5W30", 6.5, 25000),
    "M60-3.0": f("ATM", E_, 3.0, "CHAINE", 8, 5800, 4500, "10W40", 7.5, 15000, a="V"),
    "M60-4.0": f("ATM", E_, 4.0, "CHAINE", 8, 5800, 4500, "10W40", 7.5, 15000, a="V"),
    "M62-3.5": f("ATM", E_, 3.5, "CHAINE", 8, 5700, 3300, "5W30", 7.5, 15000, a="V"),
    "M62-4.4": f("ATM", E_, 4.4, "CHAINE", 8, 5400, 3600, "5W30", 7.5, 15000, a="V"),
    "M62-4.6": f("ATM", E_, 4.6, "CHAINE", 8, 5700, 3700, "5W30", 7.5, 15000, a="V"),
    "M70-5.0": f("ATM", E_, 5.0, "CHAINE", 12, 5200, 4100, "10W40", 8.5, 15000, a="V"),
    "M73-5.4": f("ATM", E_, 5.4, "CHAINE", 12, 5000, 3900, "5W30", 8.5, 15000, a="V"),
    # série N
    "N42-1.8": f("ATM", E_, 1.8, "CHAINE", 4, 5500, 3750, "5W30", 4.25, 25000),
    "N42-2.0": f("ATM", E_, 2.0, "CHAINE", 4, 6000, 3750, "5W30", 4.25, 25000),
    "N45-1.6": f("ATM", E_, 1.6, "CHAINE", 4, 6000, 4300, "5W30", 4.25, 25000),
    "N46-2.0": f("ATM", E_, 2.0, "CHAINE", 4, 6200, 3600, "5W30", 4.25, 25000),
    "N43-1.6": f("ATM", E_, 1.6, "CHAINE", 4, 6000, 4250, "5W30", 4.25, 25000),
    "N43-2.0": f("ATM", E_, 2.0, "CHAINE", 4, 6700, 4250, "5W30", 4.25, 25000),
    "N13-1.6": f("TURBO", E_, 1.6, "CHAINE", 4, 4800, 1350, "5W30", 4.25, 30000),
    "N20-2.0": f("TURBO", E_, 2.0, "CHAINE", 4, 5000, 1250, "5W30", 5.0, 30000),
    "N20-PHEV": f("HYB_TE", E_, 2.0, "CHAINE", 4, 5000, 1250, "5W30", 5.0, 30000),
    "N52-2.5": f("ATM", E_, 2.5, "CHAINE", 6, 6500, 2750, "5W30", 6.5, 25000),
    "N52-3.0": f("ATM", E_, 3.0, "CHAINE", 6, 6600, 2750, "5W30", 6.5, 25000),
    "N53-3.0": f("ATM", E_, 3.0, "CHAINE", 6, 6700, 2750, "5W30", 6.5, 25000),
    "N54-3.0": f("TURBO", E_, 3.0, "CHAINE", 6, 5800, 1300, "5W30", 6.5, 25000),
    "N55-3.0": f("TURBO", E_, 3.0, "CHAINE", 6, 5800, 1200, "5W30", 6.5, 30000),
    "N55-HYB": f("HYB_TE", E_, 3.0, "CHAINE", 6, 5800, 1200, "5W30", 6.5, 30000),
    "N62-3.6": f("ATM", E_, 3.6, "CHAINE", 8, 6200, 3700, "5W30", 8.0, 25000, a="V"),
    "N62-4.0": f("ATM", E_, 4.0, "CHAINE", 8, 6300, 3500, "5W30", 8.0, 25000, a="V"),
    "N62-4.4": f("ATM", E_, 4.4, "CHAINE", 8, 6100, 3600, "5W30", 8.0, 25000, a="V"),
    "N62-4.8": f("ATM", E_, 4.8, "CHAINE", 8, 6300, 3400, "5W30", 8.0, 25000, a="V"),
    "N63-4.4": f("TURBO", E_, 4.4, "CHAINE", 8, 5500, 1800, "5W30", 8.5, 30000, a="V"),
    "N63-HYB": f("HYB_TE", E_, 4.4, "CHAINE", 8, 5500, 1800, "5W30", 8.5, 30000, a="V"),
    "N73-6.0": f("ATM", E_, 6.0, "CHAINE", 12, 6000, 3950, "5W30", 9.5, 25000, a="V"),
    "N74-6.6": f("TURBO", E_, 6.6, "CHAINE", 12, 5500, 1500, "5W30", 9.5, 30000, a="V"),
    "B48-PHEV": f("HYB_TE", E_, 2.0, "CHAINE", 4, 5000, 1350, "0W20", 5.25, 30000),
    "B48-MHEV": f("HYB_TE", E_, 2.0, "CHAINE", 4, 5000, 1500, "0W20", 5.25, 30000),
    "B38-MHEV": f("HYB_TE", E_, 1.5, "CHAINE", 3, 5000, 1500, "0W20", 4.25, 30000),
    "B58-3.0": f("TURBO", E_, 3.0, "CHAINE", 6, 5500, 1600, "0W20", 6.5, 30000),
    "B58-MHEV": f("HYB_TE", E_, 3.0, "CHAINE", 6, 5500, 1600, "0W20", 6.5, 30000),
    "B58-PHEV": f("HYB_TE", E_, 3.0, "CHAINE", 6, 5500, 1500, "0W20", 6.5, 30000),
    # diesel
    "M21-2.4": f("ATM", D, 2.4, "COURROIE", 6, 4600, 2500, "15W40", 6.5, 10000),
    "M21-2.4T": f("TURBO", D, 2.4, "COURROIE", 6, 4800, 2400, "15W40", 6.5, 10000),
    "M41-1.7": f("TURBO", D, 1.7, "CHAINE", 4, 4400, 2000, "10W40", 5.0, 15000),
    "M51-2.5": f("TURBO", D, 2.5, "CHAINE", 6, 4800, 2200, "10W40", 6.5, 15000),
    "M47-2.0": f("TURBO", D, 2.0, "CHAINE", 4, 4000, 2000, "5W30", 5.25, 25000),
    "M57-2.5": f("TURBO", D, 2.5, "CHAINE", 6, 4000, 2000, "5W30", 6.5, 25000),
    "M57-3.0": f("TURBO", D, 3.0, "CHAINE", 6, 4000, 2000, "5W30", 6.5, 25000),
    "M67-3.9": f("TURBO", D, 3.9, "CHAINE", 8, 4000, 1750, "5W30", 9.0, 25000, a="V"),
    "M67-4.4": f("TURBO", D, 4.4, "CHAINE", 8, 3800, 1900, "5W30", 9.0, 25000, a="V"),
    "N47-1.6": f("TURBO", D, 1.6, "CHAINE", 4, 4000, 1750, "5W30", 4.5, 25000),
    "N47-2.0": f("TURBO", D, 2.0, "CHAINE", 4, 4000, 1750, "5W30", 5.2, 25000),
    "N57-3.0": f("TURBO", D, 3.0, "CHAINE", 6, 4000, 1750, "5W30", 6.5, 30000),
    "B47-MHEV": f("TURBO", D, 2.0, "CHAINE", 4, 4000, 1500, "0W30", 5.2, 30000),
    "B57-3.0": f("TURBO", D, 3.0, "CHAINE", 6, 4000, 1750, "0W30", 7.0, 30000),
    # BMW M
    "M88-3.5": f("ATM", E_, 3.5, "CHAINE", 6, 6500, 4500, "10W60", 5.75, 10000),
    "S14-2.3": f("ATM", E_, 2.3, "CHAINE", 4, 6750, 4750, "10W60", 4.5, 10000),
    "S14-2.5": f("ATM", E_, 2.5, "CHAINE", 4, 7000, 4750, "10W60", 4.5, 10000),
    "S38-3.6": f("ATM", E_, 3.6, "CHAINE", 6, 6900, 4750, "10W60", 5.75, 10000),
    "S38-3.8": f("ATM", E_, 3.8, "CHAINE", 6, 6900, 4750, "10W60", 5.75, 10000),
    "S50-3.0": f("ATM", E_, 3.0, "CHAINE", 6, 7000, 3600, "10W60", 6.5, 15000),
    "S50-3.2": f("ATM", E_, 3.2, "CHAINE", 6, 7400, 3250, "10W60", 6.5, 15000),
    "S54-3.2": f("ATM", E_, 3.2, "CHAINE", 6, 7900, 4900, "10W60", 5.5, 15000),
    "S62-5.0": f("ATM", E_, 5.0, "CHAINE", 8, 6600, 3800, "10W60", 6.5, 15000, a="V"),
    "S65-4.0": f("ATM", E_, 4.0, "CHAINE", 8, 8300, 3900, "10W60", 8.8, 15000, a="V"),
    "S70-5.6": f("ATM", E_, 5.6, "CHAINE", 12, 5300, 4000, "10W60", 8.5, 15000, a="V"),
    "S85-5.0": f("ATM", E_, 5.0, "CHAINE", 10, 7750, 6100, "10W60", 9.3, 15000, a="V"),
    "S55-3.0": f("TURBO", E_, 3.0, "CHAINE", 6, 5500, 1850, "0W40", 6.5, 15000),
    "S58-3.0": f("TURBO", E_, 3.0, "CHAINE", 6, 6250, 2750, "0W30", 6.75, 15000),
    "S63-4.4": f("TURBO", E_, 4.4, "CHAINE", 8, 6000, 1800, "0W30", 9.0, 15000, a="V"),
    "S68-4.4": f("HYB_TE", E_, 4.4, "CHAINE", 8, 5600, 1800, "0W30", 9.5, 15000, a="V"),
    # électrique
    "BMW-I3": electrique(), "BMW-EDRIVE5": electrique(), "BMW-GEN6": electrique(),
})

B, M = "BMW", "BMW M"
TABLE = {
    # --- E21 / E12 / E28 / E24 / E23 (M10, M20, M30)
    "315 75": ("M10-1.6", 75, 110), "316 90": ("M10-1.8", 90, 140), "318 98": ("M10-1.8", 98, 145),
    "318i 105": ("M10-1.8", 105, 145), "320 109": ("M10-2.0", 109, 157), "320i 125@E21": ("M10-2.0", 125, 172),
    "320/6 122": ("M20-2.0", 122, 160), "323i 143": ("M20-2.3", 143, 190), "518 90": ("M10-1.8", 90, 143),
    "520 115": ("M10-2.0", 115, 162), "520i 125@E21": ("M10-2.0", 125, 172), "520/6 122": ("M20-2.0", 122, 160),
    "525 145": ("M30-2.5", 145, 208), "528i 177": ("M30-2.8", 177, 235), "518i 105": ("M10-1.8", 105, 145),
    "520i 125": ("M20-2.0", 125, 165), "520i 129": ("M20-2.0", 129, 174), "525i 150": ("M30-2.5", 150, 215),
    "528i 184": ("M30-2.8", 184, 240), "535i 218": ("M30-3.4", 218, 310), "524td 115": ("M21-2.4T", 115, 210),
    "524d 86": ("M21-2.4", 86, 152), "630CS 185": ("M30-3.0", 185, 255), "633CSi 197": ("M30-3.2", 197, 285),
    "628CSi 184": ("M30-2.8", 184, 240), "635CSi 218": ("M30-3.4", 218, 310), "M635CSi 286": (M, "M88-3.5", 286, 340),
    "728i 184": ("M30-2.8", 184, 240), "732i 197": ("M30-3.2", 197, 285), "735i 218": ("M30-3.4", 218, 310),
    "745i 252": ("M102-3.2T", 252, 380),
    # --- E30 / E34 / E32 (M10, M20, M30, M40, M42, M21)
    "320i 125": ("M20-2.0", 125, 165), "320i 129": ("M20-2.0", 129, 164), "323i 139": ("M20-2.3", 139, 205),
    "323i 150": ("M20-2.3", 150, 205), "325i 171": ("M20-2.5", 171, 226), "325i 170": ("M20-2.5", 170, 222),
    "325e 122": ("M20-2.7", 122, 240), "324d 86": ("M21-2.4", 86, 152), "324td 115": ("M21-2.4T", 115, 210),
    "316i 100": ("M40-1.6", 100, 141), "318i 113": ("M40-1.8", 113, 162), "318is 136": ("M42-1.8", 136, 172),
    "518i 113": ("M40-1.8", 113, 162), "525i 170": ("M20-2.5", 170, 222), "530i 188": ("M30-3.0", 188, 260),
    "535i 211": ("M30-3.4", 211, 305), "730i 188": ("M30-3.0", 188, 260), "735i 211": ("M30-3.4", 211, 305),
    "750i 300": ("M70-5.0", 300, 450), "730i 218": ("M60-3.0", 218, 290), "740i 286@E36": ("M60-4.0", 286, 400),
    "850i 300": ("M70-5.0", 300, 450), "850Ci 326": ("M73-5.4", 326, 490), "840Ci 286": ("M60-4.0", 286, 400),
    "850CSi 380": (M, "S70-5.6", 380, 550), "Z1 170": ("M20-2.5", 170, 222),
    # --- E36 / E34 phase 2 (M40, M42, M43, M44, M50, M52, M41, M51)
    "318is 140": ("M42-1.8", 140, 175), "320i 150@E36": ("M50-2.0", 150, 190), "325i 192@E36": ("M50-2.5", 192, 245),
    "318tds 90": ("M41-1.7", 90, 190), "325td 115": ("M51-2.5", 115, 222), "525td 115": ("M51-2.5", 115, 222), "325tds 143": ("M51-2.5", 143, 260),
    "316i 102": ("M43-1.6", 102, 150), "318i 115": ("M43-1.8", 115, 168), "323i 170": ("M52-2.5", 170, 245),
    "328i 193": ("M52-2.8", 193, 280), "518i 115": ("M43-1.8", 115, 168), "520i 150@E36": ("M50-2.0", 150, 190),
    "525i 192@E36": ("M50-2.5", 192, 245), "530i 218": ("M60-3.0", 218, 290), "540i 286@E36": ("M60-4.0", 286, 400),
    "525tds 143": ("M51-2.5", 143, 280), "725tds 143": ("M51-2.5", 143, 280),
    # --- E46 / E39 / E38 / E53 / E83 / Z3 / E85 (M43, M52, M54, M62, M47, M57, N42)
    "316i 105": ("M43-1.9", 105, 165), "318i 118": ("M43-1.9", 118, 180), "320i 150@M5X": ("M52-2.0", 150, 190),
    "316i 115": ("N42-1.8", 115, 175), "320i 170@M5X": ("M54-2.2", 170, 210), "325i 192": ("M54-2.5", 192, 245),
    "330i 231": ("M54-3.0", 231, 300), "320d 136": ("M47-2.0", 136, 280), "318d 116": ("M47-2.0", 116, 280),
    "320d 150": ("M47-2.0", 150, 330), "330d 184": ("M57-3.0", 184, 390), "330d 204": ("M57-3.0", 204, 410),
    "520i 150@M5X": ("M52-2.0", 150, 190), "523i 170": ("M52-2.5", 170, 245), "528i 193": ("M52-2.8", 193, 280),
    "535i 235": ("M62-3.5", 235, 320), "535i 245": ("M62-3.5", 245, 345), "540i 286": ("M62-4.4", 286, 440),
    "520i 170@M5X": ("M54-2.2", 170, 210), "530i 231": ("M54-3.0", 231, 300), "520d 136": ("M47-2.0", 136, 280),
    "525d 163": ("M57-2.5", 163, 350), "530d 184": ("M57-3.0", 184, 390), "530d 193": ("M57-3.0", 193, 410),
    "728i 193": ("M52-2.8", 193, 280), "735i 238": ("M62-3.5", 238, 345), "740i 286": ("M62-4.4", 286, 440),
    "750i 326": ("M73-5.4", 326, 490), "730d 184": ("M57-3.0", 184, 410), "730d 193": ("M57-3.0", 193, 430),
    "740d 245": ("M67-3.9", 245, 560), "3.0i 231": ("M54-3.0", 231, 300), "4.4i 286": ("M62-4.4", 286, 440),
    "4.6is 347": ("M62-4.6", 347, 480), "3.0d 184": ("M57-3.0", 184, 410), "4.4i 320": ("N62-4.4", 320, 440),
    "4.8is 360": ("N62-4.8", 360, 500), "3.0d 218": ("M57-3.0", 218, 500), "2.0i 150": ("N46-2.0", 150, 200),
    "2.5i 192": ("M54-2.5", 192, 245), "2.0d 150": ("M47-2.0", 150, 330), "3.0d 204": ("M57-3.0", 204, 410),
    "2.5si 218": ("N52-2.5", 218, 250), "3.0si 272": ("N52-3.0", 272, 315), "2.0d 177": ("N47-2.0", 177, 350),
    "3.0sd 286": ("M57-3.0", 286, 580), "1.8 115": ("M43-1.8", 115, 168), "1.9 140": ("M44-1.9", 140, 180),
    "1.9 118": ("M43-1.9", 118, 180), "2.0 150": ("M52-2.0", 150, 190), "2.2i 170": ("M54-2.2", 170, 210),
    "2.8 193": ("M52-2.8", 193, 280), "2.5i 177": ("N52-2.5", 177, 230), "3.0si 265": ("N52-3.0", 265, 315),
    "Z8 400": (M, "S62-5.0", 400, 500),
    # --- 4 cylindres essence N (E87, E90, E60…)
    "116i 115": ("N45-1.6", 115, 150), "116i 122": ("N43-1.6", 122, 160), "118i 129": ("N46-2.0", 129, 180),
    "118i 143": ("N46-2.0", 143, 190), "120i 150": ("N46-2.0", 150, 200), "120i 170": ("N43-2.0", 170, 210),
    "318i 129": ("N46-2.0", 129, 180), "318i 143": ("N46-2.0", 143, 200), "320i 150": ("N46-2.0", 150, 200),
    "320i 170": ("N43-2.0", 170, 210), "316i 122": ("N43-1.6", 122, 160), "520i 170": ("N43-2.0", 170, 210),
    "sDrive18i 150": ("N46-2.0", 150, 200),
    # --- N13 / N20
    "114i 102": ("N13-1.6", 102, 180), "116i 136": ("N13-1.6", 136, 220), "118i 170": ("N13-1.6", 170, 250),
    "316i 136": ("N13-1.6", 136, 220), "125i 218": ("N20-2.0", 218, 310), "125i 218@N54": ("N52-3.0", 218, 270),
    "220i 184": ("N20-2.0", 184, 270), "228i 245": ("N20-2.0", 245, 350), "320i 184": ("N20-2.0", 184, 270),
    "328i 245": ("N20-2.0", 245, 350), "420i 184": ("N20-2.0", 184, 270), "428i 245": ("N20-2.0", 245, 350),
    "520i 184": ("N20-2.0", 184, 270), "528i 245": ("N20-2.0", 245, 350), "sDrive20i 184": ("N20-2.0", 184, 270),
    "xDrive20i 184": ("N20-2.0", 184, 270), "xDrive28i 245": ("N20-2.0", 245, 350), "sDrive28i 245": ("N20-2.0", 245, 350),
    "sDrive18i 156": ("N20-2.0", 156, 240), "xDrive40e 313": ("N20-PHEV", 313, 450),
    # --- 6 cylindres essence N52 / N53 / N54 / N55
    "130i 265": ("N52-3.0", 265, 315), "325i 218": ("N52-2.5", 218, 250), "330i 258": ("N52-3.0", 258, 300),
    "330i 272": ("N53-3.0", 272, 320), "523i 177": ("N52-2.5", 177, 230), "523i 190": ("N52-2.5", 190, 240),
    "523i 204": ("N52-3.0", 204, 270), "525i 192@M5X": ("M54-2.5", 192, 245), "525i 218": ("N52-2.5", 218, 250),
    "530i 231@M5X": ("M54-3.0", 231, 300), "530i 258": ("N52-3.0", 258, 300), "530i 272": ("N53-3.0", 272, 320),
    "528i 258": ("N52-3.0", 258, 310), "630i 258": ("N52-3.0", 258, 300), "630i 272": ("N53-3.0", 272, 320),
    "730i 231": ("M54-3.0", 231, 300), "730i 258": ("N52-3.0", 258, 300), "sDrive23i 204": ("N52-2.5", 204, 250),
    "sDrive30i 258": ("N52-3.0", 258, 310), "xDrive28i 258": ("N52-3.0", 258, 310),
    "135i 306": ("N54-3.0", 306, 400), "335i 306": ("N55-3.0", 306, 400), "335i 306@N54": ("N54-3.0", 306, 400),
    "535i 306": ("N55-3.0", 306, 400), "740i 326": ("N54-3.0", 326, 450), "740i 326@F": ("N55-3.0", 326, 450),
    "sDrive35i 306": ("N54-3.0", 306, 400), "sDrive35is 340": ("N54-3.0", 340, 450),
    "xDrive35i 306": ("N55-3.0", 306, 400), "xDrive35i 306@N54": ("N54-3.0", 306, 400),
    "M135i 320": ("N55-3.0", 320, 450), "M235i 326": ("N55-3.0", 326, 450), "435i 306": ("N55-3.0", 306, 400),
    "640i 320": ("N55-3.0", 320, 450), "M40i 360@F": ("N55-3.0", 360, 465),
    "ActiveHybrid 3 340": ("N55-HYB", 340, 450), "ActiveHybrid 5 340": ("N55-HYB", 340, 450),
    # --- V8 / V12 N
    "735i 272": ("N62-3.6", 272, 360), "740i 306": ("N62-4.0", 306, 390), "745i 333": ("N62-4.4", 333, 450),
    "545i 333": ("N62-4.4", 333, 450), "645Ci 333": ("N62-4.4", 333, 450), "750i 367": ("N62-4.8", 367, 490),
    "550i 367": ("N62-4.8", 367, 490), "650i 367": ("N62-4.8", 367, 490), "540i 306": ("N62-4.0", 306, 390),
    "4.8i 355": ("N62-4.8", 355, 475), "760i 445": ("N73-6.0", 445, 600),
    "550i 407": ("N63-4.4", 407, 600), "550i 449": ("N63-4.4", 449, 650), "650i 407": ("N63-4.4", 407, 600),
    "650i 449": ("N63-4.4", 449, 650), "750i 407": ("N63-4.4", 407, 600), "750i 449": ("N63-4.4", 449, 650),
    "750i 450": ("N63-4.4", 450, 650), "750i 530": ("N63-4.4", 530, 750), "xDrive50i 407": ("N63-4.4", 407, 600),
    "xDrive50i 450": ("N63-4.4", 450, 650), "M550i 462": ("N63-4.4", 462, 650), "M550i 530": ("N63-4.4", 530, 750),
    "M850i 530": ("N63-4.4", 530, 750), "M850i 523": ("N63-4.4", 523, 750), "M50i 530": ("N63-4.4", 530, 750),
    "ActiveHybrid 7 465": ("N63-HYB", 465, 700), "ActiveHybrid X6 485": ("N63-HYB", 485, 780),
    "760i 544": ("N74-6.6", 544, 750), "M760i 610": ("N74-6.6", 610, 800), "M760i 585": ("N74-6.6", 585, 850),
    # --- B38 / B48 / B58 (familles Mini)
    "116i 109": ("B38A15", 109, 180), "118i 136": ("B38A15", 136, 220), "118i 140": ("B38A15", 140, 220),
    "118 156": ("B38A15", 156, 240), "120 170": ("B38-MHEV", 170, 280), "216i 102": ("B38A15", 102, 180),
    "216i 109": ("B38A15", 109, 190), "218i 136": ("B38A15", 136, 220), "218i 140": ("B38A15", 140, 220),
    "220 170": ("B38-MHEV", 170, 280), "318i 136": ("B38A15", 136, 220), "sDrive18i 136": ("B38A15", 136, 220),
    "sDrive18i 140": ("B38A15", 140, 220), "sDrive20i 170": ("B38-MHEV", 170, 280),
    "225xe 224": ("B38-PHEV", 224, 385), "xDrive25e 220": ("B38-PHEV", 220, 385), "225e 245": ("B38-PHEV", 245, 477),
    "230e 326": ("B38-PHEV", 326, 477), "xDrive25e 245": ("B38-PHEV", 245, 477), "xDrive30e 326": ("B38-PHEV", 326, 477),
    "i8 362": ("B38-PHEV", 362, 570), "i8 374": ("B38-PHEV", 374, 570),
    "120i 184": ("B48A20", 184, 290), "120i 178": ("B48A20", 178, 280), "125i 224": ("B48A20", 224, 350),
    "128ti 265": ("B48A20", 265, 400), "M135i 306": ("B48A20", 306, 450), "M235i 306": ("B48A20", 306, 450), "M135 300": ("B48A20", 300, 400),
    "220i 184@G": ("B48A20", 184, 290), "220i 192": ("B48A20", 192, 280), "220i 178": ("B48A20", 178, 280),
    "225i 231": ("B48A20", 231, 350), "230i 252": ("B48A20", 252, 350), "230i 245": ("B48A20", 245, 400),
    "223 218": ("B48-MHEV", 218, 360), "318i 156": ("B48A20", 156, 250), "320i 184@G": ("B48A20", 184, 300),
    "330i 252": ("B48A20", 252, 350), "330i 258@G": ("B48A20", 258, 400), "330i 245": ("B48A20", 245, 400),
    "420i 184@G": ("B48A20", 184, 300), "430i 252": ("B48A20", 252, 350), "430i 258": ("B48A20", 258, 400),
    "430i 245": ("B48A20", 245, 400), "520i 184@G": ("B48A20", 184, 290), "530i 252": ("B48A20", 252, 350),
    "520i 208": ("B48-MHEV", 208, 330), "630i 258@G": ("B48A20", 258, 400), "730i 258@G": ("B48A20", 258, 400),
    "sDrive20i 192": ("B48A20", 192, 280), "sDrive20i 178": ("B48A20", 178, 280), "xDrive25i 231": ("B48A20", 231, 350),
    "xDrive23i 218": ("B48-MHEV", 218, 360), "M35i 306": ("B48A20", 306, 450), "M35i 300": ("B48A20", 300, 400),
    "xDrive20i 184@G": ("B48A20", 184, 290), "xDrive30i 252": ("B48A20", 252, 350), "xDrive30i 245": ("B48A20", 245, 350),
    "20 xDrive 208": ("B48-MHEV", 208, 330), "sDrive20i 197": ("B48A20", 197, 320), "sDrive30i 258@G": ("B48A20", 258, 400),
    "330e 252": ("B48-PHEV", 252, 420), "330e 292": ("B48-PHEV", 292, 420), "320e 204": ("B48-PHEV", 204, 350),
    "530e 252": ("B48-PHEV", 252, 420), "530e 292": ("B48-PHEV", 292, 420), "530e 299": ("B48-PHEV", 299, 450),
    "xDrive30e 292": ("B48-PHEV", 292, 420), "30e xDrive 299": ("B48-PHEV", 299, 450), "740e 326": ("B48-PHEV", 326, 500),
    "M140i 340": ("B58-3.0", 340, 500), "M240i 340": ("B58-3.0", 340, 500), "M240i 374": ("B58-3.0", 374, 500),
    "340i 326": ("B58-3.0", 326, 450), "M340i 374": ("B58-MHEV", 374, 500), "440i 326": ("B58-3.0", 326, 450),
    "M440i 374": ("B58-MHEV", 374, 500), "540i 340": ("B58-3.0", 340, 450), "540i 333": ("B58-MHEV", 333, 450),
    "640i 340": ("B58-3.0", 340, 450), "740i 326@G": ("B58-3.0", 326, 450), "740i 333": ("B58-3.0", 333, 450),
    "740i 380": ("B58-MHEV", 380, 520), "840i 340": ("B58-3.0", 340, 500), "840i 333": ("B58-3.0", 333, 500),
    "M40i 360": ("B58-3.0", 360, 500), "M40i 354": ("B58-MHEV", 354, 500), "M40i 340": ("B58-3.0", 340, 500),
    "M50 xDrive 398": ("B58-MHEV", 398, 580), "xDrive40i 340": ("B58-3.0", 340, 450),
    "xDrive40i 333": ("B58-MHEV", 333, 450), "xDrive40i 381": ("B58-MHEV", 381, 540),
    "545e 394": ("B58-PHEV", 394, 600), "745e 394": ("B58-PHEV", 394, 600), "xDrive45e 394": ("B58-PHEV", 394, 600),
    "xDrive50e 489": ("B58-PHEV", 489, 700), "550e 489": ("B58-PHEV", 489, 700), "750e 489": ("B58-PHEV", 489, 700),
    "M760e 571": ("B58-PHEV", 571, 800),
    "M60i 530": (M, "S68-4.4", 530, 750), "760i 544@G": (M, "S68-4.4", 544, 750),
    # --- diesel M47 / M57 / M67
    "118d 122": ("M47-2.0", 122, 280), "120d 163": ("M47-2.0", 163, 340), "318d 122": ("M47-2.0", 122, 280),
    "320d 163": ("M47-2.0", 163, 340), "520d 163": ("M47-2.0", 163, 340), "325d 197": ("M57-3.0", 197, 400),
    "330d 231": ("M57-3.0", 231, 500), "335d 286": ("M57-3.0", 286, 580), "525d 177": ("M57-2.5", 177, 400),
    "525d 197": ("M57-3.0", 197, 400), "530d 218": ("M57-3.0", 218, 500), "530d 231": ("M57-3.0", 231, 500),
    "530d 235": ("M57-3.0", 235, 520), "535d 272": ("M57-3.0", 272, 560), "535d 286": ("M57-3.0", 286, 580),
    "635d 286": ("M57-3.0", 286, 580), "730d 218": ("M57-3.0", 218, 500), "730d 231": ("M57-3.0", 231, 520),
    "740d 258": ("M67-3.9", 258, 600), "745d 300": ("M67-4.4", 300, 700), "3.0d 235": ("M57-3.0", 235, 520),
    "xDrive30d 235": ("M57-3.0", 235, 520), "xDrive35d 286": ("M57-3.0", 286, 580),
    # --- diesel N47 / N57
    "114d 95": ("N47-1.6", 95, 235), "116d 116": ("N47-2.0", 116, 260), "118d 143": ("N47-2.0", 143, 320),
    "120d 177": ("N47-2.0", 177, 350), "120d 184": ("N47-2.0", 184, 380), "123d 204": ("N47-2.0", 204, 400),
    "125d 218": ("N47-2.0", 218, 450), "316d 116": ("N47-2.0", 116, 260), "318d 143": ("N47-2.0", 143, 320),
    "320d 177": ("N47-2.0", 177, 350), "320d 184": ("N47-2.0", 184, 380), "325d 218": ("N47-2.0", 218, 450),
    "218d 143": ("N47-2.0", 143, 320), "220d 184": ("N47-2.0", 184, 380), "225d 218": ("N47-2.0", 218, 450),
    "418d 143": ("N47-2.0", 143, 320), "420d 184": ("N47-2.0", 184, 380), "425d 218": ("N47-2.0", 218, 450),
    "518d 143": ("N47-2.0", 143, 360), "520d 177": ("N47-2.0", 177, 350), "520d 184": ("N47-2.0", 184, 380),
    "525d 218": ("N47-2.0", 218, 450), "sDrive16d 116": ("N47-2.0", 116, 260), "sDrive18d 143": ("N47-2.0", 143, 320),
    "xDrive20d 177": ("N47-2.0", 177, 350), "xDrive20d 184": ("N47-2.0", 184, 380), "xDrive23d 204": ("N47-2.0", 204, 400),
    "xDrive25d 218": ("N47-2.0", 218, 450), "sDrive25d 218": ("N47-2.0", 218, 450),
    "325d 204": ("N57-3.0", 204, 430), "330d 245": ("N57-3.0", 245, 520), "330d 258": ("N57-3.0", 258, 560),
    "335d 313": ("N57-3.0", 313, 630), "430d 258": ("N57-3.0", 258, 560), "435d 313": ("N57-3.0", 313, 630),
    "525d 204": ("N57-3.0", 204, 450), "530d 245": ("N57-3.0", 245, 540), "530d 258": ("N57-3.0", 258, 560),
    "535d 300": ("N57-3.0", 300, 600), "535d 313": ("N57-3.0", 313, 630), "M550d 381": ("N57-3.0", 381, 740),
    "640d 313": ("N57-3.0", 313, 630), "730d 245": ("N57-3.0", 245, 540), "730d 258": ("N57-3.0", 258, 560),
    "740d 306": ("N57-3.0", 306, 600), "740d 313": ("N57-3.0", 313, 630), "750d 381": ("N57-3.0", 381, 740),
    "xDrive30d 245": ("N57-3.0", 245, 540), "xDrive30d 258": ("N57-3.0", 258, 560), "xDrive35d 313": ("N57-3.0", 313, 630),
    "xDrive40d 306": ("N57-3.0", 306, 600), "xDrive40d 313": ("N57-3.0", 313, 630), "M50d 381": ("N57-3.0", 381, 740),
    # --- diesel B37 / B47 / B57
    "116d 116@G": ("B37C15", 116, 270), "216d 116": ("B37C15", 116, 270), "216d 122": ("B37C15", 122, 280),
    "sDrive16d 116@G": ("B37C15", 116, 270), "118d 150": ("B47C20", 150, 350), "120d 190": ("B47C20", 190, 400),
    "120d 163@G": ("B47-MHEV", 163, 400), "125d 224": ("B47C20", 224, 450), "218d 150": ("B47C20", 150, 350),
    "220d 190": ("B47C20", 190, 400), "225d 224": ("B47C20", 224, 450), "316d 116@G": ("B47C20", 116, 270),
    "316d 122": ("B47C20", 122, 300), "318d 150": ("B47C20", 150, 320), "320d 190": ("B47C20", 190, 400),
    "325d 224": ("B47C20", 224, 450), "418d 150": ("B47C20", 150, 320), "420d 190": ("B47C20", 190, 400),
    "425d 224": ("B47C20", 224, 450), "518d 150": ("B47C20", 150, 350), "520d 190": ("B47C20", 190, 400),
    "520d 197": ("B47-MHEV", 197, 400), "525d 231": ("B47C20", 231, 500), "620d 190": ("B47C20", 190, 400),
    "sDrive18d 150": ("B47C20", 150, 350), "xDrive20d 190": ("B47C20", 190, 400), "xDrive20d 163": ("B47-MHEV", 163, 400),
    "xDrive23d 211": ("B47-MHEV", 211, 400), "xDrive25d 231": ("B47C20", 231, 450), "sDrive25d 231": ("B47C20", 231, 450),
    "20d xDrive 197": ("B47-MHEV", 197, 400),
    "330d 265": ("B57-3.0", 265, 580), "330d 286": ("B57-3.0", 286, 650), "M340d 340": ("B57-3.0", 340, 700),
    "430d 286": ("B57-3.0", 286, 650), "M440d 340": ("B57-3.0", 340, 700), "530d 265": ("B57-3.0", 265, 620),
    "530d 286": ("B57-3.0", 286, 650), "540d 320": ("B57-3.0", 320, 680), "540d 340": ("B57-3.0", 340, 700),
    "M550d 400": ("B57-3.0", 400, 760), "630d 265": ("B57-3.0", 265, 620), "630d 286": ("B57-3.0", 286, 650),
    "725d 231": ("B57-3.0", 231, 620), "730d 265": ("B57-3.0", 265, 620), "730d 286": ("B57-3.0", 286, 650),
    "740d 320": ("B57-3.0", 320, 680), "740d 340": ("B57-3.0", 340, 700), "740d 300": ("B57-3.0", 300, 670),
    "750d 400": ("B57-3.0", 400, 760), "840d 320": ("B57-3.0", 320, 680), "840d 340": ("B57-3.0", 340, 700),
    "xDrive30d 265": ("B57-3.0", 265, 620), "xDrive30d 286": ("B57-3.0", 286, 650), "xDrive30d 298": ("B57-3.0", 298, 670),
    "xDrive40d 340": ("B57-3.0", 340, 700), "xDrive40d 352": ("B57-3.0", 352, 720), "M50d 400": ("B57-3.0", 400, 760),
    "M40d 326": ("B57-3.0", 326, 680), "M40d 340": ("B57-3.0", 340, 700),
    # --- électriques
    "i3 170": ("BMW-I3", 170, 250), "i3 170 94Ah": ("BMW-I3", 170, 250), "i3 170 120Ah": ("BMW-I3", 170, 250),
    "i3s 184": ("BMW-I3", 184, 270), "i3 REx 170": ("BMW-I3", 170, 250),
    "eDrive35 286": ("BMW-EDRIVE5", 286, 400), "eDrive40 340": ("BMW-EDRIVE5", 340, 430),
    "xDrive40 401": ("BMW-EDRIVE5", 401, 600), "M50 544": ("BMW-EDRIVE5", 544, 795), "M50 601": ("BMW-EDRIVE5", 601, 795),
    "xDrive40 394": ("BMW-EDRIVE5", 394, 586), "M60 601": ("BMW-EDRIVE5", 601, 795),
    "xDrive60 544": ("BMW-EDRIVE5", 544, 745), "eDrive50 455": ("BMW-EDRIVE5", 455, 650), "M70 660": ("BMW-EDRIVE5", 660, 1100),
    "xDrive40 326": ("BMW-EDRIVE5", 326, 630), "xDrive50 523": ("BMW-EDRIVE5", 523, 765), "M60 619": ("BMW-EDRIVE5", 619, 1100),
    "xDrive45 408": ("BMW-EDRIVE5", 408, 700), "M70 659": ("BMW-EDRIVE5", 659, 1100), "iX3 286": ("BMW-EDRIVE5", 286, 400),
    "iX1 eDrive20 204": ("BMW-EDRIVE5", 204, 250), "iX1 xDrive30 313": ("BMW-EDRIVE5", 313, 494),
    "iX2 eDrive20 204": ("BMW-EDRIVE5", 204, 250), "iX2 xDrive30 313": ("BMW-EDRIVE5", 313, 494),
    "50 xDrive 469": ("BMW-GEN6", 469, 645),
    # --- BMW M
    "M1 277": (M, "M88-3.5", 277, 330), "1M 340": ("N54-3.0", 340, 450), "M2 370": ("N55-3.0", 370, 465),
    "M2 Competition 410": (M, "S55-3.0", 410, 550), "M2 CS 450": (M, "S55-3.0", 450, 550),
    "M2 460": (M, "S58-3.0", 460, 550), "M2 480": (M, "S58-3.0", 480, 600), "M2 CS 530": (M, "S58-3.0", 530, 650),
    "M3 2.3 195": (M, "S14-2.3", 195, 230), "M3 2.3 200": (M, "S14-2.3", 200, 240), "M3 Evo 2.3 220": (M, "S14-2.3", 220, 245),
    "M3 Sport Evo 2.5 238": (M, "S14-2.5", 238, 240), "M3 3.0 286": (M, "S50-3.0", 286, 320),
    "M3 3.2 321": (M, "S50-3.2", 321, 350), "M3 343": (M, "S54-3.2", 343, 365), "M3 CSL 360": (M, "S54-3.2", 360, 370),
    "M3 420": (M, "S65-4.0", 420, 400), "M3 GTS 450": (M, "S65-4.0", 450, 440), "M3 431": (M, "S55-3.0", 431, 550),
    "M3 Competition 450": (M, "S55-3.0", 450, 550), "M3 CS 460": (M, "S55-3.0", 460, 600),
    "M3 480": (M, "S58-3.0", 480, 550), "M3 Competition 510": (M, "S58-3.0", 510, 650),
    "M3 Competition 530": (M, "S58-3.0", 530, 650), "M3 CS 550": (M, "S58-3.0", 550, 650),
    "M4 431": (M, "S55-3.0", 431, 550), "M4 Competition 450": (M, "S55-3.0", 450, 550), "M4 GTS 500": (M, "S55-3.0", 500, 600),
    "M4 CS 460": (M, "S55-3.0", 460, 600), "M4 480": (M, "S58-3.0", 480, 550), "M4 Competition 510": (M, "S58-3.0", 510, 650),
    "M4 CSL 550": (M, "S58-3.0", 550, 650), "M4 Competition 530": (M, "S58-3.0", 530, 650), "M4 CS 550": (M, "S58-3.0", 550, 650),
    "M5 286": (M, "M88-3.5", 286, 340), "M5 3.6 315": (M, "S38-3.6", 315, 360), "M5 3.8 340": (M, "S38-3.8", 340, 400),
    "M5 400": (M, "S62-5.0", 400, 500), "M5 507": (M, "S85-5.0", 507, 520), "M5 560": (M, "S63-4.4", 560, 680),
    "M5 Competition 575": (M, "S63-4.4", 575, 680), "M5 30 Jahre 600": (M, "S63-4.4", 600, 700),
    "M5 600": (M, "S63-4.4", 600, 750), "M5 Competition 625": (M, "S63-4.4", 625, 750), "M5 CS 635": (M, "S63-4.4", 635, 750),
    "M5 727": (M, "S68-4.4", 727, 1000), "M6 507": (M, "S85-5.0", 507, 520), "M6 560": (M, "S63-4.4", 560, 680),
    "M6 Competition 575": (M, "S63-4.4", 575, 680), "M6 Competition 600": (M, "S63-4.4", 600, 700),
    "M8 600": (M, "S63-4.4", 600, 750), "M8 Competition 625": (M, "S63-4.4", 625, 750),
    "X3 M 480": (M, "S58-3.0", 480, 600), "X3 M Competition 510": (M, "S58-3.0", 510, 600),
    "X4 M 480": (M, "S58-3.0", 480, 600), "X4 M Competition 510": (M, "S58-3.0", 510, 600),
    "X5 M 555": (M, "S63-4.4", 555, 680), "X5 M 575": (M, "S63-4.4", 575, 750),
    "X5 M Competition 625": (M, "S63-4.4", 625, 750), "X5 M Competition 625 mhev": (M, "S68-4.4", 625, 750),
    "X6 M 555": (M, "S63-4.4", 555, 680), "X6 M 575": (M, "S63-4.4", 575, 750),
    "X6 M Competition 625": (M, "S63-4.4", 625, 750), "X6 M Competition 625 mhev": (M, "S68-4.4", 625, 750),
    "XM 653": (M, "S68-4.4", 653, 800), "XM Label 748": (M, "S68-4.4", 748, 1000),
    "Z4 M 343": (M, "S54-3.2", 343, 365), "M Roadster 321": (M, "S50-3.2", 321, 350),
    "M Roadster 325": (M, "S54-3.2", 325, 350),
}
# ères : E21/E12 (M10) ; E36 et E34/E32 phase 2 (M50/M60) ; M5X (M52/M54) ; N54 (E8x/E9x) ; F (N13/N20/N47/N55) ; G (B3x/B4x/B5x)
ERES = {"E21": "E21", "E12": "E21", "E36": "E36", ("E34", "2"): "E36", "E32": "E36",
        "E46": "M5X", "E39": "M5X", "E38": "M5X", "E53": "M5X", ("E60", "1"): "M5X", "E36/7": "M5X", "E85": "M5X",
        "E87": "N54", "E82": "N54", "E90": "N54", "E71": "N54", "E89": "N54", "E84": "N54",
        "F10": "F", ("F20", "1"): "F", ("F30", "1"): "F", ("F22", "1"): "F", ("F32", "1"): "F", "F25": "F", "F26": "F",
        "F15": "F", "F16": "F", "F12": "F", ("F01", "2"): "F",
        ("F20", "2"): "G", ("F30", "2"): "G", ("F22", "2"): "G", ("F32", "2"): "G", "F45": "G", "F48": "G", "F39": "G",
        "F40": "G", "F44": "G", "F70": "G", "G20": "G", "G22": "G", "G42": "G", "G30": "G", "G60": "G", "G11": "G",
        "G70": "G", "G32": "G", "G15": "G", "G01": "G", "G02": "G", "G45": "G", "G05": "G", "G06": "G", "G07": "G",
        "G29": "G", "U06": "G", "U11": "G", "U10": "G"}
TABLE["525i 192"] = ("M54-2.5", 192, 245)
TABLE["530i 231"] = ("M54-3.0", 231, 300)

MOT = Motorisations(B, FAMILLES, TABLE, ERES, prefixes=())
MOT.lier(L)
MOT.lier(LM)

DETAIL = {"BMW": L, "BMW M": LM}
MOTEURS = MOT.moteurs()
