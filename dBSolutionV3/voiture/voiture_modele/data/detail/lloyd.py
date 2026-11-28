"""Lloyd (groupe Borgward, Brême, 1950-1963) : générations, phases, motorisations (marché européen) et moteurs liés.
LP 300 (« Leukoplastbomber », caisse en contreplaqué recouvert de similicuir), LP 400, LP 600 Alexander (quatre temps) et Arabella (flat-4).
Deux-temps : distribution « aucune », huile « à choisir » (mélange). Puissances en ch DIN. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "LLOYD-2T-0.3": f("ATM", "ESS", 0.3, "AUCUNE", 2, 4000, 2600, "CHOISIR", 0.0, 3000),
    "LLOYD-2T-0.4": f("ATM", "ESS", 0.4, "AUCUNE", 2, 4000, 2600, "CHOISIR", 0.0, 3000),
    "LLOYD-2C-0.6": f("ATM", "ESS", 0.6, "NC", 2, 4500, 3000, "SAE30", 2.5, 3000),
    "LLOYD-B4-0.9": f("ATM", "ESS", 0.9, "NC", 4, 5000, 3000, "20W50", 3.0, 5000, a="PLAT"),
}
mg = SaisieMoteurs(FAMILLES, "Lloyd")
L = []
IND = "données indicatives"
mg(L, "LP 300", "LP 300", "1", "1950-05", "1952-12", [("0.3 10", "LLOYD-2T-0.3", 19)], portes=2, places=4, reservoir=20, remarques="Bicylindre deux temps refroidi par air ; " + IND)
mg(L, "LP 400", "LP 400", "1", "1953-01", "1957-12", [("0.4 13", "LLOYD-2T-0.4", 25)], portes=2, places=4, reservoir=25, remarques="Caisse progressivement en acier ; " + IND)
mg(L, "LP 600 Alexander", "LP 600", "1", "1955-01", "1961-12", [("0.6 19", "LLOYD-2C-0.6", 37), ("Alexander TS 0.6 25", "LLOYD-2C-0.6", 42, {"debut": "1958-01"})], portes=2, places=4, reservoir=25,
   remarques="Bicylindre quatre temps ; Alexander (1958) et Alexander TS ; " + IND)
mg(L, "Arabella", "Arabella", "1", "1959-01", "1963-12", [("0.9 38", "LLOYD-B4-0.9", 66), ("de Luxe 0.9 45", "LLOYD-B4-0.9", 68, {"debut": "1961-01"})], portes=2, places=4, reservoir=35,
   remarques="Flat-4 refroidi par eau, traction ; vendue Borgward Arabella en 1961-1963 ; " + IND)

MOT = Motorisations("Lloyd", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Lloyd": L}
MOTEURS = MOT.moteurs()
