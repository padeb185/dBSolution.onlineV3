"""Charron : générations, phases, motorisations (marché européen) et moteurs liés.
Charron, Girardot et Voigt (CGV, Puteaux) puis Charron : CGV 30 HP (1901-1906) et Charronette (1920-1925). Puissances en ch.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "CGV-7.2": f("ATM", "ESS", 7.2, "NC", 4, 1200, 800, "SAE30", 6.0, 2000),
    "CHARRON-1.0": f("ATM", "ESS", 1.0, "NC", 4, 2600, 1600, "SAE30", 2.5, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Charron", lambda fam: "Charron")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "CGV 30 HP", "CGV", "1", "1901-01", "1906-12", [("7.2 30", "CGV-7.2", 210)], portes=0, places=4, reservoir=70, remarques="Torpédo ; " + IND)
mg(L, "Charronette", "Charronette", "1", "1920-01", "1925-12", [("1.0 10", "CHARRON-1.0", 45)], portes=2, places=2, reservoir=25, remarques="Voiturette ; " + IND)

MOT = Motorisations("Charron", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Charron": L}
MOTEURS = MOT.moteurs()
