"""Hermes : générations, phases, motorisations (marché européen) et moteurs liés.
Marque de l'époque 1904-1909 associée aux Hermes-Simplex conçues par Ettore Bugatti pour Émile Mathis (Strasbourg), puis produites
sous le nom Hermes. Torpédo quatre cylindres. Puissances en ch.
Constructeur, désignations, cylindrée et dates indicatifs (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {"HERMES-L4-6.8": f("ATM", "ESS", 6.8, "NC", 4, 1400, 900, "SAE30", 6.0, 1000)}
mg = SaisieMoteurs(FAMILLES, "Hermes")
L = []

mg(L, "Type HP", "Type HP", "1", "1906-01", "1909-12", [("6.8 40", "HERMES-L4-6.8", 260)], portes=4, places=4, reservoir=80,
   remarques="Torpédo quatre cylindres, transmission par chaînes ; constructeur et données indicatifs (marque ancienne), à vérifier")

MOT = Motorisations("Hermes", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Hermes": L}
MOTEURS = MOT.moteurs()
