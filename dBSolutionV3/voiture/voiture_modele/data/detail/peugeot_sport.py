"""Peugeot Sport (Peugeot Talbot Sport / Peugeot Sport) : voitures de rallye, rallye-raid, endurance et circuit, séries
d'homologation, motorisations et moteurs liés.
205 Turbo 16 (route et Groupe B), 405 T16 Grand Raid, 905, 306 Maxi, 206 WRC, 206 S1600, 307 WRC, 207 S2000, 908 HDi FAP et 908,
208 R2, 208 T16 R5, 208 T16 Pikes Peak, 208 Rally4, 2008 DKR, 3008 DKR, 308 TCR et 9X8.
Les versions sportives de série (205 GTI, 206 RC, 207 RC, 208 GTi, 308 GTi, 508 PSE, RCZ R, e-208 GTi…) restent dans Peugeot.
Moteurs de compétition au motoriste « Peugeot Sport » (codes propres) ; moteur kit car repris de citroen_sport.py.
Données indicatives (puissances de course).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .citroen_sport import FAMILLES as FAMILLES_CITROEN_SPORT

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"


def course(t, l, rpm, nmrpm, n=4, d=C, c=E_, a="EN_LIGNE"):
    return f(t, c, l, d, n, rpm, nmrpm, "CHOISIR", 6.0, 1000, a=a)


PS = {
    "XU8T-1.8T": f("TURBO", E_, 1.8, B, 4, 6750, 4000, "10W40", 5.0, 7500),
    "XU9T-1.9T-GR": course("TURBO", 1.9, 7000, 5000, d=B),
    "SA35-3.5V10": course("ATM", 3.5, 12500, 10000, n=10, a="V"),
    "XU9J4-2.0T-WRC": course("TURBO", 2.0, 5250, 3500, d=B),
    "TU5-1.6-S1600": course("ATM", 1.6, 8500, 7000, d=B),
    "EW10J4-2.0T-WRC": course("TURBO", 2.0, 5250, 3250),
    "EW10-2.0-S2000": course("ATM", 2.0, 8250, 6500),
    "HDI-V12-5.5": course("TURBO", 5.5, 5000, 3000, n=12, c=D, a="V"),
    "HDI-V8-3.7": course("TURBO", 3.7, 5000, 3000, n=8, c=D, a="V"),
    "EP6-1.6-R2": course("ATM", 1.6, 7600, 6500),
    "V6-3.2TT-PP": course("TURBO", 3.2, 7000, 5000, n=6, a="V"),
    "EB2-1.2T-RALLY4": course("TURBO", 1.2, 5800, 3500, n=3),
    "DV-V6-3.0TT": course("TURBO", 3.0, 4500, 2500, n=6, c=D, a="V"),
    "EP6-1.6T-TCR": course("TURBO", 1.6, 6500, 3500),
    "9X8-V6-2.6TT-HYB": course("HYB_E", 2.6, 8000, 6000, n=6, a="V"),
}
CS = {k: FAMILLES_CITROEN_SPORT[k] for k in ("XU10-2.0-KIT", "EP6-1.6T-RALLY")}
FAMILLES = {**PS, **CS}


def motoriste(fam):
    return "Citroën Racing" if fam in CS else "Peugeot Sport"


mg = SaisieMoteurs(FAMILLES, "Peugeot Sport", motoriste)
L = []
R = "Voiture de compétition (non homologuée route) ; données indicatives"

mg(L, "205 Turbo 16", "205 T16", "1", "1984-03", "1986-12",
   [("Série 200 1.8 Turbo 200", "XU8T-1.8T", 255, {"fin": "1985-06"}), ("Groupe B E1 1.8 Turbo 350", "XU8T-1.8T", 410, {"fin": "1985-06"}),
    ("Groupe B E2 1.8 Turbo 450", "XU8T-1.8T", 490, {"debut": "1985-07"})], portes=3, places=2, reservoir=70,
   remarques="Moteur central et 4x4 ; série d'homologation de 200 ex. route ; titres mondiaux 1985-1986 ; données indicatives")
mg(L, "405 T16", "405 T16 GR", "1", "1988-01", "1990-12", [("Grand Raid 1.9 Turbo 360", "XU9T-1.9T-GR", 480)], portes=3, places=2, reservoir=400,
   remarques=R + " ; vainqueur du Paris-Dakar 1989 et 1990")
mg(L, "905", "905", "1", "1990-07", "1993-06", [("3.5 V10 650", "SA35-3.5V10", 400)], portes=2, places=1, reservoir=100,
   remarques=R + " ; prototype Sport ; vainqueur des 24 Heures du Mans 1992 et 1993")
mg(L, "306 Maxi", "306", "1", "1996-01", "1998-12", [("Kit Car 2.0 16V 285", "XU10-2.0-KIT", 255)], portes=3, places=2, reservoir=60, remarques=R + " ; F2 Kit Car (traction)")
mg(L, "206 WRC", "206", "1", "1999-05", "2003-12", [("WRC 2.0 Turbo 300", "XU9J4-2.0T-WRC", 535)], portes=3, places=2, reservoir=80,
   remarques=R + " ; titres constructeurs 2000-2002")
mg(L, "206 S1600", "206", "2", "2003-01", "2004-12", [("S1600 1.6 16V 215", "TU5-1.6-S1600", 200)], portes=3, places=2, reservoir=60, remarques=R + " ; traction")
mg(L, "307 WRC", "307", "1", "2004-01", "2005-12", [("WRC 2.0 Turbo 300", "EW10J4-2.0T-WRC", 570)], portes=2, places=2, reservoir=80, remarques=R + " ; base 307 CC")
mg(L, "207 S2000", "A7", "1", "2007-01", "2011-12", [("S2000 2.0 280", "EW10-2.0-S2000", 255)], portes=3, places=2, reservoir=75, remarques=R + " ; 4x4 atmosphérique, IRC")
mg(L, "908", "908 HDi FAP", "1", "2007-01", "2010-12", [("HDi FAP 5.5 V12 Diesel 700", "HDI-V12-5.5", 1200)], portes=2, places=1, reservoir=81,
   remarques=R + " ; vainqueur des 24 Heures du Mans 2009")
mg(L, "908", "908 (2011)", "1", "2011-01", "2011-12", [("HDi FAP 3.7 V8 Diesel 550", "HDI-V8-3.7", 1000)], portes=2, places=1, reservoir=65, remarques=R)
mg(L, "208 R2", "A9", "1", "2013-01", "2019-12", [("R2 1.6 185", "EP6-1.6-R2", 190)], portes=3, places=2, reservoir=60, remarques=R + " ; traction, client")
mg(L, "208 T16", "A9", "2", "2014-01", "2020-12", [("R5 1.6 Turbo 280", "EP6-1.6T-RALLY", 400)], portes=3, places=2, reservoir=80, remarques=R + " ; 4x4 client")
mg(L, "208 T16 Pikes Peak", "A9", "PP", "2013-01", "2013-12", [("Pikes Peak 3.2 V6 Biturbo 875", "V6-3.2TT-PP", 900)], portes=3, places=1, reservoir=60,
   remarques=R + " ; record de Pikes Peak 2013 (Loeb)")
mg(L, "208 Rally4", "P21", "1", "2019-06", None, [("Rally4 1.2 Turbo 212", "EB2-1.2T-RALLY4", 290)], portes=5, places=2, reservoir=60, remarques=R + " ; traction, client")
mg(L, "2008 DKR", "2008 DKR", "1", "2015-01", "2016-12", [("DKR 3.0 V6 Biturbo Diesel 340", "DV-V6-3.0TT", 800)], portes=3, places=2, reservoir=400,
   remarques=R + " ; propulsion ; vainqueur du Dakar 2016")
mg(L, "3008 DKR", "3008 DKR", "1", "2017-01", "2018-12", [("DKR 3.0 V6 Biturbo Diesel 350", "DV-V6-3.0TT", 800)], portes=3, places=2, reservoir=400,
   remarques=R + " ; vainqueur du Dakar 2017 et 2018 (3008 DKR Maxi)")
mg(L, "308 TCR", "308", "1", "2018-01", "2021-12", [("TCR 1.6 Turbo 350", "EP6-1.6T-TCR", 420)], portes=5, places=1, reservoir=100, remarques=R + " ; client")
mg(L, "9X8", "9X8", "1", "2022-07", None, [("Hybride 2.6 V6 Biturbo 680", "9X8-V6-2.6TT-HYB", 700)], portes=2, places=1, reservoir=90,
   remarques=R + " ; Hypercar WEC, V6 biturbo et moteur électrique avant (puissance système plafonnée à 500 kW)")

MOT = Motorisations("Peugeot Sport", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Peugeot Sport": L}
MOTEURS = MOT.moteurs()
