"""Méan (Liège, Belgique, 1966-1972) : générations, phases, motorisations (marché européen) et moteurs liés.
Sonora : barquette en polyester vendue en kit ou montée, moteur central Renault Gordini. Puissance en ch. Désignations et données indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "RENAULT-GORDINI-1.3": f("ATM", "ESS", 1.3, "CHAINE", 4, 6750, 5000, "20W50", 3.0, 5000),
}
mg = SaisieMoteurs(FAMILLES, "Renault")
L = []
mg(L, "Sonora", "Sonora", "1", "1966-01", "1972-12", [("1.3 Gordini 103", "RENAULT-GORDINI-1.3", 117)], portes=0, places=2, reservoir=40, remarques="Barquette à moteur central Renault 8 Gordini ; données indicatives (marque ancienne), à vérifier")

MOT = Motorisations("Renault", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Méan": L}
MOTEURS = MOT.moteurs()
