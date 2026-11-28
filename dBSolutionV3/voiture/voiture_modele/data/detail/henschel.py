"""Henschel (Henschel & Sohn, Kassel) : générations, phases, motorisations (marché européen) et moteurs liés.
Camions : Typ 33 (6x4 militaire et civil, 1934-1943 ; D1 à essence, G1 diesel), HS 140 (camion à capot, 1951-1961) et HS 3-14
(cabine avancée, 1961-1970). Activité camions reprise par Rheinstahl puis intégrée à Daimler-Benz (1969-1974). Autobus et
locomotives non repris. Puissances en ch DIN. Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "HENSCHEL-6-10.9": f("ATM", "ESS", 10.9, "NC", 6, 2400, 1400, "SAE30", 18.0, 5000),
    "HENSCHEL-6D-10.7": f("ATM", "DSL", 10.7, "NC", 6, 2000, 1300, "SAE30", 18.0, 5000),
    "HENSCHEL-6D-11.0": f("ATM", "DSL", 11.0, "NC", 6, 2000, 1300, "15W40", 20.0, 10000),
}
mg = SaisieMoteurs(FAMILLES, "Henschel")
L = []
IND = "camion ; désignations et données indicatives (marque ancienne), à vérifier"

mg(L, "33", "Typ 33", "1", "1934-01", "1943-12", [("D1 10.9 L6 100", "HENSCHEL-6-10.9", 450), ("G1 Diesel 10.7 L6 100", "HENSCHEL-6D-10.7", 480)], portes=2, places=2, reservoir=110,
   remarques="Six roues 6x4, environ 11 000 exemplaires (D1 essence, G1 diesel) ; " + IND)
mg(L, "HS 140", "HS 140", "1", "1951-01", "1961-12", [("Diesel 11.0 L6 140", "HENSCHEL-6D-11.0", 600)], portes=2, places=2, reservoir=200,
   remarques="Porteur et tracteur à capot, vaisseau amiral de l'après-guerre ; " + IND)
mg(L, "HS 3-14", "HS 3-14", "1", "1961-01", "1970-12", [("Diesel 11.0 L6 150", "HENSCHEL-6D-11.0", 620)], portes=2, places=2, reservoir=250,
   remarques="Cabine avancée « cubique » ; " + IND)

MOT = Motorisations("Henschel", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Henschel": L}
MOTEURS = MOT.moteurs()
