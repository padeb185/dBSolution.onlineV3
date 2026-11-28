"""Jenatzy (Camille Jenatzy, Bruxelles) : générations, phases, motorisations (marché européen) et moteurs liés.
La Jamais Contente (1899), première automobile à dépasser 100 km/h (électrique, deux moteurs de traction), et voitures
pétroléo-électriques (hybrides essence-électrique, 1902-1905). Puissances en ch.
Désignations, caractéristiques et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

FAMILLES = {"JENATZY-EV": electrique(1000), "JENATZY-HYBRIDE-4.0": f("HYB_E", "ESS", 4.0, "NC", 4, 1500, 900, "SAE30", 4.0, 1000)}
mg = SaisieMoteurs(FAMILLES, "Jenatzy")
L = []
IND = "données indicatives (marque ancienne), à vérifier"

mg(L, "La Jamais Contente", "La Jamais Contente", "1", "1899-04", "1899-12", [("Électrique 68", "JENATZY-EV", 300)], portes=0, places=1, reservoir=0,
   remarques="Voiture de record électrique en alliage partinium, 105,88 km/h le 29 avril 1899 (Achères) ; exemplaire unique ; " + IND)
mg(L, "Pétroléo-électrique", "Pétroléo-électrique", "1", "1902-01", "1905-12", [("Hybride 4.0 20", "JENATZY-HYBRIDE-4.0", 110)], portes=0, places=4, reservoir=50,
   remarques="Tonneau hybride : moteur à essence couplé à une dynamo-moteur ; " + IND)

MOT = Motorisations("Jenatzy", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Jenatzy": L}
MOTEURS = MOT.moteurs()
