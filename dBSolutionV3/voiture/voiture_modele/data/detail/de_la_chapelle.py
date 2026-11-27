"""De la Chapelle : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur français : Type 55 (réplique de la Bugatti Type 55, mécanique BMW, 1977-1997) et Roadster (1999-2010, mécanique PSA).
Puissances en ch. Données indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
BMW = {"BMW-M30-2.8": f("ATM", E_, 2.8, "CHAINE", 6, 5800, 4200, "10W40", 5.75, 10000)}
PSA = {"PSA-EW10-2.0": f("ATM", E_, 2.0, "COURROIE", 4, 6000, 4100, "5W40", 4.25, 20000)}
FAMILLES = {**BMW, **PSA}
mg = SaisieMoteurs(FAMILLES, "De la Chapelle", lambda fam: "BMW" if fam in BMW else "PSA")
L = []
IND = "données indicatives, à vérifier"

mg(L, "Type 55", "Type 55", "1", "1977-01", "1997-12", [("2.8 L6 170", "BMW-M30-2.8", 235)], portes=2, places=2, reservoir=60,
   remarques="Réplique de la Bugatti Type 55 sur mécanique BMW ; " + IND)
mg(L, "Roadster", "Roadster", "1", "1999-01", "2010-12", [("2.0 136", "PSA-EW10-2.0", 190)], portes=2, places=2, reservoir=55,
   remarques="Roadster néo-rétro sur mécanique PSA ; " + IND)

MOT = Motorisations("De la Chapelle", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"De la Chapelle": L}
MOTEURS = MOT.moteurs()
