"""Melkus (Dresde) : générations, phases, motorisations (marché européen) et moteurs liés.
RS 1000 (RDA, 1969-1979, trois cylindres deux temps Wartburg, portes papillon) et RS 2000 (2009-2012, quatre cylindres 2.0 TFSI Audi).
Deux-temps : distribution « aucune », huile « à choisir » (mélange). Puissances en ch. Petites séries, données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "WARTBURG-2T-1.0": f("ATM", "ESS", 1.0, "AUCUNE", 3, 4500, 3000, "CHOISIR", 0.0, 5000),
    "AUDI-2.0TFSI": f("TURBO", "ESS", 2.0, "CHAINE", 4, 6000, 2500, "5W30", 4.6, 15000),
}
mg = SaisieMoteurs(FAMILLES, "Wartburg", lambda fam: "Audi" if fam.startswith("AUDI") else "Wartburg")
L = []
IND = "petite série ; données indicatives"
mg(L, "RS 1000", "RS 1000", "1", "1969-01", "1979-12", [("1.0 70", "WARTBURG-2T-1.0", 100)], portes=2, places=2, reservoir=40, remarques="Coupé à portes papillon, 101 exemplaires ; " + IND)
mg(L, "RS 2000", "RS 2000", "1", "2009-01", "2012-12", [("2.0 TFSI 270", "AUDI-2.0TFSI", 350), ("GT 2.0 TFSI 300", "AUDI-2.0TFSI", 380, {"debut": "2011-01"})], portes=2, places=2, reservoir=50,
   remarques="Coupé à moteur central, portes papillon ; " + IND)

MOT = Motorisations("Wartburg", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Melkus": L}
MOTEURS = MOT.moteurs()
