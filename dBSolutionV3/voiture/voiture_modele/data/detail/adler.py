"""Adler (Adlerwerke, Francfort) : générations, phases, motorisations et moteurs liés.
Vis-à-vis, Standard 6, Favorit, Primus, Trumpf, Trumpf Junior, Diplomat et 2,5 Liter « Autobahn-Adler ».
Production automobile arrêtée en 1940. Moteurs à soupapes latérales Adler (et De Dion-Bouton pour le Vis-à-vis) ajoutés.
Marque ancienne : données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
SV = "NC"


def sv(l, n, rpm, nmrpm, q=4.0):
    return f("ATM", E_, l, SV, n, rpm, nmrpm, "SAE30", q, 3000)


ADLER = {"ADLER-L4-1.0": sv(1.0, 4, 3500, 2000, 3.0), "ADLER-L4-1.5": sv(1.5, 4, 3500, 2000), "ADLER-L4-1.7": sv(1.7, 4, 3800, 2000),
         "ADLER-L4-1.9": sv(1.9, 4, 3000, 1600), "ADLER-L6-2.5": sv(2.5, 6, 3400, 1800, 5.0), "ADLER-L6-3.0": sv(3.0, 6, 3400, 1800, 5.0)}
DEDION = {"DEDION-1CYL-0.5": sv(0.5, 1, 1800, 1200, 1.5)}
FAMILLES = {**ADLER, **DEDION}


def motoriste(fam):
    return "De Dion-Bouton" if fam in DEDION else "Adler"


mg = SaisieMoteurs(FAMILLES, "Adler", motoriste)
L = []
IND = "données indicatives (marque ancienne), à vérifier"

mg(L, "Vis-à-vis", "Vis-à-vis", "1", "1900-01", "1903-12", [("0.5 4", "DEDION-1CYL-0.5", 20)], portes=0, places=2, reservoir=10,
   remarques="Voiturette à moteur De Dion-Bouton ; " + IND)
mg(L, "Standard 6", "Standard 6", "1", "1927-01", "1934-12", [("2.5 L6 45", "ADLER-L6-2.5", 140)], portes=4, places=5, reservoir=60, remarques=IND)
mg(L, "Favorit", "Favorit", "1", "1929-01", "1933-12", [("1.9 35", "ADLER-L4-1.9", 110)], portes=4, places=5, reservoir=50, remarques=IND)
mg(L, "Primus", "Primus", "1", "1932-01", "1937-12", [("1.5 32", "ADLER-L4-1.5", 85)], portes=2, places=4, reservoir=40, remarques="Propulsion ; " + IND)
mg(L, "Trumpf", "Trumpf", "1", "1932-01", "1936-12", [("1.5 32", "ADLER-L4-1.5", 85), ("1.7 38", "ADLER-L4-1.7", 95, {"debut": "1933-01"})], portes=2, places=4, reservoir=40,
   remarques="Traction avant ; berline et cabriolet ; " + IND)
mg(L, "Trumpf Junior", "Trumpf Junior", "1", "1934-01", "1941-12", [("1.0 25", "ADLER-L4-1.0", 60)], portes=2, places=4, reservoir=30,
   remarques="Petite traction avant ; berline, cabriolet et roadster sport ; " + IND)
mg(L, "Diplomat", "Diplomat", "1", "1934-01", "1938-12", [("3.0 L6 60", "ADLER-L6-3.0", 170)], portes=4, places=5, reservoir=70, remarques=IND)
mg(L, "2,5 Liter Autobahn", "Typ 10", "1", "1937-01", "1940-12", [("2.5 L6 58", "ADLER-L6-2.5", 150)], portes=4, places=5, reservoir=60,
   remarques="« Autobahn-Adler » à carrosserie aérodynamique ; " + IND)

MOT = Motorisations("Adler", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Adler": L}
MOTEURS = MOT.moteurs()
