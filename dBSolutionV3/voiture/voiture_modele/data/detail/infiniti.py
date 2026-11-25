"""Infiniti : générations, phases, motorisations (marché européen, 2008-2020) et moteurs liés.
G (G37), FX puis QX70, EX puis QX50 (J50), M puis Q70, Q50, Q60, Q30/QX30, QX50 (J55). Infiniti a quitté l'Europe en 2020.
Modèles nord-américains (QX55, QX60, QX80, Q70L) : hp convertis en ch (×1,014).
Moteurs Nissan : familles de nissan.py et familles ajoutées ici (motoriste « Nissan ») ; moteurs Mercedes-Benz des Q30/QX30,
Q50 et Q70 : familles et codes de mercedes.py (motoriste « Mercedes-Benz »).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .mercedes import FAMILLES as FAMILLES_MB
from .nissan import FAMILLES as FAMILLES_NISSAN

E_, D = "ESS", "DSL"
C = "CHAINE"

AJOUTS_NISSAN = {
    "VQ25HR": f("ATM", E_, 2.5, C, 6, 6400, 4800, "5W30", 4.7, 20000, a="V"),
    "VQ35HR-HYB": f("HYB_TE", E_, 3.5, C, 6, 6800, 5000, "5W30", 4.7, 20000, a="V"),
    "VQ35DD": f("ATM", E_, 3.5, C, 6, 6400, 4800, "0W20", 5.3, 20000, a="V"),
    "VK50VE": f("ATM", E_, 5.0, C, 8, 6500, 4400, "5W30", 6.4, 20000, a="V"),
    "VK56VD": f("ATM", E_, 5.6, C, 8, 5800, 4000, "5W30", 6.9, 20000, a="V"),
    "VR30DDTT": f("TURBO", E_, 3.0, C, 6, 6400, 1600, "0W20", 5.4, 20000, a="V"),
    "VR35DDTT": f("TURBO", E_, 3.5, C, 6, 6000, 3600, "0W20", 6.3, 20000, a="V"),
    "KR20DDET": f("TURBO", E_, 2.0, C, 4, 5600, 4400, "0W20", 5.0, 20000),
}
NISSAN = {**{k: FAMILLES_NISSAN[k] for k in ("VQ37VHR", "VQ35HR", "V9X")}, **AJOUTS_NISSAN}
MERCEDES = {k: FAMILLES_MB[k] for k in ("M270-1.6", "M270-2.0", "M274-2.0", "OM607-1.5", "OM651-2.1")}
FAMILLES = {**NISSAN, **MERCEDES}

NA = "Marché nord-américain (hp convertis en ch)"
mg = SaisieMoteurs(FAMILLES, "Nissan", lambda fam: "Mercedes-Benz" if fam in MERCEDES else "Nissan")
L = []

# ---------------------------------------------------------------- berlines et coupés
mg(L, "G", "V36", "1", "2008-10", "2013-12",
   [("G37 3.7 V6 320", "VQ37VHR", 360), ("G25 2.5 V6 222", "VQ25HR", 253, {"debut": "2010-06"}), ("G37 3.7 V6 AWD 320", "VQ37VHR", 360)],
   portes=4, reservoir=80, remarques="Berline, coupé et cabriolet (2009) ; coupé et cabriolet renommés Q60 en 2013")
mg(L, "Q60", "CV36", "1", "2014-01", "2016-06", [("3.7 V6 320", "VQ37VHR", 360)], portes=2, places=4, reservoir=80,
   remarques="Ancien G37 coupé et cabriolet")
mg(L, "Q60", "CV37", "1", "2016-07", "2019-12",
   [("2.0t 211", "M274-2.0", 350), ("Red Sport 3.0t V6 405", "VR30DDTT", 475)], portes=2, places=4, reservoir=80, remarques="Coupé")
mg(L, "Q50", "V37", "1", "2013-09", "2017-12",
   [("2.0t 211", "M274-2.0", 350, {"debut": "2014-06"}), ("2.2d 170", "OM651-2.1", 400), ("2.2d AWD 170", "OM651-2.1", 400),
    ("3.5 Hybrid 364", "VQ35HR-HYB", 546), ("3.5 Hybrid AWD 364", "VQ35HR-HYB", 546)], portes=4, reservoir=70)
mg(L, "Q50", "V37", "2", "2018-01", "2019-12",
   [("2.0t 211", "M274-2.0", 350), ("2.2d 170", "OM651-2.1", 400), ("3.5 Hybrid 364", "VQ35HR-HYB", 546), ("Red Sport 3.0t V6 405", "VR30DDTT", 475)],
   portes=4, reservoir=70, remarques="Restylage ; retrait d'Europe fin 2019")
mg(L, "M", "Y51", "1", "2010-06", "2013-12",
   [("M37 3.7 V6 320", "VQ37VHR", 360), ("M30d 3.0 V6 238", "V9X", 550), ("M35h 3.5 Hybrid 364", "VQ35HR-HYB", 546, {"debut": "2011-06"})],
   portes=4, reservoir=80, remarques="Renommée Q70 en 2013")
mg(L, "Q70", "Y51", "2", "2014-01", "2018-12",
   [("3.7 V6 320", "VQ37VHR", 360), ("3.0d V6 238", "V9X", 550, {"fin": "2015-06"}), ("2.2d 170", "OM651-2.1", 400, {"debut": "2015-07"}),
    ("3.5 Hybrid 364", "VQ35HR-HYB", 546)], portes=4, reservoir=80, remarques="Ancienne M restylée")
mg(L, "Q70L", "Y51L", "1", "2015-01", "2019-12", [("3.7 V6 335", "VQ37VHR", 366), ("5.6 V8 426", "VK56VD", 563)], portes=4, reservoir=80,
   remarques=NA + " ; empattement long")

# ---------------------------------------------------------------- SUV
mg(L, "Q30", "H15", "1", "2015-12", "2019-12",
   [("1.6t 122", "M270-1.6", 200), ("1.6t 156", "M270-1.6", 250), ("2.0t AWD 211", "M270-2.0", 350), ("1.5d 109", "OM607-1.5", 260),
    ("2.2d 170", "OM651-2.1", 350), ("2.2d AWD 170", "OM651-2.1", 350)], reservoir=56, remarques="Compacte sur base Mercedes Classe A, produite à Sunderland")
mg(L, "QX30", "H15", "1", "2016-06", "2019-12", [("2.0t AWD 211", "M270-2.0", 350), ("2.2d AWD 170", "OM651-2.1", 350)], reservoir=56,
   remarques="Version crossover de la Q30")
mg(L, "FX", "S51", "1", "2008-10", "2013-12",
   [("FX37 3.7 V6 320", "VQ37VHR", 360, {"debut": "2010-06"}), ("FX35 3.5 V6 307", "VQ35HR", 358, {"fin": "2010-05"}),
    ("FX50 5.0 V8 390", "VK50VE", 500), ("FX30d 3.0 V6 238", "V9X", 550, {"debut": "2010-06"})], reservoir=90,
   remarques="Restylage 2012 ; renommé QX70 en 2013")
mg(L, "QX70", "S51", "2", "2014-01", "2017-12",
   [("3.7 V6 320", "VQ37VHR", 360), ("5.0 V8 390", "VK50VE", 500, {"fin": "2014-12"}), ("3.0d V6 238", "V9X", 550)], reservoir=90, remarques="Ancien FX")
mg(L, "EX", "J50", "1", "2008-10", "2013-12", [("EX37 3.7 V6 320", "VQ37VHR", 360), ("EX30d 3.0 V6 238", "V9X", 550, {"debut": "2010-06"})],
   reservoir=76, remarques="Renommé QX50 en 2013")
mg(L, "QX50", "J50", "2", "2014-01", "2015-12", [("3.7 V6 320", "VQ37VHR", 360), ("3.0d V6 238", "V9X", 550)], reservoir=76, remarques="Ancien EX")
mg(L, "QX50", "J55", "1", "2018-06", "2019-12", [("2.0 VC-Turbo AWD 272", "KR20DDET", 380)], reservoir=60,
   remarques="Moteur à taux de compression variable ; brièvement commercialisé en Europe ; vendu en Amérique du Nord jusqu'en 2025")
mg(L, "QX55", "J55C", "1", "2021-06", "2025-06", [("2.0 VC-Turbo AWD 272", "KR20DDET", 380)], reservoir=60, remarques=NA + " ; SUV coupé")
mg(L, "QX60", "L50", "1", "2013-01", "2020-12", [("3.5 V6 269", "VQ35DD", 336), ("3.5 V6 AWD 269", "VQ35DD", 336)], places=7, reservoir=74,
   remarques=NA + " ; JX35 en 2013")
mg(L, "QX60", "L51", "1", "2021-06", None,
   [("3.5 V6 AWD 299", "VQ35DD", 366, {"fin": "2024-12"}), ("2.0 VC-Turbo AWD 272", "KR20DDET", 386, {"debut": "2025-01"})], places=7, reservoir=74,
   remarques=NA)
mg(L, "QX80", "Z62", "1", "2013-01", "2024-06", [("5.6 V8 406", "VK56VD", 560)], places=8, reservoir=98, remarques=NA + " ; QX56 en 2010-2013, restylages 2018")
mg(L, "QX80", "Z63", "1", "2024-07", None, [("3.5 V6 Biturbo AWD 456", "VR35DDTT", 700)], places=8, reservoir=98, remarques=NA)

MOT = Motorisations("Nissan", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Infiniti": L}
MOTEURS = MOT.moteurs()
