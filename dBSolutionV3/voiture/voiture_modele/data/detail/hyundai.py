"""Hyundai : générations, phases, motorisations (marché européen) et moteurs liés.
Pony, Accent, Getz, Atos, i10, i20, Bayon, Lantra/Elantra, i30, ix20, Matrix, Trajet, Coupé, Veloster, Ioniq, Kona,
Tucson/ix35, Santa Fe, Sonata, i40, Nexo/ix35 Fuel Cell, Staria, Inster, Ioniq 3/5/6/9 ; Palisade (marché nord-américain).
Hyundai N : i20 N, i30 N (+ Fastback N), Kona N, Ioniq 5 N, Ioniq 6 N ; Veloster N et Elantra N (marché nord-américain,
hp convertis en ch ×1,014). Utilitaires (H-1, H350) non repris. Données des générations anciennes indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

FAMILLES = {
    # essence sous licence Mitsubishi
    "ORION-1.3": f("ATM", E_, 1.3, B, 4, 5500, 3500, "10W40", 3.5, 10000),
    "ORION-1.5": f("ATM", E_, 1.5, B, 4, 5500, 3500, "10W40", 3.5, 10000),
    "SIRIUS-1.6": f("ATM", E_, 1.6, B, 4, 6000, 4500, "10W40", 4.0, 10000),
    "SIRIUS-1.8": f("ATM", E_, 1.8, B, 4, 6000, 4500, "10W40", 4.0, 10000),
    "SIRIUS-2.0": f("ATM", E_, 2.0, B, 4, 6000, 4500, "10W40", 4.0, 10000),
    "CYCLONE-3.0V6": f("ATM", E_, 3.0, B, 6, 5000, 4000, "10W40", 4.5, 10000, a="V"),
    # essence Hyundai
    "EPSILON-1.0": f("ATM", E_, 1.0, B, 4, 5500, 3000, "5W30", 3.3, 15000),
    "EPSILON-1.1": f("ATM", E_, 1.1, B, 4, 5500, 3000, "5W30", 3.3, 15000),
    "ALPHA-1.3": f("ATM", E_, 1.3, B, 4, 5500, 3000, "5W30", 3.3, 15000),
    "ALPHA-1.5": f("ATM", E_, 1.5, B, 4, 5800, 3000, "5W30", 3.3, 15000),
    "ALPHA-1.6": f("ATM", E_, 1.6, B, 4, 5800, 4500, "5W30", 3.3, 15000),
    "BETA-1.6": f("ATM", E_, 1.6, B, 4, 6000, 4500, "5W30", 4.0, 15000),
    "BETA-1.8": f("ATM", E_, 1.8, B, 4, 6000, 4500, "5W30", 4.0, 15000),
    "BETA-2.0": f("ATM", E_, 2.0, B, 4, 6000, 4500, "5W30", 4.0, 15000),
    "KAPPA-1.0": f("ATM", E_, 1.0, C, 3, 6000, 3500, "0W20", 3.2, 15000),
    "KAPPA-1.2": f("ATM", E_, 1.2, C, 4, 6000, 4000, "0W20", 3.6, 15000),
    "KAPPA-1.25": f("ATM", E_, 1.25, C, 4, 6000, 4000, "0W20", 3.6, 15000),
    "KAPPA-1.0T": f("TURBO", E_, 1.0, C, 3, 6000, 1500, "0W30", 3.6, 15000),
    "KAPPA-1.0T-MHEV": f("HYB_E", E_, 1.0, C, 3, 6000, 1500, "0W30", 3.6, 15000),
    "KAPPA-1.4T": f("TURBO", E_, 1.4, C, 4, 6000, 1500, "0W30", 4.2, 15000),
    "KAPPA-1.6-HEV": f("HYB_TE", E_, 1.6, C, 4, 5700, 4000, "0W20", 3.8, 15000),
    "KAPPA-1.6-PHEV": f("HYB_TE", E_, 1.6, C, 4, 5700, 4000, "0W20", 3.8, 15000),
    "GAMMA-1.4": f("ATM", E_, 1.4, C, 4, 6300, 4000, "5W30", 3.6, 15000),
    "GAMMA-1.6": f("ATM", E_, 1.6, C, 4, 6300, 4200, "5W30", 3.6, 15000),
    "GAMMA-1.6GDI": f("ATM", E_, 1.6, C, 4, 6300, 4850, "5W30", 3.6, 15000),
    "GAMMA-1.6T": f("TURBO", E_, 1.6, C, 4, 5500, 1500, "5W30", 4.5, 15000),
    "SMARTSTREAM-1.6T": f("TURBO", E_, 1.6, C, 4, 5500, 1500, "0W30", 4.5, 15000),
    "SMARTSTREAM-1.6T-MHEV": f("HYB_E", E_, 1.6, C, 4, 5500, 1500, "0W30", 4.5, 15000),
    "SMARTSTREAM-1.6T-HEV": f("HYB_TE", E_, 1.6, C, 4, 5500, 1500, "0W20", 4.5, 15000),
    "SMARTSTREAM-1.6T-PHEV": f("HYB_TE", E_, 1.6, C, 4, 5500, 1500, "0W20", 4.5, 15000),
    "SMARTSTREAM-1.5": f("ATM", E_, 1.5, C, 4, 6300, 4500, "0W20", 3.8, 15000),
    "SMARTSTREAM-1.5T-MHEV": f("HYB_E", E_, 1.5, C, 4, 5500, 1500, "0W30", 4.2, 15000),
    "THETA-2.0": f("ATM", E_, 2.0, C, 4, 6000, 4500, "5W30", 4.5, 15000),
    "THETA-2.4": f("ATM", E_, 2.4, C, 4, 6000, 4250, "5W30", 4.5, 15000),
    "THETA-2.4GDI": f("ATM", E_, 2.4, C, 4, 6000, 4000, "5W30", 4.8, 15000),
    "THETA-2.0T": f("TURBO", E_, 2.0, C, 4, 6000, 1450, "5W30", 4.8, 15000),
    "NU-2.0": f("ATM", E_, 2.0, C, 4, 6500, 4700, "5W30", 4.0, 15000),
    "NU-2.0GDI": f("ATM", E_, 2.0, C, 4, 6500, 4700, "5W30", 4.0, 15000),
    "DELTA-2.5V6": f("ATM", E_, 2.5, B, 6, 6000, 4000, "5W30", 4.5, 15000, a="V"),
    "DELTA-2.7V6": f("ATM", E_, 2.7, B, 6, 6000, 4000, "5W30", 4.5, 15000, a="V"),
    "LAMBDA-3.3V6": f("ATM", E_, 3.3, C, 6, 6000, 3500, "5W30", 5.7, 15000, a="V"),
    "LAMBDA-3.5V6": f("ATM", E_, 3.5, C, 6, 6400, 5000, "0W20", 5.7, 15000, a="V"),
    "LAMBDA-3.8V6": f("ATM", E_, 3.8, C, 6, 6000, 5200, "5W30", 5.7, 15000, a="V"),
    "SMARTSTREAM-2.5T-HEV": f("HYB_TE", E_, 2.5, C, 4, 5800, 1700, "0W20", 5.0, 15000),
    # diesel
    "U-1.1CRDi": f("TURBO", D, 1.1, C, 3, 4000, 1750, "5W30", 4.8, 15000),
    "U-1.4CRDi": f("TURBO", D, 1.4, C, 4, 4000, 1750, "5W30", 5.3, 15000),
    "U-1.5CRDi": f("TURBO", D, 1.5, C, 4, 4000, 1900, "5W30", 5.3, 15000),
    "U-1.6CRDi": f("TURBO", D, 1.6, C, 4, 4000, 1900, "5W30", 5.3, 15000),
    "U-1.7CRDi": f("TURBO", D, 1.7, C, 4, 4000, 2000, "5W30", 5.3, 15000),
    "U3-1.6CRDi": f("TURBO", D, 1.6, C, 4, 4000, 1750, "0W30", 5.3, 15000),
    "U3-1.6CRDi-MHEV": f("HYB_E", D, 1.6, C, 4, 4000, 1750, "0W30", 5.3, 15000),
    "D-2.0CRDi": f("TURBO", D, 2.0, B, 4, 4000, 1800, "5W30", 5.9, 15000),
    "R-2.0CRDi": f("TURBO", D, 2.0, C, 4, 4000, 1800, "5W30", 6.4, 15000),
    "R-2.0CRDi-MHEV": f("HYB_E", D, 2.0, C, 4, 4000, 1750, "0W30", 6.4, 15000),
    "R-2.2CRDi": f("TURBO", D, 2.2, C, 4, 3800, 1800, "5W30", 6.4, 15000),
    # électrique / hydrogène
    "HYUNDAI-EV": electrique(),
    "HYUNDAI-FCEV": f("ELEC", "H2", 0.0, "AUCUNE", 0, 0, 0, "CHOISIR", 0.0, 30000, a="SANS"),
}


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


NA = "Marché nord-américain (hp convertis en ch)"
mg = SaisieMoteurs(FAMILLES, "Hyundai")
L = []

# ---------------------------------------------------------------- petites
mg(L, "Pony", "X2", "1", "1985-01", "1990-12", [("1.3 67", "ORION-1.3", 103), ("1.5 72", "ORION-1.5", 118)], reservoir=40,
   remarques="Moteurs Mitsubishi sous licence ; données indicatives")
mg(L, "Accent", "X3", "1", "1994-09", "1999-12", [("1.3 75", "ALPHA-1.3", 110), ("1.5 90", "ALPHA-1.5", 128)], reservoir=45,
   remarques="3 et 5 portes, berline")
mg(L, "Accent", "LC", "1", "2000-01", "2005-12",
   [("1.3 75", "ALPHA-1.3", 116), ("1.3 86", "ALPHA-1.3", 119, {"debut": "2003-01"}), ("1.5 90", "ALPHA-1.5", 133),
    ("1.6 105", "ALPHA-1.6", 143, {"debut": "2003-01"}), ("1.5 CRDi 82", "U-1.5CRDi", 187, {"debut": "2003-01"})], reservoir=45)
mg(L, "Accent", "MC", "1", "2006-01", "2010-12",
   [("1.4 97", "GAMMA-1.4", 125), ("1.6 112", "GAMMA-1.6", 145), ("1.5 CRDi 110", "U-1.5CRDi", 235)], reservoir=45,
   remarques="Remplacée en Europe par l'i20")
mg(L, "Atos", "MX", "1", "1997-12", "2008-12",
   [("1.0 54", "EPSILON-1.0", 82, {"fin": "2003-12"}), ("1.0 58", "EPSILON-1.0", 84, {"debut": "2004-01"}), ("1.1 63", "EPSILON-1.1", 96, {"debut": "2003-06"})],
   reservoir=35, remarques="Atos puis Atos Prime (1999)")
mg(L, "Getz", "TB", "1", "2002-09", "2005-08",
   [("1.1 63", "EPSILON-1.1", 96), ("1.3 82", "ALPHA-1.3", 119), ("1.6 105", "ALPHA-1.6", 143), ("1.5 CRDi 82", "U-1.5CRDi", 187)],
   reservoir=45)
mg(L, "Getz", "TB", "2", "2005-09", "2009-12",
   [("1.1 66", "EPSILON-1.1", 99), ("1.4 97", "GAMMA-1.4", 125), ("1.6 106", "GAMMA-1.6", 145), ("1.5 CRDi 88", "U-1.5CRDi", 215),
    ("1.5 CRDi 110", "U-1.5CRDi", 235)], reservoir=45, remarques="Restylage ; diesel 3 cylindres")
mg(L, "i10", "PA", "1", "2008-01", "2011-02",
   [("1.1 66", "EPSILON-1.1", 99), ("1.2 78", "KAPPA-1.2", 119, {"debut": "2008-10"}), ("1.1 CRDi 75", "U-1.1CRDi", 154)], reservoir=35)
mg(L, "i10", "PA", "2", "2011-03", "2013-10", [("1.1 69", "EPSILON-1.1", 99), ("1.2 86", "KAPPA-1.2", 121)], reservoir=35, remarques="Restylage")
mg(L, "i10", "IA", "1", "2013-11", "2016-11", [("1.0 66", "KAPPA-1.0", 95), ("1.2 87", "KAPPA-1.25", 120)], reservoir=40)
mg(L, "i10", "IA", "2", "2016-12", "2019-12", [("1.0 66", "KAPPA-1.0", 95), ("1.2 87", "KAPPA-1.25", 120)], reservoir=40, remarques="Restylage")
mg(L, "i10", "AC3", "1", "2020-01", "2023-05",
   [("1.0 MPi 67", "KAPPA-1.0", 96), ("1.2 MPi 84", "KAPPA-1.2", 118), ("N Line 1.0 T-GDi 100", "KAPPA-1.0T", 172, {"debut": "2020-05"})],
   reservoir=36)
mg(L, "i10", "AC3", "2", "2023-06", None, [("1.0 MPi 63", "KAPPA-1.0", 93), ("1.2 MPi 79", "KAPPA-1.2", 114)], reservoir=36, remarques="Restylage")
mg(L, "i20", "PB", "1", "2008-09", "2012-02",
   [("1.2 78", "KAPPA-1.2", 119), ("1.4 100", "GAMMA-1.4", 137), ("1.6 126", "GAMMA-1.6", 156), ("1.4 CRDi 90", "U-1.4CRDi", 220),
    ("1.6 CRDi 115", "U-1.6CRDi", 255), ("1.6 CRDi 128", "U-1.6CRDi", 260)], reservoir=45)
mg(L, "i20", "PB", "2", "2012-03", "2014-10",
   [("1.2 85", "KAPPA-1.2", 121), ("1.4 100", "GAMMA-1.4", 137), ("1.1 CRDi 75", "U-1.1CRDi", 180), ("1.4 CRDi 90", "U-1.4CRDi", 220)],
   reservoir=45, remarques="Restylage")
mg(L, "i20", "GB", "1", "2014-11", "2018-07",
   [("1.25 75", "KAPPA-1.25", 122), ("1.25 84", "KAPPA-1.25", 122), ("1.4 100", "GAMMA-1.4", 134),
    ("1.0 T-GDi 100", "KAPPA-1.0T", 172, {"debut": "2015-10"}), ("1.0 T-GDi 120", "KAPPA-1.0T", 172, {"debut": "2015-10"}),
    ("1.1 CRDi 75", "U-1.1CRDi", 180), ("1.4 CRDi 90", "U-1.4CRDi", 240)], reservoir=50, remarques="5 portes, Coupé 3 portes, Active")
mg(L, "i20", "GB", "2", "2018-08", "2020-09",
   [("1.25 75", "KAPPA-1.25", 122), ("1.25 84", "KAPPA-1.25", 122), ("1.0 T-GDi 100", "KAPPA-1.0T", 172), ("1.0 T-GDi 120", "KAPPA-1.0T", 172)],
   reservoir=50, remarques="Restylage ; diesel abandonné")
mg(L, "i20", "BC3", "1", "2020-10", "2023-08",
   [("1.2 MPi 84", "KAPPA-1.2", 118), ("1.0 T-GDi 100", "KAPPA-1.0T", 172), ("1.0 T-GDi 48V 100", "KAPPA-1.0T-MHEV", 172),
    ("1.0 T-GDi 48V 120", "KAPPA-1.0T-MHEV", 200)], reservoir=40)
mg(L, "i20", "BC3", "2", "2023-09", None,
   [("1.2 MPi 79", "KAPPA-1.2", 115), ("1.0 T-GDi 90", "KAPPA-1.0T", 172), ("1.0 T-GDi 100", "KAPPA-1.0T", 172)], reservoir=40,
   remarques="Restylage")
mg(L, "Bayon", "BC3 CUV", "1", "2021-05", "2024-05",
   [("1.2 MPi 84", "KAPPA-1.2", 118), ("1.0 T-GDi 100", "KAPPA-1.0T", 172), ("1.0 T-GDi 48V 100", "KAPPA-1.0T-MHEV", 172),
    ("1.0 T-GDi 48V 120", "KAPPA-1.0T-MHEV", 200)], reservoir=40)
mg(L, "Bayon", "BC3 CUV", "2", "2024-06", None,
   [("1.2 MPi 79", "KAPPA-1.2", 115), ("1.0 T-GDi 90", "KAPPA-1.0T", 172), ("1.0 T-GDi 100", "KAPPA-1.0T", 172)], reservoir=40,
   remarques="Restylage")
mg(L, "Inster", "AX1", "1", "2024-11", None, [("Standard Range 97", "HYUNDAI-EV", 147, el(42)), ("Long Range 115", "HYUNDAI-EV", 147, el(49))],
   reservoir=0, remarques="Citadine électrique ; Inster Cross (2025)")

# ---------------------------------------------------------------- compactes
mg(L, "Lantra", "J1", "1", "1991-01", "1995-09", [("1.6 114", "SIRIUS-1.6", 140), ("1.8 126", "SIRIUS-1.8", 159)], portes=4, reservoir=55,
   remarques="Moteurs Mitsubishi sous licence")
mg(L, "Lantra", "J2", "1", "1995-10", "2000-06",
   [("1.6 114", "BETA-1.6", 146), ("1.8 128", "BETA-1.8", 164), ("2.0 139", "BETA-2.0", 184, {"debut": "1998-06"})], portes=4, reservoir=55,
   remarques="Berline et break")
mg(L, "Elantra", "XD", "1", "2000-06", "2006-12",
   [("1.6 107", "BETA-1.6", 143), ("1.8 132", "BETA-1.8", 166), ("2.0 143", "BETA-2.0", 186), ("2.0 CRDi 113", "D-2.0CRDi", 235, {"debut": "2001-06"})],
   portes=4, reservoir=55, remarques="Berline et 5 portes ; restylage 2003")
mg(L, "Elantra", "MD", "1", "2011-01", "2015-12", [("1.6 132", "GAMMA-1.6", 158)], portes=4, reservoir=50,
   remarques="Commercialisée dans quelques marchés européens seulement")
mg(L, "Elantra", "AD", "1", "2016-01", "2020-12", [("1.6 128", "GAMMA-1.6", 155)], portes=4, reservoir=50,
   remarques="Commercialisée dans quelques marchés européens seulement")
mg(L, "i30", "FD", "1", "2007-06", "2010-01",
   [("1.4 109", "GAMMA-1.4", 137), ("1.6 122", "GAMMA-1.6", 154), ("2.0 143", "BETA-2.0", 186), ("1.6 CRDi 90", "U-1.6CRDi", 235),
    ("1.6 CRDi 115", "U-1.6CRDi", 255), ("2.0 CRDi 140", "D-2.0CRDi", 305)], reservoir=53, remarques="5 portes, break CW (2008)")
mg(L, "i30", "FD", "2", "2010-02", "2012-02",
   [("1.4 109", "GAMMA-1.4", 137), ("1.6 126", "GAMMA-1.6", 156), ("1.6 CRDi 90", "U-1.6CRDi", 235), ("1.6 CRDi 128", "U-1.6CRDi", 260)],
   reservoir=53, remarques="Restylage")
mg(L, "i30", "GD", "1", "2012-02", "2015-02",
   [("1.4 100", "GAMMA-1.4", 134), ("1.6 GDI 135", "GAMMA-1.6GDI", 164), ("1.4 CRDi 90", "U-1.4CRDi", 220), ("1.6 CRDi 110", "U-1.6CRDi", 260),
    ("1.6 CRDi 128", "U-1.6CRDi", 260)], reservoir=53, remarques="5 portes, 3 portes, break")
mg(L, "i30", "GD", "2", "2015-03", "2016-12",
   [("1.4 100", "GAMMA-1.4", 134), ("1.6 GDI 120", "GAMMA-1.6GDI", 156), ("1.6 GDI 135", "GAMMA-1.6GDI", 164),
    ("Turbo 1.6 T-GDi 186", "GAMMA-1.6T", 265), ("1.6 CRDi 110", "U-1.6CRDi", 280), ("1.6 CRDi 136", "U-1.6CRDi", 300)],
   reservoir=53, remarques="Restylage")
mg(L, "i30", "PD", "1", "2017-01", "2020-08",
   [("1.4 MPi 100", "GAMMA-1.4", 134), ("1.0 T-GDi 120", "KAPPA-1.0T", 172), ("1.4 T-GDi 140", "KAPPA-1.4T", 242),
    ("1.6 CRDi 95", "U3-1.6CRDi", 280), ("1.6 CRDi 110", "U3-1.6CRDi", 280), ("1.6 CRDi 136", "U3-1.6CRDi", 300)], reservoir=50,
   remarques="5 portes, break SW, Fastback (2018)")
mg(L, "i30", "PD", "2", "2020-09", "2024-01",
   [("1.0 T-GDi 120", "KAPPA-1.0T", 172), ("1.0 T-GDi 48V 120", "KAPPA-1.0T-MHEV", 200), ("1.5 DPi 110", "SMARTSTREAM-1.5", 144),
    ("1.5 T-GDi 48V 160", "SMARTSTREAM-1.5T-MHEV", 253), ("1.6 CRDi 48V 136", "U3-1.6CRDi-MHEV", 280)], reservoir=50,
   remarques="Restylage ; Fastback arrêtée en 2023")
mg(L, "i30", "PD", "3", "2024-02", None,
   [("1.0 T-GDi 48V 100", "KAPPA-1.0T-MHEV", 172), ("1.0 T-GDi 48V 120", "KAPPA-1.0T-MHEV", 200), ("1.5 T-GDi 48V 140", "SMARTSTREAM-1.5T-MHEV", 253)],
   reservoir=50, remarques="Second restylage ; 5 portes et break, deux moteurs essence en 2026")
mg(L, "ix20", "JC", "1", "2010-11", "2019-07",
   [("1.4 90", "GAMMA-1.4", 137), ("1.6 125", "GAMMA-1.6", 156), ("1.4 CRDi 77", "U-1.4CRDi", 220), ("1.4 CRDi 90", "U-1.4CRDi", 220)],
   reservoir=48, remarques="Monospace compact ; restylage 2015")
mg(L, "Matrix", "FC", "1", "2001-06", "2010-06",
   [("1.6 103", "ALPHA-1.6", 143), ("1.8 122", "BETA-1.8", 162), ("1.5 CRDi 82", "U-1.5CRDi", 187), ("1.5 CRDi 102", "U-1.5CRDi", 235, {"debut": "2005-06"})],
   reservoir=55, remarques="Monospace compact ; restylages 2005 et 2008")
mg(L, "Coupé", "RD", "1", "1996-06", "2001-12", [("1.6 114", "BETA-1.6", 146), ("2.0 139", "BETA-2.0", 182)], portes=3, places=4, reservoir=55,
   remarques="Restylage RD2 (1999)")
mg(L, "Coupé", "GK", "1", "2002-01", "2009-06",
   [("1.6 105", "ALPHA-1.6", 143), ("2.0 143", "BETA-2.0", 186), ("2.7 V6 167", "DELTA-2.7V6", 245)], portes=3, places=4, reservoir=55,
   remarques="Restylages 2005 et 2007")
mg(L, "Veloster", "FS", "1", "2011-06", "2015-12", [("1.6 GDI 140", "GAMMA-1.6GDI", 167), ("Turbo 1.6 T-GDi 186", "GAMMA-1.6T", 265, {"debut": "2012-10"})],
   portes=4, places=4, reservoir=50, remarques="Coupé à porte arrière droite supplémentaire")
mg(L, "Ioniq", "AE", "1", "2016-10", "2019-07",
   [("Hybrid 141", "KAPPA-1.6-HEV", 265), ("Plug-in 141", "KAPPA-1.6-PHEV", 265, {"debut": "2017-06", "batterie": 9}),
    ("Electric 120", "HYUNDAI-EV", 295, el(28))], reservoir=45, remarques="Hybride, hybride rechargeable et électrique")
mg(L, "Ioniq", "AE", "2", "2019-08", "2022-07",
   [("Hybrid 141", "KAPPA-1.6-HEV", 265), ("Plug-in 141", "KAPPA-1.6-PHEV", 265, {"batterie": 9}), ("Electric 136", "HYUNDAI-EV", 295, el(38))],
   reservoir=45, remarques="Restylage ; production arrêtée en juillet 2022")
mg(L, "Ioniq 3", "SX3", "1", "2026-09", None, [("Long Range 135", "HYUNDAI-EV", 250, el(61)), ("Standard Range 147", "HYUNDAI-EV", 250, el(42))],
   reservoir=0, remarques="Compacte électrique E-GMP 400 V produite à Izmit ; date de commercialisation indicative")

# ---------------------------------------------------------------- SUV
mg(L, "Kona", "OS", "1", "2017-10", "2020-10",
   [("1.0 T-GDi 120", "KAPPA-1.0T", 172), ("1.6 T-GDi 177", "GAMMA-1.6T", 265), ("1.6 CRDi 115", "U3-1.6CRDi", 280, {"debut": "2018-06"}),
    ("1.6 CRDi 136", "U3-1.6CRDi", 320, {"debut": "2018-06"}), ("Hybrid 141", "KAPPA-1.6-HEV", 265, {"debut": "2019-08"}),
    ("Electric 136", "HYUNDAI-EV", 395, el(39, debut="2018-07")), ("Electric 204", "HYUNDAI-EV", 395, el(64, debut="2018-07"))], reservoir=50)
mg(L, "Kona", "OS", "2", "2020-11", "2023-02",
   [("1.0 T-GDi 120", "KAPPA-1.0T", 172), ("1.0 T-GDi 48V 120", "KAPPA-1.0T-MHEV", 200), ("1.6 T-GDi 198", "SMARTSTREAM-1.6T", 265),
    ("1.6 CRDi 48V 136", "U3-1.6CRDi-MHEV", 280), ("Hybrid 141", "KAPPA-1.6-HEV", 265), ("Electric 136", "HYUNDAI-EV", 395, el(39)),
    ("Electric 204", "HYUNDAI-EV", 395, el(64))], reservoir=50, remarques="Restylage")
mg(L, "Kona", "SX2", "1", "2023-03", None,
   [("1.0 T-GDi 120", "KAPPA-1.0T", 200), ("1.6 T-GDi 198", "SMARTSTREAM-1.6T", 265), ("Hybrid 141", "KAPPA-1.6-HEV", 265),
    ("Electric 156", "HYUNDAI-EV", 255, el(48)), ("Electric 218", "HYUNDAI-EV", 255, el(65))], reservoir=47,
   remarques="Deuxième génération ; Electric à batterie 48,4 ou 65,4 kWh")
mg(L, "Tucson", "JM", "1", "2004-08", "2010-02",
   [("2.0 141", "BETA-2.0", 184), ("2.7 V6 175", "DELTA-2.7V6", 241), ("2.0 CRDi 113", "D-2.0CRDi", 245), ("2.0 CRDi 140", "D-2.0CRDi", 305, {"debut": "2006-01"}),
    ("2.0 CRDi 150", "D-2.0CRDi", 305, {"debut": "2008-06"})], reservoir=58)
mg(L, "ix35", "LM", "1", "2010-03", "2013-06",
   [("1.6 GDI 135", "GAMMA-1.6GDI", 164, {"debut": "2011-06"}), ("2.0 163", "THETA-2.0", 197), ("1.7 CRDi 116", "U-1.7CRDi", 260, {"debut": "2010-10"}),
    ("2.0 CRDi 136", "R-2.0CRDi", 320), ("2.0 CRDi 184", "R-2.0CRDi", 383)], reservoir=58, remarques="Remplace le Tucson en Europe")
mg(L, "ix35", "LM", "2", "2013-07", "2015-08",
   [("1.6 GDI 135", "GAMMA-1.6GDI", 164), ("2.0 GDI 166", "NU-2.0GDI", 205), ("1.7 CRDi 116", "U-1.7CRDi", 260), ("2.0 CRDi 136", "R-2.0CRDi", 373),
    ("2.0 CRDi 184", "R-2.0CRDi", 383)], reservoir=58, remarques="Restylage")
mg(L, "Tucson", "TL", "1", "2015-07", "2018-06",
   [("1.6 GDI 132", "GAMMA-1.6GDI", 161), ("1.6 T-GDi 177", "GAMMA-1.6T", 265), ("1.7 CRDi 116", "U-1.7CRDi", 280),
    ("1.7 CRDi 141", "U-1.7CRDi", 340, {"debut": "2016-01"}), ("2.0 CRDi 136", "R-2.0CRDi", 373), ("2.0 CRDi 185", "R-2.0CRDi", 400)], reservoir=62)
mg(L, "Tucson", "TL", "2", "2018-07", "2020-08",
   [("1.6 GDI 132", "GAMMA-1.6GDI", 161), ("1.6 T-GDi 177", "GAMMA-1.6T", 265), ("1.6 CRDi 115", "U3-1.6CRDi", 280),
    ("1.6 CRDi 136", "U3-1.6CRDi", 320), ("2.0 CRDi 48V 185", "R-2.0CRDi-MHEV", 400)], reservoir=62, remarques="Restylage")
mg(L, "Tucson", "NX4", "1", "2020-09", "2024-02",
   [("1.6 T-GDi 150", "SMARTSTREAM-1.6T", 250), ("1.6 T-GDi 48V 150", "SMARTSTREAM-1.6T-MHEV", 250), ("1.6 T-GDi 48V 4x4 180", "SMARTSTREAM-1.6T-MHEV", 265),
    ("1.6 CRDi 115", "U3-1.6CRDi", 280), ("1.6 CRDi 48V 136", "U3-1.6CRDi-MHEV", 320), ("Hybrid 230", "SMARTSTREAM-1.6T-HEV", 350),
    ("Plug-in 4x4 265", "SMARTSTREAM-1.6T-PHEV", 350, {"debut": "2021-06", "batterie": 14})], reservoir=54)
mg(L, "Tucson", "NX4", "2", "2024-03", None,
   [("1.6 T-GDi 160", "SMARTSTREAM-1.6T", 250), ("1.6 T-GDi 48V 160", "SMARTSTREAM-1.6T-MHEV", 250), ("1.6 CRDi 48V 136", "U3-1.6CRDi-MHEV", 320),
    ("Hybrid 215", "SMARTSTREAM-1.6T-HEV", 367), ("Plug-in 4x4 252", "SMARTSTREAM-1.6T-PHEV", 367, {"batterie": 14})], reservoir=54,
   remarques="Restylage ; 5e génération en développement")
mg(L, "Santa Fe", "SM", "1", "2000-10", "2006-02",
   [("2.0 136", "BETA-2.0", 179), ("2.4 146", "THETA-2.4", 196, {"debut": "2004-01"}), ("2.7 V6 173", "DELTA-2.7V6", 245),
    ("2.0 CRDi 113", "D-2.0CRDi", 255), ("2.0 CRDi 125", "D-2.0CRDi", 285, {"debut": "2004-06"})], reservoir=65)
mg(L, "Santa Fe", "CM", "1", "2006-03", "2012-08",
   [("2.7 V6 189", "DELTA-2.7V6", 248), ("2.4 174", "THETA-2.4", 227, {"debut": "2010-01"}), ("2.2 CRDi 150", "D-2.0CRDi", 335, {"fin": "2009-12"}),
    ("2.2 CRDi 197", "R-2.2CRDi", 421, {"debut": "2010-01"})], places=7, reservoir=75, remarques="5 ou 7 places ; restylage 2010")
mg(L, "Santa Fe", "DM", "1", "2012-09", "2018-06",
   [("2.4 GDI 192", "THETA-2.4GDI", 241), ("2.0 CRDi 150", "R-2.0CRDi", 383), ("2.2 CRDi 197", "R-2.2CRDi", 436), ("2.2 CRDi 200", "R-2.2CRDi", 440, {"debut": "2015-06"})],
   places=7, reservoir=64, remarques="Grand Santa Fe 7 places (2013) ; restylage 2015")
mg(L, "Santa Fe", "TM", "1", "2018-08", "2020-10",
   [("2.4 GDI 185", "THETA-2.4GDI", 241), ("2.0 CRDi 150", "R-2.0CRDi", 400), ("2.2 CRDi 200", "R-2.2CRDi", 440)], places=7, reservoir=71)
mg(L, "Santa Fe", "TM", "2", "2020-11", "2023-12",
   [("2.2 CRDi 202", "R-2.2CRDi", 440), ("Hybrid 230", "SMARTSTREAM-1.6T-HEV", 350), ("Plug-in 4x4 265", "SMARTSTREAM-1.6T-PHEV", 350, {"batterie": 14})],
   places=7, reservoir=67, remarques="Restylage, nouvelle plateforme")
mg(L, "Santa Fe", "MX5", "1", "2024-03", None,
   [("Hybrid 215", "SMARTSTREAM-1.6T-HEV", 367), ("Hybrid 4x4 215", "SMARTSTREAM-1.6T-HEV", 367), ("Plug-in 4x4 253", "SMARTSTREAM-1.6T-PHEV", 367, {"batterie": 14})],
   places=7, reservoir=67, remarques="Cinquième génération ; restylage annoncé pour 2027")
mg(L, "Palisade", "LX2", "1", "2018-12", "2025-03", [("3.8 V6 295", "LAMBDA-3.8V6", 355)], places=8, reservoir=71, remarques=NA + " ; restylage 2022")
mg(L, "Palisade", "LX3", "1", "2025-04", None, [("3.5 V6 291", "LAMBDA-3.5V6", 353), ("2.5 Turbo Hybrid 334", "SMARTSTREAM-2.5T-HEV", 460)],
   places=8, reservoir=72, remarques=NA)
mg(L, "Nexo", "FE", "1", "2018-08", "2025-03", [("Fuel Cell 163", "HYUNDAI-FCEV", 395)], reservoir=0, remarques="Pile à combustible, réservoirs 6,3 kg d'hydrogène")
mg(L, "Nexo", "NH2", "1", "2025-04", None, [("Fuel Cell 204", "HYUNDAI-FCEV", 350)], reservoir=0, remarques="Pile à combustible, 6,69 kg d'hydrogène")
mg(L, "ix35 Fuel Cell", "LM FCEV", "1", "2013-03", "2018-06", [("Fuel Cell 136", "HYUNDAI-FCEV", 300)], reservoir=0, remarques="Pile à combustible")
mg(L, "Ioniq 5", "NE", "1", "2021-05", "2024-03",
   [("Standard Range 170", "HYUNDAI-EV", 350, el(58)), ("Long Range 218", "HYUNDAI-EV", 350, el(73, fin="2022-12")),
    ("Long Range AWD 306", "HYUNDAI-EV", 605, el(73, fin="2022-12")), ("Long Range 229", "HYUNDAI-EV", 350, el(77, debut="2023-01")),
    ("Long Range AWD 325", "HYUNDAI-EV", 605, el(77, debut="2023-01"))], reservoir=0)
mg(L, "Ioniq 5", "NE", "2", "2024-04", None,
   [("Standard Range 170", "HYUNDAI-EV", 350, el(63)), ("Long Range 229", "HYUNDAI-EV", 350, el(84)), ("Long Range AWD 325", "HYUNDAI-EV", 605, el(84))],
   reservoir=0, remarques="Restylage ; N Line")
mg(L, "Ioniq 6", "CE", "1", "2022-09", "2025-12",
   [("Standard Range 151", "HYUNDAI-EV", 350, el(53)), ("Long Range 229", "HYUNDAI-EV", 350, el(77)), ("Long Range AWD 325", "HYUNDAI-EV", 605, el(77))],
   portes=4, reservoir=0)
mg(L, "Ioniq 6", "CE", "2", "2026-01", None,
   [("Standard Range 170", "HYUNDAI-EV", 350, el(63)), ("Long Range 229", "HYUNDAI-EV", 350, el(84)), ("Long Range AWD 325", "HYUNDAI-EV", 605, el(84))],
   portes=4, reservoir=0, remarques="Restylage, N Line ; date indicative")
mg(L, "Ioniq 9", "ME", "1", "2025-02", None,
   [("Long Range 218", "HYUNDAI-EV", 350, el(110)), ("Long Range AWD 308", "HYUNDAI-EV", 605, el(110)), ("Performance AWD 435", "HYUNDAI-EV", 700, el(110))],
   places=7, reservoir=0, remarques="Grand SUV électrique 6 ou 7 places")

# ---------------------------------------------------------------- berlines et monospaces
mg(L, "Sonata", "Y3", "1", "1993-06", "1998-12", [("2.0 139", "SIRIUS-2.0", 178), ("3.0 V6 146", "CYCLONE-3.0V6", 236)], portes=4, reservoir=65,
   remarques="Moteurs Mitsubishi ; données indicatives")
mg(L, "Sonata", "EF", "1", "1998-12", "2004-12",
   [("2.0 136", "BETA-2.0", 182), ("2.4 146", "THETA-2.4", 211, {"debut": "2001-06"}), ("2.5 V6 170", "DELTA-2.5V6", 230), ("2.7 V6 173", "DELTA-2.7V6", 245, {"debut": "2001-06"})],
   portes=4, reservoir=65, remarques="Restylage 2001")
mg(L, "Sonata", "NF", "1", "2005-01", "2010-12",
   [("2.4 161", "THETA-2.4", 219), ("3.3 V6 233", "LAMBDA-3.3V6", 304), ("2.0 CRDi 140", "D-2.0CRDi", 305, {"debut": "2006-06"}),
    ("2.0 CRDi 150", "R-2.0CRDi", 320, {"debut": "2009-01"})], portes=4, reservoir=70, remarques="Restylage 2008 ; remplacée par l'i40")
mg(L, "i40", "VF", "1", "2011-06", "2015-06",
   [("1.6 GDI 135", "GAMMA-1.6GDI", 164), ("2.0 GDI 177", "NU-2.0GDI", 213), ("1.7 CRDi 115", "U-1.7CRDi", 260), ("1.7 CRDi 136", "U-1.7CRDi", 325)],
   reservoir=70, remarques="Break SW et berline (2012)")
mg(L, "i40", "VF", "2", "2015-07", "2019-08",
   [("1.6 GDI 135", "GAMMA-1.6GDI", 164), ("2.0 GDI 165", "NU-2.0GDI", 201), ("1.7 CRDi 115", "U-1.7CRDi", 280, {"fin": "2018-08"}),
    ("1.7 CRDi 141", "U-1.7CRDi", 340, {"fin": "2018-08"}), ("1.6 CRDi 48V 136", "U3-1.6CRDi-MHEV", 320, {"debut": "2018-09"})],
   reservoir=70, remarques="Restylage")
mg(L, "Trajet", "FO", "1", "2000-06", "2008-06",
   [("2.0 136", "BETA-2.0", 179), ("2.7 V6 173", "DELTA-2.7V6", 245), ("2.0 CRDi 113", "D-2.0CRDi", 255), ("2.0 CRDi 140", "D-2.0CRDi", 305, {"debut": "2005-01"})],
   places=7, reservoir=65, remarques="Monospace 7 places ; restylage 2004")
mg(L, "Staria", "US4", "1", "2021-06", None,
   [("2.2 CRDi 177", "R-2.2CRDi", 431), ("1.6 T-GDi Hybrid 245", "SMARTSTREAM-1.6T-HEV", 367, {"debut": "2025-01"}),
    ("Electric 218", "HYUNDAI-EV", 350, el(84, debut="2026-01"))], places=9, reservoir=75, remarques="Monospace 7 à 9 places ; Staria Electric (2026)")

# ---------------------------------------------------------------- Hyundai N
LN = []
mg(LN, "i20 N", "BC3 N", "1", "2021-01", "2024-03", [("1.6 T-GDi 204", "SMARTSTREAM-1.6T", 275)], portes=5, reservoir=40,
   remarques="Production arrêtée début 2024 en Europe")
mg(LN, "i30 N", "PDe N", "1", "2017-09", "2020-10", [("2.0 T-GDi 250", "THETA-2.0T", 353), ("Performance 2.0 T-GDi 275", "THETA-2.0T", 353)],
   reservoir=50, remarques="5 portes, Fastback N (2019)")
mg(LN, "i30 N", "PDe N", "2", "2020-11", None, [("2.0 T-GDi 280", "THETA-2.0T", 392)], reservoir=50,
   remarques="Restylage, boîte DCT 8 disponible ; Fastback N arrêtée en 2023")
mg(LN, "Kona N", "OS N", "1", "2021-09", "2023-03", [("2.0 T-GDi 280", "THETA-2.0T", 392)], reservoir=50)
mg(LN, "Veloster N", "JS N", "1", "2018-06", "2022-06",
   [("2.0 T-GDi 254", "THETA-2.0T", 353), ("Performance 2.0 T-GDi 279", "THETA-2.0T", 353)], portes=4, places=4, reservoir=50, remarques=NA)
mg(LN, "Elantra N", "CN7 N", "1", "2021-07", "2023-08", [("2.0 T-GDi 280", "THETA-2.0T", 392)], portes=4, reservoir=47, remarques=NA)
mg(LN, "Elantra N", "CN7 N", "2", "2023-09", None, [("2.0 T-GDi 280", "THETA-2.0T", 392)], portes=4, reservoir=47, remarques=NA + " ; restylage")
mg(LN, "Ioniq 5 N", "NE N", "1", "2024-03", None, [("AWD 609", "HYUNDAI-EV", 740, el(84))], reservoir=0,
   remarques="650 ch et 770 Nm en mode N Grin Boost")
mg(LN, "Ioniq 6 N", "CE N", "1", "2026-03", None, [("AWD 609", "HYUNDAI-EV", 740, el(84))], portes=4, reservoir=0,
   remarques="650 ch et 770 Nm en mode N Grin Boost ; commandes ouvertes en mars 2026")

MOT = Motorisations("Hyundai", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LN)

DETAIL = {"Hyundai": L, "Hyundai N": LN}
MOTEURS = MOT.moteurs()
