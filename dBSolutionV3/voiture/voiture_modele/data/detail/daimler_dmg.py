"""Daimler (Daimler-Motoren-Gesellschaft) : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur de Cannstatt / Untertürkheim avant la fusion avec Benz (1926) : Stahlradwagen, Riemenwagen, Mercedes 35 PS,
Mercedes Simplex, Mercedes 28/95 PS et Mercedes 6/25/40 PS (compresseur). Puissances en ch.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "DMG-V2-0.57": f("ATM", E_, 0.57, "NC", 2, 600, 400, "SAE30", 1.0, 1000, a="V"),
    "DMG-PHOENIX-1.1": f("ATM", E_, 1.06, "NC", 2, 700, 500, "SAE30", 1.5, 1000),
    "DMG-5.9": f("ATM", E_, 5.9, "NC", 4, 950, 700, "SAE30", 6.0, 2000),
    "DMG-SIMPLEX-6.8": f("ATM", E_, 6.8, "NC", 4, 1100, 800, "SAE30", 6.0, 2000),
    "DMG-L6-7.3": f("ATM", E_, 7.3, "NC", 6, 1800, 1000, "SAE30", 8.0, 3000),
    "DMG-1.6C": f("TURBO", E_, 1.6, "NC", 4, 3600, 2200, "SAE30", 4.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Daimler", lambda fam: "Daimler")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Stahlradwagen", "Stahlradwagen", "1", "1889-01", "1890-12", [("0.57 V2 2", "DMG-V2-0.57", 8)], portes=0, places=2, reservoir=5,
   remarques="« Voiture à roues d'acier », bicylindre en V ; " + IND)
mg(L, "Riemenwagen", "Riemenwagen", "1", "1895-01", "1899-12", [("1.1 4", "DMG-PHOENIX-1.1", 25)], portes=0, places=4, reservoir=10,
   remarques="Vis-à-vis à transmission par courroies, moteur Phönix ; " + IND)
mg(L, "Mercedes 35 PS", "35 PS", "1", "1901-01", "1902-12", [("5.9 35", "DMG-5.9", 260)], portes=0, places=4, reservoir=60,
   remarques="Première « Mercedes » (Emil Jellinek), radiateur en nid d'abeilles ; " + IND)
mg(L, "Mercedes Simplex", "Simplex", "1", "1902-01", "1909-12", [("6.8 40", "DMG-SIMPLEX-6.8", 280)], portes=0, places=4, reservoir=70, remarques="Tonneau ; " + IND)
mg(L, "Mercedes 28/95 PS", "28/95", "1", "1914-01", "1924-12", [("7.3 L6 95", "DMG-L6-7.3", 380)], portes=4, places=4, reservoir=90,
   remarques="Six cylindres à arbre à cames en tête ; " + IND)
mg(L, "Mercedes 6/25/40 PS", "6/25/40", "1", "1923-01", "1926-12", [("1.6 Kompressor 40", "DMG-1.6C", 90)], portes=4, places=4, reservoir=45,
   remarques="25 ch, 40 ch avec compresseur enclenché ; " + IND)

MOT = Motorisations("Daimler", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Daimler": L}
MOTEURS = MOT.moteurs()
