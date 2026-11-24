"""Bugatti : générations, versions et moteurs liés.
Type 13 « Brescia », Type 35, Type 41 Royale, Type 57, Type 101, EB110, Veyron, Chiron et dérivés (Divo, Centodieci,
La Voiture Noire, Bolide, W16 Mistral, Brouillard), Tourbillon.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom.
Modèles anciens : puissances et couples indicatifs. Séries limitées et exemplaires uniques indiqués en remarque."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


FAMILLES = {
    "Bugatti-1.5-16V": f("ATM", E_, 1.5, "NC", 4, 4500, 3000, "20W50", 5.0, 2000),
    "Bugatti-2.0-I8": f("ATM", E_, 2.0, "NC", 8, 5500, 4000, "20W50", 9.0, 2000),
    "Bugatti-2.3-I8C": f("TURBO", E_, 2.3, "NC", 8, 5300, 4000, "20W50", 9.0, 2000),
    "Bugatti-12.7-I8": f("ATM", E_, 12.7, "NC", 8, 1700, 1000, "20W50", 23.0, 2000),
    "Bugatti-3.3-I8": f("ATM", E_, 3.3, "NC", 8, 5000, 3500, "20W50", 10.0, 3000),
    "Bugatti-3.3-I8C": f("TURBO", E_, 3.3, "NC", 8, 5500, 4000, "20W50", 10.0, 3000),
    "EB110-3.5-V12": f("TURBO", E_, 3.5, "CHAINE", 12, 8000, 3750, "10W60", 14.0, 10000, a="V"),
    "W16-8.0": f("TURBO", E_, 8.0, "CHAINE", 16, 6000, 2200, "0W40", 23.0, 15000, a="W"),
    "V16-8.3-PHEV": f("HYB_E", E_, 8.3, "CHAINE", 16, 9000, 7000, "0W40", 23.0, 15000, a="V"),
}

mg = SaisieMoteurs(FAMILLES, "Bugatti")
L = []

mg(L, "Type 13", "Brescia", "1", "1910-01", "1926-12", [("Type 13 Brescia 1.5 40", "Bugatti-1.5-16V", 80)], portes=0, places=2,
   reservoir=40, remarques="Voiturette ; Brescia 16 soupapes (1920) ; dates et puissance indicatives")
mg(L, "Type 35", "Type 35", "1", "1924-08", "1930-12",
   [("Type 35 2.0 90", "Bugatti-2.0-I8", 150), ("Type 35B 2.3 140", "Bugatti-2.3-I8C", 220, {"debut": "1927-01"})], portes=0, places=2,
   reservoir=100, remarques="Grand Prix biplace ; T35B à compresseur")
mg(L, "Type 41 Royale", "Type 41", "1", "1929-01", "1933-12", [("Type 41 Royale 12.7 300", "Bugatti-12.7-I8", 1000)], portes=4,
   places=4, reservoir=190, remarques="6 exemplaires, carrosseries diverses")
mg(L, "Type 57", "Type 57", "1", "1934-01", "1940-12",
   [("Type 57 3.3 135", "Bugatti-3.3-I8", 250), ("Type 57S 3.3 175", "Bugatti-3.3-I8", 270, {"debut": "1936-01", "fin": "1938-12"}),
    ("Type 57SC 3.3 200", "Bugatti-3.3-I8C", 300, {"debut": "1936-01", "fin": "1938-12"}), ("Type 57C 3.3 160", "Bugatti-3.3-I8C", 280, {"debut": "1937-01"})],
   portes=2, places=4, reservoir=100, remarques="Ventoux, Stelvio, Galibier, Atalante ; 57SC Atlantic (4 ex.)")
mg(L, "Type 101", "Type 101", "1", "1951-01", "1956-12", [("Type 101 3.3 135", "Bugatti-3.3-I8", 250)], portes=2, places=4,
   reservoir=100, remarques="Dernière Bugatti de Molsheim avant la renaissance (8 ex.)")
mg(L, "EB110", "EB110", "1", "1991-09", "1995-09",
   [("EB110 GT 560", "EB110-3.5-V12", 611), ("EB110 SS 612", "EB110-3.5-V12", 650, {"debut": "1992-10"})], portes=2, places=2,
   reservoir=120, remarques="Campogalliano ; V12 quadriturbo, transmission intégrale")
mg(L, "Veyron", "16.4", "1", "2005-09", "2011-12",
   [("Veyron 16.4 1001", "W16-8.0", 1250), ("Veyron Super Sport 1200", "W16-8.0", 1500, {"debut": "2010-08"})], portes=2, places=2,
   reservoir=100, remarques="Coupé ; 300 ex. (dont Super Sport 48 ex.)")
mg(L, "Veyron", "16.4", "Grand Sport", "2009-04", "2015-02",
   [("Veyron Grand Sport 1001", "W16-8.0", 1250), ("Veyron Grand Sport Vitesse 1200", "W16-8.0", 1500, {"debut": "2012-03"})],
   portes=2, places=2, reservoir=100, remarques="Targa ; 150 ex.")
mg(L, "Chiron", "Chiron", "1", "2016-09", "2024-06",
   [("Chiron 1500", "W16-8.0", 1600), ("Chiron Sport 1500", "W16-8.0", 1600, {"debut": "2018-03"}),
    ("Chiron Pur Sport 1500", "W16-8.0", 1600, {"debut": "2020-03"}), ("Chiron Super Sport 300+ 1600", "W16-8.0", 1600, {"debut": "2019-09", "fin": "2021-12"}),
    ("Chiron Super Sport 1600", "W16-8.0", 1600, {"debut": "2021-06"}), ("Chiron Profilée 1500", "W16-8.0", 1600, {"debut": "2022-01", "fin": "2022-12"})],
   portes=2, places=2, reservoir=100, remarques="Coupé ; 500 ex.")
mg(L, "Divo", "Chiron", "Divo", "2019-06", "2021-12", [("Divo 1500", "W16-8.0", 1600)], portes=2, places=2, reservoir=100,
   remarques="40 ex.")
mg(L, "La Voiture Noire", "Chiron", "Voiture Noire", "2021-06", "2021-12", [("La Voiture Noire 1500", "W16-8.0", 1600)], portes=2,
   places=2, reservoir=100, remarques="Exemplaire unique")
mg(L, "Centodieci", "Chiron", "Centodieci", "2021-09", "2022-12", [("Centodieci 1600", "W16-8.0", 1600)], portes=2, places=2,
   reservoir=100, remarques="Hommage à l'EB110 (10 ex.)")
mg(L, "Bolide", "Chiron", "Bolide", "2024-01", "2025-12", [("Bolide 1600", "W16-8.0", 1600)], portes=2, places=2, reservoir=100,
   remarques="Voiture de piste (40 ex.), non homologuée sur route")
mg(L, "W16 Mistral", "Chiron", "Mistral", "2024-09", "2025-12", [("W16 Mistral 1600", "W16-8.0", 1600)], portes=2, places=2,
   reservoir=100, remarques="Roadster (99 ex.), dernière Bugatti W16 de série")
mg(L, "Brouillard", "Chiron", "Brouillard", "2026-01", "2026-06", [("Brouillard 1600", "W16-8.0", 1600)], portes=2, places=2,
   reservoir=100, remarques="Exemplaire unique (Programme Solitaire), livraison 2026")
mg(L, "Tourbillon", "Tourbillon", "1", "2026-06", None, [("Tourbillon 1800", "V16-8.3-PHEV", 1600, ph(25, 100))], portes=2, places=2,
   remarques="V16 atmosphérique 8,3 l + 3 moteurs électriques ; 250 ex. ; couple système et réservoir indicatifs")

MOT = Motorisations("Bugatti", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Bugatti": L}
MOTEURS = MOT.moteurs()
