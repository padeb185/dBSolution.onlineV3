"""Mack Trucks (Allentown, Pennsylvanie ; groupe Volvo depuis 2000) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
AC « Bulldog », B-Series, R-Series, Superliner, Granite, Pinnacle, LR (benne à ordures) et Anthem. Moteurs Mack (Thermodyne, Maxidyne,
E9, MP7, MP8) ajoutés. Puissances hp converties en ch (× 1,014). Poids lourds aux configurations multiples : une motorisation
représentative, données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "MACK-AC-7.0": f("ATM", "ESS", 7.0, "NC", 4, 1400, 900, "SAE30", 10.0, 3000),
    "MACK-END673-11.0": f("ATM", "DSL", 11.0, "NC", 6, 2100, 1300, "15W40", 28.0, 15000),
    "MACK-ENDT676-11.0": f("TURBO", "DSL", 11.0, "NC", 6, 2100, 1300, "15W40", 28.0, 20000),
    "MACK-E9-16.4": f("TURBO", "DSL", 16.4, "NC", 8, 2100, 1300, "15W40", 40.0, 25000, a="V"),
    "MACK-MP7-10.8": f("TURBO", "DSL", 10.8, "NC", 6, 1800, 1100, "10W30", 36.0, 40000),
    "MACK-MP8-12.8": f("TURBO", "DSL", 12.8, "NC", 6, 1800, 1100, "10W30", 38.0, 50000),
}
mg = SaisieMoteurs(FAMILLES, "Mack")
L = []
IND = "poids lourd, marché nord-américain ; motorisations multiples, données indicatives"
mg(L, "AC Bulldog", "AC", "1", "1916-01", "1938-12", [("7.0 75", "MACK-AC-7.0", 400)], portes=2, places=2, reservoir=150, remarques="Capot « bouledogue », transmission par chaînes ; " + IND)
mg(L, "B-Series", "B", "1", "1953-01", "1966-12", [("Diesel 11.0 172", "MACK-END673-11.0", 750)], portes=2, places=2, reservoir=300, remarques=IND)
mg(L, "R-Series", "R", "1", "1965-01", "2005-12", [("Diesel 11.0 Turbo 289", "MACK-ENDT676-11.0", 1150)], portes=2, places=2, reservoir=380, remarques=IND)
mg(L, "Superliner", "Superliner", "1", "1977-01", "1993-12", [("Diesel V8 16.4 Turbo 456", "MACK-E9-16.4", 2100)], portes=2, places=2, reservoir=570, remarques="Tracteur à V8 E9 ; " + IND)
mg(L, "Granite", "Granite", "1", "2001-01", None, [("MP7 10.8 Turbo 360", "MACK-MP7-10.8", 1760)], portes=2, places=2, reservoir=380, remarques="Camion de chantier ; " + IND)
mg(L, "Pinnacle", "Pinnacle", "1", "2006-01", None, [("MP8 12.8 Turbo 512", "MACK-MP8-12.8", 2510)], portes=2, places=2, reservoir=570, remarques="Tracteur routier ; " + IND)
mg(L, "LR", "LR", "1", "2015-01", None, [("MP7 10.8 Turbo 360", "MACK-MP7-10.8", 1760)], portes=2, places=3, reservoir=280, remarques="Benne à ordures à cabine basse (LR Electric en option) ; " + IND)
mg(L, "Anthem", "Anthem", "1", "2018-01", None, [("MP8 12.8 Turbo 512", "MACK-MP8-12.8", 2510)], portes=2, places=2, reservoir=570, remarques="Tracteur routier long-courrier ; " + IND)

MOT = Motorisations("Mack", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Mack": L}
MOTEURS = MOT.moteurs()
