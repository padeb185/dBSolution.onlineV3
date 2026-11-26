"""Auto-Mixte : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur belge (Liège, procédé Henri Pieper) de véhicules hybrides essence-électrique (1906-1912) : voiture Pieper et camion Mixte.
Désignations, puissances et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "PIEPER-HYB-3.5": f("HYB_E", "ESS", 3.5, "NC", 4, 1500, 900, "SAE30", 5.0, 2000),
    "PIEPER-HYB-6.0": f("HYB_E", "ESS", 6.0, "NC", 4, 1200, 800, "SAE30", 7.0, 2000),
}
mg = SaisieMoteurs(FAMILLES, "Auto-Mixte", lambda fam: "Auto-Mixte")
L = []
IND = "hybride essence-électrique (dynamo-moteur Pieper) ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Pieper", "Pieper", "1", "1906-01", "1912-12", [("Hybride 3.5 24", "PIEPER-HYB-3.5", 120)], portes=4, places=4, reservoir=50, remarques="Torpédo ; " + IND)
mg(L, "Camion Mixte", "Mixte", "1", "1907-01", "1912-12", [("Hybride 6.0 30", "PIEPER-HYB-6.0", 200)], portes=2, places=2, reservoir=80, remarques="Camion et autobus ; " + IND)

MOT = Motorisations("Auto-Mixte", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Auto-Mixte": L}
MOTEURS = MOT.moteurs()
