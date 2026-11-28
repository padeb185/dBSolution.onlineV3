"""Hanomag : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur de Hanovre (voitures de 1925 à 1941) : 2/10 PS « Kommissbrot », 3/16 PS, Garant (ex-1,1 Liter), Kurier, Rekord (dont la
Rekord Diesel, l'une des deux premières voitures diesel de série avec la Mercedes 260 D), Sturm et 1,3 Liter. Après-guerre, Hanomag ne
produit plus de voitures (prototype Partner non produit) ; utilitaires Kurier / F 20 non repris. Puissances en ch DIN.
Données indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"

FAMILLES = {
    "HANOMAG-1C-0.5": f("ATM", E_, 0.5, "NC", 1, 3500, 2000, "SAE30", 1.5, 2000),
    "HANOMAG-L4-0.75": f("ATM", E_, 0.75, "NC", 4, 3500, 2200, "SAE30", 2.5, 3000),
    "HANOMAG-L4-1.1": f("ATM", E_, 1.1, "NC", 4, 3600, 2200, "SAE30", 3.0, 3000),
    "HANOMAG-L4-1.3": f("ATM", E_, 1.3, "NC", 4, 3800, 2400, "SAE30", 3.5, 3000),
    "HANOMAG-L4-1.5": f("ATM", E_, 1.5, "NC", 4, 3500, 2200, "SAE30", 4.0, 3000),
    "HANOMAG-D19-1.9": f("ATM", "DSL", 1.9, "NC", 4, 3000, 1800, "SAE30", 5.0, 3000),
    "HANOMAG-L6-2.3": f("ATM", E_, 2.3, "NC", 6, 3500, 2000, "SAE30", 5.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Hanomag")
L = []
IND = "données indicatives (marque ancienne), à vérifier"

mg(L, "2/10 PS Kommissbrot", "2/10 PS", "1", "1925-01", "1928-12", [("0.5 10", "HANOMAG-1C-0.5", 25)], portes=0, places=2, reservoir=15,
   remarques="Petite voiture à monocylindre arrière (surnommée « pain de munition »), sans portes ; " + IND)
mg(L, "3/16 PS", "3/16 PS", "1", "1928-01", "1931-12", [("0.75 16", "HANOMAG-L4-0.75", 38)], portes=2, places=4, reservoir=25, remarques=IND)
mg(L, "Garant", "4/23 PS", "1", "1932-01", "1938-12", [("1.1 23", "HANOMAG-L4-1.1", 60)], portes=2, places=4, reservoir=30,
   remarques="1,1 Liter (4/23 PS) jusqu'en 1934, puis Garant ; berline et cabriolet ; " + IND)
mg(L, "Kurier", "4/23 PS", "1", "1934-01", "1938-12", [("1.1 23", "HANOMAG-L4-1.1", 60)], portes=2, places=4, reservoir=30,
   remarques="Variante simplifiée du Garant ; " + IND)
mg(L, "Rekord", "Typ 15 K", "1", "1933-09", "1938-12", [("1.5 32", "HANOMAG-L4-1.5", 85, {"fin": "1936-12"}), ("1.5 35", "HANOMAG-L4-1.5", 88, {"debut": "1937-01"})],
   portes=4, places=4, reservoir=40, remarques="6/32 PS puis Rekord (1934), berline 4 portes, cabriolet et roadster ; restylage 1937 ; " + IND)
mg(L, "Rekord", "Diesel D 19", "1", "1937-01", "1940-12", [("Diesel 1.9 35", "HANOMAG-D19-1.9", 98)], portes=4, places=4, reservoir=40,
   remarques="Rekord Diesel (Typ D 19 A puis 19 K), présentée en 1936 au salon de Berlin, environ 1 100 exemplaires ; " + IND)
mg(L, "Sturm", "Sturm", "1", "1934-01", "1939-12", [("2.3 L6 50", "HANOMAG-L6-2.3", 130)], portes=4, places=5, reservoir=50,
   remarques="Six cylindres 2,25 l ; berline, cabriolet et roadster sport ; " + IND)
mg(L, "1,3 Liter", "1,3 Liter", "1", "1938-01", "1941-12", [("1.3 32", "HANOMAG-L4-1.3", 75)], portes=2, places=4, reservoir=35,
   remarques="Berline aérodynamique remplaçant Garant et Kurier, environ 9 200 exemplaires ; " + IND)

MOT = Motorisations("Hanomag", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Hanomag": L}
MOTEURS = MOT.moteurs()
