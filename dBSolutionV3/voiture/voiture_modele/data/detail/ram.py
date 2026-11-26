"""Ram (Ram Trucks) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
1500 (DS, Classic, DT), 2500 et 3500 (Heavy Duty, 4e et 5e générations) depuis la création de la marque Ram (2010), et l'ancien
Ramcharger Dodge (1974-1993). Les Ram 1500 jusqu'en 2010 restent dans Dodge, le Ram 1500 TRX dans Dodge SRT.
Moteurs Chrysler / Dodge repris de chrysler.py, dodge.py et plymouth.py (mêmes codes) ; Pentastar et Hemi eTorque et Cummins 6.7
ajoutés. Puissances SAE converties en ch (× 1,014). Le Ram 1500 REV (ex-Ramcharger à prolongateur d'autonomie, lancement
repoussé) et les utilitaires ProMaster ne sont pas repris. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .chrysler import FAMILLES as FAMILLES_CHRYSLER
from .dodge import FAMILLES as FAMILLES_DODGE
from .plymouth import FAMILLES as FAMILLES_PLYMOUTH

E_, D = "ESS", "DSL"
C = "CHAINE"

CHRYSLER = {**{k: FAMILLES_CHRYSLER[k] for k in ("PENTASTAR-3.6", "POWERTECH-4.7", "HEMI-5.7", "HEMI-6.4", "VM-3.0CRD")},
            **{k: FAMILLES_DODGE[k] for k in ("EKG-3.7", "HURRICANE-3.0TT")},
            **{k: FAMILLES_PLYMOUTH[k] for k in ("LA-5.2", "LA-5.9")},
            "PENTASTAR-3.6-ETORQUE": f("HYB_TE", E_, 3.6, C, 6, 6400, 4800, "0W20", 5.7, 12000, a="V"),
            "HEMI-5.7-ETORQUE": f("HYB_TE", E_, 5.7, C, 8, 5600, 3950, "0W20", 6.6, 12000, a="V")}
CUMMINS = {"CUMMINS-6.7": f("TURBO", D, 6.7, "NC", 6, 2800, 1700, "15W40", 11.4, 24000)}
FAMILLES = {**CHRYSLER, **CUMMINS}


def motoriste(fam):
    if fam in CUMMINS:
        return "Cummins"
    if fam == "VM-3.0CRD":
        return "VM Motori"
    return "Chrysler"


mg = SaisieMoteurs(FAMILLES, "Ram", motoriste)
L = []
NA = "Marché nord-américain"
IND = NA + " ; données indicatives"
CAB = "Regular, Quad et Crew Cab"

mg(L, "Ramcharger", "AW", "1", "1974-01", "1993-12",
   [("5.2 V8 152", "LA-5.2", 346), ("5.9 V8 177", "LA-5.9", 380, {"fin": "1991-12"}), ("5.2 V8 Magnum 233", "LA-5.2", 461, {"debut": "1992-01"})],
   portes=2, places=5, reservoir=132, remarques="SUV Dodge sur base pick-up (Plymouth Trail Duster jusqu'en 1981) ; " + IND)
mg(L, "1500", "DS", "1", "2010-09", "2018-12",
   [("3.7 V6 218", "EKG-3.7", 319, {"fin": "2012-12"}), ("4.7 V8 314", "POWERTECH-4.7", 447, {"fin": "2013-06"}), ("5.7 Hemi V8 395", "HEMI-5.7", 552),
    ("3.6 V6 309", "PENTASTAR-3.6", 363, {"debut": "2013-01"}), ("3.0 EcoDiesel V6 243", "VM-3.0CRD", 570, {"debut": "2014-01"})],
   portes=4, places=5, reservoir=98, remarques=CAB + " ; dont Rebel ; " + IND)
mg(L, "1500 Classic", "DS", "2", "2019-01", "2024-12",
   [("3.6 V6 309", "PENTASTAR-3.6", 363), ("5.7 Hemi V8 395", "HEMI-5.7", 552), ("3.0 EcoDiesel V6 243", "VM-3.0CRD", 570, {"fin": "2020-12"})],
   portes=4, places=5, reservoir=98, remarques="Ancienne génération vendue en parallèle du DT ; " + IND)
mg(L, "1500", "DT", "1", "2019-01", "2024-12",
   [("3.6 V6 eTorque 309", "PENTASTAR-3.6-ETORQUE", 365), ("5.7 Hemi V8 401", "HEMI-5.7", 556), ("5.7 Hemi V8 eTorque 401", "HEMI-5.7-ETORQUE", 556),
    ("3.0 EcoDiesel V6 264", "VM-3.0CRD", 599, {"debut": "2020-01", "fin": "2023-06"})], portes=4, places=5, reservoir=98,
   remarques="Quad et Crew Cab ; TRX dans Dodge SRT ; " + IND)
mg(L, "1500", "DT", "2", "2025-01", None,
   [("3.6 V6 eTorque 309", "PENTASTAR-3.6-ETORQUE", 365), ("3.0 Hurricane Biturbo 426", "HURRICANE-3.0TT", 635), ("3.0 Hurricane HO Biturbo 548", "HURRICANE-3.0TT", 706),
    ("5.7 Hemi V8 eTorque 401", "HEMI-5.7-ETORQUE", 556, {"debut": "2025-07", "remarques": "Retour du V8 Hemi pour l'année-modèle 2026"})],
   portes=4, places=5, reservoir=98, remarques="Restylage ; six cylindres en ligne Hurricane (dont RHO) ; " + IND)
mg(L, "2500", "DJ", "1", "2010-01", "2018-12",
   [("5.7 Hemi V8 388", "HEMI-5.7", 542), ("6.4 Hemi V8 416", "HEMI-6.4", 582, {"debut": "2014-01"}), ("6.7 Cummins 355", "CUMMINS-6.7", 881, {"fin": "2012-12"}),
    ("6.7 Cummins 375", "CUMMINS-6.7", 1152, {"debut": "2013-01"})], portes=4, places=6, reservoir=132,
   remarques="Heavy Duty ; Regular, Crew et Mega Cab ; " + IND)
mg(L, "2500", "DJ", "2", "2019-01", None,
   [("6.4 Hemi V8 416", "HEMI-6.4", 582), ("6.7 Cummins 375", "CUMMINS-6.7", 1152)], portes=4, places=6, reservoir=121,
   remarques="Heavy Duty, nouvelle génération ; Regular, Crew et Mega Cab ; dont Power Wagon ; " + IND)
mg(L, "3500", "D2", "1", "2010-01", "2018-12",
   [("5.7 Hemi V8 388", "HEMI-5.7", 542), ("6.4 Hemi V8 416", "HEMI-6.4", 582, {"debut": "2014-01"}), ("6.7 Cummins 355", "CUMMINS-6.7", 881, {"fin": "2012-12"}),
    ("6.7 Cummins HO 390", "CUMMINS-6.7", 1220, {"debut": "2013-01"})], portes=4, places=6, reservoir=132,
   remarques="Heavy Duty, roues arrière jumelées possibles ; Regular, Crew et Mega Cab ; " + IND)
mg(L, "3500", "D2", "2", "2019-01", None,
   [("6.4 Hemi V8 416", "HEMI-6.4", 582), ("6.7 Cummins 375", "CUMMINS-6.7", 1152), ("6.7 Cummins HO 406", "CUMMINS-6.7", 1356, {"fin": "2020-12"}),
    ("6.7 Cummins HO 426", "CUMMINS-6.7", 1458, {"debut": "2021-01", "fin": "2024-12"}), ("6.7 Cummins HO 436", "CUMMINS-6.7", 1458, {"debut": "2025-01"})],
   portes=4, places=6, reservoir=121, remarques="Heavy Duty, nouvelle génération ; " + IND)

MOT = Motorisations("Ram", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Ram": L}
MOTEURS = MOT.moteurs()
