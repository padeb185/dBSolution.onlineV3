"""Packard : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Model A, Model 30, Twin Six, Single Eight, Eight, Twelve, One-Twenty, Clipper, Patrician, Caribbean et Hawk.
Moteurs Packard (monocylindre, quatre cylindres, V12 Twin Six et Twelve, huit cylindres en ligne, V8 de 1955) et V8 Studebaker
à compresseur (Hawk) ajoutés. Puissances brutes (SAE gross) converties en ch (× 1,014). Données indicatives.
Marque fermée en 1958.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C = "CHAINE"
SV = "NC"

PACKARD = {
    "PACKARD-1CYL-2.0": f("ATM", E_, 2.0, SV, 1, 800, 600, "SAE30", 2.0, 1000),
    "PACKARD-4CYL-7.1": f("ATM", E_, 7.1, SV, 4, 1700, 900, "SAE30", 6.0, 2000),
    "PACKARD-V12-7.0": f("ATM", E_, 7.0, SV, 12, 2600, 1200, "SAE30", 8.0, 2000, a="V"),
    "PACKARD-V12-7.3": f("ATM", E_, 7.3, SV, 12, 3200, 1400, "SAE30", 8.0, 3000, a="V"),
    "PACKARD-L8-4.2": f("ATM", E_, 4.2, SV, 8, 3800, 2000, "SAE30", 5.5, 3000),
    "PACKARD-L8-4.6": f("ATM", E_, 4.6, SV, 8, 3800, 2000, "SAE30", 5.5, 3000),
    "PACKARD-L8-5.2": f("ATM", E_, 5.2, SV, 8, 3200, 1600, "SAE30", 6.5, 3000),
    "PACKARD-L8-5.4": f("ATM", E_, 5.4, SV, 8, 3600, 2000, "SAE30", 6.5, 3000),
    "PACKARD-L8-5.8": f("ATM", E_, 5.8, SV, 8, 3600, 2000, "SAE30", 6.5, 3000),
    "PACKARD-L8-5.9": f("ATM", E_, 5.9, SV, 8, 3200, 1600, "SAE30", 6.5, 3000),
    "PACKARD-L8-6.3": f("ATM", E_, 6.3, SV, 8, 3200, 1600, "SAE30", 6.5, 3000),
    "PACKARD-V8-5.8": f("ATM", E_, 5.8, C, 8, 4600, 2800, "10W30", 5.7, 5000, a="V"),
    "PACKARD-V8-6.1": f("ATM", E_, 6.1, C, 8, 4600, 2800, "10W30", 5.7, 5000, a="V"),
}
STUDEBAKER = {"STUDEBAKER-V8-4.7SC": f("TURBO", E_, 4.7, C, 8, 4800, 3200, "10W30", 4.7, 5000, a="V")}
FAMILLES = {**PACKARD, **STUDEBAKER}


def motoriste(fam):
    return "Studebaker" if fam in STUDEBAKER else "Packard"


mg = SaisieMoteurs(FAMILLES, "Packard", motoriste)
L = []
NA = "Marché nord-américain"
IND = NA + " ; données indicatives"

mg(L, "Model A", "Model A", "1", "1899-11", "1900-12", [("1CYL 9", "PACKARD-1CYL-2.0", 40)], portes=0, places=2, reservoir=20,
   remarques="Runabout monocylindre ; " + IND)
mg(L, "Model 30", "Model 30", "1", "1907-01", "1912-12", [("7.1 30", "PACKARD-4CYL-7.1", 250)], portes=4, places=5, reservoir=75,
   remarques="Torpédo, quatre cylindres ; " + IND)
mg(L, "Twin Six", "Twin Six", "1", "1916-01", "1923-12", [("7.0 V12 89", "PACKARD-V12-7.0", 380)], portes=4, places=7, reservoir=90,
   remarques="Premier V12 de série ; " + IND)
mg(L, "Single Eight", "Single Eight", "1", "1924-01", "1926-12", [("5.9 L8 86", "PACKARD-L8-5.9", 330)], portes=4, places=5, reservoir=90,
   remarques="Huit cylindres en ligne ; " + IND)
mg(L, "Eight", "Eight", "1", "1929-01", "1936-12",
   [("Standard 5.2 L8 91", "PACKARD-L8-5.2", 300, {"fin": "1931-12"}), ("Standard 5.2 L8 112", "PACKARD-L8-5.2", 340, {"debut": "1932-01", "fin": "1933-12"}),
    ("Standard 5.2 L8 122", "PACKARD-L8-5.2", 360, {"debut": "1934-01"}), ("Super 6.3 L8 107", "PACKARD-L8-6.3", 390, {"fin": "1931-12"}),
    ("Super 6.3 L8 122", "PACKARD-L8-6.3", 420, {"debut": "1932-01", "fin": "1933-12"}), ("Super 6.3 L8 132", "PACKARD-L8-6.3", 440, {"debut": "1934-01"})],
   portes=4, places=5, reservoir=95, remarques="Eight, Standard Eight, Super Eight et Custom Eight ; " + IND)
mg(L, "Twelve", "Twelve", "1", "1932-01", "1939-12", [("7.3 V12 162", "PACKARD-V12-7.3", 434, {"fin": "1934-12"}), ("7.3 V12 177", "PACKARD-V12-7.3", 461, {"debut": "1935-01"})],
   portes=4, places=5, reservoir=110, remarques="Twin Six en 1932, puis Twelve ; berline et cabriolet ; " + IND)
mg(L, "One-Twenty", "One-Twenty", "1", "1935-01", "1941-12", [("4.2 L8 112", "PACKARD-L8-4.2", 271, {"fin": "1936-12"}), ("4.6 L8 122", "PACKARD-L8-4.6", 305, {"debut": "1937-01"})],
   portes=4, places=5, reservoir=75, remarques="Packard d'entrée de gamme à huit cylindres ; " + IND)
mg(L, "Clipper", "Clipper", "1", "1941-04", "1947-12", [("4.6 L8 127", "PACKARD-L8-4.6", 312), ("Custom 5.8 L8 167", "PACKARD-L8-5.8", 393)], portes=4, places=6, reservoir=80,
   remarques="Production interrompue de 1942 à 1945 ; " + IND)
mg(L, "Patrician", "Patrician", "1", "1951-01", "1956-12",
   [("5.4 L8 157", "PACKARD-L8-5.4", 366, {"fin": "1953-12"}), ("5.9 L8 215", "PACKARD-L8-5.9", 420, {"debut": "1954-01", "fin": "1954-12"}),
    ("5.8 V8 264", "PACKARD-V8-5.8", 515, {"debut": "1955-01", "fin": "1955-12"}), ("6.1 V8 294", "PACKARD-V8-6.1", 549, {"debut": "1956-01"})],
   portes=4, places=6, reservoir=80, remarques="Patrician 400 ; V8 Packard à partir de 1955 ; " + IND)
mg(L, "Caribbean", "Caribbean", "1", "1953-01", "1956-12",
   [("5.4 L8 183", "PACKARD-L8-5.4", 380, {"fin": "1953-12"}), ("5.9 L8 215", "PACKARD-L8-5.9", 420, {"debut": "1954-01", "fin": "1954-12"}),
    ("5.8 V8 279", "PACKARD-V8-5.8", 522, {"debut": "1955-01", "fin": "1955-12"}), ("6.1 V8 314", "PACKARD-V8-6.1", 549, {"debut": "1956-01"})],
   portes=2, places=6, reservoir=80, remarques="Cabriolet puis aussi coupé hardtop ; " + IND)
mg(L, "Hawk", "Hawk", "1", "1958-01", "1958-12", [("4.7 V8 Supercharged 279", "STUDEBAKER-V8-4.7SC", 450)], portes=2, places=5, reservoir=68,
   remarques="Coupé sur base Studebaker Golden Hawk, 588 exemplaires ; " + IND)

MOT = Motorisations("Packard", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Packard": L}
MOTEURS = MOT.moteurs()
