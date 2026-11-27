"""Dort : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Dort Motor Car Company (Flint, 1915-1924, J. Dallas Dort) : Model 5, Model 11 et Model 27 (six cylindres).
Puissances brutes converties en ch (× 1,014). Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "LYCOMING-L4-3.0": f("ATM", "ESS", 3.0, "NC", 4, 2000, 1000, "SAE30", 4.5, 2000),
    "FALLS-L6-3.2": f("ATM", "ESS", 3.2, "NC", 6, 2600, 1200, "SAE30", 5.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Dort", lambda fam: "Lycoming" if fam.startswith("LYCOMING") else "Falls")
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Model 5", "5", "1", "1915-01", "1918-12", [("3.0 28", "LYCOMING-L4-3.0", 130)], portes=4, places=5, reservoir=50, remarques="Torpédo ; " + IND)
mg(L, "Model 11", "11", "1", "1918-01", "1921-12", [("3.0 28", "LYCOMING-L4-3.0", 130)], portes=4, places=5, reservoir=50, remarques="Berline ; " + IND)
mg(L, "Model 27", "27", "1", "1921-01", "1924-12", [("3.2 L6 46", "FALLS-L6-3.2", 170)], portes=4, places=5, reservoir=55, remarques="Berline six cylindres ; " + IND)

MOT = Motorisations("Dort", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Dort": L}
MOTEURS = MOT.moteurs()
