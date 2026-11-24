"""Benz & Cie (Mannheim, 1886-1926, avant la fusion Daimler-Benz) : modèles, motorisations et moteurs liés.
Patent-Motorwagen, Victoria, Velo, Ideal, Parsifal, Blitzen-Benz, 8/20 PS, 10/30 PS.
Les voitures après 1926 sont dans Mercedes-Benz. Toutes les données sont indicatives (marque ancienne) ; couples estimés.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom (arrondie)."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"


def mono(l, rpm, q):
    return f("ATM", E_, l, "NC", 1, rpm, rpm, "CHOISIR", q, 1000)


FAMILLES = {
    "BENZ-1C-1.0": mono(1.0, 400, 2.0),
    "BENZ-1C-1.1": mono(1.1, 700, 2.0),
    "BENZ-1C-1.7": mono(1.7, 700, 3.0),
    "BENZ-1C-2.9": mono(2.9, 700, 3.0),
    "BENZ-2C-2.7": f("ATM", E_, 2.7, "NC", 2, 1200, 1000, "CHOISIR", 4.0, 1000),
    "BENZ-4C-2.0": f("ATM", E_, 2.0, "NC", 4, 1800, 1400, "CHOISIR", 5.0, 2000),
    "BENZ-4C-2.6": f("ATM", E_, 2.6, "NC", 4, 2000, 1500, "CHOISIR", 5.0, 2000),
    "BENZ-4C-21.5": f("ATM", E_, 21.5, "NC", 4, 1600, 1400, "CHOISIR", 20.0, 1000),
}

mg = SaisieMoteurs(FAMILLES, "Benz")
L = []
R = "Désignations, dates et chiffres indicatifs (marque ancienne), à vérifier"

mg(L, "Patent-Motorwagen", "Typ 1-3", "1", "1886-01", "1893-12", [("Nr. 1 1", "BENZ-1C-1.0", 10), ("Nr. 3 2", "BENZ-1C-1.0", 15, {"debut": "1888-01"})],
   portes=0, places=2, reservoir=5, remarques=R + " ; tricycle, première automobile")
mg(L, "Victoria", "Victoria", "1", "1893-01", "1900-12", [("Victoria 3", "BENZ-1C-1.7", 30), ("Victoria 5", "BENZ-1C-2.9", 50, {"debut": "1896-01"})],
   portes=0, places=2, reservoir=20, remarques=R + " ; vis-à-vis, première quatre-roues Benz")
mg(L, "Velo", "Velo", "1", "1894-01", "1902-12", [("Velo 2", "BENZ-1C-1.0", 18), ("Comfortable 3", "BENZ-1C-1.1", 25, {"debut": "1897-01"})],
   portes=0, places=2, reservoir=15, remarques=R + " ; voiturette produite en série")
mg(L, "Ideal", "Ideal", "1", "1898-01", "1902-12", [("Ideal 3", "BENZ-1C-1.1", 28), ("Ideal 5", "BENZ-1C-1.7", 40, {"debut": "1900-01"})],
   portes=0, places=2, reservoir=15, remarques=R + " ; voiturette")
mg(L, "Parsifal", "Parsifal", "1", "1903-01", "1905-12", [("Parsifal 12", "BENZ-2C-2.7", 70)], portes=0, places=4, reservoir=30, remarques=R + " ; tonneau, 2 cylindres")
mg(L, "Blitzen-Benz", "Blitzen", "1", "1909-01", "1913-12", [("Blitzen-Benz 200", "BENZ-4C-21.5", 900)], portes=0, places=1, reservoir=60,
   remarques=R + " ; voiture de record (plus de 200 km/h en 1910)")
mg(L, "8/20 PS", "8/20", "1", "1912-01", "1921-12", [("8/20 PS 20", "BENZ-4C-2.0", 85)], portes=4, places=4, reservoir=40, remarques=R + " ; torpédo")
mg(L, "10/30 PS", "10/30", "1", "1921-01", "1926-06", [("10/30 PS 30", "BENZ-4C-2.6", 110)], portes=4, places=4, reservoir=50,
   remarques=R + " ; torpédo ; dernière Benz avant la fusion Daimler-Benz (1926)")

MOT = Motorisations("Benz", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Benz": L}
MOTEURS = MOT.moteurs()
