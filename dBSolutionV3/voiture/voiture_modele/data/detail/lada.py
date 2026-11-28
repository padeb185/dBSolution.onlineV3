"""Lada (AvtoVAZ, Togliatti) : générations, phases, motorisations (marché européen, puis russe) et moteurs liés.
Classiques à propulsion (2101 à 2107, licence Fiat 124), Niva (2121, 2131, Urban), Samara (2108 / 2109 / 21099), 110 / 111 / 112, Kalina,
Priora, Granta (berline, liftback, Cross), Largus (Dacia Logan MCV, moteurs Renault repris de dacia.py), Vesta (berline, SW, Cross) et
X-Ray (Cross). Ventes en Europe occidentale arrêtées vers 2019. Puissances en ch. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .dacia import FAMILLES as FAMILLES_DACIA

FAMILLES = {
    "VAZ-1.2": f("ATM", "ESS", 1.2, "CHAINE", 4, 5600, 3400, "15W40", 3.75, 10000),
    "VAZ-1.3": f("ATM", "ESS", 1.3, "COURROIE", 4, 5600, 3400, "15W40", 3.75, 10000),
    "VAZ-1.5": f("ATM", "ESS", 1.5, "CHAINE", 4, 5600, 3400, "15W40", 3.75, 10000),
    "VAZ-1.6": f("ATM", "ESS", 1.6, "CHAINE", 4, 5400, 3000, "15W40", 3.75, 10000),
    "VAZ-1.7": f("ATM", "ESS", 1.7, "CHAINE", 4, 5000, 4000, "10W40", 3.75, 15000),
    "VAZ-FWD-1.1": f("ATM", "ESS", 1.1, "COURROIE", 4, 5600, 3400, "15W40", 3.5, 10000),
    "VAZ-FWD-1.3": f("ATM", "ESS", 1.3, "COURROIE", 4, 5600, 3400, "15W40", 3.5, 10000),
    "VAZ-FWD-1.5": f("ATM", "ESS", 1.5, "COURROIE", 4, 5400, 3000, "10W40", 3.5, 15000),
    "VAZ-FWD-1.5-16V": f("ATM", "ESS", 1.5, "COURROIE", 4, 5600, 3700, "10W40", 3.5, 15000),
    "VAZ-FWD-1.6": f("ATM", "ESS", 1.6, "COURROIE", 4, 5200, 3000, "10W40", 3.5, 15000),
    "VAZ-FWD-1.6-16V": f("ATM", "ESS", 1.6, "COURROIE", 4, 5800, 4200, "5W40", 3.5, 15000),
    "VAZ-1.4-16V": f("ATM", "ESS", 1.4, "COURROIE", 4, 5600, 4000, "5W40", 3.5, 15000),
    "VAZ-1.8-16V": f("ATM", "ESS", 1.8, "COURROIE", 4, 6050, 3700, "5W40", 4.4, 15000),
    "K7M": FAMILLES_DACIA["K7M"], "K4M": FAMILLES_DACIA["K4M"],
}
mg = SaisieMoteurs(FAMILLES, "Lada", lambda fam: "Renault" if fam in ("K7M", "K4M") else "Lada")
L = []
IND = "données indicatives"
mg(L, "2101", "2101", "1", "1970-04", "1988-12", [("1.2 64", "VAZ-1.2", 89)], portes=4, places=5, reservoir=39, remarques="Lada 1200 (licence Fiat 124) ; " + IND)
mg(L, "2102", "2102", "1", "1972-01", "1985-12", [("1.2 64", "VAZ-1.2", 89)], portes=5, places=5, reservoir=39, remarques="Break de la 2101 ; " + IND)
mg(L, "2103", "2103", "1", "1972-01", "1984-12", [("1.5 75", "VAZ-1.5", 108)], portes=4, places=5, reservoir=39, remarques="Lada 1500 ; " + IND)
mg(L, "2105", "2105", "1", "1980-01", "2010-12", [("1.3 69", "VAZ-1.3", 95), ("1.5 72", "VAZ-1.5", 104)], portes=4, places=5, reservoir=39, remarques="Lada 1300 / 1500 (Riva au Royaume-Uni) ; " + IND)
mg(L, "2104", "2104", "1", "1984-01", "2012-12", [("1.3 69", "VAZ-1.3", 95), ("1.5 72", "VAZ-1.5", 104), ("1.6 75", "VAZ-1.6", 116, {"debut": "1996-01"})], portes=5, places=5, reservoir=39,
   remarques="Break de la 2105 ; " + IND)
mg(L, "2106", "2106", "1", "1976-01", "2006-12", [("1.5 72", "VAZ-1.5", 104), ("1.6 80", "VAZ-1.6", 121)], portes=4, places=5, reservoir=39, remarques="Lada 1600 ; " + IND)
mg(L, "2107", "2107", "1", "1982-01", "2012-12", [("1.5 72", "VAZ-1.5", 104), ("1.6 75", "VAZ-1.6", 116, {"debut": "1996-01"})], portes=4, places=5, reservoir=39, remarques="Version luxe de la 2105 ; " + IND)
NIVA = [("1.6 72", "VAZ-1.6", 121, {"fin": "1994-12"}), ("1.7 80", "VAZ-1.7", 127, {"debut": "1995-01", "fin": "2008-12"}), ("1.7 83", "VAZ-1.7", 129, {"debut": "2009-01"})]
mg(L, "Niva (2121)", "2121", "1", "1977-04", None, NIVA, portes=3, places=5, reservoir=42, remarques="Tout-terrain monocoque à transmission intégrale permanente ; Niva Legend depuis 2021 ; " + IND)
mg(L, "Niva 5 portes", "2131", "1", "1995-01", None, NIVA[1:], portes=5, places=5, reservoir=58, remarques="Empattement long ; " + IND)
mg(L, "Urban Niva", "2121", "U", "2014-01", "2021-12", [("1.7 83", "VAZ-1.7", 129)], portes=3, places=5, reservoir=42, remarques="Finition citadine de la Niva 3 portes ; " + IND)
SAM = [("1.1 54", "VAZ-FWD-1.1", 79, {"fin": "1996-12"}), ("1.3 65", "VAZ-FWD-1.3", 96, {"fin": "2001-12"}), ("1.5 73", "VAZ-FWD-1.5", 106, {"fin": "1996-12"}),
       ("1.5i 78", "VAZ-FWD-1.5", 116, {"debut": "1995-01"}), ("1.6i 82", "VAZ-FWD-1.6", 120, {"debut": "2004-01"})]
mg(L, "Samara 3 portes", "2108", "1", "1984-12", "2013-12", SAM, portes=3, places=5, reservoir=43, remarques="Première Lada à traction ; " + IND)
mg(L, "Samara 5 portes", "2109", "1", "1987-01", "2013-12", SAM, portes=5, places=5, reservoir=43, remarques=IND)
mg(L, "Samara Berline", "21099", "1", "1990-01", "2004-12", SAM[1:], portes=4, places=5, reservoir=43, remarques="Samara Forma ; " + IND)
T110 = [("1.5 78", "VAZ-FWD-1.5", 116), ("1.5 16V 94", "VAZ-FWD-1.5-16V", 128), ("1.6 81", "VAZ-FWD-1.6", 120, {"debut": "2004-01"}), ("1.6 16V 89", "VAZ-FWD-1.6-16V", 131, {"debut": "2004-01"})]
mg(L, "Lada 110", "2110", "1", "1995-01", "2009-12", T110, portes=4, places=5, reservoir=43, remarques=IND)
mg(L, "Lada 111", "2111", "1", "1998-01", "2009-12", T110, portes=5, places=5, reservoir=43, remarques="Break ; " + IND)
mg(L, "Lada 112", "2112", "1", "1999-01", "2008-12", T110, portes=5, places=5, reservoir=43, remarques="Hatchback ; " + IND)
mg(L, "Kalina", "Kalina", "1", "2004-11", "2018-07", [("1.4 16V 89", "VAZ-1.4-16V", 127, {"fin": "2013-05"}), ("1.6 81", "VAZ-FWD-1.6", 120), ("1.6 16V 98", "VAZ-FWD-1.6-16V", 145, {"debut": "2013-06"})],
   portes=5, places=5, reservoir=50, remarques="Berline, hatchback et break, Kalina II en 2013 ; " + IND)
mg(L, "Priora", "Priora", "1", "2007-03", "2018-07", [("1.6 16V 98", "VAZ-FWD-1.6-16V", 145), ("1.6 16V 106", "VAZ-FWD-1.6-16V", 148, {"debut": "2013-06"})], portes=4, places=5, reservoir=43,
   remarques="Évolution de la 110 ; " + IND)
GR = [("1.6 87", "VAZ-FWD-1.6", 140), ("1.6 16V 98", "VAZ-FWD-1.6-16V", 145), ("1.6 16V 106", "VAZ-FWD-1.6-16V", 148)]
mg(L, "Granta", "Granta", "1", "2011-12", None, GR, portes=4, places=5, reservoir=50, remarques=IND)
mg(L, "Granta Liftback", "Granta", "L", "2014-06", None, GR, portes=5, places=5, reservoir=50, remarques=IND)
mg(L, "Granta Cross", "Granta", "C", "2019-02", None, GR, portes=5, places=5, reservoir=50, remarques="Break surélevé ; " + IND)
mg(L, "Largus", "Largus", "1", "2012-07", None, [("1.6 MPI 87", "K7M", 128), ("1.6 16V 105", "K4M", 148)], portes=5, places=7, reservoir=50, remarques="Dacia Logan MCV ; " + IND)
VE = [("1.6 16V 106", "VAZ-FWD-1.6-16V", 148), ("1.8 16V 122", "VAZ-1.8-16V", 170)]
mg(L, "Vesta", "Vesta", "1", "2015-09", None, VE, portes=4, places=5, reservoir=55, remarques=IND)
mg(L, "Vesta SW", "Vesta", "S", "2017-09", None, VE, portes=5, places=5, reservoir=55, remarques="Break ; " + IND)
mg(L, "Vesta Cross", "Vesta", "C", "2017-09", None, VE, portes=5, places=5, reservoir=55, remarques="Berline et break surélevés ; " + IND)
mg(L, "X-Ray", "X-Ray", "1", "2015-12", "2022-03", VE, portes=5, places=5, reservoir=50, remarques="Base Renault Sandero ; " + IND)
mg(L, "X-Ray Cross", "X-Ray", "C", "2018-11", "2022-03", VE, portes=5, places=5, reservoir=50, remarques=IND)

MOT = Motorisations("Lada", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Lada": L}
MOTEURS = MOT.moteurs()
