"""Imperial (Chrysler) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Marque de luxe de Chrysler (1955-1975, puis 1981-1983 et 1990-1993) : Imperial (1955-1956), Custom, Crown et LeBaron (1957-1975),
coupé Imperial (1981-1983) et berline Imperial (Y-body, 1990-1993). V8 Hemi FirePower, Wedge B/RB et LA ajoutés ; V6 repris de
chrysler.py. Puissances brutes jusqu'en 1971, nettes ensuite, converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .chrysler import FAMILLES as FAMILLES_CHRYSLER

E_, C = "ESS", "CHAINE"


def v8(l, rpm, nmrpm):
    return f("ATM", E_, l, C, 8, rpm, nmrpm, "10W30", 4.7, 5000, a="V")


FAMILLES = {
    "FIREPOWER-5.4": v8(5.4, 4400, 2800), "FIREPOWER-5.8": v8(5.8, 4600, 2800), "FIREPOWER-6.4": v8(6.4, 4600, 2800),
    "RB-6.8": v8(6.8, 4600, 2800), "RB-7.2": v8(7.2, 4600, 3200), "LA-5.2": v8(5.2, 4000, 2000),
    "EGA-3.3": FAMILLES_CHRYSLER["EGA-3.3"], "EGH-3.8": FAMILLES_CHRYSLER["EGH-3.8"],
}
mg = SaisieMoteurs(FAMILLES, "Chrysler")
L = []
IND = "marché nord-américain ; données indicatives"

mg(L, "Imperial", "Imperial 1955", "1", "1955-01", "1956-12", [("5.4 V8 Hemi 254", "FIREPOWER-5.4", 461, {"fin": "1955-12"}), ("5.8 V8 Hemi 284", "FIREPOWER-5.8", 515, {"debut": "1956-01"})],
   portes=4, places=6, reservoir=76, remarques="Imperial devient une marque distincte de Chrysler en 1955 ; " + IND)
V57 = [("6.4 V8 Hemi 330", "FIREPOWER-6.4", 583, {"fin": "1958-12"}), ("6.8 V8 355", "RB-6.8", 637, {"debut": "1959-01", "fin": "1965-12"}),
       ("7.2 V8 355", "RB-7.2", 651, {"debut": "1966-01", "fin": "1971-12"}), ("7.2 V8 228", "RB-7.2", 475, {"debut": "1972-01"})]
mg(L, "Custom", "Imperial 1957", "1", "1957-01", "1963-12", V57[:2], portes=4, places=6, reservoir=87, remarques="Berline et coupé Southampton ; " + IND)
mg(L, "Crown", "Imperial 1957", "1", "1957-01", "1970-12", V57[:3], portes=4, places=6, reservoir=87, remarques="Berline, coupé, cabriolet et limousine Crown Imperial (Ghia) ; " + IND)
mg(L, "LeBaron", "Imperial 1957", "1", "1957-01", "1975-12", V57, portes=4, places=6, reservoir=87, remarques="Version la plus luxueuse ; puissances nettes dès 1972 ; " + IND)
mg(L, "Imperial", "Imperial 1981", "1", "1981-01", "1983-12", [("5.2 V8 EFI 142", "LA-5.2", 332)], portes=2, places=5, reservoir=68,
   remarques="Coupé à injection électronique, édition Frank Sinatra ; " + IND)
mg(L, "Imperial", "Y-body", "1", "1990-01", "1993-12", [("3.3 V6 149", "EGA-3.3", 251, {"fin": "1990-12"}), ("3.8 V6 152", "EGH-3.8", 271, {"debut": "1991-01"})],
   portes=4, places=6, reservoir=61, remarques="Berline à traction, dérivée de la New Yorker ; " + IND)

MOT = Motorisations("Chrysler", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Imperial": L}
MOTEURS = MOT.moteurs()
