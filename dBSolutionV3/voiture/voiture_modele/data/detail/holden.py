"""Holden (General Motors-Holden's, Australie) : générations, phases, motorisations (marché australien) et moteurs liés.
Holden « maison » (1948-2017) : 48-215 (FX) à EJ, EH, HD, HR, Kingswood / Belmont / Premier (HK à HZ), Monaro, Statesman et
Caprice, Torana, Gemini (Isuzu), Camira, Commodore (VB à VF, puis ZB importée d'Opel), Monaro V2, Cruze (assemblée à Adélaïde) et
HSV (Holden Special Vehicles : Clubsport, GTS, GTSR W1). Importations GM : Barina, Astra, Vectra, Calibra, Viva, Epica, Captiva,
Malibu, Trax, Equinox, Acadia. Non repris : modèles rebadgés Nissan / Toyota / Suzuki / Isuzu (Pulsar-Astra LB-LD, Nova, Apollo,
Barina MB-ML, Jackaroo, Rodeo, Colorado, Shuttle, Drover), utes et utilitaires. Marque fermée en 2020.
Puissances : hp brut × 1,014 jusqu'en 1976, puis kW × 1,36 (ch). Moteurs GM repris de chevrolet.py, buick.py, pontiac.py, opel.py,
daewoo.py et vauxhall.py (mêmes codes et couples). Données anciennes indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET
from .buick import FAMILLES as FAMILLES_BUICK
from .pontiac import FAMILLES as FAMILLES_PONTIAC
from .opel import FAMILLES as FAMILLES_OPEL
from .daewoo import FAMILLES as FAMILLES_DAEWOO
from .vauxhall import FAMILLES as FAMILLES_VAUXHALL

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"


def v8(l, rpm, nmrpm, q=5.5, h="15W40"):
    return f("ATM", E_, l, C, 8, rpm, nmrpm, h, q, 5000, a="V")


HOLDEN = {
    "HOLDEN-GREY-2.2": f("ATM", E_, 2.2, C, 6, 3800, 2000, "SAE30", 4.0, 3000),
    "HOLDEN-GREY-2.3": f("ATM", E_, 2.3, C, 6, 4000, 2000, "SAE30", 4.0, 3000),
    "HOLDEN-RED-2.25": f("ATM", E_, 2.25, C, 6, 4400, 2000, "20W50", 4.5, 5000),
    "HOLDEN-RED-2.4": f("ATM", E_, 2.4, C, 6, 4400, 2000, "20W50", 4.5, 5000),
    "HOLDEN-RED-2.6": f("ATM", E_, 2.6, C, 6, 4400, 2000, "20W50", 4.5, 5000),
    "HOLDEN-RED-2.8": f("ATM", E_, 2.8, C, 6, 4400, 2000, "20W50", 4.5, 5000),
    "HOLDEN-RED-2.9": f("ATM", E_, 2.9, C, 6, 4400, 2000, "20W50", 4.5, 5000),
    "HOLDEN-RED-3.0": f("ATM", E_, 3.0, C, 6, 4600, 2400, "20W50", 4.5, 5000),
    "HOLDEN-6-3.3": f("ATM", E_, 3.3, C, 6, 4400, 2400, "15W40", 4.7, 5000),
    "HOLDEN-STARFIRE-1.9": f("ATM", E_, 1.9, C, 4, 4800, 2400, "15W40", 3.8, 5000),
    "HOLDEN-V8-4.2": v8(4.2, 4500, 2600),
    "HOLDEN-V8-5.0": v8(5.0, 4800, 3000),
    "HOLDEN-V8-5.7": v8(5.7, 5000, 3600),
    "CHEV-307-5.0": v8(5.0, 4600, 2400),
    "RB30E-3.0": f("ATM", E_, 3.0, B, 6, 5200, 3200, "10W40", 4.5, 10000),
    "RB30ET-3.0T": f("TURBO", E_, 3.0, B, 6, 5600, 3200, "10W40", 4.5, 10000),
    "ISUZU-G161-1.6": f("ATM", E_, 1.6, C, 4, 5400, 3000, "10W40", 3.5, 10000),
    "ISUZU-4FB1-1.8D": f("ATM", D, 1.8, B, 4, 4800, 2600, "15W40", 4.5, 7500),
    "ISUZU-4XC1-1.5": f("ATM", E_, 1.5, B, 4, 5600, 3600, "10W40", 3.4, 10000),
    "GM-3.0-V6": f("ATM", E_, 3.0, C, 6, 6900, 2900, "5W30", 5.7, 15000, a="V"),
}
CHEV = {k: FAMILLES_CHEVROLET[k] for k in ("LS1-5.7", "LS2-6.0", "LS3-6.2", "LSA-6.2SC", "LS9-6.2SC", "SBC-5.4", "SBC-5.7", "GM-3.6-V6", "GM-2.4",
                                           "GM-1.5T", "GM-2.0T", "XK6-2.0", "XK6-2.5", "VCDI-2.0", "VCDI-2.2")}
BUICK = {k: FAMILLES_BUICK[k] for k in ("GM-3800", "GM-3800-SC")}
PONT = {"L76-6.0": FAMILLES_PONTIAC["L76-6.0"]}
OPEL = {k: FAMILLES_OPEL[k] for k in ("FAM2-1.6", "FAM2-1.8", "FAM2-2.0", "FAM2-2.0-16V", "FAM2-2.0T", "FAM2-1.8-16V", "FAM2-2.2", "FAM1-1.4", "FAM1-1.6",
                                      "FAM0-1.4", "FAM1-1.6T", "X25XE-2.5V6", "Y32SE-3.2V6", "CIH-1.9", "A20NHT-2.0T", "A20DTH-2.0CDTI", "A16XHT-1.6T",
                                      "B14XFT-1.4T", "FIAT-1.9TID", "ECOTEC-1.4T", "ECOTEC-1.6", "ECOTEC-1.8")}
DAEWOO = {"ETEC-1.6": FAMILLES_DAEWOO["ETEC-1.6"]}
VAUX = {k: FAMILLES_VAUXHALL[k] for k in ("VX-OHV-1.2", "VX-OHV-1.3", "VX-SL-1.6")}
FAMILLES = {**HOLDEN, **CHEV, **BUICK, **PONT, **OPEL, **DAEWOO, **VAUX}


def motoriste(fam):
    if fam in CHEV or fam in PONT:
        return "Chevrolet"
    if fam in BUICK:
        return "Buick"
    if fam in OPEL:
        return "Fiat" if fam == "FIAT-1.9TID" else "Opel"
    if fam in DAEWOO:
        return "Daewoo"
    if fam in VAUX:
        return "Vauxhall"
    if fam.startswith("RB30"):
        return "Nissan"
    if fam.startswith("ISUZU"):
        return "Isuzu"
    return "Holden"


mg = SaisieMoteurs(FAMILLES, "Holden", motoriste)
L = []
IND = "marché australien ; données indicatives"

# ---------------------------------------------------------------- 1948-1968
mg(L, "Holden", "48-215 (FX)", "1", "1948-11", "1953-10", [("2.2 L6 61", "HOLDEN-GREY-2.2", 152)], portes=4, places=6, reservoir=45,
   remarques="Première Holden, six cylindres « Grey motor » ; berline et ute ; " + IND)
mg(L, "Holden", "FJ", "1", "1953-10", "1956-07", [("2.2 L6 61", "HOLDEN-GREY-2.2", 152)], portes=4, places=6, reservoir=45, remarques="Standard, Business et Special ; " + IND)
mg(L, "Holden", "FE", "1", "1956-07", "1958-05", [("2.2 L6 72", "HOLDEN-GREY-2.2", 163)], portes=4, places=6, reservoir=45, remarques="Berline et break Station Sedan ; " + IND)
mg(L, "Holden", "FC", "1", "1958-05", "1960-01", [("2.2 L6 73", "HOLDEN-GREY-2.2", 165)], portes=4, places=6, reservoir=45, remarques=IND)
mg(L, "Holden", "FB", "1", "1960-01", "1961-05", [("2.3 L6 76", "HOLDEN-GREY-2.3", 172)], portes=4, places=6, reservoir=45, remarques=IND)
mg(L, "Holden", "EK", "1", "1961-05", "1962-07", [("2.3 L6 76", "HOLDEN-GREY-2.3", 172)], portes=4, places=6, reservoir=45, remarques="Première Holden à boîte automatique Hydramatic ; " + IND)
mg(L, "Holden", "EJ", "1", "1962-07", "1963-08", [("2.3 L6 76", "HOLDEN-GREY-2.3", 172)], portes=4, places=6, reservoir=45, remarques="Dont Premier ; " + IND)
mg(L, "Holden", "EH", "1", "1963-08", "1965-02", [("2.4 L6 101", "HOLDEN-RED-2.4", 190), ("2.9 L6 116", "HOLDEN-RED-2.9", 237), ("2.9 L6 X7 142", "HOLDEN-RED-2.9", 255)],
   portes=4, places=6, reservoir=45, remarques="Premier six cylindres « Red motor » ; " + IND)
mg(L, "Holden", "HD", "1", "1965-02", "1966-04", [("2.4 L6 101", "HOLDEN-RED-2.4", 190), ("2.9 L6 116", "HOLDEN-RED-2.9", 237), ("2.9 L6 X2 142", "HOLDEN-RED-2.9", 255)],
   portes=4, places=6, reservoir=45, remarques=IND)
mg(L, "Holden", "HR", "1", "1966-04", "1968-01", [("2.6 L6 116", "HOLDEN-RED-2.6", 210), ("3.0 L6 147", "HOLDEN-RED-3.0", 255), ("3.0 L6 X2 162", "HOLDEN-RED-3.0", 272)],
   portes=4, places=6, reservoir=45, remarques=IND)

# ---------------------------------------------------------------- Kingswood / Belmont / Premier (HK - HZ)
mg(L, "Kingswood", "HK", "1", "1968-01", "1969-08", [("2.6 L6 116", "HOLDEN-RED-2.6", 210), ("3.0 L6 147", "HOLDEN-RED-3.0", 255), ("3.0 L6 S 162", "HOLDEN-RED-3.0", 272),
                                                      ("5.0 V8 213", "CHEV-307-5.0", 407)], portes=4, places=6, reservoir=55,
   remarques="Belmont, Kingswood et Premier ; premier V8 (Chevrolet 307) ; " + IND)
mg(L, "Kingswood", "HT", "1", "1969-05", "1970-06", [("2.6 L6 116", "HOLDEN-RED-2.6", 210), ("3.0 L6 147", "HOLDEN-RED-3.0", 255), ("4.2 V8 188", "HOLDEN-V8-4.2", 355),
                                                      ("5.0 V8 243", "HOLDEN-V8-5.0", 427)], portes=4, places=6, reservoir=55, remarques="Premiers V8 Holden 253 et 308 ; " + IND)
mg(L, "Kingswood", "HG", "1", "1970-06", "1971-07", [("2.8 L6 117", "HOLDEN-RED-2.8", 237), ("3.3 L6 137", "HOLDEN-6-3.3", 264), ("4.2 V8 188", "HOLDEN-V8-4.2", 355),
                                                      ("5.0 V8 243", "HOLDEN-V8-5.0", 427)], portes=4, places=6, reservoir=55, remarques=IND)
mg(L, "Kingswood", "HQ", "1", "1971-07", "1974-10", [("2.8 L6 117", "HOLDEN-RED-2.8", 237), ("3.3 L6 137", "HOLDEN-6-3.3", 264), ("4.2 V8 188", "HOLDEN-V8-4.2", 355),
                                                      ("5.0 V8 243", "HOLDEN-V8-5.0", 427), ("5.7 V8 279", "SBC-5.7", 488)],
   portes=4, places=6, reservoir=75, remarques="Holden la plus vendue (près de 486 000 ex.), berline, break, ute ; " + IND)
mg(L, "Kingswood", "HJ", "1", "1974-10", "1976-06", [("2.8 L6 117", "HOLDEN-RED-2.8", 237), ("3.3 L6 137", "HOLDEN-6-3.3", 264), ("4.2 V8 188", "HOLDEN-V8-4.2", 355),
                                                      ("5.0 V8 243", "HOLDEN-V8-5.0", 427)], portes=4, places=6, reservoir=75, remarques=IND)
mg(L, "Kingswood", "HX", "1", "1976-07", "1977-10", [("3.3 L6 118", "HOLDEN-6-3.3", 255), ("4.2 V8 137", "HOLDEN-V8-4.2", 300), ("5.0 V8 163", "HOLDEN-V8-5.0", 360)],
   portes=4, places=6, reservoir=75, remarques="Normes antipollution ADR 27A, puissances nettes ; " + IND)
mg(L, "Kingswood", "HZ", "1", "1977-10", "1980-03", [("3.3 L6 118", "HOLDEN-6-3.3", 255), ("4.2 V8 137", "HOLDEN-V8-4.2", 300), ("5.0 V8 171", "HOLDEN-V8-5.0", 370)],
   portes=4, places=6, reservoir=75, remarques="Suspension « Radial Tuned » ; " + IND)

# ---------------------------------------------------------------- Monaro
mg(L, "Monaro", "HK", "1", "1968-07", "1969-05", [("3.0 L6 147", "HOLDEN-RED-3.0", 255), ("GTS 5.0 V8 213", "CHEV-307-5.0", 407), ("GTS 327 5.4 V8 253", "SBC-5.4", 441)],
   portes=2, places=5, reservoir=55, remarques="Coupé, victoire à Bathurst 1968 (GTS 327) ; " + IND)
mg(L, "Monaro", "HT", "1", "1969-05", "1970-06", [("4.2 V8 188", "HOLDEN-V8-4.2", 355), ("5.0 V8 243", "HOLDEN-V8-5.0", 427), ("GTS 350 5.7 V8 304", "SBC-5.7", 515)],
   portes=2, places=5, reservoir=55, remarques=IND)
mg(L, "Monaro", "HG", "1", "1970-06", "1971-07", [("4.2 V8 188", "HOLDEN-V8-4.2", 355), ("5.0 V8 243", "HOLDEN-V8-5.0", 427), ("GTS 350 5.7 V8 304", "SBC-5.7", 515)],
   portes=2, places=5, reservoir=55, remarques=IND)
mg(L, "Monaro", "HQ", "1", "1971-07", "1976-06", [("5.0 V8 243", "HOLDEN-V8-5.0", 427), ("GTS 350 5.7 V8 279", "SBC-5.7", 488, {"fin": "1974-10"})],
   portes=2, places=5, reservoir=75, remarques="Coupé et GTS berline 4 portes, puis HJ (1974-1976) ; " + IND)
mg(L, "Monaro", "V2", "1", "2001-11", "2005-12",
   [("CV6 3.8 V6 207", "GM-3800", 305, {"fin": "2004-08"}), ("CV8 5.7 V8 306", "LS1-5.7", 460, {"fin": "2003-06"}), ("CV8 5.7 V8 333", "LS1-5.7", 465, {"debut": "2003-07", "fin": "2004-12"}),
    ("CV8-Z 6.0 V8 354", "LS2-6.0", 510, {"debut": "2004-09"})],
   portes=2, places=4, reservoir=75, remarques="Coupé sur base Commodore VT/VX/VY/VZ ; exporté comme Pontiac GTO et Vauxhall Monaro ; " + IND)

# ---------------------------------------------------------------- Statesman / Caprice
for modele in ("Statesman", "Caprice"):
    if modele == "Statesman":
        mg(L, modele, "HQ / HJ", "1", "1971-07", "1976-06", [("4.2 V8 188", "HOLDEN-V8-4.2", 355), ("5.0 V8 243", "HOLDEN-V8-5.0", 427), ("5.7 V8 279", "SBC-5.7", 488, {"fin": "1974-10"})],
           portes=4, places=5, reservoir=75, remarques="Statesman De Ville et Caprice (vendus sans le nom Holden jusqu'en 1980) ; " + IND)
        mg(L, modele, "HX / HZ", "1", "1976-07", "1980-03", [("4.2 V8 137", "HOLDEN-V8-4.2", 300), ("5.0 V8 171", "HOLDEN-V8-5.0", 370)], portes=4, places=5, reservoir=75, remarques=IND)
        mg(L, modele, "WB", "1", "1980-04", "1984-08", [("3.3 L6 118", "HOLDEN-6-3.3", 255), ("4.2 V8 137", "HOLDEN-V8-4.2", 300), ("5.0 V8 171", "HOLDEN-V8-5.0", 370)],
           portes=4, places=5, reservoir=75, remarques="Statesman De Ville et Caprice ; dernière plateforme HQ ; " + IND)
    R = "Statesman et Caprice (version la plus luxueuse) ; " + IND
    mg(L, modele, "VQ", "1", "1990-03", "1994-01", [("5.0 V8 224", "HOLDEN-V8-5.0", 385), ("3.8 V6 170", "GM-3800", 292)], portes=4, places=5, reservoir=80, remarques=R)
    mg(L, modele, "VR / VS", "1", "1994-01", "1999-06", [("3.8 V6 Compresseur 224", "GM-3800-SC", 380), ("5.0 V8 228", "HOLDEN-V8-5.0", 395)], portes=4, places=5, reservoir=80, remarques=R)
    mg(L, modele, "WH", "1", "1999-06", "2003-06", [("3.8 V6 Compresseur 233", "GM-3800-SC", 375), ("5.7 V8 306", "LS1-5.7", 460)], portes=4, places=5, reservoir=75, remarques=R)
    mg(L, modele, "WK", "1", "2003-06", "2004-08", [("3.8 V6 Compresseur 233", "GM-3800-SC", 375), ("5.7 V8 320", "LS1-5.7", 465)], portes=4, places=5, reservoir=75, remarques=R)
    mg(L, modele, "WL", "1", "2004-08", "2006-07", [("3.6 V6 258", "GM-3.6-V6", 340), ("5.7 V8 333", "LS1-5.7", 465, {"fin": "2005-06"}), ("6.0 V8 354", "LS2-6.0", 510, {"debut": "2005-07"})],
       portes=4, places=5, reservoir=75, remarques=R)
    mg(L, modele, "WM", "1", "2006-08", "2013-05", [("3.6 V6 265", "GM-3.6-V6", 340, {"fin": "2009-08"}), ("3.6 V6 SIDI 286", "GM-3.6-V6", 350, {"debut": "2009-09"}),
                                                     ("6.0 V8 354", "L76-6.0", 510)], portes=4, places=5, reservoir=73, remarques=R + " ; exporté comme Chevrolet Caprice (Moyen-Orient)")
    mg(L, modele, "WN", "1", "2013-06", "2017-10", [("3.6 V6 SIDI 286", "GM-3.6-V6", 350), ("6.0 V8 354", "L76-6.0", 510)], portes=4, places=5, reservoir=73,
       remarques=R + " ; WN Statesman arrêtée en 2016, Caprice jusqu'en 2017")

# ---------------------------------------------------------------- Torana / Sunbird
mg(L, "Torana", "HB", "1", "1967-05", "1969-10", [("1.2 53", "VX-OHV-1.2", 83), ("Brabham 1.2 70", "VX-OHV-1.2", 92, {"debut": "1968-01"})], portes=2, places=4, reservoir=36,
   remarques="Dérivée de la Vauxhall Viva HB ; " + IND)
mg(L, "Torana", "LC", "1", "1969-10", "1972-02", [("1.2 53", "VX-OHV-1.2", 83), ("2.25 L6 96", "HOLDEN-RED-2.25", 172), ("2.6 L6 116", "HOLDEN-RED-2.6", 210),
                                                  ("GTR XU-1 3.0 L6 162", "HOLDEN-RED-3.0", 272, {"debut": "1970-08"})], portes=4, places=5, reservoir=45, remarques=IND)
mg(L, "Torana", "LJ", "1", "1972-02", "1974-03", [("1.3 54", "VX-OHV-1.3", 89), ("1.6 73", "VX-SL-1.6", 121), ("2.8 L6 117", "HOLDEN-RED-2.8", 237), ("3.3 L6 137", "HOLDEN-6-3.3", 264),
                                                  ("GTR XU-1 3.3 L6 193", "HOLDEN-6-3.3", 289)], portes=4, places=5, reservoir=45, remarques="Victoire à Bathurst 1972 (GTR XU-1) ; " + IND)
mg(L, "Torana", "LH", "1", "1974-03", "1976-02", [("1.9 90", "CIH-1.9", 147), ("3.3 L6 137", "HOLDEN-6-3.3", 264), ("4.2 V8 188", "HOLDEN-V8-4.2", 355),
                                                  ("SL/R 5000 5.0 V8 243", "HOLDEN-V8-5.0", 427)], portes=4, places=5, reservoir=53, remarques="Quatre cylindres Opel CIH 1.9 ; " + IND)
mg(L, "Torana", "LX", "1", "1976-02", "1978-02", [("1.9 90", "CIH-1.9", 147), ("3.3 L6 118", "HOLDEN-6-3.3", 255), ("4.2 V8 137", "HOLDEN-V8-4.2", 300),
                                                  ("SS / A9X 5.0 V8 163", "HOLDEN-V8-5.0", 360)], portes=3, places=5, reservoir=53,
   remarques="Berline et hatchback, dont A9X (homologation Bathurst) ; Sunbird quatre cylindres ; " + IND)
mg(L, "Torana", "UC", "1", "1978-03", "1980-01", [("1.9 78", "HOLDEN-STARFIRE-1.9", 140), ("3.3 L6 118", "HOLDEN-6-3.3", 255)], portes=4, places=5, reservoir=53,
   remarques="Torana et Sunbird ; " + IND)

# ---------------------------------------------------------------- Gemini / Camira
mg(L, "Gemini", "TX - TG", "1", "1975-03", "1985-02", [("1.6 68", "ISUZU-G161-1.6", 115), ("1.8 D 50", "ISUZU-4FB1-1.8D", 103, {"debut": "1981-01"})],
   portes=4, places=5, reservoir=50, remarques="Base Isuzu Gemini / Opel Kadett C, berline, coupé et break ; voiture de l'année Wheels 1975 ; " + IND)
mg(L, "Gemini", "RB", "1", "1985-08", "1987-12", [("1.5 73", "ISUZU-4XC1-1.5", 118)], portes=4, places=5, reservoir=50, remarques="Isuzu Gemini JT à traction ; " + IND)
mg(L, "Camira", "JB - JE", "1", "1982-08", "1989-06", [("1.6 86", "FAM2-1.6", 129, {"fin": "1984-07"}), ("1.8 115", "FAM2-1.8", 150, {"debut": "1984-08", "fin": "1987-07"}),
                                                      ("2.0 115", "FAM2-2.0", 170, {"debut": "1987-08"})], portes=4, places=5, reservoir=55,
   remarques="Plateforme GM J (Opel Ascona C), berline et break ; voiture de l'année Wheels 1982 ; " + IND)

# ---------------------------------------------------------------- Commodore
mg(L, "Commodore", "VB", "1", "1978-11", "1980-03", [("2.85 L6 87", "HOLDEN-RED-2.8", 207), ("3.3 L6 118", "HOLDEN-6-3.3", 255), ("4.2 V8 137", "HOLDEN-V8-4.2", 300),
                                                      ("5.0 V8 171", "HOLDEN-V8-5.0", 370)],
   portes=4, places=5, reservoir=63, remarques="Base Opel Rekord E / Senator, berline ; voiture de l'année Wheels 1978 ; " + IND)
mg(L, "Commodore", "VC", "1", "1980-03", "1981-09", [("1.9 78", "HOLDEN-STARFIRE-1.9", 140), ("2.85 L6 102", "HOLDEN-RED-2.8", 215), ("3.3 L6 112", "HOLDEN-6-3.3", 250),
                                                      ("4.2 V8 129", "HOLDEN-V8-4.2", 290), ("5.0 V8 171", "HOLDEN-V8-5.0", 370)], portes=4, places=5, reservoir=63,
   remarques="Six cylindres « Blue » ; berline et break ; " + IND)
mg(L, "Commodore", "VH", "1", "1981-09", "1984-03", [("1.9 78", "HOLDEN-STARFIRE-1.9", 140), ("2.85 L6 102", "HOLDEN-RED-2.8", 215), ("3.3 L6 116", "HOLDEN-6-3.3", 250),
                                                      ("4.2 V8 129", "HOLDEN-V8-4.2", 290), ("SS 5.0 V8 171", "HOLDEN-V8-5.0", 370)], portes=4, places=5, reservoir=63, remarques=IND)
mg(L, "Commodore", "VK", "1", "1984-03", "1986-02", [("3.3 L6 117", "HOLDEN-6-3.3", 255), ("3.3 L6 EFI 144", "HOLDEN-6-3.3", 265), ("5.0 V8 167", "HOLDEN-V8-5.0", 360)],
   portes=4, places=5, reservoir=63, remarques="Six cylindres « Black », injection ; Calais ; " + IND)
mg(L, "Commodore", "VL", "1", "1986-02", "1988-08", [("3.0 L6 155", "RB30E-3.0", 247), ("3.0 L6 Turbo 204", "RB30ET-3.0T", 296), ("5.0 V8 166", "HOLDEN-V8-5.0", 360),
                                                      ("SS Group A 5.0 V8 245", "HOLDEN-V8-5.0", 400, {"debut": "1988-01", "remarques": "SS Group A SV (Walkinshaw), homologation"})],
   portes=4, places=5, reservoir=63, remarques="Six cylindres Nissan RB30 ; " + IND)
mg(L, "Commodore", "VN", "1", "1988-08", "1991-09", [("3.8 V6 170", "GM-3800", 292), ("5.0 V8 224", "HOLDEN-V8-5.0", 385)], portes=4, places=5, reservoir=63,
   remarques="Plateforme élargie (Opel Omega / Senator), V6 Buick 3800 ; voiture de l'année Wheels 1988 ; " + IND)
mg(L, "Commodore", "VP", "1", "1991-09", "1993-08", [("3.8 V6 173", "GM-3800", 305), ("5.0 V8 224", "HOLDEN-V8-5.0", 385)], portes=4, places=5, reservoir=63, remarques=IND)
mg(L, "Commodore", "VR", "1", "1993-08", "1995-04", [("3.8 V6 177", "GM-3800", 308), ("5.0 V8 224", "HOLDEN-V8-5.0", 385)], portes=4, places=5, reservoir=63,
   remarques="Voiture de l'année Wheels 1993 ; " + IND)
mg(L, "Commodore", "VS", "1", "1995-04", "1997-08", [("3.8 V6 200", "GM-3800", 312), ("3.8 V6 Compresseur 224", "GM-3800-SC", 380, {"debut": "1996-06"}), ("5.0 V8 228", "HOLDEN-V8-5.0", 395)],
   portes=4, places=5, reservoir=63, remarques="V6 Ecotec ; " + IND)
mg(L, "Commodore", "VT", "1", "1997-08", "2000-10", [("3.8 V6 200", "GM-3800", 312), ("3.8 V6 Compresseur 233", "GM-3800-SC", 375), ("5.0 V8 243", "HOLDEN-V8-5.0", 427, {"fin": "1999-06"}),
                                                      ("5.7 V8 299", "LS1-5.7", 446, {"debut": "1999-06"})],
   portes=4, places=5, reservoir=75, remarques="Base Opel Omega B, berline et break ; voiture de l'année Wheels 1997 ; " + IND)
mg(L, "Commodore", "VX", "1", "2000-10", "2002-09", [("3.8 V6 207", "GM-3800", 305), ("3.8 V6 Compresseur 233", "GM-3800-SC", 375), ("5.7 V8 306", "LS1-5.7", 460)],
   portes=4, places=5, reservoir=75, remarques=IND)
mg(L, "Commodore", "VY", "1", "2002-09", "2004-08", [("3.8 V6 207", "GM-3800", 305), ("3.8 V6 Compresseur 233", "GM-3800-SC", 375), ("5.7 V8 320", "LS1-5.7", 465),
                                                      ("SS 5.7 V8 333", "LS1-5.7", 465)], portes=4, places=5, reservoir=75, remarques=IND)
mg(L, "Commodore", "VZ", "1", "2004-08", "2007-07", [("3.6 V6 238", "GM-3.6-V6", 320), ("3.6 V6 HO 258", "GM-3.6-V6", 340), ("SS 5.7 V8 333", "LS1-5.7", 465, {"fin": "2005-06"}),
                                                      ("SS 6.0 V8 354", "LS2-6.0", 510, {"debut": "2005-07"})], portes=4, places=5, reservoir=75,
   remarques="V6 Alloytec ; " + IND)
mg(L, "Commodore", "VE", "1", "2006-08", "2009-08", [("3.6 V6 245", "GM-3.6-V6", 330), ("3.6 V6 HO 265", "GM-3.6-V6", 340), ("SS 6.0 V8 354", "L76-6.0", 510)],
   portes=4, places=5, reservoir=73, remarques="Plateforme Zeta (exportée comme Pontiac G8 et Chevrolet Lumina) ; voiture de l'année Wheels 2006 ; " + IND)
mg(L, "Commodore", "VE", "2", "2009-09", "2013-05", [("3.0 V6 SIDI 258", "GM-3.0-V6", 290), ("3.6 V6 SIDI 286", "GM-3.6-V6", 350), ("SS 6.0 V8 367", "L76-6.0", 530)],
   portes=4, places=5, reservoir=73, remarques="VE Series II, injection directe SIDI ; " + IND)
mg(L, "Commodore", "VF", "1", "2013-06", "2017-10", [("3.0 V6 SIDI 258", "GM-3.0-V6", 290), ("3.6 V6 SIDI 286", "GM-3.6-V6", 350), ("SS 6.0 V8 354", "L76-6.0", 510, {"fin": "2015-09"}),
                                                      ("SS 6.2 V8 413", "LS3-6.2", 570, {"debut": "2015-10"})], portes=4, places=5, reservoir=71,
   remarques="Dernière Holden produite en Australie (20 octobre 2017) ; VF II 6.2 LS3 ; " + IND)
mg(L, "Commodore", "ZB", "1", "2018-02", "2020-02", [("2.0 Turbo 260", "A20NHT-2.0T", 400), ("3.6 V6 AWD 318", "GM-3.6-V6", 381), ("2.0 D 170", "A20DTH-2.0CDTI", 400)],
   portes=5, places=5, reservoir=62, remarques="Opel Insignia B importée d'Allemagne (Liftback et Sportwagon) ; " + IND)

# ---------------------------------------------------------------- HSV
mg(L, "HSV Clubsport", "VN - VS", "1", "1990-08", "1997-08", [("5.0 V8 245", "HOLDEN-V8-5.0", 400, {"fin": "1993-08"}), ("5.0 V8 252", "HOLDEN-V8-5.0", 410, {"debut": "1993-09"})],
   portes=4, places=5, reservoir=63, remarques="Holden Special Vehicles (Tom Walkinshaw) ; " + IND)
mg(L, "HSV Clubsport", "VT - VY", "1", "1997-09", "2004-08", [("5.7 V8 340", "LS1-5.7", 475, {"debut": "1999-06", "fin": "2002-09"}), ("5.0 V8 260", "HOLDEN-V8-5.0", 420, {"fin": "1999-06"}),
                                                              ("5.7 V8 388", "LS1-5.7", 510, {"debut": "2002-10"})], portes=4, places=5, reservoir=75, remarques=IND)
mg(L, "HSV Clubsport", "VZ", "1", "2004-08", "2006-07", [("6.0 V8 404", "LS2-6.0", 530)], portes=4, places=5, reservoir=75, remarques=IND)
mg(L, "HSV Clubsport", "E-Series", "1", "2006-08", "2013-05", [("R8 6.0 V8 417", "LS2-6.0", 550, {"fin": "2008-08"}), ("R8 6.2 V8 431", "LS3-6.2", 550, {"debut": "2008-09", "fin": "2011-08"}),
                                                               ("R8 6.2 V8 442", "LS3-6.2", 550, {"debut": "2011-09"})], portes=4, places=5, reservoir=73, remarques="Base Commodore VE ; " + IND)
mg(L, "HSV Clubsport", "Gen-F", "1", "2013-06", "2017-12", [("R8 6.2 V8 462", "LS3-6.2", 570), ("R8 LSA 6.2 V8 Compresseur 544", "LSA-6.2SC", 671, {"debut": "2015-10"})],
   portes=4, places=5, reservoir=71, remarques="Base Commodore VF ; " + IND)
mg(L, "HSV GTS", "VP - VS", "1", "1992-09", "1997-08", [("5.7 V8 292", "HOLDEN-V8-5.7", 475)], portes=4, places=5, reservoir=63, remarques="V8 Holden porté à 5,7 l ; " + IND)
mg(L, "HSV GTS", "VT - VY", "1", "1998-06", "2004-08", [("5.7 V8 347", "LS1-5.7", 475, {"fin": "2002-09"}), ("5.7 V8 408", "LS1-5.7", 510, {"debut": "2002-10"})], portes=4, places=5,
   reservoir=75, remarques="Dont GTS 300 kW (LS1 C4B) ; " + IND)
mg(L, "HSV GTS", "VZ", "1", "2004-08", "2006-07", [("6.0 V8 404", "LS2-6.0", 530)], portes=4, places=5, reservoir=75, remarques=IND)
mg(L, "HSV GTS", "E-Series", "1", "2006-08", "2013-05", [("6.0 V8 417", "LS2-6.0", 550, {"fin": "2008-08"}), ("6.2 V8 431", "LS3-6.2", 550, {"debut": "2008-09", "fin": "2011-08"}),
                                                         ("6.2 V8 442", "LS3-6.2", 550, {"debut": "2011-09"})], portes=4, places=5, reservoir=73,
   remarques="Exportée comme Vauxhall VXR8 ; " + IND)
mg(L, "HSV GTS", "Gen-F", "1", "2013-06", "2017-12", [("6.2 V8 Compresseur 585", "LSA-6.2SC", 740), ("GTSR W1 6.2 V8 Compresseur 645", "LS9-6.2SC", 815, {"debut": "2017-01", "remarques": "GTSR W1, 300 exemplaires"})],
   portes=4, places=5, reservoir=71, remarques="Base Commodore VF ; " + IND)

# ---------------------------------------------------------------- importations GM
mg(L, "Barina", "SB", "1", "1994-04", "2000-12", [("1.4 82", "FAM1-1.4", 125), ("GSi 1.6 109", "FAM1-1.6", 148)], portes=3, places=5, reservoir=46,
   remarques="Opel Corsa B (Espagne) ; " + IND)
mg(L, "Barina", "XC", "1", "2001-03", "2005-11", [("1.4 90", "FAM0-1.4", 125), ("SRi 1.8 125", "FAM2-1.8-16V", 170)], portes=3, places=5, reservoir=44,
   remarques="Opel Corsa C ; " + IND)
mg(L, "Barina", "TK", "1", "2005-12", "2011-09", [("1.6 103", "ETEC-1.6", 145)], portes=5, places=5, reservoir=45, remarques="Daewoo Kalos / Chevrolet Aveo (Corée) ; " + IND)
mg(L, "Barina", "TM", "1", "2011-10", "2018-12", [("1.6 115", "ECOTEC-1.6", 155), ("RS 1.4 Turbo 140", "ECOTEC-1.4T", 200, {"debut": "2016-01"})], portes=5, places=5, reservoir=46,
   remarques="Chevrolet Aveo / Sonic (Corée) ; " + IND)
mg(L, "Astra", "TR", "1", "1996-01", "1998-10", [("1.6 101", "FAM1-1.6", 150), ("1.8 16V 116", "FAM2-1.8-16V", 170)], portes=5, places=5, reservoir=52, remarques="Opel Astra F ; " + IND)
mg(L, "Astra", "TS", "1", "1998-10", "2005-10", [("1.8 16V 125", "FAM2-1.8-16V", 170), ("2.2 16V 147", "FAM2-2.2", 203, {"debut": "2001-09"}), ("SRi Turbo 2.0 200", "FAM2-2.0T", 250, {"debut": "2003-01"})],
   portes=5, places=5, reservoir=52, remarques="Opel Astra G, dont coupé et cabriolet Bertone ; " + IND)
mg(L, "Astra", "AH", "1", "2004-09", "2010-08", [("1.8 140", "ECOTEC-1.8", 175), ("SRi Turbo 2.0 200", "FAM2-2.0T", 250), ("1.9 CDTi 150", "FIAT-1.9TID", 320, {"debut": "2006-01"})],
   portes=5, places=5, reservoir=52, remarques="Opel Astra H ; " + IND)
mg(L, "Astra", "BK", "1", "2017-01", "2020-06", [("1.4 Turbo 150", "B14XFT-1.4T", 245), ("RS 1.6 Turbo 200", "A16XHT-1.6T", 300)], portes=5, places=5, reservoir=48,
   remarques="Opel Astra K (Pologne / Royaume-Uni) ; berline Astra BL (base Cruze) non reprise ; " + IND)
mg(L, "Vectra", "JR / JS", "1", "1997-06", "2003-02", [("2.0 16V 136", "FAM2-2.0", 185), ("2.2 16V 147", "FAM2-2.2", 203, {"debut": "2000-01"}), ("2.5 V6 170", "X25XE-2.5V6", 227)],
   portes=4, places=5, reservoir=60, remarques="Opel Vectra B, assemblée à Elizabeth puis importée ; " + IND)
mg(L, "Vectra", "ZC", "1", "2003-03", "2006-03", [("2.2 155", "FAM2-2.2", 220), ("3.2 V6 211", "Y32SE-3.2V6", 300)], portes=5, places=5, reservoir=61, remarques="Opel Vectra C ; " + IND)
mg(L, "Calibra", "YE", "1", "1991-01", "1997-12", [("2.0 16V 150", "FAM2-2.0-16V", 196), ("Turbo 4x4 2.0 204", "FAM2-2.0T", 280, {"debut": "1993-01"}), ("2.5 V6 170", "X25XE-2.5V6", 227, {"debut": "1994-01"})],
   portes=2, places=4, reservoir=65, remarques="Opel Calibra ; " + IND)
mg(L, "Viva", "JF", "1", "2005-03", "2009-12", [("1.8 122", "FAM2-1.8", 165)], portes=5, places=5, reservoir=60, remarques="Daewoo Lacetti ; " + IND)
mg(L, "Epica", "EP", "1", "2007-02", "2011-06", [("2.0 144", "XK6-2.0", 195), ("2.5 156", "XK6-2.5", 237), ("2.0 VCDi 150", "VCDI-2.0", 320, {"debut": "2008-01"})], portes=4, places=5, reservoir=65,
   remarques="Daewoo Tosca / Chevrolet Epica, six cylindres transversal ; " + IND)
mg(L, "Cruze", "JG / JH", "1", "2009-06", "2016-10",
   [("1.8 140", "ECOTEC-1.8", 175), ("1.4 Turbo 140", "ECOTEC-1.4T", 200, {"debut": "2011-03"}), ("SRi 1.6 Turbo 180", "FAM1-1.6T", 230, {"debut": "2012-03"}), ("2.0 VCDi 150", "VCDI-2.0", 320)],
   portes=4, places=5, reservoir=60, remarques="Assemblée à Elizabeth (Adélaïde) de 2011 à 2016 ; berline, hatchback et break ; " + IND)
mg(L, "Captiva", "CG", "1", "2006-09", "2018-12", [("2.4 167", "GM-2.4", 230), ("3.2 V6 227", "Y32SE-3.2V6", 297, {"fin": "2011-02"}), ("2.2 CDTi 184", "VCDI-2.2", 400, {"debut": "2011-03"}),
                                                   ("2.0 VCDi 150", "VCDI-2.0", 320, {"fin": "2011-02"})], portes=5, places=7, reservoir=65,
   remarques="Captiva 5 et 7, jumeau du Chevrolet Captiva ; V6 rattaché à la famille 3.2 Opel ; " + IND)
mg(L, "Malibu", "EM", "1", "2013-05", "2016-12", [("2.4 167", "GM-2.4", 230), ("2.0 VCDi 160", "VCDI-2.0", 350)], portes=4, places=5, reservoir=70, remarques="Chevrolet Malibu ; " + IND)
mg(L, "Trax", "TJ", "1", "2013-08", "2020-06", [("1.8 140", "ECOTEC-1.8", 175), ("1.4 Turbo 140", "ECOTEC-1.4T", 200)], portes=5, places=5, reservoir=53, remarques="Chevrolet Trax ; " + IND)
mg(L, "Equinox", "EQ", "1", "2017-11", "2020-06", [("1.5 Turbo 173", "GM-1.5T", 275), ("2.0 Turbo 256", "GM-2.0T", 400)], portes=5, places=5, reservoir=59, remarques="Chevrolet Equinox (Mexique) ; " + IND)
mg(L, "Acadia", "AC", "1", "2018-10", "2020-06", [("3.6 V6 314", "GM-3.6-V6", 361)], portes=5, places=7, reservoir=73, remarques="GMC Acadia (États-Unis) ; " + IND)

MOT = Motorisations("Holden", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Holden": L}
MOTEURS = MOT.moteurs()
