"""Komnick (Elbing, Prusse orientale, 1907-1930) : générations, phases, motorisations (marché européen) et moteurs liés.
Voitures de tourisme (Typ G 6/18 PS) ; Komnick s'est ensuite consacré aux camions et tracteurs (repris par Büssing en 1930).
Puissances en ch. Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "KOMNICK-L4-1.6": f("ATM", "ESS", 1.6, "NC", 4, 2000, 1200, "SAE30", 3.0, 1000),
}
mg = SaisieMoteurs(FAMILLES, "Komnick")
L = []
mg(L, "Typ G 6/18 PS", "Typ G", "1", "1913-01", "1918-12", [("1.6 18", "KOMNICK-L4-1.6", 70)], portes=4, places=4, reservoir=40, remarques="Torpédo ; données indicatives (marque ancienne), à vérifier")

MOT = Motorisations("Komnick", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Komnick": L}
MOTEURS = MOT.moteurs()
