"""Messerschmitt (Fahrzeug- und Maschinenbau Regensburg, 1953-1964) : générations, phases, motorisations (marché européen) et moteurs liés.
Kabinenroller KR 175 et KR 200 (trois roues, places en tandem, verrière basculante) et Tg 500 « Tiger » (quatre roues). Moteurs deux temps
Fichtel & Sachs. Nombre de portes : 2 imposé par le référentiel (verrière basculante en réalité). Deux-temps : distribution « aucune »,
huile « à choisir » (mélange). Puissances en ch DIN. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "SACHS-2T-0.17": f("ATM", "ESS", 0.17, "AUCUNE", 1, 5250, 4500, "CHOISIR", 0.0, 3000),
    "SACHS-2T-0.19": f("ATM", "ESS", 0.19, "AUCUNE", 1, 5250, 4500, "CHOISIR", 0.0, 3000),
    "SACHS-2T-0.5": f("ATM", "ESS", 0.5, "AUCUNE", 2, 5000, 4000, "CHOISIR", 0.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Fichtel & Sachs")
L = []
IND = "verrière basculante (2 portes au référentiel), places en tandem ; données indicatives"
mg(L, "KR 175", "KR 175", "1", "1953-03", "1955-12", [("0.17 9", "SACHS-2T-0.17", 12)], portes=2, places=2, reservoir=13, remarques="Trois roues ; " + IND)
mg(L, "KR 200", "KR 200", "1", "1955-03", "1964-12", [("0.19 10", "SACHS-2T-0.19", 14)], portes=2, places=2, reservoir=14, remarques="Trois roues, dont KR 201 cabriolet ; " + IND)
mg(L, "Tg 500 Tiger", "Tg 500", "1", "1958-01", "1961-12", [("0.5 20", "SACHS-2T-0.5", 34)], portes=2, places=2, reservoir=33, remarques="Quatre roues, environ 450 exemplaires ; " + IND)

MOT = Motorisations("Fichtel & Sachs", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Messerschmitt": L}
MOTEURS = MOT.moteurs()
