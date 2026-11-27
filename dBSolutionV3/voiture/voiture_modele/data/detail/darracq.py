"""Darracq : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur de Suresnes (Alexandre Darracq) : Flying Fifteen (1904-1906), Type L (1905-1907), 200 HP (voiture de record V8, 1905)
et Type V (1912-1914). Puissances en ch. Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "DARRACQ-1.6": f("ATM", E_, 1.6, "NC", 4, 1500, 900, "SAE30", 3.0, 2000),
    "DARRACQ-1.1": f("ATM", E_, 1.1, "NC", 1, 1400, 900, "SAE30", 2.0, 2000),
    "DARRACQ-V8-25.4": f("ATM", E_, 25.4, "NC", 8, 1200, 900, "SAE30", 15.0, 500, a="V"),
    "DARRACQ-2.4": f("ATM", E_, 2.4, "NC", 4, 2000, 1200, "SAE30", 4.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Darracq", lambda fam: "Darracq")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Flying Fifteen", "Flying Fifteen", "1", "1904-01", "1906-12", [("1.6 15", "DARRACQ-1.6", 80)], portes=0, places=4, reservoir=40,
   remarques="Tonneau, châssis en tôle emboutie ; " + IND)
mg(L, "Type L", "L", "1", "1905-01", "1907-12", [("1.1 9", "DARRACQ-1.1", 50)], portes=0, places=2, reservoir=30, remarques="Voiturette monocylindre ; " + IND)
mg(L, "200 HP", "200 HP", "1", "1905-01", "1905-12", [("25.4 V8 200", "DARRACQ-V8-25.4", 1200)], portes=0, places=1, reservoir=80,
   remarques="Voiture de record (Victor Hémery, 175 km/h en 1905) ; " + IND)
mg(L, "Type V", "V", "1", "1912-01", "1914-12", [("2.4 16", "DARRACQ-2.4", 90)], portes=4, places=4, reservoir=50, remarques="Torpédo ; " + IND)

MOT = Motorisations("Darracq", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Darracq": L}
MOTEURS = MOT.moteurs()
