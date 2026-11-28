"""IFA (Industrieverband Fahrzeugbau, RDA) : générations, phases, motorisations (marché est-allemand) et moteurs liés.
Voitures : F8 et F9 (deux-temps DKW reconstruits à Zwickau / Eisenach), P70 (Zwickau). Camions : H3A, W50 et L60 (Ludwigsfelde).
Moteurs deux-temps repris de dkw.py (familles). Deux-temps : distribution « aucune », huile « à choisir » (mélange). Puissances en ch DIN.
Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .dkw import FAMILLES as FAMILLES_DKW

D = "DSL"
FAMILLES = {
    "DKW-2T-0.7": FAMILLES_DKW["DKW-2T-0.7"], "DKW-2T-0.9": FAMILLES_DKW["DKW-2T-0.9"],
    "IFA-EM4-6.0D": f("ATM", D, 6.0, "NC", 4, 2000, 1300, "15W40", 12.0, 5000),
    "IFA-4VD-6.6D": f("ATM", D, 6.6, "NC", 4, 2300, 1400, "15W40", 13.0, 10000),
    "IFA-6VD-9.8D": f("TURBO", D, 9.8, "NC", 6, 2300, 1400, "15W40", 18.0, 10000),
}
mg = SaisieMoteurs(FAMILLES, "IFA")
L = []
IND = "données indicatives"

mg(L, "F8", "F8", "1", "1949-01", "1955-12", [("0.7 20", "DKW-2T-0.7", 50)], portes=2, places=4, reservoir=30, remarques="DKW F8 reconstruite à Zwickau (Horch / Audi) ; " + IND)
mg(L, "F9", "F9", "1", "1950-01", "1956-12", [("0.9 28", "DKW-2T-0.9", 62, {"fin": "1953-12"}), ("0.9 30", "DKW-2T-0.9", 65, {"debut": "1954-01"})], portes=2, places=4, reservoir=40,
   remarques="Trois cylindres deux temps, Zwickau puis Eisenach (devenue Wartburg 311) ; " + IND)
mg(L, "P70", "P70", "1", "1955-01", "1959-12", [("0.7 22", "DKW-2T-0.7", 52)], portes=2, places=4, reservoir=30,
   remarques="Première caisse en Duroplast, prédécesseur du Trabant ; berline, break et coupé ; " + IND)
mg(L, "H3A", "H3A", "1", "1952-01", "1959-12", [("Diesel 6.0 80", "IFA-EM4-6.0D", 330)], portes=2, places=2, reservoir=120, remarques="Camion 3 t (Werdau) ; " + IND)
mg(L, "W50", "W50", "1", "1965-01", "1990-12", [("Diesel 6.6 125", "IFA-4VD-6.6D", 480)], portes=2, places=3, reservoir=150,
   remarques="Camion 5 t (Ludwigsfelde), plus de 570 000 exemplaires ; " + IND)
mg(L, "L60", "L60", "1", "1987-01", "1990-12", [("Diesel 9.8 Turbo 180", "IFA-6VD-9.8D", 700)], portes=2, places=3, reservoir=200, remarques="Successeur du W50 ; " + IND)

MOT = Motorisations("IFA", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"IFA": L}
MOTEURS = MOT.moteurs()
