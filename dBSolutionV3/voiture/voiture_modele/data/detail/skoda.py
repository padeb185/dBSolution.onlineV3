"""Škoda : générations, phases, motorisations (marché européen) et moteurs liés.
Classiques (Octavia et Felicia 1959, 1000 MB, 100/110, 105 à 136, Garde/Rapid coupé, Favorit, Felicia 1994), puis
Fabia, Octavia, Superb, Roomster, Yeti, Citigo, Rapid, Scala, Kamiq, Karoq, Kodiaq, Enyaq, Elroq, Epiq.
Versions RS / Monte Carlo / Scout en variantes. Moteurs VW : familles et codes de volkswagen.py (motoriste « Volkswagen ») ;
moteurs propres (culbutés d'avant 1996) au motoriste « Škoda ». Avant-guerre et utilitaires non repris.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .volkswagen import FAMILLES as FAMILLES_VW

E_, D = "ESS", "DSL"
C = "CHAINE"

PROPRES = {
    "SK-OHV-1.0": f("ATM", E_, 1.0, C, 4, 4800, 3000, "20W50", 3.5, 5000),
    "SK-OHV-1.1": f("ATM", E_, 1.1, C, 4, 5000, 3000, "20W50", 3.5, 5000),
    "SK-OHV-1.2": f("ATM", E_, 1.2, C, 4, 5200, 3250, "20W50", 3.5, 5000),
    "SK-OHV-1.3": f("ATM", E_, 1.3, C, 4, 5000, 3000, "15W40", 4.0, 7500),
}
VW = ("EA111-1.0", "EA111-1.2", "EA111-1.4", "EA111-1.6", "EA111-1.2TSI", "EA111-1.4TSI",
      "EA827-1.6", "EA827-1.8", "EA827-2.0", "EA827-1.9D", "EA113-1.6", "EA113-1.8T", "EA113-2.0FSI", "EA113-2.0TFSI",
      "EA211-1.0MPI", "EA211-1.0TSI", "EA211-1.0eTSI", "EA211-1.2TSI", "EA211-1.4TSI", "EA211-1.5TSI", "EA211-1.5eTSI",
      "EA211-1.4TSI-PHEV", "EA211-1.5TSI-PHEV", "EA888-1.8TSI", "EA888-2.0TSI", "V6-2.8", "VR6-3.6",
      "EA180-1.9SDI", "EA180-1.9TDI", "EA188-1.4TDI", "EA188-2.0TDI", "EA189-1.2TDI", "EA189-1.6TDI", "EA189-2.0TDI",
      "EA288-1.4TDI", "EA288-1.6TDI", "EA288-2.0TDI", "EA288evo-2.0TDI", "V6-2.5TDI", "EUP-EV", "MEB-EV", "MEB-AWD")
FAMILLES = {**{k: FAMILLES_VW[k] for k in VW}, **PROPRES}


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Volkswagen", lambda fam: "Škoda" if fam in PROPRES else "Volkswagen")
L = []
CL = "Données indicatives (modèle ancien), à vérifier"

# ---------------------------------------------------------------- classiques
mg(L, "Octavia", "985", "1", "1959-01", "1971-12", [("1.1 40", "SK-OHV-1.1", 75), ("Super 1.1 50", "SK-OHV-1.1", 80, {"debut": "1960-01"})],
   portes=2, places=4, reservoir=32, remarques=CL + " ; Combi (break) jusqu'en 1971")
mg(L, "Felicia", "994", "1", "1959-01", "1964-12", [("1.1 50", "SK-OHV-1.1", 80)], portes=2, places=4, reservoir=32, remarques=CL + " ; cabriolet")
mg(L, "1000 MB", "MB", "1", "1964-03", "1969-12", [("1000 MB 42", "SK-OHV-1.0", 68), ("1100 MB 52", "SK-OHV-1.1", 82, {"debut": "1967-01"})],
   portes=4, reservoir=32, remarques=CL + " ; moteur arrière")
mg(L, "100", "722", "1", "1969-08", "1977-12", [("100 48", "SK-OHV-1.0", 73), ("110 52", "SK-OHV-1.1", 81)], portes=4, reservoir=32,
   remarques=CL + " ; 110 R coupé")
mg(L, "105", "742", "1", "1976-08", "1990-12",
   [("105 46", "SK-OHV-1.0", 74), ("120 52", "SK-OHV-1.2", 85), ("120 58", "SK-OHV-1.2", 90, {"debut": "1984-01"}),
    ("130 58", "SK-OHV-1.3", 97, {"debut": "1984-08"}), ("136 62", "SK-OHV-1.3", 100, {"debut": "1987-01"})], portes=4, reservoir=37,
   remarques=CL + " ; 105/120 puis 125/130/135/136 ; moteur arrière")
mg(L, "Rapid", "743", "1", "1981-01", "1990-12", [("Garde 1.2 54", "SK-OHV-1.2", 87, {"fin": "1984-12"}), ("Rapid 130 58", "SK-OHV-1.3", 97, {"debut": "1984-01"}),
                                                  ("Rapid 136 62", "SK-OHV-1.3", 100, {"debut": "1987-01"})], portes=2, places=4, reservoir=37,
   remarques=CL + " ; coupé (Garde) puis Rapid")
mg(L, "Favorit", "781", "1", "1987-11", "1995-08", [("1.3 62", "SK-OHV-1.3", 100), ("1.3 68", "SK-OHV-1.3", 106, {"debut": "1991-01"})],
   reservoir=47, remarques=CL + " ; Forman (break) et Pick-up")
mg(L, "Felicia", "6U", "1", "1994-10", "1998-07",
   [("1.3 54", "SK-OHV-1.3", 94), ("1.3 68", "SK-OHV-1.3", 106), ("1.6 75", "EA827-1.6", 135, {"debut": "1995-09"}), ("1.9 D 64", "EA827-1.9D", 124, {"debut": "1995-09"})],
   reservoir=47, remarques="5 portes et Combi")
mg(L, "Felicia", "6U", "2", "1998-08", "2001-06",
   [("1.3 54", "SK-OHV-1.3", 94), ("1.3 68", "SK-OHV-1.3", 106), ("1.6 75", "EA827-1.6", 135), ("1.9 D 64", "EA827-1.9D", 124)], reservoir=47,
   remarques="Restylage")

# ---------------------------------------------------------------- Fabia
mg(L, "Fabia", "6Y", "1", "1999-09", "2004-12",
   [("1.0 50", "EA111-1.0", 86), ("1.4 60", "EA111-1.4", 120), ("1.4 16V 75", "EA111-1.4", 126), ("1.4 16V 100", "EA111-1.4", 126),
    ("2.0 115", "EA827-2.0", 170, {"debut": "2000-09"}), ("1.2 HTP 54", "EA111-1.2", 106, {"debut": "2001-09"}), ("1.9 SDI 64", "EA180-1.9SDI", 125),
    ("1.9 TDI 100", "EA180-1.9TDI", 240), ("1.4 TDI 75", "EA188-1.4TDI", 195, {"debut": "2003-06"})], reservoir=45, remarques="5 portes, Combi, Sedan")
mg(L, "Fabia", "6Y", "2", "2005-01", "2007-12",
   [("1.2 HTP 54", "EA111-1.2", 106), ("1.2 HTP 64", "EA111-1.2", 112), ("1.4 16V 75", "EA111-1.4", 126), ("1.4 16V 100", "EA111-1.4", 126),
    ("2.0 115", "EA827-2.0", 170), ("1.4 TDI 70", "EA188-1.4TDI", 155), ("1.4 TDI 80", "EA188-1.4TDI", 195), ("1.9 TDI 100", "EA180-1.9TDI", 240),
    ("RS 1.9 TDI 130", "EA180-1.9TDI", 310)], reservoir=45, remarques="Restylage ; Fabia RS (2003)")
mg(L, "Fabia", "5J", "1", "2007-04", "2010-03",
   [("1.2 HTP 60", "EA111-1.2", 108), ("1.2 HTP 70", "EA111-1.2", 112), ("1.4 16V 85", "EA111-1.4", 132), ("1.6 16V 105", "EA111-1.6", 153),
    ("1.4 TDI 70", "EA188-1.4TDI", 155), ("1.4 TDI 80", "EA188-1.4TDI", 195), ("1.9 TDI 105", "EA180-1.9TDI", 240)], reservoir=45,
   remarques="5 portes et Combi ; Scout")
mg(L, "Fabia", "5J", "2", "2010-04", "2014-10",
   [("1.2 HTP 60", "EA111-1.2", 108), ("1.2 HTP 70", "EA111-1.2", 112), ("1.2 TSI 86", "EA111-1.2TSI", 160), ("1.2 TSI 105", "EA111-1.2TSI", 175),
    ("RS 1.4 TSI 180", "EA111-1.4TSI", 250), ("1.2 TDI 75", "EA189-1.2TDI", 180), ("1.6 TDI 90", "EA189-1.6TDI", 230), ("1.6 TDI 105", "EA189-1.6TDI", 250)],
   reservoir=45, remarques="Restylage ; Monte Carlo")
mg(L, "Fabia", "NJ", "1", "2014-11", "2018-07",
   [("1.0 MPI 60", "EA211-1.0MPI", 95), ("1.0 MPI 75", "EA211-1.0MPI", 95), ("1.2 TSI 90", "EA211-1.2TSI", 160), ("1.2 TSI 110", "EA211-1.2TSI", 175),
    ("1.0 TSI 95", "EA211-1.0TSI", 160, {"debut": "2016-06"}), ("1.0 TSI 110", "EA211-1.0TSI", 200, {"debut": "2016-06"}),
    ("1.4 TDI 75", "EA288-1.4TDI", 210), ("1.4 TDI 90", "EA288-1.4TDI", 230), ("1.4 TDI 105", "EA288-1.4TDI", 250)], reservoir=45, remarques="5 portes et Combi")
mg(L, "Fabia", "NJ", "2", "2018-08", "2021-08",
   [("1.0 MPI 60", "EA211-1.0MPI", 95), ("1.0 MPI 75", "EA211-1.0MPI", 95), ("1.0 TSI 95", "EA211-1.0TSI", 175), ("1.0 TSI 110", "EA211-1.0TSI", 200)],
   reservoir=45, remarques="Restylage (sans diesel)")
mg(L, "Fabia", "PJ", "1", "2021-09", None,
   [("1.0 MPI 65", "EA211-1.0MPI", 95), ("1.0 MPI 80", "EA211-1.0MPI", 93), ("1.0 TSI 95", "EA211-1.0TSI", 175), ("1.0 TSI 110", "EA211-1.0TSI", 200),
    ("1.5 TSI 150", "EA211-1.5TSI", 250), ("130 1.5 TSI 177", "EA211-1.5TSI", 250, {"debut": "2024-06"})], reservoir=40,
   remarques="MQB A0 ; Monte Carlo ; Fabia 130 (série spéciale)")

# ---------------------------------------------------------------- Octavia
mg(L, "Octavia", "1U", "1", "1996-10", "2000-08",
   [("1.6 75", "EA827-1.6", 135), ("1.6 100", "EA113-1.6", 145), ("1.8 20V 125", "EA827-1.8", 170), ("1.8 20VT 150", "EA113-1.8T", 210),
    ("1.9 SDI 68", "EA180-1.9SDI", 133), ("1.9 TDI 90", "EA180-1.9TDI", 210), ("1.9 TDI 110", "EA180-1.9TDI", 235)], reservoir=55, remarques="Berline et Combi")
mg(L, "Octavia", "1U", "2", "2000-09", "2010-12",
   [("1.4 60", "EA111-1.4", 116), ("1.4 16V 75", "EA111-1.4", 126), ("1.6 102", "EA113-1.6", 148), ("2.0 115", "EA827-2.0", 170),
    ("1.8 20VT 150", "EA113-1.8T", 210), ("RS 1.8 20VT 180", "EA113-1.8T", 235, {"debut": "2001-01"}), ("1.9 SDI 68", "EA180-1.9SDI", 133),
    ("1.9 TDI 90", "EA180-1.9TDI", 210), ("1.9 TDI 100", "EA180-1.9TDI", 240), ("1.9 TDI 130", "EA180-1.9TDI", 310)], reservoir=55,
   remarques="Restylage ; Octavia Tour vendue jusqu'en 2010")
mg(L, "Octavia", "1Z", "1", "2004-06", "2008-11",
   [("1.4 75", "EA111-1.4", 126), ("1.6 102", "EA113-1.6", 148), ("1.6 FSI 115", "EA113-1.6", 155), ("2.0 FSI 150", "EA113-2.0FSI", 200),
    ("1.8 TSI 160", "EA888-1.8TSI", 250, {"debut": "2007-01"}), ("RS 2.0 TFSI 200", "EA113-2.0TFSI", 280, {"debut": "2005-10"}),
    ("1.9 TDI 105", "EA180-1.9TDI", 250), ("2.0 TDI 140", "EA188-2.0TDI", 320), ("RS 2.0 TDI 170", "EA188-2.0TDI", 350, {"debut": "2006-09"})],
   reservoir=55, remarques="Berline et Combi ; Scout (2007)")
mg(L, "Octavia", "1Z", "2", "2008-12", "2013-03",
   [("1.4 80", "EA111-1.4", 132), ("1.2 TSI 105", "EA111-1.2TSI", 175, {"debut": "2010-01"}), ("1.4 TSI 122", "EA111-1.4TSI", 200),
    ("1.8 TSI 160", "EA888-1.8TSI", 250), ("RS 2.0 TFSI 200", "EA113-2.0TFSI", 280), ("1.6 TDI 105", "EA189-1.6TDI", 250),
    ("2.0 TDI 140", "EA189-2.0TDI", 320), ("RS 2.0 TDI 170", "EA189-2.0TDI", 350), ("1.9 TDI 105", "EA180-1.9TDI", 250, {"fin": "2010-06"})],
   reservoir=55, remarques="Restylage")
mg(L, "Octavia", "5E", "1", "2013-03", "2016-12",
   [("1.2 TSI 86", "EA211-1.2TSI", 160), ("1.2 TSI 105", "EA211-1.2TSI", 175), ("1.4 TSI 140", "EA211-1.4TSI", 250), ("1.8 TSI 180", "EA888-1.8TSI", 250),
    ("RS 2.0 TSI 220", "EA888-2.0TSI", 350), ("RS 230 2.0 TSI 230", "EA888-2.0TSI", 350, {"debut": "2015-06"}),
    ("1.6 TDI 90", "EA288-1.6TDI", 230), ("1.6 TDI 105", "EA288-1.6TDI", 250), ("1.6 TDI 110", "EA288-1.6TDI", 250, {"debut": "2014-01"}),
    ("2.0 TDI 150", "EA288-2.0TDI", 320), ("RS 2.0 TDI 184", "EA288-2.0TDI", 380), ("1.0 TSI 115", "EA211-1.0TSI", 200, {"debut": "2016-01"})],
   reservoir=50, remarques="Berline et Combi ; Scout")
mg(L, "Octavia", "5E", "2", "2017-01", "2020-03",
   [("1.0 TSI 115", "EA211-1.0TSI", 200), ("1.4 TSI 150", "EA211-1.4TSI", 250, {"fin": "2018-06"}), ("1.5 TSI 150", "EA211-1.5TSI", 250, {"debut": "2018-06"}),
    ("1.8 TSI 180", "EA888-1.8TSI", 250), ("RS 2.0 TSI 230", "EA888-2.0TSI", 350), ("RS 245 2.0 TSI 245", "EA888-2.0TSI", 370, {"debut": "2017-09"}),
    ("1.6 TDI 115", "EA288-1.6TDI", 250), ("2.0 TDI 150", "EA288-2.0TDI", 340), ("RS 2.0 TDI 184", "EA288-2.0TDI", 380)], reservoir=50, remarques="Restylage")
mg(L, "Octavia", "NX", "1", "2020-03", "2024-02",
   [("1.0 TSI 110", "EA211-1.0TSI", 200), ("1.0 eTSI 110", "EA211-1.0eTSI", 200), ("1.5 TSI 150", "EA211-1.5TSI", 250), ("1.5 eTSI 150", "EA211-1.5eTSI", 250),
    ("2.0 TSI 190", "EA888-2.0TSI", 320), ("RS 2.0 TSI 245", "EA888-2.0TSI", 370), ("1.4 iV 204", "EA211-1.4TSI-PHEV", 350, ph(13, 40)),
    ("RS iV 245", "EA211-1.4TSI-PHEV", 400, ph(13, 40)), ("2.0 TDI 115", "EA288evo-2.0TDI", 300), ("2.0 TDI 150", "EA288evo-2.0TDI", 360),
    ("RS 2.0 TDI 200", "EA288evo-2.0TDI", 400)], reservoir=50, remarques="Berline et Combi ; Scout")
mg(L, "Octavia", "NX", "2", "2024-03", None,
   [("1.5 TSI 115", "EA211-1.5TSI", 220), ("1.5 TSI 150", "EA211-1.5TSI", 250), ("1.5 eTSI 150", "EA211-1.5eTSI", 250), ("2.0 TSI 204", "EA888-2.0TSI", 320),
    ("RS 2.0 TSI 265", "EA888-2.0TSI", 370), ("2.0 TDI 115", "EA288evo-2.0TDI", 300), ("2.0 TDI 150", "EA288evo-2.0TDI", 360),
    ("RS 2.0 TDI 193", "EA288evo-2.0TDI", 400)], reservoir=45, remarques="Restylage")

# ---------------------------------------------------------------- Superb
mg(L, "Superb", "3U", "1", "2001-12", "2008-03",
   [("1.8 20VT 150", "EA113-1.8T", 210), ("2.0 115", "EA827-2.0", 170), ("2.8 V6 193", "V6-2.8", 280), ("1.9 TDI 130", "EA180-1.9TDI", 310),
    ("2.0 TDI 140", "EA188-2.0TDI", 320, {"debut": "2005-06"}), ("2.5 V6 TDI 163", "V6-2.5TDI", 350)], portes=4, reservoir=62, remarques="Berline (base VW Passat B5)")
mg(L, "Superb", "3T", "1", "2008-03", "2013-05",
   [("1.4 TSI 125", "EA111-1.4TSI", 200), ("1.8 TSI 160", "EA888-1.8TSI", 250), ("2.0 TSI 200", "EA888-2.0TSI", 280, {"debut": "2010-01"}),
    ("3.6 V6 260", "VR6-3.6", 350), ("1.6 TDI 105", "EA189-1.6TDI", 250, {"debut": "2010-01"}), ("1.9 TDI 105", "EA180-1.9TDI", 250, {"fin": "2009-12"}),
    ("2.0 TDI 140", "EA189-2.0TDI", 320), ("2.0 TDI 170", "EA189-2.0TDI", 350)], reservoir=60, remarques="Berline Twindoor et Combi (2009)")
mg(L, "Superb", "3T", "2", "2013-06", "2015-04",
   [("1.4 TSI 125", "EA111-1.4TSI", 200), ("1.8 TSI 160", "EA888-1.8TSI", 250), ("2.0 TSI 200", "EA888-2.0TSI", 280), ("3.6 V6 260", "VR6-3.6", 350),
    ("1.6 TDI 105", "EA189-1.6TDI", 250), ("2.0 TDI 140", "EA189-2.0TDI", 320), ("2.0 TDI 170", "EA189-2.0TDI", 350)], reservoir=60, remarques="Restylage")
mg(L, "Superb", "3V", "1", "2015-05", "2019-08",
   [("1.4 TSI 125", "EA211-1.4TSI", 200), ("1.4 TSI 150", "EA211-1.4TSI", 250), ("1.5 TSI 150", "EA211-1.5TSI", 250, {"debut": "2018-06"}),
    ("2.0 TSI 220", "EA888-2.0TSI", 350), ("2.0 TSI 280", "EA888-2.0TSI", 350), ("1.6 TDI 120", "EA288-1.6TDI", 250),
    ("2.0 TDI 150", "EA288-2.0TDI", 340), ("2.0 TDI 190", "EA288-2.0TDI", 400)], reservoir=66, remarques="Berline et Combi")
mg(L, "Superb", "3V", "2", "2019-09", "2023-10",
   [("1.5 TSI 150", "EA211-1.5TSI", 250), ("2.0 TSI 190", "EA888-2.0TSI", 320), ("2.0 TSI 272", "EA888-2.0TSI", 350), ("iV 218", "EA211-1.4TSI-PHEV", 400, ph(13, 50)),
    ("2.0 TDI 122", "EA288evo-2.0TDI", 320), ("2.0 TDI 150", "EA288evo-2.0TDI", 360), ("2.0 TDI 200", "EA288evo-2.0TDI", 400)], reservoir=66,
   remarques="Restylage ; Scout")
mg(L, "Superb", "3Y", "1", "2024-01", None,
   [("1.5 eTSI 150", "EA211-1.5eTSI", 250), ("2.0 TSI 204", "EA888-2.0TSI", 320), ("2.0 TSI 265", "EA888-2.0TSI", 400), ("iV 204", "EA211-1.5TSI-PHEV", 350, ph(25, 45)),
    ("2.0 TDI 122", "EA288evo-2.0TDI", 320), ("2.0 TDI 150", "EA288evo-2.0TDI", 360), ("2.0 TDI 193", "EA288evo-2.0TDI", 400)], reservoir=66,
   remarques="Berline et Combi (Bratislava)")

# ---------------------------------------------------------------- monospaces / petites
mg(L, "Roomster", "5J7", "1", "2006-06", "2015-05",
   [("1.2 HTP 64", "EA111-1.2", 112, {"fin": "2010-03"}), ("1.2 HTP 70", "EA111-1.2", 112), ("1.4 16V 85", "EA111-1.4", 132), ("1.6 16V 105", "EA111-1.6", 153, {"fin": "2010-03"}),
    ("1.2 TSI 86", "EA111-1.2TSI", 160, {"debut": "2010-04"}), ("1.2 TSI 105", "EA111-1.2TSI", 175, {"debut": "2010-04"}),
    ("1.4 TDI 80", "EA188-1.4TDI", 195, {"fin": "2010-03"}), ("1.9 TDI 105", "EA180-1.9TDI", 240, {"fin": "2010-03"}),
    ("1.2 TDI 75", "EA189-1.2TDI", 180, {"debut": "2010-04"}), ("1.6 TDI 90", "EA189-1.6TDI", 230, {"debut": "2010-04"}),
    ("1.6 TDI 105", "EA189-1.6TDI", 250, {"debut": "2010-04"})], reservoir=55, remarques="Ludospace ; restylage 2010 ; Scout")
mg(L, "Citigo", "AA", "1", "2011-11", "2019-08", [("1.0 MPI 60", "EA211-1.0MPI", 95), ("1.0 MPI 75", "EA211-1.0MPI", 95)], portes=3, places=4, reservoir=35,
   remarques="Jumelle VW up! (3 et 5 portes) ; restylage 2017")
mg(L, "Citigo", "AA", "2", "2019-09", "2020-12", [("e iV 83", "EUP-EV", 212, el(37))], places=4, reservoir=0, remarques="Citigo e iV électrique")
mg(L, "Rapid", "NH", "1", "2012-10", "2019-06",
   [("1.2 MPI 75", "EA111-1.2", 112, {"fin": "2015-06"}), ("1.2 TSI 86", "EA211-1.2TSI", 160), ("1.2 TSI 105", "EA211-1.2TSI", 175),
    ("1.0 TSI 95", "EA211-1.0TSI", 160, {"debut": "2017-01"}), ("1.0 TSI 110", "EA211-1.0TSI", 200, {"debut": "2017-01"}), ("1.4 TSI 125", "EA211-1.4TSI", 200),
    ("1.6 TDI 90", "EA189-1.6TDI", 230), ("1.6 TDI 105", "EA189-1.6TDI", 250), ("1.4 TDI 90", "EA288-1.4TDI", 230, {"debut": "2015-06"}),
    ("1.6 TDI 116", "EA288-1.6TDI", 250, {"debut": "2015-06"})], reservoir=55, remarques="5 portes (liftback) et Spaceback (2013) ; restylage 2017")
mg(L, "Scala", "NW", "1", "2019-04", "2024-03",
   [("1.0 TSI 95", "EA211-1.0TSI", 175), ("1.0 TSI 110", "EA211-1.0TSI", 200), ("1.5 TSI 150", "EA211-1.5TSI", 250), ("1.6 TDI 115", "EA288-1.6TDI", 250, {"fin": "2021-12"})],
   reservoir=50, remarques="Compacte (MQB A0) ; Monte Carlo")
mg(L, "Scala", "NW", "2", "2024-04", None, [("1.0 TSI 95", "EA211-1.0TSI", 175), ("1.0 TSI 116", "EA211-1.0TSI", 200), ("1.5 TSI 150", "EA211-1.5TSI", 250)],
   reservoir=50, remarques="Restylage")

# ---------------------------------------------------------------- SUV
mg(L, "Yeti", "5L", "1", "2009-06", "2013-08",
   [("1.2 TSI 105", "EA111-1.2TSI", 175), ("1.4 TSI 122", "EA111-1.4TSI", 200), ("1.8 TSI 160", "EA888-1.8TSI", 250), ("1.6 TDI 105", "EA189-1.6TDI", 250),
    ("2.0 TDI 110", "EA189-2.0TDI", 250), ("2.0 TDI 140", "EA189-2.0TDI", 320), ("2.0 TDI 170", "EA189-2.0TDI", 350)], reservoir=60, remarques="SUV compact, 4x4")
mg(L, "Yeti", "5L", "2", "2013-09", "2017-10",
   [("1.2 TSI 105", "EA211-1.2TSI", 175), ("1.4 TSI 125", "EA211-1.4TSI", 200), ("1.4 TSI 150", "EA211-1.4TSI", 250, {"debut": "2015-06"}), ("1.8 TSI 160", "EA888-1.8TSI", 250),
    ("1.6 TDI 105", "EA189-1.6TDI", 250), ("2.0 TDI 110", "EA189-2.0TDI", 250), ("2.0 TDI 150", "EA288-2.0TDI", 340), ("2.0 TDI 170", "EA189-2.0TDI", 350)],
   reservoir=60, remarques="Restylage (Yeti et Yeti Outdoor)")
mg(L, "Kamiq", "NW4", "1", "2019-09", "2024-03",
   [("1.0 TSI 95", "EA211-1.0TSI", 175), ("1.0 TSI 110", "EA211-1.0TSI", 200), ("1.5 TSI 150", "EA211-1.5TSI", 250), ("1.6 TDI 115", "EA288-1.6TDI", 250, {"fin": "2021-12"})],
   reservoir=50, remarques="SUV urbain ; Monte Carlo")
mg(L, "Kamiq", "NW4", "2", "2024-04", None, [("1.0 TSI 95", "EA211-1.0TSI", 175), ("1.0 TSI 116", "EA211-1.0TSI", 200), ("1.5 TSI 150", "EA211-1.5TSI", 250)],
   reservoir=50, remarques="Restylage")
mg(L, "Karoq", "NU", "1", "2017-09", "2021-12",
   [("1.0 TSI 115", "EA211-1.0TSI", 200), ("1.5 TSI 150", "EA211-1.5TSI", 250), ("2.0 TSI 190", "EA888-2.0TSI", 320, {"debut": "2018-06"}),
    ("1.6 TDI 115", "EA288-1.6TDI", 250), ("2.0 TDI 150", "EA288-2.0TDI", 340), ("2.0 TDI 190", "EA288-2.0TDI", 400)], reservoir=50, remarques="SUV compact ; Scout, Sportline")
mg(L, "Karoq", "NU", "2", "2022-01", None,
   [("1.0 TSI 110", "EA211-1.0TSI", 200), ("1.5 TSI 150", "EA211-1.5TSI", 250), ("2.0 TSI 190", "EA888-2.0TSI", 320), ("2.0 TDI 115", "EA288evo-2.0TDI", 300),
    ("2.0 TDI 150", "EA288evo-2.0TDI", 360)], reservoir=50, remarques="Restylage")
mg(L, "Kodiaq", "NS", "1", "2016-10", "2021-03",
   [("1.4 TSI 125", "EA211-1.4TSI", 200), ("1.4 TSI 150", "EA211-1.4TSI", 250, {"fin": "2019-06"}), ("1.5 TSI 150", "EA211-1.5TSI", 250, {"debut": "2019-06"}),
    ("2.0 TSI 180", "EA888-2.0TSI", 320), ("2.0 TDI 150", "EA288-2.0TDI", 340), ("2.0 TDI 190", "EA288-2.0TDI", 400),
    ("RS 2.0 BiTDI 240", "EA288-2.0TDI", 500, {"debut": "2018-10"})], places=7, reservoir=60, remarques="SUV 5 ou 7 places ; Scout, Sportline")
mg(L, "Kodiaq", "NS", "2", "2021-04", "2024-01",
   [("1.5 TSI 150", "EA211-1.5TSI", 250), ("2.0 TSI 190", "EA888-2.0TSI", 320), ("RS 2.0 TSI 245", "EA888-2.0TSI", 370), ("2.0 TDI 150", "EA288evo-2.0TDI", 360),
    ("2.0 TDI 200", "EA288evo-2.0TDI", 400)], places=7, reservoir=60, remarques="Restylage")
mg(L, "Kodiaq", "PS", "1", "2024-02", None,
   [("1.5 eTSI 150", "EA211-1.5eTSI", 250), ("2.0 TSI 204", "EA888-2.0TSI", 320), ("RS 2.0 TSI 265", "EA888-2.0TSI", 400, {"debut": "2024-10"}),
    ("iV 204", "EA211-1.5TSI-PHEV", 350, ph(25, 45)), ("2.0 TDI 150", "EA288evo-2.0TDI", 360), ("2.0 TDI 193", "EA288evo-2.0TDI", 400)], places=7, reservoir=58,
   remarques="2e génération (Kvasiny)")
mg(L, "Enyaq", "MEB", "1", "2020-11", "2025-02",
   [("iV 50 148", "MEB-EV", 220, el(52)), ("iV 60 180", "MEB-EV", 310, el(58)), ("iV 80 204", "MEB-EV", 310, el(77)),
    ("iV 80x 265", "MEB-AWD", 425, el(77)), ("RS 299", "MEB-AWD", 460, el(77, debut="2022-03")), ("85 286", "MEB-EV", 545, el(77, debut="2023-06"))],
   reservoir=0, remarques="SUV électrique ; Coupé (2022)")
mg(L, "Enyaq", "MEB", "2", "2025-03", None,
   [("60 204", "MEB-EV", 310, el(59)), ("85 286", "MEB-EV", 545, el(77)), ("85x 286", "MEB-AWD", 545, el(77)), ("RS 340", "MEB-AWD", 545, el(79))],
   reservoir=0, remarques="Restylage (Modern Solid), Coupé")
mg(L, "Elroq", "MEB", "E", "2024-11", None,
   [("50 170", "MEB-EV", 310, el(52)), ("60 204", "MEB-EV", 310, el(59)), ("85 286", "MEB-EV", 545, el(77)), ("RS 340", "MEB-AWD", 545, el(79, debut="2025-06"))],
   reservoir=0, remarques="SUV compact électrique")
mg(L, "Epiq", "MEB+", "1", "2026-09", None,
   [("35 115", "MEB-EV", 267, el(38)), ("40 135", "MEB-EV", 267, el(38)), ("55 211", "MEB-EV", 290, el(55))], reservoir=0,
   remarques="SUV urbain électrique, traction ; couple de l'Epiq 55 indicatif")

MOT = Motorisations("Volkswagen", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Skoda": L}
MOTEURS = MOT.moteurs()
