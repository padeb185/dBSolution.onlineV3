"""Essex : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Marque économique de Hudson (Detroit, 1919-1933) : Four, Coach (première berline fermée bon marché), Super Six et Terraplane.
Puissances brutes converties en ch (× 1,014). Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "ESSEX-2.9": f("ATM", E_, 2.9, "NC", 4, 2600, 1400, "SAE30", 4.5, 3000),
    "ESSEX-L6-2.1": f("ATM", E_, 2.1, "NC", 6, 3000, 1600, "SAE30", 4.5, 3000),
    "ESSEX-L6-2.6": f("ATM", E_, 2.6, "NC", 6, 3400, 1800, "SAE30", 4.5, 3000),
    "ESSEX-L6-3.2": f("ATM", E_, 3.2, "NC", 6, 3200, 1600, "SAE30", 5.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Hudson", lambda fam: "Hudson")
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Four", "Four", "1", "1919-01", "1923-12", [("2.9 56", "ESSEX-2.9", 160)], portes=4, places=5, reservoir=50, remarques="Torpédo et berline, soupapes en F ; " + IND)
mg(L, "Coach", "Coach", "1", "1922-01", "1926-12", [("2.9 56", "ESSEX-2.9", 160, {"fin": "1923-12"}), ("2.1 L6 30", "ESSEX-L6-2.1", 110, {"debut": "1924-01"})],
   portes=2, places=5, reservoir=50, remarques="Berline 2 portes fermée à bas prix ; Essex Six à partir de 1924 ; " + IND)
mg(L, "Super Six", "Super Six", "1", "1927-01", "1932-12", [("2.6 L6 56", "ESSEX-L6-2.6", 170)], portes=4, places=5, reservoir=55, remarques="Berlines, coupés et cabriolets ; " + IND)
mg(L, "Terraplane", "Terraplane", "1", "1932-07", "1933-12", [("3.2 L6 71", "ESSEX-L6-3.2", 200)], portes=2, places=5, reservoir=55,
   remarques="Essex-Terraplane, devenue marque Terraplane (Hudson) en 1934 ; " + IND)

MOT = Motorisations("Essex", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Essex": L}
MOTEURS = MOT.moteurs()
