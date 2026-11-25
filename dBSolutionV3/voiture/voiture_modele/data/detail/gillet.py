"""Gillet (Belgique, Tony Gillet) : générations, phases, motorisations et moteurs liés.
Vertigo (Ford Cosworth puis V6 Alfa Romeo), Vertigo Streiff, Vertigo .5 et Vertigo .5 Spirit (V8 Maserati).
Production artisanale : dates et puissances indicatives. Moteurs Ford et Alfa Romeo repris de ford.py et alfa_romeo.py
(mêmes motoristes et mêmes codes) ; V6 Alfa préparés par Gillet et V8 Maserati au motoriste propre.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .alfa_romeo import FAMILLES as FAMILLES_ALFA
from .ford import FAMILLES as FAMILLES_FORD

E_ = "ESS"

PROPRES = {
    "GILLET-V6-3.6": f("ATM", E_, 3.6, "COURROIE", 6, 7000, 5500, "10W60", 6.0, 10000, a="V"),
    "GILLET-V6-4.0": f("ATM", E_, 4.0, "COURROIE", 6, 7000, 5500, "10W60", 6.0, 10000, a="V"),
}
MASERATI = {"F136-4.2": f("ATM", E_, 4.2, "CHAINE", 8, 7000, 4750, "10W60", 9.0, 15000, a="V")}
FAMILLES = {"COSWORTH-YB": FAMILLES_FORD["COSWORTH-YB"], "BUSSO-3.0-24V": FAMILLES_ALFA["BUSSO-3.0-24V"], **PROPRES, **MASERATI}


def motoriste(fam):
    if fam == "COSWORTH-YB":
        return "Ford"
    if fam == "BUSSO-3.0-24V":
        return "Alfa Romeo"
    return "Maserati" if fam in MASERATI else "Gillet"


mg = SaisieMoteurs(FAMILLES, "Gillet", motoriste)
L = []

mg(L, "Vertigo", "Vertigo", "1", "1992-01", "1997-12", [("Cosworth 2.0 Turbo 220", "COSWORTH-YB", 304)], portes=2, places=2, reservoir=60,
   remarques="Châssis carbone et nid d'abeille ; présentée au Salon de Bruxelles 1992 ; données indicatives")
mg(L, "Vertigo", "Vertigo", "2", "1998-01", "2001-12",
   [("Cosworth 2.0 Turbo 220", "COSWORTH-YB", 304), ("Alfa Romeo 3.0 V6 220", "BUSSO-3.0-24V", 270)], portes=2, places=2, reservoir=60,
   remarques="Toit, portes papillon et V6 Alfa Romeo en option ; données indicatives")
mg(L, "Vertigo", "Streiff", "1", "2002-01", "2007-12", [("3.6 V6 360", "GILLET-V6-3.6", 380)], portes=2, places=2, reservoir=60,
   remarques="Vertigo Streiff, 25 exemplaires ; V6 Alfa Romeo 3,6 l ; dates indicatives")
mg(L, "Vertigo .5", "Vertigo .5", "1", "2008-01", "2010-10",
   [("3.6 V6 350", "GILLET-V6-3.6", 370), ("4.0 V6 380", "GILLET-V6-4.0", 410)], portes=2, places=2, reservoir=60,
   remarques="Présentée au Salon de Bruxelles 2008 ; V6 d'origine Alfa Romeo ; données indicatives")
mg(L, "Vertigo .5", "Vertigo .5", "2", "2010-11", None, [("Spirit 4.2 V8 420", "F136-4.2", 460)], portes=2, places=2, reservoir=60,
   remarques="Vertigo .5 Spirit, V8 Maserati 4,2 l à carter sec ; production à la demande")

MOT = Motorisations("Gillet", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Gillet": L}
MOTEURS = MOT.moteurs()
