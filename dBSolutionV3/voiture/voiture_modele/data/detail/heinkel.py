"""Heinkel : générations, phases, motorisations (marché européen) et moteurs liés.
Heinkel Kabine (1956-1958, Stuttgart-Zuffenhausen) : microvoiture « bulle » à porte frontale, trois roues (Typ 153) ou quatre roues
(Typ 154). Production poursuivie sous licence en Irlande puis au Royaume-Uni (Trojan 200, 1961-1966, non repris ici).
Nombre de portes : 2 imposé par le référentiel (porte frontale unique en réalité). Puissances en ch DIN. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {"HEINKEL-1C-0.2": f("ATM", "ESS", 0.2, "NC", 1, 5500, 4000, "SAE30", 1.0, 2000)}
mg = SaisieMoteurs(FAMILLES, "Heinkel")
L = []
R = "porte frontale unique (2 portes au référentiel), 2 adultes et 1 enfant ; données indicatives"

mg(L, "Kabine", "Typ 153", "1", "1956-03", "1958-12", [("0.17 9", "HEINKEL-1C-0.2", 12)], portes=2, places=3, reservoir=14,
   remarques="Trois roues, monocylindre quatre temps 174 cm³ ; " + R)
mg(L, "Kabine", "Typ 154", "1", "1957-01", "1958-12", [("0.2 10", "HEINKEL-1C-0.2", 14)], portes=2, places=3, reservoir=14,
   remarques="Quatre roues, monocylindre 204 cm³ ; " + R)

MOT = Motorisations("Heinkel", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Heinkel": L}
MOTEURS = MOT.moteurs()
