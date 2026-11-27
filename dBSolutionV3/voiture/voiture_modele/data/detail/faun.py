"""Faun : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur allemand de véhicules lourds (Nuremberg / Lauf) : L 900 (camion lourd, 1936-1944), F 610 (tracteur lourd, 1950-1956)
et SLT 50 Elefant (tracteur porte-char de la Bundeswehr, 1976-1980). Diesels Deutz et MTU. Puissances en ch DIN.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

D = "DSL"
DEUTZ = {
    "DEUTZ-L6-12.0": f("ATM", D, 12.0, "NC", 6, 2000, 1200, "15W40", 24.0, 10000),
    "DEUTZ-V8-13.0": f("ATM", D, 13.0, "NC", 8, 2100, 1300, "15W40", 26.0, 10000, a="V"),
}
MTU = {"MTU-V8-29.9": f("TURBO", D, 29.9, "NC", 8, 2100, 1500, "15W40", 60.0, 10000, a="V")}
FAMILLES = {**DEUTZ, **MTU}
mg = SaisieMoteurs(FAMILLES, "Faun", lambda fam: "MTU" if fam in MTU else "Deutz")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "L 900", "L 900", "1", "1936-01", "1944-12", [("12.0 Diesel 150", "DEUTZ-L6-12.0", 600)], portes=2, places=2, reservoir=200, remarques="Camion lourd ; " + IND)
mg(L, "F 610", "F 610", "1", "1950-01", "1956-12", [("13.0 V8 Diesel 180", "DEUTZ-V8-13.0", 700)], portes=2, places=2, reservoir=300, remarques="Tracteur lourd ; " + IND)
mg(L, "SLT 50 Elefant", "SLT 50", "1", "1976-01", "1980-12", [("29.9 V8 Turbo Diesel 730", "MTU-V8-29.9", 2700)], portes=4, places=4, reservoir=800,
   remarques="Tracteur porte-char 8x8 de la Bundeswehr ; " + IND)

MOT = Motorisations("Faun", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Faun": L}
MOTEURS = MOT.moteurs()
