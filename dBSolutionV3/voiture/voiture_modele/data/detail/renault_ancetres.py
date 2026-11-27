"""Renault (ancêtres et modèles anciens) : générations, phases, motorisations (marché européen) et moteurs liés.
Avant-guerre (Billancourt) : Voiturette Type A, Type AG (« taxi de la Marne »), Type AX, 40 CV, NN, Monasix, Vivasix, Reinastella,
Nervastella, Primaquatre, Celtaquatre et Juvaquatre ; après-guerre : 4CV, Frégate, Colorale, Dauphine, Floride, Caravelle, Estafette,
8, 10, 16, 6, 12, 15, 17, 14, 20, 30, Fuego et Rodeo ; puis Avantime, Vel Satis, Modus, Wind, Latitude et Twizy
(modèles absents de renault.py et renault_classiques.py). Moteurs repris de renault_classiques.py (mêmes familles, codes et couples)
via sa table ; moteurs d'avant-guerre, Frégate et « X » (Française de Mécanique) ajoutés.
Puissances en ch. Données d'avant-guerre et des années 1950-1970 indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from . import renault_classiques as rc

E_ = "ESS"


def anc(l, n, rpm, nmrpm, q, a="EN_LIGNE"):
    return f("ATM", E_, l, "NC", n, rpm, nmrpm, "SAE30", q, 3000, a=a)


ANCIENS = {
    "RENAULT-DEDION-0.27": anc(0.27, 1, 1500, 1000, 1.0),
    "RENAULT-AG-1.2": anc(1.2, 2, 1200, 800, 2.5),
    "RENAULT-AX-1.1": anc(1.1, 2, 1300, 800, 2.5),
    "RENAULT-40CV-9.1": anc(9.1, 6, 2200, 1200, 12.0),
    "RENAULT-NN-0.95": anc(0.95, 4, 2600, 1600, 2.5),
    "RENAULT-L6-1.5": anc(1.5, 6, 3000, 1600, 4.0),
    "RENAULT-L6-3.2": anc(3.2, 6, 3000, 1600, 6.0),
    "RENAULT-L8-7.1": anc(7.1, 8, 2800, 1400, 10.0),
    "RENAULT-L8-4.8": anc(4.8, 8, 3200, 1600, 8.0),
    "RENAULT-2.1": anc(2.1, 4, 3000, 1600, 4.5),
    "RENAULT-1.5": anc(1.5, 4, 3200, 1800, 3.5),
    "RENAULT-1.0": anc(1.0, 4, 3500, 2000, 2.5),
    "RENAULT-668-2.0": f("ATM", E_, 2.0, "CHAINE", 4, 4000, 2200, "20W50", 5.0, 5000),
    "RENAULT-ETENDARD-2.1": f("ATM", E_, 2.1, "CHAINE", 4, 4000, 2400, "20W50", 5.0, 5000),
    "RENAULT-85-2.4": anc(2.4, 4, 2800, 1600, 5.0),
    "X5J-1.2": f("ATM", E_, 1.2, "CHAINE", 4, 6000, 3000, "15W40", 3.5, 7500),
    "X6J-1.4": f("ATM", E_, 1.4, "CHAINE", 4, 6000, 3000, "15W40", 3.5, 7500),
    "TWIZY-EV": electrique(),
}
REPRIS = ("BILL-0.75", "BILL-0.85", "CLEON-0.95", "CLEON-1.1", "CLEON-1.3", "CLEON-1.4", "A-TYPE", "A5L", "J6R", "J7T", "J8S", "J8ST", "PRV-2.7",
          "F7R", "F4RT", "L7X", "G9T", "D4F", "K4J", "K4M", "K9K", "D4FT", "M9R", "V4Y", "P9X", "V9X")
FAMILLES = {**ANCIENS, **{k: rc.FAMILLES[k] for k in REPRIS}}


def motoriste(fam):
    if fam in ("V4Y", "V9X"):
        return "Nissan"
    if fam == "P9X":
        return "Isuzu"
    if fam in ("X5J-1.2", "X6J-1.4"):
        return "Française de Mécanique"
    return "Renault"


mg = SaisieMoteurs(FAMILLES, "Renault", motoriste)
L = []
IND = "données indicatives (modèle ancien), à vérifier"


def t(nom, *surcharges):
    """Variante reprise de la table de renault_classiques.py (même famille et couple)."""
    v = rc.TABLE[nom]
    fam, nm = v[-3], v[-1]
    return (nom, fam, nm, *surcharges)


# ---------------------------------------------------------------- avant-guerre
mg(L, "Voiturette Type A", "Type A", "1", "1898-12", "1899-12", [("0.27 2", "RENAULT-DEDION-0.27", 6)], portes=0, places=2, reservoir=8,
   remarques="Première Renault (Louis Renault, prise directe), monocylindre De Dion ; " + IND)
mg(L, "Type AG", "AG", "1", "1905-01", "1910-12", [("1.2 9", "RENAULT-AG-1.2", 40)], portes=4, places=4, reservoir=30,
   remarques="Taxi parisien, célèbre « taxi de la Marne » (1914) ; " + IND)
mg(L, "Type AX", "AX", "1", "1908-01", "1914-12", [("1.1 8", "RENAULT-AX-1.1", 38)], portes=2, places=2, reservoir=25, remarques="Petite voiture bicylindre ; " + IND)
mg(L, "40 CV", "40 CV", "1", "1921-01", "1928-12", [("9.1 L6 140", "RENAULT-40CV-9.1", 450)], portes=4, places=5, reservoir=120,
   remarques="Voiture présidentielle et de record (Montlhéry 1926) ; " + IND)
mg(L, "NN", "NN", "1", "1924-01", "1930-12", [("0.95 17", "RENAULT-NN-0.95", 45)], portes=4, places=4, reservoir=30, remarques="6 CV populaire, torpédo et berline ; " + IND)
mg(L, "Monasix", "Monasix", "1", "1927-01", "1931-12", [("1.5 L6 30", "RENAULT-L6-1.5", 75)], portes=4, places=4, reservoir=40, remarques="Petite six cylindres ; " + IND)
mg(L, "Vivasix", "Vivasix", "1", "1927-01", "1934-12", [("3.2 L6 55", "RENAULT-L6-3.2", 160)], portes=4, places=5, reservoir=55, remarques="Six cylindres ; " + IND)
mg(L, "Reinastella", "Reinastella", "1", "1929-01", "1933-12", [("7.1 L8 100", "RENAULT-L8-7.1", 380)], portes=4, places=6, reservoir=100,
   remarques="Limousine de prestige huit cylindres ; " + IND)
mg(L, "Nervastella", "Nervastella", "1", "1930-01", "1937-12", [("4.8 L8 110", "RENAULT-L8-4.8", 280)], portes=4, places=5, reservoir=90,
   remarques="Huit cylindres, dont Nervasport (records de Montlhéry) ; " + IND)
mg(L, "Primaquatre", "Primaquatre", "1", "1931-01", "1941-12", [("2.1 46", "RENAULT-2.1", 120)], portes=4, places=5, reservoir=50, remarques="Berline et cabriolet ; " + IND)
mg(L, "Celtaquatre", "Celtaquatre", "1", "1934-01", "1938-12", [("1.5 34", "RENAULT-1.5", 80)], portes=2, places=4, reservoir=40, remarques="Berline aérodynamique ; " + IND)
mg(L, "Juvaquatre", "Juvaquatre", "1", "1937-12", "1960-12", [("1.0 24", "RENAULT-1.0", 55, {"fin": "1955-12"}), ("845 26", "BILL-0.85", 55, {"debut": "1956-01"})],
   portes=2, places=4, reservoir=33, remarques="Berline puis break et fourgonnette (Dauphinoise, 1956) ; " + IND)

# ---------------------------------------------------------------- années 1940-1960
mg(L, "4CV", "R1060", "1", "1947-08", "1961-07", [("0.76 17", "BILL-0.75", 39, {"fin": "1950-12"}), ("747 21", "BILL-0.75", 45, {"debut": "1951-01"})],
   portes=4, places=4, reservoir=28, remarques="Première Renault produite à plus d'un million d'exemplaires, moteur arrière ; " + IND)
mg(L, "Frégate", "R1100", "1", "1951-01", "1960-12", [("2.0 58", "RENAULT-668-2.0", 130), ("Étendard 2.1 77", "RENAULT-ETENDARD-2.1", 157, {"debut": "1956-01"})],
   portes=4, places=6, reservoir=58, remarques="Berline, Domaine et Manoir (break), Transfluide ; " + IND)
mg(L, "Colorale", "R2090", "1", "1950-01", "1956-12", [("2.4 48", "RENAULT-85-2.4", 140)], portes=5, places=6, reservoir=60,
   remarques="Break, Prairie et Savane (4x4) ; " + IND)
mg(L, "Dauphine", "R1090", "1", "1956-03", "1968-12", [("845 30", "BILL-0.85", 57), ("Gordini 845 37", "BILL-0.85", 64, {"debut": "1957-10"}),
                                                      ("1093 845 55", "BILL-0.85", 70, {"debut": "1962-01", "fin": "1963-12"})],
   portes=4, places=4, reservoir=32, remarques="Berline à moteur arrière, Ondine, Gordini et 1093 ; " + IND)
mg(L, "Floride", "R1092", "1", "1959-01", "1963-12", [("845 40", "BILL-0.85", 66), ("S 956 51", "CLEON-0.95", 69, {"debut": "1962-07"})], portes=2, places=4, reservoir=32,
   remarques="Coupé et cabriolet Frua ; " + IND)
mg(L, "Caravelle", "R1131", "1", "1962-07", "1968-12", [("956 51", "CLEON-0.95", 69, {"fin": "1963-12"}), ("1.1 55", "CLEON-1.1", 83, {"debut": "1964-01"})],
   portes=2, places=4, reservoir=32, remarques="Évolution de la Floride, coupé et cabriolet ; " + IND)
mg(L, "Estafette", "R2130", "1", "1959-01", "1980-12", [("845 30", "BILL-0.85", 57, {"fin": "1962-12"}), ("1.1 43", "CLEON-1.1", 78, {"debut": "1963-01"}),
                                                       ("1.3 48", "CLEON-1.3", 88, {"debut": "1977-01"})], portes=4, places=8, reservoir=45,
   remarques="Fourgon et minibus à traction avant ; " + IND)
mg(L, "8", "R1130", "1", "1962-06", "1973-12", [t("956 44"), t("1.1 47", {"debut": "1965-01"}), ("Gordini 1.1 95", "CLEON-1.1", 99, {"debut": "1964-09", "fin": "1966-12"}),
                                               ("Gordini 1.3 103", "CLEON-1.3", 117, {"debut": "1967-01", "fin": "1970-12"})],
   portes=4, places=5, reservoir=38, remarques="Berline à moteur arrière, 8 Major et 8 Gordini ; " + IND)
mg(L, "10", "R1190", "1", "1965-09", "1971-12", [t("1.1 48"), ("1.3 52", "CLEON-1.3", 92, {"debut": "1969-01"})], portes=4, places=5, reservoir=38,
   remarques="Version allongée de la 8 ; " + IND)
mg(L, "16", "R1150", "1", "1965-01", "1980-12", [("1.5 55", "A-TYPE", 106), ("TS 1.6 83", "A-TYPE", 120, {"debut": "1968-01"}), ("TX 1.6 93", "A-TYPE", 128, {"debut": "1973-09"})],
   portes=5, places=5, reservoir=50, remarques="Première berline bicorps à hayon, voiture de l'année 1966 ; " + IND)
mg(L, "6", "R1180", "1", "1968-10", "1980-12", [t("845 34"), t("1.1 47", {"debut": "1970-01"})], portes=5, places=5, reservoir=40, remarques="Berline à hayon sur base 4 ; " + IND)
mg(L, "12", "R1170", "1", "1969-10", "1980-12", [("1.3 54", "CLEON-1.3", 93), ("TS 1.3 60", "CLEON-1.3", 94, {"debut": "1972-01"}),
                                                ("Gordini 1.6 125", "A-TYPE", 137, {"debut": "1970-09", "fin": "1974-12"})],
   portes=4, places=5, reservoir=47, remarques="Berline et break, Gordini ; reprise par Dacia (1300) ; " + IND)
mg(L, "15", "R1300", "1", "1971-10", "1979-12", [("1.3 60", "CLEON-1.3", 94), ("TS 1.6 90", "A-TYPE", 125)], portes=2, places=4, reservoir=55, remarques="Coupé ; " + IND)
mg(L, "17", "R1310", "1", "1971-10", "1979-12", [("TL 1.6 90", "A-TYPE", 125), ("TS 1.6 108", "A-TYPE", 134)], portes=2, places=4, reservoir=55,
   remarques="Coupé et découvrable, 17 Gordini (1974) ; " + IND)
mg(L, "14", "R1210", "1", "1976-06", "1983-12", [("1.2 57", "X5J-1.2", 87), ("TS 1.4 70", "X6J-1.4", 104, {"debut": "1979-01"})], portes=5, places=5, reservoir=50,
   remarques="Berline à hayon, moteur « X » de la Française de Mécanique (PSA-Renault) ; " + IND)
mg(L, "20", "R1270", "1", "1975-10", "1984-12", [("1.6 90", "A-TYPE", 125), t("2.0 104", {"debut": "1977-01"}), ("2.2 115", "J7T", 179, {"debut": "1981-01"}),
                                                t("2.1 D 66", {"debut": "1979-01"})], portes=5, places=5, reservoir=67, remarques="Grande berline à hayon ; " + IND)
mg(L, "30", "R1275", "1", "1975-03", "1984-12", [("V6 2.7 128", "PRV-2.7", 206), t("V6 2.7 144", {"debut": "1979-01"}), t("2.1 TD 85", {"debut": "1982-01"})],
   portes=5, places=5, reservoir=67, remarques="Haut de gamme à V6 PRV ; " + IND)
mg(L, "Fuego", "R136", "1", "1980-03", "1986-12", [t("1.4 64"), ("1.6 96", "A-TYPE", 130), ("2.0 110", "J6R", 163), ("Turbo 1.6 132", "A5L", 200, {"debut": "1983-01"}),
                                                  t("2.1 TD 88", {"debut": "1982-01"})], portes=3, places=4, reservoir=57,
   remarques="Coupé sur base 18, première voiture diesel turbo de grande série en France ; " + IND)
mg(L, "Rodeo", "Rodeo", "1", "1970-01", "1987-12", [t("845 34"), t("1.1 47", {"debut": "1972-01"})], portes=0, places=4, reservoir=30,
   remarques="Véhicule de loisirs découvrable (ACL, Teilhol) sur base 4 / 6 ; " + IND)

# ---------------------------------------------------------------- années 1990-2010
mg(L, "Avantime", "DE0", "1", "2001-11", "2003-12", [t("2.0 T 165"), t("3.0 V6 207"), t("2.2 dCi 150", {"debut": "2002-09"})], portes=3, places=4, reservoir=80,
   remarques="Coupé-monospace construit par Matra (Romorantin)")
mg(L, "Vel Satis", "BJ0", "1", "2002-03", "2009-12", [t("2.0 T 165"), t("3.5 V6 240"), t("2.2 dCi 150"), t("3.0 dCi 180"), t("2.0 dCi 175", {"debut": "2008-01"})],
   portes=5, places=5, reservoir=80, remarques="Grande routière haut de gamme ; restylage 2005")
mg(L, "Modus", "JP0", "1", "2004-09", "2012-12", [t("1.2 16v 75"), t("1.4 16v 98"), t("1.6 16v 110"), t("1.5 dCi 85"), t("1.2 TCe 100", {"debut": "2007-12"})],
   portes=5, places=5, reservoir=49, remarques="Minispace, Grand Modus (2008)")
mg(L, "Wind", "E4M", "1", "2010-06", "2013-06", [t("1.2 TCe 100"), t("1.6 133")], portes=2, places=2, reservoir=40, remarques="Roadster à toit rigide pivotant, base Twingo II")
mg(L, "Latitude", "L70", "1", "2010-09", "2015-12", [t("2.0 dCi 150"), t("2.0 dCi 175"), t("3.0 dCi 235")], portes=4, places=5, reservoir=66,
   remarques="Berline haut de gamme (Renault Samsung SM5)")
mg(L, "Twizy", "MAM", "1", "2012-03", "2023-09", [("45 Électrique 5", "TWIZY-EV", 33, {"batterie": 6}), ("80 Électrique 17", "TWIZY-EV", 57, {"batterie": 6})],
   portes=2, places=2, reservoir=0, remarques="Quadricycle électrique biplace en tandem (Twizy 45 sans permis) ; production transférée chez Mobilize (2023)")

MOT = Motorisations("Renault", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Renault": L}
MOTEURS = MOT.moteurs()
