"""Land Rover et Range Rover : générations, phases, motorisations (marché européen) et moteurs liés.
Land Rover : Series I, II, IIA, III, Defender (90/110/130 puis L663), Discovery (I, II, 3, 4, 5), Discovery Sport, Freelander
(L314, L359). Range Rover : Range Rover (Classic, P38A, L322, L405, L460, Electric), Range Rover Sport (L320, L494, L461),
Range Rover Velar, Range Rover Evoque (L538, L551). Le Range Rover est rangé sous la marque « Range Rover ».
Moteurs : Jaguar (AJ-V8, AJ133, AJ126, V6 diesel, Ingenium) repris de jaguar.py (motoriste « Jaguar ») ; BMW (bmw.py),
Ford (ford.py), Peugeot/PSA (peugeot.py), Volvo (volvo.py), VM (alfa_romeo.py, motoriste « Fiat ») et V8 Rover (ginetta.py)
avec leurs codes ; moteurs Land Rover propres au motoriste « Land Rover ». Données anciennes indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .alfa_romeo import FAMILLES as FAMILLES_ALFA
from .bmw import FAMILLES as FAMILLES_BMW
from .ford import FAMILLES as FAMILLES_FORD
from .ginetta import FAMILLES as FAMILLES_GINETTA
from .jaguar import FAMILLES as FAMILLES_JAGUAR
from .peugeot import FAMILLES as FAMILLES_PEUGEOT
from .volvo import FAMILLES as FAMILLES_VOLVO

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

PROPRES = {
    "LR-1.6P": f("ATM", E_, 1.6, C, 4, 4000, 2000, "20W50", 5.0, 3000),
    "LR-2.0P": f("ATM", E_, 2.0, C, 4, 4000, 2000, "20W50", 5.5, 3000),
    "LR-2.25P": f("ATM", E_, 2.25, C, 4, 4250, 2500, "20W50", 6.0, 5000),
    "LR-2.6-I6": f("ATM", E_, 2.6, C, 6, 4500, 1500, "20W50", 6.5, 5000),
    "LR-2.0D": f("ATM", D, 2.0, C, 4, 3500, 2000, "20W50", 6.0, 5000),
    "LR-2.25D": f("ATM", D, 2.25, C, 4, 4000, 1800, "20W50", 6.0, 5000),
    "LR-2.5D": f("ATM", D, 2.5, B, 4, 4000, 1800, "15W40", 6.0, 5000),
    "LR-2.5TD": f("TURBO", D, 2.5, B, 4, 4000, 1800, "15W40", 6.0, 5000),
    "LR-200TDI": f("TURBO", D, 2.5, B, 4, 3800, 1800, "15W40", 6.0, 10000),
    "LR-300TDI": f("TURBO", D, 2.5, B, 4, 4000, 1800, "15W40", 6.0, 10000),
    "LR-TD5": f("TURBO", D, 2.5, C, 5, 4200, 1950, "10W40", 7.0, 20000),
    "ROVER-V8-3.5": f("ATM", E_, 3.5, C, 8, 4750, 2600, "10W40", 5.0, 10000, a="V"),
    "ROVER-V8-4.0": f("ATM", E_, 4.0, C, 8, 4750, 3000, "10W40", 5.0, 10000, a="V"),
    "ROVER-V8-4.2": f("ATM", E_, 4.2, C, 8, 4850, 3250, "10W40", 5.0, 10000, a="V"),
    "ROVER-V8-4.6": f("ATM", E_, 4.6, C, 8, 4750, 3000, "10W40", 5.0, 10000, a="V"),
    "ROVER-T16-2.0": f("ATM", E_, 2.0, B, 4, 6000, 2500, "10W40", 4.5, 10000),
    "ROVER-K-1.8": f("ATM", E_, 1.8, B, 4, 5500, 2750, "10W40", 4.5, 15000),
    "ROVER-KV6-2.5": f("ATM", E_, 2.5, B, 6, 6250, 4000, "10W40", 5.0, 15000, a="V"),
    "ROVER-L-2.0DI": f("TURBO", D, 2.0, B, 4, 4200, 2000, "10W40", 5.0, 15000),
    "FORD-PUMA-2.4": f("TURBO", D, 2.4, C, 4, 3500, 2000, "5W30", 6.5, 20000),
    "TDV8-3.6": f("TURBO", D, 3.6, B, 8, 4000, 2000, "5W30", 9.0, 20000, a="V"),
    "SDV8-4.4": f("TURBO", D, 4.4, C, 8, 3500, 1750, "5W30", 9.5, 20000, a="V"),
    "AJ-V8-4.4": f("ATM", E_, 4.4, C, 8, 5500, 4000, "5W30", 7.0, 20000, a="V"),
    "AJV6D-3.0-HYB": f("HYB_TE", D, 3.0, B, 6, 4000, 1500, "0W30", 6.0, 20000, a="V"),
    "AJ300P-PHEV": f("HYB_E", E_, 3.0, C, 6, 5500, 1500, "0W20", 7.0, 21000),
    "LR-EV": electrique(),
}
JAGUAR = {k: FAMILLES_JAGUAR[k] for k in ("AJ-V8-4.2", "AJ-V8-4.2S", "AJ133-5.0", "AJ133-5.0S", "AJ126-3.0S", "AJD-V6-2.7", "AJV6D-3.0",
                                          "AJ200D", "AJ200D-MHEV", "AJ200P", "AJ200P-MHEV", "AJ200P-PHEV", "AJ300D-MHEV", "AJ300P-MHEV",
                                          "INGENIUM-1.5-PHEV")}
BMW = {k: FAMILLES_BMW[k] for k in ("M47-2.0", "M51-2.5", "M57-3.0", "M62-4.4", "N63-4.4")}
BMW_M = {"S68-4.4": FAMILLES_BMW["S68-4.4"]}
FORD = {k: FAMILLES_FORD[k] for k in ("ECOBOOST-2.0", "DURATORQ-2.2")}
PEUGEOT = {k: FAMILLES_PEUGEOT[k] for k in ("DW12C", "PUMA-2.2")}
VOLVO = {"B6324S": FAMILLES_VOLVO["B6324S"]}
VM = {k: FAMILLES_ALFA[k] for k in ("VM-2.4TD", "VM-2.5TD")}
ROVER = {"ROVER-V8-3.9": FAMILLES_GINETTA["ROVER-V8-3.9"]}
FAMILLES = {**PROPRES, **JAGUAR, **BMW, **BMW_M, **FORD, **PEUGEOT, **VOLVO, **VM, **ROVER}


def motoriste(fam):
    for groupe, nom in ((JAGUAR, "Jaguar"), (BMW, "BMW"), (BMW_M, "BMW M"), (FORD, "Ford"), (PEUGEOT, "Peugeot"), (VOLVO, "Volvo"),
                        (VM, "Fiat"), (ROVER, "Rover")):
        if fam in groupe:
            return nom
    if fam.startswith("ROVER-"):
        return "Rover"
    if fam in ("AJ-V8-4.4", "AJV6D-3.0-HYB", "AJ300P-PHEV"):
        return "Jaguar"
    return "Land Rover"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Land Rover", motoriste)
L = []

# ---------------------------------------------------------------- Series
mg(L, "Series I", "Series I", "1", "1948-04", "1958-04",
   [("1.6 50", "LR-1.6P", 108, {"fin": "1951-12"}), ("2.0 52", "LR-2.0P", 136, {"debut": "1952-01"}), ("2.0 Diesel 51", "LR-2.0D", 118, {"debut": "1957-06"})],
   portes=3, places=3, reservoir=45, remarques="Empattements 80, 86, 88, 107 et 109 pouces ; données indicatives")
mg(L, "Series II", "Series II", "1", "1958-04", "1961-09", [("2.25 72", "LR-2.25P", 167), ("2.0 Diesel 51", "LR-2.0D", 118)], portes=3, places=3, reservoir=45,
   remarques="88 et 109 pouces ; données indicatives")
mg(L, "Series IIA", "Series IIA", "1", "1961-09", "1971-09",
   [("2.25 72", "LR-2.25P", 167), ("2.25 Diesel 62", "LR-2.25D", 140), ("2.6 I6 85", "LR-2.6-I6", 180, {"debut": "1967-01"})], portes=3, places=3, reservoir=45,
   remarques="Données indicatives")
mg(L, "Series III", "Series III", "1", "1971-09", "1985-12",
   [("2.25 70", "LR-2.25P", 163), ("2.25 Diesel 62", "LR-2.25D", 140), ("2.6 I6 86", "LR-2.6-I6", 180, {"fin": "1980-12"}),
    ("Stage 1 3.5 V8 91", "ROVER-V8-3.5", 225, {"debut": "1979-01"})], portes=3, places=3, reservoir=45, remarques="Données indicatives")

# ---------------------------------------------------------------- Defender
mg(L, "Defender", "Ninety/One Ten", "1", "1983-03", "1990-09",
   [("2.5 Diesel 68", "LR-2.5D", 156, {"debut": "1984-06"}), ("2.5 Turbo D 85", "LR-2.5TD", 204, {"debut": "1986-10"}), ("2.5 83", "LR-2.25P", 180),
    ("3.5 V8 114", "ROVER-V8-3.5", 251)], portes=3, places=5, reservoir=79, remarques="Ninety, One Ten et 127 ; nommé Defender en 1990 ; données indicatives")
mg(L, "Defender", "90/110/130", "1", "1990-10", "2007-06",
   [("200Tdi 107", "LR-200TDI", 264, {"fin": "1994-06"}), ("300Tdi 111", "LR-300TDI", 265, {"debut": "1994-07", "fin": "1998-12"}),
    ("Td5 122", "LR-TD5", 300, {"debut": "1998-06"}), ("3.5 V8 134", "ROVER-V8-3.5", 255, {"fin": "1994-12"}),
    ("V8 50th 4.0 182", "ROVER-V8-4.0", 340, {"debut": "1998-01", "fin": "1998-12"})], portes=3, places=5, reservoir=75, remarques="Données indicatives")
mg(L, "Defender", "90/110/130", "2", "2007-07", "2016-01",
   [("2.4 TDCi 122", "FORD-PUMA-2.4", 360, {"fin": "2011-12"}), ("2.2 TDCi 122", "PUMA-2.2", 360, {"debut": "2012-01"})], portes=3, places=5, reservoir=75,
   remarques="Moteurs Ford Puma ; production arrêtée en janvier 2016")
mg(L, "Defender", "L663", "1", "2020-03", "2024-06",
   [("D200 3.0 MHEV 200", "AJ300D-MHEV", 500), ("D250 3.0 MHEV 249", "AJ300D-MHEV", 570), ("D300 3.0 MHEV 300", "AJ300D-MHEV", 650),
    ("P300 2.0 300", "AJ200P", 400), ("P400 3.0 MHEV 400", "AJ300P-MHEV", 550), ("P400e 2.0 PHEV 404", "AJ200P-PHEV", 640, {"debut": "2021-01", "batterie": 15}),
    ("V8 5.0 SC 525", "AJ133-5.0S", 625, {"debut": "2021-06"})], portes=5, places=5, reservoir=90, remarques="90, 110 et 130 (2022) ; produit à Nitra (Slovaquie)")
mg(L, "Defender", "L663", "2", "2024-07", None,
   [("D250 3.0 MHEV 249", "AJ300D-MHEV", 570), ("D350 3.0 MHEV 350", "AJ300D-MHEV", 700), ("P300 2.0 300", "AJ200P", 400),
    ("P425 V8 5.0 SC 425", "AJ133-5.0S", 610, {"fin": "2025-06"}), ("P400 3.0 MHEV 400", "AJ300P-MHEV", 550), ("P400e 2.0 PHEV 404", "AJ200P-PHEV", 640, {"batterie": 15}),
    ("OCTA 4.4 V8 MHEV 635", "S68-4.4", 750)], portes=5, places=5, reservoir=90, remarques="Millésime 2025 ; Defender OCTA (V8 BMW) ; données indicatives")

# ---------------------------------------------------------------- Discovery / Freelander
mg(L, "Discovery", "Series I", "1", "1989-09", "1998-11",
   [("3.5 V8 145", "ROVER-V8-3.5", 260, {"fin": "1993-12"}), ("200Tdi 111", "LR-200TDI", 265, {"fin": "1994-12"}), ("300Tdi 113", "LR-300TDI", 265, {"debut": "1995-01"}),
    ("3.9 V8 182", "ROVER-V8-3.9", 312, {"debut": "1995-01"}), ("Mpi 2.0 136", "ROVER-T16-2.0", 185, {"debut": "1993-06", "fin": "1997-12"})], portes=5, places=7,
   reservoir=89, remarques="3 et 5 portes ; restylage 1994 ; données indicatives")
mg(L, "Discovery", "Series II", "1", "1998-11", "2004-08", [("Td5 138", "LR-TD5", 300), ("4.0 V8 185", "ROVER-V8-4.0", 340)], portes=5, places=7, reservoir=95,
   remarques="Restylage 2002")
mg(L, "Discovery", "L319", "1", "2004-09", "2009-08", [("2.7 TDV6 190", "AJD-V6-2.7", 440), ("4.4 V8 300", "AJ-V8-4.4", 425)], portes=5, places=7, reservoir=86,
   remarques="Discovery 3 (LR3 en Amérique du Nord)")
mg(L, "Discovery", "L319", "2", "2009-09", "2016-12",
   [("3.0 TDV6 211", "AJV6D-3.0", 520), ("3.0 SDV6 245", "AJV6D-3.0", 600, {"fin": "2012-12"}), ("3.0 SDV6 256", "AJV6D-3.0", 600, {"debut": "2013-01"}),
    ("5.0 V8 375", "AJ133-5.0", 510, {"fin": "2013-12"})], portes=5, places=7, reservoir=82, remarques="Discovery 4 (LR4) ; restylage 2013")
mg(L, "Discovery", "L462", "1", "2017-02", "2020-12",
   [("Sd4 2.0 240", "AJ200D", 500), ("Td6 3.0 258", "AJV6D-3.0", 600), ("Si4 2.0 300", "AJ200P", 400), ("Si6 3.0 SC 340", "AJ126-3.0S", 450)], portes=5, places=7,
   reservoir=77, remarques="Discovery 5")
mg(L, "Discovery", "L462", "2", "2021-01", None,
   [("D250 3.0 MHEV 249", "AJ300D-MHEV", 570), ("D300 3.0 MHEV 300", "AJ300D-MHEV", 650), ("P360 3.0 MHEV 360", "AJ300P-MHEV", 500)], portes=5, places=7,
   reservoir=90, remarques="Restylage")
mg(L, "Discovery Sport", "L550", "1", "2015-01", "2019-08",
   [("SD4 2.2 190", "DURATORQ-2.2", 420, {"fin": "2015-12"}), ("TD4 2.0 150", "AJ200D", 380, {"debut": "2015-09"}), ("TD4 2.0 180", "AJ200D", 430, {"debut": "2015-09"}),
    ("Si4 2.0 240", "ECOBOOST-2.0", 340, {"fin": "2017-06"}), ("P250 2.0 250", "AJ200P", 365, {"debut": "2017-07"}), ("P290 2.0 290", "AJ200P", 400, {"debut": "2017-07"})],
   portes=5, places=7, reservoir=65)
mg(L, "Discovery Sport", "L550", "2", "2019-09", None,
   [("D150 2.0 MHEV 150", "AJ200D-MHEV", 380), ("D180 2.0 MHEV 180", "AJ200D-MHEV", 430), ("D200 2.0 MHEV 204", "AJ200D-MHEV", 430, {"debut": "2020-10"}),
    ("P200 2.0 MHEV 200", "AJ200P-MHEV", 320), ("P250 2.0 MHEV 249", "AJ200P-MHEV", 365), ("P300e 1.5 PHEV 309", "INGENIUM-1.5-PHEV", 540, {"debut": "2020-06", "batterie": 15})],
   portes=5, places=7, reservoir=65, remarques="Restylage (plateforme PTA) ; nouveau restylage 2024")
mg(L, "Freelander", "L314", "1", "1997-10", "2006-09",
   [("1.8 120", "ROVER-K-1.8", 165), ("2.5 V6 177", "ROVER-KV6-2.5", 240, {"debut": "2000-09"}), ("2.0 Di 98", "ROVER-L-2.0DI", 210, {"fin": "2000-12"}),
    ("2.0 Td4 112", "M47-2.0", 260, {"debut": "2000-09"})], portes=5, places=5, reservoir=59, remarques="3 et 5 portes ; restylage 2003")
mg(L, "Freelander", "L359", "1", "2006-10", "2014-12",
   [("3.2 i6 233", "B6324S", 317), ("2.2 TD4 160", "DW12C", 400), ("2.2 eD4 150", "DW12C", 420, {"debut": "2011-01"}), ("2.2 SD4 190", "DW12C", 420, {"debut": "2010-06"}),
    ("Si4 2.0 240", "ECOBOOST-2.0", 340, {"debut": "2012-09"})], portes=5, places=5, reservoir=68, remarques="Freelander 2 (LR2) ; restylages 2010 et 2012")

# ---------------------------------------------------------------- Range Rover
LR = []
mg(LR, "Range Rover", "Classic", "1", "1970-06", "1996-02",
   [("3.5 V8 132", "ROVER-V8-3.5", 252, {"fin": "1984-12"}), ("3.5 V8 Efi 165", "ROVER-V8-3.5", 280, {"debut": "1985-01", "fin": "1989-12"}),
    ("3.9 V8 185", "ROVER-V8-3.9", 319, {"debut": "1989-10"}), ("LSE 4.2 V8 200", "ROVER-V8-4.2", 340, {"debut": "1992-10"}),
    ("2.4 TD 112", "VM-2.4TD", 245, {"debut": "1986-04", "fin": "1989-12"}), ("2.5 TD 119", "VM-2.5TD", 266, {"debut": "1990-01", "fin": "1992-12"}),
    ("200Tdi 111", "LR-200TDI", 265, {"debut": "1992-06", "fin": "1994-12"}), ("300Tdi 113", "LR-300TDI", 265, {"debut": "1995-01"})], portes=5, places=5, reservoir=82,
   remarques="3 portes jusqu'en 1984, puis 5 portes ; données indicatives")
mg(LR, "Range Rover", "P38A", "1", "1994-09", "2002-02",
   [("4.0 V8 190", "ROVER-V8-4.0", 320), ("4.6 V8 225", "ROVER-V8-4.6", 380), ("2.5 DSE 136", "M51-2.5", 270)], portes=5, places=5, reservoir=100,
   remarques="Diesel BMW M51")
mg(LR, "Range Rover", "L322", "1", "2002-03", "2005-08", [("4.4 V8 286", "M62-4.4", 440), ("3.0 Td6 177", "M57-3.0", 390)], portes=5, places=5, reservoir=100,
   remarques="Moteurs BMW")
mg(LR, "Range Rover", "L322", "2", "2005-09", "2012-08",
   [("4.4 V8 306", "AJ-V8-4.4", 440, {"fin": "2009-08"}), ("4.2 V8 SC 396", "AJ-V8-4.2S", 560, {"fin": "2009-08"}), ("3.6 TDV8 272", "TDV8-3.6", 640, {"debut": "2006-09", "fin": "2010-08"}),
    ("5.0 V8 375", "AJ133-5.0", 510, {"debut": "2009-09"}), ("5.0 V8 SC 510", "AJ133-5.0S", 625, {"debut": "2009-09"}),
    ("4.4 TDV8 313", "SDV8-4.4", 700, {"debut": "2010-09"})], portes=5, places=5, reservoir=104, remarques="Moteurs Jaguar ; restylages 2005 et 2009")
mg(LR, "Range Rover", "L405", "1", "2012-09", "2021-12",
   [("3.0 TDV6 258", "AJV6D-3.0", 600), ("3.0 SDV6 Hybrid 340", "AJV6D-3.0-HYB", 700, {"debut": "2014-01", "fin": "2018-06"}), ("4.4 SDV8 339", "SDV8-4.4", 740),
    ("3.0 V6 SC 340", "AJ126-3.0S", 450, {"debut": "2014-01"}), ("5.0 V8 SC 510", "AJ133-5.0S", 625, {"fin": "2017-12"}), ("5.0 V8 SC 525", "AJ133-5.0S", 625, {"debut": "2018-01"}),
    ("SVAutobiography 5.0 V8 SC 565", "AJ133-5.0S", 700, {"debut": "2017-01"}), ("P400e 2.0 PHEV 404", "AJ200P-PHEV", 640, {"debut": "2018-01", "batterie": 13}),
    ("D350 3.0 MHEV 350", "AJ300D-MHEV", 700, {"debut": "2020-06"})], portes=5, places=5, reservoir=105, remarques="Caisse aluminium ; empattement long (2014) ; restylage 2018")
mg(LR, "Range Rover", "L460", "1", "2022-01", None,
   [("D300 3.0 MHEV 300", "AJ300D-MHEV", 650), ("D350 3.0 MHEV 350", "AJ300D-MHEV", 700), ("P400 3.0 MHEV 400", "AJ300P-MHEV", 550),
    ("P440e 3.0 PHEV 440", "AJ300P-PHEV", 620, {"debut": "2022-06", "batterie": 32}), ("P510e 3.0 PHEV 510", "AJ300P-PHEV", 700, {"debut": "2022-06", "batterie": 32}),
    ("P530 4.4 V8 Biturbo 530", "N63-4.4", 750), ("SV P615 4.4 V8 MHEV 615", "S68-4.4", 750, {"debut": "2024-06"}),
    ("Electric EV550 550", "LR-EV", 850, el(118, debut="2026-10"))], portes=5, places=5, reservoir=90,
   remarques="Empattement standard et long ; V8 BMW ; Range Rover Electric (800 V, deux moteurs de 260 kW) livré à partir de fin 2026")
mg(LR, "Range Rover Sport", "L320", "1", "2005-03", "2013-03",
   [("2.7 TDV6 190", "AJD-V6-2.7", 440, {"fin": "2009-08"}), ("3.6 TDV8 272", "TDV8-3.6", 640, {"fin": "2010-08"}), ("4.4 V8 300", "AJ-V8-4.4", 425, {"fin": "2009-08"}),
    ("4.2 V8 SC 390", "AJ-V8-4.2S", 550, {"fin": "2009-08"}), ("3.0 TDV6 211", "AJV6D-3.0", 520, {"debut": "2009-09"}), ("3.0 SDV6 256", "AJV6D-3.0", 600, {"debut": "2009-09"}),
    ("5.0 V8 375", "AJ133-5.0", 510, {"debut": "2009-09"}), ("5.0 V8 SC 510", "AJ133-5.0S", 625, {"debut": "2009-09"})], portes=5, places=5, reservoir=88,
   remarques="Restylage 2009")
mg(LR, "Range Rover Sport", "L494", "1", "2013-04", "2022-03",
   [("2.0 SD4 240", "AJ200D", 500, {"debut": "2016-01"}), ("3.0 TDV6 258", "AJV6D-3.0", 600), ("3.0 SDV6 306", "AJV6D-3.0", 700),
    ("3.0 SDV6 Hybrid 340", "AJV6D-3.0-HYB", 700, {"debut": "2014-06", "fin": "2018-06"}), ("4.4 SDV8 339", "SDV8-4.4", 740),
    ("3.0 V6 SC 340", "AJ126-3.0S", 450), ("3.0 V6 SC 380", "AJ126-3.0S", 450), ("5.0 V8 SC 510", "AJ133-5.0S", 625),
    ("SVR 5.0 V8 SC 550", "AJ133-5.0S", 680, {"debut": "2015-01", "fin": "2017-12"}), ("SVR 5.0 V8 SC 575", "AJ133-5.0S", 700, {"debut": "2018-01"}),
    ("P400e 2.0 PHEV 404", "AJ200P-PHEV", 640, {"debut": "2018-01", "batterie": 13}), ("D300 3.0 MHEV 300", "AJ300D-MHEV", 650, {"debut": "2020-06"}),
    ("P400 3.0 MHEV 400", "AJ300P-MHEV", 550, {"debut": "2019-06"})], portes=5, places=5, reservoir=105, remarques="Restylage 2018")
mg(LR, "Range Rover Sport", "L461", "1", "2022-06", None,
   [("D250 3.0 MHEV 249", "AJ300D-MHEV", 600), ("D300 3.0 MHEV 300", "AJ300D-MHEV", 650), ("D350 3.0 MHEV 350", "AJ300D-MHEV", 700),
    ("P400 3.0 MHEV 400", "AJ300P-MHEV", 550), ("P440e 3.0 PHEV 440", "AJ300P-PHEV", 620, {"batterie": 32}), ("P510e 3.0 PHEV 510", "AJ300P-PHEV", 700, {"batterie": 32}),
    ("P530 4.4 V8 Biturbo 530", "N63-4.4", 750), ("SV 4.4 V8 MHEV 635", "S68-4.4", 750, {"debut": "2024-01"})], portes=5, places=5, reservoir=80,
   remarques="Range Rover Sport SV (V8 BMW) ; version électrique annoncée")
mg(LR, "Range Rover Velar", "L560", "1", "2017-07", "2020-09",
   [("D180 2.0 180", "AJ200D", 430), ("D240 2.0 240", "AJ200D", 500), ("D300 3.0 V6 300", "AJV6D-3.0", 700), ("P250 2.0 250", "AJ200P", 365),
    ("P300 2.0 300", "AJ200P", 400), ("P380 3.0 V6 SC 380", "AJ126-3.0S", 450), ("SVAutobiography Dynamic 5.0 V8 SC 550", "AJ133-5.0S", 680, {"debut": "2019-01"})],
   portes=5, places=5, reservoir=82)
mg(LR, "Range Rover Velar", "L560", "2", "2020-10", None,
   [("D200 2.0 MHEV 204", "AJ200D-MHEV", 430), ("D300 3.0 MHEV 300", "AJ300D-MHEV", 650, {"fin": "2023-06"}), ("P250 2.0 250", "AJ200P", 365),
    ("P400 3.0 MHEV 400", "AJ300P-MHEV", 550), ("P400e 2.0 PHEV 404", "AJ200P-PHEV", 640, {"batterie": 17})], portes=5, places=5, reservoir=82,
   remarques="Restylages 2020 et 2023 ; version électrique annoncée")
mg(LR, "Range Rover Evoque", "L538", "1", "2011-09", "2018-12",
   [("2.2 TD4 150", "DURATORQ-2.2", 400, {"fin": "2015-08"}), ("2.2 SD4 190", "DURATORQ-2.2", 420, {"fin": "2015-08"}), ("Si4 2.0 240", "ECOBOOST-2.0", 340, {"fin": "2017-06"}),
    ("eD4 2.0 150", "AJ200D", 380, {"debut": "2015-09"}), ("TD4 2.0 180", "AJ200D", 430, {"debut": "2015-09"}), ("P250 2.0 250", "AJ200P", 365, {"debut": "2017-07"})],
   portes=5, places=5, reservoir=70, remarques="Coupé 3 portes et 5 portes ; cabriolet (2016) ; restylage 2015")
mg(LR, "Range Rover Evoque", "L551", "1", "2019-02", None,
   [("D150 2.0 MHEV 150", "AJ200D-MHEV", 380), ("D200 2.0 MHEV 204", "AJ200D-MHEV", 430), ("P200 2.0 MHEV 200", "AJ200P-MHEV", 320),
    ("P250 2.0 MHEV 249", "AJ200P-MHEV", 365), ("P300e 1.5 PHEV 309", "INGENIUM-1.5-PHEV", 540, {"debut": "2020-06", "batterie": 15})], portes=5, places=5, reservoir=65,
   remarques="Plateforme PTA ; restylage 2023")

MOT = Motorisations("Land Rover", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LR)

DETAIL = {"Land Rover": L, "Range Rover": LR}
MOTEURS = MOT.moteurs()
