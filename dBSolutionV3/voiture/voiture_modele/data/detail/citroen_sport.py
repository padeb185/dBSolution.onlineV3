"""Citroën Sport (Citroën Sport / Citroën Racing) : voitures de rallye et de circuit, séries d'homologation, motorisations et moteurs liés.
BX 4TC, Visa 1000 Pistes, Xsara Kit Car et WRC, C4 WRC (et la série route C4 WRC Edition), DS3 WRC / R3, C3 WRC, C3 R5 / Rally2, C-Elysée WTCC.
Les versions sportives de série (Saxo / C2 / C4 VTS…) restent dans Citroën ; DS3/DS4/DS5 Racing dans DS Automobiles.
Moteurs de compétition au motoriste « Citroën Racing » (codes propres). Données indicatives (puissances de course).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C, B = "CHAINE", "COURROIE"


def course(t, l, rpm, nmrpm, d=C):
    return f(t, E_, l, d, 4, rpm, nmrpm, "CHOISIR", 6.0, 1000)


FAMILLES = {
    "N9TE-2.1T": f("TURBO", E_, 2.1, B, 4, 5250, 3250, "10W40", 5.0, 7500),
    "XU5-1.4-PISTES": f("ATM", E_, 1.4, B, 4, 6800, 4500, "10W40", 4.0, 7500),
    "XU10-2.0-KIT": course("ATM", 2.0, 8500, 6500, B),
    "XU7JP4-2.0T-WRC": course("TURBO", 2.0, 5500, 3500, B),
    "EW10-2.0": f("ATM", E_, 2.0, C, 4, 7000, 4750, "5W40", 4.25, 20000),
    "EP6-1.6T-RALLY": course("TURBO", 1.6, 6000, 3500),
    "EP6-1.6T-R3": course("TURBO", 1.6, 6800, 4500),
    "WTCC-1.6T": course("TURBO", 1.6, 8500, 4500),
}

mg = SaisieMoteurs(FAMILLES, "Citroën Racing")
L = []
R = "Voiture de compétition (non homologuée route) ; données indicatives"

mg(L, "BX 4TC", "BX", "4TC", "1986-01", "1986-12", [("4TC route 2.1 Turbo 200", "N9TE-2.1T", 294), ("4TC Groupe B 2.1 Turbo 380", "N9TE-2.1T", 450)], portes=5, places=4,
   reservoir=70, remarques="Série d'homologation Groupe B (200 ex. route) ; version rallye non homologuée route ; données indicatives")
mg(L, "Visa 1000 Pistes", "Visa", "1000P", "1984-01", "1985-12", [("1000 Pistes 1.4 112", "XU5-1.4-PISTES", 125)], portes=5, places=4, reservoir=43,
   remarques="Série d'homologation Groupe B 4x4 (environ 200 ex.) ; données indicatives")
mg(L, "Xsara Kit Car", "N6", "KC", "1998-01", "2000-12", [("Kit Car 2.0 16V 290", "XU10-2.0-KIT", 240)], portes=3, places=2, reservoir=60, remarques=R + " ; F2 Kit Car (traction)")
mg(L, "Xsara WRC", "N6", "WRC", "2001-01", "2006-12", [("WRC 2.0 Turbo 300", "XU7JP4-2.0T-WRC", 580)], portes=3, places=2, reservoir=75,
   remarques=R + " ; titres constructeurs 2003-2005, pilotes 2004-2006 (Loeb)")
mg(L, "C4 WRC", "LA", "WRC", "2007-01", "2010-12", [("WRC 2.0 Turbo 320", "XU7JP4-2.0T-WRC", 580)], portes=3, places=2, reservoir=75, remarques=R + " ; titres 2007-2010")
mg(L, "C4 WRC Edition", "LA", "ED", "2008-01", "2008-12", [("By Loeb 2.0 16V 180", "EW10-2.0", 202)], portes=3, places=4, reservoir=60,
   remarques="Série limitée route (base C4 Coupé VTS) ; données indicatives")
mg(L, "DS3 WRC", "A55", "WRC", "2011-01", "2016-12", [("WRC 1.6 Turbo 315", "EP6-1.6T-RALLY", 350)], portes=3, places=2, reservoir=75, remarques=R + " ; titres 2011-2012")
mg(L, "DS3 R3", "A55", "R3", "2010-01", "2016-12", [("R3T 1.6 THP 210", "EP6-1.6T-R3", 300)], portes=3, places=2, reservoir=60, remarques=R + " ; traction, client")
mg(L, "C3 WRC", "B618", "WRC", "2017-01", "2019-12", [("WRC 1.6 Turbo 380", "EP6-1.6T-RALLY", 450)], portes=5, places=2, reservoir=80, remarques=R)
mg(L, "C3 R5", "B618", "R5", "2019-01", "2021-12", [("R5 1.6 Turbo 282", "EP6-1.6T-RALLY", 420)], portes=5, places=2, reservoir=80, remarques=R + " ; 4x4 client")
mg(L, "C3 Rally2", "B618", "RL2", "2021-01", None, [("Rally2 1.6 Turbo 289", "EP6-1.6T-RALLY", 455)], portes=5, places=2, reservoir=80, remarques=R + " ; 4x4 client")
mg(L, "C-Elysée WTCC", "DD", "WTCC", "2014-01", "2016-12", [("WTCC 1.6 Turbo 380", "WTCC-1.6T", 400)], portes=4, places=1, reservoir=60, remarques=R + " ; titres WTCC 2014-2016")

MOT = Motorisations("Citroën Racing", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Citroën Sport": L}
MOTEURS = MOT.moteurs()
