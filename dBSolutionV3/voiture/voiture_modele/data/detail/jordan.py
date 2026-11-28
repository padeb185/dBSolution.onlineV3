"""Jordan (Jordan Motor Car Company, Cleveland, 1916-1931) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Playboy (roadster rendu célèbre par la publicité « Somewhere West of Laramie »), Line Eight et Speedway Ace, à moteurs Continental.
Puissances brutes converties en ch (× 1,014). Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "CONTINENTAL-L6-3.7": f("ATM", E_, 3.7, "NC", 6, 2800, 1400, "SAE30", 5.0, 2000),
    "CONTINENTAL-L8-4.4": f("ATM", E_, 4.4, "NC", 8, 3200, 1600, "SAE30", 6.0, 3000),
    "CONTINENTAL-L8-5.3": f("ATM", E_, 5.3, "NC", 8, 3400, 1600, "SAE30", 6.5, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Continental")
L = []
IND = "marché nord-américain ; données indicatives (marque ancienne), à vérifier"

mg(L, "Playboy", "Playboy", "1", "1919-01", "1930-12", [("3.7 L6 56", "CONTINENTAL-L6-3.7", 180, {"fin": "1924-12"}), ("4.4 L8 75", "CONTINENTAL-L8-4.4", 230, {"debut": "1925-01"})],
   portes=2, places=2, reservoir=60, remarques="Roadster sport ; " + IND)
mg(L, "Line Eight", "Line Eight", "1", "1925-01", "1930-12", [("4.4 L8 75", "CONTINENTAL-L8-4.4", 230)], portes=4, places=5, reservoir=70, remarques=IND)
mg(L, "Speedway Ace", "Speedway", "1", "1930-01", "1931-12", [("5.3 L8 116", "CONTINENTAL-L8-5.3", 320)], portes=2, places=2, reservoir=80,
   remarques="Dernière Jordan, très petite série ; " + IND)

MOT = Motorisations("Continental", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Jordan": L}
MOTEURS = MOT.moteurs()
