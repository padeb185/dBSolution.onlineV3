"""Berliet : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur lyonnais : voitures (Type B, VB, Dauphine) puis camions et autobus (GLR, GBH, PR 100, TR 280) jusqu'à
l'intégration dans Renault Véhicules Industriels (1978-1980). Puissances en ch. Désignations et dates indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
D = "DSL"
FAMILLES = {
    "BERLIET-0.9": f("ATM", E_, 0.9, "NC", 2, 1200, 800, "SAE30", 2.5, 2000),
    "BERLIET-3.3": f("ATM", E_, 3.3, "NC", 4, 2400, 1200, "SAE30", 5.0, 3000),
    "BERLIET-2.0": f("ATM", E_, 2.0, "NC", 4, 3800, 2200, "SAE30", 4.5, 3000),
    "BERLIET-MDU-7.9": f("ATM", D, 7.9, "NC", 5, 2100, 1300, "15W40", 16.0, 10000),
    "BERLIET-MK-12": f("ATM", D, 12.0, "NC", 6, 2000, 1300, "15W40", 24.0, 10000),
    "BERLIET-MIH-9.8": f("ATM", D, 9.8, "NC", 6, 2200, 1400, "15W40", 20.0, 15000),
    "BERLIET-MIDS-15": f("TURBO", D, 15.0, "NC", 6, 2000, 1300, "15W40", 30.0, 20000),
}
mg = SaisieMoteurs(FAMILLES, "Berliet", lambda fam: "Berliet")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Type B", "Type B", "1", "1900-01", "1902-12", [("0.9 6", "BERLIET-0.9", 25)], portes=0, places=2, reservoir=20, remarques="Voiturette ; " + IND)
mg(L, "VB", "VB", "1", "1920-01", "1925-12", [("3.3 22", "BERLIET-3.3", 120)], portes=4, places=4, reservoir=60, remarques="Torpédo ; " + IND)
mg(L, "Dauphine", "Dauphine", "1", "1934-01", "1939-12", [("2.0 50", "BERLIET-2.0", 120)], portes=4, places=5, reservoir=55,
   remarques="Berline, dernière voiture particulière Berliet ; " + IND)
mg(L, "GLR", "GLR", "1", "1949-01", "1977-12", [("7.9 Diesel 125", "BERLIET-MDU-7.9", 450)], portes=2, places=2, reservoir=150,
   remarques="Camion porteur, cinq cylindres diesel MDU ; " + IND)
mg(L, "GBH", "GBH", "1", "1958-01", "1977-12", [("12.0 Diesel 200", "BERLIET-MK-12", 720)], portes=2, places=2, reservoir=200,
   remarques="Camion lourd tout-terrain 6x4 (chantier) ; " + IND)
mg(L, "PR 100", "PR 100", "1", "1971-01", "1980-12", [("9.8 Diesel 200", "BERLIET-MIH-9.8", 700)], portes=2, places=100, reservoir=200,
   remarques="Autobus urbain (poursuivi par Renault RVI) ; " + IND)
mg(L, "TR 280", "TR 280", "1", "1977-01", "1980-12", [("15.0 Turbo Diesel 280", "BERLIET-MIDS-15", 1100)], portes=2, places=2, reservoir=400,
   remarques="Tracteur routier (poursuivi par Renault RVI) ; " + IND)

MOT = Motorisations("Berliet", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Berliet": L}
MOTEURS = MOT.moteurs()
