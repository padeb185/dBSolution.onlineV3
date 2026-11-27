"""Gruau : générations, phases, motorisations (marché européen) et moteurs liés.
Carrossier-constructeur de Laval : Microbus (minibus sur base d'utilitaires, depuis 1980, ici sur base Renault Master / Iveco)
et Electron (utilitaire électrique, 2011-2016). Mécaniques des véhicules de base ; données indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

FAMILLES = {
    "GRUAU-2.3D": f("TURBO", "DSL", 2.3, "CHAINE", 4, 3500, 1500, "5W30", 7.0, 40000),
    "GRUAU-EV": electrique(),
}
mg = SaisieMoteurs(FAMILLES, "Gruau", lambda fam: "Gruau")
L = []
IND = "mécanique du véhicule de base ; données indicatives, à vérifier"

mg(L, "Microbus", "Microbus", "1", "1980-01", None, [("2.3 D 150", "GRUAU-2.3D", 350)], portes=4, places=9, reservoir=100,
   remarques="Minibus scolaire et de transport (bases successives Renault, Peugeot, Iveco) ; " + IND)
mg(L, "Electron", "Electron", "1", "2011-01", "2016-12", [("Électrique 40 kWh 82", "GRUAU-EV", 220, {"batterie": 40})], portes=4, places=2, reservoir=0,
   remarques="Utilitaire électrique (fourgon) ; " + IND)

MOT = Motorisations("Gruau", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Gruau": L}
MOTEURS = MOT.moteurs()
