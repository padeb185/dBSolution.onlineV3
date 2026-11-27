"""Bellier : générations, phases, motorisations (marché européen) et moteurs liés.
Voitures sans permis françaises (quadricycles légers, 45 km/h) : Opale, Docker et Divane.
Bicylindre diesel Lombardini bridé. Données indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {"LOMBARDINI-LDW502": f("ATM", "DSL", 0.5, "COURROIE", 2, 3200, 2400, "10W40", 1.6, 5000)}
mg = SaisieMoteurs(FAMILLES, "Lombardini", lambda fam: "Lombardini")
L = []
VSP = "Voiture sans permis (quadricycle léger, 45 km/h) ; données indicatives, à vérifier"

mg(L, "Opale", "Opale", "1", "2001-01", "2007-12", [("Diesel 0.5 5", "LOMBARDINI-LDW502", 20)], portes=2, places=2, reservoir=16, remarques=VSP)
mg(L, "Docker", "Docker", "1", "2005-01", "2012-12", [("Diesel 0.5 5", "LOMBARDINI-LDW502", 20)], portes=2, places=2, reservoir=16, remarques="Style tout-terrain ; " + VSP)
mg(L, "Divane", "Divane", "1", "2009-01", "2014-12", [("Diesel 0.5 5", "LOMBARDINI-LDW502", 20)], portes=2, places=2, reservoir=16, remarques=VSP)

MOT = Motorisations("Bellier", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Bellier": L}
MOTEURS = MOT.moteurs()
