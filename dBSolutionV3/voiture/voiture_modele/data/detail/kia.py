"""Kia : générations, phases, motorisations (marché européen) et moteurs liés.
Kia : Picanto, Rio, Ceed (+ SW), ProCeed, XCeed, K4, Venga, Soul, Niro, Stonic, Seltos, Sportage, Sorento, Carens,
Carnival/Sedona, Optima, EV2, EV3, EV4, EV5, EV6, EV9 ; modèles nord-américains : K5 (DL3), Telluride.
Kia GT : Ceed GT, ProCeed GT, Optima GT, Stinger, EV6 GT, EV9 GT, EV3 GT, EV4 GT, EV5 GT ; Forte GT et K5 GT
(marché nord-américain, hp convertis en ch ×1,014). La marque « Kia Stinger GT » n'est pas traitée ici.
Moteurs : familles et codes de hyundai.py et genesis.py (motoriste « Hyundai ») ; quelques familles propres ajoutées au même
motoriste. Couples des versions non documentées indicatifs.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .genesis import FAMILLES as FAMILLES_GENESIS
from .hyundai import FAMILLES as FAMILLES_HYUNDAI

E_, D = "ESS", "DSL"
C = "CHAINE"

PROPRES = {
    "A-2.5CRDi": f("TURBO", D, 2.5, C, 4, 3800, 2000, "5W30", 6.5, 15000),
    "J3-2.9CRDi": f("TURBO", D, 2.9, C, 4, 3800, 2000, "5W30", 7.5, 15000),
    "NU-2.0-PHEV": f("HYB_TE", E_, 2.0, C, 4, 6000, 4500, "0W20", 4.0, 15000),
    "SMARTSTREAM-2.0": f("ATM", E_, 2.0, C, 4, 6200, 4500, "0W20", 4.2, 15000),
}
FAMILLES = {**FAMILLES_HYUNDAI, **{k: FAMILLES_GENESIS[k] for k in ("SMARTSTREAM-2.5T", "LAMBDA-3.3TT")}, **PROPRES}


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


NA = "Marché nord-américain (hp convertis en ch)"
mg = SaisieMoteurs(FAMILLES, "Hyundai")
L = []

# ---------------------------------------------------------------- citadines
mg(L, "Picanto", "SA", "1", "2004-04", "2011-03",
   [("1.0 61", "EPSILON-1.0", 86), ("1.1 65", "EPSILON-1.1", 97), ("1.1 CRDi 75", "U-1.1CRDi", 154, {"debut": "2005-06", "fin": "2008-06"})],
   reservoir=35, remarques="Morning en Corée ; restylage 2008")
mg(L, "Picanto", "TA", "1", "2011-04", "2017-03", [("1.0 69", "KAPPA-1.0", 94), ("1.25 85", "KAPPA-1.25", 121)], reservoir=35, remarques="3 et 5 portes")
mg(L, "Picanto", "JA", "1", "2017-04", "2023-06",
   [("1.0 67", "KAPPA-1.0", 96), ("1.25 84", "KAPPA-1.25", 122), ("1.0 T-GDi 100", "KAPPA-1.0T", 172, {"debut": "2017-09"})], reservoir=35,
   remarques="GT Line et X-Line ; restylage 2020")
mg(L, "Picanto", "JA", "2", "2023-07", None, [("1.0 63", "KAPPA-1.0", 93), ("1.2 79", "KAPPA-1.2", 114)], reservoir=35, remarques="Second restylage")
mg(L, "Rio", "JB", "1", "2005-04", "2011-08",
   [("1.4 97", "GAMMA-1.4", 125), ("1.6 112", "GAMMA-1.6", 145), ("1.5 CRDi 110", "U-1.5CRDi", 235)], reservoir=45)
mg(L, "Rio", "UB", "1", "2011-09", "2017-02",
   [("1.25 85", "KAPPA-1.25", 121), ("1.4 109", "GAMMA-1.4", 137), ("1.1 CRDi 75", "U-1.1CRDi", 180), ("1.4 CRDi 90", "U-1.4CRDi", 220)], reservoir=43)
mg(L, "Rio", "YB", "1", "2017-03", "2020-08",
   [("1.25 84", "KAPPA-1.25", 122), ("1.0 T-GDi 100", "KAPPA-1.0T", 172), ("1.0 T-GDi 120", "KAPPA-1.0T", 172), ("1.4 CRDi 77", "U-1.4CRDi", 240),
    ("1.4 CRDi 90", "U-1.4CRDi", 240)], reservoir=45)
mg(L, "Rio", "YB", "2", "2020-09", "2023-06",
   [("1.2 84", "KAPPA-1.2", 118), ("1.0 T-GDi 48V 100", "KAPPA-1.0T-MHEV", 172), ("1.0 T-GDi 48V 120", "KAPPA-1.0T-MHEV", 200)], reservoir=45,
   remarques="Restylage ; retiré d'Europe en 2023")
mg(L, "EV2", "SY1", "1", "2026-02", None,
   [("Standard Range 147", "HYUNDAI-EV", 250, el(42)), ("Long Range 135", "HYUNDAI-EV", 250, el(61, debut="2026-06"))], reservoir=0,
   remarques="SUV urbain électrique E-GMP 400 V produit à Žilina")

# ---------------------------------------------------------------- compactes
mg(L, "Ceed", "ED", "1", "2007-01", "2012-04",
   [("1.4 109", "GAMMA-1.4", 137), ("1.6 122", "GAMMA-1.6", 154), ("2.0 143", "BETA-2.0", 186), ("1.6 CRDi 90", "U-1.6CRDi", 235),
    ("1.6 CRDi 115", "U-1.6CRDi", 255), ("2.0 CRDi 140", "D-2.0CRDi", 305)], reservoir=53, remarques="5 portes, SW et pro_cee'd 3 portes ; restylage 2009")
mg(L, "Ceed", "JD", "1", "2012-05", "2018-05",
   [("1.4 100", "GAMMA-1.4", 134), ("1.6 GDI 135", "GAMMA-1.6GDI", 164), ("1.0 T-GDi 120", "KAPPA-1.0T", 172, {"debut": "2015-06"}),
    ("1.4 CRDi 90", "U-1.4CRDi", 220), ("1.6 CRDi 110", "U-1.6CRDi", 260), ("1.6 CRDi 128", "U-1.6CRDi", 260, {"fin": "2015-05"}),
    ("1.6 CRDi 136", "U-1.6CRDi", 300, {"debut": "2015-06"})], reservoir=53, remarques="5 portes, SW et pro_cee'd ; restylage 2015")
mg(L, "Ceed", "CD", "1", "2018-06", "2021-08",
   [("1.4 MPi 100", "GAMMA-1.4", 134), ("1.0 T-GDi 120", "KAPPA-1.0T", 172), ("1.4 T-GDi 140", "KAPPA-1.4T", 242), ("1.6 CRDi 115", "U3-1.6CRDi", 280),
    ("1.6 CRDi 136", "U3-1.6CRDi", 320), ("SW 1.6 GDi PHEV 141", "KAPPA-1.6-PHEV", 265, {"debut": "2020-03", "batterie": 9})], reservoir=50,
   remarques="5 portes et SW ; produite à Žilina")
mg(L, "Ceed", "CD", "2", "2021-09", "2026-09",
   [("1.0 T-GDi 48V 120", "KAPPA-1.0T-MHEV", 200), ("1.5 T-GDi 48V 160", "SMARTSTREAM-1.5T-MHEV", 253), ("1.6 CRDi 48V 136", "U3-1.6CRDi-MHEV", 280),
    ("SW 1.6 GDi PHEV 141", "KAPPA-1.6-PHEV", 265, {"batterie": 9})], reservoir=50,
   remarques="Restylage ; remplacée par la K4 (production à partir d'octobre 2026) ; date de fin indicative")
mg(L, "ProCeed", "CD", "1", "2019-01", "2025-12",
   [("1.0 T-GDi 120", "KAPPA-1.0T", 172, {"fin": "2021-08"}), ("1.4 T-GDi 140", "KAPPA-1.4T", 242, {"fin": "2021-08"}),
    ("1.5 T-GDi 48V 160", "SMARTSTREAM-1.5T-MHEV", 253, {"debut": "2021-09"})], reservoir=50,
   remarques="Shooting brake ; version GT dans Kia GT ; date de fin indicative")
mg(L, "XCeed", "CD CUV", "1", "2019-09", "2022-05",
   [("1.0 T-GDi 120", "KAPPA-1.0T", 172), ("1.4 T-GDi 140", "KAPPA-1.4T", 242), ("1.6 T-GDi 204", "GAMMA-1.6T", 265, {"debut": "2020-06"}),
    ("1.6 CRDi 48V 136", "U3-1.6CRDi-MHEV", 280), ("1.6 GDi PHEV 141", "KAPPA-1.6-PHEV", 265, {"debut": "2020-03", "batterie": 9})], reservoir=50)
mg(L, "XCeed", "CD CUV", "2", "2022-06", None,
   [("1.0 T-GDi 120", "KAPPA-1.0T", 172), ("1.5 T-GDi 48V 160", "SMARTSTREAM-1.5T-MHEV", 253), ("1.6 GDi PHEV 141", "KAPPA-1.6-PHEV", 265, {"batterie": 9, "fin": "2024-12"})],
   reservoir=50, remarques="Restylage ; nouveau restylage annoncé pour 2026")
mg(L, "K4", "CL4", "1", "2026-10", None, [("1.6 Hybrid 141", "KAPPA-1.6-HEV", 265)], reservoir=42,
   remarques="Remplaçante de la Ceed (berline 5 portes et Sportswagon) ; production européenne depuis octobre 2026 ; données indicatives")
mg(L, "Venga", "YN", "1", "2010-02", "2019-06",
   [("1.4 90", "GAMMA-1.4", 137), ("1.6 125", "GAMMA-1.6", 156), ("1.4 CRDi 77", "U-1.4CRDi", 220), ("1.4 CRDi 90", "U-1.4CRDi", 220),
    ("1.6 CRDi 128", "U-1.6CRDi", 260, {"fin": "2014-12"})], reservoir=48, remarques="Monospace compact ; restylage 2015")
mg(L, "Soul", "AM", "1", "2009-02", "2013-12", [("1.6 126", "GAMMA-1.6", 156), ("1.6 CRDi 128", "U-1.6CRDi", 260)], reservoir=48)
mg(L, "Soul", "PS", "1", "2014-01", "2019-05",
   [("1.6 GDI 132", "GAMMA-1.6GDI", 161), ("1.6 CRDi 128", "U-1.6CRDi", 260), ("EV 110", "HYUNDAI-EV", 285, el(27, debut="2014-09"))], reservoir=54)
mg(L, "Soul", "SK3", "1", "2019-06", "2023-12", [("e-Soul 136", "HYUNDAI-EV", 395, el(39)), ("e-Soul 204", "HYUNDAI-EV", 395, el(64))], reservoir=0,
   remarques="Uniquement électrique en Europe")

# ---------------------------------------------------------------- SUV
mg(L, "Stonic", "YB CUV", "1", "2017-09", "2020-08",
   [("1.25 84", "KAPPA-1.25", 122), ("1.4 100", "GAMMA-1.4", 134), ("1.0 T-GDi 120", "KAPPA-1.0T", 172), ("1.6 CRDi 110", "U3-1.6CRDi", 280)], reservoir=45)
mg(L, "Stonic", "YB CUV", "2", "2020-09", "2025-02",
   [("1.2 84", "KAPPA-1.2", 118), ("1.0 T-GDi 100", "KAPPA-1.0T", 172), ("1.0 T-GDi 48V 100", "KAPPA-1.0T-MHEV", 172), ("1.0 T-GDi 48V 120", "KAPPA-1.0T-MHEV", 200)],
   reservoir=45, remarques="Restylage")
mg(L, "Stonic", "YB CUV", "3", "2025-03", None,
   [("1.0 T-GDi 100", "KAPPA-1.0T", 172), ("1.0 T-GDi 48V 115", "KAPPA-1.0T-MHEV", 200)], reservoir=45, remarques="Second restylage ; données indicatives")
mg(L, "Seltos", "SP3", "1", "2026-11", None, [("1.6 Hybrid 154", "KAPPA-1.6-HEV", 265), ("1.6 Hybrid e-AWD 178", "KAPPA-1.6-HEV", 265)], reservoir=47,
   remarques="Première européenne au Mondial 2026 ; 2 ou 4 roues motrices (e-AWD) ; date et couples indicatifs")
mg(L, "Niro", "DE", "1", "2016-07", "2022-06",
   [("1.6 GDi Hybrid 141", "KAPPA-1.6-HEV", 265), ("1.6 GDi PHEV 141", "KAPPA-1.6-PHEV", 265, {"debut": "2017-09", "batterie": 9}),
    ("e-Niro 136", "HYUNDAI-EV", 395, el(39, debut="2018-12")), ("e-Niro 204", "HYUNDAI-EV", 395, el(64, debut="2018-12"))], reservoir=45,
   remarques="Restylage 2019")
mg(L, "Niro", "SG2", "1", "2022-07", None,
   [("1.6 GDi Hybrid 141", "KAPPA-1.6-HEV", 265), ("1.6 GDi PHEV 183", "KAPPA-1.6-PHEV", 265, {"batterie": 11}), ("EV 204", "HYUNDAI-EV", 255, el(65))],
   reservoir=42, remarques="Restylage annoncé pour 2026")
mg(L, "Sportage", "JE", "1", "2004-09", "2010-06",
   [("2.0 141", "BETA-2.0", 184), ("2.7 V6 175", "DELTA-2.7V6", 241), ("2.0 CRDi 113", "D-2.0CRDi", 245), ("2.0 CRDi 140", "D-2.0CRDi", 305, {"debut": "2006-01"}),
    ("2.0 CRDi 150", "D-2.0CRDi", 305, {"debut": "2008-06"})], reservoir=58)
mg(L, "Sportage", "SL", "1", "2010-07", "2015-12",
   [("1.6 GDI 135", "GAMMA-1.6GDI", 164, {"debut": "2011-06"}), ("2.0 163", "THETA-2.0", 197), ("1.7 CRDi 116", "U-1.7CRDi", 260),
    ("2.0 CRDi 136", "R-2.0CRDi", 320), ("2.0 CRDi 184", "R-2.0CRDi", 383)], reservoir=58, remarques="Restylage 2014")
mg(L, "Sportage", "QL", "1", "2016-01", "2018-07",
   [("1.6 GDI 132", "GAMMA-1.6GDI", 161), ("1.6 T-GDi 177", "GAMMA-1.6T", 265), ("1.7 CRDi 116", "U-1.7CRDi", 280), ("1.7 CRDi 141", "U-1.7CRDi", 340),
    ("2.0 CRDi 136", "R-2.0CRDi", 373), ("2.0 CRDi 185", "R-2.0CRDi", 400)], reservoir=62)
mg(L, "Sportage", "QL", "2", "2018-08", "2021-08",
   [("1.6 GDI 132", "GAMMA-1.6GDI", 161), ("1.6 T-GDi 177", "GAMMA-1.6T", 265), ("1.6 CRDi 115", "U3-1.6CRDi", 280), ("1.6 CRDi 136", "U3-1.6CRDi", 320),
    ("2.0 CRDi 48V 185", "R-2.0CRDi-MHEV", 400)], reservoir=62, remarques="Restylage")
mg(L, "Sportage", "NQ5", "1", "2021-09", "2024-12",
   [("1.6 T-GDi 150", "SMARTSTREAM-1.6T", 250), ("1.6 T-GDi 48V 150", "SMARTSTREAM-1.6T-MHEV", 250), ("1.6 T-GDi 48V 4x4 180", "SMARTSTREAM-1.6T-MHEV", 265),
    ("1.6 CRDi 115", "U3-1.6CRDi", 280), ("1.6 CRDi 48V 136", "U3-1.6CRDi-MHEV", 320), ("1.6 T-GDi HEV 230", "SMARTSTREAM-1.6T-HEV", 350),
    ("1.6 T-GDi PHEV 4x4 265", "SMARTSTREAM-1.6T-PHEV", 350, {"batterie": 14})], reservoir=54, remarques="Version européenne à empattement court, produite à Žilina")
mg(L, "Sportage", "NQ5", "2", "2025-01", None,
   [("1.6 T-GDi 48V 160", "SMARTSTREAM-1.6T-MHEV", 250), ("1.6 CRDi 48V 136", "U3-1.6CRDi-MHEV", 320), ("1.6 T-GDi HEV 215", "SMARTSTREAM-1.6T-HEV", 367),
    ("1.6 T-GDi PHEV 4x4 252", "SMARTSTREAM-1.6T-PHEV", 367, {"batterie": 14})], reservoir=54, remarques="Restylage ; puissances alignées sur le Tucson restylé, indicatives")
mg(L, "Sorento", "BL", "1", "2002-08", "2009-12",
   [("2.5 CRDi 140", "A-2.5CRDi", 343), ("2.5 CRDi 170", "A-2.5CRDi", 392, {"debut": "2006-09"}), ("3.3 V6 247", "LAMBDA-3.3V6", 307, {"debut": "2006-09"})],
   reservoir=80, remarques="4x4 à châssis séparé ; restylage 2006 ; versions essence 2.4 et 3.5 V6 non reprises")
mg(L, "Sorento", "XM", "1", "2009-11", "2014-12",
   [("2.4 174", "THETA-2.4", 227), ("2.0 CRDi 150", "R-2.0CRDi", 383), ("2.2 CRDi 197", "R-2.2CRDi", 421)], places=7, reservoir=70, remarques="Restylage 2012")
mg(L, "Sorento", "UM", "1", "2015-01", "2020-08", [("2.2 CRDi 200", "R-2.2CRDi", 440), ("2.4 GDI 188", "THETA-2.4GDI", 241)], places=7, reservoir=71,
   remarques="Restylage 2018")
mg(L, "Sorento", "MQ4", "1", "2020-09", "2024-06",
   [("2.2 CRDi 202", "R-2.2CRDi", 440), ("1.6 T-GDi HEV 230", "SMARTSTREAM-1.6T-HEV", 350), ("1.6 T-GDi PHEV 4x4 265", "SMARTSTREAM-1.6T-PHEV", 350, {"batterie": 14})],
   places=7, reservoir=67)
mg(L, "Sorento", "MQ4", "2", "2024-07", None,
   [("2.2 CRDi 194", "R-2.2CRDi", 440), ("1.6 T-GDi HEV 215", "SMARTSTREAM-1.6T-HEV", 367), ("1.6 T-GDi PHEV 4x4 253", "SMARTSTREAM-1.6T-PHEV", 367, {"batterie": 14})],
   places=7, reservoir=67, remarques="Restylage")
mg(L, "Telluride", "ON", "1", "2019-03", "2025-12", [("3.8 V6 295", "LAMBDA-3.8V6", 355)], places=8, reservoir=71,
   remarques=NA + " ; restylage 2022 ; nouvelle génération pour le millésime 2027")

# ---------------------------------------------------------------- monospaces et berlines
mg(L, "Carens", "UN", "1", "2006-06", "2013-03", [("1.6 126", "GAMMA-1.6", 156), ("2.0 144", "THETA-2.0", 189), ("2.0 CRDi 140", "D-2.0CRDi", 305)], places=7,
   reservoir=60)
mg(L, "Carens", "RP", "1", "2013-04", "2019-06", [("1.6 GDI 135", "GAMMA-1.6GDI", 164), ("1.7 CRDi 115", "U-1.7CRDi", 260), ("1.7 CRDi 141", "U-1.7CRDi", 340)],
   places=7, reservoir=58)
mg(L, "Carnival / Sedona", "UP", "1", "1999-01", "2006-06", [("2.5 V6 150", "DELTA-2.5V6", 220), ("2.9 CRDi 144", "J3-2.9CRDi", 309, {"debut": "2001-06"})],
   places=7, reservoir=75, remarques="Carnival en Europe, Sedona en Amérique du Nord ; données indicatives")
mg(L, "Carnival / Sedona", "VQ", "1", "2006-07", "2014-06",
   [("2.7 V6 189", "DELTA-2.7V6", 248), ("2.9 CRDi 185", "J3-2.9CRDi", 343, {"fin": "2010-12"}), ("2.2 CRDi 197", "R-2.2CRDi", 421, {"debut": "2011-01"})],
   places=7, reservoir=80, remarques="Carnival en Europe")
mg(L, "Carnival / Sedona", "KA4", "1", "2020-08", None,
   [("2.2 CRDi 202", "R-2.2CRDi", 440), ("1.6 T-GDi HEV 245", "SMARTSTREAM-1.6T-HEV", 367, {"debut": "2024-06"})], places=8, reservoir=72,
   remarques="Restylage 2024 ; génération YP (2014-2020) non vendue en Europe")
mg(L, "Optima", "TF", "1", "2012-01", "2015-12", [("1.7 CRDi 136", "U-1.7CRDi", 325), ("2.0 CVVT 165", "NU-2.0GDI", 201)], portes=4, reservoir=70,
   remarques="Berline")
mg(L, "Optima", "JF", "1", "2016-01", "2020-06",
   [("1.7 CRDi 141", "U-1.7CRDi", 340, {"fin": "2018-08"}), ("1.6 CRDi 48V 136", "U3-1.6CRDi-MHEV", 320, {"debut": "2018-09"}), ("2.0 GDI 163", "NU-2.0GDI", 196),
    ("2.0 GDI PHEV 205", "NU-2.0-PHEV", 375, {"debut": "2016-12", "batterie": 10})], portes=4, reservoir=70,
   remarques="Berline et Sportswagon ; version GT dans Kia GT ; remplacée en Corée et en Amérique du Nord par la K5")
mg(L, "K5 / Optima", "DL3", "1", "2020-07", "2024-12", [("1.6T 183", "SMARTSTREAM-1.6T", 265), ("2.5 194", "SMARTSTREAM-2.0", 245)], portes=4, reservoir=60,
   remarques=NA + " ; 2.5 Smartstream (famille 2.0 utilisée faute de famille 2.5) ; restylage millésime 2025 ; non vendue en Europe")

# ---------------------------------------------------------------- électriques
mg(L, "EV3", "SV1", "1", "2024-09", None,
   [("Standard Range 204", "HYUNDAI-EV", 283, el(58)), ("Long Range 204", "HYUNDAI-EV", 283, el(81))], reservoir=0, remarques="SUV compact E-GMP 400 V ; version GT dans Kia GT")
mg(L, "EV4", "CV1", "1", "2025-03", None,
   [("Standard Range 204", "HYUNDAI-EV", 283, el(58)), ("Long Range 204", "HYUNDAI-EV", 283, el(81))], portes=5, reservoir=0,
   remarques="Berline et hatchback (produit à Žilina) ; version GT dans Kia GT")
mg(L, "EV5", "OV1", "1", "2025-09", None, [("Long Range 218", "HYUNDAI-EV", 310, el(81))], reservoir=0,
   remarques="SUV familial électrique ; version GT dans Kia GT ; date indicative")
mg(L, "EV6", "CV", "1", "2021-09", "2024-06",
   [("Standard Range 170", "HYUNDAI-EV", 350, el(58)), ("Long Range 229", "HYUNDAI-EV", 350, el(77)), ("Long Range AWD 325", "HYUNDAI-EV", 605, el(77))],
   reservoir=0, remarques="E-GMP 800 V ; version GT dans Kia GT")
mg(L, "EV6", "CV", "2", "2024-07", None,
   [("Standard Range 170", "HYUNDAI-EV", 350, el(63)), ("Long Range 229", "HYUNDAI-EV", 350, el(84)), ("Long Range AWD 325", "HYUNDAI-EV", 605, el(84))],
   reservoir=0, remarques="Restylage")
mg(L, "EV9", "MV", "1", "2023-09", None, [("RWD 204", "HYUNDAI-EV", 350, el(100)), ("AWD 385", "HYUNDAI-EV", 700, el(100))], places=7, reservoir=0,
   remarques="Grand SUV électrique 6 ou 7 places ; version GT dans Kia GT")

# ---------------------------------------------------------------- Kia GT
LG = []
mg(LG, "Ceed GT", "JD", "1", "2013-06", "2018-05", [("GT 1.6 T-GDi 204", "GAMMA-1.6T", 265)], reservoir=53, remarques="5 portes et pro_cee'd GT 3 portes")
mg(LG, "ProCeed GT", "CD", "1", "2019-01", "2025-12", [("GT 1.6 T-GDi 204", "GAMMA-1.6T", 265)], reservoir=50, remarques="Shooting brake ; Ceed GT 5 portes jusqu'en 2021")
mg(LG, "Optima GT", "JF", "1", "2016-01", "2020-06", [("GT 2.0 T-GDi 245", "THETA-2.0T", 353)], portes=4, reservoir=70, remarques="Berline et Sportswagon")
mg(LG, "Stinger", "CK", "1", "2017-10", "2020-08",
   [("2.2 CRDi 200", "R-2.2CRDi", 440), ("2.0 T-GDi 245", "THETA-2.0T", 353), ("GT 3.3 T-GDi V6 370", "LAMBDA-3.3TT", 510)], portes=5, reservoir=60)
mg(LG, "Stinger", "CK", "2", "2020-09", "2023-04", [("GT 3.3 T-GDi V6 366", "LAMBDA-3.3TT", 510)], portes=5, reservoir=60,
   remarques="Restylage ; en Europe uniquement en GT V6 ; production arrêtée en avril 2023")
mg(LG, "Forte GT", "BD", "1", "2019-06", "2024-06", [("GT 1.6T 204", "GAMMA-1.6T", 265)], portes=4, reservoir=50, remarques=NA + " ; K3 en Corée")
mg(LG, "K5 GT", "DL3", "1", "2020-10", "2024-12", [("GT 2.5T 294", "SMARTSTREAM-2.5T", 422)], portes=4, reservoir=60, remarques=NA)
mg(LG, "EV6 GT", "CV", "1", "2022-09", "2024-06", [("GT AWD 585", "HYUNDAI-EV", 740, el(77))], reservoir=0)
mg(LG, "EV6 GT", "CV", "2", "2025-01", None, [("GT AWD 609", "HYUNDAI-EV", 740, el(84))], reservoir=0, remarques="Restylage ; 650 ch en mode Boost")
mg(LG, "EV9 GT", "MV", "1", "2025-06", None, [("GT AWD 509", "HYUNDAI-EV", 740, el(100))], places=6, reservoir=0, remarques="Date et couple indicatifs")
mg(LG, "EV3 GT", "SV1", "1", "2026-09", None, [("GT AWD 292", "HYUNDAI-EV", 480, el(81))], reservoir=0,
   remarques="Bimoteur, révélé au Salon de Bruxelles 2026 ; couple indicatif")
mg(LG, "EV4 GT", "CV1", "1", "2026-09", None, [("GT AWD 292", "HYUNDAI-EV", 480, el(81))], reservoir=0,
   remarques="Hatchback bimoteur ; couple indicatif")
mg(LG, "EV5 GT", "OV1", "1", "2026-09", None, [("GT AWD 306", "HYUNDAI-EV", 605, el(81))], reservoir=0, remarques="Bimoteur E-GMP ; couple indicatif (aligné sur la Ioniq 5 AWD de même puissance)")

MOT = Motorisations("Hyundai", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LG)

DETAIL = {"Kia": L, "Kia GT": LG}
MOTEURS = MOT.moteurs()
