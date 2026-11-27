"""Erskine : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Marque économique de Studebaker (1927-1930, nommée d'après Albert Erskine) : Model 50 (six cylindres Continental) et Model 51.
Puissances brutes converties en ch (× 1,014). Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "CONTINENTAL-L6-2.6": f("ATM", "ESS", 2.6, "NC", 6, 3200, 1600, "SAE30", 4.5, 3000),
    "STUDE-L6-3.4": f("ATM", "ESS", 3.4, "NC", 6, 3200, 1600, "SAE30", 5.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Erskine", lambda fam: "Continental" if fam.startswith("CONTINENTAL") else "Studebaker")
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Model 50", "50", "1", "1927-01", "1929-06", [("2.6 L6 41", "CONTINENTAL-L6-2.6", 140)], portes=4, places=5, reservoir=50,
   remarques="Berline compacte à carrosserie dessinée par Ray Dietrich ; " + IND)
mg(L, "Model 51", "51", "1", "1929-07", "1930-12", [("3.4 L6 71", "STUDE-L6-3.4", 200)], portes=4, places=5, reservoir=55, remarques="Six cylindres Studebaker ; " + IND)

MOT = Motorisations("Erskine", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Erskine": L}
MOTEURS = MOT.moteurs()
