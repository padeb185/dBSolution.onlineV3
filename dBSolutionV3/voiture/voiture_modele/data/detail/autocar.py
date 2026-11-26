"""Autocar : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Camions lourds : DC (1950-1980), Xpeditor (1993-) et ACX (2006-), principalement bennes à ordures à cabine avancée.
Diesels Cummins. Puissances SAE converties en ch (× 1,014). Désignations et dates indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

D = "DSL"
FAMILLES = {
    "CUMMINS-NH-14": f("ATM", D, 14.0, "NC", 6, 2100, 1500, "15W40", 30.0, 15000),
    "CUMMINS-ISC-8.3": f("TURBO", D, 8.3, "NC", 6, 2200, 1400, "15W40", 23.0, 25000),
    "CUMMINS-ISL-8.9": f("TURBO", D, 8.9, "NC", 6, 2100, 1400, "15W40", 26.0, 25000),
}
mg = SaisieMoteurs(FAMILLES, "Cummins", lambda fam: "Cummins")
L = []
IND = "marché nord-américain ; désignations et dates indicatives, à vérifier"

mg(L, "DC", "DC", "1", "1950-01", "1980-12", [("14.0 Cummins NH 223", "CUMMINS-NH-14", 830)], portes=2, places=2, reservoir=380, remarques="Camion lourd conventionnel ; " + IND)
mg(L, "Xpeditor", "Xpeditor", "1", "1993-01", None, [("8.3 Cummins 304", "CUMMINS-ISC-8.3", 1220, {"fin": "2006-12"}), ("8.9 Cummins 335", "CUMMINS-ISL-8.9", 1355, {"debut": "2004-01"})],
   portes=2, places=3, reservoir=300, remarques="Benne à ordures à cabine avancée ; " + IND)
mg(L, "ACX", "ACX", "1", "2006-01", None, [("8.9 Cummins 355", "CUMMINS-ISL-8.9", 1355)], portes=2, places=3, reservoir=300,
   remarques="Benne à ordures à cabine avancée basse ; versions gaz naturel non reprises ; " + IND)

MOT = Motorisations("Autocar", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Autocar": L}
MOTEURS = MOT.moteurs()
