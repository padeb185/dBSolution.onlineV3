"""Alpine : générations, phases, motorisations (marché européen) et moteurs liés.
A106, A108, A110 Berlinette, A310 (4 cylindres et V6), V6 GT / V6 Turbo, A610, A110 (2017-2026), A290, A390.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom.
Moteurs d'origine Renault rattachés au motoriste Alpine ; données des modèles anciens indicatives."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

E_ = "ESS"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


FAMILLES = {
    "Billancourt-0.75": f("ATM", E_, 0.75, "CHAINE", 4, 6000, 4000, "20W50", 2.5, 5000),
    "Ventoux-0.85": f("ATM", E_, 0.85, "CHAINE", 4, 5500, 3500, "20W50", 3.0, 5000),
    "Ventoux-0.9": f("ATM", E_, 0.9, "CHAINE", 4, 6000, 4000, "20W50", 3.0, 5000),
    "Sierra-1.0": f("ATM", E_, 1.0, "CHAINE", 4, 6200, 4000, "20W50", 3.5, 5000),
    "Sierra-1.1": f("ATM", E_, 1.1, "CHAINE", 4, 6500, 4500, "20W50", 3.5, 5000),
    "Cleon-1.3": f("ATM", E_, 1.3, "CHAINE", 4, 6500, 5000, "20W50", 4.0, 5000),
    "Cleon-Alu-1.6": f("ATM", E_, 1.6, "CHAINE", 4, 6000, 5000, "20W50", 4.0, 7500),
    "PRV-2.7": f("ATM", E_, 2.7, "CHAINE", 6, 6000, 3500, "15W40", 6.0, 10000, a="V"),
    "PRV-2.85": f("ATM", E_, 2.85, "CHAINE", 6, 5750, 3750, "15W40", 6.0, 10000, a="V"),
    "PRV-2.5T": f("TURBO", E_, 2.5, "CHAINE", 6, 5750, 2500, "15W40", 6.0, 10000, a="V"),
    "PRV-3.0T": f("TURBO", E_, 3.0, "CHAINE", 6, 5750, 2900, "15W40", 6.0, 10000, a="V"),
    "M5P-1.8T": f("TURBO", E_, 1.8, "CHAINE", 4, 6000, 2000, "5W30", 5.5, 20000),
    "AMPR-EV": electrique(), "A390-EV": electrique(),
}

mg = SaisieMoteurs(FAMILLES, "Alpine")
L = []

# ---------------------------------------------------------------- années 1950-1990
mg(L, "A106", "A106", "1", "1955-07", "1961-12",
   [("A106 0.75 21", "Billancourt-0.75", 39), ("A106 Mille Miles 0.75 43", "Billancourt-0.75", 50, {"debut": "1956-06"})],
   portes=2, places=2, reservoir=30, remarques="Coupé et Cabriolet sur base Renault 4CV")
mg(L, "A108", "A108", "1", "1958-10", "1965-12",
   [("A108 0.85 37", "Ventoux-0.85", 58), ("A108 Gordini 0.9 55", "Ventoux-0.9", 64, {"debut": "1960-01"}),
    ("A108 1.0 70", "Sierra-1.0", 80, {"debut": "1962-06"})], portes=2, places=2, reservoir=38,
   remarques="Coupé, Cabriolet, Berlinette Tour de France (base Dauphine)")
mg(L, "A110", "A110 Berlinette", "1", "1962-06", "1977-07",
   [("A110 956 51", "Sierra-1.0", 70, {"fin": "1965-12"}), ("A110 1100 66", "Sierra-1.1", 85, {"debut": "1964-01", "fin": "1970-12"}),
    ("A110 1100 95", "Sierra-1.1", 92, {"debut": "1966-01", "fin": "1970-12"}),
    ("A110 1300 G 120", "Cleon-1.3", 125, {"debut": "1967-01", "fin": "1971-12"}),
    ("A110 1600 S 138", "Cleon-Alu-1.6", 145, {"debut": "1970-01", "fin": "1973-12"}),
    ("A110 1600 SC 140", "Cleon-Alu-1.6", 150, {"debut": "1974-01"})], portes=2, places=2, reservoir=38,
   remarques="Berlinette (et Cabriolet GT4) ; puissances et dates indicatives")
mg(L, "A310", "A310", "1", "1971-04", "1976-09", [("A310 1600 127", "Cleon-Alu-1.6", 145)], portes=2, places=4, reservoir=60,
   remarques="Coupé 2+2, 4 cylindres")
mg(L, "A310", "A310", "2", "1976-10", "1984-12", [("A310 V6 150", "PRV-2.7", 205)], portes=2, places=4, reservoir=60,
   remarques="Coupé 2+2 V6 PRV ; Pack GT (1982) non détaillé")
mg(L, "V6 GT / V6 Turbo", "D501", "1", "1985-01", "1991-12",
   [("V6 GT 160", "PRV-2.85", 228), ("V6 Turbo 200", "PRV-2.5T", 290),
    ("V6 Turbo catalysé 185", "PRV-2.5T", 285, {"debut": "1988-01"})], portes=2, places=4, reservoir=72,
   remarques="Alpine GTA ; Le Mans (1990-1991)")
mg(L, "A610", "D502", "1", "1991-01", "1995-07", [("A610 Turbo 250", "PRV-3.0T", 350)], portes=2, places=4, reservoir=80,
   remarques="Coupé 2+2 V6 Turbo")

# ---------------------------------------------------------------- A110 (2017)
mg(L, "A110", "AS1", "1", "2017-12", "2021-12",
   [("A110 Première Édition 252", "M5P-1.8T", 320, {"fin": "2018-06"}), ("A110 Pure 252", "M5P-1.8T", 320),
    ("A110 Légende 252", "M5P-1.8T", 320), ("A110 S 292", "M5P-1.8T", 320, {"debut": "2019-03"})],
   portes=2, places=2, reservoir=45, remarques="Berlinette à moteur central")
mg(L, "A110", "AS1", "2", "2022-01", "2026-07",
   [("A110 252", "M5P-1.8T", 320), ("A110 GT 300", "M5P-1.8T", 340), ("A110 S 300", "M5P-1.8T", 340, {"fin": "2024-05"}),
    ("A110 R 300", "M5P-1.8T", 340, {"debut": "2022-11"}), ("A110 GTS 300", "M5P-1.8T", 340, {"debut": "2024-06"}),
    ("A110 R Ultime 345", "M5P-1.8T", 420, {"debut": "2024-10"})], portes=2, places=2, reservoir=45,
   remarques="Restylage 2022 ; fin de production mi-2026 (remplacée par l'A110 électrique)")

# ---------------------------------------------------------------- électriques
mg(L, "A290", "AmpR Small", "1", "2025-01", None,
   [("A290 GT 180", "AMPR-EV", 285, el(52)), ("A290 GT Performance 220", "AMPR-EV", 300, el(52)),
    ("A290 GTS 220", "AMPR-EV", 300, el(52))], portes=5, places=5, reservoir=0,
   remarques="Citadine sportive électrique (base Renault 5 E-Tech) ; finition Collection (2026)")
mg(L, "A390", "AmpR Medium", "1", "2026-01", None,
   [("A390 GT 400", "A390-EV", 661, el(89)), ("A390 GTS 470", "A390-EV", 824, el(89))], portes=5, places=5,
   reservoir=0, remarques="SUV coupé électrique à 3 moteurs")

MOT = Motorisations("Alpine", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Alpine": L}
MOTEURS = MOT.moteurs()
