"""Krupp (Essen) : générations, phases, motorisations (marché européen) et moteurs liés.
Krupp Protze (tout-terrain militaire L2H43 / L2H143, 1934-1941), camions Mustang et Titan (diesels deux temps Krupp, 1950-1954) et KF 380
(1963-1968) ; production de camions arrêtée en 1968. Puissances en ch DIN. Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "KRUPP-B4-3.3": f("ATM", "ESS", 3.3, "NC", 4, 2500, 1500, "SAE30", 6.0, 3000, a="PLAT"),
    "KRUPP-2TD-4.8": f("ATM", "DSL", 4.8, "AUCUNE", 4, 2000, 1300, "15W40", 12.0, 5000),
    "KRUPP-2TD-9.9": f("ATM", "DSL", 9.9, "AUCUNE", 6, 2000, 1300, "15W40", 20.0, 5000),
    "KRUPP-D-11.6": f("ATM", "DSL", 11.6, "NC", 6, 2200, 1300, "15W40", 22.0, 10000),
}
mg = SaisieMoteurs(FAMILLES, "Krupp")
L = []
IND = "camion / véhicule militaire ; données indicatives (marque ancienne), à vérifier"
mg(L, "Protze", "L2H43", "1", "1934-01", "1941-12", [("3.3 Flat-4 60", "KRUPP-B4-3.3", 180)], portes=4, places=8, reservoir=110, remarques="Six roues, moteur boxer refroidi par air ; " + IND)
mg(L, "Mustang", "Mustang", "1", "1950-01", "1954-12", [("Diesel 2T 4.8 110", "KRUPP-2TD-4.8", 400)], portes=2, places=2, reservoir=150, remarques="Diesel deux temps quatre cylindres ; " + IND)
mg(L, "Titan", "Titan", "1", "1950-01", "1954-12", [("Diesel 2T 9.9 210", "KRUPP-2TD-9.9", 830)], portes=2, places=2, reservoir=250, remarques="Camion lourd, diesel deux temps six cylindres ; " + IND)
mg(L, "KF 380", "KF 380", "1", "1963-01", "1968-12", [("Diesel 11.6 210", "KRUPP-D-11.6", 800)], portes=2, places=2, reservoir=250, remarques="Cabine avancée ; " + IND)

MOT = Motorisations("Krupp", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Krupp": L}
MOTEURS = MOT.moteurs()
