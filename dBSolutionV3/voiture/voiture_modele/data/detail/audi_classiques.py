"""Audi (modèles anciens) : générations, phases, motorisations (marché européen) et moteurs liés.
Audi Automobilwerke de Zwickau (1910-1932) : Type A à Type SS ; Auto Union (1932-1940) : Front UW, 225 et 920 ;
Audi d'après-guerre jusqu'aux A4 / A6 / A8 : F103 (60 à Super 90), 50, 80 (B1 à B4), 90 (B2 / B3), 100 (C1 à C4), 200 (C2 / C3),
Coupé (B2 / B3), Cabriolet, quattro, Sport quattro et V8 ; S4 (C4) dans la marque « Audi S ».
Familles reprises d'audi.py, volkswagen.py, volkswagen_classiques.py et porsche.py (mêmes codes et couples) ; quatre et cinq cylindres
anciens ajoutés. Puissances en ch DIN. Données des modèles d'avant-guerre indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from . import audi, volkswagen, volkswagen_classiques
from .porsche import FAMILLES as FAMILLES_PORSCHE

E_, D = "ESS", "DSL"
B = "COURROIE"

ANCIENS = {
    "AUDI-A-2.6": f("ATM", E_, 2.6, "NC", 4, 1800, 1000, "SAE30", 4.5, 2000),
    "AUDI-B-2.1": f("ATM", E_, 2.1, "NC", 4, 1800, 1000, "SAE30", 4.0, 2000),
    "AUDI-C-3.6": f("ATM", E_, 3.6, "NC", 4, 1800, 1000, "SAE30", 5.5, 2000),
    "AUDI-D-4.7": f("ATM", E_, 4.7, "NC", 4, 1700, 1000, "SAE30", 6.0, 2000),
    "AUDI-E-5.7": f("ATM", E_, 5.7, "NC", 4, 1600, 1000, "SAE30", 6.5, 2000),
    "AUDI-K-3.6": f("ATM", E_, 3.6, "NC", 4, 2400, 1400, "SAE30", 5.5, 3000),
    "AUDI-M-L6-4.7": f("ATM", E_, 4.7, "NC", 6, 3000, 1600, "SAE30", 7.0, 3000),
    "AUDI-R-L8-4.9": f("ATM", E_, 4.9, "NC", 8, 3300, 1600, "SAE30", 8.0, 3000),
    "AUDI-SS-L8-5.1": f("ATM", E_, 5.1, "NC", 8, 3300, 1600, "SAE30", 8.0, 3000),
    "WANDERER-L6-2.0": f("ATM", E_, 2.0, "NC", 6, 3500, 2000, "SAE30", 4.5, 3000),
    "AUDI-L6-2.3": f("ATM", E_, 2.3, "NC", 6, 3500, 2000, "SAE30", 5.0, 3000),
    "AUDI-L6-3.3": f("ATM", E_, 3.3, "NC", 6, 3200, 1800, "SAE30", 6.0, 3000),
}
NOUVEAUX = {
    "AUDI-F103-1.5": f("ATM", E_, 1.5, "CHAINE", 4, 4750, 2600, "20W50", 4.0, 7500),
    "AUDI-F103-1.7": f("ATM", E_, 1.7, "CHAINE", 4, 5000, 3000, "20W50", 4.0, 7500),
    "AUDI-F103-1.8": f("ATM", E_, 1.8, "CHAINE", 4, 5200, 3000, "20W50", 4.0, 7500),
    "AUDI-1.9": f("ATM", E_, 1.9, "CHAINE", 4, 5500, 4000, "20W50", 4.0, 7500),
    "AUDI-5C-2.0": f("ATM", E_, 2.0, B, 5, 5400, 3200, "15W40", 4.5, 15000),
    "AUDI-5C-2.1": f("ATM", E_, 2.1, B, 5, 5700, 4200, "15W40", 4.5, 15000),
    "AUDI-5C-2.2": f("ATM", E_, 2.2, B, 5, 5700, 3500, "15W40", 4.5, 15000),
    "AUDI-5C-2.3": f("ATM", E_, 2.3, B, 5, 5500, 4000, "15W40", 4.5, 15000),
    "AUDI-5C-2.3-20V": f("ATM", E_, 2.3, B, 5, 6300, 4500, "15W40", 4.5, 15000),
    "AUDI-5C-2.1T": f("TURBO", E_, 2.1, B, 5, 5500, 3500, "15W40", 5.0, 15000),
    "AUDI-5C-2.1-20VT": f("TURBO", E_, 2.1, B, 5, 6700, 3700, "10W40", 5.0, 10000),
    "AUDI-5C-2.0D": f("ATM", D, 2.0, B, 5, 4800, 3000, "15W40", 5.0, 7500),
    "AUDI-5C-2.0TD": f("TURBO", D, 2.0, B, 5, 4500, 2500, "15W40", 5.0, 7500),
    "AUDI-5C-2.4D": f("ATM", D, 2.4, B, 5, 4400, 2400, "15W40", 6.0, 7500),
    "AUDI-1.6D": f("ATM", D, 1.6, B, 4, 4800, 2300, "15W40", 3.5, 7500),
    "AUDI-1.6TD": f("TURBO", D, 1.6, B, 4, 4500, 2500, "15W40", 3.5, 7500),
    "AUDI-1.9TD": f("TURBO", D, 1.9, B, 4, 4200, 2400, "15W40", 4.0, 7500),
}
REPRIS = {k: audi.FAMILLES[k] for k in ("EA827-1.6", "EA827-1.8", "EA827-2.0", "5C-2.2T", "5C-2.5TDI", "V6-2.6", "V6-2.8", "V8-3.6", "V8-4.2", "EA188-1.9TDI")}
VW_CL = {k: volkswagen_classiques.FAMILLES[k] for k in ("EA827-1.3", "EA827-1.5")}
VW = {k: volkswagen.FAMILLES[k] for k in ("EA111-1.1", "EA111-1.3")}
PORSCHE = {"EA831-2.0": FAMILLES_PORSCHE["EA831-2.0"]}
FAMILLES = {**ANCIENS, **NOUVEAUX, **REPRIS, **VW_CL, **VW, **PORSCHE}


def motoriste(fam):
    if fam in VW or fam in VW_CL:
        return "Volkswagen"
    if fam == "WANDERER-L6-2.0":
        return "Wanderer"
    return "Audi"


mg = SaisieMoteurs(FAMILLES, "Audi", motoriste)
L, LS = [], []
IND = "données indicatives (marque ancienne), à vérifier"

# ---------------------------------------------------------------- Zwickau (1910-1940)
mg(L, "Type A", "Type A", "1", "1910-07", "1912-12", [("2.6 22", "AUDI-A-2.6", 100)], portes=4, places=4, reservoir=50, remarques="Première Audi (August Horch) ; 10/22 PS ; " + IND)
mg(L, "Type B", "Type B", "1", "1911-01", "1917-12", [("2.1 28", "AUDI-B-2.1", 95)], portes=4, places=4, reservoir=50, remarques="10/28 PS ; " + IND)
mg(L, "Type C", "Type C", "1", "1912-01", "1921-12", [("3.6 35", "AUDI-C-3.6", 160)], portes=4, places=4, reservoir=60,
   remarques="« Alpensieger », 14/35 PS, victoires à l'Alpenfahrt autrichienne ; " + IND)
mg(L, "Type D", "Type D", "1", "1912-01", "1920-12", [("4.7 45", "AUDI-D-4.7", 210)], portes=4, places=5, reservoir=70, remarques="18/45 PS ; " + IND)
mg(L, "Type E", "Type E", "1", "1913-01", "1924-12", [("5.7 55", "AUDI-E-5.7", 260)], portes=4, places=5, reservoir=75, remarques="22/55 PS ; " + IND)
mg(L, "Type G", "Type G", "1", "1914-01", "1926-12", [("2.1 22", "AUDI-B-2.1", 90)], portes=4, places=4, reservoir=45, remarques="8/22 PS ; " + IND)
mg(L, "Type K", "Type K", "1", "1922-01", "1925-12", [("3.6 50", "AUDI-K-3.6", 180)], portes=4, places=5, reservoir=65, remarques="14/50 PS, conduite à gauche ; " + IND)
mg(L, "Type M", "Type M", "1", "1924-01", "1928-12", [("4.7 L6 70", "AUDI-M-L6-4.7", 230)], portes=4, places=5, reservoir=80, remarques="18/70 PS, six cylindres ; " + IND)
mg(L, "Type R Imperator", "Type R", "1", "1927-01", "1929-12", [("4.9 L8 100", "AUDI-R-L8-4.9", 270)], portes=4, places=5, reservoir=90, remarques="19/100 PS, huit cylindres ; " + IND)
mg(L, "Type SS Zwickau", "Type SS", "1", "1929-01", "1932-12", [("5.1 L8 100", "AUDI-SS-L8-5.1", 280)], portes=4, places=5, reservoir=90,
   remarques="Huit cylindres d'origine Rickenbacker (période J.S. Rasmussen / DKW) ; " + IND)
mg(L, "Front UW", "Front", "1", "1933-01", "1938-12", [("2.0 L6 40", "WANDERER-L6-2.0", 110), ("225 2.3 L6 50", "AUDI-L6-2.3", 130, {"debut": "1935-01"})],
   portes=4, places=5, reservoir=50, remarques="Traction avant Auto Union, six cylindres Wanderer ; Front 225 à partir de 1935 ; " + IND)
mg(L, "920", "920", "1", "1938-01", "1940-12", [("3.3 L6 75", "AUDI-L6-3.3", 200)], portes=4, places=5, reservoir=65, remarques="Propulsion, six cylindres à arbre à cames en tête ; " + IND)

# ---------------------------------------------------------------- Audi F103 et 50
mg(L, "F103", "F103", "1", "1965-09", "1972-07",
   [("72 1.7 72", "AUDI-F103-1.7", 113, {"fin": "1968-12"}), ("60 1.5 55", "AUDI-F103-1.5", 107, {"debut": "1968-01"}), ("75 1.7 75", "AUDI-F103-1.7", 125, {"debut": "1968-01"}),
    ("80 1.7 80", "AUDI-F103-1.7", 128, {"debut": "1966-09", "fin": "1969-12"}), ("Super 90 1.8 90", "AUDI-F103-1.8", 147, {"debut": "1966-09"})],
   portes=4, places=5, reservoir=53, remarques="Première Audi d'après-guerre (moteur « Mitteldruck »), berline 2 et 4 portes, Variant ; noms selon la puissance")
mg(L, "50", "86", "1", "1974-08", "1978-07", [("1.1 50", "EA111-1.1", 77), ("1.1 60", "EA111-1.1", 83), ("1.3 60", "EA111-1.3", 95, {"debut": "1977-01"})],
   portes=3, places=4, reservoir=36, remarques="Citadine, jumelle de la Volkswagen Polo I")

# ---------------------------------------------------------------- Audi 80 / 90
mg(L, "80", "B1", "1", "1972-07", "1978-07",
   [("1.3 55", "EA827-1.3", 96), ("1.3 60", "EA827-1.3", 100), ("1.5 75", "EA827-1.5", 118, {"fin": "1975-07"}), ("1.5 85", "EA827-1.5", 121, {"fin": "1975-07"}),
    ("1.6 75", "EA827-1.6", 125, {"debut": "1975-08"}), ("1.6 85", "EA827-1.6", 127, {"debut": "1975-08"}), ("GT 1.5 100", "EA827-1.5", 132, {"debut": "1973-09", "fin": "1975-07"}),
    ("GTE 1.6 110", "EA827-1.6", 137, {"debut": "1975-08"})], portes=4, places=5, reservoir=45, remarques="Berline 2 et 4 portes ; restylage 1976")
mg(L, "80", "B2", "1", "1978-08", "1986-08",
   [("1.3 55", "EA827-1.3", 96), ("1.3 60", "EA827-1.3", 100), ("1.6 75", "EA827-1.6", 125), ("1.6 85", "EA827-1.6", 127, {"fin": "1983-07"}),
    ("1.8 75", "EA827-1.8", 140, {"debut": "1983-08"}), ("1.8 90", "EA827-1.8", 145, {"debut": "1983-08"}), ("GTE 1.8 112", "EA827-1.8", 160, {"debut": "1983-08"}),
    ("quattro 2.1 136", "AUDI-5C-2.1", 180, {"debut": "1982-11", "fin": "1984-07"}), ("1.6 D 54", "AUDI-1.6D", 100), ("1.6 TD 70", "AUDI-1.6TD", 133, {"debut": "1982-01"})],
   portes=4, places=5, reservoir=60, remarques="Berline 2 et 4 portes ; quattro à partir de 1982")
mg(L, "80", "B3", "1", "1986-09", "1991-08",
   [("1.6 75", "EA827-1.6", 125), ("1.8 75", "EA827-1.8", 140), ("1.8 90", "EA827-1.8", 145), ("1.8 112", "EA827-1.8", 160), ("2.0 113", "EA827-2.0", 165, {"debut": "1988-01"}),
    ("1.6 TD 80", "AUDI-1.6TD", 155)], portes=4, places=5, reservoir=68, remarques="Berline aérodynamique galvanisée ; quattro")
mg(L, "80", "B4", "1", "1991-09", "1996-01",
   [("1.6 101", "EA827-1.6", 140), ("2.0 90", "EA827-2.0", 148), ("2.0 115", "EA827-2.0", 170), ("2.3 133", "AUDI-5C-2.3", 186, {"fin": "1994-07"}),
    ("2.6 V6 150", "V6-2.6", 225), ("2.8 V6 174", "V6-2.8", 245), ("1.9 TD 75", "AUDI-1.9TD", 150), ("1.9 TDI 90", "EA188-1.9TDI", 210)],
   portes=4, places=5, reservoir=66, remarques="Berline et Avant (1992), remplacée par l'A4 ; RS2 dans la marque Audi RS")
mg(L, "90", "B2", "1", "1984-09", "1987-08", [("2.0 115", "AUDI-5C-2.0", 154), ("2.2 136", "AUDI-5C-2.2", 186)], portes=4, places=5, reservoir=68,
   remarques="Version cinq cylindres haut de gamme de la 80 ; quattro")
mg(L, "90", "B3", "1", "1987-09", "1991-08", [("2.0 115", "AUDI-5C-2.0", 154), ("2.3 136", "AUDI-5C-2.3", 190), ("2.3 20V 170", "AUDI-5C-2.3-20V", 220, {"debut": "1988-09"})],
   portes=4, places=5, reservoir=68, remarques="Berline ; quattro")

# ---------------------------------------------------------------- Audi 100 / 200
mg(L, "100", "C1", "1", "1968-11", "1976-07",
   [("1.8 80", "AUDI-F103-1.8", 135), ("1.8 90", "AUDI-F103-1.8", 147), ("LS 1.8 100", "AUDI-F103-1.8", 153), ("Coupé S 1.9 115", "AUDI-1.9", 160, {"debut": "1970-01"})],
   portes=4, places=5, reservoir=58, remarques="Berline 2 et 4 portes et 100 Coupé S")
mg(L, "100", "C2", "1", "1976-08", "1982-07",
   [("1.6 85", "EA827-1.6", 127), ("2.0 115", "EA831-2.0", 165, {"fin": "1978-12"}), ("2.1 115", "AUDI-5C-2.1", 165, {"debut": "1977-01"}), ("2.1 136", "AUDI-5C-2.1", 180, {"debut": "1977-01"}),
    ("2.0 D 70", "AUDI-5C-2.0D", 123, {"debut": "1978-08"})], portes=4, places=5, reservoir=60, remarques="Berline et Avant à hayon ; premier cinq cylindres essence (1977)")
mg(L, "100", "C3", "1", "1982-09", "1990-11",
   [("1.8 75", "EA827-1.8", 140), ("1.8 90", "EA827-1.8", 145), ("2.0 115", "AUDI-5C-2.0", 154), ("2.2 136", "AUDI-5C-2.2", 186, {"fin": "1987-12"}),
    ("2.3 136", "AUDI-5C-2.3", 190, {"debut": "1988-01"}), ("2.0 D 70", "AUDI-5C-2.0D", 123), ("2.0 TD 87", "AUDI-5C-2.0TD", 172), ("2.5 TDI 120", "5C-2.5TDI", 265, {"debut": "1989-12"})],
   portes=4, places=5, reservoir=80, remarques="Berline aérodynamique (Cx 0,30), Avant, carrosserie galvanisée (1985), quattro")
mg(L, "100", "C4", "1", "1990-12", "1994-06",
   [("2.0 101", "EA827-2.0", 157), ("2.0 115", "EA827-2.0", 170), ("2.3 133", "AUDI-5C-2.3", 186), ("2.8 V6 174", "V6-2.8", 245), ("2.4 D 82", "AUDI-5C-2.4D", 164),
    ("2.5 TDI 115", "5C-2.5TDI", 265)], portes=4, places=5, reservoir=80, remarques="Berline et Avant, rebaptisée A6 (C4) en 1994")
mg(L, "200", "C2", "1", "1979-09", "1982-07", [("2.1 136", "AUDI-5C-2.1", 180), ("Turbo 2.1 170", "AUDI-5C-2.1T", 265)], portes=4, places=5, reservoir=60,
   remarques="Haut de gamme de la 100 C2")
mg(L, "200", "C3", "1", "1983-09", "1991-12", [("Turbo 2.1 182", "AUDI-5C-2.1T", 252), ("Turbo 2.2 165", "AUDI-5C-2.1T", 250, {"debut": "1985-01"}),
                                               ("20V Turbo 2.2 220", "5C-2.2T", 309, {"debut": "1989-01"})], portes=4, places=5, reservoir=80, remarques="Berline et Avant, quattro")

# ---------------------------------------------------------------- Coupés, cabriolet, quattro, V8
mg(L, "Coupé", "B2", "1", "1980-09", "1988-08", [("1.8 90", "EA827-1.8", 145, {"debut": "1983-08"}), ("1.9 115", "AUDI-5C-2.0", 154, {"fin": "1984-07"}),
                                               ("2.0 115", "AUDI-5C-2.0", 154, {"debut": "1984-08"}), ("GT 2.2 136", "AUDI-5C-2.2", 186)], portes=3, places=4, reservoir=68,
   remarques="Coupé GT, base 80 B2 ; quattro à partir de 1984")
mg(L, "Coupé", "8B", "1", "1988-10", "1996-01", [("2.0 115", "EA827-2.0", 170), ("2.3 133", "AUDI-5C-2.3", 186), ("2.3 20V 170", "AUDI-5C-2.3-20V", 220),
                                               ("2.6 V6 150", "V6-2.6", 225, {"debut": "1992-09"}), ("2.8 V6 174", "V6-2.8", 245, {"debut": "1991-09"})],
   portes=2, places=4, reservoir=68, remarques="Coupé ; S2 dans la marque Audi S")
mg(L, "Cabriolet", "B4", "1", "1991-05", "2000-08", [("1.8 125", "EA827-1.8", 168, {"debut": "1997-08"}), ("2.0 115", "EA827-2.0", 170), ("2.3 133", "AUDI-5C-2.3", 186, {"fin": "1994-07"}),
                                                    ("2.6 V6 150", "V6-2.6", 225), ("2.8 V6 174", "V6-2.8", 245), ("1.9 TDI 90", "EA188-1.9TDI", 210, {"debut": "1995-09"})],
   portes=2, places=4, reservoir=66, remarques="Cabriolet 4 places sur base 80 B4 / Coupé B3")
mg(L, "quattro", "Ur-quattro", "1", "1980-03", "1991-05", [("2.1 Turbo 200", "AUDI-5C-2.1T", 285, {"fin": "1987-12"}), ("2.2 Turbo 200", "5C-2.2T", 285, {"debut": "1988-01", "fin": "1989-09"}),
                                                          ("2.2 20V Turbo 220", "5C-2.2T", 309, {"debut": "1989-10"})], portes=2, places=4, reservoir=90,
   remarques="« Ur-quattro », première transmission intégrale permanente de série d'Audi")
mg(L, "Sport quattro", "Sport quattro", "1", "1984-01", "1985-12", [("2.1 20V Turbo 306", "AUDI-5C-2.1-20VT", 350)], portes=2, places=2, reservoir=90,
   remarques="Homologation Groupe B (214 exemplaires), base de la Sport quattro S1 de rallye")
mg(L, "V8", "D11", "1", "1988-10", "1994-03", [("3.6 V8 250", "V8-3.6", 340), ("4.2 V8 280", "V8-4.2", 400, {"debut": "1991-09"})], portes=4, places=5, reservoir=80,
   remarques="Berline de luxe quattro (et version longue), remplacée par l'A8")

# ---------------------------------------------------------------- Audi S (anciennes)
mg(LS, "S4", "C4", "1", "1991-09", "1994-06", [("S4 2.2 turbo 230", "5C-2.2T", 350), ("S4 4.2 V8 280", "V8-4.2", 400, {"debut": "1992-09"})], portes=4, places=5, reservoir=80,
   remarques="Berline et Avant sur base 100 C4, quattro ; devenue S6 en 1994")

MOT = Motorisations("Audi", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LS)
DETAIL = {"Audi": L, "Audi S": LS}
MOTEURS = MOT.moteurs()
