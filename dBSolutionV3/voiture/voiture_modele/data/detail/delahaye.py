"""Delahaye : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur parisien : Type 0 (1894-1898), Type 135 (1935-1954), Type 145 (course V12, 1937-1938), Type 148 (1936-1953), Type 165
(V12, 1938-1939), Type 175 (1948-1951), Type 235 (1951-1954) et VLR (tout-terrain militaire, 1951-1955). Puissances en ch.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "DELAHAYE-1.4": f("ATM", E_, 1.4, "NC", 1, 900, 600, "SAE30", 2.0, 1000),
    "DELAHAYE-L6-3.6": f("ATM", E_, 3.6, "NC", 6, 3800, 2200, "SAE30", 6.0, 3000),
    "DELAHAYE-L6-3.2": f("ATM", E_, 3.2, "NC", 6, 3800, 2200, "SAE30", 6.0, 3000),
    "DELAHAYE-V12-4.5": f("ATM", E_, 4.5, "NC", 12, 5000, 3000, "SAE30", 10.0, 2000, a="V"),
    "DELAHAYE-L6-4.5": f("ATM", E_, 4.5, "NC", 6, 3800, 2400, "SAE30", 7.0, 3000),
    "DELAHAYE-2.0": f("ATM", E_, 2.0, "NC", 4, 3800, 2200, "SAE30", 4.5, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Delahaye", lambda fam: "Delahaye")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Type 0", "0", "1", "1894-01", "1898-12", [("1.4 5", "DELAHAYE-1.4", 45)], portes=0, places=2, reservoir=15, remarques="Voiturette monocylindre ; " + IND)
mg(L, "Type 135", "135", "1", "1935-01", "1954-12",
   [("3.2 L6 95", "DELAHAYE-L6-3.2", 220, {"fin": "1938-12"}), ("M 3.6 L6 115", "DELAHAYE-L6-3.6", 250), ("MS 3.6 L6 130", "DELAHAYE-L6-3.6", 260)],
   portes=2, places=4, reservoir=90, remarques="Coupés et cabriolets carrossés (Figoni & Falaschi, Chapron, Saoutchik…), 135 M et MS ; " + IND)
mg(L, "Type 145", "145", "1", "1937-01", "1938-12", [("4.5 V12 245", "DELAHAYE-V12-4.5", 430)], portes=0, places=2, reservoir=120,
   remarques="Voiture de course (Prix du Million 1937) ; " + IND)
mg(L, "Type 148", "148", "1", "1936-01", "1953-12", [("3.6 L6 95", "DELAHAYE-L6-3.6", 230)], portes=4, places=6, reservoir=90, remarques="Berline et limousine (148 L) ; " + IND)
mg(L, "Type 165", "165", "1", "1938-01", "1939-12", [("4.5 V12 175", "DELAHAYE-V12-4.5", 340)], portes=2, places=2, reservoir=120,
   remarques="Cabriolet V12 de route (Figoni & Falaschi) ; " + IND)
mg(L, "Type 175", "175", "1", "1948-01", "1951-12", [("4.5 L6 140", "DELAHAYE-L6-4.5", 300)], portes=2, places=4, reservoir=100,
   remarques="Cabriolets et coupés (175, 178, 180) ; " + IND)
mg(L, "Type 235", "235", "1", "1951-01", "1954-12", [("3.6 L6 152", "DELAHAYE-L6-3.6", 270)], portes=2, places=4, reservoir=90, remarques="Coupé et cabriolet ; " + IND)
mg(L, "VLR", "VLR", "1", "1951-01", "1955-12", [("2.0 63", "DELAHAYE-2.0", 125)], portes=0, places=4, reservoir=60,
   remarques="Véhicule léger de reconnaissance 4x4 (armée française) ; " + IND)

MOT = Motorisations("Delahaye", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Delahaye": L}
MOTEURS = MOT.moteurs()
