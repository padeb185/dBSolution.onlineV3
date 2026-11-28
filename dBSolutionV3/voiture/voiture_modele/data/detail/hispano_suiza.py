"""Hispano-Suiza : générations, phases, motorisations (marché européen) et moteurs liés.
Historique (Barcelone, puis Bois-Colombes / Paris) : Alfonso XIII (T45), H6 / H6B, H6C « Boulogne », J12 et K6. Moderne (marque relancée
par la famille Suqué, Barcelone) : Carmen (19 ex. prévus avec la Boulogne), Carmen Boulogne et Carmen Sagrera, électriques.
Modèles espagnols utilitaires et militaires non repris. Puissances en ch. Données historiques indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

E_ = "ESS"
FAMILLES = {
    "HS-L4-3.6": f("ATM", E_, 3.6, "NC", 4, 2300, 1400, "SAE30", 7.0, 2000),
    "HS-L6-6.6": f("ATM", E_, 6.6, "NC", 6, 3000, 1600, "SAE30", 12.0, 3000),
    "HS-L6-8.0": f("ATM", E_, 8.0, "NC", 6, 3000, 1600, "SAE30", 12.0, 3000),
    "HS-V12-9.4": f("ATM", E_, 9.4, "NC", 12, 3000, 1700, "SAE30", 16.0, 3000, a="V"),
    "HS-L6-5.2": f("ATM", E_, 5.2, "NC", 6, 3400, 1800, "SAE30", 9.0, 3000),
    "HS-EV": electrique(),
}
mg = SaisieMoteurs(FAMILLES, "Hispano-Suiza")
L = []
IND = "données indicatives (marque ancienne), à vérifier"

mg(L, "Alfonso XIII", "T45", "1", "1911-01", "1914-12", [("3.6 64", "HS-L4-3.6", 200)], portes=0, places=2, reservoir=60, remarques="Voiture de sport nommée d'après le roi d'Espagne ; " + IND)
mg(L, "H6B", "H6 / H6B", "1", "1919-10", "1933-12", [("6.6 L6 135", "HS-L6-6.6", 400)], portes=4, places=5, reservoir=105,
   remarques="Six cylindres en aluminium dérivé du moteur d'aviation, servofrein ; " + IND)
mg(L, "H6C", "H6C Boulogne", "1", "1924-01", "1934-12", [("8.0 L6 160", "HS-L6-8.0", 470)], portes=2, places=4, reservoir=105, remarques="Version 8 litres, victoires à la Coupe Boillot (Boulogne) ; " + IND)
mg(L, "J12", "J12", "1", "1931-10", "1938-12", [("9.4 V12 220", "HS-V12-9.4", 550)], portes=4, places=5, reservoir=135, remarques="V12 de 9,4 l, environ 120 exemplaires ; " + IND)
mg(L, "K6", "K6", "1", "1934-01", "1937-12", [("5.2 L6 125", "HS-L6-5.2", 330)], portes=4, places=5, reservoir=100, remarques=IND)
mg(L, "Carmen", "Carmen", "1", "2020-01", "2021-12", [("Électrique 1019", "HS-EV", 1600)], portes=2, places=2, reservoir=0, batterie=80,
   remarques="GT électrique à deux moteurs, propulsion ; série limitée")
mg(L, "Carmen Boulogne", "Carmen", "B", "2022-01", None, [("Électrique 1114", "HS-EV", 1600)], portes=2, places=2, reservoir=0, batterie=80,
   remarques="Version allégée à quatre moteurs, 5 exemplaires")
mg(L, "Carmen Sagrera", "Carmen", "S", "2024-06", None, [("Électrique 1115", "HS-EV", 1160)], portes=2, places=2, reservoir=0, batterie=103,
   remarques="Quatre moteurs de 205 kW, batterie de 103 kWh de deuxième génération ; 120e anniversaire de la marque")

MOT = Motorisations("Hispano-Suiza", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Hispano-Suiza": L}
MOTEURS = MOT.moteurs()
