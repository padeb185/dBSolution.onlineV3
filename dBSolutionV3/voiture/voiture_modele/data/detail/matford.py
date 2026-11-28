"""Matford (Ford SAF et Mathis, Strasbourg puis Poissy, 1934-1940) : générations, phases, motorisations (marché français) et moteurs liés.
V8-48, V8-62 (« Alsace »), F82 et F92A ; V8 Ford à soupapes latérales 3,6 l et 2,2 l. Puissances en ch.
Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "FORD-V8-3.6": f("ATM", "ESS", 3.6, "NC", 8, 3800, 2000, "SAE30", 4.7, 3000, a="V"),
    "FORD-V8-2.2": f("ATM", "ESS", 2.2, "NC", 8, 3600, 2000, "SAE30", 4.0, 3000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Ford")
L = []
IND = "données indicatives (marque ancienne), à vérifier"
mg(L, "V8-48", "V8-48", "1", "1934-01", "1936-12", [("3.6 V8 90", "FORD-V8-3.6", 210)], portes=4, places=5, reservoir=60, remarques="Ford V8 Model 48 assemblée à Strasbourg ; " + IND)
mg(L, "V8-62", "V8-62", "1", "1936-01", "1937-12", [("2.2 V8 60", "FORD-V8-2.2", 128)], portes=4, places=5, reservoir=55, remarques="« Alsace » 13 CV ; " + IND)
mg(L, "F82", "F82", "1", "1938-01", "1939-12", [("2.2 V8 60", "FORD-V8-2.2", 128)], portes=4, places=5, reservoir=55, remarques=IND)
mg(L, "F92A", "F92A", "1", "1938-01", "1940-12", [("3.6 V8 90", "FORD-V8-3.6", 210)], portes=4, places=5, reservoir=60, remarques=IND)

MOT = Motorisations("Ford", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Matford": L}
MOTEURS = MOT.moteurs()
