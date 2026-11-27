"""Fondu : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur belge (Vilvorde, 1906-1912) : Type 1, voiturette à quatre cylindres. Puissance en ch.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {"FONDU-1.8": f("ATM", "ESS", 1.8, "NC", 4, 1800, 1100, "SAE30", 3.5, 2000)}
mg = SaisieMoteurs(FAMILLES, "Fondu", lambda fam: "Fondu")
L = []

mg(L, "Type 1", "1", "1", "1906-01", "1912-12", [("1.8 12", "FONDU-1.8", 60)], portes=0, places=2, reservoir=30,
   remarques="Voiturette ; désignations et dates indicatives (marque ancienne), à vérifier")

MOT = Motorisations("Fondu", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Fondu": L}
MOTEURS = MOT.moteurs()
