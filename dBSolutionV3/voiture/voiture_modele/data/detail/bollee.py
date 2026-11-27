"""Bollée : générations, phases, motorisations (marché européen) et moteurs liés.
Amédée Bollée père (véhicules à vapeur du Mans : L'Obéissante 1873, La Mancelle 1878) et Léon Bollée (Voiturette tricar, 1895-1898).
Les machines à vapeur n'ayant pas de type moteur dédié, elles sont saisies en « essence atmosphérique » avec remarque.
Puissances en ch. Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "BOLLEE-VAPEUR-V2": f("ATM", "ESS", 0.0, "NC", 2, 300, 100, "SAE30", 2.0, 1000, a="V"),
    "LEON-BOLLEE-0.65": f("ATM", "ESS", 0.65, "NC", 1, 1800, 1000, "SAE30", 1.0, 1000),
}
mg = SaisieMoteurs(FAMILLES, "Bollée", lambda fam: "Bollée")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"
VAP = "machine à vapeur (chaudière au charbon), type de moteur non représentable : saisie indicative"

mg(L, "L'Obéissante", "L'Obéissante", "1", "1873-01", "1873-12", [("Vapeur 15", "BOLLEE-VAPEUR-V2", 300)], portes=0, places=12, reservoir=0,
   remarques="Diligence à vapeur d'Amédée Bollée, deux moteurs bicylindres en V ; " + VAP + " ; " + IND)
mg(L, "La Mancelle", "La Mancelle", "1", "1878-01", "1880-12", [("Vapeur 15", "BOLLEE-VAPEUR-V2", 300)], portes=0, places=6, reservoir=0,
   remarques="Calèche à vapeur, moteur à l'avant ; " + VAP + " ; " + IND)
mg(L, "Voiturette", "Voiturette", "1", "1895-01", "1898-12", [("0.65 3", "LEON-BOLLEE-0.65", 9)], portes=0, places=2, reservoir=8,
   remarques="Tricar Léon Bollée, monocylindre horizontal ; " + IND)

MOT = Motorisations("Bollée", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Bollée": L}
MOTEURS = MOT.moteurs()
