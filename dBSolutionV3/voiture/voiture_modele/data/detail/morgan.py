"""Morgan et Morgan Aero : générations, phases, motorisations (marché européen) et moteurs liés.
Morgan : 4/4, Plus 4, Plus 4 Plus, Plus 8 (1968-2004 et 2012-2018), Roadster, 3 Wheeler, Super 3, Plus Six, Plus Four,
Midsummer, Supersport (dont Supersport 400). Morgan Aero : Aero 8 (Series I à V), AeroMax, Aero SuperSports, Aero Coupe, Aero GT.
Moteurs Ford repris de ford.py / caterham.py / ginetta.py, Rover de land_rover.py / ginetta.py, BMW de bmw.py / mini.py
(mêmes codes) ; moteurs Coventry Climax, Standard, Triumph, Fiat, Rover M16, S&S et Ford 1.5 Dragon ajoutés.
Données anciennes indicatives. Plus Four CX-T (8 ex.) et Plus 8 GTR (9 ex.) non repris.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .bmw import FAMILLES as FAMILLES_BMW
from .caterham import FAMILLES as FAMILLES_CATERHAM
from .ford import FAMILLES as FAMILLES_FORD
from .ginetta import FAMILLES as FAMILLES_GINETTA
from .land_rover import FAMILLES as FAMILLES_LR

E_ = "ESS"
C, B = "CHAINE", "COURROIE"

AUTRES = {
    "CLIMAX-1.1": f("ATM", E_, 1.1, C, 4, 4000, 2500, "20W50", 4.0, 3000),
    "STANDARD-1.3": f("ATM", E_, 1.3, C, 4, 4500, 2500, "20W50", 4.0, 3000),
    "STANDARD-2.1": f("ATM", E_, 2.1, C, 4, 4200, 2000, "20W50", 5.0, 5000),
    "TRIUMPH-TR-2.0": f("ATM", E_, 2.0, C, 4, 4800, 3000, "20W50", 5.0, 5000),
    "TRIUMPH-TR-2.1": f("ATM", E_, 2.1, C, 4, 4600, 3350, "20W50", 5.0, 5000),
    "FIAT-TC-1.6": f("ATM", E_, 1.6, B, 4, 6000, 3800, "10W40", 4.5, 10000),
    "FIAT-TC-2.0": f("ATM", E_, 2.0, B, 4, 5300, 3500, "10W40", 4.5, 10000),
    "ROVER-M16-2.0": f("ATM", E_, 2.0, B, 4, 6000, 4500, "10W40", 4.5, 10000),
    "SS-VTWIN-2.0": f("ATM", E_, 2.0, "NC", 2, 5250, 3250, "20W50", 3.0, 8000, a="V"),
    "DRAGON-1.5": f("ATM", E_, 1.5, C, 3, 6500, 4500, "5W20", 4.0, 10000),
    "DURATEC30-3.0": f("ATM", E_, 3.0, C, 6, 6000, 4900, "5W30", 5.7, 15000, a="V"),
}
FORD = {**{k: FAMILLES_FORD[k] for k in ("CVH-1.6", "ZETEC-1.8", "SIGMA-1.6", "DURATEC-HE-1.8")},
        **{k: FAMILLES_CATERHAM[k] for k in ("KENT-1.6", "DURATEC-2.0")}, **{k: FAMILLES_GINETTA[k] for k in ("KENT-1.5", "CYCLONE-3.7")},
        "FORD-SV-1.2": f("ATM", E_, 1.2, C, 4, 4500, 2300, "20W50", 3.5, 3000)}
FORD["DRAGON-1.5"] = AUTRES.pop("DRAGON-1.5")
FORD["DURATEC30-3.0"] = AUTRES.pop("DURATEC30-3.0")
ROVER = {**{k: FAMILLES_LR[k] for k in ("ROVER-V8-3.5", "ROVER-V8-4.6", "ROVER-T16-2.0")}, "ROVER-V8-3.9": FAMILLES_GINETTA["ROVER-V8-3.9"],
         "ROVER-M16-2.0": AUTRES.pop("ROVER-M16-2.0")}
BMW = {k: FAMILLES_BMW[k] for k in ("N62-4.4", "N62-4.8", "B58-3.0", "B48A20")}
FAMILLES = {**AUTRES, **FORD, **ROVER, **BMW}


def motoriste(fam):
    if fam in FORD:
        return "Ford"
    if fam in ROVER:
        return "Rover"
    if fam in BMW:
        return "BMW"
    return {"CLIMAX-1.1": "Coventry Climax", "STANDARD-1.3": "Standard", "STANDARD-2.1": "Standard", "TRIUMPH-TR-2.0": "Triumph",
            "TRIUMPH-TR-2.1": "Triumph", "FIAT-TC-1.6": "Fiat", "FIAT-TC-2.0": "Fiat", "SS-VTWIN-2.0": "S&S"}[fam]


mg = SaisieMoteurs(FAMILLES, "Morgan", motoriste)
L, AERO = [], []
IND = "données indicatives"

# ---------------------------------------------------------------- 4/4
mg(L, "4/4", "Series I", "1", "1936-01", "1950-12", [("1.1 34", "CLIMAX-1.1", 68, {"fin": "1939-12"}), ("1.3 39", "STANDARD-1.3", 80, {"debut": "1939-01"})],
   portes=2, places=2, reservoir=36, remarques="Roadster 2 et 4 places, coupé ; production interrompue pendant la guerre ; " + IND)
mg(L, "4/4", "Series II-V", "1", "1955-10", "1968-02", [("1.2 36", "FORD-SV-1.2", 72, {"fin": "1960-12"}), ("1.5 65", "KENT-1.5", 110, {"debut": "1961-01"})],
   portes=2, places=2, reservoir=36, remarques="Moteurs Ford (side-valve, puis Kent 1.0 à 1.5) ; " + IND)
mg(L, "4/4", "1600", "1", "1968-02", "1982-12", [("1.6 96", "KENT-1.6", 125)], portes=2, places=2, reservoir=39, remarques="2 et 4 places ; " + IND)
mg(L, "4/4", "1600", "2", "1981-06", "1993-06", [("1.6 TC 98", "FIAT-TC-1.6", 131, {"fin": "1985-12"}), ("1.6 CVH 96", "CVH-1.6", 132, {"debut": "1982-06"})],
   portes=2, places=2, reservoir=39, remarques=IND)
mg(L, "4/4", "1800", "1", "1993-07", "2004-06", [("1.8 Zetec 114", "ZETEC-1.8", 160)], portes=2, places=2, reservoir=55, remarques=IND)
mg(L, "4/4", "1800", "2", "2004-07", "2009-06", [("1.8 Duratec 125", "DURATEC-HE-1.8", 165)], portes=2, places=2, reservoir=55, remarques=IND)
mg(L, "4/4", "Sigma", "1", "2009-07", "2018-12", [("1.6 Sigma 110", "SIGMA-1.6", 140)], portes=2, places=2, reservoir=55, remarques="Dont 4/4 80th Anniversary")

# ---------------------------------------------------------------- Plus 4
mg(L, "Plus 4", "Plus 4", "1", "1950-09", "1969-06",
   [("Vanguard 2.1 68", "STANDARD-2.1", 155, {"fin": "1958-12"}), ("TR2 2.0 90", "TRIUMPH-TR-2.0", 159, {"debut": "1954-01", "fin": "1958-12"}),
    ("TR3/TR4 2.1 105", "TRIUMPH-TR-2.1", 172, {"debut": "1958-01"})], portes=2, places=2, reservoir=50, remarques="2 et 4 places, coupé ; " + IND)
mg(L, "Plus 4 Plus", "Plus 4 Plus", "1", "1964-10", "1967-12", [("TR4 2.1 105", "TRIUMPH-TR-2.1", 172)], portes=2, places=2, reservoir=50,
   remarques="Coupé à carrosserie en fibre de verre, 26 exemplaires ; " + IND)
mg(L, "Plus 4", "Plus 4 (1985)", "1", "1985-01", "2000-12",
   [("Fiat TC 2.0 122", "FIAT-TC-2.0", 167, {"fin": "1987-12"}), ("Rover M16 2.0 138", "ROVER-M16-2.0", 178, {"debut": "1988-01", "fin": "1992-06"}),
    ("Rover T16 2.0 134", "ROVER-T16-2.0", 185, {"debut": "1992-07"})], portes=2, places=2, reservoir=55, remarques=IND)
mg(L, "Plus 4", "Plus 4 (2005)", "1", "2005-01", "2020-02", [("2.0 Duratec 145", "DURATEC-2.0", 190, {"fin": "2009-06"}), ("2.0 Duratec 154", "DURATEC-2.0", 201, {"debut": "2009-07"})],
   portes=2, places=2, reservoir=55, remarques="2 et 4 places ; " + IND)

# ---------------------------------------------------------------- Plus 8 / Roadster
mg(L, "Plus 8", "Plus 8", "1", "1968-09", "2004-06",
   [("3.5 V8 160", "ROVER-V8-3.5", 285, {"fin": "1972-12"}), ("3.5 V8 155", "ROVER-V8-3.5", 271, {"debut": "1973-01", "fin": "1983-12"}),
    ("3.5 V8 Injection 190", "ROVER-V8-3.5", 298, {"debut": "1984-01", "fin": "1990-06"}), ("3.9 V8 190", "ROVER-V8-3.9", 319, {"debut": "1990-07"}),
    ("4.6 V8 220", "ROVER-V8-4.6", 353, {"debut": "1997-01"})], portes=2, places=2, reservoir=55, remarques=IND)
mg(L, "Plus 8", "Plus 8 (2012)", "1", "2012-03", "2018-12", [("4.8 V8 367", "N62-4.8", 490)], portes=2, places=2, reservoir=55,
   remarques="Châssis aluminium Aero ; dernières Plus 8 produites en 2018")
mg(L, "Roadster", "Roadster", "1", "2004-01", "2011-06", [("3.0 V6 223", "DURATEC30-3.0", 280)], portes=2, places=2, reservoir=55, remarques="2 et 4 places")
mg(L, "Roadster", "Roadster", "2", "2011-07", "2019-12", [("3.7 V6 284", "CYCLONE-3.7", 380)], portes=2, places=2, reservoir=55, remarques="2 et 4 places")

# ---------------------------------------------------------------- tricycles
mg(L, "3 Wheeler", "3 Wheeler", "1", "2011-06", "2021-12", [("2.0 V-twin 82", "SS-VTWIN-2.0", 140)], portes=0, places=2, reservoir=40,
   remarques="Tricycle, moteur S&S ; " + IND)
mg(L, "Super 3", "Super 3", "1", "2022-02", None, [("1.5 118", "DRAGON-1.5", 150)], portes=0, places=1, reservoir=30,
   remarques="Tricycle, moteur Ford 1.5 trois cylindres")

# ---------------------------------------------------------------- CX
mg(L, "Plus Six", "CX", "1", "2019-03", "2025-03", [("3.0 340", "B58-3.0", 500)], portes=2, places=2, reservoir=55,
   remarques="Remplacée par le Supersport")
mg(L, "Plus Four", "CX", "1", "2020-03", "2025-02", [("2.0 255", "B48A20", 350)], portes=2, places=2, reservoir=55,
   remarques="Couple 350 Nm (boîte manuelle), 400 Nm en automatique")
mg(L, "Plus Four", "CX", "2", "2025-03", None, [("2.0 255", "B48A20", 350)], portes=2, places=2, reservoir=55,
   remarques="Mise à jour ; couple 350 Nm (boîte manuelle), 400 Nm en automatique")
mg(L, "Midsummer", "CX", "1", "2024-03", "2025-12", [("3.0 340", "B58-3.0", 500)], portes=2, places=2, reservoir=55,
   remarques="Barquette produite à 50 exemplaires (Pininfarina) ; " + IND)
mg(L, "Supersport", "CXV", "1", "2025-03", None, [("3.0 340", "B58-3.0", 500), ("400 3.0 408", "B58-3.0", 500, {"debut": "2026-05"})],
   portes=2, places=2, reservoir=55, remarques="Successeur de la Plus Six ; Supersport 400 (moteur B58 O1)")

# ---------------------------------------------------------------- Morgan Aero
mg(AERO, "Aero 8", "Series I", "1", "2001-03", "2004-06", [("4.4 V8 286", "N62-4.4", 440)], portes=2, places=2, reservoir=55, remarques=IND)
mg(AERO, "Aero 8", "Series II-III", "1", "2004-07", "2007-06", [("4.4 V8 325", "N62-4.4", 450)], portes=2, places=2, reservoir=55, remarques=IND)
mg(AERO, "Aero 8", "Series IV", "1", "2007-07", "2009-12", [("4.8 V8 367", "N62-4.8", 490)], portes=2, places=2, reservoir=55)
mg(AERO, "Aero 8", "Series V", "1", "2015-03", "2018-12", [("4.8 V8 367", "N62-4.8", 490)], portes=2, places=2, reservoir=55)
mg(AERO, "AeroMax", "AeroMax", "1", "2008-03", "2009-12", [("4.8 V8 367", "N62-4.8", 490)], portes=2, places=2, reservoir=55, remarques="Coupé, 100 exemplaires")
mg(AERO, "Aero SuperSports", "SuperSports", "1", "2010-03", "2015-12", [("4.8 V8 367", "N62-4.8", 490)], portes=2, places=2, reservoir=60, remarques="Targa")
mg(AERO, "Aero Coupe", "Aero Coupe", "1", "2012-03", "2015-12", [("4.8 V8 367", "N62-4.8", 490)], portes=2, places=2, reservoir=60)
mg(AERO, "Aero GT", "Aero GT", "1", "2018-03", "2018-12", [("4.8 V8 367", "N62-4.8", 490)], portes=2, places=2, reservoir=60, remarques="8 exemplaires")

MOT = Motorisations("Morgan", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(AERO)

DETAIL = {"Morgan": L, "Morgan Aero": AERO}
MOTEURS = MOT.moteurs()
