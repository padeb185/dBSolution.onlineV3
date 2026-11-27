"""Brush : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Brush Runabout Company (Detroit, 1907-1911) : Runabout, voiturette à châssis en bois et monocylindre.
Puissance brute convertie en ch (× 1,014). Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {"BRUSH-1.0": f("ATM", "ESS", 1.0, "NC", 1, 1400, 800, "SAE30", 1.5, 1000)}
mg = SaisieMoteurs(FAMILLES, "Brush", lambda fam: "Brush")
L = []

mg(L, "Runabout", "Runabout", "1", "1907-01", "1911-12", [("1.0 10", "BRUSH-1.0", 50)], portes=0, places=2, reservoir=20,
   remarques="Voiturette à châssis et essieux en bois, monocylindre vertical ; marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier")

MOT = Motorisations("Brush", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Brush": L}
MOTEURS = MOT.moteurs()
