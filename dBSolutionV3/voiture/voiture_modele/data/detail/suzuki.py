"""Suzuki : générations, phases, motorisations (marché européen) et moteurs liés.
Jimny (LJ, SJ / Samurai, JB, JB74), Alto, Swift (dont Sport), Baleno, Celerio, Splash, Wagon R+, Ignis, Liana, SX4, S-Cross,
Vitara / Grand Vitara, Kizashi, Across, Swace et e Vitara.
Moteurs Suzuki K10 / K12 repris d'opel.py, diesels Fiat (opel.py, fiat.py, cadillac.py), Renault (renault.py), PSA (citroen.py),
Mazda (mazda.py) et moteurs Toyota (Across, Swace) et électrique e Vitara de toyota.py (mêmes codes) ; moteurs Suzuki ajoutés.
Solio et Cappuccino (Japon) non repris. Données anciennes indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .cadillac import FAMILLES as FAMILLES_CADILLAC
from .citroen import FAMILLES as FAMILLES_CITROEN
from .fiat import FAMILLES as FAMILLES_FIAT
from .mazda import FAMILLES as FAMILLES_MAZDA
from .opel import FAMILLES as FAMILLES_OPEL
from .renault import FAMILLES as FAMILLES_RENAULT
from .toyota import FAMILLES as FAMILLES_TOYOTA

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"


def m(l, n, rpm, nmrpm, t="ATM", d=C, q=3.5, a="EN_LIGNE"):
    return f(t, E_, l, d, n, rpm, nmrpm, "5W30", q, 15000, a=a)


SZ = {
    "SZ-2T-0.36": f("ATM", E_, 0.36, "NC", 2, 6000, 5000, "SAE30", 2.0, 3000),
    "SZ-2T-0.55": f("ATM", E_, 0.55, "NC", 3, 5500, 3500, "SAE30", 2.0, 3000),
    "F8A-0.8": m(0.8, 4, 5500, 3000, d=B), "F10A-1.0": m(1.0, 4, 5000, 3000, d=B), "F10D-1.1": m(1.1, 4, 6000, 3000, d=B),
    "G10-1.0": m(1.0, 3, 5500, 3000, d=B), "G13-1.3": m(1.3, 4, 6000, 3500, d=B), "G13B-1.3": m(1.3, 4, 6450, 5000, d=B), "G16-1.6": m(1.6, 4, 6000, 4000, d=B, q=4.0),
    "J18-1.8": m(1.8, 4, 6500, 3500, d=B, q=4.0), "J20-2.0": m(2.0, 4, 6000, 3000, q=4.5), "J24-2.4": m(2.4, 4, 6000, 3800, q=4.5),
    "M13-1.3": m(1.3, 4, 6000, 4000), "M15-1.5": m(1.5, 4, 5900, 4100), "M16-1.6": m(1.6, 4, 6000, 4400, q=4.0),
    "H20-2.0V6": m(2.0, 6, 6500, 4500, q=4.5, a="V"), "H25-2.5V6": m(2.5, 6, 6500, 4000, q=4.5, a="V"), "H27-2.7V6": m(2.7, 6, 6000, 4000, q=4.5, a="V"),
    "N32-3.2V6": m(3.2, 6, 6200, 3500, q=5.5, a="V"),
    "K10C-1.0T": m(1.0, 3, 5500, 2000, t="TURBO", q=3.2), "K14C-1.4T": m(1.4, 4, 5500, 2000, t="TURBO", q=3.5),
    "K14D-1.4T-MHEV": m(1.4, 4, 5500, 2000, t="HYB_TE", q=3.5), "K12-1.2": m(1.2, 4, 6000, 4400, q=3.2),
    "K12-SHVS": m(1.2, 4, 6000, 4400, t="HYB_TE", q=3.2), "K15C-HEV": m(1.5, 4, 6000, 4400, t="HYB_TE", q=4.0), "Z12E-MHEV": m(1.2, 3, 5700, 4500, t="HYB_TE", q=3.2),
    "K15B-1.5": m(1.5, 4, 6000, 4000, q=3.5),
}
REPRIS = {
    **{k: FAMILLES_OPEL[k] for k in ("SUZUKI-K10", "SUZUKI-K12", "FIAT-1.3CDTI")},
    "FIAT-1.9TID": FAMILLES_CADILLAC["FIAT-1.9TID"],
    **{k: FAMILLES_FIAT[k] for k in ("MJ-1.6", "MJ-2.0")},
    **{k: FAMILLES_RENAULT[k] for k in ("K9K", "F9Q", "F8Q")},
    **{k: FAMILLES_CITROEN[k] for k in ("DW10ATED", "DV4TD")},
    "MZ-RF-2.0D": FAMILLES_MAZDA["MZ-RF-2.0D"],
    **{k: FAMILLES_TOYOTA[k] for k in ("A25A-PHEV", "2ZR-FXE", "Suzuki-EV")},
}
FAMILLES = {**SZ, **REPRIS}
MOTORISTES = {"FIAT-1.3CDTI": "Fiat", "FIAT-1.9TID": "Fiat", "MJ-1.6": "Fiat", "MJ-2.0": "Fiat", "K9K": "Renault", "F9Q": "Renault", "F8Q": "Renault",
              "DW10ATED": "Peugeot", "DV4TD": "Peugeot", "MZ-RF-2.0D": "Mazda", "A25A-PHEV": "Toyota", "2ZR-FXE": "Toyota"}


def motoriste(fam):
    return MOTORISTES.get(fam, "Suzuki")


mg = SaisieMoteurs(FAMILLES, "Suzuki", motoriste)
L = []
IND = "données indicatives"

# ---------------------------------------------------------------- Jimny
mg(L, "Jimny", "LJ", "1", "1970-04", "1981-12",
   [("LJ10 0.36 2T 25", "SZ-2T-0.36", 34, {"fin": "1972-05"}), ("LJ50 0.55 2T 33", "SZ-2T-0.55", 57, {"debut": "1972-05"}), ("LJ80 0.8 41", "F8A-0.8", 60, {"debut": "1977-10"})],
   portes=2, places=4, reservoir=40, remarques="LJ10, LJ20, LJ50 et LJ80 ; " + IND)
mg(L, "Jimny", "SJ", "1", "1981-05", "1998-12", [("SJ410 1.0 45", "F10A-1.0", 74), ("SJ413 / Samurai 1.3 64", "G13-1.3", 100, {"debut": "1984-01"}),
                                                 ("Samurai 1.3 70", "G13-1.3", 103, {"debut": "1988-01"}), ("1.9 D 63", "F8Q", 120, {"debut": "1996-01"})],
   portes=2, places=4, reservoir=40, remarques="SJ410, SJ413, Samurai (fabriqué en Espagne) ; " + IND)
mg(L, "Jimny", "JB", "1", "1998-09", "2018-06",
   [("1.3 80", "G13B-1.3", 110, {"fin": "2004-12"}), ("1.3 85", "M13-1.3", 110, {"debut": "2005-01"}), ("1.5 DDiS 65", "K9K", 160, {"debut": "2004-01", "fin": "2005-12"}),
    ("1.5 DDiS 86", "K9K", 200, {"debut": "2006-01", "fin": "2009-12"})], portes=2, places=4, reservoir=40, remarques="Dont cabriolet (2000-2009)")
mg(L, "Jimny", "JB74", "1", "2018-10", "2024-12", [("1.5 102", "K15B-1.5", 130)], portes=2, places=4, reservoir=40,
   remarques="Vendu en Europe comme utilitaire 2 places à partir de 2021")

# ---------------------------------------------------------------- citadines
mg(L, "Alto", "SS80", "1", "1981-01", "1984-12", [("0.8 40", "F8A-0.8", 60)], portes=3, places=4, reservoir=27, remarques=IND)
mg(L, "Alto", "HA", "1", "1994-09", "2006-12", [("1.0 53", "F10A-1.0", 77, {"fin": "2002-06"}), ("1.1 63", "F10D-1.1", 88, {"debut": "2002-07"})], portes=5, places=4, reservoir=35, remarques=IND)
mg(L, "Alto", "GF", "1", "2009-01", "2014-12", [("1.0 68", "SUZUKI-K10", 90)], portes=5, places=4, reservoir=35, remarques="Jumelle de la Nissan Pixo")
mg(L, "Celerio", "LF", "1", "2014-09", "2019-12", [("1.0 68", "SUZUKI-K10", 90)], portes=5, places=5, reservoir=35)
mg(L, "Wagon R+", "MM", "1", "1997-12", "2008-03",
   [("1.0 65", "F10A-1.0", 82, {"fin": "2000-01"}), ("1.0 58", "SUZUKI-K10", 85, {"debut": "2000-01"}), ("1.2 76", "SUZUKI-K12", 105), ("1.3 DDiS 70", "FIAT-1.3CDTI", 170, {"debut": "2003-06"})],
   portes=5, places=5, reservoir=41, remarques="Jumelle de l'Opel Agila A ; " + IND)
mg(L, "Splash", "EX", "1", "2008-04", "2015-03", [("1.0 65", "SUZUKI-K10", 90), ("1.2 86", "SUZUKI-K12", 114), ("1.2 94", "SUZUKI-K12", 118, {"debut": "2010-01"}), ("1.3 DDiS 75", "FIAT-1.3CDTI", 190)],
   portes=5, places=5, reservoir=45, remarques="Jumelle de l'Opel Agila B")
mg(L, "Ignis", "FH", "1", "2000-09", "2008-12", [("1.3 83", "M13-1.3", 110), ("1.3 94", "M13-1.3", 118), ("Sport 1.5 109", "M15-1.5", 143, {"debut": "2003-06"}), ("1.3 DDiS 70", "FIAT-1.3CDTI", 170, {"debut": "2003-06"})],
   portes=5, places=5, reservoir=41, remarques=IND)
mg(L, "Ignis", "MF", "1", "2016-10", None, [("1.2 90", "K12-1.2", 120), ("1.2 SHVS 90", "K12-SHVS", 120), ("1.2 SHVS 83", "K12-SHVS", 107, {"debut": "2020-03"})],
   portes=5, places=5, reservoir=32, remarques="Restylage 2020 ; hybride léger SHVS")

# ---------------------------------------------------------------- Swift / Baleno
mg(L, "Swift", "SA", "1", "1983-01", "1989-12", [("1.0 50", "G10-1.0", 76), ("1.3 68", "G13-1.3", 103), ("GTi 1.3 101", "G13B-1.3", 113, {"debut": "1986-01"})], portes=3, places=5, reservoir=34,
   remarques=IND)
mg(L, "Swift", "AA/AB", "1", "1989-01", "2003-12",
   [("1.0 53", "G10-1.0", 76), ("1.3 68", "G13-1.3", 103), ("GTi 1.3 101", "G13B-1.3", 113, {"fin": "1996-12"}), ("1.6 4x4 92", "G16-1.6", 130, {"fin": "1995-12"}), ("1.3 85", "G13-1.3", 110, {"debut": "1996-01"})],
   portes=5, places=5, reservoir=40, remarques="3 et 5 portes, berline (fabriquée en Hongrie) ; " + IND)
mg(L, "Swift", "RS", "1", "2005-03", "2010-09",
   [("1.3 92", "M13-1.3", 116), ("1.5 102", "M15-1.5", 133), ("1.3 DDiS 75", "FIAT-1.3CDTI", 190), ("Sport 1.6 125", "M16-1.6", 148, {"debut": "2006-06"})], portes=5, places=5, reservoir=43,
   remarques="3 et 5 portes")
mg(L, "Swift", "FZ", "1", "2010-09", "2017-03", [("1.2 94", "SUZUKI-K12", 118), ("1.3 DDiS 75", "FIAT-1.3CDTI", 190), ("Sport 1.6 136", "M16-1.6", 160, {"debut": "2011-12"})],
   portes=5, places=5, reservoir=42, remarques="3 et 5 portes")
mg(L, "Swift", "AZ", "1", "2017-04", "2024-03",
   [("1.2 90", "K12-1.2", 120), ("1.2 SHVS 90", "K12-SHVS", 120), ("1.0 Boosterjet 111", "K10C-1.0T", 170, {"fin": "2020-03"}), ("Sport 1.4 Boosterjet 140", "K14C-1.4T", 220, {"debut": "2018-01", "fin": "2020-03"}),
    ("1.2 SHVS 83", "K12-SHVS", 107, {"debut": "2020-04"}), ("Sport 1.4 Boosterjet Hybrid 129", "K14D-1.4T-MHEV", 235, {"debut": "2020-04"})], portes=5, places=5, reservoir=37,
   remarques="Dont Swift Sport")
mg(L, "Swift", "AZH", "1", "2024-04", None, [("1.2 Hybrid 82", "Z12E-MHEV", 112)], portes=5, places=5, reservoir=37, remarques="Nouveau trois cylindres hybride léger")
mg(L, "Baleno", "EG", "1", "1995-09", "2002-12", [("1.3 85", "G13-1.3", 110), ("1.6 98", "G16-1.6", 130), ("GTi 1.8 120", "J18-1.8", 152, {"debut": "1996-01"})],
   portes=4, places=5, reservoir=51, remarques="3 portes, berline et break ; " + IND)
mg(L, "Baleno", "EW", "1", "2016-04", "2019-12", [("1.2 90", "K12-1.2", 120), ("1.2 SHVS 90", "K12-SHVS", 120), ("1.0 Boosterjet 111", "K10C-1.0T", 170)], portes=5, places=5, reservoir=37)
mg(L, "Liana", "ER", "1", "2001-09", "2007-12", [("1.3 90", "M13-1.3", 113), ("1.6 106", "M16-1.6", 145), ("1.4 DDiS 90", "DV4TD", 160, {"debut": "2004-06", "remarques": "DV4 PSA 90 ch"})],
   portes=5, places=5, reservoir=50, remarques="Berline et 5 portes")

# ---------------------------------------------------------------- SX4 / S-Cross
mg(L, "SX4", "GY", "1", "2006-06", "2014-12",
   [("1.5 112", "M15-1.5", 145), ("1.6 107", "M16-1.6", 145, {"fin": "2009-12"}), ("1.6 120", "M16-1.6", 156, {"debut": "2010-01"}), ("1.9 DDiS 120", "FIAT-1.9TID", 280, {"fin": "2009-12"}),
    ("2.0 DDiS 135", "MJ-2.0", 320, {"debut": "2010-01"})], portes=5, places=5, reservoir=50, remarques="Jumeau du Fiat Sedici ; berline 2007")
mg(L, "S-Cross", "JY", "1", "2013-09", "2021-12",
   [("1.6 120", "M16-1.6", 156), ("1.6 DDiS 120", "MJ-1.6", 300), ("1.0 Boosterjet 111", "K10C-1.0T", 170, {"debut": "2016-09"}), ("1.4 Boosterjet 140", "K14C-1.4T", 220, {"debut": "2016-09"}),
    ("1.4 Boosterjet Hybrid 129", "K14D-1.4T-MHEV", 235, {"debut": "2020-04"})], portes=5, places=5, reservoir=47, remarques="SX4 S-Cross ; restylage 2016")
mg(L, "S-Cross", "JY", "2", "2022-01", None, [("1.4 Boosterjet Hybrid 129", "K14D-1.4T-MHEV", 235), ("1.5 Full Hybrid 115", "K15C-HEV", 138, {"debut": "2022-09"})],
   portes=5, places=5, reservoir=47, remarques="Nouvelle carrosserie sur la même base")

# ---------------------------------------------------------------- Vitara / Grand Vitara
mg(L, "Vitara", "ET/TA", "1", "1988-09", "1998-12",
   [("1.6 80", "G16-1.6", 127), ("1.6 16V 97", "G16-1.6", 133, {"debut": "1991-01"}), ("2.0 V6 136", "H20-2.0V6", 174, {"debut": "1994-01"}),
    ("2.0 TD 87", "MZ-RF-2.0D", 212, {"debut": "1996-01", "remarques": "Diesel Mazda RF"})], portes=3, places=4, reservoir=42, remarques="3 et 5 portes, cabriolet ; " + IND)
mg(L, "Grand Vitara", "FT", "1", "1998-03", "2005-08",
   [("1.6 94", "G16-1.6", 135), ("2.0 128", "J20-2.0", 182), ("2.5 V6 144", "H25-2.5V6", 204), ("2.0 HDi 109", "DW10ATED", 250, {"debut": "2001-01"}),
    ("XL-7 2.7 V6 173", "H27-2.7V6", 231, {"debut": "2001-06"})], portes=5, places=5, reservoir=66, remarques="3 et 5 portes, XL-7 (7 places) ; " + IND)
mg(L, "Grand Vitara", "JT", "1", "2005-09", "2015-12",
   [("1.6 106", "M16-1.6", 145), ("2.0 140", "J20-2.0", 183), ("2.4 169", "J24-2.4", 225, {"debut": "2008-09"}), ("3.2 V6 233", "N32-3.2V6", 284, {"debut": "2008-09"}),
    ("1.9 DDiS 129", "F9Q", 300)], portes=5, places=5, reservoir=66, remarques="3 et 5 portes ; restylages 2008 et 2012")
mg(L, "Vitara", "LY", "1", "2015-03", "2024-03",
   [("1.6 120", "M16-1.6", 156, {"fin": "2020-03"}), ("1.6 DDiS 120", "MJ-1.6", 300, {"fin": "2018-08"}), ("1.0 Boosterjet 111", "K10C-1.0T", 170, {"debut": "2018-09", "fin": "2020-03"}),
    ("1.4 Boosterjet 140", "K14C-1.4T", 220, {"debut": "2016-06", "fin": "2020-03"}), ("1.4 Boosterjet Hybrid 129", "K14D-1.4T-MHEV", 235, {"debut": "2020-04"}),
    ("1.5 Full Hybrid 115", "K15C-HEV", 138, {"debut": "2022-04"})], portes=5, places=5, reservoir=47, remarques="Restylage 2018")
mg(L, "Vitara", "LY", "2", "2024-04", None, [("1.4 Boosterjet Hybrid 129", "K14D-1.4T-MHEV", 235), ("1.5 Full Hybrid 115", "K15C-HEV", 138)], portes=5, places=5, reservoir=47,
   remarques="Restylage")
mg(L, "e Vitara", "YY8", "1", "2025-11", None,
   [("e Vitara 144", "Suzuki-EV", 189, {"reservoir": 0, "batterie": 49}), ("e Vitara 174", "Suzuki-EV", 193, {"reservoir": 0, "batterie": 61}),
    ("e Vitara AWD 184", "Suzuki-EV", 307, {"reservoir": 0, "batterie": 61})], portes=5, places=5, reservoir=0,
   remarques="SUV électrique (jumeau du Toyota Urban Cruiser) ; " + IND)

# ---------------------------------------------------------------- autres
mg(L, "Kizashi", "RE", "1", "2010-01", "2014-12", [("2.4 178", "J24-2.4", 230)], portes=4, places=5, reservoir=63, remarques="Berline, 4x4 en option")
mg(L, "Across", "AXAH54", "1", "2020-10", None, [("2.5 Plug-in Hybrid 306", "A25A-PHEV", 227, {"batterie": 18})], portes=5, places=5, reservoir=55, remarques="Jumeau du Toyota RAV4 PHEV")
mg(L, "Swace", "E210", "1", "2020-09", None, [("1.8 Hybrid 122", "2ZR-FXE", 142, {"fin": "2022-12"}), ("1.8 Hybrid 140", "2ZR-FXE", 142, {"debut": "2023-01"})], portes=5, places=5, reservoir=43,
   remarques="Break, jumeau de la Toyota Corolla Touring Sports")

MOT = Motorisations("Suzuki", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Suzuki": L}
MOTEURS = MOT.moteurs()
