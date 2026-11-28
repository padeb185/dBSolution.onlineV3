"""Iran Khodro (IKCO, Téhéran) : générations, phases, motorisations (marché iranien) et moteurs liés.
Paykan (Hillman Hunter, 1967-2005) et Paykan pick-up (Bardo), Peugeot 405 et Pars, Samand / Soren, Arisun (pick-up), Runna / Runna+,
Dena / Dena+ / Dena+ Turbo, Tara et Reera. Moteurs PSA XU7 / TU5 (codes et couples repris de citroen.py et peugeot.py) et IKCO EF7 ajoutés.
Peugeot 206 / 207 / 2008 assemblées sous licence non reprises. Puissances en ch. Données indicatives (marché hors Europe).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .citroen import FAMILLES as FAMILLES_CITROEN
from .peugeot import FAMILLES as FAMILLES_PEUGEOT

E_ = "ESS"
FAMILLES = {
    "ROOTES-1.7": f("ATM", E_, 1.7, "CHAINE", 4, 5000, 3000, "20W50", 4.5, 5000),
    "XU7": FAMILLES_CITROEN["XU7"], "TU5J4": FAMILLES_PEUGEOT["TU5J4"],
    "IKCO-EF7-1.7": f("ATM", E_, 1.65, "COURROIE", 4, 6000, 4500, "10W40", 4.0, 10000),
    "IKCO-EF7TC-1.7T": f("TURBO", E_, 1.65, "COURROIE", 4, 5500, 2200, "10W40", 4.0, 10000),
}


def motoriste(fam):
    return "Peugeot" if fam in ("XU7", "TU5J4") else ("Hillman" if fam.startswith("ROOTES") else "Iran Khodro")


mg = SaisieMoteurs(FAMILLES, "Iran Khodro", motoriste)
L = []
IND = "marché iranien ; données indicatives"

mg(L, "Paykan", "Paykan", "1", "1967-01", "2005-05", [("1.7 72", "ROOTES-1.7", 130)], portes=4, places=5, reservoir=45, remarques="Hillman Hunter sous licence Rootes ; " + IND)
mg(L, "Paykan Pickup", "Bardo", "1", "1970-01", "2015-12", [("1.7 72", "ROOTES-1.7", 130)], portes=2, places=2, reservoir=45, remarques="Pick-up dérivé de la Paykan ; " + IND)
mg(L, "Peugeot 405", "405", "1", "1993-01", "2020-12", [("1.8 99", "XU7", 147)], portes=4, places=5, reservoir=60, remarques="Peugeot 405 assemblée sous licence (GLX, SLX) ; " + IND)
mg(L, "Peugeot Pars", "Pars", "1", "1999-01", None, [("1.8 99", "XU7", 147), ("1.7 113", "IKCO-EF7-1.7", 155, {"debut": "2012-01"}), ("1.6 16v 110", "TU5J4", 147, {"debut": "2014-01"})],
   portes=4, places=5, reservoir=60, remarques="Évolution iranienne de la 405 ; " + IND)
mg(L, "Samand", "Samand", "1", "2002-01", "2021-12", [("1.8 99", "XU7", 147), ("1.7 113", "IKCO-EF7-1.7", 155, {"debut": "2009-01"})], portes=4, places=5, reservoir=55,
   remarques="Première voiture nationale iranienne, base 405 ; dont Samand LX et version bicarburation GNV ; " + IND)
mg(L, "Samand Soren", "Samand", "S", "2007-01", None, [("1.8 99", "XU7", 147), ("1.7 113", "IKCO-EF7-1.7", 155, {"debut": "2009-01"}), ("Turbo 1.7 150", "IKCO-EF7TC-1.7T", 215, {"debut": "2019-01"})],
   portes=4, places=5, reservoir=55, remarques="Soren et Soren+ / Soren Plus ; " + IND)
mg(L, "Arisun", "Arisun", "1", "2008-01", None, [("1.8 99", "XU7", 147), ("1.7 113", "IKCO-EF7-1.7", 155, {"debut": "2014-01"})], portes=2, places=2, reservoir=45,
   remarques="Pick-up sur base Samand, puis Arisun 2 ; " + IND)
mg(L, "Runna", "Runna", "1", "2010-01", "2020-12", [("1.6 16v 110", "TU5J4", 147)], portes=4, places=5, reservoir=50, remarques="Berline dérivée de la Peugeot 206 ; " + IND)
mg(L, "Runna+", "Runna", "2", "2020-01", None, [("1.6 16v 110", "TU5J4", 147)], portes=4, places=5, reservoir=50, remarques=IND)
mg(L, "Dena", "Dena", "1", "2011-01", "2021-12", [("1.7 113", "IKCO-EF7-1.7", 155), ("1.6 16v 110", "TU5J4", 147)], portes=4, places=5, reservoir=55, remarques=IND)
mg(L, "Dena+", "Dena", "2", "2015-01", None, [("1.7 113", "IKCO-EF7-1.7", 155)], portes=4, places=5, reservoir=55, remarques=IND)
mg(L, "Dena+ Turbo", "Dena", "T", "2017-01", None, [("Turbo 1.7 150", "IKCO-EF7TC-1.7T", 215)], portes=4, places=5, reservoir=55, remarques=IND)
mg(L, "Tara", "Tara", "1", "2019-01", None, [("1.6 16v 110", "TU5J4", 147)], portes=4, places=5, reservoir=50, remarques="Berline sur plateforme Peugeot 301 ; " + IND)
mg(L, "Reera", "Reera", "1", "2023-01", None, [("Turbo 1.7 150", "IKCO-EF7TC-1.7T", 215)], portes=5, places=5, reservoir=50, remarques="Crossover ; " + IND)

MOT = Motorisations("Iran Khodro", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Iran Khodro": L}
MOTEURS = MOT.moteurs()
