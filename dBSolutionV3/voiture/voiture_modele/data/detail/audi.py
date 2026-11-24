"""Audi, Audi S et Audi RS : générations, phases (2 = restylage), motorisations (marché européen) et moteurs liés.
A1, A2, A3, A4, A5, A6, A7, A8, TT, R8, Q2, Q3, Q4 e-tron, Q5, Q6 e-tron, Q7, Q8, e-tron / Q8 e-tron, A6 e-tron,
e-tron GT ; versions S et RS dans les marques « Audi S » et « Audi RS ».
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom.
Carrosseries (Sportback, Avant, Cabriolet, berline) indiquées en remarque."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


FAMILLES = {
    # --- essence 3/4/5 cylindres
    "EA827-1.6": f("ATM", E_, 1.6, B, 4, 5600, 3800, "5W40", 4.0, 15000),
    "EA827-1.8": f("ATM", E_, 1.8, B, 4, 6000, 3500, "5W40", 4.0, 15000),
    "EA827-2.0": f("ATM", E_, 2.0, B, 4, 5400, 3200, "5W40", 4.0, 15000),
    "EA827-1.8T": f("TURBO", E_, 1.8, B, 4, 5700, 1750, "5W40", 4.5, 15000),
    "EA111-1.4": f("ATM", E_, 1.4, B, 4, 5000, 3800, "5W40", 3.5, 15000),
    "EA111-1.2TFSI": f("TURBO", E_, 1.2, C, 4, 4800, 1500, "5W40", 3.6, 15000),
    "EA111-1.4TFSI": f("TURBO", E_, 1.4, C, 4, 5000, 1500, "5W40", 3.6, 15000),
    "EA113-1.6FSI": f("ATM", E_, 1.6, B, 4, 5800, 4000, "5W40", 4.5, 15000),
    "EA113-2.0FSI": f("ATM", E_, 2.0, B, 4, 6000, 3500, "5W40", 4.6, 15000),
    "EA113-2.0TFSI": f("TURBO", E_, 2.0, B, 4, 5100, 1800, "5W40", 4.6, 15000),
    "EA211-1.0TFSI": f("TURBO", E_, 1.0, B, 3, 5000, 2000, "0W20", 4.0, 30000),
    "EA211-1.2TFSI": f("TURBO", E_, 1.2, B, 4, 4500, 1400, "5W30", 4.0, 30000),
    "EA211-1.4TFSI": f("TURBO", E_, 1.4, B, 4, 5000, 1500, "5W30", 4.0, 30000),
    "EA211-1.5TFSI": f("TURBO", E_, 1.5, B, 4, 5000, 1500, "0W20", 4.0, 30000),
    "EA211-1.5MHEV": f("HYB_TE", E_, 1.5, B, 4, 5000, 1500, "0W20", 4.0, 30000),
    "EA211-1.4PHEV": f("HYB_TE", E_, 1.4, B, 4, 5000, 1600, "0W20", 4.0, 30000),
    "EA211-1.5PHEV": f("HYB_TE", E_, 1.5, B, 4, 5000, 1500, "0W20", 4.0, 30000),
    "EA888-1.8TFSI": f("TURBO", E_, 1.8, C, 4, 5100, 1500, "5W30", 4.6, 30000),
    "EA888-2.0TFSI": f("TURBO", E_, 2.0, C, 4, 5000, 1600, "0W20", 5.7, 30000),
    "EA888-2.0MHEV": f("HYB_TE", E_, 2.0, C, 4, 5000, 1600, "0W20", 5.7, 30000),
    "EA888-2.0PHEV": f("HYB_TE", E_, 2.0, C, 4, 5000, 1600, "0W20", 5.7, 30000),
    "EA888-2.0S": f("TURBO", E_, 2.0, C, 4, 6200, 2100, "0W30", 5.7, 15000),
    "5C-2.2T": f("TURBO", E_, 2.2, B, 5, 5900, 1950, "10W40", 5.0, 15000),
    "EA855-2.5TFSI": f("TURBO", E_, 2.5, B, 5, 6000, 1950, "0W40", 6.3, 15000),
    # --- V6 / V8 / V10 / W12
    "V6-2.4": f("ATM", E_, 2.4, B, 6, 6000, 3200, "5W40", 6.0, 15000, a="V"),
    "V6-2.6": f("ATM", E_, 2.6, B, 6, 5750, 3500, "5W40", 6.0, 15000, a="V"),
    "V6-2.8": f("ATM", E_, 2.8, B, 6, 6000, 3200, "5W40", 6.0, 15000, a="V"),
    "V6-2.7T": f("TURBO", E_, 2.7, B, 6, 5800, 1800, "5W40", 6.5, 15000, a="V"),
    "V6-3.0": f("ATM", E_, 3.0, C, 6, 6300, 3200, "5W40", 6.5, 15000, a="V"),
    "VR6-3.2": f("ATM", E_, 3.2, C, 6, 6300, 2800, "5W40", 6.0, 15000, a="VR"),
    "EA837-2.8FSI": f("ATM", E_, 2.8, C, 6, 5500, 3000, "5W30", 6.5, 30000, a="V"),
    "EA837-3.2FSI": f("ATM", E_, 3.2, C, 6, 6500, 3000, "5W30", 6.5, 30000, a="V"),
    "EA837-3.0TFSI": f("TURBO", E_, 3.0, C, 6, 5500, 2900, "5W30", 6.5, 30000, a="V"),
    "EA839-3.0TFSI": f("TURBO", E_, 3.0, C, 6, 5400, 1370, "0W20", 6.8, 30000, a="V"),
    "EA839-3.0PHEV": f("HYB_TE", E_, 3.0, C, 6, 5300, 1370, "0W20", 6.8, 30000, a="V"),
    "EA839-2.9TFSI": f("TURBO", E_, 2.9, C, 6, 6500, 1900, "0W40", 6.8, 15000, a="V"),
    "EA839-2.9PHEV": f("HYB_TE", E_, 2.9, C, 6, 6500, 1900, "0W40", 6.8, 15000, a="V"),
    "V8-3.6": f("ATM", E_, 3.6, B, 8, 5800, 4000, "10W40", 8.0, 15000, a="V"),
    "V8-3.7": f("ATM", E_, 3.7, B, 8, 6000, 4000, "5W40", 8.0, 15000, a="V"),
    "V8-4.2": f("ATM", E_, 4.2, B, 8, 6200, 3000, "5W40", 8.0, 15000, a="V"),
    "V8-4.2FSI": f("ATM", E_, 4.2, C, 8, 7000, 3500, "5W40", 8.0, 15000, a="V"),
    "V8-4.0TFSI": f("TURBO", E_, 4.0, C, 8, 6000, 2000, "0W40", 9.0, 15000, a="V"),
    "V8-4.0PHEV": f("HYB_TE", E_, 4.0, C, 8, 6000, 2000, "0W40", 9.0, 15000, a="V"),
    "V10-5.2FSI": f("ATM", E_, 5.2, C, 10, 8000, 6500, "0W40", 9.0, 15000, a="V"),
    "V10-5.0TFSI": f("TURBO", E_, 5.0, C, 10, 6250, 1500, "5W40", 9.0, 15000, a="V"),
    "W12-6.0": f("ATM", E_, 6.0, C, 12, 6200, 4000, "5W40", 11.0, 15000, a="W"),
    "W12-6.3": f("ATM", E_, 6.3, C, 12, 6200, 4750, "5W40", 11.0, 15000, a="W"),
    # --- diesel
    "TDI-1.2": f("TURBO", D, 1.2, B, 3, 4000, 1800, "5W30", 3.6, 15000),
    "TDI-1.4": f("TURBO", D, 1.4, B, 3, 4000, 1800, "5W30", 3.6, 15000),
    "5C-2.5TDI": f("TURBO", D, 2.5, B, 5, 4000, 1900, "10W40", 6.0, 15000),
    "EA188-1.9TDI": f("TURBO", D, 1.9, B, 4, 4000, 1900, "5W40", 4.3, 15000),
    "EA188-2.0TDI": f("TURBO", D, 2.0, B, 4, 4000, 1750, "5W40", 4.3, 15000),
    "EA189-1.6TDI": f("TURBO", D, 1.6, B, 4, 4400, 1500, "5W30", 4.3, 30000),
    "EA189-2.0TDI": f("TURBO", D, 2.0, B, 4, 4200, 1750, "5W30", 4.3, 30000),
    "EA288-1.6TDI": f("TURBO", D, 1.6, B, 4, 4000, 1500, "0W30", 4.3, 30000),
    "EA288-2.0TDI": f("TURBO", D, 2.0, B, 4, 3800, 1750, "0W30", 4.3, 30000),
    "EA288-2.0MHEV": f("TURBO", D, 2.0, B, 4, 3800, 1750, "0W30", 4.3, 30000),
    "V6-2.5TDI": f("TURBO", D, 2.5, B, 6, 4000, 1500, "5W40", 7.0, 15000, a="V"),
    "V6-2.7TDI": f("TURBO", D, 2.7, C, 6, 3900, 1400, "5W30", 7.5, 30000, a="V"),
    "V6-3.0TDI": f("TURBO", D, 3.0, C, 6, 4000, 1500, "0W30", 7.5, 30000, a="V"),
    "V6-3.0TDI-MHEV": f("TURBO", D, 3.0, C, 6, 3750, 1500, "0W30", 7.5, 30000, a="V"),
    "V6-3.3TDI": f("TURBO", D, 3.3, C, 8, 4000, 1800, "5W40", 9.0, 15000, a="V"),
    "V8-4.0TDI": f("TURBO", D, 4.0, C, 8, 3750, 1250, "0W30", 9.0, 30000, a="V"),
    "V8-4.2TDI": f("TURBO", D, 4.2, C, 8, 3750, 1750, "5W30", 9.0, 30000, a="V"),
    "V12-6.0TDI": f("TURBO", D, 6.0, C, 12, 3750, 1750, "5W30", 12.0, 30000, a="V"),
    # --- électriques
    "MLB-EV": electrique(), "MEB-EV": electrique(), "PPE-EV": electrique(), "J1-EV": electrique(),
}

mg = SaisieMoteurs(FAMILLES, "Audi")
L, LS, LR = [], [], []   # Audi, Audi S, Audi RS

# ---------------------------------------------------------------- A1 / A2
mg(L, "A1", "8X", "1", "2010-08", "2014-10",
   [("1.2 TFSI 86", "EA111-1.2TFSI", 160), ("1.4 TFSI 122", "EA111-1.4TFSI", 200), ("1.4 TFSI 185", "EA111-1.4TFSI", 250, {"debut": "2011-03"}),
    ("1.6 TDI 90", "EA189-1.6TDI", 230), ("1.6 TDI 105", "EA189-1.6TDI", 250), ("2.0 TDI 143", "EA189-2.0TDI", 320, {"debut": "2011-09"})],
   portes=3, places=4, reservoir=45, remarques="3 portes et Sportback 5 portes (2011)")
mg(L, "A1", "8X", "2", "2014-11", "2018-06",
   [("1.0 TFSI 95", "EA211-1.0TFSI", 160), ("1.4 TFSI 125", "EA211-1.4TFSI", 200), ("1.4 TFSI COD 150", "EA211-1.4TFSI", 250),
    ("1.8 TFSI 192", "EA888-1.8TFSI", 250), ("1.4 TDI 90", "TDI-1.4", 230), ("1.6 TDI 116", "EA288-1.6TDI", 250)],
   portes=3, places=4, reservoir=45, remarques="3 portes et Sportback")
mg(L, "A1", "GB", "1", "2018-07", None,
   [("25 TFSI 95", "EA211-1.0TFSI", 175), ("30 TFSI 116", "EA211-1.0TFSI", 200), ("35 TFSI 150", "EA211-1.5TFSI", 250),
    ("40 TFSI 200", "EA888-2.0TFSI", 320, {"fin": "2023-12"})], reservoir=40, remarques="Sportback et citycarver")
mg(L, "A2", "8Z", "1", "1999-11", "2005-08",
   [("1.4 75", "EA111-1.4", 126), ("1.6 FSI 110", "EA111-1.4", 155, {"debut": "2002-06"}), ("1.2 TDI 61", "TDI-1.2", 140),
    ("1.4 TDI 75", "TDI-1.4", 195), ("1.4 TDI 90", "TDI-1.4", 230, {"debut": "2003-09"})], reservoir=42,
   remarques="Monospace compact en aluminium ; A2 e-tron électrique annoncée (livraisons 2027)")

# ---------------------------------------------------------------- A3
mg(L, "A3", "8L", "1", "1996-09", "2003-05",
   [("1.6 101", "EA827-1.6", 145), ("1.8 125", "EA827-1.8", 170), ("1.8 T 150", "EA827-1.8T", 210), ("1.8 T 180", "EA827-1.8T", 235, {"debut": "1998-09"}),
    ("1.9 TDI 90", "EA188-1.9TDI", 210), ("1.9 TDI 110", "EA188-1.9TDI", 235), ("1.9 TDI 130", "EA188-1.9TDI", 310, {"debut": "2000-09"})],
   reservoir=55, remarques="3 et 5 portes ; restylage 2000 non détaillé")
mg(L, "A3", "8P", "1", "2003-06", "2008-04",
   [("1.6 102", "EA827-1.6", 148), ("1.6 FSI 115", "EA113-1.6FSI", 155), ("2.0 FSI 150", "EA113-2.0FSI", 200), ("2.0 TFSI 200", "EA113-2.0TFSI", 280),
    ("3.2 V6 250", "VR6-3.2", 320), ("1.4 TFSI 125", "EA111-1.4TFSI", 200, {"debut": "2007-06"}), ("1.8 TFSI 160", "EA888-1.8TFSI", 250, {"debut": "2006-09"}),
    ("1.9 TDI 105", "EA188-1.9TDI", 250), ("2.0 TDI 140", "EA188-2.0TDI", 320), ("2.0 TDI 170", "EA188-2.0TDI", 350, {"debut": "2006-09"})],
   reservoir=55, remarques="3 portes, Sportback (2004), Cabriolet (2008)")
mg(L, "A3", "8P", "2", "2008-05", "2012-07",
   [("1.2 TFSI 105", "EA111-1.2TFSI", 175, {"debut": "2010-01"}), ("1.4 TFSI 125", "EA111-1.4TFSI", 200), ("1.8 TFSI 160", "EA888-1.8TFSI", 250),
    ("2.0 TFSI 200", "EA888-2.0TFSI", 280), ("3.2 V6 250", "VR6-3.2", 320), ("1.6 TDI 105", "EA189-1.6TDI", 250, {"debut": "2009-06"}),
    ("1.9 TDI 105", "EA188-1.9TDI", 250, {"fin": "2009-05"}), ("2.0 TDI 140", "EA189-2.0TDI", 320), ("2.0 TDI 170", "EA189-2.0TDI", 350)],
   reservoir=55, remarques="3 portes, Sportback, Cabriolet")
mg(L, "A3", "8V", "1", "2012-08", "2016-08",
   [("1.2 TFSI 105", "EA211-1.2TFSI", 175), ("1.4 TFSI 122", "EA211-1.4TFSI", 200), ("1.4 TFSI COD 140", "EA211-1.4TFSI", 250),
    ("1.8 TFSI 180", "EA888-1.8TFSI", 250), ("1.4 TFSI e-tron 204", "EA211-1.4PHEV", 350, ph(9, 40, debut="2014-09")),
    ("1.6 TDI 105", "EA288-1.6TDI", 250), ("2.0 TDI 150", "EA288-2.0TDI", 320), ("2.0 TDI 184", "EA288-2.0TDI", 380)],
   reservoir=50, remarques="3 portes, Sportback, Berline (2013), Cabriolet (2014)")
mg(L, "A3", "8V", "2", "2016-09", "2020-03",
   [("1.0 TFSI 116", "EA211-1.0TFSI", 200), ("1.5 TFSI 150", "EA211-1.5TFSI", 250), ("2.0 TFSI 190", "EA888-2.0TFSI", 320),
    ("1.4 TFSI e-tron 204", "EA211-1.4PHEV", 350, ph(9, 40, fin="2018-08")), ("1.6 TDI 116", "EA288-1.6TDI", 250),
    ("2.0 TDI 150", "EA288-2.0TDI", 340), ("2.0 TDI 184", "EA288-2.0TDI", 380, {"fin": "2018-08"})], reservoir=50,
   remarques="3 portes, Sportback, Berline, Cabriolet ; dénominations 30/35/40 à partir de 2018")
mg(L, "A3", "8Y", "1", "2020-04", "2024-06",
   [("30 TFSI 110", "EA211-1.0TFSI", 200), ("35 TFSI 150", "EA211-1.5TFSI", 250), ("35 TFSI S tronic 150", "EA211-1.5MHEV", 250),
    ("40 TFSI e 204", "EA211-1.4PHEV", 350, ph(13, 40)), ("45 TFSI e 245", "EA211-1.4PHEV", 400, ph(13, 40)),
    ("30 TDI 116", "EA288-2.0TDI", 300), ("35 TDI 150", "EA288-2.0TDI", 360)], reservoir=50,
   remarques="Sportback, Berline ; allstreet (2022)")
mg(L, "A3", "8Y", "2", "2024-07", None,
   [("30 TFSI 116", "EA211-1.5TFSI", 220), ("35 TFSI 150", "EA211-1.5MHEV", 250), ("TFSI e 204", "EA211-1.5PHEV", 350, ph(20, 40)),
    ("TFSI e 272", "EA211-1.5PHEV", 400, ph(20, 40)), ("35 TDI 150", "EA288-2.0TDI", 360)], reservoir=50,
   remarques="Sportback, Berline, allstreet ; e-hybrid 25,7 kWh brut")

# ---------------------------------------------------------------- A4 / A5 (ancienne)
mg(L, "A4", "B5", "1", "1994-11", "2001-08",
   [("1.6 101", "EA827-1.6", 140), ("1.8 125", "EA827-1.8", 168), ("1.8 T 150", "EA827-1.8T", 210), ("2.4 V6 165", "V6-2.4", 230, {"debut": "1997-09"}),
    ("2.6 V6 150", "V6-2.6", 225, {"fin": "1997-08"}), ("2.8 V6 193", "V6-2.8", 280), ("1.9 TDI 90", "EA188-1.9TDI", 202),
    ("1.9 TDI 110", "EA188-1.9TDI", 235), ("2.5 TDI 150", "V6-2.5TDI", 310, {"debut": "1997-09"})], portes=4, reservoir=62,
   remarques="Berline et Avant ; restylage 1999 non détaillé")
mg(L, "A4", "B6", "1", "2000-11", "2004-11",
   [("1.6 102", "EA827-1.6", 148), ("2.0 130", "EA827-2.0", 195), ("2.0 FSI 150", "EA113-2.0FSI", 200, {"debut": "2002-06"}),
    ("1.8 T 150", "EA827-1.8T", 210), ("1.8 T 163", "EA827-1.8T", 225), ("3.0 V6 220", "V6-3.0", 300), ("1.9 TDI 100", "EA188-1.9TDI", 240),
    ("1.9 TDI 130", "EA188-1.9TDI", 285), ("2.5 TDI 163", "V6-2.5TDI", 350)], portes=4, reservoir=70, remarques="Berline, Avant, Cabriolet (2002)")
mg(L, "A4", "B7", "1", "2004-11", "2008-03",
   [("1.6 102", "EA827-1.6", 148), ("2.0 130", "EA827-2.0", 195), ("1.8 T 163", "EA827-1.8T", 225), ("2.0 TFSI 200", "EA113-2.0TFSI", 280),
    ("3.2 FSI 255", "EA837-3.2FSI", 330), ("1.9 TDI 115", "EA188-1.9TDI", 285), ("2.0 TDI 140", "EA188-2.0TDI", 320),
    ("2.7 TDI 180", "V6-2.7TDI", 380), ("3.0 TDI 233", "V6-3.0TDI", 450)], portes=4, reservoir=70, remarques="Berline, Avant, Cabriolet")
mg(L, "A4", "B8", "1", "2007-11", "2011-12",
   [("1.8 TFSI 120", "EA888-1.8TFSI", 230), ("1.8 TFSI 160", "EA888-1.8TFSI", 250), ("2.0 TFSI 180", "EA888-2.0TFSI", 320),
    ("2.0 TFSI 211", "EA888-2.0TFSI", 350), ("3.2 FSI 265", "EA837-3.2FSI", 330), ("2.0 TDI 120", "EA189-2.0TDI", 290),
    ("2.0 TDI 143", "EA189-2.0TDI", 320), ("2.0 TDI 170", "EA189-2.0TDI", 350), ("2.7 TDI 190", "V6-2.7TDI", 400), ("3.0 TDI 240", "V6-3.0TDI", 500)],
   portes=4, reservoir=65, remarques="Berline, Avant (2008), allroad (2009)")
mg(L, "A4", "B8", "2", "2012-01", "2015-10",
   [("1.8 TFSI 120", "EA888-1.8TFSI", 230), ("1.8 TFSI 170", "EA888-1.8TFSI", 320), ("2.0 TFSI 225", "EA888-2.0TFSI", 350),
    ("2.0 TDI 136", "EA189-2.0TDI", 320), ("2.0 TDI 150", "EA189-2.0TDI", 320), ("2.0 TDI 177", "EA189-2.0TDI", 380),
    ("3.0 TDI 204", "V6-3.0TDI", 400), ("3.0 TDI 245", "V6-3.0TDI", 500)], portes=4, reservoir=65, remarques="Berline, Avant, allroad")
mg(L, "A4", "B9", "1", "2015-11", "2019-06",
   [("1.4 TFSI 150", "EA211-1.4TFSI", 250), ("2.0 TFSI 190", "EA888-2.0TFSI", 320), ("2.0 TFSI 252", "EA888-2.0TFSI", 370),
    ("2.0 TDI 122", "EA288-2.0TDI", 290), ("2.0 TDI 150", "EA288-2.0TDI", 320), ("2.0 TDI 190", "EA288-2.0TDI", 400),
    ("3.0 TDI 218", "V6-3.0TDI", 400), ("3.0 TDI 272", "V6-3.0TDI", 600)], portes=4, reservoir=54, remarques="Berline, Avant, allroad")
mg(L, "A4", "B9", "2", "2019-07", "2024-12",
   [("35 TFSI 150", "EA888-2.0MHEV", 270), ("40 TFSI 204", "EA888-2.0MHEV", 320), ("45 TFSI 265", "EA888-2.0MHEV", 370),
    ("30 TDI 136", "EA288-2.0TDI", 320), ("35 TDI 163", "EA288-2.0MHEV", 380), ("40 TDI 204", "EA288-2.0MHEV", 400),
    ("50 TDI 286", "V6-3.0TDI-MHEV", 620)], portes=4, reservoir=54, remarques="Berline, Avant, allroad ; remplacée par l'A5 (B10)")
mg(L, "A5", "8T", "1", "2007-06", "2011-09",
   [("1.8 TFSI 160", "EA888-1.8TFSI", 250), ("2.0 TFSI 211", "EA888-2.0TFSI", 350), ("3.2 FSI 265", "EA837-3.2FSI", 330),
    ("2.0 TDI 170", "EA189-2.0TDI", 350), ("2.7 TDI 190", "V6-2.7TDI", 400), ("3.0 TDI 240", "V6-3.0TDI", 500)], portes=2, places=4,
   reservoir=64, remarques="Coupé, Cabriolet (2009), Sportback (2009)")
mg(L, "A5", "8T", "2", "2011-10", "2016-06",
   [("1.8 TFSI 170", "EA888-1.8TFSI", 320), ("2.0 TFSI 225", "EA888-2.0TFSI", 350), ("2.0 TDI 150", "EA189-2.0TDI", 320),
    ("2.0 TDI 177", "EA189-2.0TDI", 380), ("3.0 TDI 204", "V6-3.0TDI", 400), ("3.0 TDI 245", "V6-3.0TDI", 500)], portes=2, places=4,
   reservoir=64, remarques="Coupé, Cabriolet, Sportback")
mg(L, "A5", "F5", "1", "2016-07", "2019-08",
   [("2.0 TFSI 190", "EA888-2.0TFSI", 320), ("2.0 TFSI 252", "EA888-2.0TFSI", 370), ("2.0 TDI 190", "EA288-2.0TDI", 400),
    ("3.0 TDI 218", "V6-3.0TDI", 400), ("3.0 TDI 286", "V6-3.0TDI", 620)], portes=2, places=4, reservoir=54,
   remarques="Coupé, Cabriolet, Sportback")
mg(L, "A5", "F5", "2", "2019-09", "2024-06",
   [("35 TFSI 150", "EA888-2.0MHEV", 270), ("40 TFSI 204", "EA888-2.0MHEV", 320), ("45 TFSI 265", "EA888-2.0MHEV", 370),
    ("35 TDI 163", "EA288-2.0MHEV", 380), ("40 TDI 204", "EA288-2.0MHEV", 400), ("50 TDI 286", "V6-3.0TDI-MHEV", 620)], portes=2,
   places=4, reservoir=54, remarques="Coupé, Cabriolet, Sportback")
mg(L, "A5", "B10", "1", "2024-09", None,
   [("TFSI 150", "EA888-2.0TFSI", 280), ("TFSI 204", "EA888-2.0TFSI", 340), ("TFSI quattro 272", "EA888-2.0TFSI", 400),
    ("TDI 204", "EA288-2.0MHEV", 400), ("e-hybrid quattro 299", "EA888-2.0PHEV", 450, ph(20, 54, debut="2025-03")),
    ("e-hybrid quattro 367", "EA888-2.0PHEV", 500, ph(20, 54, debut="2025-03"))], portes=5, reservoir=54,
   remarques="Remplace l'A4 : berline à hayon et Avant (plateforme PPC)")

# ---------------------------------------------------------------- A6 / A7 / A8
mg(L, "A6", "C4", "1", "1994-06", "1997-03",
   [("1.8 125", "EA827-1.8", 168), ("2.0 115", "EA827-2.0", 168), ("2.6 V6 150", "V6-2.6", 225), ("2.8 V6 174", "V6-2.8", 245),
    ("1.9 TDI 90", "EA188-1.9TDI", 202), ("2.5 TDI 140", "5C-2.5TDI", 290)], portes=4, reservoir=80, remarques="Berline et Avant (ex-100)")
mg(L, "A6", "C5", "1", "1997-04", "2004-05",
   [("1.8 T 150", "EA827-1.8T", 210), ("1.8 T 180", "EA827-1.8T", 235), ("2.4 V6 165", "V6-2.4", 230), ("2.8 V6 193", "V6-2.8", 280),
    ("2.7 T 250", "V6-2.7T", 350), ("3.0 V6 220", "V6-3.0", 300, {"debut": "2001-09"}), ("4.2 V8 300", "V8-4.2", 400),
    ("1.9 TDI 110", "EA188-1.9TDI", 235), ("1.9 TDI 130", "EA188-1.9TDI", 285, {"debut": "2001-09"}),
    ("2.5 TDI 150", "V6-2.5TDI", 310), ("2.5 TDI 180", "V6-2.5TDI", 370, {"debut": "2001-09"})], portes=4, reservoir=70,
   remarques="Berline, Avant, allroad quattro (2000) ; restylage 2001")
mg(L, "A6", "C6", "1", "2004-05", "2011-03",
   [("2.0 TFSI 170", "EA113-2.0TFSI", 280), ("2.4 177", "EA837-2.8FSI", 230, {"fin": "2008-08"}), ("2.8 FSI 210", "EA837-2.8FSI", 280, {"debut": "2006-09"}),
    ("3.2 FSI 255", "EA837-3.2FSI", 330), ("3.0 TFSI 290", "EA837-3.0TFSI", 420, {"debut": "2008-09"}), ("4.2 FSI 350", "V8-4.2FSI", 440),
    ("2.0 TDI 140", "EA188-2.0TDI", 320), ("2.0 TDI 170", "EA189-2.0TDI", 350, {"debut": "2008-09"}), ("2.7 TDI 190", "V6-2.7TDI", 400),
    ("3.0 TDI 240", "V6-3.0TDI", 500)], portes=4, reservoir=80, remarques="Berline, Avant, allroad ; restylage 2008 non détaillé")
mg(L, "A6", "C7", "1", "2011-03", "2014-09",
   [("2.0 TFSI 180", "EA888-2.0TFSI", 320), ("2.8 FSI 204", "EA837-2.8FSI", 280), ("3.0 TFSI 300", "EA837-3.0TFSI", 440),
    ("2.0 TDI 177", "EA189-2.0TDI", 380), ("3.0 TDI 204", "V6-3.0TDI", 400), ("3.0 TDI 245", "V6-3.0TDI", 500),
    ("3.0 BiTDI 313", "V6-3.0TDI", 650)], portes=4, reservoir=73, remarques="Berline, Avant, allroad ; A6 hybrid (2012) non détaillée")
mg(L, "A6", "C7", "2", "2014-10", "2018-05",
   [("1.8 TFSI 190", "EA888-1.8TFSI", 320), ("2.0 TFSI 252", "EA888-2.0TFSI", 370), ("3.0 TFSI 333", "EA837-3.0TFSI", 440),
    ("2.0 TDI 150", "EA288-2.0TDI", 350), ("2.0 TDI 190", "EA288-2.0TDI", 400), ("3.0 TDI 218", "V6-3.0TDI", 500),
    ("3.0 TDI 272", "V6-3.0TDI", 580), ("3.0 BiTDI 320", "V6-3.0TDI", 650)], portes=4, reservoir=73, remarques="Berline, Avant, allroad")
mg(L, "A6", "C8", "1", "2018-06", "2025-02",
   [("40 TFSI 204", "EA888-2.0MHEV", 320), ("45 TFSI 265", "EA888-2.0MHEV", 370), ("55 TFSI 340", "EA839-3.0TFSI", 500),
    ("50 TFSI e 299", "EA888-2.0PHEV", 450, ph(14, 53, debut="2019-09")), ("55 TFSI e 367", "EA888-2.0PHEV", 500, ph(17, 53, debut="2020-09")),
    ("35 TDI 163", "EA288-2.0MHEV", 370), ("40 TDI 204", "EA288-2.0MHEV", 400), ("45 TDI 231", "V6-3.0TDI-MHEV", 500),
    ("50 TDI 286", "V6-3.0TDI-MHEV", 620)], portes=4, reservoir=63, remarques="Berline, Avant, allroad (2019)")
mg(L, "A6", "C9", "1", "2025-03", None,
   [("TFSI 204", "EA888-2.0MHEV", 340), ("TFSI quattro 367", "EA839-3.0TFSI", 550), ("TDI 204", "EA288-2.0MHEV", 400),
    ("e-hybrid quattro 299", "EA888-2.0PHEV", 450, ph(20, 55, debut="2025-09")), ("e-hybrid quattro 367", "EA888-2.0PHEV", 500, ph(20, 55, debut="2025-09"))],
   portes=4, reservoir=63, remarques="Berline et Avant (PPC) ; nouvelle A6 allroad (2026) non détaillée")
mg(L, "A6 e-tron", "PPE", "1", "2024-09", None,
   [("A6 e-tron performance 367", "PPE-EV", 565, el(95)), ("A6 e-tron quattro 428", "PPE-EV", 580, el(95, debut="2025-01")),
    ("A6 e-tron 286", "PPE-EV", 450, el(76, debut="2025-03"))], portes=5, reservoir=0,
   remarques="Sportback et Avant électriques (800 V)")
mg(L, "A7", "4G", "1", "2010-10", "2018-01",
   [("2.8 FSI 204", "EA837-2.8FSI", 280), ("3.0 TFSI 300", "EA837-3.0TFSI", 440, {"fin": "2014-09"}), ("3.0 TFSI 333", "EA837-3.0TFSI", 440, {"debut": "2014-10"}),
    ("3.0 TDI 204", "V6-3.0TDI", 400), ("3.0 TDI 245", "V6-3.0TDI", 500, {"fin": "2014-09"}), ("3.0 TDI 272", "V6-3.0TDI", 580, {"debut": "2014-10"}),
    ("3.0 BiTDI 313", "V6-3.0TDI", 650, {"fin": "2014-09"}), ("3.0 BiTDI 326", "V6-3.0TDI", 650, {"debut": "2014-10"})], portes=5,
   reservoir=73, remarques="Sportback ; restylage 2014")
mg(L, "A7", "4K", "1", "2018-02", "2025-06",
   [("45 TFSI 245", "EA888-2.0MHEV", 370), ("55 TFSI 340", "EA839-3.0TFSI", 500), ("50 TFSI e 299", "EA888-2.0PHEV", 450, ph(14, 53, debut="2019-09")),
    ("55 TFSI e 367", "EA888-2.0PHEV", 500, ph(17, 53, debut="2020-09")), ("40 TDI 204", "EA288-2.0MHEV", 400),
    ("45 TDI 231", "V6-3.0TDI-MHEV", 500), ("50 TDI 286", "V6-3.0TDI-MHEV", 620)], portes=5, reservoir=63, remarques="Sportback")
mg(L, "A8", "D2", "1", "1994-03", "2002-09",
   [("2.8 V6 193", "V6-2.8", 280), ("3.7 V8 230", "V8-3.7", 315), ("4.2 V8 300", "V8-4.2", 400), ("6.0 W12 420", "W12-6.0", 550, {"debut": "2001-01"}),
    ("2.5 TDI 150", "V6-2.5TDI", 310, {"debut": "1997-09"}), ("3.3 TDI 225", "V6-3.3TDI", 480, {"debut": "1999-09"})], portes=4,
   reservoir=90, remarques="Berline aluminium et version longue")
mg(L, "A8", "D3", "1", "2002-10", "2010-01",
   [("3.0 V6 220", "V6-3.0", 300), ("3.2 FSI 260", "EA837-3.2FSI", 330), ("3.7 V8 280", "V8-3.7", 360), ("4.2 V8 335", "V8-4.2", 430),
    ("4.2 FSI 350", "V8-4.2FSI", 440, {"debut": "2006-09"}), ("6.0 W12 450", "W12-6.0", 580), ("3.0 TDI 233", "V6-3.0TDI", 450),
    ("4.0 TDI 275", "V8-4.0TDI", 650, {"fin": "2005-08"}), ("4.2 TDI 326", "V8-4.2TDI", 650, {"debut": "2005-09"})], portes=4,
   reservoir=90, remarques="Berline et version longue")
mg(L, "A8", "D4", "1", "2010-02", "2017-10",
   [("3.0 TFSI 290", "EA837-3.0TFSI", 420), ("3.0 TFSI 310", "EA837-3.0TFSI", 440, {"debut": "2013-09"}), ("4.2 FSI 372", "V8-4.2FSI", 445),
    ("4.0 TFSI 435", "V8-4.0TFSI", 600, {"debut": "2013-09"}), ("6.3 W12 500", "W12-6.3", 625), ("3.0 TDI 250", "V6-3.0TDI", 550),
    ("3.0 TDI 258", "V6-3.0TDI", 580, {"debut": "2013-09"}), ("4.2 TDI 350", "V8-4.2TDI", 800), ("4.2 TDI 385", "V8-4.2TDI", 850, {"debut": "2013-09"}),
    ("hybrid 245", "EA888-2.0PHEV", 480, {"debut": "2012-03", "batterie": 1})], portes=4, reservoir=90,
   remarques="Berline et version longue ; restylage 2013")
mg(L, "A8", "D5", "1", "2017-11", None,
   [("50 TDI 286", "V6-3.0TDI-MHEV", 600), ("55 TFSI 340", "EA839-3.0TFSI", 500), ("60 TFSI 460", "V8-4.0TFSI", 660, {"debut": "2019-01"}),
    ("60 TFSI e 449", "EA839-3.0PHEV", 700, ph(18, 72, debut="2019-09"))], portes=4, reservoir=72,
   remarques="Berline et version longue ; restylage 2021 non détaillé")

# ---------------------------------------------------------------- TT / R8
mg(L, "TT", "8N", "1", "1998-09", "2006-06",
   [("1.8 T 150", "EA827-1.8T", 210, {"debut": "2000-01"}), ("1.8 T 180", "EA827-1.8T", 235), ("1.8 T quattro 225", "EA827-1.8T", 280),
    ("3.2 V6 250", "VR6-3.2", 320, {"debut": "2003-04"})], portes=2, places=4, reservoir=55, remarques="Coupé 2+2 et Roadster (1999)")
mg(L, "TT", "8J", "1", "2006-08", "2014-06",
   [("1.8 TFSI 160", "EA888-1.8TFSI", 250, {"debut": "2008-01"}), ("2.0 TFSI 200", "EA113-2.0TFSI", 280, {"fin": "2010-05"}),
    ("2.0 TFSI 211", "EA888-2.0TFSI", 350, {"debut": "2010-06"}), ("3.2 V6 250", "VR6-3.2", 320, {"fin": "2010-05"}),
    ("2.0 TDI 170", "EA189-2.0TDI", 350, {"debut": "2008-06"})], portes=2, places=4, reservoir=60, remarques="Coupé et Roadster")
mg(L, "TT", "8S", "1", "2014-09", "2023-11",
   [("1.8 TFSI 180", "EA888-1.8TFSI", 250, {"fin": "2018-08"}), ("2.0 TFSI 230", "EA888-2.0TFSI", 370, {"fin": "2018-08"}),
    ("40 TFSI 197", "EA888-2.0TFSI", 320, {"debut": "2018-09"}), ("45 TFSI 245", "EA888-2.0TFSI", 370, {"debut": "2018-09"}),
    ("2.0 TDI 184", "EA288-2.0TDI", 380, {"fin": "2018-08"})], portes=2, places=4, reservoir=50, remarques="Coupé et Roadster ; restylage 2018")
mg(L, "R8", "42", "1", "2007-04", "2015-03",
   [("4.2 FSI 420", "V8-4.2FSI", 430, {"fin": "2012-08"}), ("4.2 FSI 430", "V8-4.2FSI", 430, {"debut": "2012-09"}),
    ("5.2 V10 525", "V10-5.2FSI", 530, {"debut": "2009-03"}), ("5.2 V10 plus 550", "V10-5.2FSI", 540, {"debut": "2012-09"})],
   portes=2, places=2, reservoir=90, remarques="Coupé et Spyder (2010) à moteur central")
mg(L, "R8", "4S", "1", "2015-03", "2024-03",
   [("V10 540", "V10-5.2FSI", 540), ("V10 plus 610", "V10-5.2FSI", 560), ("V10 performance 620", "V10-5.2FSI", 580, {"debut": "2019-01"}),
    ("V10 performance RWD 570", "V10-5.2FSI", 550, {"debut": "2021-06"}), ("GT 620", "V10-5.2FSI", 565, {"debut": "2022-11"})],
   portes=2, places=2, reservoir=73, remarques="Coupé et Spyder ; restylage 2019 ; fin de production mars 2024")

# ---------------------------------------------------------------- Q2 / Q3 / Q4
mg(L, "Q2", "GA", "1", "2016-09", "2020-09",
   [("1.0 TFSI 116", "EA211-1.0TFSI", 200), ("1.4 TFSI 150", "EA211-1.4TFSI", 250), ("1.5 TFSI 150", "EA211-1.5TFSI", 250, {"debut": "2018-06"}),
    ("2.0 TFSI 190", "EA888-2.0TFSI", 320), ("1.6 TDI 116", "EA288-1.6TDI", 250), ("2.0 TDI 150", "EA288-2.0TDI", 340),
    ("2.0 TDI 190", "EA288-2.0TDI", 400)], reservoir=50, remarques="SUV urbain")
mg(L, "Q2", "GA", "2", "2020-10", None,
   [("30 TFSI 110", "EA211-1.0TFSI", 200), ("35 TFSI 150", "EA211-1.5TFSI", 250), ("30 TDI 116", "EA288-2.0TDI", 300),
    ("35 TDI 150", "EA288-2.0TDI", 340)], reservoir=50, remarques="SUV urbain restylé")
mg(L, "Q3", "8U", "1", "2011-06", "2018-08",
   [("1.4 TFSI 150", "EA211-1.4TFSI", 250, {"debut": "2013-09"}), ("2.0 TFSI 170", "EA888-2.0TFSI", 280), ("2.0 TFSI 180", "EA888-2.0TFSI", 320, {"debut": "2014-09"}),
    ("2.0 TFSI 220", "EA888-2.0TFSI", 350, {"debut": "2014-09"}), ("2.0 TDI 140", "EA189-2.0TDI", 320, {"fin": "2014-08"}),
    ("2.0 TDI 177", "EA189-2.0TDI", 380, {"fin": "2014-08"}), ("2.0 TDI 150", "EA288-2.0TDI", 340, {"debut": "2014-09"}),
    ("2.0 TDI 184", "EA288-2.0TDI", 380, {"debut": "2014-09"})], reservoir=64, remarques="SUV compact ; restylage 2014")
mg(L, "Q3", "F3", "1", "2018-09", "2025-09",
   [("35 TFSI 150", "EA211-1.5TFSI", 250), ("40 TFSI 190", "EA888-2.0TFSI", 320), ("45 TFSI 230", "EA888-2.0TFSI", 350),
    ("45 TFSI e 245", "EA211-1.4PHEV", 400, ph(13, 45, debut="2021-03")), ("35 TDI 150", "EA288-2.0TDI", 340),
    ("40 TDI 200", "EA288-2.0TDI", 400)], reservoir=60, remarques="SUV et Sportback (2019)")
mg(L, "Q3", "F3-III", "1", "2025-10", None,
   [("TFSI 150", "EA211-1.5MHEV", 250), ("TFSI quattro 265", "EA888-2.0TFSI", 400), ("e-hybrid 272", "EA211-1.5PHEV", 400, ph(20, 55)),
    ("TDI 150", "EA288-2.0TDI", 360)], reservoir=58, remarques="3e génération (code indicatif), SUV et Sportback")
mg(L, "Q4 e-tron", "FZ", "1", "2021-06", "2026-05",
   [("35 e-tron 170", "MEB-EV", 310, el(52)), ("40 e-tron 204", "MEB-EV", 310, el(77)), ("45 e-tron quattro 265", "MEB-EV", 425, el(77)),
    ("50 e-tron quattro 299", "MEB-EV", 460, el(77)), ("45 e-tron 286", "MEB-EV", 545, el(77, debut="2023-09")),
    ("55 e-tron quattro 340", "MEB-EV", 679, el(77, debut="2023-09"))], reservoir=0, remarques="SUV et Sportback électriques")
mg(L, "Q4 e-tron", "FZ", "2", "2026-06", None,
   [("Q4 e-tron 204", "MEB-EV", 310, el(59)), ("Q4 e-tron 286", "MEB-EV", 545, el(77)), ("Q4 e-tron quattro performance 340", "MEB-EV", 679, el(77))],
   reservoir=0, remarques="Restylage 2026 (puissances indicatives)")

# ---------------------------------------------------------------- Q5 / Q6 / Q7 / Q8 / e-tron
mg(L, "Q5", "8R", "1", "2008-11", "2012-06",
   [("2.0 TFSI 180", "EA888-2.0TFSI", 320), ("2.0 TFSI 211", "EA888-2.0TFSI", 350), ("3.2 FSI 270", "EA837-3.2FSI", 330),
    ("2.0 TDI 143", "EA189-2.0TDI", 320), ("2.0 TDI 170", "EA189-2.0TDI", 350), ("3.0 TDI 240", "V6-3.0TDI", 500)], reservoir=75)
mg(L, "Q5", "8R", "2", "2012-07", "2016-12",
   [("2.0 TFSI 180", "EA888-2.0TFSI", 320), ("2.0 TFSI 225", "EA888-2.0TFSI", 350), ("3.0 TFSI 272", "EA837-3.0TFSI", 400),
    ("hybrid 245", "EA888-2.0PHEV", 480, {"batterie": 1}), ("2.0 TDI 150", "EA189-2.0TDI", 320), ("2.0 TDI 177", "EA189-2.0TDI", 380),
    ("3.0 TDI 245", "V6-3.0TDI", 580), ("3.0 TDI 258", "V6-3.0TDI", 580, {"debut": "2014-09"})], reservoir=75)
mg(L, "Q5", "FY", "1", "2016-12", "2020-08",
   [("2.0 TFSI 252", "EA888-2.0TFSI", 370), ("2.0 TDI 150", "EA288-2.0TDI", 320), ("2.0 TDI 190", "EA288-2.0TDI", 400),
    ("3.0 TDI 286", "V6-3.0TDI", 620), ("55 TFSI e 367", "EA888-2.0PHEV", 500, ph(14, 55, debut="2019-09"))], reservoir=70,
   remarques="SUV")
mg(L, "Q5", "FY", "2", "2020-09", "2024-11",
   [("40 TFSI 204", "EA888-2.0MHEV", 320), ("45 TFSI 265", "EA888-2.0MHEV", 370), ("50 TFSI e 299", "EA888-2.0PHEV", 450, ph(17, 55)),
    ("55 TFSI e 367", "EA888-2.0PHEV", 500, ph(17, 55)), ("35 TDI 163", "EA288-2.0MHEV", 370), ("40 TDI 204", "EA288-2.0MHEV", 400),
    ("50 TDI 286", "V6-3.0TDI-MHEV", 620)], reservoir=70, remarques="SUV et Sportback (2021)")
mg(L, "Q5", "GU", "1", "2024-12", None,
   [("TFSI 204", "EA888-2.0MHEV", 340), ("TDI 204", "EA288-2.0MHEV", 400), ("e-hybrid quattro 299", "EA888-2.0PHEV", 450, ph(20, 60, debut="2025-06")),
    ("e-hybrid quattro 367", "EA888-2.0PHEV", 500, ph(20, 60, debut="2025-06"))], reservoir=65,
   remarques="3e génération (PPC) : SUV et Sportback ; code de série indicatif")
mg(L, "Q6 e-tron", "PPE", "1", "2024-06", None,
   [("Q6 e-tron 252", "PPE-EV", 450, el(75, debut="2024-11")), ("Q6 e-tron performance 326", "PPE-EV", 485, el(95, debut="2024-11")),
    ("Q6 e-tron quattro 387", "PPE-EV", 580, el(95))], reservoir=0, remarques="SUV et Sportback (2024) électriques, 800 V")
mg(L, "Q7", "4L", "1", "2006-03", "2015-05",
   [("3.6 FSI 280", "VR6-3.2", 360), ("4.2 FSI 350", "V8-4.2FSI", 440), ("3.0 TFSI 272", "EA837-3.0TFSI", 400, {"debut": "2010-06"}),
    ("3.0 TDI 233", "V6-3.0TDI", 500, {"fin": "2010-05"}), ("3.0 TDI 245", "V6-3.0TDI", 550, {"debut": "2010-06"}),
    ("4.2 TDI 326", "V8-4.2TDI", 760), ("6.0 V12 TDI 500", "V12-6.0TDI", 1000, {"debut": "2008-09", "fin": "2012-08"})], places=7,
   reservoir=100, remarques="SUV 5 ou 7 places")
mg(L, "Q7", "4M", "1", "2015-06", "2019-08",
   [("3.0 TFSI 333", "EA837-3.0TFSI", 440), ("3.0 TDI 218", "V6-3.0TDI", 500), ("3.0 TDI 272", "V6-3.0TDI", 600),
    ("e-tron 3.0 TDI 373", "V6-3.0TDI", 700, {"debut": "2016-03", "batterie": 17})], places=7, reservoir=85, remarques="SUV 5 ou 7 places")
mg(L, "Q7", "4M", "2", "2019-09", None,
   [("45 TDI 231", "V6-3.0TDI-MHEV", 500), ("50 TDI 286", "V6-3.0TDI-MHEV", 600), ("55 TFSI 340", "EA839-3.0TFSI", 500),
    ("55 TFSI e 381", "EA839-3.0PHEV", 600, ph(17, 75)), ("60 TFSI e 456", "EA839-3.0PHEV", 700, ph(17, 75))], places=7, reservoir=85,
   remarques="SUV 5 ou 7 places ; nouveau Q7 présenté en 2026 non détaillé")
mg(L, "Q8", "4M", "1", "2018-08", "2023-08",
   [("45 TDI 231", "V6-3.0TDI-MHEV", 500), ("50 TDI 286", "V6-3.0TDI-MHEV", 600), ("55 TFSI 340", "EA839-3.0TFSI", 500),
    ("60 TFSI e 462", "EA839-3.0PHEV", 700, ph(17, 75, debut="2020-09"))], reservoir=85, remarques="SUV coupé")
mg(L, "Q8", "4M", "2", "2023-09", None,
   [("50 TDI 286", "V6-3.0TDI-MHEV", 600), ("55 TFSI 340", "EA839-3.0TFSI", 500), ("60 TFSI e 490", "EA839-3.0PHEV", 700, ph(26, 75))],
   reservoir=85, remarques="SUV coupé restylé")
mg(L, "e-tron", "GE", "1", "2019-03", "2022-12",
   [("50 quattro 313", "MLB-EV", 540, el(64)), ("55 quattro 408", "MLB-EV", 664, el(86))], reservoir=0,
   remarques="SUV et Sportback (2020) électriques")
mg(L, "Q8 e-tron", "GE", "2", "2023-01", "2025-02",
   [("50 quattro 340", "MLB-EV", 664, el(89)), ("55 quattro 408", "MLB-EV", 664, el(106))], reservoir=0,
   remarques="Ex-e-tron restylé et renommé ; SUV et Sportback")
mg(L, "e-tron GT", "J1", "1", "2021-03", "2024-04", [("e-tron GT quattro 530", "J1-EV", 640, el(84))], portes=4, places=4,
   reservoir=0, remarques="Grand Tourisme électrique (base Porsche Taycan) ; puissance avec overboost")
mg(L, "e-tron GT", "J1", "2", "2024-05", None, [("e-tron GT quattro 585", "J1-EV", 740, el(97))], portes=4, places=4,
   reservoir=0, remarques="Restylage : batterie 105 kWh brut")

# ---------------------------------------------------------------- Audi S
mg(LS, "S1", "8X", "2", "2014-05", "2018-06", [("S1 231", "EA888-2.0TFSI", 370)], portes=3, places=4, reservoir=40,
   remarques="3 portes et Sportback, quattro")
mg(LS, "S2", "B3", "1", "1991-01", "1995-12", [("S2 220", "5C-2.2T", 309, {"fin": "1992-12"}), ("S2 230", "5C-2.2T", 350, {"debut": "1993-01"})],
   portes=2, places=4, reservoir=70, remarques="Coupé, Avant et berline (1993)")
mg(LS, "S3", "8L", "1", "1999-01", "2003-05", [("S3 210", "EA827-1.8T", 270, {"fin": "2001-06"}), ("S3 225", "EA827-1.8T", 280, {"debut": "2001-07"})],
   portes=3, reservoir=55)
mg(LS, "S3", "8P", "1", "2006-09", "2012-07", [("S3 265", "EA113-2.0TFSI", 350)], portes=3, reservoir=55, remarques="3 portes et Sportback")
mg(LS, "S3", "8V", "1", "2013-01", "2020-03", [("S3 300", "EA888-2.0S", 380, {"fin": "2016-08"}), ("S3 310", "EA888-2.0S", 400, {"debut": "2016-09"})],
   reservoir=55, remarques="3 portes, Sportback, Berline, Cabriolet")
mg(LS, "S3", "8Y", "1", "2020-09", None, [("S3 310", "EA888-2.0S", 400, {"fin": "2024-06"}), ("S3 333", "EA888-2.0S", 420, {"debut": "2024-07"})],
   reservoir=55, remarques="Sportback et Berline")
mg(LS, "S4", "B5", "1", "1997-11", "2001-08", [("S4 2.7 biturbo 265", "V6-2.7T", 400)], portes=4, reservoir=62, remarques="Berline et Avant")
mg(LS, "S4", "B6", "1", "2003-02", "2008-03", [("S4 4.2 V8 344", "V8-4.2", 410)], portes=4, reservoir=70, remarques="Berline, Avant, Cabriolet")
mg(LS, "S4", "B8", "1", "2008-11", "2015-10", [("S4 3.0 TFSI 333", "EA837-3.0TFSI", 440)], portes=4, reservoir=65, remarques="Berline et Avant")
mg(LS, "S4", "B9", "1", "2016-06", "2019-06", [("S4 3.0 TFSI 354", "EA839-3.0TFSI", 500)], portes=4, reservoir=58, remarques="Berline et Avant")
mg(LS, "S4", "B9", "2", "2019-07", "2024-12", [("S4 TDI 347", "V6-3.0TDI-MHEV", 700)], portes=4, reservoir=58,
   remarques="Berline et Avant diesel en Europe")
mg(LS, "S5", "8T", "1", "2007-06", "2016-06", [("S5 4.2 V8 354", "V8-4.2FSI", 440, {"fin": "2011-12"}), ("S5 3.0 TFSI 333", "EA837-3.0TFSI", 440, {"debut": "2009-03"})],
   portes=2, places=4, reservoir=64, remarques="Coupé, Cabriolet, Sportback")
mg(LS, "S5", "F5", "1", "2016-07", "2024-06", [("S5 3.0 TFSI 354", "EA839-3.0TFSI", 500, {"fin": "2019-08"}), ("S5 TDI 347", "V6-3.0TDI-MHEV", 700, {"debut": "2019-09"})],
   portes=2, places=4, reservoir=58, remarques="Coupé, Cabriolet, Sportback")
mg(LS, "S5", "B10", "1", "2024-09", None, [("S5 367", "EA839-3.0TFSI", 550)], portes=5, reservoir=58, remarques="Berline à hayon et Avant")
mg(LS, "S6", "C4", "1", "1994-06", "1997-03", [("S6 2.2 turbo 230", "5C-2.2T", 350), ("S6 4.2 V8 290", "V8-4.2", 400)], portes=4, reservoir=80)
mg(LS, "S6", "C5", "1", "1999-05", "2004-05", [("S6 4.2 V8 340", "V8-4.2", 420)], portes=4, reservoir=70, remarques="Berline et Avant")
mg(LS, "S6", "C6", "1", "2006-03", "2011-03", [("S6 5.2 V10 435", "V10-5.2FSI", 540)], portes=4, reservoir=80, remarques="Berline et Avant")
mg(LS, "S6", "C7", "1", "2012-03", "2018-05", [("S6 4.0 TFSI 420", "V8-4.0TFSI", 550, {"fin": "2014-09"}), ("S6 4.0 TFSI 450", "V8-4.0TFSI", 550, {"debut": "2014-10"})],
   portes=4, reservoir=75, remarques="Berline et Avant")
mg(LS, "S6", "C8", "1", "2019-06", "2025-02", [("S6 TDI 349", "V6-3.0TDI-MHEV", 700)], portes=4, reservoir=63, remarques="Berline et Avant")
mg(LS, "S6 e-tron", "PPE", "1", "2024-09", None, [("S6 e-tron 551", "PPE-EV", 855, el(95))], portes=5, reservoir=0,
   remarques="Sportback et Avant électriques ; puissance avec Launch Control")
mg(LS, "S7", "4G", "1", "2012-03", "2018-01", [("S7 4.0 TFSI 420", "V8-4.0TFSI", 550, {"fin": "2014-09"}), ("S7 4.0 TFSI 450", "V8-4.0TFSI", 550, {"debut": "2014-10"})],
   portes=5, reservoir=75)
mg(LS, "S7", "4K", "1", "2019-06", "2025-06", [("S7 TDI 349", "V6-3.0TDI-MHEV", 700)], portes=5, reservoir=63)
mg(LS, "S8", "D2", "1", "1996-06", "2002-09", [("S8 4.2 V8 340", "V8-4.2", 410, {"fin": "1999-08"}), ("S8 4.2 V8 360", "V8-4.2", 430, {"debut": "1999-09"})],
   portes=4, reservoir=90)
mg(LS, "S8", "D3", "1", "2006-03", "2010-01", [("S8 5.2 V10 450", "V10-5.2FSI", 540)], portes=4, reservoir=90)
mg(LS, "S8", "D4", "1", "2012-03", "2017-10", [("S8 4.0 TFSI 520", "V8-4.0TFSI", 650), ("S8 plus 605", "V8-4.0TFSI", 700, {"debut": "2015-09"})],
   portes=4, reservoir=90)
mg(LS, "S8", "D5", "1", "2019-09", None, [("S8 571", "V8-4.0TFSI", 800)], portes=4, reservoir=82)
mg(LS, "TTS", "8J", "1", "2008-06", "2014-06", [("TTS 272", "EA113-2.0TFSI", 350)], portes=2, places=4, reservoir=60, remarques="Coupé et Roadster")
mg(LS, "TTS", "8S", "1", "2014-09", "2023-11", [("TTS 310", "EA888-2.0S", 380, {"fin": "2018-08"}), ("TTS 306", "EA888-2.0S", 400, {"debut": "2018-09", "fin": "2019-12"}),
   ("TTS 320", "EA888-2.0S", 400, {"debut": "2020-01"})], portes=2, places=4, reservoir=55, remarques="Coupé et Roadster")
mg(LS, "SQ5", "8R", "1", "2012-09", "2016-12", [("SQ5 TDI 313", "V6-3.0TDI", 650, {"fin": "2014-08"}), ("SQ5 TDI 326", "V6-3.0TDI", 650, {"debut": "2014-09"})],
   reservoir=75)
mg(LS, "SQ5", "FY", "1", "2017-03", "2024-11", [("SQ5 3.0 TFSI 354", "EA839-3.0TFSI", 500, {"fin": "2019-06"}), ("SQ5 TDI 347", "V6-3.0TDI-MHEV", 700, {"debut": "2019-07"})],
   reservoir=70, remarques="SUV et Sportback")
mg(LS, "SQ5", "GU", "1", "2024-12", None, [("SQ5 367", "EA839-3.0TFSI", 550)], reservoir=65, remarques="SUV et Sportback")
mg(LS, "SQ6 e-tron", "PPE", "1", "2024-06", None, [("SQ6 e-tron 517", "PPE-EV", 855, el(95))], reservoir=0, remarques="SUV et Sportback électriques")
mg(LS, "SQ7", "4M", "1", "2016-03", "2019-08", [("SQ7 TDI 435", "V8-4.0TDI", 900)], places=7, reservoir=85)
mg(LS, "SQ7", "4M", "2", "2019-09", None, [("SQ7 TDI 435", "V8-4.0TDI", 900, {"fin": "2020-08"}), ("SQ7 TFSI 507", "V8-4.0TFSI", 770, {"debut": "2020-09"})],
   places=7, reservoir=85)
mg(LS, "SQ8", "4M", "1", "2019-06", None, [("SQ8 TDI 435", "V8-4.0TDI", 900, {"fin": "2020-08"}), ("SQ8 TFSI 507", "V8-4.0TFSI", 770, {"debut": "2020-09"})],
   reservoir=85)
mg(LS, "S e-tron GT", "J1", "2", "2024-05", None, [("S e-tron GT 679", "J1-EV", 740, el(97))], portes=4, places=4, reservoir=0)

# ---------------------------------------------------------------- Audi RS
mg(LR, "RS2", "B4", "1", "1994-03", "1995-07", [("RS2 Avant 315", "5C-2.2T", 410)], portes=5, reservoir=66, remarques="Break co-développé avec Porsche")
mg(LR, "RS3", "8P", "1", "2011-04", "2012-12", [("RS3 Sportback 340", "EA855-2.5TFSI", 450)], reservoir=55)
mg(LR, "RS3", "8V", "1", "2015-03", "2020-03", [("RS3 367", "EA855-2.5TFSI", 465, {"fin": "2016-12"}), ("RS3 400", "EA855-2.5TFSI", 480, {"debut": "2017-01"})],
   reservoir=55, remarques="Sportback et Berline (2017)")
mg(LR, "RS3", "8Y", "1", "2021-07", None, [("RS3 400", "EA855-2.5TFSI", 500)], reservoir=55, remarques="Sportback et Berline ; restylage 2024")
mg(LR, "RS4", "B5", "1", "2000-03", "2001-09", [("RS4 380", "V6-2.7T", 440)], portes=5, reservoir=62, remarques="Avant")
mg(LR, "RS4", "B7", "1", "2006-01", "2008-06", [("RS4 420", "V8-4.2FSI", 430)], portes=4, reservoir=63, remarques="Berline, Avant, Cabriolet")
mg(LR, "RS4", "B8", "1", "2012-06", "2015-10", [("RS4 450", "V8-4.2FSI", 430)], portes=5, reservoir=65, remarques="Avant")
mg(LR, "RS4", "B9", "1", "2018-01", "2024-12", [("RS4 450", "EA839-2.9TFSI", 600)], portes=5, reservoir=58, remarques="Avant")
mg(LR, "RS5", "8T", "1", "2010-03", "2015-12", [("RS5 450", "V8-4.2FSI", 430)], portes=2, places=4, reservoir=61, remarques="Coupé et Cabriolet")
mg(LR, "RS5", "F5", "1", "2017-06", "2024-06", [("RS5 450", "EA839-2.9TFSI", 600)], portes=2, places=4, reservoir=58, remarques="Coupé et Sportback")
mg(LR, "RS5", "B10", "1", "2026-05", None, [("RS5 639", "EA839-2.9PHEV", 825, ph(20, 58))], portes=5, reservoir=58,
   remarques="Berline à hayon et Avant hybrides rechargeables (première RS électrifiée)")
mg(LR, "RS6", "C5", "1", "2002-06", "2004-09", [("RS6 450", "V8-4.2", 560), ("RS6 plus 480", "V8-4.2", 560, {"debut": "2004-06"})], portes=4,
   reservoir=82, remarques="Berline et Avant")
mg(LR, "RS6", "C6", "1", "2008-01", "2010-09", [("RS6 5.0 V10 580", "V10-5.0TFSI", 650)], portes=4, reservoir=80, remarques="Berline et Avant")
mg(LR, "RS6", "C7", "1", "2013-03", "2018-05", [("RS6 560", "V8-4.0TFSI", 700), ("RS6 performance 605", "V8-4.0TFSI", 750, {"debut": "2015-09"})],
   portes=5, reservoir=75, remarques="Avant")
mg(LR, "RS6", "C8", "1", "2019-09", "2025-12", [("RS6 600", "V8-4.0TFSI", 800, {"fin": "2023-03"}), ("RS6 performance 630", "V8-4.0TFSI", 850, {"debut": "2023-04"})],
   portes=5, reservoir=73, remarques="Avant ; RS6 GT (2024) non détaillée")
mg(LR, "RS7", "4G", "1", "2013-06", "2018-01", [("RS7 560", "V8-4.0TFSI", 700), ("RS7 performance 605", "V8-4.0TFSI", 750, {"debut": "2015-09"})],
   portes=5, reservoir=75)
mg(LR, "RS7", "4K", "1", "2019-09", "2025-06", [("RS7 600", "V8-4.0TFSI", 800, {"fin": "2023-03"}), ("RS7 performance 630", "V8-4.0TFSI", 850, {"debut": "2023-04"})],
   portes=5, reservoir=73)
mg(LR, "TT RS", "8J", "1", "2009-06", "2014-06", [("TT RS 340", "EA855-2.5TFSI", 450), ("TT RS plus 360", "EA855-2.5TFSI", 465, {"debut": "2012-06"})],
   portes=2, places=4, reservoir=60, remarques="Coupé et Roadster")
mg(LR, "TT RS", "8S", "1", "2016-09", "2023-11", [("TT RS 400", "EA855-2.5TFSI", 480)], portes=2, places=4, reservoir=55, remarques="Coupé et Roadster")
mg(LR, "RS Q3", "8U", "1", "2013-09", "2018-08", [("RS Q3 310", "EA855-2.5TFSI", 420, {"fin": "2014-12"}), ("RS Q3 340", "EA855-2.5TFSI", 450, {"debut": "2015-01"}),
   ("RS Q3 performance 367", "EA855-2.5TFSI", 465, {"debut": "2016-03"})], reservoir=64)
mg(LR, "RS Q3", "F3", "1", "2019-11", "2025-09", [("RS Q3 400", "EA855-2.5TFSI", 480)], reservoir=60, remarques="SUV et Sportback")
mg(LR, "RS Q8", "4M", "1", "2020-01", None, [("RS Q8 600", "V8-4.0TFSI", 800, {"fin": "2024-08"}), ("RS Q8 performance 640", "V8-4.0TFSI", 850, {"debut": "2024-09"})],
   reservoir=85)
mg(LR, "RS e-tron GT", "J1", "1", "2021-03", "2024-04", [("RS e-tron GT 646", "J1-EV", 830, el(84))], portes=4, places=4, reservoir=0)
mg(LR, "RS e-tron GT", "J1", "2", "2024-05", None, [("RS e-tron GT performance 925", "J1-EV", 1027, el(97)), ("RS e-tron GT 856", "J1-EV", 1027, el(97))],
   portes=4, places=4, reservoir=0, remarques="Puissances avec boost")

MOT = Motorisations("Audi", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LS)
MOT.lier(LR)

DETAIL = {"Audi": L, "Audi S": LS, "Audi RS": LR}
MOTEURS = MOT.moteurs()
