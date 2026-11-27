"""Chenard-Walcker : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur de Gennevilliers : U3 (1920-1923), Tank (course, 1925-1926), Y7 (1930-1932) et Aigle 8 (V8 Ford, 1934-1936).
Puissances en ch. Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
CW = {
    "CHENARD-3.0": f("ATM", E_, 3.0, "NC", 4, 2400, 1400, "SAE30", 5.0, 3000),
    "CHENARD-1.1-DOHC": f("ATM", E_, 1.1, "NC", 4, 5500, 4000, "SAE30", 3.0, 2000),
    "CHENARD-1.5": f("ATM", E_, 1.5, "NC", 4, 3500, 2000, "SAE30", 3.5, 3000),
}
FORD = {"FORD-FLATHEAD-3.6": f("ATM", E_, 3.6, "NC", 8, 3800, 2000, "SAE30", 5.0, 3000, a="V")}
FAMILLES = {**CW, **FORD}
mg = SaisieMoteurs(FAMILLES, "Chenard-Walcker", lambda fam: "Ford" if fam in FORD else "Chenard-Walcker")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "U3", "U3", "1", "1920-01", "1923-12", [("3.0 40", "CHENARD-3.0", 150)], portes=4, places=4, reservoir=60, remarques="Torpédo 15 CV ; " + IND)
mg(L, "Tank", "Tank", "1", "1925-01", "1926-12", [("1.1 55", "CHENARD-1.1-DOHC", 80)], portes=0, places=2, reservoir=60,
   remarques="Voiture de course carénée, victoires aux 24 Heures du Mans (catégorie) ; " + IND)
mg(L, "Y7", "Y7", "1", "1930-01", "1932-12", [("1.5 35", "CHENARD-1.5", 85)], portes=4, places=5, reservoir=45, remarques="Berline ; " + IND)
mg(L, "Aigle 8", "Aigle 8", "1", "1934-01", "1936-12", [("3.6 V8 90", "FORD-FLATHEAD-3.6", 210)], portes=4, places=5, reservoir=60,
   remarques="Berline à V8 Ford (Matford) ; " + IND)

MOT = Motorisations("Chenard-Walcker", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Chenard-Walcker": L}
MOTEURS = MOT.moteurs()
