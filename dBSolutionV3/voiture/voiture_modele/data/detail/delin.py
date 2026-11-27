"""Delin : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur belge (Louvain, 1899-1901) : Voiturette à monocylindre De Dion. Puissance en ch.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .de_dion_bouton import FAMILLES as FAMILLES_DEDION

FAMILLES = {"DEDION-0.4": FAMILLES_DEDION["DEDION-0.4"]}
mg = SaisieMoteurs(FAMILLES, "De Dion-Bouton", lambda fam: "De Dion-Bouton")
L = []

mg(L, "Voiturette", "Voiturette", "1", "1899-01", "1901-12", [("0.4 4", "DEDION-0.4", 18)], portes=0, places=2, reservoir=15,
   remarques="Voiturette à monocylindre De Dion-Bouton (même moteur que de_dion_bouton.py) ; désignations et dates indicatives (marque ancienne), à vérifier")

MOT = Motorisations("Delin", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Delin": L}
MOTEURS = MOT.moteurs()
