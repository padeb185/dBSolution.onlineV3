"""MG : générations, phases, motorisations (marché européen) et moteurs liés.
MG britannique : TD, MGA, MGB, Midget, Metro, MGF/TF, ZR, ZS (Rover), XPower SV ; MG sous SAIC : MG3, MG4 EV, MG5 EV, MG6,
MG7 (Chine), MG ZS (2017), MG ZS EV, MG HS/EHS, Marvel R, Cyberster, MGS5 EV, MGS6 EV.
Moteurs Rover et BMW repris de land_rover.py, V8 Ford de lincoln.py (motoristes « Rover », « BMW », « Ford ») ; moteurs BMC,
Triumph et SAIC ajoutés. Données anciennes indicatives. MG GT (Chine) et MG4 Urban non repris.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .land_rover import FAMILLES as FAMILLES_LR
from .lincoln import FAMILLES as FAMILLES_LINCOLN

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

BMC = {
    "MG-XPAG-1.25": f("ATM", E_, 1.25, C, 4, 5200, 2600, "20W50", 4.5, 3000),
    "BMC-B-1.5": f("ATM", E_, 1.5, C, 4, 5500, 3500, "20W50", 4.5, 5000),
    "BMC-B-1.6": f("ATM", E_, 1.6, C, 4, 5500, 3500, "20W50", 4.5, 5000),
    "BMC-B-1.8": f("ATM", E_, 1.8, C, 4, 5400, 3000, "20W50", 4.5, 5000),
    "BMC-A-0.95": f("ATM", E_, 0.95, C, 4, 5500, 3000, "20W50", 3.5, 5000),
    "BMC-A-1.1": f("ATM", E_, 1.1, C, 4, 5500, 3000, "20W50", 3.5, 5000),
    "BMC-A-1.3": f("ATM", E_, 1.3, C, 4, 6000, 3000, "20W50", 3.5, 5000),
    "BMC-A-1.3T": f("TURBO", E_, 1.3, C, 4, 6130, 2650, "20W50", 3.5, 6000),
}
TRIUMPH = {"TRIUMPH-1.5": f("ATM", E_, 1.5, C, 4, 5500, 3000, "20W50", 4.5, 5000)}
ROVER_AJ = {
    "ROVER-K-1.4": f("ATM", E_, 1.4, B, 4, 6000, 4000, "10W40", 4.5, 15000),
    "ROVER-K-1.6": f("ATM", E_, 1.6, B, 4, 6000, 4000, "10W40", 4.5, 15000),
    "ROVER-K-1.8T": f("TURBO", E_, 1.8, B, 4, 5500, 2500, "5W30", 4.5, 15000),
}
SAIC = {
    "SAIC-1.5": f("ATM", E_, 1.5, C, 4, 6000, 4500, "5W30", 4.0, 15000),
    "SAIC-1.0T": f("TURBO", E_, 1.0, C, 3, 5200, 1800, "5W30", 4.0, 15000),
    "SAIC-1.5T": f("TURBO", E_, 1.5, C, 4, 5600, 1700, "5W30", 4.5, 15000),
    "SAIC-1.5T-PHEV": f("HYB_E", E_, 1.5, C, 4, 5600, 1700, "0W20", 4.5, 15000),
    "SAIC-1.5-HEV": f("HYB_TE", E_, 1.5, C, 4, 6000, 4500, "0W20", 4.0, 15000),
    "SAIC-1.9D": f("TURBO", D, 1.9, C, 4, 4000, 2000, "5W30", 5.5, 15000),
    "MG-EV": electrique(),
}
LR = {k: FAMILLES_LR[k] for k in ("ROVER-K-1.8", "ROVER-KV6-2.5", "ROVER-L-2.0DI", "M47-2.0")}
FORD = {k: FAMILLES_LINCOLN[k] for k in ("MODULAR-4.6", "MODULAR-4.6-DOHC")}
FAMILLES = {**BMC, **TRIUMPH, **ROVER_AJ, **SAIC, **LR, **FORD}


def motoriste(fam):
    if fam in BMC:
        return "BMC" if fam != "MG-XPAG-1.25" else "MG"
    if fam in TRIUMPH:
        return "Triumph"
    if fam in ROVER_AJ or fam in ("ROVER-K-1.8", "ROVER-KV6-2.5", "ROVER-L-2.0DI"):
        return "Rover"
    if fam == "M47-2.0":
        return "BMW"
    if fam in FORD:
        return "Ford"
    return "SAIC"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "MG", motoriste)
L = []

# ---------------------------------------------------------------- MG britannique
mg(L, "MG TD", "TD", "1", "1950-01", "1953-08", [("1.25 54", "MG-XPAG-1.25", 87)], portes=2, places=2, reservoir=55, remarques="Roadster ; données indicatives")
mg(L, "MGA", "MGA", "1", "1955-09", "1962-07",
   [("1500 1.5 69", "BMC-B-1.5", 110, {"fin": "1959-05"}), ("1600 1.6 80", "BMC-B-1.6", 118, {"debut": "1959-05"})], portes=2, places=2, reservoir=45,
   remarques="Roadster et coupé ; Twin Cam (1958-1960) non reprise ; données indicatives")
mg(L, "MGB", "MGB", "1", "1962-09", "1980-10", [("1.8 95", "BMC-B-1.8", 149)], portes=2, places=2, reservoir=55,
   remarques="Roadster et GT ; MGB GT V8 (1973-1976) et MGC non repris ; données indicatives")
mg(L, "MG Midget", "Midget", "1", "1961-06", "1979-12",
   [("948 0.95 47", "BMC-A-0.95", 72, {"fin": "1962-10"}), ("1098 1.1 56", "BMC-A-1.1", 84, {"debut": "1962-10", "fin": "1966-09"}),
    ("1275 1.3 65", "BMC-A-1.3", 98, {"debut": "1966-10", "fin": "1974-09"}), ("1500 1.5 66", "TRIUMPH-1.5", 105, {"debut": "1974-10"})], portes=2, places=2,
   reservoir=32, remarques="Données indicatives")
mg(L, "MG Metro", "Metro", "1", "1982-05", "1990-12", [("1.3 72", "BMC-A-1.3", 99), ("Turbo 1.3 93", "BMC-A-1.3T", 115, {"debut": "1983-10"})], portes=3, places=4,
   reservoir=35, remarques="Austin Metro sportive ; données indicatives")
mg(L, "MG TF", "MGF", "1", "1995-09", "2002-02",
   [("MGF 1.8 120", "ROVER-K-1.8", 165), ("MGF VVC 1.8 145", "ROVER-K-1.8", 174), ("MGF 1.6 112", "ROVER-K-1.6", 145, {"debut": "2000-01"})], portes=2, places=2, reservoir=50,
   remarques="MGF à moteur central")
mg(L, "MG TF", "TF", "1", "2002-03", "2011-12",
   [("1.6 115", "ROVER-K-1.6", 145), ("1.8 135", "ROVER-K-1.8", 165), ("1.8 VVC 160", "ROVER-K-1.8", 174)], portes=2, places=2, reservoir=50,
   remarques="Arrêt en 2005 (faillite MG Rover), puis reprise par NAC/SAIC (2007-2011) ; données indicatives")
mg(L, "MG ZR", "ZR", "1", "2001-06", "2005-04",
   [("1.4 105", "ROVER-K-1.4", 130), ("1.8 120", "ROVER-K-1.8", 165), ("1.8 VVC 160", "ROVER-K-1.8", 174), ("2.0 TD 101", "ROVER-L-2.0DI", 240)], portes=5, places=5,
   reservoir=50, remarques="Base Rover 25")
mg(L, "MG ZS", "ZS (Rover)", "1", "2001-06", "2005-04", [("1.8 120", "ROVER-K-1.8", 165), ("2.5 V6 177", "ROVER-KV6-2.5", 240), ("2.0 TD 113", "ROVER-L-2.0DI", 260)],
   portes=5, places=5, reservoir=55, remarques="Base Rover 45 ; berline et 5 portes")
mg(L, "MG7", "ZT", "1", "2001-06", "2005-04",
   [("ZT 1.8 Turbo 160", "ROVER-K-1.8T", 215), ("ZT 2.5 V6 190", "ROVER-KV6-2.5", 245), ("ZT CDTi 2.0 135", "M47-2.0", 300), ("ZT 260 4.6 V8 260", "MODULAR-4.6", 410, {"debut": "2003-06"})],
   portes=4, places=5, reservoir=65, remarques="MG ZT (base Rover 75), devenue MG7 en Chine (2007-2016)")
mg(L, "MG XPower SV", "SV", "1", "2003-10", "2005-04", [("4.6 V8 320", "MODULAR-4.6-DOHC", 410), ("SV-R 5.0 V8 385", "MODULAR-4.6-DOHC", 510, {"debut": "2004-06"})],
   portes=2, places=2, reservoir=75, remarques="Coupé carbone (base Qvale Mangusta), environ 80 exemplaires ; données indicatives (5.0 rattaché à la famille 4.6)")

# ---------------------------------------------------------------- MG SAIC
mg(L, "MG6", "MG6", "1", "2011-06", "2016-12", [("1.8 Turbo 160", "ROVER-K-1.8T", 215), ("1.9 DTi 150", "SAIC-1.9D", 350, {"debut": "2012-06"})], portes=5, places=5,
   reservoir=50, remarques="Berline et 5 portes GT")
mg(L, "MG3", "MG3", "1", "2013-09", "2023-12", [("1.5 106", "SAIC-1.5", 141)], portes=5, places=5, reservoir=45, remarques="Restylage 2018")
mg(L, "MG3", "MG3 Hybrid+", "1", "2024-03", None, [("Hybrid+ 1.5 194", "SAIC-1.5-HEV", 128)], portes=5, places=5, reservoir=36,
   remarques="Hybride (puissance système) ; mise à jour MY26,5 (moteur refroidi par huile)")
mg(L, "MG ZS", "ZS", "1", "2017-10", "2024-03", [("1.5 106", "SAIC-1.5", 141), ("1.0 T-GDI 111", "SAIC-1.0T", 160)], portes=5, places=5, reservoir=48,
   remarques="SUV compact ; restylage 2020")
mg(L, "MG ZS", "ZS (2024)", "1", "2024-04", None, [("Hybrid+ 1.5 197", "SAIC-1.5-HEV", 128), ("1.5 106", "SAIC-1.5", 141)], portes=5, places=5, reservoir=44,
   remarques="Deuxième génération (thermique et hybride) ; mise à jour MY26,5")
mg(L, "MG ZS EV", "ZS EV", "1", "2019-09", "2021-08", [("EV 143", "MG-EV", 353, el(44))], portes=5, places=5, reservoir=0)
mg(L, "MG ZS EV", "ZS EV", "2", "2021-09", "2024-12", [("Standard Range 177", "MG-EV", 280, el(51)), ("Long Range 156", "MG-EV", 280, el(72))], portes=5, places=5,
   reservoir=0, remarques="Restylage ; remplacé par le MGS5 EV")
mg(L, "MG5", "MG5 EV", "1", "2020-09", "2024-12", [("Standard 156", "MG-EV", 280, el(50)), ("Long Range 156", "MG-EV", 280, el(61)), ("Long Range 177", "MG-EV", 280, el(61, debut="2022-06"))], portes=5, places=5, reservoir=0,
   remarques="MG5 EV, break électrique")
mg(L, "MG HS", "HS", "1", "2019-06", "2024-12", [("1.5 T-GDI 162", "SAIC-1.5T", 250), ("EHS PHEV 1.5 T 258", "SAIC-1.5T-PHEV", 370, {"debut": "2020-06", "batterie": 17})],
   portes=5, places=5, reservoir=55, remarques="EHS hybride rechargeable")
mg(L, "MG HS", "HS (2024)", "1", "2024-09", None,
   [("1.5 T-GDI 170", "SAIC-1.5T", 275), ("PHEV 1.5 T 272", "SAIC-1.5T-PHEV", 370, {"debut": "2025-01", "batterie": 21}),
    ("Hybrid+ 1.5 224", "SAIC-1.5-HEV", 128, {"debut": "2025-06"})], portes=5, places=5, reservoir=57, remarques="Deuxième génération ; données indicatives")
mg(L, "MG HS PHEV", "HS", "1", "2020-06", "2024-12", [("EHS PHEV 1.5 T 258", "SAIC-1.5T-PHEV", 370, {"batterie": 17})], portes=5, places=5, reservoir=37,
   remarques="Ancienne ligne conservée ; voir MG HS")
mg(L, "MG4 EV", "EH32", "1", "2022-09", "2025-12",
   [("Standard 170", "MG-EV", 250, el(51)), ("Comfort 204", "MG-EV", 250, el(64)), ("Extended Range 245", "MG-EV", 350, el(77, debut="2023-06")),
    ("XPower AWD 435", "MG-EV", 600, el(64, debut="2023-09"))], portes=5, places=5, reservoir=0, remarques="Plateforme MSP")
mg(L, "MG4 EV", "EH32", "2", "2026-01", None,
   [("Standard 170", "MG-EV", 250, el(51)), ("Comfort 204", "MG-EV", 250, el(64)), ("Extended Range 245", "MG-EV", 350, el(77))], portes=5, places=5, reservoir=0,
   remarques="Restylage européen ; données indicatives")
mg(L, "MG Cyberster", "Cyberster", "1", "2024-06", None, [("RWD 340", "MG-EV", 475, el(77)), ("AWD 510", "MG-EV", 725, el(77))], portes=2, places=2, reservoir=0,
   remarques="Roadster électrique à portes en élytre")
mg(L, "MGS5 EV", "S5", "1", "2025-05", None, [("Standard 170", "MG-EV", 250, el(49)), ("Long Range 231", "MG-EV", 350, el(64))], portes=5, places=5, reservoir=0,
   remarques="Remplace le ZS EV ; données indicatives")
mg(L, "MGS6 EV", "S6", "1", "2026-03", None, [("RWD 245", "MG-EV", 350, el(77)), ("AWD 359", "MG-EV", 550, el(77))], portes=5, places=5, reservoir=0,
   remarques="SUV familial électrique de 4,71 m ; données indicatives")

MOT = Motorisations("MG", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"MG": L}
MOTEURS = MOT.moteurs()
