"""Gemballa : générations, phases, motorisations (marché européen) et moteurs liés.
Préparateur et constructeur de Leonberg sur base Porsche : Avalanche (911 Turbo 930), Mirage GT (Carrera GT), Mistrale (Panamera Turbo)
et Marsien (911 Turbo S 992, tout-terrain). Moteurs Porsche retravaillés au motoriste « Gemballa ». Données indicatives (petites séries).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "GEMBALLA-930-3.3T": f("TURBO", E_, 3.3, "CHAINE", 6, 5500, 4000, "15W50", 13.0, 10000, a="PLAT"),
    "GEMBALLA-V10-5.7": f("ATM", E_, 5.7, "CHAINE", 10, 8000, 5750, "0W40", 10.0, 10000, a="V"),
    "GEMBALLA-V8-4.8TT": f("TURBO", E_, 4.8, "CHAINE", 8, 6000, 2500, "0W40", 9.0, 15000, a="V"),
    "GEMBALLA-992-3.7TT": f("TURBO", E_, 3.7, "CHAINE", 6, 6750, 2500, "0W40", 8.5, 15000, a="PLAT"),
}
mg = SaisieMoteurs(FAMILLES, "Gemballa", lambda fam: "Gemballa")
L = []
IND = "données indicatives (petite série)"

mg(L, "Avalanche", "930", "1", "1985-01", "1990-12", [("3.3 Turbo 330", "GEMBALLA-930-3.3T", 480)], portes=2, places=4, reservoir=80,
   remarques="Coupé large sur base Porsche 911 Turbo (930) ; " + IND)
mg(L, "Mirage GT", "980", "1", "2007-01", "2009-12", [("5.7 V10 670", "GEMBALLA-V10-5.7", 630)], portes=2, places=2, reservoir=92,
   remarques="Sur base Porsche Carrera GT, 25 exemplaires ; " + IND)
mg(L, "Mistrale", "970", "1", "2010-01", "2011-12", [("4.8 V8 Biturbo 700", "GEMBALLA-V8-4.8TT", 900)], portes=4, places=4, reservoir=100,
   remarques="Sur base Porsche Panamera Turbo ; " + IND)
mg(L, "Marsien", "992", "1", "2023-01", None, [("3.7 Biturbo 750", "GEMBALLA-992-3.7TT", 920)], portes=2, places=2, reservoir=67,
   remarques="911 Turbo S tout-terrain, 40 exemplaires ; " + IND)

MOT = Motorisations("Gemballa", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Gemballa": L}
MOTEURS = MOT.moteurs()
