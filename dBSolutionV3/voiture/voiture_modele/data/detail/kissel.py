"""Kissel (Kissel Motor Car Company, Hartford, Wisconsin, 1906-1931) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Kissel Kar 6-60, Gold Bug (speedster rendu célèbre par Amelia Earhart) et White Eagle (huit cylindres Lycoming).
Puissances brutes converties en ch (× 1,014). Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "KISSEL-L6-6.4": f("ATM", "ESS", 6.4, "NC", 6, 2200, 1100, "SAE30", 6.0, 2000),
    "KISSEL-L6-4.3": f("ATM", "ESS", 4.3, "NC", 6, 2600, 1300, "SAE30", 5.0, 3000),
    "LYCOMING-L8-4.9": f("ATM", "ESS", 4.9, "NC", 8, 3300, 1600, "SAE30", 6.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Kissel", lambda fam: "Lycoming" if fam.startswith("LYCOMING") else "Kissel")
L = []
IND = "marché nord-américain ; données indicatives (marque ancienne), à vérifier"
mg(L, "Kissel Kar 6-60", "6-60", "1", "1913-01", "1917-12", [("6.4 L6 61", "KISSEL-L6-6.4", 250)], portes=4, places=5, reservoir=75, remarques=IND)
mg(L, "Gold Bug", "Gold Bug", "1", "1919-01", "1928-12", [("4.3 L6 62", "KISSEL-L6-4.3", 200, {"fin": "1924-12"}), ("4.9 L8 72", "LYCOMING-L8-4.9", 240, {"debut": "1925-01"})],
   portes=2, places=2, reservoir=70, remarques="Speedster ; " + IND)
mg(L, "White Eagle", "White Eagle", "1", "1929-01", "1931-12", [("4.9 L8 128", "LYCOMING-L8-4.9", 330)], portes=4, places=5, reservoir=80, remarques="Huit cylindres 8-126 ; " + IND)

MOT = Motorisations("Kissel", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Kissel": L}
MOTEURS = MOT.moteurs()
