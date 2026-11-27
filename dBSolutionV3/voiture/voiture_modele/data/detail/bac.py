"""BAC (Briggs Automotive Company) : générations, phases, motorisations (marché européen) et moteurs liés.
Mono (1re génération 2011-2022, Cosworth 2.3 puis Mountune 2.5), Mono R (2019-) et Mono 2e génération (2023-).
Quatre cylindres atmosphériques dérivés du Ford Duratec, préparés par Cosworth puis Mountune. Puissances bhp converties en ch (× 1,014).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C = "CHAINE"
COSWORTH = {"COSWORTH-BAC-2.3": f("ATM", E_, 2.3, C, 4, 7700, 6000, "5W40", 5.0, 5000)}
MOUNTUNE = {
    "MOUNTUNE-BAC-2.5": f("ATM", E_, 2.5, C, 4, 8000, 5500, "5W40", 5.0, 5000),
    "MOUNTUNE-BAC-2.5R": f("ATM", E_, 2.5, C, 4, 8800, 6500, "5W40", 5.0, 5000),
}
FAMILLES = {**COSWORTH, **MOUNTUNE}


def motoriste(fam):
    return "Cosworth" if fam in COSWORTH else "Mountune"


mg = SaisieMoteurs(FAMILLES, "BAC", motoriste)
L = []
MONO = "Monoplace homologuée pour la route, châssis carbone, moteur central arrière"

mg(L, "Mono", "Mono", "1", "2011-01", "2022-12", [("2.3 284", "COSWORTH-BAC-2.3", 281, {"fin": "2015-12"}), ("2.5 309", "MOUNTUNE-BAC-2.5", 308, {"debut": "2016-01"})],
   portes=0, places=1, reservoir=35, remarques=MONO + " ; Cosworth 2.3 (2011-2015) puis Mountune 2.5 (2016)")
mg(L, "Mono R", "Mono R", "1", "2019-07", None, [("2.5 348", "MOUNTUNE-BAC-2.5R", 330)], portes=0, places=1, reservoir=35,
   remarques=MONO + " ; Mountune 2.5 à course réduite, 8 800 tr/min, carrosserie en graphène")
mg(L, "Mono", "Mono II", "1", "2023-08", None, [("2.5 315", "MOUNTUNE-BAC-2.5", 313, {"fin": "2024-12"}), ("2.5 319", "MOUNTUNE-BAC-2.5", 313, {"debut": "2025-01"}),
                                                ("Cup 2.5 340", "MOUNTUNE-BAC-2.5", 330, {"debut": "2025-01"})], portes=0, places=1, reservoir=35,
   remarques=MONO + " ; 2e génération (Monterey 2023), millésime 2025 à 315 bhp ; Mono Cup orientée circuit")

MOT = Motorisations("BAC", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"BAC Mono": L}
MOTEURS = MOT.moteurs()
