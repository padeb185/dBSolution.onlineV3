"""Dasse : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur belge (Verviers, 1894-1924) : Type B (1905-1914) et Type 12/14 CV (1920-1924). Puissances en ch.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "DASSE-3.0": f("ATM", "ESS", 3.0, "NC", 4, 1600, 1000, "SAE30", 5.0, 2000),
    "DASSE-2.6": f("ATM", "ESS", 2.6, "NC", 4, 2400, 1400, "SAE30", 4.5, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Dasse", lambda fam: "Dasse")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Type B", "B", "1", "1905-01", "1914-12", [("3.0 20", "DASSE-3.0", 110)], portes=4, places=4, reservoir=55, remarques="Torpédo ; " + IND)
mg(L, "Type 12/14 CV", "12/14 CV", "1", "1920-01", "1924-12", [("2.6 30", "DASSE-2.6", 115)], portes=4, places=4, reservoir=55, remarques="Torpédo ; " + IND)

MOT = Motorisations("Dasse", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Dasse": L}
MOTEURS = MOT.moteurs()
