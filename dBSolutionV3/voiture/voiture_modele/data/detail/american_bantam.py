"""American Bantam : générations, phases, motorisations (marché nord-américain) et moteurs liés.
60 / 65 (petites voitures dérivées de l'Austin Seven, 1938-1941) et BRC-40 (premier véhicule de reconnaissance « Jeep », 1941).
Quatre cylindres Bantam (dérivé Austin Seven) et Continental ajoutés. Puissances brutes converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"

FAMILLES = {
    "BANTAM-0.75": f("ATM", E_, 0.75, "NC", 4, 3500, 2000, "SAE30", 2.5, 3000),
    "CONTINENTAL-BY4112": f("ATM", E_, 2.0, "NC", 4, 3500, 2000, "SAE30", 4.0, 3000),
}


def motoriste(fam):
    return "Continental" if fam == "CONTINENTAL-BY4112" else "American Bantam"


mg = SaisieMoteurs(FAMILLES, "American Bantam", motoriste)
L = []
IND = "marché nord-américain ; données indicatives"

mg(L, "60", "60", "1", "1938-01", "1941-12", [("0.75 20", "BANTAM-0.75", 46), ("65 0.75 22", "BANTAM-0.75", 48, {"debut": "1940-01"})], portes=2, places=2, reservoir=30,
   remarques="Roadster, coupé, break et utilitaires ; dérivée de l'Austin Seven (60 puis 65) ; " + IND)
mg(L, "BRC-40", "BRC", "1", "1941-01", "1941-12", [("2.0 46", "CONTINENTAL-BY4112", 115)], portes=0, places=4, reservoir=38,
   remarques="Véhicule de reconnaissance militaire 4x4, environ 2 600 exemplaires (ancêtre de la Jeep) ; " + IND)

MOT = Motorisations("American Bantam", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"American Bantam": L}
MOTEURS = MOT.moteurs()
