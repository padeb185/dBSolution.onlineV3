"""Honda, Honda Type R et Honda S2000 : générations, phases, motorisations (marché européen) et moteurs liés.
Honda : Civic, Accord, Jazz, HR-V, CR-V, ZR-V, Insight, CR-Z, FR-V, Stream, CRX, Prelude, NSX, Honda e, e:Ny1.
Honda Type R : Civic Type R (EP3, FN2, FK2, FK8, FL5) et Integra Type R (DC2). Honda S2000 : AP1 et AP2.
Modèles nord-américains (Pilot, Passport, Odyssey US) et Acura non repris ; versions antérieures à 1990 non reprises.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


FAMILLES = {
    # --- essence courroie (années 90)
    "D13": f("ATM", E_, 1.3, B, 4, 6300, 4800, "10W40", 3.5, 10000),
    "D14": f("ATM", E_, 1.4, B, 4, 6300, 4800, "10W40", 3.5, 10000),
    "D15": f("ATM", E_, 1.5, B, 4, 6000, 4500, "10W40", 3.5, 10000),
    "D16": f("ATM", E_, 1.6, B, 4, 6500, 5000, "10W40", 3.5, 10000),
    "D17": f("ATM", E_, 1.7, B, 4, 6100, 4800, "5W30", 3.5, 20000),
    "B16A": f("ATM", E_, 1.6, B, 4, 7600, 7000, "10W40", 4.0, 10000),
    "B18C": f("ATM", E_, 1.8, B, 4, 8000, 7300, "10W40", 4.0, 10000),
    "B20B": f("ATM", E_, 2.0, B, 4, 5400, 4300, "10W40", 4.0, 10000),
    "F18": f("ATM", E_, 1.8, B, 4, 6100, 5000, "10W40", 4.0, 10000),
    "F20": f("ATM", E_, 2.0, B, 4, 6000, 4800, "10W40", 4.0, 10000),
    "F23": f("ATM", E_, 2.3, B, 4, 5800, 4800, "10W40", 4.0, 10000),
    "H22": f("ATM", E_, 2.2, B, 4, 7000, 5500, "10W40", 4.5, 10000),
    "C30": f("ATM", E_, 3.0, B, 6, 7300, 5400, "10W40", 5.0, 10000, a="V"),
    "C32": f("ATM", E_, 3.2, B, 6, 7300, 5300, "10W40", 5.0, 10000, a="V"),
    # --- essence chaîne
    "L12": f("ATM", E_, 1.2, C, 4, 6000, 4800, "0W20", 3.4, 20000),
    "L13": f("ATM", E_, 1.3, C, 4, 6000, 4800, "0W20", 3.4, 20000),
    "L15": f("ATM", E_, 1.5, C, 4, 6600, 4600, "0W20", 3.6, 20000),
    "R18": f("ATM", E_, 1.8, C, 4, 6300, 4300, "0W20", 3.7, 20000),
    "K20": f("ATM", E_, 2.0, C, 4, 6000, 4500, "0W20", 4.2, 20000),
    "K20A-R": f("ATM", E_, 2.0, C, 4, 7400, 5600, "5W30", 4.2, 20000),
    "K24": f("ATM", E_, 2.4, C, 4, 7000, 4500, "0W20", 4.2, 20000),
    "F20C": f("ATM", E_, 2.0, C, 4, 8300, 7500, "10W40", 4.8, 10000),
    "F22C": f("ATM", E_, 2.2, C, 4, 7800, 6500, "10W40", 4.8, 10000),
    "P10-VTEC-T": f("TURBO", E_, 1.0, C, 3, 5500, 2250, "0W20", 3.6, 20000),
    "L15-VTEC-T": f("TURBO", E_, 1.5, C, 4, 5500, 1900, "0W20", 3.7, 20000),
    "K20C1": f("TURBO", E_, 2.0, C, 4, 6500, 2500, "0W30", 5.0, 15000),
    # --- hybrides
    "IMA-1.3": f("HYB_TE", E_, 1.3, C, 4, 5800, 1000, "0W20", 3.5, 20000),
    "IMA-1.5": f("HYB_TE", E_, 1.5, C, 4, 6100, 1000, "0W20", 3.6, 20000),
    "EHEV-1.5": f("HYB_TE", E_, 1.5, C, 4, 6000, 0, "0W20", 3.6, 20000),
    "EHEV-2.0": f("HYB_TE", E_, 2.0, C, 4, 6000, 0, "0W20", 4.0, 20000),
    "EPHEV-2.0": f("HYB_E", E_, 2.0, C, 4, 6000, 0, "0W20", 4.0, 20000),
    "NSX-HYB-3.5": f("HYB_TE", E_, 3.5, C, 6, 7500, 2000, "0W40", 7.0, 15000, a="V"),
    # --- diesel
    "ICTDI-2.2": f("TURBO", D, 2.2, C, 4, 4000, 2000, "5W30", 5.9, 20000),
    "IDTEC-2.2": f("TURBO", D, 2.2, C, 4, 4000, 2000, "0W30", 5.9, 20000),
    "IDTEC-1.6": f("TURBO", D, 1.6, C, 4, 4000, 2000, "0W30", 5.1, 20000),
    "ROVER-L-2.0TD": f("TURBO", D, 2.0, B, 4, 4200, 2000, "10W40", 4.5, 10000),
    "ISUZU-1.7TD": f("TURBO", D, 1.7, B, 4, 4400, 1800, "5W30", 4.5, 10000),
    # --- électriques
    "HONDA-E": electrique(), "ENY1-EV": electrique(),
}

mg = SaisieMoteurs(FAMILLES, "Honda")
L, LR, LS = [], [], []   # Honda, Honda Type R, Honda S2000
CL = "Données indicatives, à vérifier"

# ---------------------------------------------------------------- Civic
mg(L, "Civic", "EG", "1", "1991-10", "1995-08",
   [("1.3 75", "D13", 103), ("1.5 90", "D15", 128), ("1.6 VTEC 125", "D16", 144), ("VTi 1.6 160", "B16A", 150)], portes=3, reservoir=45,
   remarques=CL + " ; 3 portes, berline, CRX del Sol (1992)")
mg(L, "Civic", "EK", "1", "1995-09", "2001-01",
   [("1.4 90", "D14", 121), ("1.5 VTEC-E 90", "D15", 132), ("1.6 VTEC 114", "D16", 144), ("VTi 1.6 160", "B16A", 153),
    ("1.8 VTi 169", "B18C", 174, {"debut": "1997-01"}), ("2.0 TD 105", "ROVER-L-2.0TD", 210, {"debut": "1997-01"})], portes=3, reservoir=45,
   remarques=CL + " ; 3 portes, berline, Aerodeck et 5 portes (base Rover, Swindon)")
mg(L, "Civic", "EP", "1", "2001-02", "2005-12",
   [("1.4 90", "D14", 130), ("1.6 110", "D17", 152), ("1.7 i-CTDi 100", "ISUZU-1.7TD", 200, {"debut": "2002-06"}), ("1.3 IMA 86", "IMA-1.3", 119, {"debut": "2003-01"})],
   portes=3, reservoir=50, remarques="3 portes (EP), 5 portes (EU), berline IMA")
mg(L, "Civic", "FK", "1", "2006-01", "2011-12",
   [("1.4 83", "L13", 119), ("1.4 100", "L13", 127, {"debut": "2010-01"}), ("1.8 i-VTEC 140", "R18", 174), ("2.2 i-CTDi 140", "ICTDI-2.2", 340),
    ("2.2 i-DTEC 150", "IDTEC-2.2", 350, {"debut": "2010-01"}), ("Hybrid 1.3 IMA 115", "IMA-1.3", 123)], reservoir=50,
   remarques="3 et 5 portes (FK/FN) ; berline Hybrid (FD)")
mg(L, "Civic", "FK2", "1", "2012-02", "2014-12",
   [("1.4 100", "L13", 127), ("1.8 i-VTEC 142", "R18", 174), ("2.2 i-DTEC 150", "IDTEC-2.2", 350), ("1.6 i-DTEC 120", "IDTEC-1.6", 300, {"debut": "2013-01"})],
   reservoir=50, remarques="5 portes et Tourer (2014)")
mg(L, "Civic", "FK2", "2", "2015-01", "2016-12",
   [("1.4 100", "L13", 127), ("1.8 i-VTEC 142", "R18", 174), ("1.6 i-DTEC 120", "IDTEC-1.6", 300)], reservoir=50, remarques="Restylage")
mg(L, "Civic", "FK7", "1", "2017-03", "2022-03",
   [("1.0 VTEC Turbo 129", "P10-VTEC-T", 200), ("1.0 VTEC Turbo 126", "P10-VTEC-T", 180, {"debut": "2019-09"}), ("1.5 VTEC Turbo 182", "L15-VTEC-T", 240),
    ("1.6 i-DTEC 120", "IDTEC-1.6", 300, {"debut": "2018-03"})], reservoir=46, remarques="5 portes et berline (FC)")
mg(L, "Civic", "FL", "1", "2022-10", "2025-06", [("e:HEV 184", "EHEV-2.0", 315)], reservoir=40, remarques="11e génération, uniquement hybride en Europe")
mg(L, "Civic", "FL", "2", "2025-07", None, [("e:HEV 184", "EHEV-2.0", 315)], reservoir=40, remarques="Restylage")

# ---------------------------------------------------------------- Accord
mg(L, "Accord", "CE", "1", "1993-03", "1998-09",
   [("1.8 115", "F18", 158), ("2.0 131", "F20", 179), ("2.2 VTEC 150", "H22", 200), ("2.0 TDi 105", "ROVER-L-2.0TD", 210, {"debut": "1996-01"})],
   portes=4, reservoir=65, remarques=CL + " ; berline, coupé et Aerodeck")
mg(L, "Accord", "CG", "1", "1998-10", "2002-12",
   [("1.6 116", "D16", 145), ("1.8 136", "F18", 165), ("2.0 147", "F20", 186), ("Type-R 2.2 VTEC 212", "H22", 221), ("2.0 TDi 105", "ROVER-L-2.0TD", 210)],
   portes=4, reservoir=65, remarques=CL)
mg(L, "Accord", "CL", "1", "2003-01", "2008-06",
   [("2.0 155", "K20", 190), ("2.4 190", "K24", 223), ("2.2 i-CTDi 140", "ICTDI-2.2", 340, {"debut": "2004-01"})], portes=4, reservoir=65,
   remarques="Berline et Tourer ; Type-S")
mg(L, "Accord", "CU", "1", "2008-07", "2015-06",
   [("2.0 156", "K20", 192), ("2.4 201", "K24", 234), ("2.2 i-DTEC 150", "IDTEC-2.2", 350), ("2.2 i-DTEC 180", "IDTEC-2.2", 380)], portes=4, reservoir=65,
   remarques="Berline et Tourer ; restylage 2011 ; fin des ventes européennes 2015")

# ---------------------------------------------------------------- Jazz / petites
mg(L, "Jazz", "GD", "1", "2002-03", "2008-09", [("1.2 78", "L12", 110), ("1.4 83", "L13", 119)], reservoir=42, remarques="Monospace urbain (Magic Seats)")
mg(L, "Jazz", "GE", "1", "2008-10", "2015-08",
   [("1.2 90", "L12", 114), ("1.4 100", "L13", 127), ("Hybrid 1.3 IMA 98", "IMA-1.3", 123, {"debut": "2011-01"})], reservoir=42)
mg(L, "Jazz", "GK", "1", "2015-09", "2020-05", [("1.3 i-VTEC 102", "L13", 123), ("Dynamic 1.5 i-VTEC 130", "L15", 155, {"debut": "2018-06"})], reservoir=40)
mg(L, "Jazz", "GR", "1", "2020-06", "2023-08", [("e:HEV 109", "EHEV-1.5", 253)], reservoir=40, remarques="Hybride e:HEV ; Crosstar")
mg(L, "Jazz", "GR", "2", "2023-09", None, [("e:HEV 122", "EHEV-1.5", 253)], reservoir=40, remarques="Restylage ; Crosstar, Advance Sport")
mg(L, "Stream", "RN", "1", "2001-01", "2006-12", [("1.7 125", "D17", 154), ("2.0 156", "K20", 189)], places=7, reservoir=55, remarques="Monospace 7 places")
mg(L, "FR-V", "BE", "1", "2004-10", "2009-12",
   [("1.7 125", "D17", 154), ("1.8 i-VTEC 140", "R18", 174, {"debut": "2007-01"}), ("2.0 150", "K20", 192), ("2.2 i-CTDi 140", "ICTDI-2.2", 340)],
   places=6, reservoir=58, remarques="Monospace 6 places (3+3)")
mg(L, "Insight", "ZE2", "1", "2009-03", "2014-12", [("1.3 IMA 98", "IMA-1.3", 167)], reservoir=40, remarques="Hybride")
mg(L, "CR-Z", "ZF1", "1", "2010-06", "2016-12", [("1.5 IMA 124", "IMA-1.5", 174, {"fin": "2012-12"}), ("1.5 IMA 137", "IMA-1.5", 190, {"debut": "2013-01"})],
   portes=3, places=4, reservoir=40, remarques="Coupé hybride")
mg(L, "Honda e", "ZC7", "1", "2020-06", "2024-01", [("e 136", "HONDA-E", 315, el(36)), ("e Advance 154", "HONDA-E", 315, el(36))], places=4, reservoir=0,
   remarques="Citadine électrique (propulsion)")

# ---------------------------------------------------------------- SUV
mg(L, "HR-V", "GH", "1", "1999-01", "2006-06", [("1.6 105", "D16", 135), ("1.6 VTEC 124", "D16", 144)], portes=3, reservoir=55, remarques=CL + " ; 3 et 5 portes, 4WD")
mg(L, "HR-V", "RU", "1", "2015-09", "2021-03",
   [("1.5 i-VTEC 130", "L15", 155), ("1.6 i-DTEC 120", "IDTEC-1.6", 300), ("Sport 1.5 VTEC Turbo 182", "L15-VTEC-T", 240, {"debut": "2019-01"})], reservoir=50,
   remarques="Restylage 2018")
mg(L, "HR-V", "RV", "1", "2021-04", "2024-03", [("e:HEV 131", "EHEV-1.5", 253)], reservoir=40, remarques="Hybride e:HEV")
mg(L, "HR-V", "RV", "2", "2024-04", None, [("e:HEV 131", "EHEV-1.5", 253)], reservoir=40, remarques="Restylage")
mg(L, "CR-V", "RD1", "1", "1997-01", "2001-12", [("2.0 128", "B20B", 179), ("2.0 147", "B20B", 182, {"debut": "1999-01"})], reservoir=58, remarques=CL)
mg(L, "CR-V", "RD4", "1", "2002-01", "2006-12", [("2.0 150", "K20", 192), ("2.2 i-CTDi 140", "ICTDI-2.2", 340, {"debut": "2004-11"})], reservoir=58)
mg(L, "CR-V", "RE", "1", "2007-01", "2012-09",
   [("2.0 150", "K20", 192), ("2.2 i-CTDi 140", "ICTDI-2.2", 340, {"fin": "2009-12"}), ("2.2 i-DTEC 150", "IDTEC-2.2", 350, {"debut": "2010-01"})],
   reservoir=58, remarques="Restylage 2010")
mg(L, "CR-V", "RM", "1", "2012-10", "2018-08",
   [("2.0 i-VTEC 155", "K20", 192), ("2.2 i-DTEC 150", "IDTEC-2.2", 350, {"fin": "2014-12"}), ("1.6 i-DTEC 120", "IDTEC-1.6", 300, {"debut": "2013-09"}),
    ("1.6 i-DTEC 160", "IDTEC-1.6", 350, {"debut": "2015-01"})], reservoir=58, remarques="Restylage 2015")
mg(L, "CR-V", "RW", "1", "2018-09", "2023-08",
   [("1.5 VTEC Turbo 173", "L15-VTEC-T", 220), ("1.5 VTEC Turbo 193", "L15-VTEC-T", 243), ("Hybrid 184", "EHEV-2.0", 315, {"debut": "2019-03"})],
   reservoir=57, remarques="5 ou 7 places (essence)")
mg(L, "CR-V", "RS", "1", "2023-09", None,
   [("e:HEV 184", "EHEV-2.0", 335), ("e:PHEV 184", "EPHEV-2.0", 335, ph(18, 57))], reservoir=57, remarques="6e génération ; e:HEV AWD, e:PHEV traction")
mg(L, "ZR-V", "RZ", "1", "2023-01", None, [("e:HEV 184", "EHEV-2.0", 315)], reservoir=57, remarques="SUV compact hybride")
mg(L, "e:Ny1", "RS", "1", "2023-09", None, [("e:Ny1 204", "ENY1-EV", 310, el(69))], reservoir=0, remarques="SUV électrique (e:N Architecture F)")

# ---------------------------------------------------------------- coupés / sport
mg(L, "CRX", "EF", "1", "1987-09", "1991-12", [("1.4 90", "D14", 116), ("1.6 i 16V 125", "D16", 143), ("1.6 VTEC 150", "B16A", 145, {"debut": "1989-09"})],
   portes=2, places=4, reservoir=45, remarques=CL + " ; CRX del Sol (1992-1998) non détaillé")
mg(L, "Prelude", "BB1", "1", "1992-01", "1996-12", [("2.0 133", "F20", 177), ("2.2 VTEC 185", "H22", 206), ("2.3 160", "F23", 212)], portes=2, places=4,
   reservoir=60, remarques=CL)
mg(L, "Prelude", "BB5", "1", "1997-01", "2001-12", [("2.0 133", "F20", 177), ("2.2 VTi 185", "H22", 206), ("2.2 Type-S 200", "H22", 212, {"debut": "1998-09"})],
   portes=2, places=4, reservoir=60, remarques=CL)
mg(L, "Prelude", "BF1", "1", "2026-01", None, [("e:HEV 200", "EHEV-2.0", 315)], portes=2, places=4, reservoir=40,
   remarques="Coupé hybride (châssis du Civic Type R), S+ Shift ; date et puissance indicatives")
mg(L, "NSX", "NA1", "1", "1990-09", "2005-12",
   [("3.0 V6 274", "C30", 284, {"fin": "1997-02"}), ("3.2 V6 280", "C32", 304, {"debut": "1997-03"}), ("NSX-T 3.0 V6 252", "C30", 284, {"debut": "1995-03"})],
   portes=2, places=2, reservoir=70, remarques=CL + " ; restylage 2002 (phares fixes)")
mg(L, "NSX", "NC1", "1", "2016-09", "2022-11", [("3.5 V6 Hybrid 581", "NSX-HYB-3.5", 646)], portes=2, places=2, reservoir=59, remarques="Hybride 3 moteurs électriques")

# ---------------------------------------------------------------- Honda Type R
mg(LR, "Integra Type R", "DC2", "1", "1998-01", "2001-12", [("1.8 VTEC 190", "B18C", 178)], portes=3, places=4, reservoir=50, remarques=CL)
mg(LR, "Civic Type R", "EP3", "1", "2001-06", "2005-12", [("2.0 i-VTEC 200", "K20A-R", 196)], portes=3, places=4, reservoir=50, remarques="Produite à Swindon")
mg(LR, "Civic Type R", "FN2", "1", "2007-03", "2011-12", [("2.0 i-VTEC 201", "K20A-R", 193)], portes=3, places=4, reservoir=50)
mg(LR, "Civic Type R", "FK2", "1", "2015-06", "2017-03", [("2.0 VTEC Turbo 310", "K20C1", 400)], places=4, reservoir=50)
mg(LR, "Civic Type R", "FK8", "1", "2017-06", "2021-12", [("2.0 VTEC Turbo 320", "K20C1", 400)], places=4, reservoir=46, remarques="Restylage 2020 ; Limited Edition")
mg(LR, "Civic Type R", "FL5", "1", "2022-10", "2025-12", [("2.0 VTEC Turbo 329", "K20C1", 420)], places=4, reservoir=47,
   remarques="Fin de commercialisation en Europe (date indicative)")

# ---------------------------------------------------------------- Honda S2000
mg(LS, "S2000", "AP1", "1", "1999-09", "2003-12", [("2.0 VTEC 240", "F20C", 208)], portes=2, places=2, reservoir=50)
mg(LS, "S2000", "AP2", "1", "2004-01", "2009-06", [("2.0 VTEC 240", "F20C", 208), ("GT 2.0 VTEC 240", "F20C", 208)], portes=2, places=2, reservoir=50,
   remarques="Moteur 2.0 conservé en Europe (2.2 F22C réservé aux États-Unis) ; S2000 GT T (2008)")

MOT = Motorisations("Honda", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LR)
MOT.lier(LS)

DETAIL = {"Honda": L, "Honda Type R": LR, "Honda S2000": LS}
MOTEURS = MOT.moteurs()
