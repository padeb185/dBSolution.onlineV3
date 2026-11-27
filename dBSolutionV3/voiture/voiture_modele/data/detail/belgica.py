"""Belgica : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur belge (Bruxelles, 1899-1909) : Type 16/20 HP. Désignations, puissances et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {"BELGICA-3.8": f("ATM", "ESS", 3.8, "NC", 4, 1400, 900, "SAE30", 5.0, 2000)}
mg = SaisieMoteurs(FAMILLES, "Belgica", lambda fam: "Belgica")
L = []

mg(L, "Type 16/20 HP", "16/20 HP", "1", "1900-01", "1909-12", [("3.8 20", "BELGICA-3.8", 110)], portes=4, places=4, reservoir=50,
   remarques="Torpédo ; désignations et dates indicatives (marque ancienne), à vérifier")

MOT = Motorisations("Belgica", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Belgica": L}
MOTEURS = MOT.moteurs()
