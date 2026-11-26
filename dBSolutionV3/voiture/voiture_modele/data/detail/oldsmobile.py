"""Oldsmobile : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Curved Dash, Model 20, Light Eight, 88 / Delta 88, 98, Starfire, F-85, Cutlass, 442, Vista Cruiser, Custom Cruiser, Toronado,
Omega, Firenza, Cutlass Ciera, Cutlass Calais, Cutlass Supreme, Touring Sedan, Achieva, Silhouette, Bravada, Aurora,
Intrigue, Alero. Marque fermée en 2004.
Moteurs GM repris de buick.py, chevrolet.py et cadillac.py (mêmes codes) ; V8 Rocket et moteurs Oldsmobile ajoutés.
Puissances SAE converties en ch (× 1,014) ; jusqu'en 1971 puissances brutes (SAE gross). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .buick import FAMILLES as FAMILLES_BUICK
from .cadillac import FAMILLES as FAMILLES_CADILLAC
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET

E_, D = "ESS", "DSL"
C = "CHAINE"


def v8(t, l, rpm, nmrpm, c=E_):
    return f(t, c, l, C, 8, rpm, nmrpm, "10W30", 4.7, 5000, a="V")


OLDS = {
    "OLDS-CD-1.6": f("ATM", E_, 1.6, "NC", 1, 600, 500, "SAE30", 2.0, 1000),
    "OLDS-4CYL-2.7": f("ATM", E_, 2.7, "NC", 4, 1800, 1000, "SAE30", 4.0, 2000),
    "OLDS-V8-4.0": f("ATM", E_, 4.0, "NC", 8, 2600, 1200, "SAE30", 5.0, 2000, a="V"),
    "OLDS-L8-4.2": f("ATM", E_, 4.2, "NC", 8, 3400, 1600, "SAE30", 5.0, 3000),
    "OLDS-ROCKET-5.0": v8("ATM", 5.0, 3600, 1800), "OLDS-ROCKET-5.3": v8("ATM", 5.3, 4400, 2400), "OLDS-ROCKET-6.1": v8("ATM", 6.1, 4400, 2800),
    "OLDS-ROCKET-6.5": v8("ATM", 6.5, 4600, 3000), "OLDS-330-5.4": v8("ATM", 5.4, 4800, 3200), "OLDS-400-6.6": v8("ATM", 6.6, 4800, 3200),
    "OLDS-425-7.0": v8("ATM", 7.0, 4800, 3200), "OLDS-455-7.5": v8("ATM", 7.5, 4600, 3000), "OLDS-350-5.7": v8("ATM", 5.7, 4800, 2800),
    "OLDS-403-6.6": v8("ATM", 6.6, 3600, 2200), "OLDS-307-5.0": v8("ATM", 5.0, 4000, 2400), "OLDS-260-4.3": v8("ATM", 4.3, 3800, 2000),
    "OLDS-350D-5.7": v8("ATM", 5.7, 3600, 1600, c=D),
    "OLDS-AURORA-4.0": v8("ATM", 4.0, 5600, 4400),
    "GM-LD9-2.4": f("ATM", E_, 2.4, C, 4, 5600, 4400, "5W30", 3.8, 12000),
    "GM-LQ1-3.4": f("ATM", E_, 3.4, "COURROIE", 6, 5200, 4000, "5W30", 4.3, 12000, a="V"),
}
BUICK_PROPRES = {
    "BUICK-215-3.5": v8("ATM", 3.5, 4800, 2800), "BUICK-215T-3.5": v8("TURBO", 3.5, 4600, 3200),
    "BUICK-V6-3.7": f("ATM", E_, 3.7, C, 6, 4400, 2400, "10W30", 4.3, 5000, a="V"),
    "BUICK-V6-3.8": f("ATM", E_, 3.8, C, 6, 4000, 2000, "10W30", 4.3, 7500, a="V"),
    "BUICK-V6-4.1": f("ATM", E_, 4.1, C, 6, 4000, 2000, "10W30", 4.3, 7500, a="V"),
    "BUICK-V6-3.3": f("ATM", E_, 3.3, C, 6, 5200, 2000, "5W30", 4.3, 12000, a="V"),
}
BUICK = {k: FAMILLES_BUICK[k] for k in ("GM-3800", "GM-3800-SC", "GM-3.1", "GM-3.4", "GM-3.5", "GM-2.3-QUAD4", "GM-4.2-I6", "GM-5.3-V8")}
CHEVROLET = {k: FAMILLES_CHEVROLET[k] for k in ("SBC-5.7", "CHEVY-I6-4.1")}
CHEVROLET_PROPRES = {
    "VORTEC-4.3": f("ATM", E_, 4.3, C, 6, 4400, 2800, "5W30", 4.7, 7500, a="V"),
    "GM-J-2.0": f("ATM", E_, 2.0, C, 4, 5600, 3200, "10W30", 4.0, 7500),
    "GM-122-2.2": f("ATM", E_, 2.2, C, 4, 5200, 3600, "5W30", 4.0, 7500),
    "ECOTEC-2.2": f("ATM", E_, 2.2, C, 4, 5600, 4000, "5W30", 4.7, 12000),
}
CADILLAC = {"GM-V6-2.8": FAMILLES_CADILLAC["GM-V6-2.8"]}
PONTIAC = {"IRON-DUKE-2.5": f("ATM", E_, 2.5, "NC", 4, 4400, 2400, "10W30", 3.0, 7500)}
FAMILLES = {**OLDS, **BUICK_PROPRES, **BUICK, **CHEVROLET, **CHEVROLET_PROPRES, **CADILLAC, **PONTIAC}


def motoriste(fam):
    if fam in BUICK or fam in BUICK_PROPRES:
        return "Buick"
    if fam in CHEVROLET or fam in CHEVROLET_PROPRES or fam in CADILLAC:
        return "Chevrolet" if fam not in CADILLAC else "Cadillac"
    if fam in PONTIAC:
        return "Pontiac"
    return "Oldsmobile"


mg = SaisieMoteurs(FAMILLES, "Oldsmobile", motoriste)
L = []
NA = "Marché nord-américain"
IND = NA + " ; données indicatives"

# ---------------------------------------------------------------- débuts
mg(L, "Curved Dash", "Curved Dash", "1", "1901-01", "1907-12", [("1.6 5", "OLDS-CD-1.6", 20)], portes=0, places=2, reservoir=19,
   remarques="Monocylindre ; première voiture produite en grande série ; " + IND)
mg(L, "Model 20", "Model 20", "1", "1909-01", "1910-12", [("2.7 22", "OLDS-4CYL-2.7", 90)], portes=2, places=2, reservoir=40, remarques=IND)
mg(L, "Light Eight", "Model 45", "1", "1916-01", "1923-12", [("4.0 V8 41", "OLDS-V8-4.0", 160)], portes=4, places=5, reservoir=60, remarques=IND)

# ---------------------------------------------------------------- 88 / 98
mg(L, "98", "1941", "1", "1941-01", "1948-12", [("4.2 L8 112", "OLDS-L8-4.2", 285)], portes=4, places=6, reservoir=76,
   remarques="Huit cylindres en ligne ; production interrompue de 1942 à 1945 ; " + IND)
mg(L, "88", "1949", "1", "1949-01", "1953-12", [("5.0 V8 137", "OLDS-ROCKET-5.0", 359), ("5.0 V8 167", "OLDS-ROCKET-5.0", 380, {"debut": "1952-01"})],
   portes=4, places=6, reservoir=76, remarques="Premier V8 Rocket ; " + IND)
mg(L, "88", "1954", "1", "1954-01", "1956-12", [("5.3 V8 172", "OLDS-ROCKET-5.3", 400), ("5.3 V8 233", "OLDS-ROCKET-5.3", 474, {"debut": "1956-01"})],
   portes=4, places=6, reservoir=76, remarques=IND)
mg(L, "98", "1949", "1", "1949-01", "1956-12", [("5.0 V8 137", "OLDS-ROCKET-5.0", 359, {"fin": "1953-12"}), ("5.3 V8 243", "OLDS-ROCKET-5.3", 474, {"debut": "1954-01"})],
   portes=4, places=6, reservoir=76, remarques=IND)
mg(L, "88", "1957", "1", "1957-01", "1958-12", [("6.1 V8 281", "OLDS-ROCKET-6.1", 542)], portes=4, places=6, reservoir=76, remarques=IND)
mg(L, "88", "1959", "1", "1959-01", "1964-12", [("6.5 V8 254", "OLDS-ROCKET-6.5", 549), ("6.5 V8 335", "OLDS-ROCKET-6.5", 597)], portes=4, places=6, reservoir=79,
   remarques="Dynamic 88, Super 88, Jetstar 88 ; " + IND)
mg(L, "98", "1957", "1", "1957-01", "1964-12", [("6.1 V8 304", "OLDS-ROCKET-6.1", 556, {"fin": "1958-12"}), ("6.5 V8 335", "OLDS-ROCKET-6.5", 597, {"debut": "1959-01"})],
   portes=4, places=6, reservoir=79, remarques=IND)
mg(L, "Starfire", "1961", "1", "1961-01", "1966-12", [("6.5 V8 335", "OLDS-ROCKET-6.5", 597, {"fin": "1964-12"}), ("7.0 V8 380", "OLDS-425-7.0", 637, {"debut": "1965-01"})],
   portes=2, places=5, reservoir=79, remarques="Coupé et cabriolet ; " + IND)
mg(L, "88", "1965", "1", "1965-01", "1970-12", [("7.0 V8 314", "OLDS-425-7.0", 637), ("7.5 V8 370", "OLDS-455-7.5", 678, {"debut": "1968-01"})],
   portes=4, places=6, reservoir=95, remarques="Delta 88 à partir de 1965 ; " + IND)
mg(L, "98", "1965", "1", "1965-01", "1970-12", [("7.0 V8 365", "OLDS-425-7.0", 637), ("7.5 V8 370", "OLDS-455-7.5", 678, {"debut": "1968-01"})],
   portes=4, places=6, reservoir=95, remarques=IND)
mg(L, "88", "1971", "1", "1971-01", "1976-12", [("5.7 V8 162", "OLDS-350-5.7", 373), ("7.5 V8 193", "OLDS-455-7.5", 475)], portes=4, places=6, reservoir=95,
   remarques="Puissances nettes (SAE net) à partir de 1972 ; " + IND)
mg(L, "98", "1971", "1", "1971-01", "1976-12", [("7.5 V8 213", "OLDS-455-7.5", 488)], portes=4, places=6, reservoir=95, remarques=IND)
mg(L, "88", "1977", "1", "1977-01", "1985-12",
   [("4.3 V8 112", "OLDS-260-4.3", 278, {"fin": "1982-12"}), ("5.0 V8 142", "OLDS-307-5.0", 339, {"debut": "1980-01"}), ("5.7 V8 172", "OLDS-350-5.7", 373),
    ("6.6 V8 187", "OLDS-403-6.6", 434, {"fin": "1979-12"}), ("5.7 V8 Diesel 106", "OLDS-350D-5.7", 278, {"debut": "1978-01"})], portes=4, places=6, reservoir=95,
   remarques="Delta 88 (B-body) ; " + IND)
mg(L, "98", "1977", "1", "1977-01", "1984-12",
   [("5.7 V8 172", "OLDS-350-5.7", 373), ("6.6 V8 187", "OLDS-403-6.6", 434, {"fin": "1979-12"}), ("5.0 V8 142", "OLDS-307-5.0", 339, {"debut": "1980-01"}),
    ("5.7 V8 Diesel 106", "OLDS-350D-5.7", 278, {"debut": "1978-01"})], portes=4, places=6, reservoir=95, remarques="C-body propulsion ; " + IND)
mg(L, "98", "C-body", "1", "1985-01", "1990-12", [("3.0 V6 112", "BUICK-V6-3.8", 197, {"fin": "1985-12"}), ("3.8 V6 152", "GM-3800", 271), ("3.8 V6 167", "GM-3800", 285, {"debut": "1988-01"})],
   portes=4, places=6, reservoir=68, remarques="Ninety-Eight Regency, traction ; 3.0 V6 rattaché à la famille Buick V6 ; " + IND)
mg(L, "Touring Sedan", "C-body", "1", "1987-01", "1993-12", [("3.8 V6 152", "GM-3800", 271, {"fin": "1987-12"}), ("3.8 V6 167", "GM-3800", 285, {"debut": "1988-01"})],
   portes=4, places=5, reservoir=68, remarques="Ninety-Eight Touring Sedan ; " + IND)
mg(L, "98", "C-body (1991)", "1", "1991-01", "1996-12", [("3.8 V6 172", "GM-3800", 305), ("3.8 V6 208", "GM-3800", 312, {"debut": "1995-01"}),
                                                        ("3.8 V6 Supercharged 228", "GM-3800-SC", 373, {"debut": "1992-01"})],
   portes=4, places=6, reservoir=68, remarques="Regency Elite ; " + IND)
mg(L, "88", "H-body", "1", "1986-01", "1991-12", [("3.8 V6 152", "GM-3800", 271), ("3.8 V6 167", "GM-3800", 285, {"debut": "1988-01"})], portes=4, places=6, reservoir=68,
   remarques="Delta 88 traction ; " + IND)
mg(L, "88", "H-body", "2", "1992-01", "1999-12", [("3.8 V6 172", "GM-3800", 305), ("3.8 V6 208", "GM-3800", 312, {"debut": "1995-01"}),
                                                  ("LSS 3.8 V6 Supercharged 243", "GM-3800-SC", 380, {"debut": "1996-01"})],
   portes=4, places=6, reservoir=68, remarques="Eighty-Eight et LSS ; " + IND)

# ---------------------------------------------------------------- F-85 / Cutlass / 442
mg(L, "F-85", "Y-body", "1", "1961-01", "1963-12", [("3.5 V8 157", "BUICK-215-3.5", 285), ("3.5 V8 188", "BUICK-215-3.5", 312), ("Jetfire 3.5 V8 Turbo 218", "BUICK-215T-3.5", 407, {"debut": "1962-01"})],
   portes=4, places=5, reservoir=60, remarques="V8 aluminium 215 ; Jetfire : premier turbo de série avec la Corvair ; " + IND)
mg(L, "F-85", "A-body 1964", "1", "1964-01", "1967-12", [("3.7 V6 157", "BUICK-V6-3.7", 312), ("5.4 V8 254", "OLDS-330-5.4", 461)], portes=4, places=5, reservoir=76, remarques=IND)
mg(L, "Cutlass", "A-body 1964", "1", "1964-01", "1967-12", [("5.4 V8 294", "OLDS-330-5.4", 482), ("5.4 V8 325", "OLDS-330-5.4", 488)], portes=2, places=5, reservoir=76,
   remarques="Coupé, cabriolet et berline ; " + IND)
mg(L, "Cutlass", "A-body 1968", "1", "1968-01", "1972-12", [("5.7 V8 254", "OLDS-350-5.7", 481), ("5.7 V8 314", "OLDS-350-5.7", 488), ("7.5 V8 325", "OLDS-455-7.5", 678, {"debut": "1970-01"})],
   portes=2, places=5, reservoir=76, remarques="Cutlass Supreme dès 1966 ; " + IND)
mg(L, "Cutlass", "A-body 1973", "1", "1973-01", "1977-12", [("5.7 V8 182", "OLDS-350-5.7", 373), ("7.5 V8 254", "OLDS-455-7.5", 515, {"fin": "1976-12"}), ("4.3 V8 112", "OLDS-260-4.3", 278, {"debut": "1975-01"})],
   portes=2, places=5, reservoir=83, remarques="Colonnade ; puissances nettes ; " + IND)
mg(L, "442", "A-body 1964", "1", "1964-01", "1967-12", [("5.4 V8 314", "OLDS-330-5.4", 481, {"fin": "1964-12"}), ("6.6 V8 355", "OLDS-400-6.6", 597, {"debut": "1965-01"})],
   portes=2, places=5, reservoir=76, remarques="Option sportive des F-85 / Cutlass ; " + IND)
mg(L, "442", "A-body 1968", "1", "1968-01", "1972-12", [("6.6 V8 355", "OLDS-400-6.6", 597, {"fin": "1969-12"}), ("7.5 V8 370", "OLDS-455-7.5", 678, {"debut": "1970-01"}),
                                                        ("W-30 7.5 V8 375", "OLDS-455-7.5", 678, {"debut": "1970-01", "fin": "1971-12"})],
   portes=2, places=5, reservoir=76, remarques="Modèle à part entière de 1968 à 1971 ; " + IND)
mg(L, "442", "G-body", "1", "1985-01", "1987-12", [("5.0 V8 172", "OLDS-307-5.0", 339)], portes=2, places=5, reservoir=68, remarques="Cutlass Supreme 442 ; " + IND)
mg(L, "Vista Cruiser", "A-body 1964", "1", "1964-01", "1967-12", [("5.4 V8 254", "OLDS-330-5.4", 461)], portes=5, places=8, reservoir=76, remarques="Break à toit vitré ; " + IND)
mg(L, "Vista Cruiser", "A-body 1968", "1", "1968-01", "1972-12", [("5.7 V8 254", "OLDS-350-5.7", 481), ("7.5 V8 325", "OLDS-455-7.5", 678, {"debut": "1970-01"})],
   portes=5, places=8, reservoir=76, remarques=IND)
mg(L, "Vista Cruiser", "A-body 1973", "1", "1973-01", "1977-12", [("5.7 V8 182", "OLDS-350-5.7", 373)], portes=5, places=8, reservoir=83, remarques=IND)
mg(L, "Custom Cruiser", "B-body 1971", "1", "1971-01", "1976-12", [("7.5 V8 193", "OLDS-455-7.5", 475)], portes=5, places=9, reservoir=91, remarques=IND)
mg(L, "Custom Cruiser", "B-body 1977", "1", "1977-01", "1990-12", [("5.7 V8 172", "OLDS-350-5.7", 373, {"fin": "1985-12"}), ("5.0 V8 142", "OLDS-307-5.0", 339, {"debut": "1980-01"}),
                                                                   ("5.7 V8 Diesel 106", "OLDS-350D-5.7", 278, {"debut": "1978-01", "fin": "1985-12"})],
   portes=5, places=8, reservoir=83, remarques=IND)
mg(L, "Custom Cruiser", "B-body 1991", "1", "1991-01", "1992-12", [("5.7 V8 182", "SBC-5.7", 407)], portes=5, places=8, reservoir=83, remarques=IND)

# ---------------------------------------------------------------- Toronado
mg(L, "Toronado", "E-body 1966", "1", "1966-01", "1970-12", [("7.0 V8 390", "OLDS-425-7.0", 645), ("7.5 V8 380", "OLDS-455-7.5", 678, {"debut": "1968-01"})],
   portes=2, places=5, reservoir=91, remarques="Traction ; " + IND)
mg(L, "Toronado", "E-body 1971", "1", "1971-01", "1978-12", [("7.5 V8 254", "OLDS-455-7.5", 515, {"fin": "1976-12"}), ("6.6 V8 187", "OLDS-403-6.6", 434, {"debut": "1977-01"})],
   portes=2, places=5, reservoir=98, remarques=IND)
mg(L, "Toronado", "E-body 1979", "1", "1979-01", "1985-12", [("5.7 V8 172", "OLDS-350-5.7", 373, {"fin": "1980-12"}), ("5.0 V8 142", "OLDS-307-5.0", 339, {"debut": "1980-01"}),
                                                              ("4.1 V6 127", "BUICK-V6-4.1", 278, {"debut": "1981-01", "fin": "1984-12"}), ("5.7 V8 Diesel 106", "OLDS-350D-5.7", 278)],
   portes=2, places=5, reservoir=79, remarques=IND)
mg(L, "Toronado", "E-body 1986", "1", "1986-01", "1992-12", [("3.8 V6 142", "GM-3800", 271, {"fin": "1987-12"}), ("3.8 V6 167", "GM-3800", 285, {"debut": "1988-01", "fin": "1990-12"}),
                                                              ("3.8 V6 172", "GM-3800", 305, {"debut": "1991-01"})], portes=2, places=5, reservoir=70, remarques="Dont Trofeo ; " + IND)

# ---------------------------------------------------------------- compactes
mg(L, "Omega", "X-body 1973", "1", "1973-01", "1979-12", [("4.1 I6 101", "CHEVY-I6-4.1", 237), ("5.7 V8 172", "OLDS-350-5.7", 373)], portes=4, places=5, reservoir=79,
   remarques="Propulsion, base Chevrolet Nova ; " + IND)
mg(L, "Omega", "X-body 1980", "1", "1980-01", "1984-12", [("2.5 91", "IRON-DUKE-2.5", 182), ("2.8 V6 112", "GM-V6-2.8", 197), ("2.8 V6 HO 137", "GM-V6-2.8", 197, {"debut": "1981-01"})],
   portes=4, places=5, reservoir=53, remarques="Traction ; " + IND)
mg(L, "Firenza", "J-body", "1", "1982-01", "1988-12", [("1.8 89", "GM-J-2.0", 134, {"fin": "1986-12"}), ("2.0 91", "GM-J-2.0", 149), ("2.8 V6 132", "GM-V6-2.8", 230, {"debut": "1985-01"})],
   portes=3, places=5, reservoir=53, remarques="Berline, coupé et break ; 1.8 rattaché à la famille 2.0 ; " + IND)
mg(L, "Cutlass Ciera", "A-body 1982", "1", "1982-01", "1996-12",
   [("2.5 99", "IRON-DUKE-2.5", 183, {"fin": "1992-12"}), ("2.8 V6 127", "GM-V6-2.8", 197, {"fin": "1989-12"}), ("3.8 V6 152", "BUICK-V6-3.8", 271, {"debut": "1984-01", "fin": "1988-12"}),
    ("3.3 V6 162", "BUICK-V6-3.3", 251, {"debut": "1989-01", "fin": "1993-12"}), ("2.2 122", "GM-122-2.2", 176, {"debut": "1992-01"}), ("3.1 V6 162", "GM-3.1", 251, {"debut": "1994-01"})],
   portes=4, places=6, reservoir=59, remarques="Berline, coupé et break Cruiser ; " + IND)
mg(L, "Cutlass Calais", "N-body", "1", "1985-01", "1991-12",
   [("2.5 93", "IRON-DUKE-2.5", 183, {"fin": "1991-12"}), ("3.0 V6 127", "BUICK-V6-3.8", 197, {"fin": "1988-12"}), ("2.3 Quad 4 152", "GM-2.3-QUAD4", 217, {"debut": "1988-01"}),
    ("442 2.3 Quad 4 W41 193", "GM-2.3-QUAD4", 217, {"debut": "1990-01"}), ("3.3 V6 162", "BUICK-V6-3.3", 251, {"debut": "1989-01"})],
   portes=2, places=5, reservoir=51, remarques="Coupé et berline ; 3.0 V6 rattaché à la famille Buick V6 ; " + IND)
mg(L, "Achieva", "N-body 1992", "1", "1992-01", "1998-12",
   [("2.3 Quad 4 117", "GM-2.3-QUAD4", 190), ("2.3 Quad 4 162", "GM-2.3-QUAD4", 217, {"fin": "1995-12"}), ("SCX 2.3 Quad 4 193", "GM-2.3-QUAD4", 217, {"fin": "1993-12"}),
    ("3.3 V6 162", "BUICK-V6-3.3", 251, {"fin": "1993-12"}), ("3.1 V6 157", "GM-3.1", 251, {"debut": "1994-01"}), ("2.4 Twin Cam 152", "GM-LD9-2.4", 210, {"debut": "1996-01"})],
   portes=4, places=5, reservoir=57, remarques="Coupé et berline ; " + IND)
mg(L, "Alero", "N-body 1999", "1", "1999-01", "2004-12",
   [("2.4 Twin Cam 152", "GM-LD9-2.4", 210, {"fin": "2001-12"}), ("2.2 Ecotec 142", "ECOTEC-2.2", 203, {"debut": "2002-01"}), ("3.4 V6 172", "GM-3.4", 271)],
   portes=4, places=5, reservoir=57, remarques="Coupé et berline ; dernière Oldsmobile produite ; " + IND)

# ---------------------------------------------------------------- W-body
mg(L, "Cutlass Supreme", "W-body", "1", "1988-01", "1997-12",
   [("2.8 V6 132", "GM-V6-2.8", 230, {"fin": "1989-12"}), ("3.1 V6 142", "GM-3.1", 251, {"debut": "1989-01", "fin": "1993-12"}), ("3.1 V6 162", "GM-3.1", 251, {"debut": "1994-01"}),
    ("2.3 Quad 4 182", "GM-2.3-QUAD4", 217, {"debut": "1990-01", "fin": "1991-12"}), ("3.4 V6 DOHC 213", "GM-LQ1-3.4", 292, {"debut": "1991-01"})],
   portes=2, places=5, reservoir=62, remarques="Coupé, berline et cabriolet ; " + IND)
mg(L, "Intrigue", "W-body 1998", "1", "1998-01", "2002-12", [("3.8 V6 198", "GM-3800", 312, {"fin": "1999-12"}), ("3.5 V6 218", "GM-3.5", 312, {"debut": "1999-01"})],
   portes=4, places=5, reservoir=65, remarques="3.5 V6 « Shortstar » ; " + IND)
mg(L, "Aurora", "G-body 1995", "1", "1995-01", "1999-12", [("4.0 V8 254", "OLDS-AURORA-4.0", 353)], portes=4, places=5, reservoir=76, remarques=IND)
mg(L, "Aurora", "G-body 2001", "1", "2001-01", "2003-12", [("3.5 V6 218", "GM-3.5", 312), ("4.0 V8 254", "OLDS-AURORA-4.0", 353)], portes=4, places=5, reservoir=70, remarques=IND)

# ---------------------------------------------------------------- monospace et SUV
mg(L, "Silhouette", "U-body", "1", "1990-01", "1996-12", [("3.1 V6 122", "GM-3.1", 217, {"fin": "1991-12"}), ("3.8 V6 172", "GM-3800", 305, {"debut": "1992-01", "fin": "1995-12"}),
                                                          ("3.4 V6 182", "GM-3.4", 278, {"debut": "1996-01"})], portes=3, places=7, reservoir=76, remarques=IND)
mg(L, "Silhouette", "U-body 1997", "1", "1997-01", "2004-12", [("3.4 V6 187", "GM-3.4", 285)], portes=4, places=7, reservoir=95, remarques=IND)
mg(L, "Bravada", "S-body", "1", "1991-01", "1994-12", [("4.3 V6 162", "VORTEC-4.3", 312), ("4.3 V6 203", "VORTEC-4.3", 353, {"debut": "1992-01"})], portes=5, places=5, reservoir=76,
   remarques="Transmission intégrale ; " + IND)
mg(L, "Bravada", "S-body", "2", "1996-01", "2001-12", [("4.3 V6 193", "VORTEC-4.3", 339)], portes=5, places=5, reservoir=68, remarques=IND)
mg(L, "Bravada", "GMT360", "1", "2002-01", "2004-12", [("4.2 I6 274", "GM-4.2-I6", 373), ("5.3 V8 294", "GM-5.3-V8", 441, {"debut": "2003-01"})], portes=5, places=5, reservoir=83,
   remarques=IND)

MOT = Motorisations("Oldsmobile", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Oldsmobile": L}
MOTEURS = MOT.moteurs()
