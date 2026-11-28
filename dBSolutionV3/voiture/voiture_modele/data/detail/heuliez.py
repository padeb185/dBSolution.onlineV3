"""Heuliez (Heuliez Bus, Rorthais) : générations, phases, motorisations (marché français) et moteurs liés.
Autobus urbains standards de 12 m : GX 107 (châssis Renault PR 100), GX 317 et GX 327 (Access'Bus, plancher bas) et GX 337
(Iveco Bus, diesel, GNV et électrique « E », vendu E-Way hors des pays francophones). Les voitures carrossées ou assemblées par
Heuliez (Peugeot 205 / 206 CC, Citroën BX / XM Break, Opel Tigra TwinTop…) sont rattachées à leur marque et ne sont pas reprises ici.
Nombre de portes : 3 (portes de service) ; places : capacité totale indicative. Puissances en ch. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

D = "DSL"
FAMILLES = {
    "RENAULT-MIDS-06.20.45": f("TURBO", D, 9.8, "NC", 6, 2200, 1200, "15W40", 25.0, 30000),
    "IVECO-CURSOR8": f("TURBO", D, 7.8, "NC", 6, 2200, 1200, "10W40", 25.0, 40000),
    "IVECO-CURSOR8-GNV": f("TURBO", "CNG", 7.8, "NC", 6, 2000, 1100, "10W40", 25.0, 40000),
    "FPT-TECTOR7": f("TURBO", D, 6.7, "NC", 6, 2500, 1250, "10W40", 18.0, 40000),
    "HEULIEZ-ELEC": electrique(40000),
}
mg = SaisieMoteurs(FAMILLES, "Iveco", lambda fam: "Renault" if fam.startswith("RENAULT") else ("Heuliez" if fam == "HEULIEZ-ELEC" else "Iveco"))
L = []
IND = "autobus urbain ; données indicatives"

mg(L, "GX 107", "GX 107", "1", "1984-01", "2000-12", [("Diesel 9.8 L6 230", "RENAULT-MIDS-06.20.45", 900)], portes=3, places=100, reservoir=250,
   remarques="Sur châssis Renault PR 100, 2 ou 3 portes, 25 à 41 places assises ; " + IND)
mg(L, "GX 317", "GX 317", "1", "1994-01", "2005-12", [("Diesel 9.8 L6 253", "RENAULT-MIDS-06.20.45", 1000), ("GNV 7.8 L6 272", "IVECO-CURSOR8-GNV", 1100, {"debut": "2004-01"})],
   portes=3, places=100, reservoir=250, remarques="Access'Bus à plancher bas sur châssis Renault ; " + IND)
mg(L, "GX 327", "GX 327", "1", "2005-01", "2013-12",
   [("Diesel 7.8 L6 290", "IVECO-CURSOR8", 1100), ("GNV 7.8 L6 209", "IVECO-CURSOR8-GNV", 900), ("GNV 7.8 L6 272", "IVECO-CURSOR8-GNV", 1100)],
   portes=3, places=100, reservoir=250, remarques="Même châssis et moteur que l'Irisbus Citelis ; " + IND)
mg(L, "GX 337", "GX 337", "1", "2013-10", None,
   [("Diesel 6.7 L6 286", "FPT-TECTOR7", 1000), ("GNV 7.8 L6 272", "IVECO-CURSOR8-GNV", 1100, {"debut": "2017-09"}),
    ("E Électrique 218", "HEULIEZ-ELEC", 2000, {"debut": "2016-01", "reservoir": 0, "batterie": 350, "remarques": "GX 337 Elec puis GX 337 E (Iveco E-Way) ; batterie et puissance selon configuration, indicatives"})],
   portes=3, places=100, reservoir=250, remarques="Remplaçant du GX 327 (Euro 6), versions hybride et H2 non reprises ; " + IND)

MOT = Motorisations("Iveco", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Heuliez": L}
MOTEURS = MOT.moteurs()
