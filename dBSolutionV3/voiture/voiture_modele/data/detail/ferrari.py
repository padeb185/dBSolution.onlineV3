"""Ferrari : générations, phases, motorisations (marché européen) et moteurs liés.
Modèles de route depuis 1948 (166 Inter) jusqu'à la Luce électrique (2026). Les voitures de course pures
(125 S, 166 MM, 250 Testa Rossa…) et séries XX ne sont pas reprises. Données antérieures à 1990 indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

E_ = "ESS"
C, B = "CHAINE", "COURROIE"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def v12(l, rpm, nmrpm, huile, qte, km=10000, d=C, t="ATM"):
    return f(t, E_, l, d, 12, rpm, nmrpm, huile, qte, km, a="V")


def v8(l, rpm, nmrpm, huile, qte, km=10000, d=B, t="ATM"):
    return f(t, E_, l, d, 8, rpm, nmrpm, huile, qte, km, a="V")


FAMILLES = {
    # --- V12 avant (Colombo, Lampredi, F116/F133, F140)
    "V12-2.0": v12(2.0, 6000, 4500, "20W50", 10.0, 5000),
    "V12-2.6": v12(2.6, 6500, 5000, "20W50", 10.0, 5000),
    "V12-3.0": v12(3.0, 7000, 5500, "20W50", 10.0, 5000),
    "V12-3.3": v12(3.3, 7600, 5500, "20W50", 10.0, 5000),
    "V12-4.0": v12(4.0, 7000, 5000, "20W50", 10.0, 5000),
    "V12-4.4": v12(4.4, 7500, 5500, "20W50", 12.0, 5000),
    "V12-4.8": v12(4.8, 6800, 4600, "20W50", 12.0, 5000),
    "V12-4.9": v12(4.9, 6000, 4200, "20W50", 12.0, 5000),
    "F116-5.5": v12(5.5, 6500, 5000, "10W60", 12.0, 10000, d=B),
    "F133-5.7": v12(5.7, 7250, 5250, "10W60", 12.0, 10000, d=B),
    "F140-6.0": v12(6.0, 7600, 5600, "10W60", 15.0, 20000),
    "F140-6.3": v12(6.3, 8000, 6000, "5W40", 15.0, 20000),
    "F140-6.3-HY": v12(6.3, 9000, 6750, "5W40", 15.0, 20000, t="HYB_TE"),
    "F140-6.5": v12(6.5, 8500, 7000, "5W40", 16.0, 20000),
    # --- 12 cylindres à plat
    "B12-4.4": f("ATM", E_, 4.4, B, 12, 7000, 4600, "20W50", 13.0, 5000, a="PLAT"),
    "B12-4.9": f("ATM", E_, 4.9, B, 12, 6300, 4500, "10W60", 13.0, 10000, a="PLAT"),
    # --- V6 / V8 central arrière
    "DINO-V6-2.4": f("ATM", E_, 2.4, C, 6, 7600, 5500, "20W50", 8.0, 5000, a="V"),
    "V8-3.0": v8(3.0, 7000, 5000, "20W50", 10.0, 5000),
    "V8-3.2": v8(3.2, 7000, 5500, "20W50", 10.0, 10000),
    "V8-3.4": v8(3.4, 7200, 4200, "10W60", 10.0, 10000),
    "F129-3.5": v8(3.5, 8250, 6000, "10W60", 10.0, 10000),
    "F131-3.6": v8(3.6, 8500, 4750, "10W60", 10.0, 10000),
    "F136-4.3": v8(4.3, 8500, 5250, "10W60", 9.0, 20000, d=C),
    "F136-4.5": v8(4.5, 9000, 6000, "5W40", 9.0, 20000, d=C),
    "V8T-2.0": v8(2.0, 6500, 4100, "20W50", 10.0, 5000, t="TURBO"),
    "V8T-2.9": v8(2.9, 7000, 4000, "10W60", 10.0, 10000, t="TURBO"),
    "F154-3.9": v8(3.9, 7500, 3000, "5W40", 10.0, 20000, d=C, t="TURBO"),
    "F154-4.0-PHEV": v8(4.0, 7500, 6000, "5W40", 10.0, 20000, d=C, t="HYB_E"),
    "F163-3.0-PHEV": f("HYB_E", E_, 3.0, C, 6, 8000, 6250, "5W40", 8.0, 20000, a="V"),
    "F163-3.0-HY": f("HYB_TE", E_, 3.0, C, 6, 9000, 5550, "5W40", 8.0, 20000, a="V"),
    # --- électrique
    "LUCE-EV": electrique(),
}

mg = SaisieMoteurs(FAMILLES, "Ferrari")
L = []
CL = "Données indicatives (modèle ancien), à vérifier"

# ---------------------------------------------------------------- V12 avant classiques
mg(L, "166 Inter", "166", "1", "1948-01", "1951-12", [("Coupé 110", "V12-2.0", 160)], portes=2, places=2, reservoir=90, remarques=CL)
mg(L, "212 Inter", "212", "1", "1951-01", "1953-12", [("Coupé 150", "V12-2.6", 210)], portes=2, places=2, reservoir=100, remarques=CL)
mg(L, "250 GT", "250", "1", "1954-01", "1964-12",
   [("Europa GT 220", "V12-3.0", 260), ("Coupé Pinin Farina 240", "V12-3.0", 260, {"debut": "1958-01", "fin": "1960-12"}),
    ("California Spyder 260", "V12-3.0", 270, {"debut": "1957-06", "fin": "1962-12"}), ("Berlinetta SWB 280", "V12-3.0", 280, {"debut": "1959-10", "fin": "1962-12"}),
    ("GT 2+2 240", "V12-3.0", 260, {"debut": "1960-06", "fin": "1963-12"}), ("Lusso 250", "V12-3.0", 270, {"debut": "1962-10"})],
   portes=2, places=2, reservoir=100, remarques=CL)
mg(L, "250 GTO", "250 GTO", "1", "1962-01", "1964-12", [("GTO 300", "V12-3.0", 294)], portes=2, places=2, reservoir=130, remarques=CL)
mg(L, "275", "275", "1", "1964-10", "1968-12",
   [("GTB 280", "V12-3.3", 294), ("GTS 260", "V12-3.3", 294, {"fin": "1966-12"}), ("GTB/4 300", "V12-3.3", 294, {"debut": "1966-10"})],
   portes=2, places=2, reservoir=94, remarques=CL)
mg(L, "330", "330", "1", "1964-01", "1968-12", [("GT 2+2 300", "V12-4.0", 288), ("GTC 300", "V12-4.0", 330, {"debut": "1966-06"})],
   portes=2, places=4, reservoir=90, remarques=CL)
mg(L, "365", "365", "1", "1967-01", "1976-12",
   [("GT 2+2 320", "V12-4.4", 365, {"fin": "1971-12"}), ("GTC 320", "V12-4.4", 365, {"fin": "1970-12"}),
    ("GTB/4 Daytona 352", "V12-4.4", 431, {"debut": "1968-10", "fin": "1973-12"}), ("GTC/4 340", "V12-4.4", 432, {"debut": "1971-01", "fin": "1972-12"}),
    ("GT4 2+2 340", "V12-4.4", 422, {"debut": "1972-10"})], portes=2, places=2, reservoir=128, remarques=CL)
mg(L, "400", "400", "1", "1976-10", "1985-12", [("400 GT 340", "V12-4.8", 471, {"fin": "1979-06"}), ("400i 310", "V12-4.8", 416, {"debut": "1979-07"})],
   portes=2, places=4, reservoir=120, remarques=CL)
mg(L, "412", "412", "1", "1985-01", "1989-12", [("412 340", "V12-4.9", 451)], portes=2, places=4, reservoir=116, remarques=CL)

# ---------------------------------------------------------------- 12 à plat
mg(L, "365 GT4 BB", "BB", "1", "1973-01", "1976-12", [("BB 360", "B12-4.4", 422)], portes=2, places=2, reservoir=120, remarques=CL)
mg(L, "512 BB", "BB", "2", "1976-10", "1984-12", [("512 BB 360", "B12-4.9", 451, {"fin": "1981-06"}), ("512 BBi 340", "B12-4.9", 451, {"debut": "1981-07"})],
   portes=2, places=2, reservoir=120, remarques=CL)
mg(L, "Testarossa", "F110", "1", "1984-10", "1991-12", [("Testarossa 390", "B12-4.9", 490)], portes=2, places=2, reservoir=115)
mg(L, "Testarossa", "F110", "2", "1992-01", "1996-12",
   [("512 TR 428", "B12-4.9", 491, {"fin": "1994-12"}), ("F512 M 440", "B12-4.9", 500, {"debut": "1994-10"})], portes=2, places=2, reservoir=110)

# ---------------------------------------------------------------- V12 avant modernes
mg(L, "456", "F116", "1", "1992-10", "2003-12", [("456 GT 442", "F116-5.5", 550, {"fin": "1998-06"}), ("456M GT 442", "F116-5.5", 550, {"debut": "1998-07"})],
   portes=2, places=4, reservoir=110, remarques="GT et GTA (boîte auto)")
mg(L, "550", "F133", "1", "1996-07", "2001-12", [("Maranello 485", "F116-5.5", 568), ("Barchetta 485", "F116-5.5", 568, {"debut": "2000-10"})],
   portes=2, places=2, reservoir=114)
mg(L, "575M", "F133", "2", "2002-03", "2006-06", [("575M Maranello 515", "F133-5.7", 588), ("Superamerica 540", "F133-5.7", 588, {"debut": "2005-03"})],
   portes=2, places=2, reservoir=105)
mg(L, "612 Scaglietti", "F137", "1", "2004-01", "2011-06", [("612 Scaglietti 540", "F133-5.7", 588)], portes=2, places=4, reservoir=108)
mg(L, "Enzo", "F140", "1", "2002-10", "2004-12", [("Enzo 660", "F140-6.0", 657)], portes=2, places=2, reservoir=110, remarques="Série limitée (399 ex.)")
mg(L, "599", "F141", "1", "2006-03", "2012-06",
   [("GTB Fiorano 620", "F140-6.0", 608), ("GTO 670", "F140-6.0", 620, {"debut": "2010-04", "fin": "2011-12"}),
    ("SA Aperta 670", "F140-6.0", 620, {"debut": "2010-10", "fin": "2011-12"})], portes=2, places=2, reservoir=105)
mg(L, "FF", "F151", "1", "2011-03", "2016-06", [("FF 660", "F140-6.3", 683)], portes=2, places=4, reservoir=91, remarques="Shooting brake 4 roues motrices")
mg(L, "GTC4Lusso", "F151M", "1", "2016-07", "2020-12", [("GTC4Lusso 690", "F140-6.3", 697), ("GTC4Lusso T 610", "F154-3.9", 760, {"debut": "2016-10"})],
   portes=2, places=4, reservoir=91, remarques="Shooting brake ; T = V8 propulsion")
mg(L, "F12", "F152", "1", "2012-03", "2017-06", [("F12berlinetta 740", "F140-6.3", 690), ("F12tdf 780", "F140-6.3", 705, {"debut": "2015-10"})],
   portes=2, places=2, reservoir=92)
mg(L, "LaFerrari", "F150", "1", "2013-03", "2018-12", [("LaFerrari 963", "F140-6.3-HY", 900), ("Aperta 963", "F140-6.3-HY", 900, {"debut": "2016-10"})],
   portes=2, places=2, reservoir=86, remarques="Hybride HY-KERS, série limitée")
mg(L, "812", "F152M", "1", "2017-03", "2023-12",
   [("Superfast 800", "F140-6.5", 718), ("GTS 800", "F140-6.5", 718, {"debut": "2019-09"}),
    ("Competizione 830", "F140-6.5", 692, {"debut": "2021-05"}), ("Competizione A 830", "F140-6.5", 692, {"debut": "2021-12"})],
   portes=2, places=2, reservoir=92)
mg(L, "Monza", "F176", "1", "2019-01", "2021-12", [("SP1 810", "F140-6.5", 719), ("SP2 810", "F140-6.5", 719)], portes=0, places=2, reservoir=86,
   remarques="Série Icona, barchetta (SP1 monoplace)")
mg(L, "Daytona SP3", "F176-SP3", "1", "2022-01", "2024-12", [("Daytona SP3 840", "F140-6.5", 697)], portes=2, places=2, reservoir=86,
   remarques="Série Icona (599 ex.)")
mg(L, "Purosangue", "F175", "1", "2023-03", None, [("Purosangue 725", "F140-6.5", 716)], portes=4, places=4, reservoir=100, remarques="SUV 4 portes V12")
mg(L, "12Cilindri", "F167", "1", "2024-10", None, [("12Cilindri 830", "F140-6.5", 678), ("12Cilindri Spider 830", "F140-6.5", 678, {"debut": "2025-01"})],
   portes=2, places=2, reservoir=92)

# ---------------------------------------------------------------- Dino et V8 centraux
mg(L, "Dino", "Dino", "1", "1967-11", "1974-12", [("206 GT 180", "DINO-V6-2.4", 187, {"fin": "1969-12"}), ("246 GT 195", "DINO-V6-2.4", 225, {"debut": "1969-01"})],
   portes=2, places=2, reservoir=65, remarques=CL + " ; 246 GTS (1972)")
mg(L, "Dino 308 GT4", "F106", "1", "1973-10", "1980-12", [("308 GT4 255", "V8-3.0", 284)], portes=2, places=4, reservoir=80, remarques=CL)
mg(L, "308", "F106", "2", "1975-10", "1985-09",
   [("GTB 255", "V8-3.0", 284, {"fin": "1980-06"}), ("GTBi 214", "V8-3.0", 243, {"debut": "1980-07", "fin": "1982-09"}),
    ("GTB Quattrovalvole 240", "V8-3.0", 260, {"debut": "1982-10"}), ("GTS Quattrovalvole 240", "V8-3.0", 260, {"debut": "1982-10"})],
   portes=2, places=2, reservoir=74, remarques=CL + " ; GTS targa (1977)")
mg(L, "288 GTO", "F114", "1", "1984-03", "1987-12", [("288 GTO 400", "V8T-2.9", 496)], portes=2, places=2, reservoir=120, remarques="Série limitée (272 ex.)")
mg(L, "328", "F106", "3", "1985-09", "1989-12", [("GTB 270", "V8-3.2", 304), ("GTS 270", "V8-3.2", 304)], portes=2, places=2, reservoir=74)
mg(L, "GTB Turbo", "F106", "T", "1986-01", "1989-12", [("GTB Turbo 254", "V8T-2.0", 328), ("GTS Turbo 254", "V8T-2.0", 328)], portes=2, places=2,
   reservoir=74, remarques="Version 2.0 turbo (marché italien)")
mg(L, "F40", "F120", "1", "1987-07", "1992-12", [("F40 478", "V8T-2.9", 577)], portes=2, places=2, reservoir=120)
mg(L, "348", "F119", "1", "1989-09", "1995-12",
   [("tb 300", "V8-3.4", 324, {"fin": "1993-06"}), ("ts 300", "V8-3.4", 324, {"fin": "1993-06"}),
    ("GTB 320", "V8-3.4", 324, {"debut": "1993-07"}), ("Spider 320", "V8-3.4", 324, {"debut": "1993-03"})], portes=2, places=2, reservoir=88)
mg(L, "F355", "F129", "1", "1994-05", "1999-06",
   [("Berlinetta 380", "F129-3.5", 363), ("GTS 380", "F129-3.5", 363), ("Spider 380", "F129-3.5", 363, {"debut": "1995-03"})],
   portes=2, places=2, reservoir=82, remarques="Boîte F1 (1997)")
mg(L, "360", "F131", "1", "1999-03", "2005-06",
   [("Modena 400", "F131-3.6", 373), ("Spider 400", "F131-3.6", 373, {"debut": "2000-03"}),
    ("Challenge Stradale 425", "F131-3.6", 373, {"debut": "2003-03", "fin": "2004-12"})], portes=2, places=2, reservoir=95)
mg(L, "F430", "F131 EVO", "1", "2004-10", "2009-12",
   [("F430 490", "F136-4.3", 465), ("Spider 490", "F136-4.3", 465, {"debut": "2005-03"}),
    ("Scuderia 510", "F136-4.3", 470, {"debut": "2007-09"}), ("Scuderia Spider 16M 510", "F136-4.3", 470, {"debut": "2009-01"})],
   portes=2, places=2, reservoir=95)
mg(L, "458", "F142", "1", "2009-09", "2015-09",
   [("Italia 570", "F136-4.5", 540), ("Spider 570", "F136-4.5", 540, {"debut": "2011-09"}),
    ("Speciale 605", "F136-4.5", 540, {"debut": "2013-09"}), ("Speciale A 605", "F136-4.5", 540, {"debut": "2014-10"})],
   portes=2, places=2, reservoir=86)
mg(L, "488", "F142M", "1", "2015-03", "2019-12",
   [("GTB 670", "F154-3.9", 760), ("Spider 670", "F154-3.9", 760, {"debut": "2015-09"}),
    ("Pista 720", "F154-3.9", 770, {"debut": "2018-03"}), ("Pista Spider 720", "F154-3.9", 770, {"debut": "2018-09"})],
   portes=2, places=2, reservoir=78)
mg(L, "F8", "F142MFL", "1", "2019-03", "2023-06", [("Tributo 720", "F154-3.9", 770), ("Spider 720", "F154-3.9", 770, {"debut": "2019-09"})],
   portes=2, places=2, reservoir=78)
mg(L, "SF90", "F173", "1", "2019-06", "2025-06",
   [("Stradale 1000", "F154-4.0-PHEV", 800, {"batterie": 8}), ("Spider 1000", "F154-4.0-PHEV", 800, {"batterie": 8, "debut": "2020-11"})],
   portes=2, places=2, reservoir=68, remarques="Hybride rechargeable 4 roues motrices ; XX non reprise")
mg(L, "849 Testarossa", "F173M", "1", "2025-11", None,
   [("Testarossa 1050", "F154-4.0-PHEV", 842, {"batterie": 8}), ("Spider 1050", "F154-4.0-PHEV", 842, {"batterie": 8})],
   portes=2, places=2, reservoir=68, remarques="Remplace la SF90 ; données indicatives")
mg(L, "296", "F171", "1", "2022-06", None,
   [("GTB 830", "F163-3.0-PHEV", 740, {"batterie": 7}), ("GTS 830", "F163-3.0-PHEV", 740, {"batterie": 7, "debut": "2022-10"}),
    ("Speciale 880", "F163-3.0-PHEV", 740, {"batterie": 7, "debut": "2025-10"}), ("Speciale A 880", "F163-3.0-PHEV", 740, {"batterie": 7, "debut": "2026-01"})],
   portes=2, places=2, reservoir=65, remarques="V6 hybride rechargeable")
mg(L, "F80", "F250", "1", "2025-06", None, [("F80 1200", "F163-3.0-HY", 850)], portes=2, places=2, reservoir=69,
   remarques="Supercar hybride (799 ex.)")

# ---------------------------------------------------------------- GT V8 avant
mg(L, "California", "F149", "1", "2008-10", "2014-03", [("California 460", "F136-4.3", 485, {"fin": "2012-06"}), ("California 30 490", "F136-4.3", 505, {"debut": "2012-07"})],
   portes=2, places=4, reservoir=78, remarques="Coupé-cabriolet 2+2")
mg(L, "California", "F149M", "1", "2014-03", "2017-12", [("California T 560", "F154-3.9", 755)], portes=2, places=4, reservoir=78)
mg(L, "Portofino", "F164", "1", "2017-10", "2023-06", [("Portofino 600", "F154-3.9", 760, {"fin": "2020-09"}), ("Portofino M 620", "F154-3.9", 760, {"debut": "2020-10"})],
   portes=2, places=4, reservoir=80, remarques="Coupé-cabriolet 2+2")
mg(L, "Roma", "F169", "1", "2020-03", "2025-12", [("Roma 620", "F154-3.9", 760), ("Spider 620", "F154-3.9", 760, {"debut": "2023-06"})],
   portes=2, places=4, reservoir=80)
mg(L, "Amalfi", "F169M", "1", "2025-09", None, [("Amalfi 640", "F154-3.9", 760)], portes=2, places=4, reservoir=80, remarques="Remplace la Roma")

# ---------------------------------------------------------------- électrique
mg(L, "Luce", "F244", "1", "2026-10", None, [("Luce 1050", "LUCE-EV", 990, el(122))], portes=4, places=5, reservoir=0,
   remarques="Première Ferrari 100 % électrique, 4 moteurs ; premières livraisons octobre 2026")

MOT = Motorisations("Ferrari", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Ferrari": L}
MOTEURS = MOT.moteurs()
