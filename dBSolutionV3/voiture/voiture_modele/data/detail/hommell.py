"""Hommell : générations, phases, motorisations (marché français) et moteurs liés.
Michel Hommell (Lohéac, puis Plélan-le-Grand) : Berlinette Échappement (1994-1999), Berlinette RS (1999-2003) et Barquette (2000-2003),
châssis tubulaire et moteur PSA XU10J4 2.0 16V (codes et couples repris de citroen.py). RS2 (prototype, 2003) non reprise.
Puissances en ch. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .citroen import FAMILLES as FAMILLES_CITROEN

FAMILLES = {"XU10J4": FAMILLES_CITROEN["XU10J4"]}
mg = SaisieMoteurs(FAMILLES, "Peugeot")
L = []
IND = "données indicatives"

mg(L, "Berlinette Échappement", "Berlinette", "1", "1994-01", "1999-12", [("2.0 16V 155", "XU10J4", 183)], portes=2, places=2, reservoir=50,
   remarques="Coupé à châssis tubulaire, moteur central avant PSA (Peugeot 306 S16) ; " + IND)
mg(L, "Berlinette RS", "Berlinette", "2", "1999-01", "2003-12", [("2.0 16V 167", "XU10J4", 193)], portes=2, places=2, reservoir=50, remarques="Moteur de la Peugeot 306 S16 / GTi-6 ; " + IND)
mg(L, "Barquette", "Barquette", "1", "2000-01", "2003-12", [("2.0 16V 167", "XU10J4", 193)], portes=0, places=2, reservoir=50, remarques="Barquette sans pare-brise intégral ; " + IND)

MOT = Motorisations("Peugeot", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Hommell": L}
MOTEURS = MOT.moteurs()
