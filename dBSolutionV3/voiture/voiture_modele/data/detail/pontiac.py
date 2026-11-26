"""Pontiac : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Torpedo, Streamliner, Chieftain, Catalina, Star Chief, Bonneville, Grand Prix, GTO, Firebird, Trans Am, Fiero, Grand Am,
Sunfire, Aztek, Vibe, Wave / G3, Torrent, G6, Solstice et G8. Marque fermée en 2010.
Moteurs GM repris de chevrolet.py, buick.py, cadillac.py et oldsmobile.py, Toyota de toyota.py, Daewoo de daewoo.py (mêmes codes) ;
six et huit cylindres en ligne et V8 Pontiac (287 à 455), V8 5.0 TPI, 3.8 Turbo, 6.0 L76 ajoutés.
Puissances SAE converties en ch (× 1,014) ; jusqu'en 1971 puissances brutes (SAE gross). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .buick import FAMILLES as FAMILLES_BUICK
from .cadillac import FAMILLES as FAMILLES_CADILLAC
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET
from .daewoo import FAMILLES as FAMILLES_DAEWOO
from .oldsmobile import FAMILLES as FAMILLES_OLDS
from .toyota import FAMILLES as FAMILLES_TOYOTA

E_ = "ESS"
C, SV = "CHAINE", "NC"


def v8(l, rpm, nmrpm, t="ATM"):
    return f(t, E_, l, C, 8, rpm, nmrpm, "10W30", 4.7, 5000, a="V")


PONTIAC = {
    "PONT-I6-3.9": f("ATM", E_, 3.9, SV, 6, 3600, 1600, "SAE30", 5.0, 3000),
    "PONT-I8-4.1": f("ATM", E_, 4.1, SV, 8, 3600, 1600, "SAE30", 5.5, 3000),
    "PONT-I8-4.4": f("ATM", E_, 4.4, SV, 8, 3800, 2000, "SAE30", 5.5, 3000),
    "PONT-V8-4.7": v8(4.7, 4600, 2400), "PONT-V8-5.2": v8(5.2, 4800, 2800), "PONT-V8-5.7": v8(5.7, 4800, 2800), "PONT-V8-6.1": v8(6.1, 4800, 2800),
    "PONT-V8-6.4": v8(6.4, 4800, 2800), "PONT-V8-6.9": v8(6.9, 5200, 3600), "PONT-V8-6.6": v8(6.6, 5000, 3400), "PONT-V8-7.0": v8(7.0, 4800, 3200),
    "PONT-V8-7.5": v8(7.5, 4400, 3200), "PONT-V8-4.9": v8(4.9, 4000, 2000), "PONT-V8-4.9T": v8(4.9, 4400, 2800, t="TURBO"),
    "IRON-DUKE-2.5": FAMILLES_OLDS["IRON-DUKE-2.5"],
}
CHEVROLET = {**{k: FAMILLES_CHEVROLET[k] for k in ("SBC-5.7", "L98-5.7", "LT1-5.7", "LS1-5.7", "LS2-6.0", "LS3-6.2", "GM-2.4", "GM-2.0T")},
             "LB9-5.0": v8(5.0, 4400, 3200), "L76-6.0": v8(6.0, 5300, 4400),
             **{k: FAMILLES_OLDS[k] for k in ("GM-122-2.2", "ECOTEC-2.2")}}
BUICK = {**{k: FAMILLES_BUICK[k] for k in ("GM-3800", "GM-3800-SC", "GM-3.1", "GM-3.4", "GM-3.5", "GM-3.9", "GM-3.6", "GM-2.3-QUAD4")},
         "BUICK-3.8T": f("TURBO", E_, 3.8, C, 6, 4400, 2800, "10W30", 4.3, 5000, a="V")}
OLDS = {"GM-LD9-2.4": FAMILLES_OLDS["GM-LD9-2.4"]}
CADILLAC = {"GM-V6-2.8": FAMILLES_CADILLAC["GM-V6-2.8"]}
TOYOTA = {k: FAMILLES_TOYOTA[k] for k in ("1ZZ-FE", "2ZZ-GE", "2AZ-FE")}
DAEWOO = {"ETEC-1.6": FAMILLES_DAEWOO["ETEC-1.6"]}
FAMILLES = {**PONTIAC, **CHEVROLET, **BUICK, **OLDS, **CADILLAC, **TOYOTA, **DAEWOO}


def motoriste(fam):
    if fam in CHEVROLET or fam in CADILLAC:
        return "Oldsmobile" if fam in ("GM-122-2.2", "ECOTEC-2.2") else ("Cadillac" if fam in CADILLAC else "Chevrolet")
    if fam in BUICK:
        return "Buick"
    if fam in OLDS:
        return "Oldsmobile"
    if fam in TOYOTA:
        return "Toyota"
    if fam in DAEWOO:
        return "Daewoo"
    return "Pontiac"


mg = SaisieMoteurs(FAMILLES, "Pontiac", motoriste)
L = []
NA = "Marché nord-américain"
IND = NA + " ; données indicatives"

# ---------------------------------------------------------------- années 1940-1950
mg(L, "Torpedo", "Torpedo", "1", "1940-01", "1948-12", [("3.9 L6 91", "PONT-I6-3.9", 251), ("4.1 L8 104", "PONT-I8-4.1", 258)], portes=4, places=6, reservoir=68,
   remarques="Production interrompue de 1942 à 1945 ; " + IND)
mg(L, "Streamliner", "Streamliner", "1", "1941-01", "1952-12", [("3.9 L6 91", "PONT-I6-3.9", 251), ("4.1 L8 104", "PONT-I8-4.1", 258, {"fin": "1948-12"}),
                                                                ("4.4 L8 107", "PONT-I8-4.4", 312, {"debut": "1949-01"})], portes=4, places=6, reservoir=68, remarques=IND)
mg(L, "Chieftain", "Chieftain", "1", "1949-01", "1958-12", [("3.9 L6 91", "PONT-I6-3.9", 251, {"fin": "1954-12"}), ("4.4 L8 129", "PONT-I8-4.4", 312, {"fin": "1954-12"}),
                                                            ("4.7 V8 183", "PONT-V8-4.7", 359, {"debut": "1955-01", "fin": "1955-12"}), ("5.2 V8 208", "PONT-V8-5.2", 400, {"debut": "1956-01", "fin": "1956-12"}),
                                                            ("5.7 V8 256", "PONT-V8-5.7", 461, {"debut": "1957-01"})],
   portes=4, places=6, reservoir=76, remarques="V8 Strato-Streak à partir de 1955 ; " + IND)
mg(L, "Star Chief", "Star Chief", "1", "1954-01", "1966-12",
   [("4.4 L8 129", "PONT-I8-4.4", 312, {"fin": "1954-12"}), ("4.7 V8 183", "PONT-V8-4.7", 359, {"debut": "1955-01", "fin": "1955-12"}), ("5.7 V8 256", "PONT-V8-5.7", 461, {"debut": "1957-01", "fin": "1957-12"}),
    ("6.1 V8 259", "PONT-V8-6.1", 515, {"debut": "1958-01", "fin": "1958-12"}), ("6.4 V8 307", "PONT-V8-6.4", 563, {"debut": "1959-01"})], portes=4, places=6, reservoir=76, remarques=IND)
mg(L, "Catalina", "1950", "1", "1950-01", "1958-12", [("4.4 L8 107", "PONT-I8-4.4", 312, {"fin": "1954-12"}), ("4.7 V8 183", "PONT-V8-4.7", 359, {"debut": "1955-01"})],
   portes=2, places=6, reservoir=76, remarques="Coupé hardtop (finition des Chieftain / Star Chief) ; " + IND)
mg(L, "Catalina", "1959", "1", "1959-01", "1970-12",
   [("6.4 V8 248", "PONT-V8-6.4", 542, {"fin": "1966-12"}), ("6.4 V8 Tri-Power 335", "PONT-V8-6.4", 576, {"fin": "1966-12"}), ("6.9 V8 355", "PONT-V8-6.9", 624, {"debut": "1961-01", "fin": "1966-12"}),
    ("6.6 V8 294", "PONT-V8-6.6", 556, {"debut": "1967-01"}), ("7.0 V8 365", "PONT-V8-7.0", 637, {"debut": "1967-01"})], portes=4, places=6, reservoir=95,
   remarques="Modèle à part entière ; dont 2+2 ; " + IND)
mg(L, "Catalina", "1971", "1", "1971-01", "1981-12", [("5.7 V8 177", "PONT-V8-5.7", 373, {"fin": "1977-12"}), ("6.6 V8 203", "PONT-V8-6.6", 414, {"fin": "1979-12"}),
                                                      ("7.5 V8 254", "PONT-V8-7.5", 515, {"fin": "1975-12"}), ("4.9 V8 142", "PONT-V8-4.9", 319, {"debut": "1977-01"})],
   portes=4, places=6, reservoir=95, remarques="Puissances nettes à partir de 1972 ; " + IND)

# ---------------------------------------------------------------- Bonneville / Grand Prix
mg(L, "Bonneville", "1957", "1", "1957-01", "1970-12",
   [("Fuel Injection 5.7 V8 314", "PONT-V8-5.7", 495, {"fin": "1957-12"}), ("6.1 V8 304", "PONT-V8-6.1", 515, {"debut": "1958-01", "fin": "1958-12"}),
    ("6.4 V8 335", "PONT-V8-6.4", 576, {"debut": "1959-01", "fin": "1966-12"}), ("7.0 V8 365", "PONT-V8-7.0", 637, {"debut": "1967-01", "fin": "1969-12"}),
    ("7.5 V8 375", "PONT-V8-7.5", 678, {"debut": "1970-01"})], portes=4, places=6, reservoir=95, remarques=IND)
mg(L, "Bonneville", "1971", "1", "1971-01", "1986-12",
   [("7.5 V8 254", "PONT-V8-7.5", 515, {"fin": "1976-12"}), ("6.6 V8 203", "PONT-V8-6.6", 414, {"fin": "1979-12"}), ("4.9 V8 142", "PONT-V8-4.9", 319, {"debut": "1977-01", "fin": "1981-12"}),
    ("5.0 V8 152", "LB9-5.0", 325, {"debut": "1982-01", "remarques": "V8 Chevrolet 305 rattaché à la famille 5.0"})], portes=4, places=6, reservoir=95,
   remarques="Bonneville Brougham ; G-body (intermédiaire) de 1982 à 1986 ; " + IND)
mg(L, "Bonneville", "H-body", "1", "1987-01", "1999-12",
   [("3.8 V6 152", "GM-3800", 271, {"fin": "1991-12"}), ("3.8 V6 172", "GM-3800", 305, {"debut": "1992-01"}), ("SSEi 3.8 V6 Supercharged 208", "GM-3800-SC", 353, {"debut": "1992-01", "fin": "1995-12"}),
    ("SSEi 3.8 V6 Supercharged 243", "GM-3800-SC", 380, {"debut": "1996-01"})], portes=4, places=5, reservoir=68, remarques="Traction ; " + IND)
mg(L, "Bonneville", "G-body", "1", "2000-01", "2005-12", [("3.8 V6 208", "GM-3800", 312), ("SSEi 3.8 V6 Supercharged 243", "GM-3800-SC", 380, {"fin": "2003-12"}),
                                                          ("GXP 4.6 V8 279", "GM-3.9", 380, {"debut": "2004-01", "remarques": "V8 Northstar 4.6 rattaché provisoirement à la famille 3.9"})],
   portes=4, places=5, reservoir=70, remarques=IND)
mg(L, "Grand Prix", "1962", "1", "1962-01", "1968-12", [("6.4 V8 307", "PONT-V8-6.4", 563, {"fin": "1966-12"}), ("6.9 V8 355", "PONT-V8-6.9", 624, {"fin": "1966-12"}),
                                                        ("6.6 V8 355", "PONT-V8-6.6", 597, {"debut": "1967-01"}), ("7.0 V8 380", "PONT-V8-7.0", 651, {"debut": "1967-01"})],
   portes=2, places=5, reservoir=95, remarques="Coupé de luxe sportif ; " + IND)
mg(L, "Grand Prix", "G-body 1969", "1", "1969-01", "1987-12",
   [("6.6 V8 355", "PONT-V8-6.6", 597, {"fin": "1972-12"}), ("7.5 V8 375", "PONT-V8-7.5", 678, {"debut": "1970-01", "fin": "1972-12"}), ("6.6 V8 233", "PONT-V8-6.6", 441, {"debut": "1973-01", "fin": "1979-12"}),
    ("4.9 V8 137", "PONT-V8-4.9", 319, {"debut": "1977-01", "fin": "1981-12"}), ("3.8 V6 112", "GM-3800", 258, {"debut": "1978-01"}), ("5.0 V8 152", "LB9-5.0", 325, {"debut": "1982-01"})],
   portes=2, places=5, reservoir=68, remarques="A-body puis G-body ; dont SJ et 2+2 ; " + IND)
mg(L, "Grand Prix", "W-body", "1", "1988-01", "1996-12",
   [("2.8 V6 132", "GM-V6-2.8", 230, {"fin": "1989-12"}), ("3.1 V6 142", "GM-3.1", 251, {"debut": "1990-01", "fin": "1993-12"}), ("3.1 V6 162", "GM-3.1", 251, {"debut": "1994-01"}),
    ("Turbo 3.1 V6 208", "GM-3.1", 312, {"debut": "1989-01", "fin": "1990-12", "remarques": "3.1 Turbo (ASC/McLaren) rattaché à la famille 3.1"}), ("GTP 3.4 V6 DOHC 213", "GM-3.4", 292, {"debut": "1991-01"})],
   portes=2, places=5, reservoir=62, remarques="Coupé et berline ; " + IND)
mg(L, "Grand Prix", "W-body 1997", "1", "1997-01", "2003-12", [("3.1 V6 162", "GM-3.1", 251), ("3.8 V6 198", "GM-3800", 312), ("GTP 3.8 V6 Supercharged 243", "GM-3800-SC", 380)],
   portes=4, places=5, reservoir=68, remarques=IND)
mg(L, "Grand Prix", "W-body 2004", "1", "2004-01", "2008-12", [("3.8 V6 203", "GM-3800", 312), ("GTP 3.8 V6 Supercharged 264", "GM-3800-SC", 380),
                                                               ("GXP 5.3 V8 307", "LS2-6.0", 441, {"debut": "2005-01", "remarques": "V8 5.3 LS4 rattaché à la famille LS"})],
   portes=4, places=5, reservoir=64, remarques=IND)

# ---------------------------------------------------------------- GTO / Firebird / Trans Am / Fiero
mg(L, "GTO", "A-body 1964", "1", "1964-01", "1967-12", [("6.4 V8 330", "PONT-V8-6.4", 577, {"fin": "1966-12"}), ("Tri-Power 6.4 V8 365", "PONT-V8-6.4", 576, {"fin": "1966-12"}),
                                                        ("6.6 V8 340", "PONT-V8-6.6", 597, {"debut": "1967-01"}), ("6.6 V8 HO 365", "PONT-V8-6.6", 597, {"debut": "1967-01"})],
   portes=2, places=4, reservoir=81, remarques="Option des LeMans puis modèle à part entière (1966) ; " + IND)
mg(L, "GTO", "A-body 1968", "1", "1968-01", "1974-12",
   [("6.6 V8 355", "PONT-V8-6.6", 597, {"fin": "1971-12"}), ("Ram Air IV 6.6 V8 375", "PONT-V8-6.6", 603, {"debut": "1969-01", "fin": "1970-12"}), ("7.5 V8 365", "PONT-V8-7.5", 678, {"debut": "1970-01", "fin": "1971-12"}),
    ("6.6 V8 254", "PONT-V8-6.6", 441, {"debut": "1972-01", "fin": "1973-12"}), ("5.7 V8 203", "PONT-V8-5.7", 400, {"debut": "1974-01"})],
   portes=2, places=4, reservoir=81, remarques="Dont The Judge (1969-1971) ; GTO sur base Ventura en 1974 ; " + IND)
mg(L, "GTO", "Monaro", "1", "2004-01", "2006-12", [("5.7 V8 355", "LS1-5.7", 495, {"fin": "2004-12"}), ("6.0 V8 406", "LS2-6.0", 542, {"debut": "2005-01"})], portes=2, places=4, reservoir=68,
   remarques="Base Holden Monaro (Australie)")
mg(L, "Firebird", "F-body 1967", "1", "1967-01", "1969-12",
   [("3.8 L6 OHC 167", "PONT-I6-3.9", 292, {"remarques": "Six en ligne OHC 230 rattaché à la famille six cylindres"}), ("5.3 V8 254", "PONT-V8-5.7", 481, {"remarques": "V8 326 / 350 rattaché à la famille 5.7"}),
    ("6.6 V8 330", "PONT-V8-6.6", 597)], portes=2, places=4, reservoir=68, remarques="Coupé et cabriolet ; " + IND)
mg(L, "Firebird", "F-body 1970", "1", "1970-01", "1981-12",
   [("5.7 V8 259", "PONT-V8-5.7", 481, {"fin": "1971-12"}), ("6.6 V8 335", "PONT-V8-6.6", 597, {"fin": "1971-12"}), ("5.7 V8 177", "PONT-V8-5.7", 373, {"debut": "1972-01", "fin": "1977-12"}),
    ("6.6 V8 203", "PONT-V8-6.6", 414, {"debut": "1972-01", "fin": "1979-12"}), ("4.9 V8 152", "PONT-V8-4.9", 339, {"debut": "1977-01"}), ("3.8 V6 107", "GM-3800", 258, {"debut": "1976-01"})],
   portes=2, places=4, reservoir=78, remarques="Firebird, Esprit, Formula ; " + IND)
mg(L, "Firebird", "F-body 1982", "1", "1982-01", "1992-12",
   [("2.5 92", "IRON-DUKE-2.5", 180, {"fin": "1986-12"}), ("2.8 V6 137", "GM-V6-2.8", 197, {"fin": "1989-12"}), ("3.1 V6 142", "GM-3.1", 251, {"debut": "1990-01"}),
    ("5.0 V8 152", "LB9-5.0", 325), ("5.0 V8 TPI 218", "LB9-5.0", 386, {"debut": "1985-01"}), ("5.7 V8 TPI 233", "L98-5.7", 447, {"debut": "1987-01"})],
   portes=3, places=4, reservoir=60, remarques="Firebird et Formula ; " + IND)
mg(L, "Firebird", "F-body 1993", "1", "1993-01", "2002-12",
   [("3.4 V6 162", "GM-3.4", 271, {"fin": "1995-12"}), ("3.8 V6 203", "GM-3800", 312, {"debut": "1995-06"}), ("Formula 5.7 V8 279", "LT1-5.7", 441, {"fin": "1997-12"}),
    ("Formula 5.7 V8 309", "LS1-5.7", 454, {"debut": "1998-01"})], portes=3, places=4, reservoir=59, remarques="Coupé et cabriolet ; " + IND)
mg(L, "Trans Am", "F-body 1969", "1", "1969-03", "1981-12",
   [("Ram Air III 6.6 V8 340", "PONT-V8-6.6", 597, {"fin": "1970-12"}), ("7.5 V8 340", "PONT-V8-7.5", 678, {"debut": "1971-01", "fin": "1971-12"}),
    ("SD-455 7.5 V8 294", "PONT-V8-7.5", 529, {"debut": "1973-01", "fin": "1974-12"}), ("6.6 V8 223", "PONT-V8-6.6", 447, {"debut": "1975-01", "fin": "1979-12"}),
    ("4.9 V8 Turbo 213", "PONT-V8-4.9T", 461, {"debut": "1980-01"})], portes=2, places=4, reservoir=78, remarques="Version sportive de la Firebird ; " + IND)
mg(L, "Trans Am", "F-body 1982", "1", "1982-01", "1992-12",
   [("5.0 V8 TPI 218", "LB9-5.0", 386, {"debut": "1985-01"}), ("GTA 5.7 V8 TPI 238", "L98-5.7", 461, {"debut": "1987-01"}),
    ("Turbo Trans Am 3.8 V6 Turbo 254", "BUICK-3.8T", 461, {"debut": "1989-01", "fin": "1989-12"})], portes=3, places=4, reservoir=60, remarques="Dont GTA ; " + IND)
mg(L, "Trans Am", "F-body 1993", "1", "1993-01", "2002-12", [("5.7 V8 279", "LT1-5.7", 441, {"fin": "1997-12"}), ("5.7 V8 309", "LS1-5.7", 454, {"debut": "1998-01"}),
                                                             ("WS6 5.7 V8 330", "LS1-5.7", 468, {"debut": "1998-01"})], portes=3, places=4, reservoir=59, remarques=IND)
mg(L, "Fiero", "P-body", "1", "1984-01", "1988-12", [("2.5 93", "IRON-DUKE-2.5", 183), ("GT 2.8 V6 142", "GM-V6-2.8", 230, {"debut": "1985-01"})], portes=2, places=2, reservoir=38,
   remarques="Coupé à moteur central ; " + IND)

# ---------------------------------------------------------------- traction et années 2000
mg(L, "Grand Am", "N-body", "1", "1985-01", "1991-12", [("2.5 93", "IRON-DUKE-2.5", 183), ("2.0 Turbo 167", "GM-2.3-QUAD4", 237, {"debut": "1987-01", "fin": "1990-12", "remarques": "2.0 Turbo rattaché à la famille Quad 4"}),
                                                        ("2.3 Quad 4 152", "GM-2.3-QUAD4", 217, {"debut": "1988-01"}), ("3.0 V6 127", "GM-3.1", 217, {"fin": "1987-12"})],
   portes=2, places=5, reservoir=51, remarques="Coupé et berline ; " + IND)
mg(L, "Grand Am", "N-body 1992", "1", "1992-01", "1998-12", [("2.3 Quad 4 117", "GM-2.3-QUAD4", 190), ("2.3 Quad 4 177", "GM-2.3-QUAD4", 217, {"fin": "1994-12"}), ("3.1 V6 157", "GM-3.1", 251),
                                                             ("2.4 Twin Cam 152", "GM-LD9-2.4", 210, {"debut": "1996-01"})], portes=2, places=5, reservoir=57, remarques=IND)
mg(L, "Grand Am", "N-body 1999", "1", "1999-01", "2005-12", [("2.4 Twin Cam 152", "GM-LD9-2.4", 210, {"fin": "2001-12"}), ("2.2 Ecotec 142", "ECOTEC-2.2", 203, {"debut": "2002-01"}),
                                                             ("3.4 V6 172", "GM-3.4", 271)], portes=2, places=5, reservoir=57, remarques=IND)
mg(L, "Sunfire", "J-body", "1", "1995-01", "2005-12", [("2.2 122", "GM-122-2.2", 176, {"fin": "2002-12"}), ("2.4 Twin Cam 152", "GM-LD9-2.4", 210, {"fin": "2002-12"}),
                                                       ("2.2 Ecotec 142", "ECOTEC-2.2", 203, {"debut": "2003-01"})], portes=2, places=4, reservoir=57,
   remarques="Coupé, berline et cabriolet ; " + IND)
mg(L, "Aztek", "U-body", "1", "2001-01", "2005-12", [("3.4 V6 188", "GM-3.4", 285)], portes=5, places=5, reservoir=70, remarques=IND)
mg(L, "Vibe", "E130", "1", "2002-06", "2008-12", [("1.8 132", "1ZZ-FE", 170), ("GT 1.8 182", "2ZZ-GE", 176, {"fin": "2006-12"})], portes=5, places=5, reservoir=50,
   remarques="Jumelle de la Toyota Matrix ; " + IND)
mg(L, "Vibe", "E140", "1", "2009-01", "2010-08", [("1.8 134", "1ZZ-FE", 172), ("2.4 160", "2AZ-FE", 218)], portes=5, places=5, reservoir=50, remarques="Jumelle de la Toyota Matrix ; " + IND)
mg(L, "Wave", "T200", "1", "2004-09", "2009-12", [("1.6 107", "ETEC-1.6", 145)], portes=4, places=5, reservoir=45,
   remarques="Base Daewoo Kalos (Canada) ; renommée G3 en 2009 (aussi vendue aux États-Unis) ; " + IND)
mg(L, "Torrent", "Theta", "1", "2005-09", "2009-12", [("3.4 V6 188", "GM-3.4", 285, {"fin": "2007-12"}), ("3.6 V6 268", "GM-3.6", 337, {"debut": "2008-01"})],
   portes=5, places=5, reservoir=78, remarques="Jumeau du Chevrolet Equinox ; dont GXP ; " + IND)
mg(L, "G6", "Epsilon", "1", "2005-01", "2010-12", [("2.4 167", "GM-2.4", 230, {"debut": "2006-01"}), ("3.5 V6 204", "GM-3.5", 298), ("3.9 V6 230", "GM-3.9", 325, {"debut": "2006-01"}),
                                                   ("GXP 3.6 V6 256", "GM-3.6", 339, {"debut": "2008-01"})], portes=4, places=5, reservoir=61,
   remarques="Berline, coupé et coupé-cabriolet ; " + IND)
mg(L, "Solstice", "Kappa", "1", "2006-01", "2009-12", [("2.4 179", "GM-2.4", 225), ("GXP 2.0 Turbo 264", "GM-2.0T", 353, {"debut": "2007-01"})], portes=2, places=2, reservoir=51,
   remarques="Roadster, coupé targa en 2009 ; " + IND)
mg(L, "G8", "Zeta", "1", "2008-01", "2009-12", [("3.6 V6 260", "GM-3.6", 339), ("GT 6.0 V8 366", "L76-6.0", 522), ("GXP 6.2 V8 421", "LS3-6.2", 529, {"debut": "2009-01"})],
   portes=4, places=5, reservoir=73, remarques="Base Holden Commodore (Australie)")

MOT = Motorisations("Pontiac", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Pontiac": L}
MOTEURS = MOT.moteurs()
