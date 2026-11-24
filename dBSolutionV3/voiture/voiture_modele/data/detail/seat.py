"""SEAT : générations, phases, motorisations (marché européen) et moteurs liés.
Classiques (600, 850, 124, 127, 131, Ronda, Malaga, Marbella), Ibiza, Cordoba, Toledo, Leon (versions Cupra d'avant 2018
comprises), Altea, Alhambra, Arosa, Mii, Exeo, Ateca, Arona, Tarraco. Les Cupra depuis 2018 sont dans la marque Cupra.
Moteurs VW/Audi : familles et codes de volkswagen.py (motoriste « Volkswagen ») ; moteurs propres (classiques sous licence
Fiat, System Porsche) au motoriste « SEAT ». Saisie : (nom, famille, couple_nm[, surcharges]) ; puissance = dernier nombre."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .volkswagen import FAMILLES as FAMILLES_VW

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

PROPRES = {
    "SEAT-0.6": f("ATM", E_, 0.6, C, 4, 4800, 3400, "20W50", 2.5, 5000),
    "SEAT-0.85": f("ATM", E_, 0.85, C, 4, 5300, 3500, "20W50", 3.0, 5000),
    "SEAT-0.9": f("ATM", E_, 0.9, C, 4, 5600, 3000, "20W50", 3.5, 5000),
    "SEAT-1.2": f("ATM", E_, 1.2, C, 4, 5600, 3300, "20W50", 4.0, 5000),
    "SEAT-1.4": f("ATM", E_, 1.4, B, 4, 5800, 3500, "20W50", 4.0, 7500),
    "SEAT-1.6": f("ATM", E_, 1.6, B, 4, 6000, 4000, "20W50", 4.0, 7500),
    "SEAT-2.0": f("ATM", E_, 2.0, B, 4, 5800, 3500, "20W50", 4.5, 7500),
    "SEAT-1.7D": f("ATM", D, 1.7, B, 4, 4500, 2500, "15W40", 4.5, 7500),
    "PORSCHE-1.2": f("ATM", E_, 1.2, B, 4, 5800, 3500, "15W40", 3.75, 10000),
    "PORSCHE-1.5": f("ATM", E_, 1.5, B, 4, 5800, 3500, "15W40", 3.75, 10000),
}
VW = ("EA111-1.0", "EA111-1.2", "EA111-1.4", "EA111-1.6", "EA111-1.4FSI", "EA111-1.2TSI", "EA111-1.4TSI",
      "EA827-1.6", "EA827-1.8", "EA827-2.0", "EA827-1.9D", "EA827-1.9TD", "EA827-2.0-16v",
      "EA113-1.6", "EA113-1.8T", "EA113-2.0FSI", "EA113-2.0TFSI",
      "EA211-1.0MPI", "EA211-1.0TSI", "EA211-1.0eTSI", "EA211-1.2TSI", "EA211-1.4TSI", "EA211-1.5TSI", "EA211-1.5eTSI",
      "EA211-1.4TSI-PHEV", "EA211-1.5TSI-PHEV", "EA888-1.8TSI", "EA888-2.0TSI", "VR6-2.8", "EA390-2.3V5",
      "EA180-1.9SDI", "EA180-1.9TDI", "EA188-1.4TDI", "EA188-2.0TDI", "EA189-1.2TDI", "EA189-1.6TDI", "EA189-2.0TDI",
      "EA288-1.6TDI", "EA288-2.0TDI", "EA288evo-2.0TDI", "EUP-EV")
FAMILLES = {**{k: FAMILLES_VW[k] for k in VW}, **PROPRES}


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Volkswagen", lambda fam: "SEAT" if fam in PROPRES else "Volkswagen")
L = []
CL = "Données indicatives (modèle ancien), à vérifier"

# ---------------------------------------------------------------- classiques (licence Fiat)
mg(L, "600", "600", "1", "1957-06", "1973-08", [("600 19", "SEAT-0.6", 39), ("600 D 25", "SEAT-0.6", 39, {"debut": "1963-01"}),
                                                 ("600 E 25", "SEAT-0.6", 39, {"debut": "1970-01"})], portes=2, places=4, reservoir=27, remarques=CL)
mg(L, "850", "850", "1", "1966-01", "1974-12", [("850 37", "SEAT-0.85", 56)], portes=2, places=4, reservoir=30, remarques=CL)
mg(L, "124", "124", "1", "1968-01", "1980-12", [("124 1.2 60", "SEAT-1.2", 88), ("124 1430 70", "SEAT-1.4", 108, {"debut": "1969-01"}),
                                                 ("124 Sport 1.6 90", "SEAT-1.6", 128, {"debut": "1974-01"})], portes=4, reservoir=39, remarques=CL)
mg(L, "127", "127", "1", "1972-04", "1982-12", [("127 0.9 43", "SEAT-0.9", 64)], portes=2, places=5, reservoir=30, remarques=CL)
mg(L, "131", "131", "1", "1975-01", "1982-12", [("131 1.4 75", "SEAT-1.4", 108), ("131 1.6 85", "SEAT-1.6", 125), ("131 2.0 100", "SEAT-2.0", 160, {"debut": "1978-01"})],
   portes=4, reservoir=50, remarques=CL)
mg(L, "Ronda", "Ronda", "1", "1982-06", "1986-12", [("1.2 63", "SEAT-1.2", 88), ("1.6 95", "SEAT-1.6", 128), ("1.7 D 55", "SEAT-1.7D", 103)],
   portes=3, reservoir=50, remarques=CL + " ; dérivée de la Fiat Ritmo")
mg(L, "Marbella", "Marbella", "1", "1986-01", "1998-12", [("0.9 40", "SEAT-0.9", 64)], portes=3, places=4, reservoir=30, remarques=CL + " ; base Fiat Panda")
mg(L, "Malaga", "Malaga", "1", "1985-01", "1991-12", [("1.2 63", "PORSCHE-1.2", 92), ("1.5 85", "PORSCHE-1.5", 120), ("1.7 D 55", "SEAT-1.7D", 103)],
   portes=4, reservoir=50, remarques=CL + " ; moteurs System Porsche")

# ---------------------------------------------------------------- Ibiza / Cordoba
mg(L, "Ibiza", "021A", "1", "1984-06", "1993-03",
   [("1.2 63", "PORSCHE-1.2", 92), ("1.5 85", "PORSCHE-1.5", 120), ("1.5 i 100", "PORSCHE-1.5", 125, {"debut": "1989-01"}), ("1.7 D 55", "SEAT-1.7D", 103)],
   portes=3, reservoir=50, remarques=CL + " ; moteurs System Porsche, restylage 1991")
mg(L, "Ibiza", "6K", "1", "1993-04", "1999-08",
   [("1.0 50", "EA111-1.0", 86), ("1.4 60", "EA111-1.4", 116), ("1.6 75", "EA827-1.6", 125), ("1.8 90", "EA827-1.8", 145), ("GTi 2.0 115", "EA827-2.0", 166),
    ("GTi 2.0 16V 150", "EA827-2.0-16v", 180, {"debut": "1996-01"}), ("Cupra 2.0 16V 150", "EA827-2.0-16v", 180, {"debut": "1996-06"}),
    ("1.9 D 64", "EA827-1.9D", 124), ("1.9 TD 75", "EA827-1.9TD", 150), ("1.9 TDI 90", "EA180-1.9TDI", 202)], portes=3, reservoir=45,
   remarques="3 et 5 portes")
mg(L, "Ibiza", "6K", "2", "1999-09", "2002-02",
   [("1.0 50", "EA111-1.0", 86), ("1.4 60", "EA111-1.4", 116), ("1.4 16V 75", "EA111-1.4", 126), ("1.6 100", "EA113-1.6", 145),
    ("Cupra 1.8 20VT 156", "EA113-1.8T", 220), ("1.9 SDI 68", "EA180-1.9SDI", 133), ("1.9 TDI 90", "EA180-1.9TDI", 210),
    ("1.9 TDI 110", "EA180-1.9TDI", 235)], portes=3, reservoir=45, remarques="Restylage")
mg(L, "Ibiza", "6L", "1", "2002-03", "2008-04",
   [("1.2 64", "EA111-1.2", 112), ("1.4 75", "EA111-1.4", 126), ("1.4 16V 100", "EA111-1.4", 130), ("2.0 115", "EA827-2.0", 170),
    ("FR 1.8 20VT 150", "EA113-1.8T", 220, {"debut": "2004-01"}), ("Cupra 1.8 20VT 180", "EA113-1.8T", 235, {"debut": "2004-01"}),
    ("1.4 TDI 80", "EA188-1.4TDI", 195), ("1.9 TDI 100", "EA180-1.9TDI", 240), ("1.9 TDI 130", "EA180-1.9TDI", 310),
    ("Cupra 1.9 TDI 160", "EA180-1.9TDI", 330, {"debut": "2004-01"})], portes=3, reservoir=45, remarques="3 et 5 portes ; restylage 2006")
mg(L, "Ibiza", "6J", "1", "2008-05", "2012-04",
   [("1.2 70", "EA111-1.2", 112), ("1.4 85", "EA111-1.4", 132), ("1.6 105", "EA111-1.6", 153), ("1.2 TSI 105", "EA111-1.2TSI", 175, {"debut": "2010-01"}),
    ("FR 1.4 TSI 150", "EA111-1.4TSI", 220, {"debut": "2009-06"}), ("Cupra 1.4 TSI 180", "EA111-1.4TSI", 250, {"debut": "2009-06"}),
    ("1.2 TDI 75", "EA189-1.2TDI", 180, {"debut": "2010-01"}), ("1.6 TDI 90", "EA189-1.6TDI", 230, {"debut": "2010-01"}),
    ("1.6 TDI 105", "EA189-1.6TDI", 250, {"debut": "2010-01"}), ("1.9 TDI 105", "EA180-1.9TDI", 240, {"fin": "2009-12"})], portes=3, reservoir=45,
   remarques="SC 3 portes, 5 portes, ST break (2010)")
mg(L, "Ibiza", "6J", "2", "2012-05", "2017-05",
   [("1.2 70", "EA111-1.2", 112, {"fin": "2014-12"}), ("1.0 MPI 75", "EA211-1.0MPI", 95, {"debut": "2015-01"}), ("1.2 TSI 90", "EA211-1.2TSI", 160),
    ("1.0 TSI 95", "EA211-1.0TSI", 160, {"debut": "2015-06"}), ("1.0 TSI 110", "EA211-1.0TSI", 200, {"debut": "2015-06"}),
    ("FR 1.4 TSI 150", "EA211-1.4TSI", 250), ("Cupra 1.4 TSI 180", "EA111-1.4TSI", 250, {"fin": "2014-12"}),
    ("Cupra 1.8 TSI 192", "EA888-1.8TSI", 320, {"debut": "2015-06"}), ("1.2 TDI 75", "EA189-1.2TDI", 180, {"fin": "2014-12"}),
    ("1.4 TDI 90", "EA288-1.6TDI", 230, {"debut": "2015-01"}), ("1.6 TDI 105", "EA189-1.6TDI", 250, {"fin": "2014-12"})],
   portes=3, reservoir=45, remarques="Restylage")
mg(L, "Ibiza", "KJ", "1", "2017-06", "2021-03",
   [("1.0 MPI 75", "EA211-1.0MPI", 95), ("1.0 TSI 95", "EA211-1.0TSI", 175), ("1.0 TSI 115", "EA211-1.0TSI", 200),
    ("1.5 TSI 150", "EA211-1.5TSI", 250, {"debut": "2018-06"}), ("1.6 TDI 80", "EA288-1.6TDI", 250), ("1.6 TDI 95", "EA288-1.6TDI", 250),
    ("1.6 TDI 115", "EA288-1.6TDI", 250)], reservoir=40, remarques="Plateforme MQB A0")
mg(L, "Ibiza", "KJ", "2", "2021-04", None,
   [("1.0 MPI 80", "EA211-1.0MPI", 93), ("1.0 TSI 95", "EA211-1.0TSI", 175), ("1.0 TSI 110", "EA211-1.0TSI", 200), ("1.5 TSI 150", "EA211-1.5TSI", 250)],
   reservoir=40, remarques="Restylage 2021 ; restylage 2025 non détaillé")
mg(L, "Cordoba", "6K", "1", "1993-09", "2002-12",
   [("1.4 60", "EA111-1.4", 116), ("1.6 75", "EA827-1.6", 125), ("1.8 90", "EA827-1.8", 145), ("2.0 115", "EA827-2.0", 166),
    ("1.9 TD 75", "EA827-1.9TD", 150), ("1.9 TDI 90", "EA180-1.9TDI", 202), ("1.9 TDI 110", "EA180-1.9TDI", 235, {"debut": "1999-09"})],
   portes=4, reservoir=45, remarques="Berline, Vario, Coupé ; restylage 1999")
mg(L, "Cordoba", "6L", "1", "2002-09", "2009-12",
   [("1.4 75", "EA111-1.4", 126), ("1.4 16V 100", "EA111-1.4", 130), ("2.0 115", "EA827-2.0", 170), ("1.4 TDI 80", "EA188-1.4TDI", 195),
    ("1.9 TDI 100", "EA180-1.9TDI", 240), ("1.9 TDI 130", "EA180-1.9TDI", 310)], portes=4, reservoir=45)

# ---------------------------------------------------------------- Toledo / Leon
mg(L, "Toledo", "1L", "1", "1991-05", "1999-03",
   [("1.6 75", "EA827-1.6", 125), ("1.8 90", "EA827-1.8", 145), ("2.0 115", "EA827-2.0", 166), ("2.0 16V 150", "EA827-2.0-16v", 180),
    ("1.9 TD 75", "EA827-1.9TD", 150), ("1.9 TDI 90", "EA180-1.9TDI", 202)], reservoir=55, remarques=CL)
mg(L, "Toledo", "1M", "1", "1999-04", "2004-12",
   [("1.6 100", "EA113-1.6", 145), ("1.8 20V 125", "EA827-1.8", 170), ("2.3 V5 150", "EA390-2.3V5", 205), ("1.9 TDI 90", "EA180-1.9TDI", 210),
    ("1.9 TDI 110", "EA180-1.9TDI", 235), ("1.9 TDI 150", "EA180-1.9TDI", 320, {"debut": "2001-06"})], portes=4, reservoir=55)
mg(L, "Toledo", "5P", "1", "2004-10", "2009-05",
   [("1.6 102", "EA113-1.6", 148), ("2.0 FSI 150", "EA113-2.0FSI", 200), ("1.9 TDI 105", "EA180-1.9TDI", 250), ("2.0 TDI 140", "EA188-2.0TDI", 320)],
   reservoir=55, remarques="Monospace 5 portes (base Altea)")
mg(L, "Toledo", "NH", "1", "2012-10", "2019-04",
   [("1.2 MPI 75", "EA111-1.2", 112), ("1.2 TSI 90", "EA211-1.2TSI", 160), ("1.2 TSI 105", "EA211-1.2TSI", 175), ("1.0 TSI 95", "EA211-1.0TSI", 160, {"debut": "2015-06"}),
    ("1.0 TSI 110", "EA211-1.0TSI", 200, {"debut": "2015-06"}), ("1.4 TSI 125", "EA211-1.4TSI", 200), ("1.6 TDI 90", "EA189-1.6TDI", 230),
    ("1.6 TDI 105", "EA189-1.6TDI", 250), ("1.6 TDI 115", "EA288-1.6TDI", 250, {"debut": "2015-06"})], reservoir=55,
   remarques="5 portes (jumelle de la Skoda Rapid)")
mg(L, "Leon", "1M", "1", "1999-09", "2005-12",
   [("1.4 16V 75", "EA111-1.4", 126), ("1.6 100", "EA113-1.6", 145), ("1.8 20V 125", "EA827-1.8", 170), ("1.8 20VT 180", "EA113-1.8T", 235),
    ("Cupra 2.8 V6 204", "VR6-2.8", 270, {"fin": "2002-12"}), ("Cupra R 1.8 20VT 210", "EA113-1.8T", 270, {"debut": "2002-01", "fin": "2003-06"}),
    ("Cupra R 1.8 20VT 225", "EA113-1.8T", 280, {"debut": "2003-07"}), ("1.9 SDI 68", "EA180-1.9SDI", 133), ("1.9 TDI 90", "EA180-1.9TDI", 210),
    ("1.9 TDI 110", "EA180-1.9TDI", 235), ("1.9 TDI 150", "EA180-1.9TDI", 320, {"debut": "2001-06"})], reservoir=55)
mg(L, "Leon", "1P", "1", "2005-06", "2009-04",
   [("1.4 85", "EA111-1.4", 132), ("1.6 102", "EA113-1.6", 148), ("2.0 FSI 150", "EA113-2.0FSI", 200), ("FR 2.0 TFSI 200", "EA113-2.0TFSI", 280),
    ("Cupra 2.0 TFSI 240", "EA113-2.0TFSI", 300, {"debut": "2007-01"}), ("1.9 TDI 105", "EA180-1.9TDI", 250), ("2.0 TDI 140", "EA188-2.0TDI", 320),
    ("FR 2.0 TDI 170", "EA188-2.0TDI", 350, {"debut": "2006-09"})], reservoir=55)
mg(L, "Leon", "1P", "2", "2009-05", "2012-11",
   [("1.4 85", "EA111-1.4", 132), ("1.2 TSI 105", "EA111-1.2TSI", 175, {"debut": "2010-01"}), ("1.4 TSI 125", "EA111-1.4TSI", 200),
    ("1.8 TSI 160", "EA888-1.8TSI", 250), ("FR 2.0 TFSI 211", "EA113-2.0TFSI", 280), ("Cupra 2.0 TFSI 240", "EA113-2.0TFSI", 300),
    ("Cupra R 2.0 TFSI 265", "EA113-2.0TFSI", 350, {"debut": "2010-06"}), ("1.6 TDI 90", "EA189-1.6TDI", 230), ("1.6 TDI 105", "EA189-1.6TDI", 250),
    ("2.0 TDI 140", "EA189-2.0TDI", 320), ("FR 2.0 TDI 170", "EA189-2.0TDI", 350)], reservoir=55, remarques="Restylage")
mg(L, "Leon", "5F", "1", "2012-11", "2016-12",
   [("1.2 TSI 86", "EA211-1.2TSI", 160), ("1.2 TSI 105", "EA211-1.2TSI", 175), ("1.4 TSI 125", "EA211-1.4TSI", 200), ("1.4 TSI 150", "EA211-1.4TSI", 250),
    ("1.8 TSI 180", "EA888-1.8TSI", 250), ("Cupra 2.0 TSI 265", "EA888-2.0TSI", 350, {"debut": "2014-02"}),
    ("Cupra 2.0 TSI 280", "EA888-2.0TSI", 350, {"debut": "2014-02"}), ("Cupra 2.0 TSI 290", "EA888-2.0TSI", 350, {"debut": "2016-01"}),
    ("1.6 TDI 90", "EA288-1.6TDI", 230), ("1.6 TDI 105", "EA288-1.6TDI", 250), ("2.0 TDI 150", "EA288-2.0TDI", 320), ("FR 2.0 TDI 184", "EA288-2.0TDI", 380)],
   reservoir=50, remarques="5 portes, SC 3 portes, ST break, X-Perience")
mg(L, "Leon", "5F", "2", "2017-01", "2020-02",
   [("1.0 TSI 115", "EA211-1.0TSI", 200), ("1.4 TSI 125", "EA211-1.4TSI", 200, {"fin": "2018-06"}), ("1.5 TSI 130", "EA211-1.5TSI", 200, {"debut": "2018-06"}),
    ("1.5 TSI 150", "EA211-1.5TSI", 250, {"debut": "2018-06"}), ("1.8 TSI 180", "EA888-1.8TSI", 250), ("Cupra 2.0 TSI 300", "EA888-2.0TSI", 380),
    ("1.6 TDI 115", "EA288-1.6TDI", 250), ("2.0 TDI 150", "EA288-2.0TDI", 340), ("FR 2.0 TDI 184", "EA288-2.0TDI", 380)], reservoir=50, remarques="Restylage")
mg(L, "Leon", "KL", "1", "2020-03", "2024-08",
   [("1.0 TSI 110", "EA211-1.0TSI", 200), ("1.0 eTSI 110", "EA211-1.0eTSI", 200), ("1.5 TSI 130", "EA211-1.5TSI", 200), ("1.5 TSI 150", "EA211-1.5TSI", 250),
    ("1.5 eTSI 150", "EA211-1.5eTSI", 250), ("FR 2.0 TSI 190", "EA888-2.0TSI", 320), ("1.4 e-Hybrid 204", "EA211-1.4TSI-PHEV", 350, ph(13, 40)),
    ("2.0 TDI 115", "EA288evo-2.0TDI", 300), ("2.0 TDI 150", "EA288evo-2.0TDI", 360)], reservoir=50, remarques="5 portes et Sportstourer")
mg(L, "Leon", "KL", "2", "2024-09", None,
   [("1.5 TSI 115", "EA211-1.5TSI", 220), ("1.5 TSI 150", "EA211-1.5TSI", 250), ("1.5 eTSI 150", "EA211-1.5eTSI", 250),
    ("1.5 e-Hybrid 204", "EA211-1.5TSI-PHEV", 350, ph(20, 40)), ("1.5 e-Hybrid 272", "EA211-1.5TSI-PHEV", 400, ph(20, 40)),
    ("2.0 TDI 115", "EA288evo-2.0TDI", 300), ("2.0 TDI 150", "EA288evo-2.0TDI", 360)], reservoir=50, remarques="Restylage")

# ---------------------------------------------------------------- monospaces, citadines, SUV
mg(L, "Arosa", "6H", "1", "1997-05", "2004-06", [("1.0 50", "EA111-1.0", 86), ("1.4 60", "EA111-1.4", 116), ("1.7 SDI 60", "EA180-1.9SDI", 115),
                                                  ("1.4 TDI 75", "EA188-1.4TDI", 195, {"debut": "2000-09"})], portes=3, places=4, reservoir=34,
   remarques="Jumelle VW Lupo ; restylage 2000")
mg(L, "Altea", "5P", "1", "2004-03", "2015-08",
   [("1.4 85", "EA111-1.4", 132), ("1.6 102", "EA113-1.6", 148), ("1.2 TSI 105", "EA111-1.2TSI", 175, {"debut": "2010-01"}), ("1.4 TSI 125", "EA111-1.4TSI", 200, {"debut": "2007-06"}),
    ("2.0 FSI 150", "EA113-2.0FSI", 200, {"fin": "2008-12"}), ("1.8 TSI 160", "EA888-1.8TSI", 250, {"debut": "2008-01"}), ("1.9 TDI 105", "EA180-1.9TDI", 250, {"fin": "2010-06"}),
    ("1.6 TDI 105", "EA189-1.6TDI", 250, {"debut": "2010-06"}), ("2.0 TDI 140", "EA188-2.0TDI", 320)], reservoir=55, remarques="Monospace ; Altea XL et Freetrack")
mg(L, "Alhambra", "7M", "1", "1996-04", "2010-03",
   [("2.0 115", "EA827-2.0", 170), ("1.8 20VT 150", "EA113-1.8T", 210, {"debut": "2000-06"}), ("2.8 VR6 204", "VR6-2.8", 265, {"debut": "2000-06"}),
    ("1.9 TDI 90", "EA180-1.9TDI", 202), ("1.9 TDI 115", "EA180-1.9TDI", 310, {"debut": "2000-06"}), ("2.0 TDI 140", "EA188-2.0TDI", 320, {"debut": "2005-01"})],
   places=7, reservoir=70, remarques="Jumeau VW Sharan / Ford Galaxy ; restylage 2000")
mg(L, "Alhambra", "7N", "1", "2010-09", "2020-12",
   [("1.4 TSI 150", "EA111-1.4TSI", 240), ("2.0 TSI 200", "EA888-2.0TSI", 280, {"fin": "2015-06"}), ("2.0 TSI 220", "EA888-2.0TSI", 350, {"debut": "2015-06"}),
    ("2.0 TDI 115", "EA189-2.0TDI", 280), ("2.0 TDI 140", "EA189-2.0TDI", 320, {"fin": "2015-06"}), ("2.0 TDI 150", "EA288-2.0TDI", 340, {"debut": "2015-06"}),
    ("2.0 TDI 177", "EA189-2.0TDI", 380, {"fin": "2015-06"}), ("2.0 TDI 184", "EA288-2.0TDI", 380, {"debut": "2015-06"})], places=7, reservoir=70)
mg(L, "Mii", "AA", "1", "2011-12", "2019-12", [("1.0 MPI 60", "EA211-1.0MPI", 95), ("1.0 MPI 75", "EA211-1.0MPI", 95)], portes=3, places=4, reservoir=35,
   remarques="Jumelle VW up! (3 et 5 portes)")
mg(L, "Mii", "AA", "2", "2019-10", "2021-06", [("Electric 83", "EUP-EV", 212, el(37))], places=4, reservoir=0, remarques="Mii electric")
mg(L, "Exeo", "3R", "1", "2009-01", "2013-05",
   [("1.6 102", "EA113-1.6", 148), ("1.8 TSI 120", "EA888-1.8TSI", 230), ("1.8 TSI 160", "EA888-1.8TSI", 250), ("2.0 TSI 200", "EA888-2.0TSI", 280),
    ("2.0 TDI 120", "EA189-2.0TDI", 290), ("2.0 TDI 143", "EA189-2.0TDI", 320), ("2.0 TDI 170", "EA189-2.0TDI", 350)], portes=4, reservoir=70,
   remarques="Ex-Audi A4 B7 ; berline et ST")
mg(L, "Ateca", "KH7", "1", "2016-06", "2020-06",
   [("1.0 TSI 115", "EA211-1.0TSI", 200), ("1.4 TSI 150", "EA211-1.4TSI", 250, {"fin": "2018-12"}), ("1.5 TSI 150", "EA211-1.5TSI", 250, {"debut": "2018-09"}),
    ("2.0 TSI 190", "EA888-2.0TSI", 320, {"debut": "2017-06"}), ("1.6 TDI 115", "EA288-1.6TDI", 250), ("2.0 TDI 150", "EA288-2.0TDI", 340),
    ("2.0 TDI 190", "EA288-2.0TDI", 400)], reservoir=50)
mg(L, "Ateca", "KH7", "2", "2020-07", None,
   [("1.0 TSI 110", "EA211-1.0TSI", 200), ("1.5 TSI 150", "EA211-1.5TSI", 250), ("2.0 TSI 190", "EA888-2.0TSI", 320, {"fin": "2023-12"}),
    ("2.0 TDI 115", "EA288evo-2.0TDI", 300), ("2.0 TDI 150", "EA288evo-2.0TDI", 360)], reservoir=50, remarques="Restylage")
mg(L, "Arona", "KJ7", "1", "2017-09", "2021-06",
   [("1.0 TSI 95", "EA211-1.0TSI", 175), ("1.0 TSI 115", "EA211-1.0TSI", 200), ("1.5 TSI 150", "EA211-1.5TSI", 250),
    ("1.6 TDI 95", "EA288-1.6TDI", 250), ("1.6 TDI 115", "EA288-1.6TDI", 250)], reservoir=40)
mg(L, "Arona", "KJ7", "2", "2021-07", None,
   [("1.0 TSI 95", "EA211-1.0TSI", 175), ("1.0 TSI 110", "EA211-1.0TSI", 200), ("1.5 TSI 150", "EA211-1.5TSI", 250)], reservoir=40,
   remarques="Restylage 2021 ; restylage 2025 non détaillé")
mg(L, "Tarraco", "KN2", "1", "2018-11", "2024-06",
   [("1.5 TSI 150", "EA211-1.5TSI", 250), ("2.0 TSI 190", "EA888-2.0TSI", 320), ("2.0 TSI 245", "EA888-2.0TSI", 370, {"debut": "2020-09"}),
    ("1.4 e-Hybrid 245", "EA211-1.4TSI-PHEV", 400, ph(13, 45, debut="2021-03")), ("2.0 TDI 150", "EA288evo-2.0TDI", 340), ("2.0 TDI 200", "EA288evo-2.0TDI", 400)],
   places=7, reservoir=60, remarques="SUV 5 ou 7 places")

MOT = Motorisations("Volkswagen", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"SEAT": L}
MOTEURS = MOT.moteurs()
