"""Microcar (Boufféré, groupe Bénéteau puis Ligier Group depuis 2008) : générations, phases, motorisations (marché européen) et moteurs liés.
Voitures sans permis (catégorie L6e, 45 km/h, 4 kW) : Virgo, MC1 / MC2, M.Go et Due. Moteur Lombardini repris de ligier.py (même code).
Puissances en ch. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .ligier import FAMILLES as FAMILLES_LIGIER

FAMILLES = {
    "LOMBARDINI-0.5": FAMILLES_LIGIER["LOMBARDINI-0.5"],
}
mg = SaisieMoteurs(FAMILLES, "Lombardini")
L = []
IND = "voiture sans permis ; données indicatives"
mg(L, "Virgo", "Virgo", "1", "1995-01", "2004-12", [("Diesel 0.5 7", "LOMBARDINI-0.5", 23)], portes=2, places=2, reservoir=16, remarques=IND)
mg(L, "MC1", "MC", "1", "2003-01", "2009-12", [("Diesel 0.5 7", "LOMBARDINI-0.5", 23)], portes=2, places=2, reservoir=16, remarques="MC1 et MC2 ; " + IND)
mg(L, "M.Go", "M.Go", "1", "2008-01", "2014-12", [("Diesel 0.5 7", "LOMBARDINI-0.5", 23)], portes=2, places=2, reservoir=20, remarques=IND)
mg(L, "Due", "Due", "1", "2010-01", "2019-12", [("Diesel 0.5 7", "LOMBARDINI-0.5", 23)], portes=2, places=2, reservoir=20, remarques="Dont Due First et Dué Initial ; " + IND)

MOT = Motorisations("Lombardini", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Microcar": L}
MOTEURS = MOT.moteurs()
