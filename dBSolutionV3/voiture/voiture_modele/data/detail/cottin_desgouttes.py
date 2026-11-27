"""Cottin & Desgouttes : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur lyonnais (1904-1931) : Type M (1912-1922) et Sans Secousses (suspension à quatre roues indépendantes, 1927-1931).
Puissances en ch. Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "COTTIN-3.2": f("ATM", "ESS", 3.2, "NC", 4, 2000, 1200, "SAE30", 5.0, 3000),
    "COTTIN-2.6": f("ATM", "ESS", 2.6, "NC", 4, 3000, 1600, "SAE30", 4.5, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Cottin & Desgouttes", lambda fam: "Cottin & Desgouttes")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Type M", "M", "1", "1912-01", "1922-12", [("3.2 30", "COTTIN-3.2", 140)], portes=4, places=4, reservoir=60, remarques="Torpédo ; " + IND)
mg(L, "Sans Secousses", "Sans Secousses", "1", "1927-01", "1931-12", [("2.6 50", "COTTIN-2.6", 150)], portes=4, places=5, reservoir=55,
   remarques="Berline à quatre roues indépendantes ; " + IND)

MOT = Motorisations("Cottin & Desgouttes", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Cottin & Desgouttes": L}
MOTEURS = MOT.moteurs()
