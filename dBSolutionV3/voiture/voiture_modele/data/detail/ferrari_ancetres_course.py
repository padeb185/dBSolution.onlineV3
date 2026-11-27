"""Ferrari (ancêtres, modèles anciens manquants et voitures de course) : générations, phases, motorisations et moteurs liés.
Ancêtre : Auto Avio Costruzioni 815 (1940). Routières absentes de ferrari.py : 340 / 342 / 375 America, 250 Europa, 410 et 400 Superamerica,
500 Superfast, 208 et Mondial. Course (non homologuées route) : 125 S, 166 MM, 250 Testa Rossa, 250 LM, 330 P4, 512 S, 312 PB, F40 LM,
333 SP, FXX, 599XX, FXX K, 488 GT3 / GTE, 296 GT3 et 499P. Familles reprises de ferrari.py (mêmes codes et couples) ; V12 Colombo 1.5,
V12 Lampredi, flat-12 3.0 et moteurs de course ajoutés. Puissances en ch. Données indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .ferrari import FAMILLES as FAMILLES_FERRARI

E_ = "ESS"
C = "CHAINE"


def v12(l, rpm, nmrpm, q=12.0, t="ATM"):
    return f(t, E_, l, C, 12, rpm, nmrpm, "20W50", q, 3000, a="V")


NOUVEAUX = {
    "AAC-L8-1.5": f("ATM", E_, 1.5, "NC", 8, 5500, 4000, "SAE30", 6.0, 2000),
    "V12-1.5": v12(1.5, 7000, 5500, 8.0),
    "LAMPREDI-3.0": v12(3.0, 6300, 4800),
    "LAMPREDI-4.1": v12(4.1, 6600, 5000),
    "LAMPREDI-4.5": v12(4.5, 7000, 5500),
    "LAMPREDI-5.0": v12(5.0, 6500, 5000),
    "V12-5.0": v12(5.0, 6500, 4800),
    "V12-5.0-COURSE": v12(5.0, 8500, 5500, 14.0),
    "B12-3.0-COURSE": f("ATM", E_, 3.0, C, 12, 10800, 9000, "10W60", 10.0, 1000, a="PLAT"),
    "V12-4.0-333": v12(4.0, 11000, 9000, 12.0),
    "V8-2.0": f("ATM", E_, 2.0, "COURROIE", 8, 6800, 5000, "20W50", 10.0, 5000, a="V"),
    "F163-3.0-GT3": f("TURBO", E_, 3.0, C, 6, 7000, 5000, "5W40", 8.0, 5000, a="V"),
    "F163-3.0-499P": f("HYB_TE", E_, 3.0, C, 6, 8000, 6000, "5W40", 8.0, 2000, a="V"),
}
REPRIS = {k: FAMILLES_FERRARI[k] for k in ("V12-2.0", "V12-3.0", "V12-3.3", "V12-4.0", "V8-3.0", "V8-3.2", "V8-3.4", "V8T-2.9", "F140-6.0", "F140-6.3",
                                           "F140-6.3-HY", "F154-3.9")}
FAMILLES = {**NOUVEAUX, **REPRIS}
mg = SaisieMoteurs(FAMILLES, "Ferrari", lambda fam: "Alfa Romeo" if fam == "AAC-L8-1.5" else "Ferrari")
L = []
IND = "données indicatives, à vérifier"
COURSE = "voiture de course, non homologuée route ; " + IND

# ---------------------------------------------------------------- ancêtre et routières anciennes
mg(L, "815", "AAC 815", "1", "1940-01", "1940-12", [("1.5 L8 72", "AAC-L8-1.5", 105)], portes=0, places=2, reservoir=80,
   remarques="Auto Avio Costruzioni 815 d'Enzo Ferrari (Mille Miglia 1940), deux exemplaires, huit cylindres sur base Fiat ; " + IND)
mg(L, "340 America", "340", "1", "1950-01", "1952-12", [("4.1 V12 220", "LAMPREDI-4.1", 300)], portes=2, places=2, reservoir=150,
   remarques="Coupés et spiders (Vignale, Touring), V12 Lampredi ; " + IND)
mg(L, "342 America", "342", "1", "1952-01", "1953-12", [("4.1 V12 200", "LAMPREDI-4.1", 290)], portes=2, places=2, reservoir=150, remarques="Version routière, 6 exemplaires ; " + IND)
mg(L, "375 America", "375", "1", "1953-01", "1955-12", [("4.5 V12 300", "LAMPREDI-4.5", 320)], portes=2, places=2, reservoir=150, remarques="Grand tourisme de luxe ; " + IND)
mg(L, "250 Europa", "250 Europa", "1", "1953-10", "1954-12", [("3.0 V12 200", "LAMPREDI-3.0", 240)], portes=2, places=2, reservoir=100,
   remarques="Première 250, V12 Lampredi (250 Europa GT à moteur Colombo en 1954) ; " + IND)
mg(L, "410 Superamerica", "410", "1", "1955-10", "1959-12", [("5.0 V12 340", "LAMPREDI-5.0", 420)], portes=2, places=2, reservoir=100, remarques="Coupés Pinin Farina ; " + IND)
mg(L, "400 Superamerica", "400", "1", "1960-01", "1964-12", [("4.0 V12 340", "V12-4.0", 360)], portes=2, places=2, reservoir=100,
   remarques="Coupé Aerodinamico et cabriolet, V12 Colombo ; " + IND)
mg(L, "500 Superfast", "500", "1", "1964-01", "1966-12", [("5.0 V12 400", "V12-5.0", 480)], portes=2, places=2, reservoir=100, remarques="Coupé de grand luxe, 36 exemplaires ; " + IND)
mg(L, "208", "F106", "1", "1980-01", "1982-12", [("GTB 2.0 V8 155", "V8-2.0", 177)], portes=2, places=2, reservoir=74,
   remarques="208 GTB / GTS, version 2 litres de la 308 (marché italien) ; GTB Turbo dans ferrari.py ; " + IND)
mg(L, "Mondial", "F108", "1", "1980-01", "1993-12",
   [("8 3.0 V8 214", "V8-3.0", 243, {"fin": "1982-12"}), ("Quattrovalvole 3.0 V8 240", "V8-3.0", 260, {"debut": "1982-01", "fin": "1985-08"}),
    ("3.2 V8 270", "V8-3.2", 304, {"debut": "1985-09", "fin": "1988-12"}), ("t 3.4 V8 300", "V8-3.4", 324, {"debut": "1989-01"})],
   portes=2, places=4, reservoir=87, remarques="Coupé et cabriolet 2+2 à moteur central ; " + IND)

# ---------------------------------------------------------------- voitures de course
mg(L, "125 S", "125 S", "1", "1947-03", "1947-12", [("1.5 V12 118", "V12-1.5", 110)], portes=0, places=2, reservoir=75,
   remarques="Première Ferrari, V12 Colombo 1.5 ; " + COURSE)
mg(L, "166 MM", "166 MM", "1", "1948-01", "1953-12", [("2.0 V12 140", "V12-2.0", 160), ("2.0 V12 160", "V12-2.0", 170, {"debut": "1950-01"})], portes=0, places=2, reservoir=90,
   remarques="Barchetta Touring, victoires aux Mille Miglia et au Mans (1949) ; " + COURSE)
mg(L, "250 Testa Rossa", "250 TR", "1", "1957-11", "1961-12", [("3.0 V12 300", "V12-3.0", 294)], portes=0, places=2, reservoir=140,
   remarques="Barquette Scaglietti « ponton », victoires au Mans (1958, 1960, 1961) ; " + COURSE)
mg(L, "250 LM", "250 LM", "1", "1963-11", "1965-12", [("3.3 V12 320", "V12-3.3", 314)], portes=2, places=2, reservoir=130, remarques="Moteur central, victoire au Mans 1965 ; " + COURSE)
mg(L, "330 P4", "330 P4", "1", "1967-01", "1967-12", [("4.0 V12 450", "V12-4.0", 431)], portes=2, places=2, reservoir=140,
   remarques="Prototype, triplé de Daytona 1967 ; " + COURSE)
mg(L, "512 S", "512", "1", "1970-01", "1971-12", [("S 5.0 V12 550", "V12-5.0-COURSE", 510), ("M 5.0 V12 610", "V12-5.0-COURSE", 520, {"debut": "1970-10"})],
   portes=2, places=2, reservoir=120, remarques="Sport-prototype Groupe 5 (512 S puis 512 M) ; " + COURSE)
mg(L, "312 PB", "312 PB", "1", "1971-01", "1973-12", [("3.0 Flat-12 440", "B12-3.0-COURSE", 320)], portes=0, places=2, reservoir=120,
   remarques="Barquette, championne du monde des marques 1972 ; " + COURSE)
mg(L, "F40 LM", "F120", "C", "1989-01", "1996-12", [("2.9 V8 Biturbo 720", "V8T-2.9", 700)], portes=2, places=1, reservoir=120, remarques="Version course de la F40 (IMSA, BPR) ; " + COURSE)
mg(L, "333 SP", "333 SP", "1", "1994-01", "2003-12", [("4.0 V12 650", "V12-4.0-333", 450)], portes=0, places=1, reservoir=90,
   remarques="Barquette IMSA WSC / Sportscar, V12 dérivé de la F1 ; " + COURSE)
mg(L, "FXX", "F140", "C", "2005-01", "2007-12", [("6.3 V12 800", "F140-6.3", 765)], portes=2, places=1, reservoir=110,
   remarques="Programme « Corse Clienti » sur base Enzo, 30 exemplaires ; " + COURSE)
mg(L, "599XX", "F141", "C", "2009-01", "2011-12", [("6.0 V12 730", "F140-6.0", 686)], portes=2, places=1, reservoir=110, remarques="Programme « Corse Clienti » sur base 599 ; " + COURSE)
mg(L, "FXX K", "F150", "C", "2015-01", "2017-12", [("6.3 V12 Hybrid 1050", "F140-6.3-HY", 900)], portes=2, places=1, reservoir=85,
   remarques="Programme « XX » sur base LaFerrari, hybride HY-KERS ; " + COURSE)
mg(L, "488 GT3 / GTE", "F142M", "C", "2016-01", "2022-12", [("GT3 3.9 V8 Biturbo 600", "F154-3.9", 760), ("GTE 3.9 V8 Biturbo 670", "F154-3.9", 760)],
   portes=2, places=1, reservoir=120, remarques="GT3 (clients) et GTE (WEC, victoires au Mans en GTE Pro) ; puissances selon réglementation ; " + COURSE)
mg(L, "296 GT3", "F171", "C", "2023-01", None, [("3.0 V6 Biturbo 600", "F163-3.0-GT3", 710)], portes=2, places=1, reservoir=120,
   remarques="GT3 sans hybridation ; puissance selon balance of performance ; " + COURSE)
mg(L, "499P", "499P", "1", "2023-01", None, [("3.0 V6 Biturbo Hybrid 680", "F163-3.0-499P", 700)], portes=2, places=1, reservoir=90,
   remarques="Hypercar LMH (WEC), victoires au Mans 2023, 2024 et 2025 ; puissance cumulée réglementée ; " + COURSE)

MOT = Motorisations("Ferrari", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Ferrari": L}
MOTEURS = MOT.moteurs()
