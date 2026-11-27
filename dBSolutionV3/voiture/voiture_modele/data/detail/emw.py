"""EMW (Eisenacher Motorenwerk) : générations, phases, motorisations (marché européen) et moteurs liés.
Ancienne usine BMW d'Eisenach en RDA (1945-1955) : 340 (berline dérivée de la BMW 326, 1949-1955) et 327 (coupé / cabriolet, 1952-1955).
Six cylindres 2.0 d'origine BMW. Puissances en ch DIN. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {"EMW-L6-2.0": f("ATM", "ESS", 2.0, "NC", 6, 3750, 2000, "SAE30", 5.0, 3000)}
mg = SaisieMoteurs(FAMILLES, "EMW", lambda fam: "EMW")
L = []
IND = "six cylindres 2.0 d'origine BMW (M78) ; données indicatives"

mg(L, "340", "340", "1", "1949-01", "1955-12", [("2.0 L6 55", "EMW-L6-2.0", 130)], portes=4, places=5, reservoir=50, remarques="Berline, break et ambulance ; " + IND)
mg(L, "327", "327", "1", "1952-01", "1955-12", [("2.0 L6 55", "EMW-L6-2.0", 130)], portes=2, places=4, reservoir=50, remarques="Coupé et cabriolet ; " + IND)

MOT = Motorisations("EMW", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"EMW": L}
MOTEURS = MOT.moteurs()
