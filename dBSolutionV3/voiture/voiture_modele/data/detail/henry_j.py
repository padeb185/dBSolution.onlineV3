"""Henry J (Kaiser-Frazer) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Compacte économique 2 portes (1950-1954) : Henry J, Vagabond (1952) et Corsair (1952-1954). Quatre et six cylindres Willys repris
d'allstate.py (version Sears de la même voiture). Puissances brutes (SAE gross) converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .allstate import FAMILLES as FAMILLES_ALLSTATE

FAMILLES = dict(FAMILLES_ALLSTATE)
mg = SaisieMoteurs(FAMILLES, "Willys")
L = []
V = [("2.2 69", "WILLYS-L4-2.2", 155), ("2.6 L6 81", "WILLYS-L6-2.6", 183)]
IND = "marché nord-américain ; données indicatives"

mg(L, "Henry J", "Henry J", "1", "1950-09", "1951-12", V, portes=2, places=5, reservoir=49,
   remarques="Standard (quatre cylindres) et DeLuxe (six cylindres), berline fastback sans malle ouvrante à l'origine ; " + IND)
mg(L, "Vagabond", "Henry J", "1", "1952-01", "1952-12", V, portes=2, places=5, reservoir=49,
   remarques="Henry J 1951 invendues rebaptisées, roue de secours extérieure (continental kit) ; " + IND)
mg(L, "Corsair", "Henry J", "2", "1952-01", "1954-08", V, portes=2, places=5, reservoir=49,
   remarques="Corsair et Corsair DeLuxe (restylage 1952, malle ouvrante) ; " + IND)

MOT = Motorisations("Willys", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Henry J": L}
MOTEURS = MOT.moteurs()
