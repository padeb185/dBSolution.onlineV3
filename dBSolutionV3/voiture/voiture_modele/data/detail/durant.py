"""Durant : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Durant Motors (William C. Durant, 1921-1931) : Model A-22, Model 40 et Model 65. Six cylindres Continental.
Puissances brutes converties en ch (× 1,014). Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "CONTINENTAL-L6-4.2": f("ATM", "ESS", 4.2, "NC", 6, 2600, 1200, "SAE30", 5.5, 3000),
    "CONTINENTAL-L6-3.0": f("ATM", "ESS", 3.0, "NC", 6, 3000, 1400, "SAE30", 5.0, 3000),
    "CONTINENTAL-L6-3.4": f("ATM", "ESS", 3.4, "NC", 6, 3200, 1600, "SAE30", 5.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Continental", lambda fam: "Continental")
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Model A-22", "A-22", "1", "1922-01", "1926-12", [("4.2 L6 71", "CONTINENTAL-L6-4.2", 250)], portes=4, places=5, reservoir=65, remarques="Berline et torpédo ; " + IND)
mg(L, "Model 40", "40", "1", "1926-01", "1928-12", [("3.0 L6 41", "CONTINENTAL-L6-3.0", 160)], portes=4, places=5, reservoir=55, remarques="Berline ; " + IND)
mg(L, "Model 65", "65", "1", "1928-01", "1929-12", [("3.4 L6 66", "CONTINENTAL-L6-3.4", 200)], portes=4, places=5, reservoir=60, remarques="Berline ; " + IND)

MOT = Motorisations("Durant", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Durant": L}
MOTEURS = MOT.moteurs()
