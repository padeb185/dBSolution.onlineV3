"""Volvo : générations, phases, motorisations (marché européen) et moteurs liés.
PV444/544, Amazon, P1800, 140/164, 240/260, 340/360, 440/460/480, 740/760, 940/960, 850, S/V40, S/V70, S80,
S60/V60, S90/V90, XC40/60/70/90, C30, C70, S40/V50, EX30, EX40/EC40, EX90, ES90, EX60.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom.
Moteurs d'origine Renault, PRV, PSA, Ford et Volkswagen rattachés au motoriste Volvo ; données anciennes indicatives."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


FAMILLES = {
    # --- anciens (soupapes en tête, pignons)
    "B16": f("ATM", E_, 1.6, "NC", 4, 5500, 3500, "20W50", 3.5, 5000),
    "B18": f("ATM", E_, 1.8, "NC", 4, 5800, 3500, "20W50", 3.75, 5000),
    "B20": f("ATM", E_, 2.0, "NC", 4, 6000, 3500, "20W50", 3.75, 7500),
    "B30": f("ATM", E_, 3.0, "NC", 6, 5000, 2500, "20W50", 5.0, 7500),
    # --- série « Red Block » et dérivés
    "B19": f("ATM", E_, 2.0, B, 4, 5500, 3000, "15W40", 3.85, 10000),
    "B21": f("ATM", E_, 2.1, B, 4, 5500, 3500, "15W40", 3.85, 10000),
    "B21T": f("TURBO", E_, 2.1, B, 4, 5500, 3500, "15W40", 3.85, 10000),
    "B23": f("ATM", E_, 2.3, B, 4, 5400, 3500, "15W40", 3.85, 10000),
    "B230F": f("ATM", E_, 2.3, B, 4, 5400, 2750, "10W40", 3.85, 15000),
    "B230FT": f("TURBO", E_, 2.3, B, 4, 5300, 2900, "10W40", 3.85, 15000),
    "B200": f("ATM", E_, 2.0, B, 4, 5400, 3000, "10W40", 3.85, 15000),
    "B6304": f("ATM", E_, 2.9, B, 6, 6000, 4300, "10W40", 5.9, 15000),
    "PRV-2.7": f("ATM", E_, 2.7, C, 6, 5750, 3000, "15W40", 6.0, 10000, a="V"),
    "PRV-2.85": f("ATM", E_, 2.85, C, 6, 5400, 3000, "15W40", 6.0, 10000, a="V"),
    # --- Renault (340, 440, 480, S40 I)
    "B14": f("ATM", E_, 1.4, C, 4, 5500, 3500, "15W40", 3.5, 10000),
    "B172": f("ATM", E_, 1.7, B, 4, 5500, 3000, "15W40", 4.0, 10000),
    "B18F": f("ATM", E_, 1.7, B, 4, 5800, 4000, "15W40", 4.0, 10000),
    "B18FT": f("TURBO", E_, 1.7, B, 4, 5400, 4000, "15W40", 4.0, 10000),
    "B20F": f("ATM", E_, 2.0, B, 4, 5400, 3500, "15W40", 4.0, 10000),
    "F8Q": f("TURBO", D, 1.9, B, 4, 4250, 2250, "15W40", 5.0, 10000),
    "F9Q": f("TURBO", D, 1.9, B, 4, 4000, 1750, "5W40", 5.0, 15000),
    # --- diesels Volkswagen
    "D24": f("ATM", D, 2.4, B, 6, 4800, 2800, "15W40", 6.5, 7500),
    "D24T": f("TURBO", D, 2.4, B, 6, 4800, 2400, "15W40", 6.5, 7500),
    "D5252T": f("TURBO", D, 2.5, B, 5, 4000, 1900, "10W40", 6.0, 15000),
    # --- modulaires 4/5/6 cylindres (1991-2016)
    "B4164S": f("ATM", E_, 1.6, B, 4, 5500, 4200, "10W40", 4.4, 20000),
    "B4184S": f("ATM", E_, 1.8, B, 4, 5500, 4500, "10W40", 4.4, 20000),
    "B4204S": f("ATM", E_, 2.0, B, 4, 6000, 4500, "10W40", 4.4, 20000),
    "B4194T": f("TURBO", E_, 1.9, B, 4, 5500, 2400, "10W40", 4.4, 20000),
    "B5202S": f("ATM", E_, 2.0, B, 5, 6250, 4800, "10W40", 5.5, 20000),
    "B5252S": f("ATM", E_, 2.5, B, 5, 6250, 3300, "10W40", 5.5, 20000),
    "B5244S": f("ATM", E_, 2.4, B, 5, 6000, 4500, "5W30", 5.5, 20000),
    "B5234T": f("TURBO", E_, 2.3, B, 5, 5200, 2700, "5W30", 5.5, 20000),
    "B5204T": f("TURBO", E_, 2.0, B, 5, 5500, 2200, "5W30", 5.5, 20000),
    "B5244T": f("TURBO", E_, 2.4, B, 5, 5900, 2000, "5W30", 5.5, 20000),
    "B5254T": f("TURBO", E_, 2.5, B, 5, 5000, 1500, "5W30", 5.5, 20000),
    "B5254T-R": f("TURBO", E_, 2.5, B, 5, 5500, 1950, "5W30", 5.8, 20000),
    "B6294T": f("TURBO", E_, 2.9, B, 6, 5400, 1800, "5W30", 6.4, 20000),
    "B6324S": f("ATM", E_, 3.2, C, 6, 6200, 3200, "5W30", 6.8, 30000),
    "B6304T": f("TURBO", E_, 3.0, C, 6, 5600, 2100, "5W30", 6.8, 30000),
    "B8444S": f("ATM", E_, 4.4, C, 8, 5850, 3900, "5W30", 7.4, 30000, a="V"),
    "D5244T": f("TURBO", D, 2.4, B, 5, 4000, 1750, "5W30", 6.0, 30000),
    "D5204T": f("TURBO", D, 2.0, B, 5, 3500, 1500, "5W30", 6.0, 30000),
    "D4164T": f("TURBO", D, 1.6, B, 4, 4000, 1750, "5W30", 3.75, 30000),
    "D4204T-PSA": f("TURBO", D, 2.0, B, 4, 4000, 2000, "5W30", 5.5, 30000),
    "B4164S3": f("ATM", E_, 1.6, B, 4, 6000, 4100, "5W30", 4.1, 20000),
    "B4184S11": f("ATM", E_, 1.8, C, 4, 6000, 4000, "5W30", 4.3, 20000),
    "B4204S3": f("ATM", E_, 2.0, C, 4, 6000, 4500, "5W30", 4.3, 20000),
    "B4164T": f("TURBO", E_, 1.6, B, 4, 5700, 1600, "5W30", 4.2, 30000),
    # --- Drive-E (2013-)
    "B3154T": f("TURBO", E_, 1.5, B, 3, 5500, 1850, "0W20", 4.5, 30000),
    "B3154T-PHEV": f("HYB_TE", E_, 1.5, B, 3, 5800, 1850, "0W20", 4.5, 30000),
    "B4204T": f("TURBO", E_, 2.0, B, 4, 5500, 1500, "0W20", 5.6, 30000),
    "B4204T-PHEV": f("HYB_TE", E_, 2.0, B, 4, 5700, 2200, "0W20", 5.6, 30000),
    "B4204T-MHEV": f("HYB_TE", E_, 2.0, B, 4, 5400, 1800, "0W20", 5.6, 30000),
    "D4204T": f("TURBO", D, 2.0, B, 4, 4250, 1750, "0W30", 5.6, 30000),
    "D4204T-MHEV": f("TURBO", D, 2.0, B, 4, 4000, 1750, "0W30", 5.6, 30000),
    # --- électriques
    "EV-CMA": electrique(), "EV-SEA": electrique(), "EV-SPA2": electrique(), "EV-SPA3": electrique(),
}

mg = SaisieMoteurs(FAMILLES, "Volvo")
L = []

# ---------------------------------------------------------------- classiques
mg(L, "PV444 / PV544", "PV", "1", "1947-02", "1965-10",
   [("PV444 1.4 40", "B16", 82, {"fin": "1956-12"}), ("PV444 1.6 60", "B16", 118, {"debut": "1957-01", "fin": "1958-08"}),
    ("PV544 1.6 66", "B16", 118, {"debut": "1958-08", "fin": "1961-08"}), ("PV544 1.8 75", "B18", 136, {"debut": "1961-08"}),
    ("PV544 1.8 Sport 95", "B18", 140, {"debut": "1961-08"})], portes=2, places=5, reservoir=35,
   remarques="Berline 2 portes « bossue » ; Duett (break)")
mg(L, "Amazon", "120", "1", "1956-08", "1970-07",
   [("121 1.6 60", "B16", 118, {"fin": "1961-07"}), ("122 S 1.6 85", "B16", 118, {"debut": "1958-01", "fin": "1961-07"}),
    ("121 1.8 75", "B18", 136, {"debut": "1961-08", "fin": "1968-07"}), ("123 GT 1.8 115", "B18", 154, {"debut": "1966-09", "fin": "1967-12"}),
    ("121 2.0 82", "B20", 157, {"debut": "1968-08"})], portes=4, reservoir=45,
   remarques="Berline 2 (130) et 4 portes (120), Break 220")
mg(L, "P1800", "P1800", "1", "1961-05", "1973-06",
   [("P1800 1.8 100", "B18", 147, {"fin": "1968-07"}), ("1800 E 2.0 130", "B20", 176, {"debut": "1969-08"}),
    ("1800 ES 2.0 125", "B20", 170, {"debut": "1971-08"})], portes=2, places=4, reservoir=45,
   remarques="Coupé ; break de chasse 1800 ES (1972-1973)")
mg(L, "140", "140", "1", "1966-08", "1974-07",
   [("142 / 144 1.8 75", "B18", 136, {"fin": "1968-07"}), ("144 2.0 90", "B20", 160, {"debut": "1968-08"}),
    ("144 E 2.0 124", "B20", 167, {"debut": "1971-08"})], portes=4, reservoir=58, remarques="Berline 142 (2 p.), 144 (4 p.), Break 145")
mg(L, "164", "164", "1", "1968-09", "1975-07",
   [("164 3.0 130", "B30", 208), ("164 E 3.0 160", "B30", 230, {"debut": "1971-08"})], portes=4, reservoir=68,
   remarques="Berline 6 cylindres")
mg(L, "240", "240", "1", "1974-08", "1993-05",
   [("244 2.0 90", "B19", 160, {"fin": "1984-07"}), ("244 2.1 100", "B21", 165, {"fin": "1984-07"}),
    ("244 GLT 2.3 136", "B23", 190, {"debut": "1978-08", "fin": "1984-07"}), ("240 Turbo 2.1 155", "B21T", 240, {"debut": "1981-02", "fin": "1985-07"}),
    ("240 2.3 116", "B230F", 185, {"debut": "1984-08"}), ("240 D 2.4 82", "D24", 140, {"debut": "1979-08"})], portes=4,
   reservoir=60, remarques="Berline 242 (2 p.) et 244 (4 p.), Break 245")
mg(L, "260", "260", "1", "1974-08", "1985-07",
   [("264 2.7 140", "PRV-2.7", 208, {"fin": "1980-07"}), ("264 2.8 155", "PRV-2.85", 230, {"debut": "1980-08"})],
   portes=4, reservoir=60, remarques="Berline V6 PRV, Break 265, Coupé Bertone 262C")
mg(L, "340 / 360", "300", "1", "1976-02", "1991-06",
   [("343 / 345 1.4 70", "B14", 108), ("340 1.7 82", "B172", 133, {"debut": "1985-08"}),
    ("360 2.0 95", "B19", 158, {"debut": "1982-08", "fin": "1984-07"}), ("360 GLT 2.0 115", "B200", 165, {"debut": "1983-08"}),
    ("340 1.6 D 54", "F8Q", 100, {"debut": "1984-08"})], portes=5, reservoir=45,
   remarques="Berline 3/5 portes et 4 portes (ex-DAF), transmission Variomatic ou manuelle")
mg(L, "740 / 760", "700", "1", "1982-02", "1992-06",
   [("740 2.3 115", "B230F", 185), ("740 Turbo 2.3 165", "B230FT", 264), ("760 2.8 V6 156", "PRV-2.85", 235),
    ("740 TD 2.4 109", "D24T", 205)], portes=4, reservoir=60, remarques="Berline et Break (1985)")
mg(L, "940 / 960", "900", "1", "1990-08", "1998-06",
   [("940 2.3 131", "B230F", 185), ("940 Turbo 2.3 165", "B230FT", 264), ("960 2.9 204", "B6304", 267),
    ("940 TD 2.4 122", "D24T", 235)], portes=4, reservoir=80, remarques="Berline et Break ; S90/V90 (1997-1998)")
mg(L, "480", "480", "1", "1986-06", "1995-10",
   [("480 1.7 109", "B18F", 140), ("480 Turbo 1.7 120", "B18FT", 175, {"debut": "1988-08"}),
    ("480 2.0 110", "B20F", 165, {"debut": "1992-08"})], portes=3, places=4, reservoir=48, remarques="Coupé break 3 portes")
mg(L, "440 / 460", "400", "1", "1988-06", "1996-12",
   [("440 1.7 109", "B18F", 140), ("440 Turbo 1.7 120", "B18FT", 175), ("440 2.0 110", "B20F", 165, {"debut": "1992-08"}),
    ("440 1.9 TD 90", "F8Q", 176, {"debut": "1994-01"})], portes=5, reservoir=48, remarques="Berline 5 portes (440) et 4 portes (460)")

# ---------------------------------------------------------------- 850 / S70 / V70 / S80 / XC70
mg(L, "850", "850", "1", "1991-06", "1996-12",
   [("2.0 10v 126", "B5202S", 170), ("2.0 20v 143", "B5202S", 184), ("2.5 10v 144", "B5252S", 206), ("2.5 20v 170", "B5252S", 220),
    ("T5 225", "B5234T", 300), ("T-5R 240", "B5234T", 330, {"debut": "1995-01", "fin": "1995-12"}), ("R 250", "B5234T", 350, {"debut": "1996-01"}),
    ("2.5 TDI 140", "D5252T", 290, {"debut": "1995-01"})], portes=4, reservoir=73, remarques="Berline et Break (1993)")
mg(L, "S70 / V70", "P80", "1", "1997-01", "2000-12",
   [("2.0 126", "B5202S", 170), ("2.5 10v 144", "B5252S", 206), ("2.5 20v 170", "B5252S", 220), ("2.4 T 193", "B5244T", 270),
    ("T5 236", "B5234T", 330), ("R 250", "B5234T", 350), ("2.5 TDI 140", "D5252T", 290)], portes=4, reservoir=70,
   remarques="Berline S70, Break V70, V70 XC (Cross Country) ; C70 Coupé/Cabriolet (1997-2005)")
mg(L, "S80", "TS", "1", "1998-05", "2006-03",
   [("2.4 140", "B5244S", 220), ("2.4 170", "B5244S", 230), ("2.4 T 200", "B5244T", 285), ("T6 272", "B6294T", 380),
    ("2.9 204", "B6304", 280, {"fin": "2001-12"}), ("2.5 T 210", "B5254T", 320, {"debut": "2003-08"}),
    ("D5 163", "D5244T", 340, {"debut": "2001-09"}), ("2.5 TDI 140", "D5252T", 290, {"fin": "2001-08"})], portes=4, reservoir=70,
   remarques="Berline")
mg(L, "S60 / V70", "P2", "1", "2000-03", "2004-06",
   [("2.4 140", "B5244S", 220), ("2.4 170", "B5244S", 230), ("2.0 T 180", "B5204T", 240), ("2.4 T 200", "B5244T", 285),
    ("T5 250", "B5234T", 330), ("R 300", "B5254T-R", 400, {"debut": "2003-03"}), ("D5 163", "D5244T", 340),
    ("2.4 D 130", "D5244T", 280, {"debut": "2002-01"})], portes=4, reservoir=70,
   remarques="Berline S60, Break V70, XC70 (Cross Country)")
mg(L, "S60 / V70", "P2", "2", "2004-07", "2009-12",
   [("2.4 140", "B5244S", 220), ("2.4 170", "B5244S", 230), ("2.5 T 210", "B5254T", 320), ("T5 260", "B5254T", 350),
    ("R 300", "B5254T-R", 400, {"fin": "2007-06"}), ("D5 185", "D5244T", 400), ("2.4 D 163", "D5244T", 340),
    ("2.4 D 130", "D5244T", 280)], portes=4, reservoir=70, remarques="S60 jusqu'en 2009, V70/XC70 jusqu'en 2007")
mg(L, "V70 / XC70", "P3", "1", "2007-08", "2016-04",
   [("2.0 145", "B4204S3", 185, {"fin": "2010-12"}), ("2.5 T 200", "B5254T", 300, {"fin": "2010-12"}),
    ("3.2 238", "B6324S", 320, {"fin": "2010-12"}), ("T6 285", "B6304T", 400, {"debut": "2008-08"}),
    ("1.6 DRIVe 109", "D4164T", 240, {"debut": "2009-08", "fin": "2013-12"}), ("D3 163", "D5204T", 400, {"debut": "2010-08"}),
    ("D4 181", "D5244T", 400, {"debut": "2011-08", "fin": "2015-12"}), ("D5 215", "D5244T", 440, {"debut": "2011-08"}),
    ("2.4 D 175", "D5244T", 420, {"fin": "2010-07"}), ("D4 190", "D4204T", 400, {"debut": "2014-08"})], portes=5, reservoir=70,
   remarques="Break V70 et XC70 ; restylage 2013")
mg(L, "S80", "P3", "1", "2006-05", "2016-04",
   [("2.5 T 200", "B5254T", 300, {"fin": "2010-12"}), ("3.2 238", "B6324S", 320), ("V8 4.4 315", "B8444S", 440, {"fin": "2010-12"}),
    ("T6 285", "B6304T", 400, {"debut": "2008-08"}), ("D5 185", "D5244T", 400, {"fin": "2009-12"}), ("D5 215", "D5244T", 440, {"debut": "2011-08"}),
    ("D3 163", "D5204T", 400, {"debut": "2010-08"}), ("D4 190", "D4204T", 400, {"debut": "2014-08"})], portes=4, reservoir=70,
   remarques="Berline ; restylage 2009")

# ---------------------------------------------------------------- S40 / V40 / V50 / C30 / C70
mg(L, "S40 / V40", "P1", "1", "1995-09", "2004-06",
   [("1.6 105", "B4164S", 145), ("1.8 115", "B4184S", 165), ("2.0 140", "B4204S", 183), ("T4 200", "B4194T", 300, {"debut": "1997-09"}),
    ("1.9 TD 90", "F8Q", 176, {"fin": "1999-12"}), ("1.9 D 115", "F9Q", 265, {"debut": "2000-01"})], portes=4, reservoir=60,
   remarques="Berline S40 et Break V40 (Nedcar, base Mitsubishi Carisma)")
mg(L, "S40 / V50", "P1-C1", "1", "2004-01", "2012-06",
   [("1.6 101", "B4164S3", 150), ("1.8 125", "B4184S11", 165), ("2.0 145", "B4204S3", 185), ("2.4 170", "B5244S", 230),
    ("T5 220", "B5254T", 320), ("T5 230", "B5254T", 320, {"debut": "2007-08"}), ("1.6 D 109", "D4164T", 240),
    ("2.0 D 136", "D4204T-PSA", 320), ("D5 180", "D5244T", 350, {"debut": "2006-01"}), ("D3 150", "D5204T", 350, {"debut": "2010-08"})],
   portes=4, reservoir=62, remarques="Berline S40, Break V50 (plateforme Ford C1) ; restylage 2007")
mg(L, "C30", "P1-C1", "1", "2006-12", "2013-12",
   [("1.6 100", "B4164S3", 150), ("1.8 125", "B4184S11", 165), ("2.0 145", "B4204S3", 185), ("2.4 170", "B5244S", 230),
    ("T5 230", "B5254T", 320), ("1.6 D 109", "D4164T", 240), ("2.0 D 136", "D4204T-PSA", 320), ("D5 180", "D5244T", 350)],
   portes=3, places=4, reservoir=62, remarques="Coupé 3 portes ; restylage 2010 ; C30 Electric (2011) non détaillée")
mg(L, "C70", "P1-C1", "1", "2006-03", "2013-06",
   [("2.4 170", "B5244S", 230), ("T5 220", "B5254T", 320), ("T5 230", "B5254T", 320, {"debut": "2008-01"}),
    ("2.0 D 136", "D4204T-PSA", 320), ("D5 180", "D5244T", 350)], portes=2, places=4, reservoir=62,
   remarques="Coupé-cabriolet à toit rigide rétractable")
mg(L, "V40", "P1-V40", "1", "2012-05", "2019-06",
   [("T2 122", "B4164T", 220, {"fin": "2015-06"}), ("T3 150", "B4164T", 240, {"fin": "2015-06"}), ("T4 180", "B4164T", 240, {"fin": "2015-06"}),
    ("T5 254", "B5254T", 360, {"fin": "2015-06"}), ("D2 115", "D4164T", 270, {"fin": "2015-06"}), ("D3 150", "D5204T", 350, {"fin": "2015-06"}),
    ("D4 177", "D5204T", 400, {"fin": "2015-06"}), ("T2 Drive-E 122", "B4204T", 220, {"debut": "2015-07"}),
    ("T3 152", "B4204T", 250, {"debut": "2015-07"}), ("T5 245", "B4204T", 350, {"debut": "2015-07"}),
    ("D2 120", "D4204T", 280, {"debut": "2015-07"}), ("D3 Drive-E 150", "D4204T", 320, {"debut": "2015-07"}),
    ("D4 190", "D4204T", 400, {"debut": "2015-07"})], portes=5, reservoir=62, remarques="Compacte 5 portes et Cross Country ; restylage 2016")

# ---------------------------------------------------------------- S60 / V60 / S90 / V90
mg(L, "S60 / V60", "P3", "1", "2010-04", "2018-06",
   [("T3 150", "B4164T", 240), ("T4 180", "B4164T", 240), ("T5 240", "B4204T", 320, {"fin": "2014-07"}), ("T6 304", "B6304T", 440),
    ("D2 115", "D4164T", 270), ("D3 163", "D5204T", 400), ("D4 181", "D5244T", 400, {"fin": "2014-07"}), ("D5 215", "D5244T", 440),
    ("D4 190", "D4204T", 400, {"debut": "2014-08"}), ("T5 245", "B4204T", 350, {"debut": "2014-08"}),
    ("D6 Plug-in 285", "D5244T", 640, {"debut": "2012-11", "fin": "2015-12", "batterie": 11})], portes=4, reservoir=68,
   remarques="Berline S60, Break V60 (2010-10), V60 Cross Country (2015) ; restylage 2013 ; D6 hybride diesel rechargeable")
mg(L, "S60 / V60", "SPA", "1", "2018-06", "2024-06",
   [("T4 190", "B4204T", 300, {"fin": "2020-06"}), ("T5 250", "B4204T", 350, {"fin": "2020-06"}),
    ("D3 150", "D4204T", 320, {"fin": "2019-12"}), ("D4 190", "D4204T", 400, {"fin": "2019-12"}),
    ("B4 197", "B4204T-MHEV", 300, {"debut": "2020-01"}), ("B5 250", "B4204T-MHEV", 350, {"debut": "2020-01"}),
    ("B4 Diesel 197", "D4204T-MHEV", 420, {"debut": "2020-01", "fin": "2021-12"}),
    ("T6 Recharge 340", "B4204T-PHEV", 590, ph(11, 60, debut="2019-06")), ("T8 Recharge 390", "B4204T-PHEV", 640, ph(11, 60)),
    ("T8 Recharge 455", "B4204T-PHEV", 709, ph(19, 60, debut="2022-01")), ("Polestar Engineered 405", "B4204T-PHEV", 670, ph(11, 60))],
   portes=4, reservoir=60, remarques="Berline S60 (fin en Europe 2024), Break V60 et V60 Cross Country")
mg(L, "S90 / V90", "SPA", "1", "2016-06", "2020-06",
   [("T4 190", "B4204T", 300), ("T5 254", "B4204T", 350), ("T6 320", "B4204T", 400), ("T8 Twin Engine 390", "B4204T-PHEV", 640, ph(10, 60)),
    ("D3 150", "D4204T", 320), ("D4 190", "D4204T", 400), ("D5 235", "D4204T", 480)], portes=4, reservoir=60,
   remarques="Berline S90, Break V90, V90 Cross Country")
mg(L, "S90 / V90", "SPA", "2", "2020-07", None,
   [("B4 197", "B4204T-MHEV", 300), ("B5 250", "B4204T-MHEV", 350), ("B4 Diesel 197", "D4204T-MHEV", 420, {"fin": "2023-12"}),
    ("B5 Diesel 235", "D4204T-MHEV", 480, {"fin": "2023-12"}), ("T8 Recharge 455", "B4204T-PHEV", 709, ph(19, 60))],
   portes=4, reservoir=60, remarques="Berline S90 (fin en Europe 2024) et Break V90 / V90 Cross Country")

# ---------------------------------------------------------------- SUV thermiques
mg(L, "XC90", "P2", "1", "2002-10", "2014-12",
   [("2.5 T 210", "B5254T", 320), ("T6 272", "B6294T", 380, {"fin": "2005-12"}), ("3.2 238", "B6324S", 320, {"debut": "2006-01"}),
    ("V8 4.4 315", "B8444S", 440, {"debut": "2005-01", "fin": "2011-12"}), ("D5 163", "D5244T", 340, {"fin": "2005-12"}),
    ("D5 185", "D5244T", 400, {"debut": "2006-01", "fin": "2011-12"}), ("D5 200", "D5244T", 420, {"debut": "2012-01"})], places=7,
   reservoir=72, remarques="SUV 5 ou 7 places ; restylages 2006 et 2012")
mg(L, "XC90", "SPA", "1", "2015-01", "2019-05",
   [("T5 254", "B4204T", 350), ("T6 320", "B4204T", 400), ("T8 Twin Engine 407", "B4204T-PHEV", 640, ph(10, 50)),
    ("D4 190", "D4204T", 400), ("D5 235", "D4204T", 480)], places=7, reservoir=71, remarques="SUV 7 places")
mg(L, "XC90", "SPA", "2", "2019-06", "2024-08",
   [("B5 250", "B4204T-MHEV", 350), ("B6 300", "B4204T-MHEV", 420), ("B5 Diesel 235", "D4204T-MHEV", 480, {"fin": "2023-12"}),
    ("T8 Recharge 390", "B4204T-PHEV", 640, ph(11, 50, fin="2021-12")), ("T8 Recharge 455", "B4204T-PHEV", 709, ph(19, 50, debut="2022-01"))],
   places=7, reservoir=71, remarques="SUV 7 places, hybridation légère 48 V")
mg(L, "XC90", "SPA", "3", "2024-09", None,
   [("B5 250", "B4204T-MHEV", 360), ("T8 Recharge 455", "B4204T-PHEV", 709, ph(19, 50))], places=7, reservoir=71,
   remarques="2e restylage")
mg(L, "XC60", "P3", "1", "2008-10", "2013-06",
   [("2.0 T 203", "B4204T", 300), ("3.0 T6 285", "B6304T", 400), ("3.2 243", "B6324S", 320), ("DRIVe 2.0 D 163", "D5204T", 400),
    ("D3 163", "D5204T", 400), ("D5 205", "D5244T", 420)], reservoir=70, remarques="SUV")
mg(L, "XC60", "P3", "2", "2013-07", "2017-03",
   [("T5 245", "B4204T", 350), ("T6 304", "B6304T", 440), ("D3 150", "D5204T", 350), ("D4 190", "D4204T", 400),
    ("D5 220", "D5244T", 440)], reservoir=70, remarques="SUV restylé")
mg(L, "XC60", "SPA", "1", "2017-04", "2021-06",
   [("T5 250", "B4204T", 350), ("T6 320", "B4204T", 400), ("T8 Twin Engine 390", "B4204T-PHEV", 640, ph(10, 50)),
    ("D4 190", "D4204T", 400), ("D5 235", "D4204T", 480), ("B4 197", "B4204T-MHEV", 300, {"debut": "2020-01"}),
    ("B5 250", "B4204T-MHEV", 350, {"debut": "2020-01"}), ("B4 Diesel 197", "D4204T-MHEV", 420, {"debut": "2020-01"})],
   reservoir=71, remarques="SUV")
mg(L, "XC60", "SPA", "2", "2021-07", "2025-03",
   [("B4 197", "B4204T-MHEV", 300), ("B5 250", "B4204T-MHEV", 350), ("B4 Diesel 197", "D4204T-MHEV", 420, {"fin": "2023-12"}),
    ("T6 Recharge 350", "B4204T-PHEV", 590, ph(19, 50, debut="2022-01")), ("T8 Recharge 455", "B4204T-PHEV", 709, ph(19, 50, debut="2022-01"))],
   reservoir=71, remarques="SUV restylé (Android Automotive)")
mg(L, "XC60", "SPA", "3", "2025-04", None,
   [("B5 250", "B4204T-MHEV", 360), ("T6 Plug-in 350", "B4204T-PHEV", 590, ph(19, 50)), ("T8 Plug-in 455", "B4204T-PHEV", 709, ph(19, 50))],
   reservoir=71, remarques="2e restylage")
mg(L, "XC40", "CMA", "1", "2017-11", "2022-06",
   [("T2 129", "B3154T", 245, {"debut": "2019-06"}), ("T3 156", "B3154T", 265), ("T4 190", "B4204T", 300), ("T5 247", "B4204T", 350),
    ("D3 150", "D4204T", 320, {"fin": "2020-12"}), ("D4 190", "D4204T", 400, {"fin": "2020-12"}),
    ("T4 Recharge 211", "B3154T-PHEV", 425, ph(11, 48, debut="2020-06")), ("T5 Recharge 262", "B3154T-PHEV", 425, ph(11, 48, debut="2020-01")),
    ("B4 197", "B4204T-MHEV", 300, {"debut": "2020-09"}), ("B5 250", "B4204T-MHEV", 350, {"debut": "2020-09"})], reservoir=54,
   remarques="SUV compact")
mg(L, "XC40", "CMA", "2", "2022-07", "2026-08",
   [("B3 163", "B4204T-MHEV", 265), ("B4 197", "B4204T-MHEV", 300), ("T4 Recharge 211", "B3154T-PHEV", 425, ph(14, 48, fin="2024-06")),
    ("T5 Recharge 262", "B3154T-PHEV", 425, ph(14, 48, fin="2024-06"))], reservoir=54, remarques="SUV compact restylé")
mg(L, "XC40", "CMA", "3", "2026-09", None, [("B3 163", "B4204T-MHEV", 265), ("B4 197", "B4204T-MHEV", 300)], reservoir=54,
   remarques="2e restylage (millésime 2027)")

# ---------------------------------------------------------------- électriques
mg(L, "EX40", "CMA", "1", "2020-10", "2026-08",
   [("Recharge P8 408", "EV-CMA", 660, el(75, fin="2022-12")), ("Recharge 231", "EV-CMA", 330, el(67, debut="2022-01", fin="2023-12")),
    ("Single Motor 238", "EV-CMA", 420, el(67, debut="2024-01")), ("Single Motor Extended Range 252", "EV-CMA", 420, el(79, debut="2024-01")),
    ("Twin Motor 408", "EV-CMA", 670, el(79, debut="2023-01"))], reservoir=0,
   remarques="SUV compact électrique (ex-XC40 Recharge, renommé EX40 en 2024) ; propulsion à partir de 2023")
mg(L, "EX40", "CMA", "2", "2026-09", None,
   [("Single Motor 238", "EV-CMA", 420, el(67)), ("Single Motor Extended Range 252", "EV-CMA", 420, el(79)),
    ("Twin Motor 408", "EV-CMA", 670, el(79))], reservoir=0, remarques="2e restylage (millésime 2027), pompe à chaleur de série")
mg(L, "EC40", "CMA", "1", "2021-10", None,
   [("Recharge Twin 408", "EV-CMA", 660, el(75, fin="2022-12")), ("Single Motor 238", "EV-CMA", 420, el(67, debut="2023-01")),
    ("Single Motor Extended Range 252", "EV-CMA", 420, el(79, debut="2023-01")), ("Twin Motor 408", "EV-CMA", 670, el(79, debut="2023-01"))],
   reservoir=0, remarques="SUV coupé électrique (ex-C40 Recharge, renommé EC40 en 2024)")
mg(L, "EX30", "SEA", "1", "2023-11", None,
   [("Single Motor 272", "EV-SEA", 343, el(49)), ("Single Motor Extended Range 272", "EV-SEA", 343, el(64)),
    ("Twin Motor Performance 428", "EV-SEA", 543, el(64)), ("Single Motor 150", "EV-SEA", 200, el(49, debut="2026-02")),
    ("Single Motor Extended Range 150", "EV-SEA", 200, el(64, debut="2026-02"))], reservoir=0,
   remarques="SUV urbain électrique ; EX30 Cross Country (2025) ; version 150 ch (millésime 2026)")
mg(L, "EX90", "SPA2", "1", "2024-06", None,
   [("Twin Motor 408", "EV-SPA2", 770, el(107)), ("Twin Motor Performance 517", "EV-SPA2", 910, el(107, fin="2025-08")),
    ("Twin Motor Performance 680", "EV-SPA2", 910, el(107, debut="2025-09"))], places=7, reservoir=0,
   remarques="SUV 7 places électrique ; architecture 800 V et calculateur Orin (millésime 2026)")
mg(L, "ES90", "SPA2-ES90", "1", "2025-09", None,
   [("Single Motor 333", "EV-SPA2", 480, el(88)), ("Twin Motor 449", "EV-SPA2", 670, el(102)),
    ("Twin Motor Performance 680", "EV-SPA2", 870, el(102))], portes=5, reservoir=0,
   remarques="Berline électrique à hayon, 800 V")
mg(L, "EX60", "SPA3", "1", "2026-09", None,
   [("P6 374", "EV-SPA3", 480, el(80)), ("P10 AWD 510", "EV-SPA3", 710, el(95)),
    ("P12 AWD 680", "EV-SPA3", 790, el(117, debut="2027-07"))], reservoir=0,
   remarques="SUV moyen électrique 800 V (plateforme SPA3) ; P12 annoncée pour le 2e semestre 2027")

MOT = Motorisations("Volvo", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Volvo": L}
MOTEURS = MOT.moteurs()
