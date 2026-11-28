"""Hansa : générations, phases, motorisations (marché européen) et moteurs liés.
Marque de Brême reprise par Borgward (1929) : Hansa 400 / 500 (deux-temps arrière, 1933-1934), 1100 (1934-1939), 1700 (1934-1939),
2000 (1937-1939, devenue Borgward 2000) et 3500 Privat (1936-1939) ; Hansa 1100 (1958-1961, ex-Goliath 1100, moteurs repris de
goliath.py). Les Borgward Hansa 1500 / 1800 d'après-guerre sont dans borgward.py. Modèles Hansa et Hansa-Lloyd d'avant 1929 non repris.
Deux-temps : distribution « aucune », huile « à choisir » (mélange). Puissances en ch DIN. Données indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .goliath import FAMILLES as FAMILLES_GOLIATH

E_ = "ESS"

FAMILLES = {
    "HANSA-2T-0.4": f("ATM", E_, 0.4, "AUCUNE", 2, 3500, 2500, "CHOISIR", 0.0, 2000),
    "HANSA-2T-0.5": f("ATM", E_, 0.5, "AUCUNE", 2, 3500, 2500, "CHOISIR", 0.0, 2000),
    "HANSA-L4-1.1": f("ATM", E_, 1.1, "NC", 4, 3800, 2400, "SAE30", 3.0, 3000),
    "HANSA-L6-1.7": f("ATM", E_, 1.7, "NC", 6, 3800, 2200, "SAE30", 4.0, 3000),
    "HANSA-L6-2.0": f("ATM", E_, 2.0, "NC", 6, 3800, 2200, "SAE30", 4.5, 3000),
    "HANSA-L6-3.5": f("ATM", E_, 3.5, "NC", 6, 3600, 2000, "SAE30", 6.0, 3000),
    "GOLIATH-1.1": FAMILLES_GOLIATH["GOLIATH-1.1"],
}
mg = SaisieMoteurs(FAMILLES, "Borgward", lambda fam: "Goliath" if fam == "GOLIATH-1.1" else "Borgward")
L = []
IND = "données indicatives (marque ancienne), à vérifier"

mg(L, "400", "400 / 500", "1", "1933-01", "1934-12", [("0.4 12", "HANSA-2T-0.4", 25), ("500 0.5 14", "HANSA-2T-0.5", 30)], portes=2, places=2, reservoir=20,
   remarques="Microvoiture à bicylindre deux temps arrière dérivée du Goliath Pionier, berline et cabriolet ; " + IND)
mg(L, "1100", "1100 (1934)", "1", "1934-01", "1939-12", [("1.1 28", "HANSA-L4-1.1", 65)], portes=2, places=4, reservoir=30,
   remarques="Berline, cabriolet et roadster, suspension à roues indépendantes ; " + IND)
mg(L, "1700", "1700", "1", "1934-01", "1939-12", [("1.7 L6 40", "HANSA-L6-1.7", 95), ("Sport 1.7 L6 50", "HANSA-L6-1.7", 100, {"fin": "1936-12"})],
   portes=2, places=4, reservoir=40, remarques="Six cylindres 1 640 cm³ ; 1700 Sport à deux carburateurs ; " + IND)
mg(L, "2000", "2000", "1", "1937-01", "1939-12", [("2.0 L6 50", "HANSA-L6-2.0", 115)], portes=4, places=5, reservoir=45,
   remarques="Commercialisée ensuite comme Borgward 2000 ; " + IND)
mg(L, "3500 Privat", "3500", "1", "1936-01", "1939-12", [("3.5 L6 90", "HANSA-L6-3.5", 220)], portes=4, places=5, reservoir=70,
   remarques="Grande routière, environ 200 exemplaires ; " + IND)
mg(L, "1100", "1100 (1958)", "1", "1958-08", "1961-08", [("1.1 40", "GOLIATH-1.1", 75), ("TS 1.1 55", "GOLIATH-1.1", 80)], portes=2, places=4, reservoir=33,
   remarques="Ex-Goliath 1100 (flat-4 à eau, traction), berline, break et coupé ; " + IND)

MOT = Motorisations("Borgward", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Hansa": L}
MOTEURS = MOT.moteurs()
