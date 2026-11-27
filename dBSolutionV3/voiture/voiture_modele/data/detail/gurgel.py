"""Gurgel : générations, phases, motorisations (marché brésilien) et moteurs liés.
Constructeur brésilien (Rio Claro, 1969-1996) : X-12 et X-15 (tout-terrain en plastique sur mécanique VW à air), Carajás (moteur VW AP),
Tocantins, BR-800 et Supermini (bicylindre maison Enertron). Puissances en ch. Données indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .volkswagen_classiques import FAMILLES as FAMILLES_VW

VW = {"BOXER-1.6": FAMILLES_VW["BOXER-1.6"], "VW-AP-1.8": f("ATM", "ESS", 1.8, "COURROIE", 4, 5200, 3000, "15W40", 4.0, 10000)}
GURGEL = {"GURGEL-ENERTRON-0.8": f("ATM", "ESS", 0.8, "COURROIE", 2, 5500, 2500, "15W40", 2.5, 7500, a="PLAT")}
FAMILLES = {**VW, **GURGEL}
mg = SaisieMoteurs(FAMILLES, "Gurgel", lambda fam: "Volkswagen" if fam in VW else "Gurgel")
L = []
IND = "marché brésilien ; données indicatives, à vérifier"

mg(L, "X-12", "X-12", "1", "1975-01", "1988-12", [("1.6 50", "BOXER-1.6", 106)], portes=2, places=4, reservoir=45, remarques="Tout-terrain léger, mécanique Coccinelle ; " + IND)
mg(L, "X-15", "X-15", "1", "1979-01", "1990-12", [("1.6 50", "BOXER-1.6", 106)], portes=2, places=4, reservoir=45, remarques="Utilitaire tout-terrain ; " + IND)
mg(L, "Tocantins", "Tocantins", "1", "1989-01", "1993-12", [("1.6 50", "BOXER-1.6", 106)], portes=2, places=4, reservoir=45, remarques="Successeur du X-12 ; " + IND)
mg(L, "Carajás", "Carajás", "1", "1984-01", "1989-12", [("1.8 90", "VW-AP-1.8", 145)], portes=4, places=5, reservoir=60, remarques="Tout-terrain à moteur VW AP avant ; " + IND)
mg(L, "BR-800", "BR-800", "1", "1988-01", "1991-12", [("0.8 33", "GURGEL-ENERTRON-0.8", 58)], portes=3, places=4, reservoir=30,
   remarques="Citadine 100 % brésilienne, bicylindre à plat Enertron ; " + IND)
mg(L, "Supermini", "Supermini", "1", "1992-01", "1994-12", [("0.8 36", "GURGEL-ENERTRON-0.8", 62)], portes=3, places=4, reservoir=32, remarques="Évolution de la BR-800 ; " + IND)

MOT = Motorisations("Gurgel", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Gurgel": L}
MOTEURS = MOT.moteurs()
