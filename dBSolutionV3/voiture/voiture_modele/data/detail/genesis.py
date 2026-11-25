"""Genesis : générations, phases, motorisations (marché européen) et moteurs liés.
Genesis Coupe et Genesis DH (vendues en Europe sous la marque Hyundai), G70 (+ Shooting Brake), G80, Electrified G80, G90,
GV60 (+ Magma), GV70, Electrified GV70, GV80 (+ Coupé). Les G70, G80 et GV80 thermiques sont retirées du catalogue
européen en 2025 (vente sur stock), dates de fin indicatives.
Genesis G70 Sport : versions sportives de la G70 (V6 3.3T, 2.5T) du marché nord-américain, hp convertis en ch (×1,014).
Moteurs : familles de hyundai.py reprises (motoriste « Hyundai ») et familles propres ajoutées au même motoriste.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .hyundai import FAMILLES as FAMILLES_HYUNDAI

E_, D = "ESS", "DSL"
C = "CHAINE"

AJOUTS = {
    "SMARTSTREAM-2.5T": f("TURBO", E_, 2.5, C, 4, 5800, 1650, "0W30", 5.7, 15000),
    "LAMBDA-3.3TT": f("TURBO", E_, 3.3, C, 6, 6000, 1300, "5W30", 6.1, 15000, a="V"),
    "SMARTSTREAM-3.5TT": f("TURBO", E_, 3.5, C, 6, 5800, 1300, "0W30", 6.6, 15000, a="V"),
    "SMARTSTREAM-3.5TT-MHEV": f("HYB_E", E_, 3.5, C, 6, 5800, 1300, "0W30", 6.6, 15000, a="V"),
    "SMARTSTREAM-D3.0": f("TURBO", D, 3.0, C, 6, 3800, 1500, "0W30", 6.9, 15000),
}
HYUNDAI = ("THETA-2.0T", "LAMBDA-3.8V6", "R-2.2CRDi", "HYUNDAI-EV")
FAMILLES = {**{k: FAMILLES_HYUNDAI[k] for k in HYUNDAI}, **AJOUTS}


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


NA = "Marché nord-américain (hp convertis en ch)"
RETRAIT = "retirée du catalogue européen en 2025, vente sur stock ; date de fin indicative"
mg = SaisieMoteurs(FAMILLES, "Hyundai")
L = []

# ---------------------------------------------------------------- avant la marque
mg(L, "Genesis Coupe", "BK", "1", "2010-03", "2012-12", [("2.0 Turbo 213", "THETA-2.0T", 302), ("3.8 V6 303", "LAMBDA-3.8V6", 361)],
   portes=2, places=4, reservoir=65, remarques="Vendue en Europe sous la marque Hyundai")
mg(L, "G80", "DH", "1", "2014-11", "2016-12", [("3.8 V6 GDI 4WD 315", "LAMBDA-3.8V6", 397)], portes=4, reservoir=77,
   remarques="Vendue en Europe comme Hyundai Genesis ; devenue Genesis G80 en 2016")

# ---------------------------------------------------------------- berlines
mg(L, "G70", "IK", "2", "2021-06", "2025-01",
   [("2.0T 197", "THETA-2.0T", 353), ("2.0T 245", "THETA-2.0T", 353), ("2.0T AWD 245", "THETA-2.0T", 353), ("2.2D 200", "R-2.2CRDi", 440),
    ("2.2D AWD 200", "R-2.2CRDi", 440)], portes=4, reservoir=60,
   remarques="Lancement européen sur la G70 restylée ; Shooting Brake (break propre à l'Europe, novembre 2021) ; " + RETRAIT)
mg(L, "G80", "RG3", "1", "2021-06", "2025-01",
   [("2.5T 304", "SMARTSTREAM-2.5T", 422), ("2.5T AWD 304", "SMARTSTREAM-2.5T", 422), ("2.2D 210", "R-2.2CRDi", 441),
    ("2.2D AWD 210", "R-2.2CRDi", 441)], portes=4, reservoir=73, remarques=RETRAIT)
mg(L, "G80 Electrified", "RG3 EV", "1", "2022-03", "2025-06", [("AWD 370", "HYUNDAI-EV", 700, el(87))], portes=4, reservoir=0,
   remarques="Electrified G80, batterie 87,2 kWh")
mg(L, "G80 Electrified", "RG3 EV", "2", "2025-07", None, [("AWD 370", "HYUNDAI-EV", 700, el(94))], portes=4, reservoir=0,
   remarques="Restylage, batterie 94,5 kWh ; date indicative")
mg(L, "G90", "RS4", "1", "2023-06", None, [("3.5T V6 48V AWD 415", "SMARTSTREAM-3.5TT-MHEV", 549)], portes=4, reservoir=83,
   remarques="Distribution européenne limitée (sur consultation)")

# ---------------------------------------------------------------- SUV
mg(L, "GV60", "JW", "1", "2021-11", "2025-05",
   [("RWD 229", "HYUNDAI-EV", 350, el(77)), ("AWD 318", "HYUNDAI-EV", 605, el(77)), ("Performance AWD 490", "HYUNDAI-EV", 700, el(77))],
   reservoir=0, remarques="E-GMP 800 V ; Performance : 435 ch, 490 ch en mode Boost")
mg(L, "GV60", "JW", "2", "2025-06", None,
   [("RWD 229", "HYUNDAI-EV", 350, el(84)), ("AWD 318", "HYUNDAI-EV", 605, el(84)), ("Performance AWD 490", "HYUNDAI-EV", 700, el(84)),
    ("Magma AWD 609", "HYUNDAI-EV", 740, el(84, debut="2026-06"))], reservoir=0,
   remarques="Restylage, batterie 84 kWh ; GV60 Magma (650 ch en mode Boost) ; dates indicatives")
mg(L, "GV70", "JK1", "1", "2021-06", "2024-06",
   [("2.5T AWD 304", "SMARTSTREAM-2.5T", 422), ("2.2D AWD 210", "R-2.2CRDi", 441), ("2.2D 210", "R-2.2CRDi", 441)], reservoir=66)
mg(L, "GV70", "JK1", "2", "2024-07", None, [("2.5T AWD 304", "SMARTSTREAM-2.5T", 422)], reservoir=66,
   remarques="Restylage ; diesel abandonné ; disponibilité européenne réduite depuis 2025")
mg(L, "GV70", "JK1 EV", "1", "2022-06", "2025-02", [("Electrified AWD 435", "HYUNDAI-EV", 700, el(77))], reservoir=0,
   remarques="Electrified GV70, 490 ch en mode Boost")
mg(L, "GV70", "JK1 EV", "2", "2025-03", None, [("Electrified AWD 435", "HYUNDAI-EV", 700, el(84))], reservoir=0,
   remarques="Electrified GV70 restylé, batterie 84 kWh, 490 ch en mode Boost ; date indicative")
mg(L, "GV80", "JX1", "1", "2021-06", "2023-12",
   [("2.5T AWD 304", "SMARTSTREAM-2.5T", 422), ("3.0D AWD 278", "SMARTSTREAM-D3.0", 588), ("3.5T AWD 380", "SMARTSTREAM-3.5TT", 530)],
   places=7, reservoir=80, remarques="5 ou 7 places")
mg(L, "GV80", "JX1", "2", "2024-01", "2025-06",
   [("2.5T AWD 304", "SMARTSTREAM-2.5T", 422), ("3.5T AWD 380", "SMARTSTREAM-3.5TT", 530),
    ("Coupé 3.5T AWD 380", "SMARTSTREAM-3.5TT", 530, {"debut": "2024-06"}), ("Coupé 3.5T 48V AWD 415", "SMARTSTREAM-3.5TT-MHEV", 549, {"debut": "2024-06"})],
   places=7, reservoir=80, remarques="Restylage ; GV80 Coupé (5 places) ; " + RETRAIT)

# ---------------------------------------------------------------- Genesis G70 Sport (Amérique du Nord)
LS = []
mg(LS, "G70", "IK", "1", "2018-09", "2021-09",
   [("Sport 2.0T 256", "THETA-2.0T", 353), ("Sport 3.3T V6 370", "LAMBDA-3.3TT", 510), ("Sport 3.3T V6 AWD 370", "LAMBDA-3.3TT", 510)],
   portes=4, reservoir=60, remarques=NA + " ; 2.0T Sport en boîte manuelle (millésimes 2019-2020)")
mg(LS, "G70", "IK", "2", "2021-10", "2023-12",
   [("Sport 3.3T V6 370", "LAMBDA-3.3TT", 510), ("Sport 3.3T V6 AWD 370", "LAMBDA-3.3TT", 510)], portes=4, reservoir=60, remarques=NA + " ; restylage")
mg(LS, "G70", "IK", "3", "2024-01", None,
   [("Sport 2.5T 304", "SMARTSTREAM-2.5T", 422), ("Sport 3.3T V6 380", "LAMBDA-3.3TT", 530), ("Sport 3.3T V6 AWD 380", "LAMBDA-3.3TT", 530)],
   portes=4, reservoir=60, remarques=NA + " ; millésime 2024 : 2.5T remplace le 2.0T, V6 porté à 375 hp")

MOT = Motorisations("Hyundai", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LS)

DETAIL = {"Genesis": L, "Genesis G70 Sport": LS}
MOTEURS = MOT.moteurs()
