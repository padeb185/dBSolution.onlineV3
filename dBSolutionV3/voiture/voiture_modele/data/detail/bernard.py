"""Bernard : générations, phases, motorisations (marché européen) et moteurs liés.
Camions Bernard (Arcueil, France) : Type 110 (1950-1955) et Type 150 (1955-1963), diesels sous licence MAN.
Puissances en ch. Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

D = "DSL"
FAMILLES = {
    "BERNARD-MAN-8.3": f("ATM", D, 8.3, "NC", 6, 2000, 1200, "15W40", 16.0, 10000),
    "BERNARD-MAN-10.6": f("ATM", D, 10.6, "NC", 6, 2000, 1200, "15W40", 20.0, 10000),
}
mg = SaisieMoteurs(FAMILLES, "Bernard", lambda fam: "Bernard")
L = []
IND = "camion ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Type 110", "110", "1", "1950-01", "1955-12", [("8.3 Diesel 110", "BERNARD-MAN-8.3", 450)], portes=2, places=2, reservoir=150, remarques=IND)
mg(L, "Type 150", "150", "1", "1955-01", "1963-12", [("10.6 Diesel 150", "BERNARD-MAN-10.6", 600)], portes=2, places=2, reservoir=200, remarques=IND)

MOT = Motorisations("Bernard", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Bernard": L}
MOTEURS = MOT.moteurs()
