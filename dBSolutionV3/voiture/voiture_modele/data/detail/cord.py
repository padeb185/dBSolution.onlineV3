"""Cord : générations, phases, motorisations (marché nord-américain) et moteurs liés.
L-29 (traction avant, 1929-1932) et 810 / 812 (carrosserie « coffin nose », 1936-1937). Huit cylindres en ligne et V8 Lycoming
(L8 4.9 de la même famille qu'auburn.py). Puissances brutes converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .auburn import FAMILLES as FAMILLES_AUBURN

FAMILLES = {
    "LYCOMING-L8-4.9": FAMILLES_AUBURN["LYCOMING-L8-4.9"],
    "LYCOMING-V8-4.7": f("ATM", "ESS", 4.7, "NC", 8, 3500, 2000, "SAE30", 6.5, 3000, a="V"),
    "LYCOMING-V8-4.7SC": f("TURBO", "ESS", 4.7, "NC", 8, 3500, 2400, "SAE30", 6.5, 3000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Lycoming", lambda fam: "Lycoming")
L = []
NA = "marché nord-américain ; données indicatives"

mg(L, "L-29", "L-29", "1", "1929-08", "1932-12", [("4.9 L8 127", "LYCOMING-L8-4.9", 315)], portes=4, places=5, reservoir=80,
   remarques="Première traction avant américaine de série ; berline, cabriolet, brougham ; " + NA)
mg(L, "810", "810", "1", "1936-01", "1936-12", [("4.7 V8 127", "LYCOMING-V8-4.7", 265)], portes=4, places=5, reservoir=75,
   remarques="Berlines Westchester / Beverly, cabriolet Phaeton et Sportsman ; phares escamotables ; " + NA)
mg(L, "812", "812", "1", "1937-01", "1937-12", [("4.7 V8 127", "LYCOMING-V8-4.7", 265), ("Supercharged 4.7 V8 173", "LYCOMING-V8-4.7SC", 330)],
   portes=4, places=5, reservoir=75, remarques="Évolution de la 810, version à compresseur (170 hp) ; " + NA)

MOT = Motorisations("Cord", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Cord": L}
MOTEURS = MOT.moteurs()
