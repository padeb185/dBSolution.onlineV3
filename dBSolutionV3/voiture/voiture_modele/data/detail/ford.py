"""Ford : générations, phases, motorisations (marché européen) et moteurs liés.
Ka, Fiesta, Escort, Sierra, Focus, Mondeo, Puma (coupé, crossover, Gen-E), Fusion, B-Max, C-Max, S-Max, Galaxy,
Kuga, EcoSport, Edge, Explorer et Capri électriques, Mustang, Mustang Mach-E, Ranger, Bronco, Tourneo Courier/Connect/Custom.
GT40, GT (2005) et GT (2017), anciennement marque Ford GT. Modèles nord-américains non vendus en Europe et utilitaires Transit non repris.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


FAMILLES = {
    # --- essence anciennes
    "KENT-1.0": f("ATM", E_, 1.0, C, 4, 5500, 3000, "20W50", 3.25, 5000),
    "KENT-1.1": f("ATM", E_, 1.1, C, 4, 5500, 3000, "20W50", 3.25, 5000),
    "KENT-1.3": f("ATM", E_, 1.3, C, 4, 5000, 3000, "20W50", 3.25, 7500),
    "CVH-1.3": f("ATM", E_, 1.3, B, 4, 6000, 3500, "15W40", 3.75, 10000),
    "CVH-1.4": f("ATM", E_, 1.4, B, 4, 5600, 4000, "15W40", 3.75, 10000),
    "CVH-1.6": f("ATM", E_, 1.6, B, 4, 6000, 4000, "15W40", 3.75, 10000),
    "CVH-1.6T": f("TURBO", E_, 1.6, B, 4, 6000, 3000, "15W40", 3.75, 10000),
    "PINTO-2.0": f("ATM", E_, 2.0, B, 4, 5200, 3500, "15W40", 4.0, 10000),
    "COSWORTH-YB": f("TURBO", E_, 2.0, B, 4, 6000, 4500, "10W40", 4.5, 10000),
    "COLOGNE-2.9": f("ATM", E_, 2.9, C, 6, 5700, 3000, "15W40", 4.5, 10000, a="V"),
    # --- Zetec / Sigma / Duratec
    "SIGMA-1.25": f("ATM", E_, 1.25, B, 4, 6000, 4000, "5W30", 3.8, 20000),
    "SIGMA-1.4": f("ATM", E_, 1.4, B, 4, 5700, 4000, "5W30", 3.8, 20000),
    "SIGMA-1.6": f("ATM", E_, 1.6, B, 4, 6000, 4000, "5W30", 4.1, 20000),
    "SIGMA-1.6-TI": f("ATM", E_, 1.6, B, 4, 6300, 4150, "5W30", 4.1, 20000),
    "ZETEC-1.6": f("ATM", E_, 1.6, B, 4, 6000, 4000, "5W30", 4.25, 20000),
    "ZETEC-1.8": f("ATM", E_, 1.8, B, 4, 5500, 4000, "5W30", 4.25, 20000),
    "ZETEC-2.0": f("ATM", E_, 2.0, B, 4, 6000, 4500, "5W30", 4.25, 20000),
    "DURATEC-1.25": f("ATM", E_, 1.25, B, 4, 6000, 4000, "5W30", 3.8, 20000),
    "DURATEC-1.0": f("ATM", E_, 1.0, C, 3, 6300, 4100, "5W20", 4.0, 20000),
    "DURATEC-HE-1.8": f("ATM", E_, 1.8, C, 4, 6000, 4000, "5W30", 4.3, 20000),
    "DURATEC-HE-2.0": f("ATM", E_, 2.0, C, 4, 6000, 4500, "5W30", 4.3, 20000),
    "DURATEC-HE-2.3": f("ATM", E_, 2.3, C, 4, 6500, 4200, "5W30", 4.3, 20000),
    "DURATEC-V6-2.5": f("ATM", E_, 2.5, C, 6, 6250, 4250, "5W30", 5.7, 20000, a="V"),
    "DURATEC-V6-3.0": f("ATM", E_, 3.0, C, 6, 6500, 4750, "5W30", 5.7, 20000, a="V"),
    "DURATEC-ST-2.5T": f("TURBO", E_, 2.5, C, 5, 6000, 1600, "5W30", 6.0, 20000),
    # --- EcoBoost
    "ECOBOOST-1.0": f("TURBO", E_, 1.0, B, 3, 6000, 1400, "5W20", 4.1, 20000),
    "ECOBOOST-1.0-MHEV": f("HYB_TE", E_, 1.0, B, 3, 6000, 1500, "5W20", 4.1, 20000),
    "ECOBOOST-1.5-3C": f("TURBO", E_, 1.5, B, 3, 6000, 1600, "5W20", 4.1, 20000),
    "ECOBOOST-1.5": f("TURBO", E_, 1.5, C, 4, 6000, 1600, "5W20", 4.1, 20000),
    "ECOBOOST-1.6": f("TURBO", E_, 1.6, C, 4, 5700, 1600, "5W30", 4.1, 20000),
    "ECOBOOST-2.0": f("TURBO", E_, 2.0, C, 4, 5500, 2000, "5W30", 5.4, 20000),
    "ECOBOOST-2.3": f("TURBO", E_, 2.3, C, 4, 6000, 2500, "5W30", 5.7, 20000),
    "ECOBOOST-V6-2.7": f("TURBO", E_, 2.7, C, 6, 5500, 3000, "5W30", 5.7, 15000, a="V"),
    "ECOBOOST-V6-3.0": f("TURBO", E_, 3.0, C, 6, 5750, 3500, "5W30", 5.7, 15000, a="V"),
    "ECOBOOST-V6-3.5": f("TURBO", E_, 3.5, C, 6, 6250, 5900, "5W30", 5.7, 15000, a="V"),
    "COYOTE-5.0": f("ATM", E_, 5.0, C, 8, 7000, 4600, "5W20", 9.0, 15000, a="V"),
    "MODULAR-5.4S": f("TURBO", E_, 5.4, C, 8, 6500, 4500, "5W50", 9.0, 10000, a="V"),
    "FORD-V8-4.7": f("ATM", E_, 4.7, C, 8, 6000, 4200, "20W50", 6.0, 5000, a="V"),
    "DURATEC-2.5-HEV": f("HYB_TE", E_, 2.5, C, 4, 6000, 4500, "0W20", 5.0, 20000),
    "DURATEC-2.5-PHEV": f("HYB_E", E_, 2.5, C, 4, 6000, 4500, "0W20", 5.0, 20000),
    "ECOBOOST-2.3-PHEV": f("HYB_E", E_, 2.3, C, 4, 5500, 2500, "5W30", 5.7, 20000),
    # --- diesel
    "D-1.6": f("ATM", D, 1.6, B, 4, 4800, 2500, "15W40", 5.0, 10000),
    "D-1.8": f("ATM", D, 1.8, B, 4, 4800, 2500, "15W40", 5.0, 10000),
    "ENDURA-1.8TD": f("TURBO", D, 1.8, B, 4, 4500, 2000, "10W40", 5.5, 10000),
    "DURATORQ-1.8": f("TURBO", D, 1.8, B, 4, 3700, 1900, "5W30", 5.5, 20000),
    "DV4-1.4": f("TURBO", D, 1.4, B, 4, 4000, 1750, "5W30", 3.8, 20000),
    "DV6-1.6": f("TURBO", D, 1.6, B, 4, 4000, 1750, "5W30", 3.8, 20000),
    "DV6-1.5": f("TURBO", D, 1.5, B, 4, 3600, 1750, "5W30", 3.8, 20000),
    "ECOBLUE-1.5": f("TURBO", D, 1.5, C, 4, 3600, 1500, "0W30", 4.0, 20000),
    "DW10-2.0": f("TURBO", D, 2.0, B, 4, 4000, 2000, "5W30", 5.5, 20000),
    "DURATORQ-2.0": f("TURBO", D, 2.0, C, 4, 4000, 1800, "5W30", 6.0, 20000),
    "DURATORQ-2.2": f("TURBO", D, 2.2, C, 4, 3500, 1800, "5W30", 6.0, 20000),
    "DURATORQ-2.2-RANGER": f("TURBO", D, 2.2, C, 4, 3700, 1500, "5W30", 7.0, 20000),
    "DURATORQ-3.2": f("TURBO", D, 3.2, C, 5, 3000, 1750, "5W30", 9.0, 20000),
    "EcoBlue-2.0": f("TURBO", D, 2.0, B, 4, 3500, 1750, "0W30", 6.0, 30000),
    "Lion-3.0V6": f("TURBO", D, 3.0, "COURROIE", 6, 3250, 1750, "5W30", 7.0, 30000, a="V"),
    # --- électriques
    "PUMA-GEN-E": electrique(), "MEB-FORD": electrique(), "MACH-E": electrique(),
}

mg = SaisieMoteurs(FAMILLES, "Ford")
L = []
CL = "Données indicatives (modèle ancien), à vérifier"

# ---------------------------------------------------------------- Ka / Fiesta
mg(L, "Ka", "RB", "1", "1996-09", "2008-11", [("1.3 60", "KENT-1.3", 103), ("1.3 70", "DURATEC-1.25", 106, {"debut": "2002-09"}),
                                             ("SportKa 1.6 95", "SIGMA-1.6", 135, {"debut": "2003-01", "fin": "2005-12"})],
   portes=3, places=4, reservoir=42, remarques="StreetKa roadster (2003)")
mg(L, "Ka", "RU8", "1", "2008-11", "2016-05", [("1.2 69", "DURATEC-1.25", 102), ("1.3 TDCi 75", "DV4-1.4", 145)], portes=3, places=4,
   reservoir=35, remarques="Base Fiat 500 (Tychy) ; moteurs Fiat")
mg(L, "Ka+", "B515", "1", "2016-10", "2020-06", [("1.2 70", "DURATEC-1.25", 112), ("1.2 85", "DURATEC-1.25", 112), ("1.5 TDCi 95", "DV6-1.5", 215, {"debut": "2018-09"})],
   reservoir=42, remarques="Ka+ et Ka+ Active")
mg(L, "Fiesta", "Mk1", "1", "1976-07", "1983-08", [("1.0 40", "KENT-1.0", 64), ("1.1 53", "KENT-1.1", 80), ("1.3 66", "KENT-1.3", 92)],
   portes=3, reservoir=34, remarques=CL)
mg(L, "Fiesta", "Mk2", "1", "1983-09", "1989-02",
   [("1.0 45", "KENT-1.0", 68), ("1.1 50", "KENT-1.1", 82), ("1.4 73", "CVH-1.4", 109), ("XR2 1.6 96", "CVH-1.6", 132), ("1.6 D 54", "D-1.6", 95)],
   portes=3, reservoir=34, remarques=CL)
mg(L, "Fiesta", "Mk3", "1", "1989-03", "1995-12",
   [("1.0 45", "KENT-1.0", 68), ("1.1 55", "KENT-1.1", 86), ("1.3 60", "KENT-1.3", 100, {"debut": "1992-01"}), ("1.4 73", "CVH-1.4", 109),
    ("XR2i 1.6 110", "CVH-1.6", 138), ("RS Turbo 1.6 133", "CVH-1.6T", 182, {"debut": "1990-06", "fin": "1992-12"}), ("1.8 D 60", "D-1.8", 110)],
   portes=3, reservoir=42, remarques="3 et 5 portes")
mg(L, "Fiesta", "Mk4", "1", "1995-10", "2002-03",
   [("1.25 16V 75", "SIGMA-1.25", 110), ("1.3 60", "KENT-1.3", 103), ("1.4 16V 90", "SIGMA-1.4", 123), ("1.6 16V 103", "SIGMA-1.6", 145, {"debut": "1999-09"}),
    ("1.8 D 60", "D-1.8", 105), ("1.8 TDDi 75", "ENDURA-1.8TD", 140, {"debut": "1999-09"})], portes=3, reservoir=40, remarques="Restylage 1999")
mg(L, "Fiesta", "Mk5", "1", "2002-04", "2008-09",
   [("1.25 75", "DURATEC-1.25", 110), ("1.4 80", "SIGMA-1.4", 124), ("1.6 100", "SIGMA-1.6", 146), ("ST 2.0 150", "DURATEC-HE-2.0", 190, {"debut": "2004-10"}),
    ("1.4 TDCi 68", "DV4-1.4", 160), ("1.6 TDCi 90", "DV6-1.6", 204, {"debut": "2004-01"})], portes=3, reservoir=45, remarques="Restylage 2005")
mg(L, "Fiesta", "Mk6", "1", "2008-10", "2012-08",
   [("1.25 60", "DURATEC-1.25", 110), ("1.25 82", "DURATEC-1.25", 114), ("1.4 96", "SIGMA-1.4", 128), ("1.6 120", "SIGMA-1.6-TI", 152),
    ("1.4 TDCi 70", "DV4-1.4", 160), ("1.6 TDCi 90", "DV6-1.6", 204), ("1.6 TDCi 95", "DV6-1.6", 205, {"debut": "2010-01"})], portes=3, reservoir=42)
mg(L, "Fiesta", "Mk6", "2", "2012-09", "2017-04",
   [("1.25 60", "DURATEC-1.25", 110), ("1.25 82", "DURATEC-1.25", 114), ("1.0 EcoBoost 100", "ECOBOOST-1.0", 170), ("1.0 EcoBoost 125", "ECOBOOST-1.0", 170),
    ("1.0 EcoBoost 140", "ECOBOOST-1.0", 180, {"debut": "2014-01"}), ("ST 1.6 EcoBoost 182", "ECOBOOST-1.6", 240, {"debut": "2013-03"}),
    ("ST200 1.6 EcoBoost 200", "ECOBOOST-1.6", 290, {"debut": "2016-06"}), ("1.5 TDCi 75", "DV6-1.5", 185), ("1.6 TDCi 95", "DV6-1.6", 215)],
   portes=3, reservoir=42, remarques="Restylage")
mg(L, "Fiesta", "Mk7", "1", "2017-05", "2021-12",
   [("1.1 70", "DURATEC-1.0", 105), ("1.1 85", "DURATEC-1.0", 110), ("1.0 EcoBoost 100", "ECOBOOST-1.0", 170), ("1.0 EcoBoost 125", "ECOBOOST-1.0", 170),
    ("1.0 EcoBoost 140", "ECOBOOST-1.0", 180), ("ST 1.5 EcoBoost 200", "ECOBOOST-1.5-3C", 290, {"debut": "2018-06"}),
    ("1.5 TDCi 85", "DV6-1.5", 215), ("1.5 TDCi 120", "DV6-1.5", 270, {"fin": "2019-12"}), ("1.0 EcoBoost Hybrid 125", "ECOBOOST-1.0-MHEV", 210, {"debut": "2020-06"})],
   portes=3, reservoir=42, remarques="Active (crossover) 2018")
mg(L, "Fiesta", "Mk7", "2", "2022-01", "2023-07",
   [("1.1 75", "DURATEC-1.0", 105), ("1.0 EcoBoost 100", "ECOBOOST-1.0", 170), ("1.0 EcoBoost Hybrid 125", "ECOBOOST-1.0-MHEV", 210),
    ("1.0 EcoBoost Hybrid 155", "ECOBOOST-1.0-MHEV", 240), ("ST 1.5 EcoBoost 200", "ECOBOOST-1.5-3C", 320)], portes=5, reservoir=42,
   remarques="Restylage ; fin de production juillet 2023")

# ---------------------------------------------------------------- Escort / Sierra
mg(L, "Escort", "Erika", "1", "1980-09", "1986-01",
   [("1.1 55", "KENT-1.1", 86), ("1.3 69", "CVH-1.3", 100), ("1.6 79", "CVH-1.6", 125), ("XR3i 1.6 105", "CVH-1.6", 138, {"debut": "1982-10"}),
    ("RS Turbo 1.6 132", "CVH-1.6T", 180, {"debut": "1984-10"}), ("1.6 D 54", "D-1.6", 95, {"debut": "1983-09"})], portes=3, reservoir=48, remarques=CL)
mg(L, "Escort", "Erika", "2", "1986-02", "1990-08",
   [("1.1 50", "KENT-1.1", 80), ("1.3 63", "KENT-1.3", 100), ("1.4 75", "CVH-1.4", 109), ("1.6 90", "CVH-1.6", 132), ("XR3i 1.6 105", "CVH-1.6", 138),
    ("RS Turbo 1.6 132", "CVH-1.6T", 180), ("1.6 D 54", "D-1.6", 95)], portes=3, reservoir=48, remarques=CL)
mg(L, "Escort", "CE14", "1", "1990-09", "1995-01",
   [("1.3 60", "KENT-1.3", 100), ("1.4 75", "CVH-1.4", 109), ("1.6 16V 90", "ZETEC-1.6", 134), ("1.8 16V 105", "ZETEC-1.8", 153),
    ("XR3i 1.8 16V 130", "ZETEC-1.8", 162), ("RS Cosworth 220", "COSWORTH-YB", 304, {"debut": "1992-05"}), ("1.8 D 60", "D-1.8", 110),
    ("1.8 TD 90", "ENDURA-1.8TD", 180)], portes=3, reservoir=55, remarques="3 et 5 portes, break, cabriolet")
mg(L, "Escort", "CE14", "2", "1995-01", "2000-12",
   [("1.3 60", "KENT-1.3", 103), ("1.4 75", "CVH-1.4", 109), ("1.6 16V 90", "ZETEC-1.6", 134), ("1.8 16V 115", "ZETEC-1.8", 160),
    ("1.8 D 60", "D-1.8", 110), ("1.8 TD 90", "ENDURA-1.8TD", 180)], portes=5, reservoir=55, remarques="3 et 5 portes, berline, break, cabriolet")
mg(L, "Sierra", "Mk1", "1", "1982-09", "1993-02",
   [("1.6 75", "CVH-1.6", 123), ("1.8 90", "CVH-1.6", 140), ("2.0 i 115", "PINTO-2.0", 160), ("XR4i 2.8 150", "COLOGNE-2.9", 216, {"fin": "1985-12"}),
    ("2.9 V6 4x4 150", "COLOGNE-2.9", 233, {"debut": "1987-01"}), ("RS Cosworth 204", "COSWORTH-YB", 277, {"debut": "1986-07", "fin": "1992-12"}),
    ("2.3 D 67", "D-1.8", 138), ("1.8 TD 75", "ENDURA-1.8TD", 155, {"debut": "1989-01"})], portes=5, reservoir=60, remarques=CL + " ; berline Sapphire, break")

# ---------------------------------------------------------------- Focus
mg(L, "Focus", "C170", "1", "1998-09", "2004-10",
   [("1.4 16V 75", "ZETEC-1.6", 123), ("1.6 16V 100", "ZETEC-1.6", 145), ("1.8 16V 115", "ZETEC-1.8", 160), ("2.0 16V 131", "ZETEC-2.0", 178),
    ("ST170 2.0 173", "ZETEC-2.0", 196, {"debut": "2002-01"}), ("RS 2.0 Turbo 215", "ZETEC-2.0", 310, {"debut": "2002-10", "fin": "2003-12"}),
    ("1.8 TDDi 90", "ENDURA-1.8TD", 200), ("1.8 TDCi 115", "DURATORQ-1.8", 250, {"debut": "2001-09"})], portes=5, reservoir=55,
   remarques="3 et 5 portes, berline, break ; restylage 2001")
mg(L, "Focus", "C307", "1", "2004-10", "2007-12",
   [("1.4 80", "SIGMA-1.4", 124), ("1.6 100", "SIGMA-1.6", 150), ("1.6 Ti-VCT 115", "SIGMA-1.6-TI", 155), ("1.8 125", "DURATEC-HE-1.8", 165),
    ("2.0 145", "DURATEC-HE-2.0", 185), ("ST 2.5 225", "DURATEC-ST-2.5T", 320, {"debut": "2005-09"}),
    ("1.6 TDCi 90", "DV6-1.6", 215), ("1.6 TDCi 110", "DV6-1.6", 240), ("1.8 TDCi 115", "DURATORQ-1.8", 280), ("2.0 TDCi 136", "DW10-2.0", 320)],
   portes=5, reservoir=55, remarques="3 et 5 portes, berline, break, CC")
mg(L, "Focus", "C307", "2", "2008-01", "2011-03",
   [("1.6 100", "SIGMA-1.6", 150), ("1.6 Ti-VCT 115", "SIGMA-1.6-TI", 155), ("1.8 125", "DURATEC-HE-1.8", 165), ("2.0 145", "DURATEC-HE-2.0", 185),
    ("ST 2.5 225", "DURATEC-ST-2.5T", 320), ("RS 2.5 305", "DURATEC-ST-2.5T", 440, {"debut": "2009-01"}),
    ("1.6 TDCi 90", "DV6-1.6", 215), ("1.6 TDCi 110", "DV6-1.6", 240), ("2.0 TDCi 136", "DW10-2.0", 320)], portes=5, reservoir=55, remarques="Restylage")
mg(L, "Focus", "C346", "1", "2011-03", "2014-09",
   [("1.6 85", "SIGMA-1.6-TI", 141), ("1.6 Ti-VCT 105", "SIGMA-1.6-TI", 150), ("1.6 Ti-VCT 125", "SIGMA-1.6-TI", 159),
    ("1.0 EcoBoost 100", "ECOBOOST-1.0", 170, {"debut": "2012-04"}), ("1.0 EcoBoost 125", "ECOBOOST-1.0", 170, {"debut": "2012-04"}),
    ("1.6 EcoBoost 150", "ECOBOOST-1.6", 240), ("1.6 EcoBoost 182", "ECOBOOST-1.6", 240),
    ("ST 2.0 EcoBoost 250", "ECOBOOST-2.0", 340, {"debut": "2012-06"}), ("1.6 TDCi 95", "DV6-1.6", 230), ("1.6 TDCi 115", "DV6-1.6", 270),
    ("2.0 TDCi 115", "DW10-2.0", 300), ("2.0 TDCi 140", "DW10-2.0", 320), ("2.0 TDCi 163", "DW10-2.0", 340)], portes=5, reservoir=55,
   remarques="5 portes, berline, break")
mg(L, "Focus", "C346", "2", "2014-10", "2018-05",
   [("1.6 85", "SIGMA-1.6-TI", 141), ("1.6 Ti-VCT 125", "SIGMA-1.6-TI", 159), ("1.0 EcoBoost 100", "ECOBOOST-1.0", 170),
    ("1.0 EcoBoost 125", "ECOBOOST-1.0", 170), ("1.5 EcoBoost 150", "ECOBOOST-1.5", 240), ("1.5 EcoBoost 182", "ECOBOOST-1.5", 240),
    ("ST 2.0 EcoBoost 250", "ECOBOOST-2.0", 360), ("RS 2.3 EcoBoost 350", "ECOBOOST-2.3", 440, {"debut": "2016-04"}),
    ("1.5 TDCi 95", "DV6-1.5", 250), ("1.5 TDCi 120", "DV6-1.5", 270), ("2.0 TDCi 150", "DW10-2.0", 370), ("ST 2.0 TDCi 185", "DW10-2.0", 400)],
   portes=5, reservoir=55, remarques="Restylage ; Electric non repris")
mg(L, "Focus", "C519", "1", "2018-06", "2022-03",
   [("1.0 EcoBoost 100", "ECOBOOST-1.0", 170), ("1.0 EcoBoost 125", "ECOBOOST-1.0", 170), ("1.5 EcoBoost 150", "ECOBOOST-1.5-3C", 240),
    ("1.5 EcoBoost 182", "ECOBOOST-1.5-3C", 240), ("ST 2.3 EcoBoost 280", "ECOBOOST-2.3", 420, {"debut": "2019-06"}),
    ("1.5 EcoBlue 95", "ECOBLUE-1.5", 250), ("1.5 EcoBlue 120", "ECOBLUE-1.5", 300), ("2.0 EcoBlue 150", "EcoBlue-2.0", 370),
    ("ST 2.0 EcoBlue 190", "EcoBlue-2.0", 400, {"debut": "2019-06"}), ("1.0 EcoBoost Hybrid 125", "ECOBOOST-1.0-MHEV", 210, {"debut": "2020-09"}),
    ("1.0 EcoBoost Hybrid 155", "ECOBOOST-1.0-MHEV", 240, {"debut": "2020-09"})], portes=5, reservoir=52, remarques="5 portes, break, Active")
mg(L, "Focus", "C519", "2", "2022-04", "2025-11",
   [("1.0 EcoBoost 100", "ECOBOOST-1.0", 170), ("1.0 EcoBoost Hybrid 125", "ECOBOOST-1.0-MHEV", 210), ("1.0 EcoBoost Hybrid 155", "ECOBOOST-1.0-MHEV", 240),
    ("ST 2.3 EcoBoost 280", "ECOBOOST-2.3", 420), ("1.5 EcoBlue 115", "ECOBLUE-1.5", 300)], portes=5, reservoir=52,
   remarques="Restylage ; fin de production novembre 2025")

# ---------------------------------------------------------------- Mondeo
mg(L, "Mondeo", "CDW27", "1", "1993-02", "1996-09",
   [("1.6 16V 90", "ZETEC-1.6", 130), ("1.8 16V 115", "ZETEC-1.8", 158), ("2.0 16V 136", "ZETEC-2.0", 180), ("2.5 V6 170", "DURATEC-V6-2.5", 220, {"debut": "1994-01"}),
    ("1.8 TD 90", "ENDURA-1.8TD", 180)], portes=4, reservoir=61, remarques="Berline, 5 portes, break")
mg(L, "Mondeo", "CDW27", "2", "1996-10", "2000-10",
   [("1.6 16V 90", "ZETEC-1.6", 140), ("1.8 16V 115", "ZETEC-1.8", 158), ("2.0 16V 131", "ZETEC-2.0", 178), ("2.5 V6 170", "DURATEC-V6-2.5", 220),
    ("ST200 2.5 V6 205", "DURATEC-V6-2.5", 235, {"debut": "1999-01"}), ("1.8 TD 90", "ENDURA-1.8TD", 180)], portes=4, reservoir=61)
mg(L, "Mondeo", "CD132", "1", "2000-11", "2007-03",
   [("1.8 110", "DURATEC-HE-1.8", 165), ("1.8 125", "DURATEC-HE-1.8", 170), ("2.0 145", "DURATEC-HE-2.0", 190), ("2.5 V6 170", "DURATEC-V6-2.5", 220),
    ("ST220 3.0 V6 226", "DURATEC-V6-3.0", 280, {"debut": "2002-01"}), ("2.0 TDCi 115", "DURATORQ-2.0", 280), ("2.0 TDCi 130", "DURATORQ-2.0", 330),
    ("2.2 TDCi 155", "DURATORQ-2.2", 360, {"debut": "2004-09"})], portes=4, reservoir=58, remarques="Restylage 2003")
mg(L, "Mondeo", "CD345", "1", "2007-04", "2014-12",
   [("1.6 Ti-VCT 125", "SIGMA-1.6-TI", 159), ("2.0 145", "DURATEC-HE-2.0", 185), ("2.3 161", "DURATEC-HE-2.3", 208), ("2.5 T 220", "DURATEC-ST-2.5T", 320),
    ("1.6 EcoBoost 160", "ECOBOOST-1.6", 240, {"debut": "2010-09"}), ("2.0 EcoBoost 203", "ECOBOOST-2.0", 300, {"debut": "2010-09"}),
    ("2.0 EcoBoost 240", "ECOBOOST-2.0", 340, {"debut": "2010-09"}), ("1.6 TDCi 115", "DV6-1.6", 270, {"debut": "2010-09"}),
    ("1.8 TDCi 125", "DURATORQ-1.8", 320, {"fin": "2010-08"}), ("2.0 TDCi 140", "DW10-2.0", 320), ("2.0 TDCi 163", "DW10-2.0", 340, {"debut": "2010-09"}),
    ("2.2 TDCi 175", "DURATORQ-2.2", 400, {"debut": "2008-09"}), ("2.2 TDCi 200", "DURATORQ-2.2", 420, {"debut": "2010-09"})],
   portes=4, reservoir=70, remarques="Restylage 2010")
mg(L, "Mondeo", "CD391", "1", "2014-11", "2022-03",
   [("1.0 EcoBoost 125", "ECOBOOST-1.0", 170, {"fin": "2018-12"}), ("1.5 EcoBoost 160", "ECOBOOST-1.5", 240), ("2.0 EcoBoost 203", "ECOBOOST-2.0", 300, {"fin": "2018-12"}),
    ("2.0 EcoBoost 240", "ECOBOOST-2.0", 345, {"fin": "2018-12"}), ("Hybrid 187", "DURATEC-2.5-HEV", 173), ("1.5 TDCi 120", "DV6-1.5", 270, {"fin": "2018-12"}),
    ("2.0 TDCi 150", "DW10-2.0", 350, {"fin": "2018-12"}), ("2.0 TDCi 180", "DW10-2.0", 400, {"fin": "2018-12"}), ("2.0 Bi-Turbo TDCi 210", "DW10-2.0", 450, {"fin": "2018-12"}),
    ("2.0 EcoBlue 150", "EcoBlue-2.0", 370, {"debut": "2019-01"}), ("2.0 EcoBlue 190", "EcoBlue-2.0", 400, {"debut": "2019-01"})],
   portes=4, reservoir=62, remarques="Berline, 5 portes, SW ; restylage 2019")

# ---------------------------------------------------------------- Puma / petits monospaces
mg(L, "Puma", "Coupé", "1", "1997-06", "2002-06", [("1.4 90", "SIGMA-1.4", 123, {"fin": "2000-12"}), ("1.6 103", "SIGMA-1.6", 145, {"debut": "2000-01"}),
                                                   ("1.7 125", "SIGMA-1.6", 157), ("Racing 1.7 155", "SIGMA-1.6", 162, {"debut": "2000-01", "fin": "2001-12"})],
   portes=2, places=4, reservoir=40, remarques="Coupé (base Fiesta Mk4)")
mg(L, "Puma", "J2K", "1", "2019-10", "2024-08",
   [("1.0 EcoBoost 125", "ECOBOOST-1.0", 170), ("1.0 EcoBoost Hybrid 125", "ECOBOOST-1.0-MHEV", 210), ("1.0 EcoBoost Hybrid 155", "ECOBOOST-1.0-MHEV", 240),
    ("ST 1.5 EcoBoost 200", "ECOBOOST-1.5-3C", 320, {"debut": "2020-09"}), ("1.5 EcoBlue 120", "ECOBLUE-1.5", 300, {"fin": "2021-12"})], reservoir=42,
   remarques="Crossover (base Fiesta)")
mg(L, "Puma", "J2K", "2", "2024-09", None,
   [("1.0 EcoBoost Hybrid 125", "ECOBOOST-1.0-MHEV", 210), ("1.0 EcoBoost Hybrid 155", "ECOBOOST-1.0-MHEV", 240), ("ST 1.0 EcoBoost Hybrid 170", "ECOBOOST-1.0-MHEV", 248),
    ("Gen-E 168", "PUMA-GEN-E", 290, el(43, debut="2025-01"))], reservoir=42, remarques="Restylage ; Puma Gen-E 100 % électrique (2025)")
mg(L, "Fusion", "JU2", "1", "2002-09", "2012-12",
   [("1.25 75", "DURATEC-1.25", 110), ("1.4 80", "SIGMA-1.4", 124), ("1.6 100", "SIGMA-1.6", 146), ("1.4 TDCi 68", "DV4-1.4", 160),
    ("1.6 TDCi 90", "DV6-1.6", 204, {"debut": "2005-09"})], reservoir=45, remarques="Mini-monospace")
mg(L, "B-Max", "JK8", "1", "2012-09", "2017-09",
   [("1.4 90", "SIGMA-1.4", 128), ("1.0 EcoBoost 100", "ECOBOOST-1.0", 170), ("1.0 EcoBoost 120", "ECOBOOST-1.0", 170), ("1.5 TDCi 75", "DV6-1.5", 185),
    ("1.6 TDCi 95", "DV6-1.6", 215)], reservoir=48, remarques="Monospace (portes coulissantes sans pied milieu)")
mg(L, "C-Max", "C214", "1", "2003-06", "2010-08",
   [("1.6 100", "SIGMA-1.6", 150), ("1.8 125", "DURATEC-HE-1.8", 165), ("2.0 145", "DURATEC-HE-2.0", 185), ("1.6 TDCi 110", "DV6-1.6", 240),
    ("2.0 TDCi 136", "DW10-2.0", 320)], reservoir=55, remarques="Focus C-Max jusqu'en 2007")
mg(L, "C-Max", "C344", "1", "2010-09", "2019-06",
   [("1.6 Ti-VCT 125", "SIGMA-1.6-TI", 159), ("1.0 EcoBoost 125", "ECOBOOST-1.0", 170, {"debut": "2012-09"}), ("1.6 EcoBoost 150", "ECOBOOST-1.6", 240),
    ("1.5 EcoBoost 150", "ECOBOOST-1.5", 240, {"debut": "2015-04"}), ("1.6 TDCi 115", "DV6-1.6", 270), ("2.0 TDCi 150", "DW10-2.0", 370)], reservoir=55,
   remarques="C-Max et Grand C-Max 7 places ; restylage 2015")
mg(L, "S-Max", "CD340", "1", "2006-05", "2015-08",
   [("2.0 145", "DURATEC-HE-2.0", 185), ("2.3 161", "DURATEC-HE-2.3", 208), ("2.5 T 220", "DURATEC-ST-2.5T", 320, {"fin": "2010-08"}),
    ("2.0 EcoBoost 203", "ECOBOOST-2.0", 300, {"debut": "2010-09"}), ("1.8 TDCi 125", "DURATORQ-1.8", 320, {"fin": "2010-08"}),
    ("2.0 TDCi 140", "DW10-2.0", 320), ("2.0 TDCi 163", "DW10-2.0", 340, {"debut": "2010-09"}), ("2.2 TDCi 200", "DURATORQ-2.2", 420, {"debut": "2010-09"})],
   places=7, reservoir=70, remarques="Monospace 5 ou 7 places ; restylage 2010")
mg(L, "S-Max", "CD539", "1", "2015-06", "2023-04",
   [("1.5 EcoBoost 160", "ECOBOOST-1.5", 240, {"fin": "2018-12"}), ("2.0 EcoBoost 240", "ECOBOOST-2.0", 345, {"fin": "2018-12"}),
    ("2.0 TDCi 150", "DW10-2.0", 350, {"fin": "2018-12"}), ("2.0 TDCi 180", "DW10-2.0", 400, {"fin": "2018-12"}),
    ("2.0 EcoBlue 150", "EcoBlue-2.0", 370, {"debut": "2019-01"}), ("2.0 EcoBlue 190", "EcoBlue-2.0", 400, {"debut": "2019-01"}),
    ("Hybrid 190", "DURATEC-2.5-HEV", 200, {"debut": "2021-04"})], places=7, reservoir=70)
mg(L, "Galaxy", "WGR", "1", "1995-06", "2006-03",
   [("2.0 116", "ZETEC-2.0", 170), ("2.3 16V 145", "DURATEC-HE-2.3", 203, {"debut": "1997-01"}), ("2.8 V6 174", "DURATEC-V6-2.5", 235),
    ("1.9 TDI 90", "ENDURA-1.8TD", 202), ("1.9 TDI 115", "ENDURA-1.8TD", 310, {"debut": "2000-06"})], places=7, reservoir=70,
   remarques="Jumeau VW Sharan / Seat Alhambra (moteurs VW) ; restylage 2000")
mg(L, "Galaxy", "CD340", "1", "2006-05", "2015-08",
   [("2.0 145", "DURATEC-HE-2.0", 185), ("2.3 161", "DURATEC-HE-2.3", 208), ("2.0 EcoBoost 203", "ECOBOOST-2.0", 300, {"debut": "2010-09"}),
    ("1.8 TDCi 125", "DURATORQ-1.8", 320, {"fin": "2010-08"}), ("2.0 TDCi 140", "DW10-2.0", 320), ("2.0 TDCi 163", "DW10-2.0", 340, {"debut": "2010-09"}),
    ("2.2 TDCi 200", "DURATORQ-2.2", 420, {"debut": "2010-09"})], places=7, reservoir=70)
mg(L, "Galaxy", "CD539", "1", "2015-06", "2023-04",
   [("1.5 EcoBoost 160", "ECOBOOST-1.5", 240, {"fin": "2018-12"}), ("2.0 EcoBoost 240", "ECOBOOST-2.0", 345, {"fin": "2018-12"}),
    ("2.0 TDCi 150", "DW10-2.0", 350, {"fin": "2018-12"}), ("2.0 TDCi 180", "DW10-2.0", 400, {"fin": "2018-12"}),
    ("2.0 EcoBlue 150", "EcoBlue-2.0", 370, {"debut": "2019-01"}), ("2.0 EcoBlue 190", "EcoBlue-2.0", 400, {"debut": "2019-01"}),
    ("Hybrid 190", "DURATEC-2.5-HEV", 200, {"debut": "2021-04"})], places=7, reservoir=70)

# ---------------------------------------------------------------- SUV
mg(L, "Kuga", "C394", "1", "2008-03", "2012-12",
   [("2.5 T 200", "DURATEC-ST-2.5T", 320, {"debut": "2009-01"}), ("2.0 TDCi 136", "DW10-2.0", 320), ("2.0 TDCi 140", "DW10-2.0", 320, {"debut": "2010-06"}),
    ("2.0 TDCi 163", "DW10-2.0", 340, {"debut": "2010-06"})], reservoir=66)
mg(L, "Kuga", "C520", "1", "2013-01", "2016-12",
   [("1.6 EcoBoost 150", "ECOBOOST-1.6", 240), ("1.6 EcoBoost 182", "ECOBOOST-1.6", 240), ("1.5 EcoBoost 150", "ECOBOOST-1.5", 240, {"debut": "2014-09"}),
    ("2.0 TDCi 120", "DW10-2.0", 310, {"debut": "2014-09"}), ("2.0 TDCi 140", "DW10-2.0", 320), ("2.0 TDCi 150", "DW10-2.0", 370, {"debut": "2014-09"}),
    ("2.0 TDCi 163", "DW10-2.0", 340, {"fin": "2014-08"}), ("2.0 TDCi 180", "DW10-2.0", 400, {"debut": "2014-09"})], reservoir=60)
mg(L, "Kuga", "C520", "2", "2017-01", "2019-12",
   [("1.5 EcoBoost 120", "ECOBOOST-1.5", 240), ("1.5 EcoBoost 150", "ECOBOOST-1.5", 240), ("1.5 EcoBoost 182", "ECOBOOST-1.5", 240),
    ("1.5 TDCi 120", "DV6-1.5", 270), ("2.0 TDCi 150", "DW10-2.0", 370), ("2.0 TDCi 180", "DW10-2.0", 400)], reservoir=60, remarques="Restylage")
mg(L, "Kuga", "C482", "1", "2020-01", "2024-03",
   [("1.5 EcoBoost 120", "ECOBOOST-1.5-3C", 240), ("1.5 EcoBoost 150", "ECOBOOST-1.5-3C", 240), ("1.5 EcoBlue 120", "ECOBLUE-1.5", 300),
    ("2.0 EcoBlue Hybrid 150", "EcoBlue-2.0", 370), ("2.0 EcoBlue 190", "EcoBlue-2.0", 400), ("2.5 Hybrid 190", "DURATEC-2.5-HEV", 200, {"debut": "2020-09"}),
    ("2.5 PHEV 225", "DURATEC-2.5-PHEV", 200, ph(14, 43))], reservoir=54)
mg(L, "Kuga", "C482", "2", "2024-04", None,
   [("1.5 EcoBoost 150", "ECOBOOST-1.5-3C", 240), ("2.5 Hybrid 183", "DURATEC-2.5-HEV", 200), ("2.5 PHEV 243", "DURATEC-2.5-PHEV", 200, ph(14, 43)),
    ("1.5 EcoBlue 120", "ECOBLUE-1.5", 300, {"fin": "2024-12"})], reservoir=54, remarques="Restylage ; hybride E85 en France")
mg(L, "EcoSport", "B515", "1", "2014-06", "2022-12",
   [("1.5 112", "SIGMA-1.6-TI", 140, {"fin": "2017-12"}), ("1.0 EcoBoost 100", "ECOBOOST-1.0", 170), ("1.0 EcoBoost 125", "ECOBOOST-1.0", 170),
    ("1.0 EcoBoost 140", "ECOBOOST-1.0", 180, {"debut": "2017-09"}), ("1.5 TDCi 95", "DV6-1.5", 215), ("1.5 EcoBlue 100", "ECOBLUE-1.5", 215, {"debut": "2018-09"}),
    ("1.5 EcoBlue 125", "ECOBLUE-1.5", 300, {"debut": "2018-09"})], reservoir=52, remarques="Restylage 2017")
mg(L, "Edge", "CD539", "1", "2016-04", "2020-12",
   [("2.0 TDCi 180", "DW10-2.0", 400, {"fin": "2018-12"}), ("2.0 Bi-Turbo TDCi 210", "DW10-2.0", 450, {"fin": "2018-12"}),
    ("2.0 EcoBlue 238", "EcoBlue-2.0", 500, {"debut": "2019-01"})], reservoir=69, remarques="SUV ; restylage 2019")
mg(L, "Explorer", "MEB", "1", "2024-06", None,
   [("Standard Range 170", "MEB-FORD", 310, el(52)), ("Extended Range 286", "MEB-FORD", 545, el(77)),
    ("Extended Range AWD 340", "MEB-FORD", 679, el(79))], reservoir=0, remarques="SUV électrique (MEB Volkswagen), produit à Cologne ; batteries LFP (2026)")
mg(L, "Capri", "MEB", "1", "2024-11", None,
   [("Standard Range 170", "MEB-FORD", 310, el(52)), ("Extended Range 286", "MEB-FORD", 545, el(77)),
    ("Extended Range AWD 340", "MEB-FORD", 679, el(79))], reservoir=0, remarques="SUV coupé électrique (MEB Volkswagen), produit à Cologne")
mg(L, "Mustang Mach-E", "CX727", "1", "2021-01", None,
   [("Standard Range 269", "MACH-E", 430, el(76)), ("Extended Range 294", "MACH-E", 430, el(91)),
    ("Extended Range AWD 351", "MACH-E", 580, el(91)), ("GT 487", "MACH-E", 860, el(91, debut="2021-09"))], reservoir=0, remarques="SUV électrique")
mg(L, "Bronco", "U725", "1", "2024-03", None, [("2.7 EcoBoost V6 335", "ECOBOOST-V6-2.7", 563)], portes=5, reservoir=63, remarques="4x4 (Badlands, Outer Banks)")

# ---------------------------------------------------------------- Mustang / Ranger
mg(L, "Mustang", "S550", "1", "2015-06", "2017-12", [("2.3 EcoBoost 317", "ECOBOOST-2.3", 432), ("GT 5.0 V8 421", "COYOTE-5.0", 524)],
   portes=2, places=4, reservoir=61, remarques="Fastback et Convertible (première vente officielle en Europe)")
mg(L, "Mustang", "S550", "2", "2018-01", "2023-12",
   [("2.3 EcoBoost 290", "ECOBOOST-2.3", 440, {"fin": "2020-12"}), ("GT 5.0 V8 450", "COYOTE-5.0", 529), ("Bullitt 5.0 V8 460", "COYOTE-5.0", 529, {"debut": "2018-06", "fin": "2019-12"}),
    ("Mach 1 5.0 V8 460", "COYOTE-5.0", 529, {"debut": "2021-06"})], portes=2, places=4, reservoir=61, remarques="Restylage")
mg(L, "Mustang", "S650", "1", "2024-03", None, [("GT 5.0 V8 446", "COYOTE-5.0", 540), ("Dark Horse 5.0 V8 454", "COYOTE-5.0", 540)],
   portes=2, places=4, reservoir=61, remarques="Fastback et Convertible")
mg(L, "Ranger", "T6", "1", "2012-01", "2015-12",
   [("2.2 TDCi 125", "DURATORQ-2.2-RANGER", 330), ("2.2 TDCi 150", "DURATORQ-2.2-RANGER", 375), ("3.2 TDCi 200", "DURATORQ-3.2", 470)], portes=4,
   reservoir=80, remarques="Pick-up simple, super et double cabine")
mg(L, "Ranger", "T6", "2", "2016-01", "2022-12",
   [("2.2 TDCi 130", "DURATORQ-2.2-RANGER", 385, {"fin": "2019-06"}), ("2.2 TDCi 160", "DURATORQ-2.2-RANGER", 385, {"fin": "2019-06"}),
    ("3.2 TDCi 200", "DURATORQ-3.2", 470, {"fin": "2019-06"}), ("2.0 EcoBlue 130", "EcoBlue-2.0", 340, {"debut": "2019-07"}),
    ("2.0 EcoBlue 170", "EcoBlue-2.0", 405, {"debut": "2019-07"}), ("2.0 EcoBlue Bi-Turbo 213", "EcoBlue-2.0", 500, {"debut": "2019-07"}),
    ("Raptor 2.0 EcoBlue Bi-Turbo 213", "EcoBlue-2.0", 500, {"debut": "2019-07"})], portes=4, reservoir=80, remarques="Restylages 2016 et 2019")
mg(L, "Ranger", "P703", "1", "2023-01", None,
   [("2.0 EcoBlue 170", "EcoBlue-2.0", 405), ("2.0 EcoBlue Bi-Turbo 205", "EcoBlue-2.0", 500), ("3.0 V6 EcoBlue 240", "Lion-3.0V6", 600),
    ("Raptor 3.0 EcoBoost V6 292", "ECOBOOST-V6-3.0", 491), ("PHEV 2.3 EcoBoost 281", "ECOBOOST-2.3-PHEV", 697, ph(11, 80, debut="2025-06"))],
   portes=4, reservoir=80, remarques="Pick-up ; Ranger PHEV (2025)")

# ---------------------------------------------------------------- Tourneo (versions voitures)
mg(L, "Tourneo Courier", "B460", "1", "2014-06", "2023-08",
   [("1.0 EcoBoost 100", "ECOBOOST-1.0", 170), ("1.5 TDCi 75", "DV6-1.5", 185), ("1.5 TDCi 95", "DV6-1.5", 215)], reservoir=48, remarques="Ludospace")
mg(L, "Tourneo Courier", "B795", "1", "2023-09", None,
   [("1.0 EcoBoost 125", "ECOBOOST-1.0", 200), ("1.5 EcoBlue 100", "ECOBLUE-1.5", 260), ("E-Tourneo Courier 136", "PUMA-GEN-E", 290, el(43, debut="2024-06"))],
   reservoir=45, remarques="Ludospace (Craiova)")
mg(L, "Tourneo Connect", "V408", "1", "2014-01", "2021-12",
   [("1.0 EcoBoost 100", "ECOBOOST-1.0", 170), ("1.5 EcoBlue 100", "ECOBLUE-1.5", 250, {"debut": "2018-09"}), ("1.5 EcoBlue 120", "ECOBLUE-1.5", 300, {"debut": "2018-09"}),
    ("1.6 TDCi 95", "DV6-1.6", 230, {"fin": "2015-12"}), ("1.5 TDCi 120", "DV6-1.5", 270, {"debut": "2016-01", "fin": "2018-08"})], places=7, reservoir=60,
   remarques="Ludospace, Grand Tourneo Connect 7 places")
mg(L, "Tourneo Connect", "SK8", "1", "2022-03", None,
   [("1.5 EcoBoost 114", "ECOBOOST-1.5", 220), ("2.0 EcoBlue 102", "EcoBlue-2.0", 280), ("2.0 EcoBlue 122", "EcoBlue-2.0", 320),
    ("1.5 EcoBoost PHEV 150", "ECOBOOST-1.5", 350, ph(20, 50, debut="2024-06"))], places=7, reservoir=50,
   remarques="Base VW Caddy (moteurs VW) ; Grand Tourneo Connect")
mg(L, "Tourneo Custom", "V362", "1", "2012-10", "2023-06",
   [("2.2 TDCi 125", "DURATORQ-2.2-RANGER", 350, {"fin": "2016-06"}), ("2.2 TDCi 155", "DURATORQ-2.2-RANGER", 385, {"fin": "2016-06"}),
    ("2.0 EcoBlue 130", "EcoBlue-2.0", 385, {"debut": "2016-07"}), ("2.0 EcoBlue 170", "EcoBlue-2.0", 405, {"debut": "2016-07"}),
    ("1.0 EcoBoost PHEV 126", "ECOBOOST-1.0", 355, ph(14, 60, debut="2019-09"))], portes=4, places=8, reservoir=80, remarques="Minibus 8-9 places")
mg(L, "Tourneo Custom", "V710", "1", "2023-07", None,
   [("2.0 EcoBlue 136", "EcoBlue-2.0", 360), ("2.0 EcoBlue 170", "EcoBlue-2.0", 405), ("2.5 PHEV 233", "DURATEC-2.5-PHEV", 200, ph(12, 55)),
    ("E-Tourneo Custom 218", "MACH-E", 415, el(64)), ("E-Tourneo Custom 136", "MACH-E", 415, el(64))], portes=4, places=8, reservoir=70,
   remarques="Minibus ; E-Tourneo Custom électrique")

# ---------------------------------------------------------------- GT40 et GT (ancienne marque Ford GT)
mg(L, "GT40", "Mk III", "1", "1967-01", "1969-12", [("GT40 Mk III 4.7 V8 306", "FORD-V8-4.7", 446)], portes=2, places=2, reservoir=106,
   remarques="Version route (7 ex.) ; GT40 de course non reprises ; " + CL)
mg(L, "GT", "2005", "1", "2004-09", "2006-09", [("GT 5.4 V8 550", "MODULAR-5.4S", 678)], portes=2, places=2, reservoir=65,
   remarques="V8 compresseur")
mg(L, "GT", "2017", "1", "2017-01", "2022-12", [("GT 3.5 EcoBoost V6 656", "ECOBOOST-V6-3.5", 746)], portes=2, places=2, reservoir=57,
   remarques="Supercar biturbo (série limitée)")

MOT = Motorisations("Ford", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Ford": L}
MOTEURS = MOT.moteurs()
