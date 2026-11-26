"""Allstate : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Allstate (1952-1953) : Henry J de Kaiser-Frazer vendue sur catalogue par Sears, Roebuck & Co.
Quatre et six cylindres Willys ajoutés. Puissances brutes (SAE gross) converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"

FAMILLES = {
    "WILLYS-L4-2.2": f("ATM", E_, 2.2, "NC", 4, 4000, 2000, "SAE30", 4.0, 3000),
    "WILLYS-L6-2.6": f("ATM", E_, 2.6, "NC", 6, 3800, 1600, "SAE30", 4.5, 3000),
}

mg = SaisieMoteurs(FAMILLES, "Allstate", lambda fam: "Willys")
L = []

mg(L, "Allstate", "Henry J", "1", "1952-01", "1953-12", [("2.2 69", "WILLYS-L4-2.2", 155), ("2.6 L6 81", "WILLYS-L6-2.6", 183)], portes=2, places=5, reservoir=49,
   remarques="Berline 2 portes, version Sears de la Henry J (environ 2 400 ex.) ; marché nord-américain ; données indicatives")

MOT = Motorisations("Allstate", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Allstate": L}
MOTEURS = MOT.moteurs()
