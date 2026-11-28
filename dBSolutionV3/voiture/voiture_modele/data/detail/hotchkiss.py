"""Hotchkiss (Saint-Denis) : générations, phases, motorisations (marché français) et moteurs liés.
AM 2, AM 80, 411, 686 (dont Grand Sport, victoires au Rallye Monte-Carlo), Anjou, Grégoire (flat-4 Jean-Albert Grégoire) et jeep
M201 (licence Willys MB, moteur Go Devil repris de jeep.py). Fusion avec Delahaye (1954), fin des voitures particulières en 1954.
Puissances en ch. Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .jeep import FAMILLES as FAMILLES_JEEP

E_ = "ESS"
FAMILLES = {
    "HOTCHKISS-L4-2.4": f("ATM", E_, 2.4, "NC", 4, 3200, 1800, "SAE30", 5.0, 3000),
    "HOTCHKISS-L6-3.0": f("ATM", E_, 3.0, "NC", 6, 3400, 1800, "SAE30", 6.0, 3000),
    "HOTCHKISS-L4-2.3": f("ATM", E_, 2.3, "NC", 4, 3800, 2000, "SAE30", 5.0, 3000),
    "HOTCHKISS-L6-3.5": f("ATM", E_, 3.5, "NC", 6, 3800, 2000, "SAE30", 6.0, 3000),
    "GREGOIRE-B4-2.2": f("ATM", E_, 2.2, "NC", 4, 4000, 2600, "SAE30", 4.0, 3000, a="PLAT"),
    "GO-DEVIL-2.2": FAMILLES_JEEP["GO-DEVIL-2.2"],
}
mg = SaisieMoteurs(FAMILLES, "Hotchkiss", lambda fam: "Jeep" if fam == "GO-DEVIL-2.2" else "Hotchkiss")
L = []
IND = "données indicatives (marque ancienne), à vérifier"

mg(L, "AM 2", "AM 2", "1", "1926-01", "1929-12", [("2.4 48", "HOTCHKISS-L4-2.4", 130)], portes=4, places=5, reservoir=60, remarques=IND)
mg(L, "AM 80", "AM 80", "1", "1929-01", "1933-12", [("3.0 L6 70", "HOTCHKISS-L6-3.0", 180)], portes=4, places=5, reservoir=70, remarques=IND)
mg(L, "411", "411", "1", "1933-01", "1934-12", [("2.3 55", "HOTCHKISS-L4-2.3", 140)], portes=4, places=5, reservoir=60, remarques=IND)
mg(L, "686", "686", "1", "1936-01", "1954-12", [("3.5 L6 100", "HOTCHKISS-L6-3.5", 220)], portes=4, places=5, reservoir=75,
   remarques="Berline, coupé et cabriolet ; production interrompue pendant la guerre ; " + IND)
mg(L, "Grand Sport", "686 GS", "1", "1935-01", "1940-12", [("3.5 L6 115", "HOTCHKISS-L6-3.5", 230)], portes=2, places=4, reservoir=75,
   remarques="Version sportive de la 686, victoires au Rallye Monte-Carlo ; " + IND)
mg(L, "Anjou", "Anjou", "1", "1950-01", "1954-12", [("1350 2.3 70", "HOTCHKISS-L4-2.3", 150), ("2050 3.5 L6 100", "HOTCHKISS-L6-3.5", 220)], portes=4, places=5, reservoir=75,
   remarques="Anjou 1350 (quatre cylindres) et 2050 (six cylindres) ; " + IND)
mg(L, "Grégoire", "Grégoire", "1", "1951-01", "1954-12", [("2.2 Flat-4 75", "GREGOIRE-B4-2.2", 155)], portes=4, places=5, reservoir=60,
   remarques="Traction avant à caisse en aluminium (J.-A. Grégoire), environ 250 exemplaires ; " + IND)
mg(L, "M201", "M201", "1", "1955-01", "1966-12", [("Go Devil 2.2 61", "GO-DEVIL-2.2", 142)], portes=0, places=4, reservoir=57,
   remarques="Jeep Willys MB sous licence pour l'armée française ; " + IND)

MOT = Motorisations("Hotchkiss", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Hotchkiss": L}
MOTEURS = MOT.moteurs()
