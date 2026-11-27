"""Duesenberg : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Model A (premier huit cylindres en ligne de série américain, 1921-1926), Model X (1927), Model J (1928-1937), SJ (compresseur,
1932-1937) et SSJ (1935, 2 exemplaires). Huit cylindres en ligne 4.3 puis 6.9 double arbre (Lycoming).
Puissances brutes converties en ch (× 1,014). Couples indicatifs.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
DUESENBERG = {"DUESENBERG-L8-4.3": f("ATM", E_, 4.3, "NC", 8, 3600, 2000, "SAE30", 7.0, 3000)}
LYCOMING = {
    "LYCOMING-J-6.9": f("ATM", E_, 6.9, "CHAINE", 8, 4200, 2000, "SAE30", 9.0, 3000),
    "LYCOMING-J-6.9SC": f("TURBO", E_, 6.9, "CHAINE", 8, 4750, 2500, "SAE30", 9.0, 3000),
}
FAMILLES = {**DUESENBERG, **LYCOMING}
mg = SaisieMoteurs(FAMILLES, "Duesenberg", lambda fam: "Lycoming" if fam in LYCOMING else "Duesenberg")
L = []
NA = "marché nord-américain ; couples indicatifs"

mg(L, "Model A", "A", "1", "1921-01", "1926-12", [("4.3 L8 101", "DUESENBERG-L8-4.3", 230)], portes=4, places=5, reservoir=80,
   remarques="Huit cylindres en ligne à arbre à cames en tête, freins hydrauliques aux quatre roues ; " + NA)
mg(L, "Model X", "X", "1", "1927-01", "1927-12", [("4.3 L8 101", "DUESENBERG-L8-4.3", 230)], portes=4, places=5, reservoir=80, remarques="Évolution de la Model A, 13 exemplaires ; " + NA)
mg(L, "Model J", "J", "1", "1928-12", "1937-12", [("6.9 L8 269", "LYCOMING-J-6.9", 508)], portes=4, places=5, reservoir=100,
   remarques="Châssis carrossés (Murphy, LeBaron, Rollston, Derham…), double arbre 32 soupapes ; " + NA)
mg(L, "Model SJ", "SJ", "1", "1932-05", "1937-12", [("Supercharged 6.9 L8 324", "LYCOMING-J-6.9SC", 576)], portes=2, places=4, reservoir=100,
   remarques="Model J à compresseur centrifuge, échappements extérieurs chromés ; " + NA)
mg(L, "Model SSJ", "SSJ", "1", "1935-01", "1935-12", [("Supercharged 6.9 L8 406", "LYCOMING-J-6.9SC", 650)], portes=2, places=2, reservoir=100,
   remarques="Roadster à empattement court, 2 exemplaires (Gary Cooper, Clark Gable) ; " + NA)

MOT = Motorisations("Duesenberg", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Duesenberg": L}
MOTEURS = MOT.moteurs()
