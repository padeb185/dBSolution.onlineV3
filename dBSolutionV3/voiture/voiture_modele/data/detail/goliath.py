"""Goliath : générations, phases, motorisations (marché européen) et moteurs liés.
Marque du groupe Borgward (Brême) : Pionier (triporteur, 1931-1934), GP 700 et GP 900 (deux-temps, injection directe dès 1951),
1100 (flat-4 refroidi par eau, 1957-1958, devenu Hansa 1100) et Goli (triporteur utilitaire). Deux-temps : distribution « aucune »,
huile « à choisir » (mélange). Puissances en ch DIN. Données indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"


def dt(l, n, rpm, nmrpm):
    return f("ATM", E_, l, "AUCUNE", n, rpm, nmrpm, "CHOISIR", 0.0, 3000)


FAMILLES = {
    "GOLIATH-2T-0.2": dt(0.2, 1, 3500, 2500), "GOLIATH-2T-0.4": dt(0.4, 2, 4000, 2800),
    "GOLIATH-2T-0.7": dt(0.69, 2, 3800, 2800), "GOLIATH-2T-0.9": dt(0.89, 2, 4000, 3000),
    "GOLIATH-1.1": f("ATM", E_, 1.1, "NC", 4, 4250, 2500, "20W50", 3.5, 5000, a="PLAT"),
}
mg = SaisieMoteurs(FAMILLES, "Goliath", lambda fam: "Goliath")
L = []
IND = "données indicatives (marque ancienne), à vérifier"

mg(L, "Pionier", "Pionier", "1", "1931-01", "1934-12", [("0.2 2T 6", "GOLIATH-2T-0.2", 12)], portes=2, places=2, reservoir=12,
   remarques="Petite voiture à trois roues (carrosserie simili-cuir) et triporteur ; " + IND)
mg(L, "GP 700", "GP 700", "1", "1950-01", "1957-12", [("0.7 2T 24", "GOLIATH-2T-0.7", 50), ("E 0.7 2T 29", "GOLIATH-2T-0.7", 54, {"debut": "1951-01"})],
   portes=2, places=4, reservoir=30, remarques="Berline, break et coupé ; première injection directe d'essence en série (GP 700 E) ; " + IND)
mg(L, "GP 900", "GP 900", "1", "1955-01", "1957-12", [("0.9 2T 40", "GOLIATH-2T-0.9", 70)], portes=2, places=4, reservoir=30, remarques="Berline et break à injection ; " + IND)
mg(L, "1100", "1100", "1", "1957-01", "1958-12", [("1.1 40", "GOLIATH-1.1", 75), ("TS 1.1 55", "GOLIATH-1.1", 80)], portes=2, places=4, reservoir=33,
   remarques="Berline, break et coupé, flat-4 à eau ; poursuivie comme Hansa 1100 (1958-1961) ; " + IND)
mg(L, "Goli", "Goli", "1", "1955-01", "1961-12", [("0.4 2T 16", "GOLIATH-2T-0.4", 30)], portes=2, places=2, reservoir=20, remarques="Triporteur utilitaire ; " + IND)

MOT = Motorisations("Goliath", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Goliath": L}
MOTEURS = MOT.moteurs()
