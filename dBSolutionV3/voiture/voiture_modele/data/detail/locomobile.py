"""Locomobile (Locomobile Company of America, Bridgeport, 1899-1929) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Steam Runabout (vapeur, licence Stanley), Old 16 (victoire à la Coupe Vanderbilt 1908), Model 48 (voiture de luxe) et Junior Eight.
Vapeur : référentiel sans carburant « vapeur », saisie en essence atmosphérique (brûleur à essence). Puissances brutes converties en ch (× 1,014).
Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "LOCO-VAPEUR-2C": f("ATM", "ESS", 0.6, "AUCUNE", 2, 500, 300, "SAE30", 1.0, 500),
    "LOCO-L4-16.2": f("ATM", "ESS", 16.2, "NC", 4, 1200, 800, "SAE30", 12.0, 1000),
    "LOCO-L6-8.6": f("ATM", "ESS", 8.6, "NC", 6, 2000, 1000, "SAE30", 9.0, 2000),
    "LOCO-L8-3.2": f("ATM", "ESS", 3.2, "NC", 8, 3200, 1600, "SAE30", 5.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Locomobile")
L = []
IND = "marché nord-américain ; données indicatives (marque ancienne), à vérifier"
mg(L, "Steam Runabout", "Steam", "1", "1899-01", "1903-12", [("Vapeur 5", "LOCO-VAPEUR-2C", 50)], portes=0, places=2, reservoir=60,
   remarques="Voiture à vapeur, bicylindre, chaudière chauffée à l'essence (pas de carburant « vapeur » au référentiel) ; " + IND)
mg(L, "Old 16", "Old 16", "1", "1906-01", "1906-12", [("16.2 91", "LOCO-L4-16.2", 450)], portes=0, places=2, reservoir=100,
   remarques="Voiture de course, première américaine victorieuse en compétition internationale (Coupe Vanderbilt 1908) ; " + IND)
mg(L, "Model 48", "Model 48", "1", "1911-01", "1929-12", [("8.6 L6 96", "LOCO-L6-8.6", 380)], portes=4, places=7, reservoir=100, remarques="Voiture de luxe à six cylindres ; " + IND)
mg(L, "Junior Eight", "Junior Eight", "1", "1925-01", "1929-12", [("3.2 L8 67", "LOCO-L8-3.2", 180)], portes=4, places=5, reservoir=70, remarques="Période Durant Motors ; " + IND)

MOT = Motorisations("Locomobile", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Locomobile": L}
MOTEURS = MOT.moteurs()
