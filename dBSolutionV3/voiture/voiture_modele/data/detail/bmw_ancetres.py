"""BMW (ancêtres et modèles anciens) : générations, phases, motorisations (marché européen) et moteurs liés.
Avant-guerre (Eisenach) : 3/15 (DA-2 à DA-4, suite de la Dixi), 3/20, 303, 309, 315, 319, 326, 320 / 321, 327, 328 et 335 ;
après-guerre (Munich) : 501, 502, 503, 507, 3200 CS, Isetta, 600, 700, « Neue Klasse » 1500-2000, série 02 (1602 à 2002 turbo),
2000 C / CS, grandes berlines E3 (2500 à 3.3 Li) et coupés E9 (2800 CS à 3.0 CSL) ; absents de bmw.py.
Quatre et six cylindres M10 / M30 repris de bmw.py (mêmes familles, codes et couples) via sa table ; moteurs anciens, V8 « 501/502 »,
monocylindre Isetta et bicylindres 600 / 700 ajoutés. Puissances en ch DIN. Données d'avant 1970 indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from . import bmw

E_ = "ESS"
C = "CHAINE"


def anc(l, n, rpm, nmrpm, q, a="EN_LIGNE"):
    return f("ATM", E_, l, "NC", n, rpm, nmrpm, "SAE30", q, 3000, a=a)


ANCIENS = {
    "BMW-0.75": anc(0.75, 4, 3000, 2000, 2.0),
    "BMW-0.8": anc(0.8, 4, 3500, 2000, 2.0),
    "BMW-L6-1.2": anc(1.2, 6, 4000, 2500, 3.5),
    "BMW-0.85": anc(0.85, 4, 4000, 2500, 2.5),
    "BMW-L6-1.5": anc(1.5, 6, 4000, 2500, 3.5),
    "BMW-L6-1.9": anc(1.9, 6, 4000, 2500, 4.0),
    "BMW-M78-2.0": anc(2.0, 6, 3750, 2000, 4.5),
    "BMW-328-2.0": anc(2.0, 6, 5000, 4000, 4.5),
    "BMW-L6-3.5": anc(3.5, 6, 3500, 2000, 6.0),
    "BMW-501-2.0": f("ATM", E_, 2.0, C, 6, 4400, 2500, "20W50", 4.5, 5000),
    "BMW-V8-2.6": f("ATM", E_, 2.6, C, 8, 4800, 2500, "20W50", 6.0, 5000, a="V"),
    "BMW-V8-3.2": f("ATM", E_, 3.2, C, 8, 5600, 3800, "20W50", 6.5, 5000, a="V"),
    "BMW-1C-0.25": f("ATM", E_, 0.25, "NC", 1, 5800, 4500, "20W50", 1.25, 3000),
    "BMW-1C-0.3": f("ATM", E_, 0.3, "NC", 1, 5200, 4600, "20W50", 1.25, 3000),
    "BMW-2C-0.6": f("ATM", E_, 0.6, "NC", 2, 4500, 2800, "20W50", 2.0, 3000, a="PLAT"),
    "BMW-2C-0.7": f("ATM", E_, 0.7, "NC", 2, 5000, 3400, "20W50", 2.0, 3000, a="PLAT"),
    "M10-1.5": f("ATM", E_, 1.5, C, 4, 5700, 3000, "15W40", 4.0, 10000),
    "M10-2.0T": f("TURBO", E_, 2.0, C, 4, 5800, 4000, "15W40", 4.25, 7500),
}
REPRIS = {k: bmw.FAMILLES[k] for k in ("M10-1.6", "M10-1.8", "M10-2.0", "M30-2.5", "M30-2.8", "M30-3.0", "M30-3.2")}
FAMILLES = {**ANCIENS, **REPRIS}
mg = SaisieMoteurs(FAMILLES, bmw.B, lambda fam: bmw.B)
L = []
IND = "données indicatives (modèle ancien), à vérifier"


def t(cle, nom=None, *surcharges):
    """Variante reprise de la table de bmw.py (même famille et couple) ; nom affiché facultatif."""
    v = bmw.TABLE[cle]
    return (nom or cle, v[-3], v[-1], *surcharges)


# ---------------------------------------------------------------- avant-guerre (Eisenach)
mg(L, "3/15", "DA", "1", "1929-04", "1932-03", [("0.75 15", "BMW-0.75", 35)], portes=2, places=4, reservoir=25,
   remarques="Première BMW (Austin Seven sous licence, DA-2 à DA-4), suite de la Dixi 3/15 DA-1 ; " + IND)
mg(L, "3/20", "AM", "1", "1932-03", "1934-12", [("0.8 20", "BMW-0.8", 45)], portes=2, places=4, reservoir=25, remarques="Première BMW de conception propre ; " + IND)
mg(L, "303", "303", "1", "1933-02", "1934-12", [("1.2 L6 30", "BMW-L6-1.2", 70)], portes=2, places=4, reservoir=40,
   remarques="Premier six cylindres BMW, première calandre « double haricot » ; " + IND)
mg(L, "309", "309", "1", "1934-01", "1936-12", [("0.85 22", "BMW-0.85", 50)], portes=2, places=4, reservoir=35, remarques="Quatre cylindres sur base 303 ; " + IND)
mg(L, "315", "315", "1", "1934-04", "1937-12", [("1.5 L6 34", "BMW-L6-1.5", 80), ("315/1 1.5 L6 40", "BMW-L6-1.5", 85)], portes=2, places=4, reservoir=40,
   remarques="Berline, cabriolet et roadster 315/1 ; " + IND)
mg(L, "319", "319", "1", "1935-01", "1937-12", [("1.9 L6 45", "BMW-L6-1.9", 110), ("319/1 1.9 L6 55", "BMW-L6-1.9", 115)], portes=2, places=4, reservoir=40,
   remarques="Berline, cabriolet et roadster 319/1 ; " + IND)
mg(L, "326", "326", "1", "1936-02", "1941-12", [("2.0 L6 50", "BMW-M78-2.0", 125)], portes=4, places=5, reservoir=50, remarques="Berline 4 portes et cabriolets ; " + IND)
mg(L, "320 / 321", "320", "1", "1937-01", "1941-12", [("2.0 L6 45", "BMW-M78-2.0", 120)], portes=2, places=4, reservoir=45, remarques="Berline 2 portes et cabriolet ; " + IND)
mg(L, "327", "327", "1", "1937-01", "1941-12", [("2.0 L6 55", "BMW-M78-2.0", 130), ("327/28 2.0 L6 80", "BMW-328-2.0", 126, {"debut": "1938-01"})],
   portes=2, places=4, reservoir=50, remarques="Coupé et cabriolet ; 327/28 à moteur de 328 ; " + IND)
mg(L, "328", "328", "1", "1936-06", "1940-12", [("2.0 L6 80", "BMW-328-2.0", 126)], portes=2, places=2, reservoir=50,
   remarques="Roadster sportif (Mille Miglia 1940), culasse à soupapes en V ; " + IND)
mg(L, "335", "335", "1", "1939-01", "1941-12", [("3.5 L6 90", "BMW-L6-3.5", 230)], portes=4, places=5, reservoir=65, remarques="Grande berline six cylindres ; " + IND)

# ---------------------------------------------------------------- après-guerre (Munich)
mg(L, "501", "501", "1", "1952-01", "1958-12", [("2.0 L6 65", "BMW-501-2.0", 130), ("2.0 L6 72", "BMW-501-2.0", 142, {"debut": "1955-01"})],
   portes=4, places=5, reservoir=58, remarques="« Ange baroque », première BMW d'après-guerre ; " + IND)
mg(L, "502", "502", "1", "1954-01", "1964-12", [("2.6 V8 95", "BMW-V8-2.6", 177), ("2.6 V8 100", "BMW-V8-2.6", 186, {"debut": "1958-01"}),
                                              ("3.2 V8 120", "BMW-V8-3.2", 211, {"debut": "1955-09"}), ("Super 3.2 V8 140", "BMW-V8-3.2", 220, {"debut": "1957-09"})],
   portes=4, places=5, reservoir=70, remarques="Premier V8 allemand d'après-guerre (2.6, 3.2, 3200 S) ; " + IND)
mg(L, "503", "503", "1", "1956-05", "1959-12", [("3.2 V8 140", "BMW-V8-3.2", 220)], portes=2, places=4, reservoir=75, remarques="Coupé et cabriolet Goertz ; " + IND)
mg(L, "507", "507", "1", "1956-11", "1959-12", [("3.2 V8 150", "BMW-V8-3.2", 236)], portes=2, places=2, reservoir=110,
   remarques="Roadster Albrecht von Goertz, 252 exemplaires ; " + IND)
mg(L, "3200 CS", "3200 CS", "1", "1962-02", "1965-12", [("3.2 V8 160", "BMW-V8-3.2", 240)], portes=2, places=4, reservoir=75, remarques="Coupé Bertone, dernier V8 BMW avant 1992 ; " + IND)
mg(L, "Isetta", "Isetta", "1", "1955-04", "1962-12", [("250 0.25 12", "BMW-1C-0.25", 14), ("300 0.3 13", "BMW-1C-0.3", 18, {"debut": "1956-01"})],
   portes=2, places=2, reservoir=13, remarques="Microvoiture sous licence Iso, porte frontale unique (choix 1 porte absent) ; monocylindre de moto BMW ; " + IND)
mg(L, "600", "600", "1", "1957-08", "1959-12", [("0.6 20", "BMW-2C-0.6", 39)], portes=2, places=4, reservoir=23, remarques="Isetta allongée à 4 places, bicylindre à plat ; " + IND)
mg(L, "700", "700", "1", "1959-08", "1965-12", [("0.7 30", "BMW-2C-0.7", 51), ("Sport 0.7 40", "BMW-2C-0.7", 52, {"debut": "1960-08"})],
   portes=2, places=4, reservoir=33, remarques="Berline, coupé et cabriolet Michelotti, sauvetage de BMW ; " + IND)
mg(L, "Neue Klasse", "115-121", "1", "1962-10", "1972-12",
   [("1500 1.5 80", "M10-1.5", 118, {"fin": "1964-12"}), ("1600 1.6 83", "M10-1.6", 125, {"debut": "1964-01", "fin": "1966-12"}), ("1800 1.8 90", "M10-1.8", 140, {"debut": "1963-09"}),
    ("1800 TI 1.8 110", "M10-1.8", 147, {"debut": "1964-01", "fin": "1966-12"}), ("2000 2.0 100", "M10-2.0", 157, {"debut": "1966-01"}),
    ("2000 tii 2.0 130", "M10-2.0", 181, {"debut": "1969-01"})], portes=4, places=5, reservoir=53, remarques="Berlines 1500 à 2000 tii, base de la renaissance de BMW ; " + IND)
mg(L, "02", "114", "1", "1966-03", "1977-07",
   [("1602 1.6 85", "M10-1.6", 123), ("1802 1.8 90", "M10-1.8", 140, {"debut": "1971-01"}), ("2002 2.0 100", "M10-2.0", 157, {"debut": "1968-01"}),
    ("2002 ti 2.0 120", "M10-2.0", 167, {"debut": "1968-09", "fin": "1971-12"}), ("2002 tii 2.0 130", "M10-2.0", 181, {"debut": "1971-04"}),
    ("2002 turbo 2.0 170", "M10-2.0T", 240, {"debut": "1973-09", "fin": "1975-12"})], portes=2, places=5, reservoir=46,
   remarques="Berline 2 portes, cabriolet et Touring ; 2002 turbo, première voiture de série européenne turbocompressée ; " + IND)
mg(L, "2000 C / CS", "120 C", "1", "1965-09", "1969-12", [("2000 C 2.0 100", "M10-2.0", 157), ("2000 CS 2.0 120", "M10-2.0", 167)], portes=2, places=4, reservoir=55,
   remarques="Coupé Karmann ; " + IND)
mg(L, "E3", "E3", "1", "1968-09", "1977-12",
   [t("525i 150", "2500 2.5 150"), ("2800 2.8 170", "M30-2.8", 234), ("3.0 S 3.0 180", "M30-3.0", 255, {"debut": "1971-04"}),
    ("3.0 Si 3.0 200", "M30-3.0", 272, {"debut": "1971-04"}), ("3.3 L 3.2 190", "M30-3.2", 290, {"debut": "1974-01"}), t("732i 197", "3.3 Li 3.2 197", {"debut": "1975-01"})],
   portes=4, places=5, reservoir=75, remarques="Grandes berlines six cylindres 2500 à 3.3 Li ; " + IND)
mg(L, "E9", "E9", "1", "1968-12", "1975-12",
   [("2800 CS 2.8 170", "M30-2.8", 234, {"fin": "1971-12"}), ("3.0 CS 3.0 180", "M30-3.0", 255, {"debut": "1971-04"}), ("3.0 CSi 3.0 200", "M30-3.0", 272, {"debut": "1971-04"}),
    ("3.0 CSL 3.2 206", "M30-3.2", 289, {"debut": "1972-08"})], portes=2, places=4, reservoir=70,
   remarques="Coupés Karmann, 3.0 CSL allégée (« Batmobile ») d'homologation ; " + IND)

MOT = Motorisations(bmw.B, FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"BMW": L}
MOTEURS = MOT.moteurs()
