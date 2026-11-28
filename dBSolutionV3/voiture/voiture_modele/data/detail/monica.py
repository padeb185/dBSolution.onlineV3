"""Monica (Balbigny, France, 1973-1975) : générations, phases, motorisations (marché français) et moteurs liés.
Monica 560, berline de grand luxe à V8 Chrysler (environ 25 exemplaires). Puissance en ch. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "CHRYSLER-LA-5.6": f("ATM", "ESS", 5.6, "CHAINE", 8, 5000, 3200, "10W30", 4.7, 5000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Chrysler")
L = []
mg(L, "560", "560", "1", "1973-01", "1975-12", [("5.6 V8 285", "CHRYSLER-LA-5.6", 460)], portes=4, places=5, reservoir=100,
   remarques="Berline de luxe (Jean Tastevin), environ 25 exemplaires ; données indicatives")

MOT = Motorisations("Chrysler", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Monica": L}
MOTEURS = MOT.moteurs()
