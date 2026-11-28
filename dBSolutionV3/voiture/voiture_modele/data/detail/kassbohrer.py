"""Kässbohrer (Ulm) : générations, phases, motorisations (marché européen) et moteurs liés.
Autocar Setra S 8 (premier autocar autoporteur de série, 1951-1956 ; les Setra suivants sont dans la marque Setra) et dameuse PistenBully
(depuis 1969, moteurs Mercedes-Benz puis Cummins). Une motorisation représentative par génération. Puissances en ch. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "HENSCHEL-6D-5.5": f("ATM", "DSL", 5.5, "NC", 6, 2400, 1400, "15W40", 12.0, 10000),
    "MB-OM-5.7D": f("ATM", "DSL", 5.7, "NC", 6, 2800, 1600, "15W40", 12.0, 500),
    "MB-OM460-12.8D": f("TURBO", "DSL", 12.8, "NC", 6, 1800, 1200, "10W40", 35.0, 500),
}
mg = SaisieMoteurs(FAMILLES, "Mercedes-Benz", lambda fam: "Henschel" if fam.startswith("HENSCHEL") else "Mercedes-Benz")
L = []
IND = "données indicatives"
mg(L, "Setra S 8", "S 8", "1", "1951-01", "1956-12", [("Diesel 5.5 L6 115", "HENSCHEL-6D-5.5", 380)], portes=2, places=30, reservoir=150,
   remarques="Autocar à caisse autoporteuse (Selbsttragend → Setra), 8 rangées de sièges ; " + IND)
mg(L, "PistenBully", "PistenBully", "1", "1969-01", "1990-12", [("Diesel 5.7 L6 100", "MB-OM-5.7D", 350)], portes=2, places=2, reservoir=150,
   remarques="Dameuse de pistes à chenilles ; intervalle d'entretien en heures, valeur indicative ; " + IND)
mg(L, "PistenBully", "PistenBully 600", "1", "2000-01", None, [("Diesel 12.8 Turbo 400", "MB-OM460-12.8D", 2000)], portes=2, places=2, reservoir=250,
   remarques="PistenBully 600 (puis moteurs Cummins, versions hybride et électrique) ; " + IND)

MOT = Motorisations("Mercedes-Benz", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Kässbohrer": L}
MOTEURS = MOT.moteurs()
