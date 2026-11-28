"""Metropolitan (Nash puis Hudson / AMC, construite par Austin à Longbridge, 1953-1961) : générations, phases, motorisations et moteurs liés.
Petite voiture américaine (hardtop et cabriolet), aussi vendue au Royaume-Uni sous la marque Austin Metropolitan. Moteurs Austin série A puis
série B. Puissances brutes converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "AUSTIN-A40-1.2": f("ATM", "ESS", 1.2, "CHAINE", 4, 4500, 2400, "20W50", 3.5, 5000),
    "BMC-B-1.5": f("ATM", "ESS", 1.5, "CHAINE", 4, 4500, 2100, "20W50", 4.5, 5000),
}
mg = SaisieMoteurs(FAMILLES, "Austin")
L = []
IND = "données indicatives"
mg(L, "Metropolitan", "Series I-II", "1", "1953-10", "1956-08", [("1.2 43", "AUSTIN-A40-1.2", 79)], portes=2, places=3, reservoir=40, remarques="Hardtop et cabriolet, moteur Austin A40 ; " + IND)
mg(L, "Metropolitan", "Series III-IV", "1", "1956-09", "1961-12", [("1500 1.5 53", "BMC-B-1.5", 102, {"fin": "1959-01"}), ("1500 1.5 56", "BMC-B-1.5", 106, {"debut": "1959-02"})],
   portes=2, places=3, reservoir=40, remarques="Moteur série B 1 489 cm³, coffre ouvrant dès 1959 ; " + IND)

MOT = Motorisations("Austin", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Metropolitan": L}
MOTEURS = MOT.moteurs()
