"""Cole : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Cole Motor Car Company (Indianapolis, 1909-1925) : Model 30 et Aero Eight (V8 Northway).
Puissances brutes converties en ch (× 1,014). Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "COLE-4.0": f("ATM", "ESS", 4.0, "NC", 4, 1800, 1000, "SAE30", 5.0, 2000),
    "NORTHWAY-V8-5.8": f("ATM", "ESS", 5.8, "NC", 8, 2600, 1200, "SAE30", 7.0, 3000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Cole", lambda fam: "Northway" if fam.startswith("NORTHWAY") else "Cole")
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Model 30", "30", "1", "1909-01", "1914-12", [("4.0 30", "COLE-4.0", 150)], portes=4, places=5, reservoir=60, remarques="Torpédo ; " + IND)
mg(L, "Aero Eight", "Aero Eight", "1", "1916-01", "1925-12", [("5.8 V8 81", "NORTHWAY-V8-5.8", 290)], portes=4, places=7, reservoir=75, remarques="Torpédo et berline ; " + IND)

MOT = Motorisations("Cole", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Cole": L}
MOTEURS = MOT.moteurs()
