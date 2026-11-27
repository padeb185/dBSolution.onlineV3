"""Büssing : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur de Brunswick de camions et d'autobus : NAG 500 (Büssing-NAG), 8000, Burglöwe, Commodore (moteur sous plancher),
Präfekt et BS 110 V (autobus standard VÖV). Reprise par MAN en 1971. Diesels six cylindres Büssing. Puissances en ch DIN.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

D = "DSL"
FAMILLES = {
    "BUSSING-L6-7.4": f("ATM", D, 7.4, "NC", 6, 2000, 1200, "15W40", 14.0, 10000),
    "BUSSING-L6-13.5": f("ATM", D, 13.5, "NC", 6, 2000, 1200, "15W40", 25.0, 10000),
    "BUSSING-L6-8.7": f("ATM", D, 8.7, "NC", 6, 2200, 1300, "15W40", 18.0, 10000),
    "BUSSING-U-11.6": f("ATM", D, 11.6, "NC", 6, 2200, 1300, "15W40", 24.0, 15000),
    "BUSSING-U-11.0": f("ATM", D, 11.0, "NC", 6, 2200, 1300, "15W40", 22.0, 15000),
}
mg = SaisieMoteurs(FAMILLES, "Büssing", lambda fam: "Büssing")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "NAG 500", "500", "1", "1932-01", "1940-12", [("7.4 Diesel 90", "BUSSING-L6-7.4", 380)], portes=2, places=2, reservoir=120, remarques="Camion Büssing-NAG ; " + IND)
mg(L, "8000", "8000", "1", "1950-01", "1955-12", [("13.5 Diesel 180", "BUSSING-L6-13.5", 700)], portes=2, places=2, reservoir=200, remarques="Camion lourd ; " + IND)
mg(L, "Burglöwe", "Burglöwe", "1", "1955-01", "1962-12", [("8.7 Diesel 150", "BUSSING-L6-8.7", 540)], portes=2, places=2, reservoir=180, remarques="Camion lourd ; " + IND)
mg(L, "Commodore", "Commodore", "1", "1964-01", "1971-12", [("11.6 Diesel 210", "BUSSING-U-11.6", 800)], portes=2, places=2, reservoir=250,
   remarques="Camion à cabine avancée, moteur horizontal sous plancher ; " + IND)
mg(L, "Präfekt", "Präfekt", "1", "1960-01", "1971-12", [("11.0 Diesel 150", "BUSSING-U-11.0", 560), ("11.0 Diesel 192", "BUSSING-U-11.0", 700, {"debut": "1965-01"})],
   portes=2, places=80, reservoir=200, remarques="Autobus à moteur sous plancher ; " + IND)
mg(L, "BS 110 V", "BS 110 V", "1", "1968-01", "1971-12", [("11.0 Diesel 192", "BUSSING-U-11.0", 700)], portes=2, places=100, reservoir=200,
   remarques="Autobus standard VÖV, poursuivi par MAN (SL 200) ; " + IND)

MOT = Motorisations("Büssing", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Büssing": L}
MOTEURS = MOT.moteurs()
