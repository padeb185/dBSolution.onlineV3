"""Abarth : générations, phases, motorisations (marché européen) et moteurs liés.
Fiat-Abarth anciennes (595/695, 850/1000 TC, 124 et 131 Rally, Ritmo), Grande Punto / Punto Evo, 500 / 595 / 695,
124 Spider, 500e et 600e. L'Autobianchi A112 Abarth relève de la marque Autobianchi.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom.
Données des modèles anciens indicatives."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

E_ = "ESS"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


FAMILLES = {
    "Fiat-0.6": f("ATM", E_, 0.6, "CHAINE", 2, 5500, 3500, "20W50", 2.5, 5000),
    "Fiat100-0.85": f("ATM", E_, 0.85, "CHAINE", 4, 6200, 4000, "20W50", 3.5, 5000),
    "Fiat100-1.0": f("ATM", E_, 1.0, "CHAINE", 4, 6000, 4500, "20W50", 3.5, 5000),
    "FiatTC-1.8": f("ATM", E_, 1.8, "COURROIE", 4, 6500, 5200, "15W40", 4.5, 10000),
    "FiatTC-2.0": f("ATM", E_, 2.0, "COURROIE", 4, 5900, 3500, "15W40", 4.5, 10000),
    "FiatTC-2.0-16V": f("ATM", E_, 2.0, "COURROIE", 4, 6400, 3600, "15W40", 4.5, 10000),
    "TJet-1.4": f("TURBO", E_, 1.4, "COURROIE", 4, 5500, 2500, "5W40", 3.0, 15000),
    "MultiAir-1.4T": f("TURBO", E_, 1.4, "COURROIE", 4, 5500, 2250, "5W40", 3.5, 15000),
    "Abarth-EV-500": electrique(), "Abarth-EV-600": electrique(),
}

mg = SaisieMoteurs(FAMILLES, "Abarth")
L = []

# ---------------------------------------------------------------- Fiat-Abarth anciennes
mg(L, "595 / 695", "Fiat 500 (110F)", "1", "1963-09", "1971-12",
   [("595 27", "Fiat-0.6", 40, {"fin": "1970-12"}), ("595 SS 32", "Fiat-0.6", 44, {"debut": "1964-01"}),
    ("695 30", "Fiat-0.6", 45, {"debut": "1964-06"}), ("695 SS 38", "Fiat-0.6", 54, {"debut": "1964-06"})],
   portes=2, places=4, reservoir=21, remarques="Fiat Nuova 500 préparée par Abarth ; dates et puissances indicatives")
mg(L, "850 / 1000 TC", "Fiat 600 (100)", "1", "1961-03", "1970-12",
   [("850 TC 52", "Fiat100-0.85", 63), ("850 TC SS 55", "Fiat100-0.85", 66, {"debut": "1962-01"}),
    ("1000 TC 60", "Fiat100-1.0", 78, {"debut": "1962-09"})], portes=2, places=4, reservoir=27,
   remarques="Berlina Corsa sur base Fiat 600 ; TC = Turismo Competizione ; données indicatives")
mg(L, "124 Abarth Rally", "124 Sport Spider", "1", "1972-11", "1975-12", [("124 Rally 128", "FiatTC-1.8", 159)],
   portes=2, places=2, reservoir=50, remarques="Spider d'homologation Groupe 4")
mg(L, "131 Abarth Rally", "131", "1", "1976-04", "1978-06", [("131 Abarth 140", "FiatTC-2.0-16V", 172)],
   portes=2, places=4, reservoir=50, remarques="Berline 2 portes d'homologation Groupe 4 (Fiat 131 Abarth)")
mg(L, "Ritmo Abarth", "138", "1", "1981-03", "1987-12",
   [("Ritmo 125 TC 125", "FiatTC-2.0", 172, {"fin": "1982-12"}), ("Ritmo 130 TC 130", "FiatTC-2.0", 176, {"debut": "1983-01"})],
   portes=3, places=5, reservoir=50, remarques="Fiat Ritmo Abarth 3 portes")

# ---------------------------------------------------------------- Punto
mg(L, "Grande Punto", "199", "1", "2007-09", "2010-06",
   [("Grande Punto 1.4 T-Jet 155", "TJet-1.4", 230), ("Grande Punto esseesse 180", "TJet-1.4", 270, {"debut": "2008-09"})],
   portes=3, places=5, reservoir=45, remarques="Abarth Grande Punto ; kit esseesse")
mg(L, "Grande Punto", "199", "2", "2010-09", "2012-09",
   [("Punto Evo 1.4 MultiAir 165", "MultiAir-1.4T", 250), ("Punto Evo esseesse 180", "MultiAir-1.4T", 270, {"debut": "2011-06"})],
   portes=3, places=5, reservoir=45, remarques="Abarth Punto Evo")
mg(L, "Grande Punto", "199", "3", "2012-10", "2014-12",
   [("Punto 1.4 T-Jet 165", "TJet-1.4", 250), ("Punto Supersport 180", "TJet-1.4", 270)], portes=3, places=5,
   reservoir=45, remarques="Abarth Punto (dernière série)")

# ---------------------------------------------------------------- 500 / 595 / 695
mg(L, "500 / 595 / 695", "312", "1", "2008-06", "2016-05",
   [("500 135", "TJet-1.4", 206, {"fin": "2012-12"}), ("500 esseesse 160", "TJet-1.4", 230, {"debut": "2009-03", "fin": "2012-12"}),
    ("500C 140", "TJet-1.4", 206, {"debut": "2010-03", "fin": "2012-12"}),
    ("695 Tributo Ferrari 180", "TJet-1.4", 250, {"debut": "2009-09", "fin": "2012-12"}),
    ("695 Edizione Maserati 180", "TJet-1.4", 250, {"debut": "2012-09", "fin": "2013-12"}),
    ("595 Turismo 160", "TJet-1.4", 230, {"debut": "2012-09"}), ("595 Competizione 160", "TJet-1.4", 230, {"debut": "2012-09"}),
    ("595 140", "TJet-1.4", 206, {"debut": "2013-01"}), ("695 Biposto 190", "TJet-1.4", 250, {"debut": "2014-06"})],
   portes=3, places=4, reservoir=35, remarques="Berline 3 portes et 500C/595C/695C (toit toile)")
mg(L, "500 / 595 / 695", "312", "2", "2016-06", "2024-12",
   [("595 145", "TJet-1.4", 206, {"fin": "2019-08"}), ("595 165", "TJet-1.4", 230, {"debut": "2019-09"}),
    ("595 Turismo 165", "TJet-1.4", 230), ("595 Pista 165", "TJet-1.4", 230, {"debut": "2017-06"}),
    ("595 Competizione 180", "TJet-1.4", 250), ("595 Esseesse 180", "TJet-1.4", 250, {"debut": "2019-06"}),
    ("695 Rivale 180", "TJet-1.4", 250, {"debut": "2017-06", "fin": "2020-12"}),
    ("695 XSR Yamaha 180", "TJet-1.4", 250, {"debut": "2017-09", "fin": "2018-12"}),
    ("695 70° Anniversario 180", "TJet-1.4", 250, {"debut": "2019-03", "fin": "2019-12"}),
    ("695 Tributo 131 Rally 180", "TJet-1.4", 250, {"debut": "2021-06", "fin": "2021-12"}),
    ("695 180", "TJet-1.4", 250, {"debut": "2022-06"}), ("695 75° Anniversario 180", "TJet-1.4", 250, {"debut": "2024-06"})],
   portes=3, places=4, reservoir=35, remarques="Restylage 2016 : 595/695 et versions C (toit toile) ; fin des thermiques en Europe fin 2024")
mg(L, "124 Spider", "348", "1", "2016-04", "2019-12",
   [("124 Spider 170", "MultiAir-1.4T", 250), ("124 GT 170", "MultiAir-1.4T", 250, {"debut": "2018-03"})],
   portes=2, places=2, reservoir=45, remarques="Roadster (base Mazda MX-5 ND) ; GT à hard-top carbone")

# ---------------------------------------------------------------- électriques
mg(L, "500e", "332", "1", "2023-05", None,
   [("500e Scorpionissima 155", "Abarth-EV-500", 235, el(37, fin="2024-06")), ("500e Turismo 155", "Abarth-EV-500", 235, el(37, debut="2023-09"))],
   portes=3, places=4, reservoir=0, remarques="Berline 3 portes et Cabriolet électriques (batterie 42 kWh brute)")
mg(L, "600e", "600", "1", "2024-10", "2025-12",
   [("600e 240", "Abarth-EV-600", 345, el(51)), ("600e Scorpionissima 280", "Abarth-EV-600", 345, el(51))],
   portes=5, places=5, reservoir=0, remarques="SUV compact électrique (batterie 54 kWh brute) ; Scorpionissima limitée à 1 949 ex.")
mg(L, "600e", "600", "2", "2026-01", None,
   [("600e Turismo 240", "Abarth-EV-600", 345, el(51)), ("600e Competizione 280", "Abarth-EV-600", 345, el(51))],
   portes=5, places=5, reservoir=0, remarques="Millésime 2026 : Turismo et Competizione remplacent 600e et Scorpionissima")

MOT = Motorisations("Abarth", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Abarth": L}
MOTEURS = MOT.moteurs()
