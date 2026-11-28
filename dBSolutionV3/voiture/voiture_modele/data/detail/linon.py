"""Linon (Verviers, Belgique, 1900-1914) : générations, phases, motorisations (marché européen) et moteurs liés.
Voiturettes à moteurs De Dion-Bouton puis Linon. Puissances en ch. Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "LINON-1C-0.5": f("ATM", "ESS", 0.5, "NC", 1, 1800, 1200, "SAE30", 1.5, 1000),
}
mg = SaisieMoteurs(FAMILLES, "Linon")
L = []
mg(L, "Voiturette", "Voiturette", "1", "1900-01", "1914-12", [("0.5 6", "LINON-1C-0.5", 22)], portes=0, places=2, reservoir=20, remarques="Voiturette monocylindre ; données indicatives (marque ancienne), à vérifier")

MOT = Motorisations("Linon", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Linon": L}
MOTEURS = MOT.moteurs()
