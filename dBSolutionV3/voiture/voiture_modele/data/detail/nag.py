"""NAG (Neue Automobil-Gesellschaft, Berlin, groupe AEG, 1901-1934) : générations, phases, motorisations (marché européen) et moteurs liés.
C4, D4 et 212 (NAG-Protos) ; activité voitures fusionnée avec Büssing (Büssing-NAG). Puissances en ch.
Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "NAG-L4-2.5": f("ATM", "ESS", 2.5, "NC", 4, 2400, 1400, "SAE30", 4.0, 2000),
    "NAG-L4-2.6": f("ATM", "ESS", 2.6, "NC", 4, 2500, 1400, "SAE30", 4.0, 2000),
    "NAG-L6-3.1": f("ATM", "ESS", 3.1, "NC", 6, 3000, 1600, "SAE30", 5.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "NAG")
L = []
IND = "données indicatives (marque ancienne), à vérifier"
mg(L, "C4", "C4", "1", "1920-01", "1924-12", [("2.5 30", "NAG-L4-2.5", 110)], portes=4, places=4, reservoir=50, remarques=IND)
mg(L, "D4", "D4", "1", "1925-01", "1927-12", [("2.6 35", "NAG-L4-2.6", 120)], portes=4, places=4, reservoir=50, remarques=IND)
mg(L, "212", "212", "1", "1927-01", "1929-12", [("3.1 L6 60", "NAG-L6-3.1", 170)], portes=4, places=5, reservoir=60, remarques="NAG-Protos ; " + IND)

MOT = Motorisations("NAG", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"NAG": L}
MOTEURS = MOT.moteurs()
