"""Apperson : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Jack Rabbit (quatre cylindres, 1907-1916) et Eight (V8, 1916-1926). Constructeur de Kokomo (Indiana).
Puissances brutes converties en ch (× 1,014). Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "APPERSON-6.4": f("ATM", E_, 6.4, "NC", 4, 1800, 1000, "SAE30", 6.0, 2000),
    "APPERSON-5.4V8": f("ATM", E_, 5.4, "NC", 8, 2600, 1200, "SAE30", 6.0, 2000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Apperson", lambda fam: "Apperson")
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Jack Rabbit", "Jack Rabbit", "1", "1907-01", "1916-12", [("6.4 41", "APPERSON-6.4", 200)], portes=2, places=2, reservoir=60, remarques="Roadster ; " + IND)
mg(L, "Eight", "Eight", "1", "1916-01", "1926-12", [("5.4 V8 61", "APPERSON-5.4V8", 250)], portes=4, places=5, reservoir=75, remarques="Torpédo et berlines ; " + IND)

MOT = Motorisations("Apperson", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Apperson": L}
MOTEURS = MOT.moteurs()
