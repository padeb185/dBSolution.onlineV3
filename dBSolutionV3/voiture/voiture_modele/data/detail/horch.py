"""Horch : générations, phases, motorisations (marché européen) et moteurs liés.
August Horch (Cologne, puis Zwickau, 1899) ; marque de luxe d'Auto Union (1932) : 10-16 PS, 8 (Typ 303), 350, 450, 670 V12, 830 (V8),
853 (huit cylindres en ligne) et 901 (tout-terrain militaire) ; Horch P240 « Sachsenring » (RDA, 1956-1959). Puissances en ch DIN.
Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "HORCH-2C-2.0": f("ATM", E_, 2.0, "NC", 2, 1400, 900, "SAE30", 2.5, 1000),
    "HORCH-L8-3.1": f("ATM", E_, 3.1, "NC", 8, 3200, 1600, "SAE30", 6.0, 3000),
    "HORCH-L8-4.0": f("ATM", E_, 4.0, "NC", 8, 3200, 1600, "SAE30", 7.0, 3000),
    "HORCH-L8-4.5": f("ATM", E_, 4.5, "NC", 8, 3200, 1600, "SAE30", 7.0, 3000),
    "HORCH-V12-6.0": f("ATM", E_, 6.0, "NC", 12, 3200, 1600, "SAE30", 9.0, 3000, a="V"),
    "HORCH-V8-3.0": f("ATM", E_, 3.0, "NC", 8, 3400, 1800, "SAE30", 6.0, 3000, a="V"),
    "HORCH-V8-3.5": f("ATM", E_, 3.5, "NC", 8, 3600, 1800, "SAE30", 6.0, 3000, a="V"),
    "HORCH-V8-3.8": f("ATM", E_, 3.8, "NC", 8, 3600, 1800, "SAE30", 6.0, 3000, a="V"),
    "HORCH-L8-4.9": f("ATM", E_, 4.9, "NC", 8, 3600, 2000, "SAE30", 8.0, 3000),
    "HORCH-L6-2.4": f("ATM", E_, 2.4, "NC", 6, 4000, 2500, "SAE30", 4.5, 5000),
}
mg = SaisieMoteurs(FAMILLES, "Horch")
L = []
IND = "données indicatives (marque ancienne), à vérifier"

mg(L, "10-16 PS", "10-16 PS", "1", "1902-01", "1904-12", [("2.0 16", "HORCH-2C-2.0", 60)], portes=0, places=4, reservoir=30, remarques="Tonneau bicylindre ; " + IND)
mg(L, "8 Typ 303", "Typ 303", "1", "1926-01", "1927-12", [("3.1 L8 60", "HORCH-L8-3.1", 170)], portes=4, places=5, reservoir=70,
   remarques="Première huit cylindres allemande de série (Paul Daimler) ; " + IND)
mg(L, "350", "350", "1", "1928-01", "1930-12", [("4.0 L8 80", "HORCH-L8-4.0", 220)], portes=4, places=5, reservoir=80, remarques=IND)
mg(L, "450", "450", "1", "1930-01", "1931-12", [("4.5 L8 90", "HORCH-L8-4.5", 250)], portes=4, places=5, reservoir=80, remarques=IND)
mg(L, "670 V12", "670", "1", "1931-01", "1934-12", [("6.0 V12 120", "HORCH-V12-6.0", 330)], portes=2, places=4, reservoir=100, remarques="Cabriolet et limousine 600 / 670 ; " + IND)
mg(L, "830", "830", "1", "1933-01", "1940-12", [("3.0 V8 62", "HORCH-V8-3.0", 170, {"fin": "1934-12"}), ("3.5 V8 75", "HORCH-V8-3.5", 200, {"debut": "1935-01"})],
   portes=4, places=5, reservoir=75, remarques="830, 830 B et 830 BL (V8 3,0 à 3,8 l) ; " + IND)
mg(L, "853", "853", "1", "1935-01", "1939-12", [("4.9 L8 100", "HORCH-L8-4.9", 280), ("853 A 4.9 L8 120", "HORCH-L8-4.9", 310, {"debut": "1937-01"})], portes=2, places=2, reservoir=90,
   remarques="Cabriolet sport et Spezial Roadster ; " + IND)
mg(L, "901", "901", "1", "1937-01", "1943-12", [("3.5 V8 80", "HORCH-V8-3.5", 210, {"fin": "1939-12"}), ("3.8 V8 90", "HORCH-V8-3.8", 230, {"debut": "1940-01"})],
   portes=4, places=8, reservoir=120, remarques="Véhicule militaire tout-terrain de la Wehrmacht ; " + IND)
mg(L, "P240", "Sachsenring", "1", "1956-01", "1959-12", [("2.4 L6 80", "HORCH-L6-2.4", 158)], portes=4, places=5, reservoir=60,
   remarques="Construite à Zwickau (RDA), vendue Horch puis Sachsenring P240 ; " + IND)

MOT = Motorisations("Horch", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Horch": L}
MOTEURS = MOT.moteurs()
