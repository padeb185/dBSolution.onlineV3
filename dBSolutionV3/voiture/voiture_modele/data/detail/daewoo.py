"""Daewoo : générations, motorisations (marché européen, 1995-2004) et moteurs liés.
Nexia, Espero, Lanos, Nubira, Leganza, Matiz, Tacuma (Rezzo), Kalos, Lacetti, Evanda, Korando et Musso (SsangYong vendus Daewoo).
Les modèles sont ensuite vendus sous la marque Chevrolet en Europe (2005). Données indicatives (marque disparue).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

FAMILLES = {
    "F8CV-0.8": f("ATM", E_, 0.8, B, 3, 6000, 4600, "10W40", 2.7, 10000),
    "SOHC-1.0": f("ATM", E_, 1.0, B, 4, 5400, 4200, "10W40", 3.25, 10000),
    "SOHC-1.2": f("ATM", E_, 1.2, B, 4, 5400, 3000, "10W40", 3.25, 10000),
    "SOHC-1.3": f("ATM", E_, 1.3, B, 4, 5400, 3400, "10W40", 3.75, 10000),
    "SOHC-1.4": f("ATM", E_, 1.4, B, 4, 5600, 3000, "10W40", 3.75, 10000),
    "SOHC-1.5": f("ATM", E_, 1.5, B, 4, 5400, 3200, "10W40", 3.75, 10000),
    "DOHC-1.5": f("ATM", E_, 1.5, B, 4, 6200, 3400, "10W40", 3.75, 10000),
    "ETEC-1.4": f("ATM", E_, 1.4, B, 4, 6200, 3400, "10W40", 3.75, 10000),
    "ETEC-1.6": f("ATM", E_, 1.6, B, 4, 6000, 3400, "10W40", 3.75, 10000),
    "FAM2-1.8": f("ATM", E_, 1.8, B, 4, 5800, 4000, "10W40", 4.0, 10000),
    "FAM2-2.0": f("ATM", E_, 2.0, B, 4, 5400, 4400, "10W40", 4.0, 10000),
    "FAM2-2.2": f("ATM", E_, 2.2, B, 4, 5200, 4400, "10W40", 4.0, 10000),
    "MB-2.3": f("ATM", E_, 2.3, C, 4, 5500, 4000, "10W40", 6.0, 10000),
    "MB-3.2": f("ATM", E_, 3.2, C, 6, 5500, 3750, "10W40", 7.5, 10000),
    "MB-2.9TD": f("TURBO", D, 2.9, C, 5, 4000, 2250, "15W40", 7.5, 10000),
}

mg = SaisieMoteurs(FAMILLES, "Daewoo")
L = []
IND = "Données indicatives"

mg(L, "Nexia", "KLETN", "1", "1995-01", "1997-12", [("1.5 75", "SOHC-1.5", 123), ("1.5 16V 90", "DOHC-1.5", 134)], portes=3, reservoir=50,
   remarques=IND + " ; 3 et 5 portes, berline (base Opel Kadett E)")
mg(L, "Espero", "KLEJ", "1", "1995-01", "1999-12", [("1.5 16V 90", "DOHC-1.5", 134), ("1.8 95", "FAM2-1.8", 148), ("2.0 105", "FAM2-2.0", 170)],
   portes=4, reservoir=60, remarques=IND)
mg(L, "Lanos", "KLAT", "1", "1997-06", "2004-12",
   [("1.3 75", "SOHC-1.3", 107, {"fin": "1999-12"}), ("1.4 75", "SOHC-1.4", 115, {"debut": "2000-01"}), ("1.5 86", "SOHC-1.5", 130),
    ("1.6 16V 106", "ETEC-1.6", 145)], portes=3, reservoir=48, remarques=IND + " ; 3 et 5 portes, berline")
mg(L, "Nubira", "J100", "1", "1997-04", "1999-08", [("1.6 16V 106", "ETEC-1.6", 145), ("2.0 16V 133", "FAM2-2.0", 184)], portes=4, reservoir=60,
   remarques=IND + " ; berline, 5 portes, Wagon")
mg(L, "Nubira", "J150", "1", "1999-09", "2003-06", [("1.6 16V 106", "ETEC-1.6", 145), ("2.0 16V 133", "FAM2-2.0", 184)], portes=4, reservoir=60,
   remarques=IND + " ; restylage (Nubira II)")
mg(L, "Leganza", "V100", "1", "1997-06", "2003-06", [("2.0 16V 133", "FAM2-2.0", 184), ("2.2 16V 136", "FAM2-2.2", 207, {"debut": "1999-01"})],
   portes=4, reservoir=65, remarques=IND + " ; berline Italdesign")
mg(L, "Matiz", "M100", "1", "1998-03", "2000-08", [("0.8 51", "F8CV-0.8", 69)], reservoir=35, remarques=IND + " ; citadine Italdesign")
mg(L, "Matiz", "M150", "1", "2000-09", "2005-02", [("0.8 52", "F8CV-0.8", 69), ("1.0 64", "SOHC-1.0", 87, {"debut": "2003-01"})], reservoir=35,
   remarques=IND + " ; restylage ; vendue ensuite Chevrolet Matiz")
mg(L, "Tacuma", "U100", "1", "2000-09", "2004-12", [("1.6 16V 105", "ETEC-1.6", 145), ("1.8 98", "FAM2-1.8", 148), ("2.0 16V 121", "FAM2-2.0", 175)],
   reservoir=60, remarques=IND + " ; monospace (Rezzo sur certains marchés)")
mg(L, "Kalos", "T200", "1", "2002-09", "2004-12", [("1.2 72", "SOHC-1.2", 104), ("1.4 83", "SOHC-1.4", 123), ("1.4 16V 94", "ETEC-1.4", 130)],
   reservoir=45, remarques=IND + " ; 3 et 5 portes, berline ; vendue ensuite Chevrolet Kalos")
mg(L, "Lacetti", "J200", "1", "2003-03", "2004-12", [("1.4 16V 95", "ETEC-1.4", 131), ("1.6 16V 109", "ETEC-1.6", 150), ("1.8 16V 122", "FAM2-1.8", 165)],
   reservoir=60, remarques=IND + " ; 5 portes (Nubira berline/Wagon) ; vendue ensuite Chevrolet")
mg(L, "Evanda", "V200", "1", "2002-06", "2004-12", [("2.0 16V 131", "FAM2-2.0", 184)], portes=4, reservoir=65, remarques=IND + " ; vendue ensuite Chevrolet Evanda")
mg(L, "Korando", "KJ", "1", "1997-09", "2002-12", [("2.3 150", "MB-2.3", 214), ("2.9 TD 120", "MB-2.9TD", 250)], portes=3, reservoir=70,
   remarques=IND + " ; SsangYong vendu sous la marque Daewoo (moteurs Mercedes sous licence)")
mg(L, "Musso", "FJ", "1", "1998-01", "2002-12", [("2.3 150", "MB-2.3", 214), ("3.2 220", "MB-3.2", 310), ("2.9 TD 120", "MB-2.9TD", 250)], reservoir=75,
   remarques=IND + " ; SsangYong vendu sous la marque Daewoo")

MOT = Motorisations("Daewoo", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Daewoo": L}
MOTEURS = MOT.moteurs()
