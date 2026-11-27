"""GAZ (Gorkovski Avtomobilny Zavod, Nijni Novgorod) : générations, phases, motorisations et moteurs liés.
Voitures : M20 Pobeda, Volga M21, M24 et 3102, Chaika GAZ-13 et GAZ-14 ; utilitaires et camions : GAZ-51, GAZ-66, GAZelle,
GAZelle Next, Sobol et Tigr (4x4 militaire). Moteurs GAZ / ZMZ et Cummins. Puissances en ch. Données indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_, D = "ESS", "DSL"
C = "CHAINE"
GAZ = {
    "GAZ-M20-2.1": f("ATM", E_, 2.1, "NC", 4, 3600, 2000, "SAE30", 4.5, 3000),
    "GAZ-51-L6-3.5": f("ATM", E_, 3.5, "NC", 6, 2800, 1500, "SAE30", 6.0, 3000),
    "GAZ-13-V8-5.5": f("ATM", E_, 5.5, C, 8, 4400, 2200, "20W50", 6.5, 5000, a="V"),
    "GAZ-14-V8-5.5": f("ATM", E_, 5.5, C, 8, 4200, 2500, "20W50", 6.5, 5000, a="V"),
    "GAZ-66-V8-4.25": f("ATM", E_, 4.25, C, 8, 3200, 2000, "20W50", 8.0, 5000, a="V"),
}
ZMZ = {
    "ZMZ-21-2.4": f("ATM", E_, 2.4, C, 4, 4000, 2200, "20W50", 6.0, 5000),
    "ZMZ-24-2.4": f("ATM", E_, 2.4, C, 4, 4500, 2400, "20W50", 6.0, 7500),
    "ZMZ-406-2.3": f("ATM", E_, 2.3, C, 4, 5200, 4000, "10W40", 6.0, 10000),
}
CUMMINS = {
    "CUMMINS-ISF-2.8": f("TURBO", D, 2.8, C, 4, 3600, 1600, "15W40", 6.0, 20000),
    "CUMMINS-6BT-5.9": f("TURBO", D, 5.9, "NC", 6, 2500, 1500, "15W40", 14.0, 15000),
}
FAMILLES = {**GAZ, **ZMZ, **CUMMINS}


def motoriste(fam):
    if fam in ZMZ:
        return "ZMZ"
    if fam in CUMMINS:
        return "Cummins"
    return "GAZ"


mg = SaisieMoteurs(FAMILLES, "GAZ", motoriste)
L = []
IND = "données indicatives, à vérifier"

mg(L, "M20 Pobeda", "M20", "1", "1946-06", "1958-05", [("2.1 52", "GAZ-M20-2.1", 125)], portes=4, places=5, reservoir=55, remarques="Berline fastback « Victoire » ; " + IND)
mg(L, "Volga M21", "M21", "1", "1956-10", "1970-07", [("2.4 70", "ZMZ-21-2.4", 166, {"fin": "1958-12"}), ("2.4 75", "ZMZ-21-2.4", 170, {"debut": "1959-01"})],
   portes=4, places=5, reservoir=60, remarques="Berline et break (M22) ; " + IND)
mg(L, "Volga M24", "M24", "1", "1970-07", "1992-12", [("2.4 95", "ZMZ-24-2.4", 186), ("24-10 2.4 100", "ZMZ-24-2.4", 191, {"debut": "1985-01"})],
   portes=4, places=5, reservoir=55, remarques="Berline et break (24-02), taxi ; " + IND)
mg(L, "Volga 3102", "3102", "1", "1982-01", "2008-12", [("2.4 100", "ZMZ-24-2.4", 191), ("2.3 16V 131", "ZMZ-406-2.3", 200, {"debut": "1997-01"})],
   portes=4, places=5, reservoir=55, remarques="Berline de fonction ; " + IND)
mg(L, "Chaika GAZ-13", "GAZ-13", "1", "1959-01", "1981-12", [("5.5 V8 195", "GAZ-13-V8-5.5", 412)], portes=4, places=7, reservoir=80,
   remarques="Limousine officielle soviétique ; " + IND)
mg(L, "Chaika GAZ-14", "GAZ-14", "1", "1977-01", "1988-12", [("5.5 V8 220", "GAZ-14-V8-5.5", 451)], portes=4, places=7, reservoir=80, remarques="Limousine officielle ; " + IND)
mg(L, "GAZ-51", "GAZ-51", "1", "1946-01", "1975-12", [("3.5 L6 70", "GAZ-51-L6-3.5", 205)], portes=2, places=3, reservoir=90, remarques="Camion 2,5 t ; " + IND)
mg(L, "GAZ-66", "GAZ-66", "1", "1964-01", "1999-12", [("4.25 V8 115", "GAZ-66-V8-4.25", 284)], portes=2, places=2, reservoir=210, remarques="Camion 4x4 militaire « Chichiga » ; " + IND)
mg(L, "GAZelle", "3302", "1", "1994-07", "2010-12", [("2.4 100", "ZMZ-24-2.4", 191), ("2.3 110", "ZMZ-406-2.3", 191, {"debut": "1997-01"}),
                                                    ("2.8 TD 120", "CUMMINS-ISF-2.8", 297, {"debut": "2010-01"})], portes=4, places=3, reservoir=70,
   remarques="Utilitaire léger (fourgon, plateau, minibus) ; " + IND)
mg(L, "GAZelle Next", "Next", "1", "2013-04", None, [("2.8 TD 120", "CUMMINS-ISF-2.8", 297)], portes=4, places=3, reservoir=80,
   remarques="Utilitaire léger, version électrique non reprise ; " + IND)
mg(L, "Sobol", "2217", "1", "1998-01", None, [("2.3 110", "ZMZ-406-2.3", 191), ("2.8 TD 120", "CUMMINS-ISF-2.8", 297, {"debut": "2010-01"})], portes=5, places=7, reservoir=70,
   remarques="Minibus et fourgon compact ; " + IND)
mg(L, "Tigr", "GAZ-2330", "1", "2005-01", None, [("5.9 TD 205", "CUMMINS-6BT-5.9", 680)], portes=5, places=7, reservoir=120,
   remarques="Véhicule blindé 4x4 militaire et civil ; moteurs YaMZ non repris ; " + IND)

MOT = Motorisations("GAZ", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"GAZ": L}
MOTEURS = MOT.moteurs()
