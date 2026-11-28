"""LAG (Lambert Achiel Genk, Belgique) : générations, phases, motorisations (marché européen) et moteurs liés.
Carrossier-constructeur d'autocars : Galaxy (1982-1998) et Panoramic (1983-1995), sur châssis DAF, Volvo ou MAN ; repris par EOS (1995)
puis VDL. Moteur DAF repris de jonckheere.py (même code). Nombre de portes : 2 (portes de service) ; places : capacité indicative.
Puissances en ch. Désignations et données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .jonckheere import FAMILLES as FAMILLES_JK

FAMILLES = {
    "DAF-DKX-11.6": FAMILLES_JK["DAF-DKX-11.6"],
}
mg = SaisieMoteurs(FAMILLES, "DAF")
L = []
IND = "autocar ; moteur selon châssis, données indicatives"
mg(L, "Galaxy", "Galaxy", "1", "1982-01", "1998-12", [("Diesel 11.6 Turbo 280", "DAF-DKX-11.6", 1050)], portes=2, places=50, reservoir=400, remarques=IND)
mg(L, "Panoramic", "Panoramic", "1", "1983-01", "1995-12", [("Diesel 11.6 Turbo 280", "DAF-DKX-11.6", 1050)], portes=2, places=50, reservoir=400, remarques="Autocar à pavillon surélevé ; " + IND)

MOT = Motorisations("DAF", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"LAG": L}
MOTEURS = MOT.moteurs()
