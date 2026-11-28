"""Kaiser (Kaiser-Frazer puis Kaiser Motors, Willow Run, 1947-1955) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Special, Custom, Virginian, Deluxe, Dragon, Manhattan (dont compresseur McCulloch 1954-1955) et roadster Darrin (portes coulissantes).
Six cylindres Continental « Supersonic » et Willys F-head ajoutés ; Henry J dans henry_j.py, Frazer dans frazer.py.
Puissances brutes converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "CONTINENTAL-L6-3.7": f("ATM", "ESS", 3.7, "NC", 6, 3650, 1800, "SAE30", 5.0, 3000),
    "CONTINENTAL-L6-3.7SC": f("TURBO", "ESS", 3.7, "NC", 6, 3900, 2000, "SAE30", 5.0, 3000),
    "WILLYS-F6-2.6": f("ATM", "ESS", 2.6, "NC", 6, 4200, 2000, "SAE30", 4.5, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Continental", lambda fam: "Willys" if fam.startswith("WILLYS") else "Continental")
L = []
IND = "marché nord-américain ; données indicatives"
mg(L, "Special", "Kaiser 1947", "1", "1946-06", "1950-12", [("3.7 L6 101", "CONTINENTAL-L6-3.7", 251)], portes=4, places=6, reservoir=64, remarques="Special et Custom (112 ch) ; " + IND)
mg(L, "Custom", "Kaiser 1947", "1", "1946-06", "1950-12", [("3.7 L6 114", "CONTINENTAL-L6-3.7", 267)], portes=4, places=6, reservoir=64, remarques="Version luxe ; " + IND)
mg(L, "Virginian", "Kaiser 1947", "1", "1949-01", "1950-12", [("3.7 L6 114", "CONTINENTAL-L6-3.7", 267)], portes=4, places=6, reservoir=64, remarques="Berline hardtop à toit toile ; " + IND)
mg(L, "Deluxe", "Kaiser 1951", "1", "1949-01", "1953-12", [("3.7 L6 117", "CONTINENTAL-L6-3.7", 271)], portes=4, places=6, reservoir=64, remarques="Dont Traveler (hayon) ; " + IND)
mg(L, "Dragon", "Kaiser 1951", "1", "1951-01", "1953-12", [("3.7 L6 117", "CONTINENTAL-L6-3.7", 271)], portes=4, places=6, reservoir=64, remarques="Finition de prestige ; " + IND)
mg(L, "Manhattan", "Kaiser 1951", "1", "1951-01", "1955-12", [("3.7 L6 117", "CONTINENTAL-L6-3.7", 271, {"fin": "1953-12"}), ("3.7 L6 Compresseur 142", "CONTINENTAL-L6-3.7SC", 300, {"debut": "1954-01"})],
   portes=4, places=6, reservoir=64, remarques="Compresseur McCulloch en 1954-1955 ; " + IND)
mg(L, "Darrin", "Darrin", "1", "1954-01", "1954-12", [("2.6 L6 91", "WILLYS-F6-2.6", 184)], portes=2, places=2, reservoir=49,
   remarques="Roadster en polyester à portes coulissantes (Howard Darrin), 435 exemplaires ; " + IND)

MOT = Motorisations("Continental", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Kaiser": L}
MOTEURS = MOT.moteurs()
