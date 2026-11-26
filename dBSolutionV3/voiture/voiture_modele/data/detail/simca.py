"""Simca : générations, phases, motorisations (marché européen) et moteurs liés.
5, 8, Aronde (9, 90 A, P60), Vedette, Ariane, 1000 (dont Rallye), 1000 Coupé, 1200 S, 1300 / 1500, 1301 / 1501, 1100,
1307 / 1308 / 1309 et Horizon. Marque remplacée par Talbot en 1979-1980.
Moteurs Poissy repris de peugeot_classiques.py (Peugeot 104 / 205), 1.6 de plymouth.py, diesel XUD de peugeot_classiques.py
(mêmes codes) ; moteurs Fiat, Flash, Rush, Type 1300 / 1500, V8 Aquilon et Poissy 0.9 à 1.4 ajoutés. Données indicatives.
Le Simca Cargo (camion) n'est pas repris ; Matra-Simca Bagheera / Rancho dans Matra.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .peugeot_classiques import FAMILLES as FAMILLES_PEUGEOT
from .plymouth import FAMILLES as FAMILLES_PLYMOUTH

E_, D = "ESS", "DSL"
C, SV = "CHAINE", "NC"

SIMCA_PROPRES = {
    "FIAT-0.6": f("ATM", E_, 0.57, SV, 4, 4000, 2500, "SAE30", 2.5, 3000),
    "FIAT-1.1-SIMCA": f("ATM", E_, 1.1, C, 4, 4400, 2800, "SAE30", 3.0, 3000),
    "FLASH-1.3": f("ATM", E_, 1.3, C, 4, 5000, 2600, "20W50", 3.5, 5000),
    "AQUILON-V8-2.35": f("ATM", E_, 2.35, SV, 8, 4800, 2600, "20W50", 4.5, 5000, a="V"),
    "SIMCA-TYPE-1.3": f("ATM", E_, 1.3, C, 4, 5400, 3000, "20W50", 3.5, 7500),
    "SIMCA-TYPE-1.5": f("ATM", E_, 1.5, C, 4, 5200, 2800, "20W50", 3.5, 7500),
    "POISSY-0.9": f("ATM", E_, 0.94, C, 4, 5200, 2800, "15W40", 3.0, 7500),
    "POISSY-1.2": f("ATM", E_, 1.2, C, 4, 6000, 4500, "15W40", 3.5, 7500),
    "POISSY-1.4": f("ATM", E_, 1.4, C, 4, 5600, 3000, "15W40", 3.5, 7500),
}
PSA = {k: FAMILLES_PEUGEOT[k] for k in ("POISSY-1.1", "POISSY-1.3", "XUD9")}
CHRYSLER_EU = {"SIMCA-1.6": FAMILLES_PLYMOUTH["SIMCA-1.6"]}
FAMILLES = {**SIMCA_PROPRES, **PSA, **CHRYSLER_EU}


def motoriste(fam):
    if fam.startswith("FIAT-"):
        return "Fiat"
    if fam == "AQUILON-V8-2.35":
        return "Ford"
    if fam == "XUD9":
        return "Peugeot"
    return "Simca"


mg = SaisieMoteurs(FAMILLES, "Simca", motoriste)
L = []
IND = "données indicatives"

mg(L, "5", "5", "1", "1936-01", "1949-12", [("0.6 13", "FIAT-0.6", 30)], portes=2, places=2, reservoir=21, remarques="Fiat 500 Topolino construite en France ; " + IND)
mg(L, "8", "8", "1", "1937-01", "1951-12", [("1.1 32", "FIAT-1.1-SIMCA", 65), ("1.2 40", "FIAT-1.1-SIMCA", 72, {"debut": "1949-01"})], portes=4, places=5, reservoir=36,
   remarques="Base Fiat 508 C ; berline, coupé et cabriolet ; 1.2 rattaché à la famille 1.1 ; " + IND)
mg(L, "Aronde", "9", "1", "1951-05", "1955-09", [("1.2 45", "FIAT-1.1-SIMCA", 78)], portes=4, places=5, reservoir=42, remarques="Simca 9 Aronde ; " + IND)
mg(L, "Aronde", "90 A", "1", "1955-10", "1958-09", [("Flash 1.3 48", "FLASH-1.3", 88), ("Flash Spécial 1.3 57", "FLASH-1.3", 90, {"debut": "1957-01"})], portes=4, places=5, reservoir=42,
   remarques="Berline, break Châtelaine, coupé et cabriolet Océane / Plein Ciel ; " + IND)
mg(L, "Aronde", "P60", "1", "1958-10", "1964-02", [("Flash 1.3 48", "FLASH-1.3", 88), ("Rush 1.3 57", "SIMCA-TYPE-1.3", 95, {"debut": "1960-09"}), ("Montlhéry 1.3 62", "SIMCA-TYPE-1.3", 98, {"debut": "1961-09"})],
   portes=4, places=5, reservoir=42, remarques=IND)
mg(L, "Vedette", "Vedette", "1", "1955-01", "1961-12", [("2.35 V8 80", "AQUILON-V8-2.35", 150), ("2.35 V8 84", "AQUILON-V8-2.35", 152, {"debut": "1958-01"})],
   portes=4, places=6, reservoir=60, remarques="Ex-Ford France ; Trianon, Versailles, Régence, Beaulieu, Chambord, Marly ; " + IND)
mg(L, "Ariane", "Ariane", "1", "1957-01", "1963-12", [("1.3 48", "FLASH-1.3", 88), ("2.35 V8 84", "AQUILON-V8-2.35", 152, {"fin": "1959-12"})], portes=4, places=6, reservoir=60,
   remarques="Caisse de Vedette, moteur d'Aronde ; " + IND)
mg(L, "1000", "1000", "1", "1961-10", "1978-12",
   [("0.9 35", "POISSY-0.9", 64), ("0.9 40", "POISSY-0.9", 66, {"debut": "1966-01"}), ("1.1 45", "POISSY-1.1", 80, {"debut": "1969-01"}), ("1.3 54", "POISSY-1.3", 93, {"debut": "1976-01"}),
    ("Rallye 1 1.3 60", "POISSY-1.3", 96, {"debut": "1970-10", "fin": "1972-12"}), ("Rallye 2 1.3 82", "POISSY-1.3", 106, {"debut": "1972-01"}), ("Rallye 3 1.3 103", "POISSY-1.3", 118, {"debut": "1977-06"})],
   portes=4, places=5, reservoir=36, remarques="Moteur arrière ; " + IND)
mg(L, "1000 Coupé", "1000 Coupé", "1", "1962-09", "1967-12", [("0.9 52", "POISSY-0.9", 72)], portes=2, places=4, reservoir=36, remarques="Coupé Bertone ; " + IND)
mg(L, "1200 S", "1200 S", "1", "1967-09", "1971-12", [("1.2 80", "POISSY-1.2", 103), ("1.2 85", "POISSY-1.2", 105, {"debut": "1969-01"})], portes=2, places=4, reservoir=36,
   remarques="Évolution du 1000 Coupé ; " + IND)
mg(L, "1300", "1300 / 1500", "1", "1963-04", "1966-09", [("1300 1.3 62", "SIMCA-TYPE-1.3", 98), ("1500 1.5 81", "SIMCA-TYPE-1.5", 118)], portes=4, places=5, reservoir=56,
   remarques="Simca 1300 et 1500, berline et break ; " + IND)
mg(L, "1301", "1301 / 1501", "1", "1966-10", "1976-07", [("1301 1.3 54", "SIMCA-TYPE-1.3", 95), ("1301 S 1.3 70", "SIMCA-TYPE-1.3", 100), ("1501 1.5 69", "SIMCA-TYPE-1.5", 112),
                                                         ("1501 S 1.5 81", "SIMCA-TYPE-1.5", 118)], portes=4, places=5, reservoir=56,
   remarques="Simca 1301 et 1501, berline et break ; " + IND)
mg(L, "1100", "1100", "1", "1967-10", "1982-12",
   [("0.9 45", "POISSY-0.9", 70, {"fin": "1974-12"}), ("1.1 50", "POISSY-1.1", 80), ("1.1 60", "POISSY-1.1", 86), ("Ti 1.3 82", "POISSY-1.3", 106, {"debut": "1973-01", "fin": "1975-12"}),
    ("1.3 68", "POISSY-1.3", 102, {"debut": "1976-01"})], portes=5, places=5, reservoir=42, remarques="Traction ; 3 et 5 portes, break, fourgonnette ; Talbot à partir de 1979 ; " + IND)
mg(L, "1307", "1307 / 1308", "1", "1975-09", "1979-12",
   [("1307 1.3 68", "POISSY-1.3", 102), ("1307 S 1.3 82", "POISSY-1.3", 106), ("1308 1.4 85", "POISSY-1.4", 122), ("1309 1.6 88", "SIMCA-1.6", 132, {"debut": "1978-09"})],
   portes=5, places=5, reservoir=60, remarques="Voiture européenne de l'année 1976 ; Chrysler Alpine en Angleterre ; puis Talbot 1510 ; " + IND)
mg(L, "Horizon", "Horizon", "1", "1977-12", "1979-12", [("1.1 59", "POISSY-1.1", 86), ("1.3 68", "POISSY-1.3", 102), ("1.5 83", "POISSY-1.4", 122, {"remarques": "1.5 Type 1442 réalésé"})],
   portes=5, places=5, reservoir=47, remarques="Voiture européenne de l'année 1979 ; vendue sous la marque Talbot à partir de 1979 ; " + IND)

MOT = Motorisations("Simca", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Simca": L}
MOTEURS = MOT.moteurs()
