"""Frazer : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Marque haut de gamme de Kaiser-Frazer (Willow Run, 1947-1951) : Standard, Manhattan (berline, puis cabriolet 4 portes en 1949-1951)
et Vagabond (berline à hayon, 1949-1951). Six cylindres Continental 3.7 à soupapes latérales (famille reprise d'auburn.py).
Puissances brutes converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .auburn import FAMILLES as FAMILLES_AUBURN

FAMILLES = {"CONTINENTAL-L6-3.7": FAMILLES_AUBURN["CONTINENTAL-L6-3.7"]}
mg = SaisieMoteurs(FAMILLES, "Continental", lambda fam: "Continental")
L = []
NA = "marché nord-américain ; données indicatives"
MOT6 = [("3.7 L6 101", "CONTINENTAL-L6-3.7", 251, {"fin": "1948-12"}), ("Supersonic 3.7 L6 114", "CONTINENTAL-L6-3.7", 267, {"debut": "1949-01"})]

mg(L, "Standard", "Frazer", "1", "1946-06", "1951-12", MOT6, portes=4, places=6, reservoir=68, remarques="Berline ; " + NA)
mg(L, "Manhattan", "Frazer", "2", "1946-06", "1951-12", MOT6, portes=4, places=6, reservoir=68, remarques="Berline de luxe, cabriolet 4 portes à partir de 1949 ; " + NA)
mg(L, "Vagabond", "Frazer", "3", "1949-01", "1951-12", [("Supersonic 3.7 L6 114", "CONTINENTAL-L6-3.7", 267)], portes=4, places=6, reservoir=68,
   remarques="Berline utilitaire à hayon ; " + NA)

MOT = Motorisations("Frazer", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Frazer": L}
MOTEURS = MOT.moteurs()
