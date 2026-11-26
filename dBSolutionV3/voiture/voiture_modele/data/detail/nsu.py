"""NSU : générations, phases, motorisations (marché européen) et moteurs liés.
Kettenkrad, Prinz (I à III), Sport Prinz, Prinz 4, Wankel Spider, Prinz 1000, Typ 110 / 1200, TT / TTS et Ro 80.
Bicylindres et quatre cylindres refroidis par air NSU, moteurs rotatifs Wankel KKM 502 et KKM 612, et 1.5 Opel (Kettenkrad)
ajoutés. Données indicatives. Le K 70 (prototype NSU de 1969) n'est pas repris : il a été produit sous la marque Volkswagen.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C = "CHAINE"

NSU = {
    "NSU-2CYL-0.6": f("ATM", E_, 0.6, "NC", 2, 5500, 3000, "20W50", 2.5, 5000),
    "NSU-4CYL-1.0": f("ATM", E_, 1.0, C, 4, 5500, 3500, "20W50", 3.5, 5000),
    "NSU-4CYL-1.1": f("ATM", E_, 1.1, C, 4, 5500, 3500, "20W50", 3.5, 5000),
    "NSU-4CYL-1.2": f("ATM", E_, 1.2, C, 4, 5800, 3500, "20W50", 3.5, 5000),
    "KKM502-0.5": f("WANKEL", E_, 0.5, "AUCUNE", 1, 6000, 3500, "20W50", 3.0, 5000, a="ROTATIF"),
    "KKM612-1.0": f("WANKEL", E_, 1.0, "AUCUNE", 2, 5500, 4500, "20W50", 6.0, 5000, a="ROTATIF"),
}
OPEL = {"OPEL-1.5": f("ATM", E_, 1.5, C, 4, 3400, 2000, "20W50", 3.0, 3000)}
FAMILLES = {**NSU, **OPEL}


def motoriste(fam):
    return "Opel" if fam in OPEL else "NSU"


mg = SaisieMoteurs(FAMILLES, "NSU", motoriste)
L = []
IND = "données indicatives"

mg(L, "Kettenkrad", "HK 101", "1", "1940-06", "1949-12", [("1.5 36", "OPEL-1.5", 98)], portes=0, places=3, reservoir=42,
   remarques="Semi-chenillé militaire puis agricole, moteur Opel Olympia ; " + IND)
mg(L, "Prinz", "Prinz I-III", "1", "1958-03", "1962-12", [("0.6 20", "NSU-2CYL-0.6", 33, {"fin": "1959-12"}), ("0.6 23", "NSU-2CYL-0.6", 37, {"debut": "1959-01"}),
                                                             ("0.6 30", "NSU-2CYL-0.6", 44, {"debut": "1960-06"})],
   portes=2, places=4, reservoir=25, remarques="Bicylindre 583 cm³ refroidi par air ; " + IND)
mg(L, "Sport Prinz", "Sport Prinz", "1", "1959-09", "1967-12", [("0.6 30", "NSU-2CYL-0.6", 44)], portes=2, places=2, reservoir=25,
   remarques="Coupé carrossé par Bertone ; " + IND)
mg(L, "Prinz 4", "Prinz 4", "1", "1961-09", "1973-07", [("0.6 30", "NSU-2CYL-0.6", 44), ("0.6 36", "NSU-2CYL-0.6", 46, {"debut": "1967-01"})],
   portes=2, places=4, reservoir=36, remarques="Bicylindre 598 cm³ ; " + IND)
mg(L, "Wankel Spider", "Spider", "1", "1964-09", "1967-12", [("Wankel 0.5 50", "KKM502-0.5", 72)], portes=2, places=2, reservoir=35,
   remarques="Première voiture de série à moteur rotatif Wankel (monorotor) ; " + IND)
mg(L, "Prinz 1000", "Prinz 1000", "1", "1964-01", "1972-12", [("1.0 43", "NSU-4CYL-1.0", 72)], portes=2, places=5, reservoir=40,
   remarques="Quatre cylindres refroidi par air, dit aussi NSU 1000 ; " + IND)
mg(L, "Typ 110", "Typ 110", "1", "1965-10", "1967-12", [("1.1 53", "NSU-4CYL-1.1", 82)], portes=2, places=5, reservoir=45, remarques=IND)
mg(L, "Typ 110", "1200", "1", "1967-01", "1973-07", [("1200 1.2 55", "NSU-4CYL-1.2", 88)], portes=2, places=5, reservoir=45, remarques="NSU 1200 ; " + IND)
mg(L, "TT", "TT", "1", "1965-06", "1972-07",
   [("TTS 1.0 70", "NSU-4CYL-1.0", 83, {"fin": "1971-12"}), ("TT 1.1 55", "NSU-4CYL-1.1", 85, {"fin": "1967-08"}), ("TT 1.2 65", "NSU-4CYL-1.2", 88, {"debut": "1967-09"})],
   portes=2, places=5, reservoir=40, remarques="Version sportive de la Prinz 1000 ; " + IND)
mg(L, "Ro 80", "Ro 80", "1", "1967-10", "1977-04", [("Wankel 1.0 115", "KKM612-1.0", 158)], portes=4, places=5, reservoir=83,
   remarques="Moteur rotatif birotor 2 × 497 cm³ ; voiture européenne de l'année 1968")

MOT = Motorisations("NSU", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"NSU": L}
MOTEURS = MOT.moteurs()
