"""International Harvester (Chicago) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Auto Buggy (high wheeler, 1907-1911), Travelall (1953-1975), Scout 80 / 800 / II (1961-1980) et pick-up Light Line (1969-1975).
Camions lourds sous la marque International (voir international.py). Diesel Nissan SD33 du Scout II ajouté.
Puissances brutes jusqu'en 1971, nettes ensuite, converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_, D, C = "ESS", "DSL", "CHAINE"


def v8(l):
    return f("ATM", E_, l, C, 8, 4400, 2400, "10W30", 5.7, 5000, a="V")


FAMILLES = {
    "IH-B2-2.6": f("ATM", E_, 2.6, "NC", 2, 1200, 800, "SAE30", 2.0, 1000, a="PLAT"),
    "IH-BD240-3.9": f("ATM", E_, 3.9, "NC", 6, 3800, 2000, "SAE30", 5.7, 3000),
    "IH-COMANCHE-2.5": f("ATM", E_, 2.5, "NC", 4, 4400, 2400, "10W30", 4.7, 5000),
    "IH-COMANCHE-3.2": f("ATM", E_, 3.2, "NC", 4, 4000, 2400, "10W30", 4.7, 5000),
    "IH-V8-4.4": v8(4.4), "IH-V8-5.0": v8(5.0), "IH-V8-5.6": v8(5.6), "IH-V8-6.4": v8(6.4),
    "NISSAN-SD33-3.3D": f("ATM", D, 3.3, "NC", 6, 4000, 2000, "15W40", 6.0, 5000),
    "NISSAN-SD33T-3.3TD": f("TURBO", D, 3.3, "NC", 6, 3800, 2200, "15W40", 6.0, 5000),
}
mg = SaisieMoteurs(FAMILLES, "International Harvester", lambda fam: "Nissan" if fam.startswith("NISSAN") else "International Harvester")
L = []
IND = "marché nord-américain ; données indicatives"

mg(L, "Auto Buggy", "Auto Buggy", "1", "1907-01", "1911-12", [("2.6 14", "IH-B2-2.6", 60)], portes=0, places=2, reservoir=25,
   remarques="High wheeler à bicylindre à plat refroidi par air ; " + IND)
mg(L, "Travelall", "Travelall", "1", "1953-01", "1975-12",
   [("3.9 L6 142", "IH-BD240-3.9", 305, {"fin": "1968-12"}), ("4.4 V8 157", "IH-V8-4.4", 308, {"debut": "1959-01", "fin": "1968-12"}), ("5.0 V8 196", "IH-V8-5.0", 393, {"debut": "1969-01"}),
    ("5.6 V8 200", "IH-V8-5.6", 451, {"debut": "1969-01"}), ("6.4 V8 238", "IH-V8-6.4", 481, {"debut": "1969-01"})],
   portes=4, places=6, reservoir=72, remarques="Précurseur des SUV ; générations R, S, A, B, C, D et 1000-1500 ; " + IND)
mg(L, "Scout 80", "Scout 80", "1", "1961-01", "1965-12", [("2.5 94", "IH-COMANCHE-2.5", 183)], portes=2, places=4, reservoir=42, remarques="Tout-terrain à pare-brise rabattable ; " + IND)
mg(L, "Scout 800", "Scout 800", "1", "1965-01", "1971-12", [("2.5 94", "IH-COMANCHE-2.5", 183), ("3.2 113", "IH-COMANCHE-3.2", 244), ("4.4 V8 157", "IH-V8-4.4", 308, {"debut": "1967-01"}),
                                                           ("5.0 V8 196", "IH-V8-5.0", 393, {"debut": "1969-01"})], portes=2, places=4, reservoir=42, remarques=IND)
mg(L, "Scout II", "Scout II", "1", "1971-01", "1980-12",
   [("3.2 87", "IH-COMANCHE-3.2", 214), ("5.0 V8 147", "IH-V8-5.0", 332), ("5.6 V8 159", "IH-V8-5.6", 386), ("Diesel 3.3 82", "NISSAN-SD33-3.3D", 186, {"debut": "1976-01"}),
    ("Diesel Turbo 3.3 102", "NISSAN-SD33T-3.3TD", 237, {"debut": "1980-01"})], portes=2, places=5, reservoir=72,
   remarques="Dont Traveler et Terra (empattement long) ; puissances nettes ; " + IND)
mg(L, "Light Line Pickup", "D-1000 / 1100", "1", "1969-01", "1975-12", [("5.0 V8 196", "IH-V8-5.0", 393), ("5.6 V8 200", "IH-V8-5.6", 451)], portes=2, places=3, reservoir=72,
   remarques="Pick-up léger ; " + IND)

MOT = Motorisations("International Harvester", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"International Harvester": L}
MOTEURS = MOT.moteurs()
