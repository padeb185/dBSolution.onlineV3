"""Magirus-Deutz (Ulm, groupe KHD) : générations, phases, motorisations (marché européen) et moteurs liés.
Camions à capot « Rundhauber » à diesels Deutz refroidis par air (Mercur, Saturn, Uranus, Jupiter militaire) puis « Eckhauber » à capot
anguleux (1965-1985) ; intégré à Iveco en 1975. Puissances en ch DIN. Poids lourds aux configurations multiples : une motorisation
représentative, désignations et données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "DEUTZ-F4L-5.3": f("ATM", "DSL", 5.3, "NC", 4, 2300, 1400, "15W40", 12.0, 5000),
    "DEUTZ-F6L-7.9": f("ATM", "DSL", 7.9, "NC", 6, 2300, 1400, "15W40", 16.0, 5000),
    "DEUTZ-F8L-10.6": f("ATM", "DSL", 10.6, "NC", 8, 2300, 1400, "15W40", 20.0, 5000, a="V"),
    "DEUTZ-F8L-12.7": f("ATM", "DSL", 12.7, "NC", 8, 2300, 1400, "15W40", 24.0, 10000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Deutz")
L = []
IND = "camion ; motorisations multiples, données indicatives"
mg(L, "Saturn", "Rundhauber", "1", "1953-01", "1970-12", [("Diesel 5.3 L4 90", "DEUTZ-F4L-5.3", 320)], portes=2, places=2, reservoir=120, remarques="Camion moyen, diesel refroidi par air ; " + IND)
mg(L, "Mercur", "Rundhauber", "1", "1952-01", "1970-12", [("Diesel 7.9 L6 125", "DEUTZ-F6L-7.9", 450)], portes=2, places=2, reservoir=150, remarques=IND)
mg(L, "Uranus", "Rundhauber", "1", "1953-01", "1966-12", [("Diesel 10.6 V8 175", "DEUTZ-F8L-10.6", 620)], portes=2, places=2, reservoir=200, remarques="Camion lourd ; " + IND)
mg(L, "Jupiter", "Jupiter", "1", "1955-01", "1965-12", [("Diesel 12.7 V8 178", "DEUTZ-F8L-12.7", 680)], portes=2, places=2, reservoir=200, remarques="Tout-terrain 6x6 de la Bundeswehr ; " + IND)
mg(L, "Eckhauber", "Eckhauber", "1", "1965-01", "1985-12", [("Diesel 12.7 V8 256", "DEUTZ-F8L-12.7", 900)], portes=2, places=2, reservoir=300, remarques="Capot anguleux, dont versions chantier ; " + IND)

MOT = Motorisations("Deutz", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Magirus-Deutz": L}
MOTEURS = MOT.moteurs()
