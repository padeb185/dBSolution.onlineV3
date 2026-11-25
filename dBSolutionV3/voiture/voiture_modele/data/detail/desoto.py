"""DeSoto (Chrysler, Detroit, 1928-1961) : modèles, motorisations et moteurs liés.
Series K, Airflow, Custom, Diplomat (export), Firedome, Fireflite, Adventurer. Marché nord-américain.
Puissances SAE brutes converties en ch (×1,014). Toutes les données sont indicatives (marque ancienne).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C = "CHAINE"


def i6(l, rpm, nmrpm):
    return f("ATM", E_, l, C, 6, rpm, nmrpm, "CHOISIR", 5.0, 3000)


def hemi(l, rpm, nmrpm):
    return f("ATM", E_, l, C, 8, rpm, nmrpm, "CHOISIR", 5.7, 3000, a="V")


FAMILLES = {
    "DS-I6-2.9": i6(2.9, 2800, 1200), "DS-I6-3.6": i6(3.6, 3600, 1600), "DS-I6-3.9": i6(3.9, 3600, 1600), "DS-I6-4.0": i6(4.0, 3400, 1600),
    "DS-I6-4.1": i6(4.1, 3600, 1600),
    "FIREDOME-4.5": hemi(4.5, 4400, 2000), "HEMI-4.8": hemi(4.8, 4400, 2400), "HEMI-5.4": hemi(5.4, 4400, 2800), "HEMI-5.6": hemi(5.6, 5200, 3200),
    "TURBOFLASH-5.9": hemi(5.9, 4600, 3200), "TURBOFLASH-6.3": hemi(6.3, 4600, 3000),
}

mg = SaisieMoteurs(FAMILLES, "DeSoto")
L = []
R = "Marché nord-américain ; données indicatives (marque ancienne), à vérifier"

mg(L, "Series K", "K", "1", "1928-08", "1930-12", [("Series K Six 56", "DS-I6-2.9", 160)], portes=4, places=5, reservoir=50, remarques=R)
mg(L, "Airflow", "SE", "1", "1934-01", "1936-12", [("Airflow 4.0 I6 101", "DS-I6-4.0", 251)], portes=4, places=6, reservoir=60, remarques=R + " ; carrosserie aérodynamique")
mg(L, "Custom", "S-series", "1", "1939-01", "1952-12", [("Custom 3.9 I6 101", "DS-I6-3.9", 244, {"fin": "1941-12"}), ("Custom 3.9 I6 110", "DS-I6-3.9", 251, {"debut": "1946-01", "fin": "1949-12"}),
                                                         ("Custom 4.1 I6 118", "DS-I6-4.1", 264, {"debut": "1950-01"})], portes=4, places=6, reservoir=64, remarques=R)
mg(L, "Diplomat", "Export", "1", "1946-01", "1961-12", [("Diplomat 3.6 I6 96", "DS-I6-3.6", 230)], portes=4, places=6, reservoir=64,
   remarques=R + " ; modèle d'exportation (base Plymouth / Dodge)")
mg(L, "Firedome", "S-16", "1", "1952-01", "1959-12", [("Firedome 4.5 V8 162", "FIREDOME-4.5", 339, {"fin": "1954-12"}), ("Firedome 4.8 V8 188", "HEMI-4.8", 366, {"debut": "1955-01", "fin": "1956-12"}),
                                                       ("Firedome 5.6 V8 274", "TURBOFLASH-5.9", 461, {"debut": "1957-01"})], portes=4, places=6, reservoir=64,
   remarques=R + " ; V8 Hemi « FireDome »")
mg(L, "Fireflite", "S-21", "1", "1955-01", "1960-12", [("Fireflite 4.8 V8 203", "HEMI-4.8", 373, {"fin": "1955-12"}), ("Fireflite 5.4 V8 259", "HEMI-5.4", 441, {"debut": "1956-01", "fin": "1956-12"}),
                                                       ("Fireflite 5.6 V8 299", "HEMI-5.6", 488, {"debut": "1957-01", "fin": "1958-12"}), ("Fireflite 6.3 V8 330", "TURBOFLASH-6.3", 576, {"debut": "1959-01"})],
   portes=4, places=6, reservoir=76, remarques=R + " ; berline, coupé hardtop, cabriolet")
mg(L, "Adventurer", "S-24", "1", "1956-01", "1960-12", [("Adventurer 5.6 V8 325", "HEMI-5.6", 495, {"fin": "1957-12"}), ("Adventurer 5.9 V8 350", "TURBOFLASH-5.9", 590, {"debut": "1958-01", "fin": "1958-12"}),
                                                         ("Adventurer 6.3 V8 355", "TURBOFLASH-6.3", 590, {"debut": "1959-01"})], portes=2, places=6, reservoir=76,
   remarques=R + " ; coupé hardtop et cabriolet hautes performances")

MOT = Motorisations("DeSoto", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"DeSoto": L}
MOTEURS = MOT.moteurs()
