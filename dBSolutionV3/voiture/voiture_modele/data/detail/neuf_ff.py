"""9ff (Dortmund) : préparateur de Porsche ; modèles GT9 (base 997 GT3, moteur central) et programme GTurbo.
Fichier nommé neuf_ff.py car un nom de module Python ne peut pas commencer par un chiffre.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom.
Petites séries : dates, couples et réservoirs indicatifs."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "9ff-3.6TT": f("TURBO", E_, 3.6, "CHAINE", 6, 7500, 5000, "10W60", 10.0, 10000, a="PLAT"),
    "9ff-3.8TT": f("TURBO", E_, 3.8, "CHAINE", 6, 7500, 5000, "10W60", 10.0, 10000, a="PLAT"),
    "9ff-4.0TT": f("TURBO", E_, 4.0, "CHAINE", 6, 7850, 5970, "10W60", 10.0, 10000, a="PLAT"),
    "9ff-4.2TT": f("TURBO", E_, 4.2, "CHAINE", 6, 7950, 6000, "10W60", 10.0, 10000, a="PLAT"),
}

mg = SaisieMoteurs(FAMILLES, "9ff")
L = []

mg(L, "GT9", "997", "1", "2007-08", "2008-12",
   [("GT9 987", "9ff-4.0TT", 964), ("GT9 750", "9ff-4.0TT", 800, {"remarques": "Version d'entrée de gamme, boîte Tiptronic possible"})],
   portes=2, places=2, reservoir=90, remarques="Coupé à moteur central sur base Porsche 997 GT3 (série limitée)")
mg(L, "GT9", "997", "R", "2009-12", "2011-12", [("GT9-R 1120", "9ff-4.0TT", 1050)], portes=2, places=2, reservoir=90,
   remarques="Version définitive, 20 exemplaires prévus")
mg(L, "GT9", "997", "CS", "2011-01", "2012-12", [("GT9-CS 748", "9ff-3.6TT", 850)], portes=2, places=2, reservoir=90,
   remarques="Version allégée (1 240 kg)")
mg(L, "GT9", "997", "Vmax", "2012-12", "2013-12", [("GT9 Vmax 1400", "9ff-4.2TT", 1160)], portes=2, places=2,
   reservoir=90, remarques="Version record (437 km/h annoncés)")
mg(L, "GTurbo", "997 GT3", "1", "2010-01", None, [("GTurbo 1000", "9ff-3.8TT", 1000)], portes=2, places=2, reservoir=64,
   remarques="Programme de transformation biturbo des Porsche GT3 / GT3 RS ; puissance selon le niveau (jusqu'à 1 000 ch)")

MOT = Motorisations("9ff", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"9ff": L}
MOTEURS = MOT.moteurs()
