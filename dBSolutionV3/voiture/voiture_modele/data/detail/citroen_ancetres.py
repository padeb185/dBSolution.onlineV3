"""Citroën (ancêtres et modèles anciens) : générations, phases, motorisations (marché européen) et moteurs liés.
Avant-guerre (quai de Javel) : Type A (première Citroën, 1919), B2, 5 CV (Type C), B12 / B14, C4, C6 et Rosalie (8 / 10 / 15 CV) ;
puis Type H, Acadiane, C15, C25, Jumpy (I), Jumper (I) et C3 Pluriel (absents de citroen.py). Moteurs repris de citroen.py
(mêmes familles, codes, couples et motoristes) via sa table ; moteurs d'avant-guerre et Sofim 2.8 ajoutés.
Puissances en ch. Données d'avant-guerre indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from . import citroen

E_, D = "ESS", "DSL"


def anc(l, n, rpm, nmrpm, q):
    return f("ATM", E_, l, "NC", n, rpm, nmrpm, "SAE30", q, 3000)


ANCIENS = {
    "CIT-A-1.3": anc(1.3, 4, 2100, 1200, 3.0),
    "CIT-B-1.45": anc(1.45, 4, 2100, 1200, 3.0),
    "CIT-C-0.86": anc(0.86, 4, 2100, 1200, 2.5),
    "CIT-B14-1.5": anc(1.54, 4, 2300, 1200, 3.0),
    "CIT-C4-1.6": anc(1.6, 4, 3000, 1600, 3.5),
    "CIT-C6-L6-2.4": anc(2.4, 6, 3000, 1600, 5.0),
    "CIT-ROS-1.45": anc(1.45, 4, 3200, 1800, 3.5),
    "CIT-ROS-1.8": anc(1.8, 4, 3200, 1800, 4.0),
    "CIT-ROS-L6-2.65": anc(2.65, 6, 3400, 1800, 5.0),
    "SOFIM-2.8": f("TURBO", D, 2.8, "COURROIE", 4, 3600, 1800, "10W40", 6.0, 20000),
}
FAMILLES = {**citroen.FAMILLES, **ANCIENS}


AUTRES = {v[1]: v[0] for v in citroen.TABLE.values() if len(v) == 4}


def motoriste(fam):
    if fam in AUTRES:
        return AUTRES[fam]
    if fam in ANCIENS:
        return "Iveco" if fam == "SOFIM-2.8" else "Citroën"
    return "Peugeot"


mg = SaisieMoteurs(FAMILLES, "Citroën", motoriste)
L = []
IND = "données indicatives (modèle ancien), à vérifier"


def t(cle, nom=None, *surcharges):
    """Variante reprise de la table de citroen.py (même famille et couple) ; nom affiché facultatif."""
    v = citroen.TABLE[cle]
    fam, nm = v[-3], v[-1]
    return (nom or cle, fam, nm, *surcharges)


# ---------------------------------------------------------------- avant-guerre
mg(L, "Type A", "Type A", "1", "1919-06", "1921-12", [("1.3 18", "CIT-A-1.3", 60)], portes=4, places=4, reservoir=40,
   remarques="Première Citroën, première voiture européenne produite en grande série ; " + IND)
mg(L, "B2", "B2", "1", "1921-06", "1926-12", [("1.45 20", "CIT-B-1.45", 65)], portes=4, places=4, reservoir=40,
   remarques="Torpédo, conduite intérieure ; autochenilles Kégresse (Croisière noire) ; " + IND)
mg(L, "5 CV", "Type C", "1", "1922-01", "1926-12", [("0.86 11", "CIT-C-0.86", 35)], portes=2, places=2, reservoir=25,
   remarques="« Petit citron », torpédo et Trèfle (3 places) ; " + IND)
mg(L, "B12 / B14", "B12", "1", "1925-01", "1928-12", [("B12 1.45 22", "CIT-B-1.45", 70), ("B14 1.5 22", "CIT-B14-1.5", 75, {"debut": "1926-10"})],
   portes=4, places=5, reservoir=40, remarques="Première carrosserie tout acier en Europe (B10, 1924) ; " + IND)
mg(L, "C4", "C4", "1", "1928-10", "1932-12", [("1.6 30", "CIT-C4-1.6", 90)], portes=4, places=5, reservoir=45, remarques="Berline, coupé et utilitaires ; " + IND)
mg(L, "C6", "C6", "1", "1928-10", "1932-12", [("2.4 L6 45", "CIT-C6-L6-2.4", 130)], portes=4, places=5, reservoir=55, remarques="Première Citroën six cylindres ; " + IND)
mg(L, "Rosalie", "Rosalie", "1", "1932-10", "1938-12", [("8 CV 1.45 32", "CIT-ROS-1.45", 80), ("10 CV 1.8 36", "CIT-ROS-1.8", 95),
                                                      ("15 CV 2.65 L6 56", "CIT-ROS-L6-2.65", 150)], portes=4, places=5, reservoir=50,
   remarques="8, 10 et 15 CV, moteur flottant, records de Montlhéry (Petite Rosalie, 1933) ; " + IND)

# ---------------------------------------------------------------- utilitaires et modèles absents
mg(L, "Type H", "H", "1", "1947-12", "1981-12", [("1.9 45", "CIT-11", 115, {"fin": "1960-12"}), ("1.9 58", "CIT-11", 127, {"debut": "1961-01"})],
   portes=3, places=3, reservoir=55, remarques="Fourgon à tôle ondulée et traction avant, moteur de Traction 11 ; versions diesel non reprises ; " + IND)
mg(L, "Acadiane", "Acadiane", "1", "1978-01", "1987-12", [("602 31", "2CV-602", 42)], portes=4, places=2, reservoir=25, remarques="Fourgonnette dérivée de la Dyane ; " + IND)
mg(L, "C15", "VD", "1", "1984-10", "2005-12", [t("1.1 50"), t("1.8 D 60"), t("1.9 D 65", None, {"debut": "1995-01"}), t("1.9 D 70", None, {"debut": "2000-01"})],
   portes=2, places=2, reservoir=43, remarques="Fourgonnette dérivée de la Visa")
mg(L, "C25", "280", "1", "1981-09", "1994-06", [t("2.5 D 75"), t("2.5 TD 95", None, {"debut": "1987-01"})], portes=4, places=3, reservoir=80,
   remarques="Fourgon Sevel (jumeau Peugeot J5 / Fiat Ducato) ; versions essence non reprises")
mg(L, "Jumpy", "U64", "1", "1994-11", "2006-12", [t("1.9 D 70"), t("1.9 TD 90"), t("2.0 HDi 90", None, {"debut": "1999-01"}), t("2.0 HDi 109", None, {"debut": "2004-01"})],
   portes=4, places=3, reservoir=70, remarques="Fourgon Sevel Nord (jumeau Peugeot Expert / Fiat Scudo), Jumpy Combi")
mg(L, "Jumper", "230", "1", "1994-03", "2006-06", [t("1.9 D 68"), t("2.2 HDi 100", None, {"debut": "2002-01"}), ("2.8 HDi 128", "SOFIM-2.8", 300, {"debut": "2000-01"})],
   portes=4, places=3, reservoir=80, remarques="Fourgon Sevel (jumeau Peugeot Boxer / Fiat Ducato) ; versions 2.5 D / TD non reprises")
mg(L, "C3 Pluriel", "HB", "1", "2003-04", "2010-12", [t("1.4 75"), t("1.6 16v 110"), t("1.4 HDi 70")], portes=2, places=4, reservoir=47,
   remarques="Cabriolet modulable sur base C3")

MOT = Motorisations("Citroën", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Citroën": L}
MOTEURS = MOT.moteurs()
