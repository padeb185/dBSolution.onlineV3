"""Triumph : générations, phases, motorisations (marché européen) et moteurs liés.
TR2, TR3, TR4 / TR4A, TR5 / TR250, TR6, TR7, TR8, Herald, Vitesse, Spitfire, GT6, 2000 / 2500, Toledo, Dolomite, Stag et Acclaim.
Marque automobile arrêtée en 1984 (les motos Triumph sont une autre entreprise).
Quatre cylindres TR repris de morgan.py, 1.5 de mg.py, V8 Rover de land_rover.py, Honda 1.3 de rover.py (mêmes codes) ;
moteurs Standard / Triumph SC, six cylindres, Slant-4 et V8 Stag ajoutés. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .land_rover import FAMILLES as FAMILLES_LR
from .mg import FAMILLES as FAMILLES_MG
from .morgan import FAMILLES as FAMILLES_MORGAN
from .rover import FAMILLES as FAMILLES_ROVER

E_ = "ESS"
C = "CHAINE"


def t(l, n, rpm, nmrpm, q=4.5, a="EN_LIGNE"):
    return f("ATM", E_, l, C, n, rpm, nmrpm, "20W50", q, 5000, a=a)


TRIUMPH_PROPRES = {
    "TRIUMPH-SC-0.95": t(0.95, 4, 5500, 3000, 3.5), "TRIUMPH-SC-1.15": t(1.15, 4, 5500, 3000, 3.5), "TRIUMPH-SC-1.3": t(1.3, 4, 6000, 3500, 3.5),
    "TRIUMPH-L6-1.6": t(1.6, 6, 5000, 2800, 4.8), "TRIUMPH-L6-2.0": t(2.0, 6, 5300, 3000, 4.8), "TRIUMPH-L6-2.5": t(2.5, 6, 5500, 3500, 4.8),
    "TRIUMPH-SLANT-1.85": t(1.85, 4, 5200, 3500, 4.0), "TRIUMPH-SLANT-2.0": t(2.0, 4, 5500, 3500, 4.0), "TRIUMPH-SLANT-2.0-16V": t(2.0, 4, 5700, 4500, 4.0),
    "TRIUMPH-V8-3.0": t(3.0, 8, 5500, 3500, 5.0, a="V"),
}
TRIUMPH = {**TRIUMPH_PROPRES, **{k: FAMILLES_MORGAN[k] for k in ("TRIUMPH-TR-2.0", "TRIUMPH-TR-2.1")}, "TRIUMPH-1.5": FAMILLES_MG["TRIUMPH-1.5"]}
ROVER = {"ROVER-V8-3.5": FAMILLES_LR["ROVER-V8-3.5"]}
HONDA = {"HONDA-EV-1.3": FAMILLES_ROVER["HONDA-EV-1.3"]}
FAMILLES = {**TRIUMPH, **ROVER, **HONDA}


def motoriste(fam):
    if fam in ROVER:
        return "Rover"
    if fam in HONDA:
        return "Honda"
    return "Triumph"


mg = SaisieMoteurs(FAMILLES, "Triumph", motoriste)
L = []
IND = "données indicatives"

# ---------------------------------------------------------------- TR
mg(L, "TR2", "TR2", "1", "1953-08", "1955-10", [("2.0 90", "TRIUMPH-TR-2.0", 159)], portes=2, places=2, reservoir=57, remarques="Roadster ; " + IND)
mg(L, "TR3", "TR3", "1", "1955-10", "1962-10", [("2.0 95", "TRIUMPH-TR-2.0", 159, {"fin": "1956-12"}), ("2.0 100", "TRIUMPH-TR-2.0", 159, {"debut": "1957-01"})],
   portes=2, places=2, reservoir=57, remarques="TR3, TR3A et TR3B ; " + IND)
mg(L, "TR4", "TR4", "1", "1961-08", "1967-12", [("2.1 105", "TRIUMPH-TR-2.1", 172)], portes=2, places=2, reservoir=53, remarques="TR4 et TR4A (suspension arrière indépendante, 1965) ; " + IND)
mg(L, "TR5", "TR5", "1", "1967-08", "1968-09", [("2.5 PI 152", "TRIUMPH-L6-2.5", 222), ("TR250 2.5 106", "TRIUMPH-L6-2.5", 194, {"remarques": "TR250 à carburateurs (Amérique du Nord)"})],
   portes=2, places=2, reservoir=51, remarques="Six cylindres à injection (PI) ; " + IND)
mg(L, "TR6", "TR6", "1", "1968-11", "1976-07", [("2.5 PI 152", "TRIUMPH-L6-2.5", 222, {"fin": "1972-12"}), ("2.5 PI 126", "TRIUMPH-L6-2.5", 194, {"debut": "1973-01"}),
                                                ("2.5 106", "TRIUMPH-L6-2.5", 194, {"remarques": "Version carburateurs (Amérique du Nord)"})],
   portes=2, places=2, reservoir=51, remarques=IND)
mg(L, "TR7", "TR7", "1", "1975-01", "1981-10", [("2.0 105", "TRIUMPH-SLANT-2.0", 162)], portes=2, places=2, reservoir=55, remarques="Coupé puis cabriolet (1979) ; " + IND)
mg(L, "TR8", "TR7", "2", "1978-01", "1981-10", [("3.5 V8 137", "ROVER-V8-3.5", 224)], portes=2, places=2, reservoir=55, remarques="TR7 à V8 Rover, surtout Amérique du Nord ; " + IND)

# ---------------------------------------------------------------- petites Triumph
mg(L, "Herald", "Herald", "1", "1959-04", "1971-05",
   [("948 0.95 35", "TRIUMPH-SC-0.95", 66, {"fin": "1961-06"}), ("948 S 0.95 45", "TRIUMPH-SC-0.95", 69, {"fin": "1961-06"}), ("1200 1.15 39", "TRIUMPH-SC-1.15", 82, {"debut": "1961-04"}),
    ("12/50 1.15 51", "TRIUMPH-SC-1.15", 85, {"debut": "1963-03", "fin": "1967-12"}), ("13/60 1.3 61", "TRIUMPH-SC-1.3", 99, {"debut": "1967-10"})],
   portes=2, places=4, reservoir=32, remarques="Berline, coupé, cabriolet, break et Courier ; " + IND)
mg(L, "Vitesse", "Vitesse", "1", "1962-05", "1971-07", [("1.6 L6 71", "TRIUMPH-L6-1.6", 125, {"fin": "1966-09"}), ("2-Litre 2.0 L6 96", "TRIUMPH-L6-2.0", 159, {"debut": "1966-09", "fin": "1968-09"}),
                                                       ("Mk2 2.0 L6 105", "TRIUMPH-L6-2.0", 159, {"debut": "1968-10"})], portes=2, places=4, reservoir=40, remarques="Six cylindres sur base Herald ; " + IND)
mg(L, "Spitfire", "Spitfire", "1", "1962-10", "1980-08",
   [("Mk1/2 1.15 63", "TRIUMPH-SC-1.15", 91, {"fin": "1967-01"}), ("Mk3 1.3 75", "TRIUMPH-SC-1.3", 102, {"debut": "1967-01", "fin": "1970-10"}),
    ("Mk IV 1.3 63", "TRIUMPH-SC-1.3", 94, {"debut": "1970-11", "fin": "1974-12"}), ("1500 1.5 71", "TRIUMPH-1.5", 111, {"debut": "1974-12"})],
   portes=2, places=2, reservoir=37, remarques="Roadster ; " + IND)
mg(L, "GT6", "GT6", "1", "1966-07", "1973-12", [("2.0 L6 96", "TRIUMPH-L6-2.0", 159, {"fin": "1968-09"}), ("Mk2 / Mk3 2.0 L6 105", "TRIUMPH-L6-2.0", 159, {"debut": "1968-10"})],
   portes=3, places=2, reservoir=44, remarques="Coupé fastback sur base Spitfire ; " + IND)

# ---------------------------------------------------------------- berlines
mg(L, "2000", "2000 / 2500", "1", "1963-10", "1977-05",
   [("2000 2.0 L6 91", "TRIUMPH-L6-2.0", 159), ("2.5 PI 2.5 L6 133", "TRIUMPH-L6-2.5", 207, {"debut": "1968-10", "fin": "1975-06"}), ("2500 S 2.5 L6 107", "TRIUMPH-L6-2.5", 189, {"debut": "1974-01"})],
   portes=4, places=5, reservoir=64, remarques="Triumph 2000, 2.5 PI, 2500 TC / S ; berline et break ; " + IND)
mg(L, "Toledo", "Toledo", "1", "1970-08", "1976-03", [("1.3 59", "TRIUMPH-SC-1.3", 99), ("1.5 65", "TRIUMPH-1.5", 107)], portes=4, places=5, reservoir=52, remarques="Propulsion ; " + IND)
mg(L, "Dolomite", "Dolomite", "1", "1972-01", "1980-08",
   [("1300 1.3 59", "TRIUMPH-SC-1.3", 99, {"debut": "1976-03"}), ("1500 1.5 71", "TRIUMPH-1.5", 111, {"debut": "1976-03"}), ("1850 1.85 92", "TRIUMPH-SLANT-1.85", 142),
    ("Sprint 2.0 16V 129", "TRIUMPH-SLANT-2.0-16V", 169, {"debut": "1973-06"})], portes=4, places=5, reservoir=57,
   remarques="Dont Dolomite Sprint (première culasse 16 soupapes de grande série) ; " + IND)
mg(L, "Stag", "Stag", "1", "1970-06", "1977-12", [("3.0 V8 147", "TRIUMPH-V8-3.0", 230)], portes=2, places=4, reservoir=64, remarques="Cabriolet 2+2 à arceau ; " + IND)
mg(L, "Acclaim", "Acclaim", "1", "1981-10", "1984-06", [("1.3 70", "HONDA-EV-1.3", 101)], portes=4, places=5, reservoir=48,
   remarques="Base Honda Ballade, dernière voiture Triumph ; " + IND)

MOT = Motorisations("Triumph", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Triumph": L}
MOTEURS = MOT.moteurs()
