"""DB (Deutsch et Bonnet) : générations, phases, motorisations (marché européen) et moteurs liés.
Coach Panhard (1952-1954), HBR5 (1954-1961) et Le Mans (cabriolet, 1959-1964), sur mécanique Panhard bicylindre à plat.
Puissances en ch. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "PANHARD-0.75": f("ATM", "ESS", 0.75, "NC", 2, 5000, 3500, "20W50", 2.5, 5000, a="PLAT"),
    "PANHARD-0.85": f("ATM", "ESS", 0.85, "NC", 2, 5300, 3500, "20W50", 2.5, 5000, a="PLAT"),
}
mg = SaisieMoteurs(FAMILLES, "Panhard", lambda fam: "Panhard")
L = []
IND = "mécanique Panhard bicylindre à plat refroidi par air ; données indicatives"

mg(L, "Coach Panhard", "Coach", "1", "1952-01", "1954-12", [("0.75 40", "PANHARD-0.75", 54), ("0.85 42", "PANHARD-0.85", 64, {"debut": "1953-01"})],
   portes=2, places=2, reservoir=40, remarques="Coupé en aluminium ; " + IND)
mg(L, "HBR5", "HBR5", "1", "1954-01", "1961-12", [("0.85 42", "PANHARD-0.85", 64), ("Super 0.85 50", "PANHARD-0.85", 68, {"debut": "1957-01"})],
   portes=2, places=2, reservoir=40, remarques="Coupé en polyester, victoires de classe aux 24 Heures du Mans ; " + IND)
mg(L, "Le Mans", "Le Mans", "1", "1959-10", "1964-12", [("0.85 50", "PANHARD-0.85", 68), ("Tigre 0.85 60", "PANHARD-0.85", 72, {"debut": "1962-01"})],
   portes=2, places=2, reservoir=40, remarques="Cabriolet 2+2 ; " + IND)

MOT = Motorisations("DB", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"DB": L}
MOTEURS = MOT.moteurs()
