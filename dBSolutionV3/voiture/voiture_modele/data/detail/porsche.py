"""Porsche : générations, phases (2 = restylage / « .2 »), motorisations (marché européen) et moteurs liés.
356 et 550 à 992, transaxles (924, 944, 968, 928), Boxster/Cayman, Cayenne, Macan, Panamera, Taycan, supercars.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom.
Les moteurs d'origine Volkswagen/Audi (924, Cayenne, Macan…) sont rattachés au motoriste Porsche."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

E_, D = "ESS", "DSL"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


# ---------------------------------------------------------------- Moteurs
P = "PLAT"
FAMILLES = {
    # --- 4 cylindres à plat refroidis par air
    "356-1.1": f("ATM", E_, 1.1, "NC", 4, 4000, 2800, "20W50", 3.5, 5000, a=P),
    "356-1.3": f("ATM", E_, 1.3, "NC", 4, 4200, 2800, "20W50", 3.5, 5000, a=P),
    "356-1.5": f("ATM", E_, 1.5, "NC", 4, 5000, 3300, "20W50", 3.5, 5000, a=P),
    "616-1.6": f("ATM", E_, 1.6, "NC", 4, 5500, 3700, "20W50", 4.5, 5000, a=P),
    "547-1.5": f("ATM", E_, 1.5, "NC", 4, 6200, 5200, "20W50", 6.0, 5000, a=P),
    "587-2.0": f("ATM", E_, 2.0, "NC", 4, 6200, 4600, "20W50", 6.0, 5000, a=P),
    "T4-1.7": f("ATM", E_, 1.7, "NC", 4, 4900, 2700, "20W50", 3.5, 10000, a=P),
    "T4-1.8": f("ATM", E_, 1.8, "NC", 4, 4800, 3400, "20W50", 3.5, 10000, a=P),
    "T4-2.0": f("ATM", E_, 2.0, "NC", 4, 4900, 3500, "20W50", 3.5, 10000, a=P),
    # --- 6 cylindres à plat refroidis par air (carter sec)
    "901-2.0": f("ATM", E_, 2.0, "CHAINE", 6, 6600, 4600, "20W50", 9.0, 10000, a=P),
    "911-2.2": f("ATM", E_, 2.2, "CHAINE", 6, 6500, 5200, "20W50", 10.0, 10000, a=P),
    "911-2.4": f("ATM", E_, 2.4, "CHAINE", 6, 6300, 5200, "20W50", 10.0, 10000, a=P),
    "911-2.7": f("ATM", E_, 2.7, "CHAINE", 6, 5800, 4000, "20W50", 11.0, 10000, a=P),
    "911-3.0": f("ATM", E_, 3.0, "CHAINE", 6, 5500, 4300, "20W50", 11.0, 10000, a=P),
    "911-3.2": f("ATM", E_, 3.2, "CHAINE", 6, 5900, 4800, "20W50", 11.5, 10000, a=P),
    "930-3.0T": f("TURBO", E_, 3.0, "CHAINE", 6, 5500, 4000, "20W50", 13.0, 10000, a=P),
    "930-3.3T": f("TURBO", E_, 3.3, "CHAINE", 6, 5500, 4000, "20W50", 13.0, 10000, a=P),
    "M64-3.6": f("ATM", E_, 3.6, "CHAINE", 6, 6100, 4800, "15W50", 11.5, 20000, a=P),
    "M64-3.8": f("ATM", E_, 3.8, "CHAINE", 6, 6500, 5400, "15W50", 11.5, 20000, a=P),
    "M30-3.3T": f("TURBO", E_, 3.3, "CHAINE", 6, 5750, 4500, "15W50", 13.0, 20000, a=P),
    "M64-3.6T": f("TURBO", E_, 3.6, "CHAINE", 6, 5750, 4500, "15W50", 11.5, 20000, a=P),
    "959-2.85T": f("TURBO", E_, 2.85, "CHAINE", 6, 6500, 5500, "15W50", 18.0, 10000, a=P),
    # --- 6 cylindres à plat refroidis par eau
    "M96-2.5": f("ATM", E_, 2.5, "CHAINE", 6, 6000, 4500, "0W40", 8.75, 20000, a=P),
    "M96-2.7": f("ATM", E_, 2.7, "CHAINE", 6, 6400, 4750, "0W40", 8.75, 20000, a=P),
    "M96-3.2": f("ATM", E_, 3.2, "CHAINE", 6, 6250, 4500, "0W40", 8.75, 20000, a=P),
    "M96-3.4": f("ATM", E_, 3.4, "CHAINE", 6, 6800, 4600, "0W40", 9.75, 20000, a=P),
    "M96-3.6": f("ATM", E_, 3.6, "CHAINE", 6, 6800, 4250, "0W40", 9.75, 20000, a=P),
    "M97-2.7": f("ATM", E_, 2.7, "CHAINE", 6, 6500, 4600, "0W40", 8.75, 20000, a=P),
    "M97-3.4": f("ATM", E_, 3.4, "CHAINE", 6, 7200, 4750, "0W40", 8.75, 20000, a=P),
    "M97-3.6": f("ATM", E_, 3.6, "CHAINE", 6, 6800, 4250, "0W40", 9.75, 20000, a=P),
    "M97-3.8": f("ATM", E_, 3.8, "CHAINE", 6, 6600, 4600, "0W40", 9.75, 20000, a=P),
    "Mezger-3.6": f("ATM", E_, 3.6, "CHAINE", 6, 7600, 5500, "0W40", 10.5, 20000, a=P),
    "Mezger-3.8": f("ATM", E_, 3.8, "CHAINE", 6, 7900, 6250, "0W40", 10.5, 20000, a=P),
    "Mezger-4.0": f("ATM", E_, 4.0, "CHAINE", 6, 8250, 5750, "0W40", 10.5, 20000, a=P),
    "Mezger-3.6T": f("TURBO", E_, 3.6, "CHAINE", 6, 6000, 2700, "0W40", 10.5, 20000, a=P),
    "9A1-2.7": f("ATM", E_, 2.7, "CHAINE", 6, 6700, 4500, "0W40", 8.0, 20000, a=P),
    "9A1-2.9": f("ATM", E_, 2.9, "CHAINE", 6, 7200, 4400, "0W40", 8.0, 20000, a=P),
    "9A1-3.4": f("ATM", E_, 3.4, "CHAINE", 6, 7400, 5000, "0W40", 8.5, 20000, a=P),
    "9A1-3.6": f("ATM", E_, 3.6, "CHAINE", 6, 6500, 4400, "0W40", 8.5, 20000, a=P),
    "9A1-3.8": f("ATM", E_, 3.8, "CHAINE", 6, 7400, 5600, "0W40", 8.5, 20000, a=P),
    "9A1-3.8T": f("TURBO", E_, 3.8, "CHAINE", 6, 6000, 2100, "0W40", 9.0, 20000, a=P),
    "9A1-3.8GT": f("ATM", E_, 3.8, "CHAINE", 6, 8250, 6250, "0W40", 10.0, 15000, a=P),
    "9A1-4.0": f("ATM", E_, 4.0, "CHAINE", 6, 7600, 5000, "0W40", 9.0, 20000, a=P),
    "9A1-4.0GT": f("ATM", E_, 4.0, "CHAINE", 6, 8400, 6100, "0W40", 10.0, 15000, a=P),
    "9A2-3.0T": f("TURBO", E_, 3.0, "CHAINE", 6, 6500, 1700, "0W40", 8.5, 20000, a=P),
    "9A2-3.8T": f("TURBO", E_, 3.8, "CHAINE", 6, 6750, 2500, "0W40", 9.0, 20000, a=P),
    "9A3-3.0T": f("TURBO", E_, 3.0, "CHAINE", 6, 6500, 2000, "0W40", 8.5, 20000, a=P),
    "9A3-3.6-HYB": f("HYB_TE", E_, 3.6, "CHAINE", 6, 7500, 2000, "0W40", 9.0, 20000, a=P),
    "9A2-2.0T": f("TURBO", E_, 2.0, "CHAINE", 4, 6500, 1950, "0W40", 7.0, 20000, a=P),
    "9A2-2.5T": f("TURBO", E_, 2.5, "CHAINE", 4, 6500, 1900, "0W40", 7.0, 20000, a=P),
    # --- transaxles
    "EA831-2.0": f("ATM", E_, 2.0, "COURROIE", 4, 5800, 3500, "15W40", 5.5, 15000),
    "931-2.0T": f("TURBO", E_, 2.0, "COURROIE", 4, 5500, 3500, "15W40", 5.5, 15000),
    "M44-2.5": f("ATM", E_, 2.5, "COURROIE", 4, 5800, 3000, "15W40", 6.0, 20000),
    "M44-2.5-16V": f("ATM", E_, 2.5, "COURROIE", 4, 6000, 4300, "15W40", 6.0, 20000),
    "M44-2.7": f("ATM", E_, 2.7, "COURROIE", 4, 5800, 4200, "15W40", 6.0, 20000),
    "M44-3.0": f("ATM", E_, 3.0, "COURROIE", 4, 6200, 4100, "15W40", 6.5, 20000),
    "M44-2.5T": f("TURBO", E_, 2.5, "COURROIE", 4, 5800, 3500, "15W40", 6.5, 20000),
    "M28-4.5": f("ATM", E_, 4.5, "COURROIE", 8, 5500, 3600, "15W40", 7.5, 20000, a="V"),
    "M28-4.7": f("ATM", E_, 4.7, "COURROIE", 8, 5900, 4500, "15W40", 7.5, 20000, a="V"),
    "M28-5.0": f("ATM", E_, 5.0, "COURROIE", 8, 6000, 3000, "15W40", 7.5, 20000, a="V"),
    "M28-5.4": f("ATM", E_, 5.4, "COURROIE", 8, 5700, 4250, "15W40", 7.5, 20000, a="V"),
    # --- supercars
    "980-5.7": f("ATM", E_, 5.7, "CHAINE", 10, 8000, 5750, "0W40", 10.0, 15000, a="V"),
    "918-4.6": f("HYB_E", E_, 4.6, "CHAINE", 8, 8700, 6600, "0W40", 10.0, 15000, a="V"),
    # --- Cayenne / Macan / Panamera
    "VR6-3.2": f("ATM", E_, 3.2, "CHAINE", 6, 6000, 2500, "5W40", 6.5, 30000, a="VR"),
    "VR6-3.6": f("ATM", E_, 3.6, "CHAINE", 6, 6200, 3000, "5W40", 6.5, 30000, a="VR"),
    "V6-3.6": f("ATM", E_, 3.6, "CHAINE", 6, 6200, 3750, "5W40", 8.0, 30000, a="V"),
    "M48-4.5": f("ATM", E_, 4.5, "CHAINE", 8, 6000, 2500, "5W40", 9.0, 30000, a="V"),
    "M48-4.5T": f("TURBO", E_, 4.5, "CHAINE", 8, 6000, 2250, "5W40", 9.0, 30000, a="V"),
    "M48-4.8": f("ATM", E_, 4.8, "CHAINE", 8, 6500, 3500, "5W40", 9.0, 30000, a="V"),
    "M48-4.8T": f("TURBO", E_, 4.8, "CHAINE", 8, 6000, 2250, "5W40", 9.0, 30000, a="V"),
    "EA837-HYB": f("HYB_TE", E_, 3.0, "CHAINE", 6, 5500, 1000, "5W40", 7.0, 30000, a="V"),
    "EA888-2.0T": f("TURBO", E_, 2.0, "CHAINE", 4, 5000, 1600, "0W30", 5.7, 30000),
    "V6-3.0TT": f("TURBO", E_, 3.0, "CHAINE", 6, 6000, 1450, "0W40", 7.5, 30000, a="V"),
    "V6-3.6TT": f("TURBO", E_, 3.6, "CHAINE", 6, 6000, 1350, "0W40", 7.5, 30000, a="V"),
    "V6-3.0T": f("TURBO", E_, 3.0, "CHAINE", 6, 5300, 1340, "0W40", 7.5, 30000, a="V"),
    "V6-2.9TT": f("TURBO", E_, 2.9, "CHAINE", 6, 5700, 1800, "0W40", 7.5, 30000, a="V"),
    "V6-PHEV": f("HYB_TE", E_, 2.9, "CHAINE", 6, 5300, 1450, "0W40", 7.5, 30000, a="V"),
    "V8-4.0TT": f("TURBO", E_, 4.0, "CHAINE", 8, 6000, 2000, "0W40", 9.0, 30000, a="V"),
    "V8-PHEV": f("HYB_TE", E_, 4.0, "CHAINE", 8, 6000, 2000, "0W40", 9.0, 30000, a="V"),
    "TDI-3.0": f("TURBO", D, 3.0, "CHAINE", 6, 4000, 1750, "5W30", 7.5, 30000, a="V"),
    "TDI-4.2": f("TURBO", D, 4.2, "CHAINE", 8, 3750, 2000, "5W30", 9.0, 30000, a="V"),
    "TDI-4.0": f("TURBO", D, 4.0, "CHAINE", 8, 3500, 1000, "5W30", 9.0, 30000, a="V"),
    # --- électriques
    "J1-EV": electrique(), "PPE-EV": electrique(),
}

mg = SaisieMoteurs(FAMILLES, "Porsche")
L = []

# ---------------------------------------------------------------- 356 / 550
mg(L, "356", "Pré-A", "1", "1948-06", "1955-09",
   [("356 1100 40", "356-1.1", 64, {"fin": "1954-12"}), ("356 1300 44", "356-1.3", 81, {"debut": "1951-04"}),
    ("356 1500 55", "356-1.5", 106, {"debut": "1951-10"}), ("356 1500 S 70", "356-1.5", 108, {"debut": "1952-11"})],
   portes=2, places=4, reservoir=52, remarques="Coupé et Cabriolet ; America Roadster, Speedster (1954)")
mg(L, "356", "356 A", "1", "1955-10", "1959-08",
   [("356 A 1300 44", "356-1.3", 81, {"fin": "1957-09"}), ("356 A 1600 60", "616-1.6", 110),
    ("356 A 1600 S 75", "616-1.6", 117), ("356 A Carrera 1500 GS 100", "547-1.5", 121, {"fin": "1958-12"}),
    ("356 A Carrera 1600 GS 105", "547-1.5", 121, {"debut": "1958-01"})], portes=2, places=4, reservoir=52,
   remarques="Coupé, Cabriolet, Speedster, Convertible D")
mg(L, "356", "356 B", "1", "1959-09", "1963-07",
   [("356 B 1600 60", "616-1.6", 110), ("356 B 1600 Super 75", "616-1.6", 117),
    ("356 B 1600 Super 90 90", "616-1.6", 121, {"debut": "1960-03"}), ("356 B Carrera 2 130", "587-2.0", 162, {"debut": "1962-04"})],
   portes=2, places=4, reservoir=52, remarques="Coupé, Cabriolet, Roadster, Karmann Hardtop")
mg(L, "356", "356 C", "1", "1963-07", "1965-09",
   [("356 C 1600 C 75", "616-1.6", 123), ("356 C 1600 SC 95", "616-1.6", 124),
    ("356 C Carrera 2 130", "587-2.0", 162, {"fin": "1964-09"})], portes=2, places=4, reservoir=52,
   remarques="Coupé et Cabriolet")
mg(L, "550 Spyder", "550", "1", "1953-10", "1956-12", [("550 1500 RS 110", "547-1.5", 121)], portes=2, places=2,
   reservoir=80, remarques="Barquette de course ; 550 A (1956)")

# ---------------------------------------------------------------- 911 refroidies par air
mg(L, "911", "901", "1", "1964-09", "1969-07",
   [("911 2.0 130", "901-2.0", 174, {"fin": "1967-07"}), ("911 S 2.0 160", "901-2.0", 179, {"debut": "1966-08"}),
    ("911 T 2.0 110", "901-2.0", 157, {"debut": "1967-08"}), ("911 L 2.0 130", "901-2.0", 174, {"debut": "1967-08", "fin": "1968-07"}),
    ("911 E 2.0 140", "901-2.0", 175, {"debut": "1968-08"}), ("911 S 2.0 170", "901-2.0", 182, {"debut": "1968-08"})],
   portes=2, places=4, reservoir=62, remarques="Série O à B : Coupé, Targa (1966) ; 912 4 cylindres à part")
mg(L, "911", "901", "2", "1969-08", "1971-07",
   [("911 T 2.2 125", "911-2.2", 176), ("911 E 2.2 155", "911-2.2", 191), ("911 S 2.2 180", "911-2.2", 199)],
   portes=2, places=4, reservoir=62, remarques="Série C/D 2,2 l : Coupé et Targa")
mg(L, "911", "901", "3", "1971-08", "1973-07",
   [("911 T 2.4 130", "911-2.4", 196), ("911 E 2.4 165", "911-2.4", 206), ("911 S 2.4 190", "911-2.4", 216),
    ("Carrera RS 2.7 210", "911-2.7", 255, {"debut": "1972-10"})], portes=2, places=4, reservoir=85,
   remarques="Série E/F 2,4 l : Coupé et Targa ; Carrera RS 2.7")
mg(L, "911", "G", "1", "1973-08", "1977-07",
   [("911 2.7 150", "911-2.7", 235), ("911 S 2.7 175", "911-2.7", 235), ("Carrera 2.7 210", "911-2.7", 255, {"fin": "1975-07"}),
    ("Carrera 3.0 200", "911-3.0", 255, {"debut": "1975-08"}), ("911 Turbo 3.0 260", "930-3.0T", 343, {"debut": "1975-03"})],
   portes=2, places=4, reservoir=80, remarques="Série G : Coupé et Targa ; Turbo (930)")
mg(L, "911", "G", "2", "1977-08", "1983-07",
   [("911 SC 180", "911-3.0", 265, {"fin": "1980-07"}), ("911 SC 188", "911-3.0", 265, {"debut": "1980-08", "fin": "1981-07"}),
    ("911 SC 204", "911-3.0", 267, {"debut": "1981-08"}), ("911 Turbo 3.3 300", "930-3.3T", 412)], portes=2, places=4,
   reservoir=80, remarques="Coupé, Targa, Cabriolet SC (1982) ; Turbo (930)")
mg(L, "911", "G", "3", "1983-08", "1989-07",
   [("Carrera 3.2 231", "911-3.2", 284), ("911 Turbo 3.3 300", "930-3.3T", 432),
    ("911 Turbo 3.3 330", "930-3.3T", 432, {"debut": "1987-08", "remarques": "Turbo S (Flachbau)"})], portes=2, places=4,
   reservoir=85, remarques="Coupé, Targa, Cabriolet, Speedster (1989) ; Turbo (930)")
mg(L, "911", "964", "1", "1988-08", "1994-07",
   [("Carrera 4 250", "M64-3.6", 310), ("Carrera 2 250", "M64-3.6", 310, {"debut": "1989-08"}),
    ("Turbo 3.3 320", "M30-3.3T", 450, {"debut": "1990-03", "fin": "1992-12"}), ("Turbo 3.6 360", "M64-3.6T", 520, {"debut": "1993-01"}),
    ("Carrera RS 260", "M64-3.6", 325, {"debut": "1991-08", "fin": "1992-07"}),
    ("Carrera RS 3.8 300", "M64-3.8", 360, {"debut": "1993-01", "fin": "1993-12"})], portes=2, places=4, reservoir=77,
   remarques="Coupé, Targa, Cabriolet, Speedster (1993) ; Turbo")
mg(L, "911", "993", "1", "1993-12", "1998-03",
   [("Carrera 272", "M64-3.6", 330, {"fin": "1995-08"}), ("Carrera 285", "M64-3.6", 340, {"debut": "1995-09"}),
    ("Carrera 4 272", "M64-3.6", 330, {"fin": "1995-08"}), ("Carrera 4 285", "M64-3.6", 340, {"debut": "1995-09"}),
    ("Carrera 4S 285", "M64-3.6", 340, {"debut": "1995-09"}), ("Carrera S 285", "M64-3.6", 340, {"debut": "1996-09"}),
    ("Carrera RS 300", "M64-3.8", 355, {"debut": "1995-01", "fin": "1996-12"}), ("Turbo 408", "M64-3.6T", 540, {"debut": "1995-03"}),
    ("GT2 430", "M64-3.6T", 540, {"debut": "1995-06"}), ("Turbo S 450", "M64-3.6T", 585, {"debut": "1997-08"})],
   portes=2, places=4, reservoir=73, remarques="Dernière 911 refroidie par air : Coupé, Cabriolet, Targa (1996)")

# ---------------------------------------------------------------- 911 refroidies par eau
mg(L, "911", "996", "1", "1997-10", "2001-08",
   [("Carrera 300", "M96-3.4", 350), ("Carrera 4 300", "M96-3.4", 350, {"debut": "1998-08"}),
    ("GT3 360", "Mezger-3.6", 370, {"debut": "1999-05"}), ("Turbo 420", "Mezger-3.6T", 560, {"debut": "2000-06"}),
    ("GT2 462", "Mezger-3.6T", 620, {"debut": "2001-02"})], portes=2, places=4, reservoir=64,
   remarques="Coupé et Cabriolet")
mg(L, "911", "996", "2", "2001-09", "2005-07",
   [("Carrera 320", "M96-3.6", 370), ("Carrera 4 320", "M96-3.6", 370), ("Carrera 4S 320", "M96-3.6", 370),
    ("Targa 320", "M96-3.6", 370), ("GT3 381", "Mezger-3.6", 385, {"debut": "2003-04"}),
    ("GT3 RS 381", "Mezger-3.6", 385, {"debut": "2003-10"}), ("Turbo 420", "Mezger-3.6T", 560),
    ("Turbo S 450", "Mezger-3.6T", 620, {"debut": "2004-08"}), ("GT2 483", "Mezger-3.6T", 640, {"debut": "2003-08"})],
   portes=2, places=4, reservoir=64, remarques="Coupé, Cabriolet, Targa")
mg(L, "911", "997", "1", "2004-07", "2008-06",
   [("Carrera 325", "M97-3.6", 370), ("Carrera S 355", "M97-3.8", 400), ("Carrera 4 325", "M97-3.6", 370, {"debut": "2005-11"}),
    ("Carrera 4S 355", "M97-3.8", 400, {"debut": "2005-11"}), ("Targa 4 325", "M97-3.6", 370, {"debut": "2006-11"}),
    ("Targa 4S 355", "M97-3.8", 400, {"debut": "2006-11"}), ("GT3 415", "Mezger-3.6", 405, {"debut": "2006-05"}),
    ("GT3 RS 415", "Mezger-3.6", 405, {"debut": "2006-10"}), ("Turbo 480", "Mezger-3.6T", 620, {"debut": "2006-06"}),
    ("GT2 530", "Mezger-3.6T", 680, {"debut": "2007-11"})], portes=2, places=4, reservoir=64,
   remarques="Coupé, Cabriolet, Targa")
mg(L, "911", "997", "2", "2008-07", "2012-12",
   [("Carrera 345", "9A1-3.6", 390), ("Carrera S 385", "9A1-3.8", 420), ("Carrera 4 345", "9A1-3.6", 390),
    ("Carrera 4S 385", "9A1-3.8", 420), ("Targa 4 345", "9A1-3.6", 390), ("Targa 4S 385", "9A1-3.8", 420),
    ("Carrera GTS 408", "9A1-3.8", 420, {"debut": "2010-09"}), ("GT3 435", "Mezger-3.8", 430, {"debut": "2009-06", "fin": "2011-12"}),
    ("GT3 RS 450", "Mezger-3.8", 430, {"debut": "2009-10", "fin": "2011-12"}),
    ("GT3 RS 4.0 500", "Mezger-4.0", 460, {"debut": "2011-06", "fin": "2012-03"}),
    ("Turbo 500", "9A1-3.8T", 650, {"debut": "2009-09"}), ("Turbo S 530", "9A1-3.8T", 700, {"debut": "2010-05"}),
    ("GT2 RS 620", "Mezger-3.6T", 700, {"debut": "2010-09", "fin": "2011-12"})], portes=2, places=4, reservoir=67,
   remarques="Coupé, Cabriolet, Targa, Speedster (2010)")
mg(L, "911", "991", "1", "2011-12", "2015-08",
   [("Carrera 350", "9A1-3.4", 390), ("Carrera S 400", "9A1-3.8", 440), ("Carrera 4 350", "9A1-3.4", 390, {"debut": "2012-09"}),
    ("Carrera 4S 400", "9A1-3.8", 440, {"debut": "2012-09"}), ("Targa 4 350", "9A1-3.4", 390, {"debut": "2014-05"}),
    ("Targa 4S 400", "9A1-3.8", 440, {"debut": "2014-05"}), ("Carrera GTS 430", "9A1-3.8", 440, {"debut": "2014-11"}),
    ("GT3 475", "9A1-3.8GT", 440, {"debut": "2013-08"}), ("GT3 RS 500", "9A1-4.0GT", 460, {"debut": "2015-05"}),
    ("Turbo 520", "9A1-3.8T", 660, {"debut": "2013-09"}), ("Turbo S 560", "9A1-3.8T", 700, {"debut": "2013-09"})],
   portes=2, places=4, reservoir=64, remarques="Coupé, Cabriolet, Targa (2014)")
mg(L, "911", "991", "2", "2015-09", "2019-12",
   [("Carrera 370", "9A2-3.0T", 450), ("Carrera S 420", "9A2-3.0T", 500), ("Carrera 4 370", "9A2-3.0T", 450),
    ("Carrera 4S 420", "9A2-3.0T", 500), ("Targa 4 370", "9A2-3.0T", 450), ("Targa 4S 420", "9A2-3.0T", 500),
    ("Carrera T 370", "9A2-3.0T", 450, {"debut": "2017-10"}), ("Carrera GTS 450", "9A2-3.0T", 550, {"debut": "2017-01"}),
    ("R 500", "9A1-4.0GT", 460, {"debut": "2016-05", "fin": "2016-12"}), ("GT3 500", "9A1-4.0GT", 460, {"debut": "2017-04"}),
    ("GT3 RS 520", "9A1-4.0GT", 470, {"debut": "2018-04"}), ("Turbo 540", "9A1-3.8T", 710, {"debut": "2016-01"}),
    ("Turbo S 580", "9A1-3.8T", 750, {"debut": "2016-01"}), ("GT2 RS 700", "9A1-3.8T", 750, {"debut": "2017-11", "fin": "2019-03"})],
   portes=2, places=4, reservoir=64, remarques="Coupé, Cabriolet, Targa ; Speedster (2019)")
mg(L, "911", "992", "1", "2019-01", "2024-05",
   [("Carrera 385", "9A2-3.0T", 450, {"debut": "2019-07"}), ("Carrera S 450", "9A2-3.0T", 530), ("Carrera 4 385", "9A2-3.0T", 450, {"debut": "2019-07"}),
    ("Carrera 4S 450", "9A2-3.0T", 530), ("Targa 4 385", "9A2-3.0T", 450, {"debut": "2020-08"}),
    ("Targa 4S 450", "9A2-3.0T", 530, {"debut": "2020-08"}), ("Carrera T 385", "9A2-3.0T", 450, {"debut": "2022-10"}),
    ("Carrera GTS 480", "9A2-3.0T", 570, {"debut": "2021-09"}), ("Sport Classic 550", "9A2-3.8T", 600, {"debut": "2022-05"}),
    ("Dakar 480", "9A2-3.0T", 570, {"debut": "2022-11"}), ("GT3 510", "9A1-4.0GT", 470, {"debut": "2021-05"}),
    ("GT3 RS 525", "9A1-4.0GT", 465, {"debut": "2022-10"}), ("S/T 525", "9A1-4.0GT", 465, {"debut": "2023-09"}),
    ("Turbo 580", "9A2-3.8T", 750, {"debut": "2020-05"}), ("Turbo S 650", "9A2-3.8T", 800, {"debut": "2020-05"})],
   portes=2, places=4, reservoir=64, remarques="Coupé, Cabriolet, Targa")
mg(L, "911", "992", "2", "2024-06", None,
   [("Carrera 394", "9A3-3.0T", 450), ("Carrera 4 394", "9A3-3.0T", 450, {"debut": "2024-11"}),
    ("Targa 4 394", "9A3-3.0T", 450, {"debut": "2024-11"}), ("Carrera T 394", "9A3-3.0T", 450, {"debut": "2025-03"}),
    ("Carrera S 480", "9A3-3.0T", 530, {"debut": "2025-03"}), ("Carrera 4S 480", "9A3-3.0T", 530, {"debut": "2025-03"}),
    ("Carrera GTS T-Hybrid 541", "9A3-3.6-HYB", 610), ("Carrera 4 GTS T-Hybrid 541", "9A3-3.6-HYB", 610),
    ("Targa 4 GTS T-Hybrid 541", "9A3-3.6-HYB", 610), ("GT3 510", "9A1-4.0GT", 450, {"debut": "2024-10"}),
    ("Turbo S T-Hybrid 711", "9A3-3.6-HYB", 800, {"debut": "2025-09"})], portes=2, places=4, reservoir=63,
   remarques="Coupé, Cabriolet, Targa ; T-Hybrid 400 V")

# ---------------------------------------------------------------- 912 / 914 / 959 / Carrera GT / 918
mg(L, "912", "912", "1", "1965-04", "1969-07", [("912 1.6 90", "616-1.6", 122)], portes=2, places=4, reservoir=62,
   remarques="Coupé et Targa 4 cylindres (carrosserie 911)")
mg(L, "912", "912 E", "1", "1975-09", "1976-07", [("912 E 2.0 90", "T4-2.0", 133)], portes=2, places=4, reservoir=80,
   remarques="Marché nord-américain")
mg(L, "914", "914", "1", "1969-09", "1976-07",
   [("914/4 1.7 80", "T4-1.7", 133, {"fin": "1973-07"}), ("914/6 2.0 110", "901-2.0", 157, {"fin": "1972-07"}),
    ("914/4 2.0 100", "T4-2.0", 157, {"debut": "1972-08"}), ("914/4 1.8 85", "T4-1.8", 138, {"debut": "1973-08"})],
   portes=2, places=2, reservoir=62, remarques="Targa à moteur central (VW-Porsche)")
mg(L, "959", "959", "1", "1986-04", "1988-12", [("959 450", "959-2.85T", 500)], portes=2, places=2, reservoir=85,
   remarques="Coupé à transmission intégrale, biturbo séquentiel ; Komfort et Sport")
mg(L, "Carrera GT", "980", "1", "2003-09", "2006-05", [("Carrera GT 612", "980-5.7", 590)], portes=2, places=2,
   reservoir=92, remarques="Roadster V10 à moteur central")
mg(L, "918 Spyder", "918", "1", "2013-09", "2015-06", [("918 Spyder 887", "918-4.6", 1280, ph(7, 70))], portes=2,
   places=2, remarques="Hypercar hybride rechargeable (V8 + 2 moteurs électriques)")

# ---------------------------------------------------------------- transaxles
mg(L, "924", "924", "1", "1976-02", "1988-07",
   [("924 2.0 125", "EA831-2.0", 165, {"fin": "1985-07"}), ("924 Turbo 170", "931-2.0T", 245, {"debut": "1978-10", "fin": "1980-07"}),
    ("924 Turbo 177", "931-2.0T", 250, {"debut": "1980-08", "fin": "1982-12"}),
    ("924 Carrera GT 210", "931-2.0T", 280, {"debut": "1980-06", "fin": "1981-12"}),
    ("924 S 150", "M44-2.5", 190, {"debut": "1985-08", "fin": "1987-07"}), ("924 S 160", "M44-2.5", 210, {"debut": "1987-08"})],
   portes=3, places=4, reservoir=66, remarques="Coupé transaxle 2+2")
mg(L, "944", "944", "1", "1981-11", "1991-07",
   [("944 163", "M44-2.5", 205, {"fin": "1988-07"}), ("944 Turbo 220", "M44-2.5T", 330, {"debut": "1985-01", "fin": "1988-07"}),
    ("944 S 190", "M44-2.5-16V", 230, {"debut": "1986-08", "fin": "1988-07"}), ("944 Turbo S 250", "M44-2.5T", 350, {"debut": "1988-01", "fin": "1988-12"}),
    ("944 2.7 165", "M44-2.7", 225, {"debut": "1988-08", "fin": "1989-07"}), ("944 S2 211", "M44-3.0", 280, {"debut": "1988-08"}),
    ("944 Turbo 250", "M44-2.5T", 350, {"debut": "1989-01"})], portes=3, places=4, reservoir=80,
   remarques="Coupé transaxle 2+2, Cabriolet (1989)")
mg(L, "968", "968", "1", "1991-07", "1995-07",
   [("968 240", "M44-3.0", 305), ("968 Club Sport 240", "M44-3.0", 305, {"debut": "1992-10"})], portes=3, places=4,
   reservoir=74, remarques="Coupé et Cabriolet transaxle")
mg(L, "928", "928", "1", "1977-03", "1995-06",
   [("928 240", "M28-4.5", 350, {"fin": "1982-07"}), ("928 S 300", "M28-4.7", 385, {"debut": "1979-08", "fin": "1983-07"}),
    ("928 S 310", "M28-4.7", 400, {"debut": "1983-08", "fin": "1986-07"}), ("928 S4 320", "M28-5.0", 430, {"debut": "1986-08", "fin": "1991-07"}),
    ("928 GT 330", "M28-5.0", 430, {"debut": "1989-01", "fin": "1991-07"}), ("928 GTS 350", "M28-5.4", 500, {"debut": "1991-08"})],
   portes=3, places=4, reservoir=86, remarques="Coupé V8 transaxle 2+2")

# ---------------------------------------------------------------- Boxster / Cayman
mg(L, "Boxster", "986", "1", "1996-10", "1999-08", [("Boxster 204", "M96-2.5", 245)], portes=2, places=2, reservoir=57,
   remarques="Roadster à moteur central")
mg(L, "Boxster", "986", "2", "1999-09", "2002-08", [("Boxster 220", "M96-2.7", 260), ("Boxster S 252", "M96-3.2", 305)],
   portes=2, places=2, reservoir=64, remarques="Roadster à moteur central")
mg(L, "Boxster", "986", "3", "2002-09", "2004-08", [("Boxster 228", "M96-2.7", 260), ("Boxster S 260", "M96-3.2", 310)],
   portes=2, places=2, reservoir=64, remarques="Roadster ; restylage 2003")
mg(L, "Boxster", "987", "1", "2004-09", "2008-12",
   [("Boxster 240", "M97-2.7", 270, {"fin": "2006-07"}), ("Boxster 245", "M97-2.7", 273, {"debut": "2006-08"}),
    ("Boxster S 280", "M97-3.4", 320, {"fin": "2006-07"}), ("Boxster S 295", "M97-3.4", 340, {"debut": "2006-08"}),
    ("Boxster RS 60 Spyder 303", "M97-3.4", 340, {"debut": "2008-01", "fin": "2008-12"})], portes=2, places=2, reservoir=64,
   remarques="Roadster à moteur central")
mg(L, "Boxster", "987", "2", "2009-01", "2012-03",
   [("Boxster 255", "9A1-2.9", 290), ("Boxster S 310", "9A1-3.4", 360), ("Boxster Spyder 320", "9A1-3.4", 370, {"debut": "2010-02"})],
   portes=2, places=2, reservoir=64, remarques="Roadster à moteur central")
mg(L, "Cayman", "987c", "1", "2005-11", "2008-12",
   [("Cayman S 295", "M97-3.4", 340), ("Cayman 245", "M97-2.7", 273, {"debut": "2006-07"})], portes=2, places=2,
   reservoir=64, remarques="Coupé à moteur central")
mg(L, "Cayman", "987c", "2", "2009-01", "2013-02",
   [("Cayman 265", "9A1-2.9", 300), ("Cayman S 320", "9A1-3.4", 370), ("Cayman R 330", "9A1-3.4", 370, {"debut": "2011-02"})],
   portes=2, places=2, reservoir=64, remarques="Coupé à moteur central")
mg(L, "Boxster", "981", "1", "2012-04", "2016-03",
   [("Boxster 265", "9A1-2.7", 280), ("Boxster S 315", "9A1-3.4", 360), ("Boxster GTS 330", "9A1-3.4", 370, {"debut": "2014-05"}),
    ("Boxster Spyder 375", "9A1-3.8", 420, {"debut": "2015-07"})], portes=2, places=2, reservoir=64,
   remarques="Roadster à moteur central")
mg(L, "Cayman", "981c", "1", "2013-03", "2016-03",
   [("Cayman 275", "9A1-2.7", 290), ("Cayman S 325", "9A1-3.4", 370), ("Cayman GTS 340", "9A1-3.4", 380, {"debut": "2014-05"}),
    ("Cayman GT4 385", "9A1-3.8", 420, {"debut": "2015-05"})], portes=2, places=2, reservoir=64,
   remarques="Coupé à moteur central")
mg(L, "718 Boxster", "982", "1", "2016-04", "2025-10",
   [("718 Boxster 300", "9A2-2.0T", 380), ("718 Boxster S 350", "9A2-2.5T", 420),
    ("718 Boxster GTS 365", "9A2-2.5T", 430, {"debut": "2017-11", "fin": "2019-12"}), ("718 Boxster T 300", "9A2-2.0T", 380, {"debut": "2019-03"}),
    ("718 Boxster GTS 4.0 400", "9A1-4.0", 420, {"debut": "2020-03"}), ("718 Spyder 420", "9A1-4.0", 420, {"debut": "2019-07"}),
    ("718 Spyder RS 500", "9A1-4.0GT", 450, {"debut": "2023-08"})], portes=2, places=2, reservoir=54,
   remarques="Roadster à moteur central")
mg(L, "718 Cayman", "982c", "1", "2016-09", "2025-10",
   [("718 Cayman 300", "9A2-2.0T", 380), ("718 Cayman S 350", "9A2-2.5T", 420),
    ("718 Cayman GTS 365", "9A2-2.5T", 430, {"debut": "2017-11", "fin": "2019-12"}), ("718 Cayman T 300", "9A2-2.0T", 380, {"debut": "2019-03"}),
    ("718 Cayman GTS 4.0 400", "9A1-4.0", 420, {"debut": "2020-03"}), ("718 Cayman GT4 420", "9A1-4.0", 420, {"debut": "2019-07"}),
    ("718 Cayman GT4 RS 500", "9A1-4.0GT", 450, {"debut": "2021-11"})], portes=2, places=2, reservoir=54,
   remarques="Coupé à moteur central")

# ---------------------------------------------------------------- Cayenne
mg(L, "Cayenne", "9PA", "1", "2002-09", "2007-02",
   [("Cayenne S 340", "M48-4.5", 420), ("Cayenne Turbo 450", "M48-4.5T", 620), ("Cayenne 250", "VR6-3.2", 310, {"debut": "2003-09"}),
    ("Cayenne Turbo S 521", "M48-4.5T", 720, {"debut": "2006-01"})], reservoir=100, remarques="SUV (type 955)")
mg(L, "Cayenne", "9PA", "2", "2007-03", "2010-03",
   [("Cayenne 290", "VR6-3.6", 385), ("Cayenne S 385", "M48-4.8", 500), ("Cayenne GTS 405", "M48-4.8", 500, {"debut": "2007-11"}),
    ("Cayenne Turbo 500", "M48-4.8T", 700), ("Cayenne Turbo S 550", "M48-4.8T", 750, {"debut": "2008-09"}),
    ("Cayenne Diesel 240", "TDI-3.0", 550, {"debut": "2009-03"})], reservoir=100, remarques="SUV (type 957)")
mg(L, "Cayenne", "92A", "1", "2010-04", "2014-09",
   [("Cayenne 300", "VR6-3.6", 400), ("Cayenne S 400", "M48-4.8", 500), ("Cayenne S Hybrid 380", "EA837-HYB", 580),
    ("Cayenne GTS 420", "M48-4.8", 515, {"debut": "2012-05"}), ("Cayenne Turbo 500", "M48-4.8T", 700),
    ("Cayenne Turbo S 550", "M48-4.8T", 750, {"debut": "2012-10"}), ("Cayenne Diesel 245", "TDI-3.0", 550),
    ("Cayenne S Diesel 382", "TDI-4.2", 850, {"debut": "2012-09"})], reservoir=85, remarques="SUV")
mg(L, "Cayenne", "92A", "2", "2014-10", "2018-01",
   [("Cayenne 300", "VR6-3.6", 400), ("Cayenne S 420", "V6-3.6TT", 550), ("Cayenne S E-Hybrid 416", "EA837-HYB", 590, ph(11, 80)),
    ("Cayenne GTS 440", "V6-3.6TT", 600, {"debut": "2015-03"}), ("Cayenne Turbo 520", "M48-4.8T", 750),
    ("Cayenne Turbo S 570", "M48-4.8T", 800, {"debut": "2015-03"}), ("Cayenne Diesel 262", "TDI-3.0", 580),
    ("Cayenne S Diesel 385", "TDI-4.2", 850)], reservoir=85, remarques="SUV")
mg(L, "Cayenne", "9YA", "1", "2017-12", "2023-03",
   [("Cayenne 340", "V6-3.0T", 450), ("Cayenne S 440", "V6-2.9TT", 550), ("Cayenne E-Hybrid 462", "V6-PHEV", 700, ph(14, 75, debut="2018-10")),
    ("Cayenne GTS 460", "V8-4.0TT", 620, {"debut": "2020-01"}), ("Cayenne Turbo 550", "V8-4.0TT", 770),
    ("Cayenne Turbo S E-Hybrid 680", "V8-PHEV", 900, ph(14, 75, debut="2019-09")),
    ("Cayenne Turbo GT 640", "V8-4.0TT", 850, {"debut": "2021-07"})], reservoir=75,
   remarques="SUV et Cayenne Coupé (2019)")
mg(L, "Cayenne", "9YA", "2", "2023-04", None,
   [("Cayenne 353", "V6-3.0T", 500), ("Cayenne E-Hybrid 470", "V6-PHEV", 650, ph(26, 75)), ("Cayenne S 474", "V8-4.0TT", 600),
    ("Cayenne S E-Hybrid 519", "V6-PHEV", 750, ph(26, 75)), ("Cayenne GTS 500", "V8-4.0TT", 660, {"debut": "2024-03"}),
    ("Cayenne Turbo E-Hybrid 739", "V8-PHEV", 950, ph(26, 75)), ("Cayenne Turbo GT 659", "V8-4.0TT", 850)], reservoir=75,
   remarques="SUV et Cayenne Coupé ; Cayenne électrique (2025) non détaillé")

# ---------------------------------------------------------------- Macan
mg(L, "Macan", "95B", "1", "2014-04", "2018-09",
   [("Macan 252", "EA888-2.0T", 370, {"debut": "2016-03"}), ("Macan S 340", "V6-3.0TT", 460), ("Macan S Diesel 258", "TDI-3.0", 580),
    ("Macan GTS 360", "V6-3.0TT", 500, {"debut": "2016-01"}), ("Macan Turbo 400", "V6-3.6TT", 550),
    ("Macan Turbo Performance 440", "V6-3.6TT", 600, {"debut": "2016-09"})], reservoir=75, remarques="SUV compact")
mg(L, "Macan", "95B", "2", "2018-10", "2021-08",
   [("Macan 245", "EA888-2.0T", 370), ("Macan S 354", "V6-3.0T", 480), ("Macan GTS 380", "V6-2.9TT", 520, {"debut": "2020-01"}),
    ("Macan Turbo 440", "V6-2.9TT", 550, {"debut": "2019-07"})], reservoir=65, remarques="SUV compact")
mg(L, "Macan", "95B", "3", "2021-09", "2024-04",
   [("Macan 265", "EA888-2.0T", 400), ("Macan T 265", "EA888-2.0T", 400, {"debut": "2022-09"}),
    ("Macan S 380", "V6-2.9TT", 520), ("Macan GTS 440", "V6-2.9TT", 550)], reservoir=65,
   remarques="SUV compact (vendu hors UE jusqu'en 2025)")
mg(L, "Macan Electric", "XAB", "1", "2024-01", None,
   [("Macan 4 408", "PPE-EV", 650, el(100)), ("Macan Turbo 639", "PPE-EV", 1130, el(100)),
    ("Macan 360", "PPE-EV", 563, el(96, debut="2024-07")), ("Macan 4S 516", "PPE-EV", 820, el(100, debut="2024-07")),
    ("Macan GTS 571", "PPE-EV", 955, el(100, debut="2025-10"))], reservoir=0,
   remarques="SUV électrique (plateforme PPE, 800 V) ; puissances avec Launch Control")

# ---------------------------------------------------------------- Panamera
mg(L, "Panamera", "970", "1", "2009-09", "2013-05",
   [("Panamera S 400", "M48-4.8", 500), ("Panamera 4S 400", "M48-4.8", 500), ("Panamera Turbo 500", "M48-4.8T", 700),
    ("Panamera 300", "V6-3.6", 400, {"debut": "2010-04"}), ("Panamera 4 300", "V6-3.6", 400, {"debut": "2010-04"}),
    ("Panamera GTS 430", "M48-4.8", 520, {"debut": "2011-03"}), ("Panamera Turbo S 550", "M48-4.8T", 750, {"debut": "2011-05"}),
    ("Panamera S Hybrid 380", "EA837-HYB", 580, {"debut": "2011-05"}), ("Panamera Diesel 250", "TDI-3.0", 550, {"debut": "2011-07"})],
   places=4, reservoir=80, remarques="Berline 4 places à hayon")
mg(L, "Panamera", "970", "2", "2013-06", "2016-09",
   [("Panamera 310", "V6-3.6", 400), ("Panamera 4 310", "V6-3.6", 400), ("Panamera S 420", "V6-3.0TT", 520),
    ("Panamera 4S 420", "V6-3.0TT", 520), ("Panamera S E-Hybrid 416", "EA837-HYB", 590, ph(9, 80)),
    ("Panamera GTS 440", "M48-4.8", 520), ("Panamera Turbo 520", "M48-4.8T", 700), ("Panamera Turbo S 570", "M48-4.8T", 800),
    ("Panamera Diesel 300", "TDI-3.0", 650)], places=4, reservoir=80, remarques="Berline et version longue Executive")
mg(L, "Panamera", "971", "1", "2016-11", "2020-08",
   [("Panamera 330", "V6-2.9TT", 450, {"debut": "2017-04"}), ("Panamera 4 330", "V6-2.9TT", 450, {"debut": "2017-04"}),
    ("Panamera 4 E-Hybrid 462", "V6-PHEV", 700, ph(14, 80, debut="2017-04")), ("Panamera 4S 440", "V6-2.9TT", 550),
    ("Panamera 4S Diesel 422", "TDI-4.0", 850, {"fin": "2018-08"}), ("Panamera GTS 460", "V8-4.0TT", 620, {"debut": "2018-11"}),
    ("Panamera Turbo 550", "V8-4.0TT", 770), ("Panamera Turbo S E-Hybrid 680", "V8-PHEV", 850, ph(14, 80, debut="2017-07"))],
   places=4, reservoir=75, remarques="Berline, Sport Turismo (2017), Executive")
mg(L, "Panamera", "971", "2", "2020-09", "2023-09",
   [("Panamera 330", "V6-2.9TT", 450), ("Panamera 4 330", "V6-2.9TT", 450), ("Panamera 4 E-Hybrid 462", "V6-PHEV", 700, ph(18, 80)),
    ("Panamera 4S 440", "V6-2.9TT", 550), ("Panamera 4S E-Hybrid 560", "V6-PHEV", 750, ph(18, 80)),
    ("Panamera GTS 480", "V8-4.0TT", 620), ("Panamera Turbo S 630", "V8-4.0TT", 820),
    ("Panamera Turbo S E-Hybrid 700", "V8-PHEV", 870, ph(18, 80))], places=4, reservoir=75, remarques="Berline, Sport Turismo, Executive")
mg(L, "Panamera", "976", "1", "2023-11", None,
   [("Panamera 353", "V6-2.9TT", 500), ("Panamera 4 353", "V6-2.9TT", 500), ("Panamera 4 E-Hybrid 470", "V6-PHEV", 650, ph(26, 80)),
    ("Panamera 4S E-Hybrid 544", "V6-PHEV", 750, ph(26, 80)), ("Panamera GTS 500", "V8-4.0TT", 660, {"debut": "2024-06"}),
    ("Panamera Turbo E-Hybrid 680", "V8-PHEV", 930, ph(26, 80)),
    ("Panamera Turbo S E-Hybrid 782", "V8-PHEV", 1000, ph(26, 80, debut="2024-06"))], places=4, reservoir=75,
   remarques="Berline et Executive")

# ---------------------------------------------------------------- Taycan
mg(L, "Taycan", "J1", "1", "2019-09", "2024-02",
   [("Taycan 4S 530", "J1-EV", 640, el(79)), ("Taycan Turbo 680", "J1-EV", 850, el(93)), ("Taycan Turbo S 761", "J1-EV", 1050, el(93)),
    ("Taycan 408", "J1-EV", 345, el(79, debut="2021-01")), ("Taycan 4 Cross Turismo 476", "J1-EV", 500, el(93, debut="2021-03")),
    ("Taycan GTS 598", "J1-EV", 850, el(93, debut="2021-11"))], portes=4, places=4, reservoir=0,
   remarques="Berline électrique, Cross Turismo (2021), Sport Turismo (2022) ; puissances avec Launch Control")
mg(L, "Taycan", "J1", "2", "2024-03", None,
   [("Taycan 435", "J1-EV", 410, el(89)), ("Taycan 4 435", "J1-EV", 520, el(89, debut="2024-09")),
    ("Taycan 4S 598", "J1-EV", 710, el(105)), ("Taycan GTS 700", "J1-EV", 810, el(105, debut="2024-09")),
    ("Taycan Turbo 884", "J1-EV", 890, el(105)), ("Taycan Turbo S 952", "J1-EV", 1110, el(105)),
    ("Taycan Turbo GT 1034", "J1-EV", 1340, el(105))], portes=4, places=4, reservoir=0,
   remarques="Berline, Cross Turismo, Sport Turismo ; puissances avec Launch Control")

MOT = Motorisations("Porsche", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Porsche": L}
MOTEURS = MOT.moteurs()
