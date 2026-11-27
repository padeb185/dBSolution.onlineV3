"""Borgward : générations, phases, motorisations (marché européen) et moteurs liés.
Borgward historique (Brême) : Hansa 1500 / 1800, Isabella et P100 (1949-1961).
Borgward Group (relance sino-allemande, 2016-2021) : BX5, BX7, BX7 TS et BXi7 électrique ; faillite en 2022.
Puissances en ch DIN. Données historiques indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

E_ = "ESS"
FAMILLES = {
    "BORGWARD-1.5": f("ATM", E_, 1.5, "NC", 4, 4000, 2400, "SAE30", 3.5, 3000),
    "BORGWARD-1.8": f("ATM", E_, 1.8, "NC", 4, 4000, 2400, "SAE30", 4.0, 3000),
    "BORGWARD-1.8D": f("ATM", "DSL", 1.8, "NC", 4, 3200, 2000, "SAE30", 4.5, 3000),
    "BORGWARD-L6-2.2": f("ATM", E_, 2.2, "NC", 6, 5000, 2800, "SAE30", 5.0, 3000),
    "BORGWARD-1.4T": f("TURBO", E_, 1.4, "CHAINE", 4, 5500, 1750, "5W30", 4.5, 10000),
    "BORGWARD-2.0T": f("TURBO", E_, 2.0, "CHAINE", 4, 5500, 2000, "5W30", 5.0, 10000),
    "BORGWARD-EV": electrique(),
}
mg = SaisieMoteurs(FAMILLES, "Borgward", lambda fam: "Borgward")
L = []
IND = "données indicatives (marque ancienne), à vérifier"

mg(L, "Hansa 1500", "Hansa 1500", "1", "1949-01", "1952-12", [("1.5 48", "BORGWARD-1.5", 98)], portes=4, places=5, reservoir=50,
   remarques="Berline ponton (aussi coupé et cabriolet) ; " + IND)
mg(L, "Hansa 1800", "Hansa 1800", "1", "1952-01", "1954-12", [("1.8 60", "BORGWARD-1.8", 125), ("1.8 Diesel 42", "BORGWARD-1.8D", 96, {"debut": "1953-01"})],
   portes=4, places=5, reservoir=50, remarques="Berline ; " + IND)
mg(L, "Isabella", "Isabella", "1", "1954-06", "1961-12", [("1.5 60", "BORGWARD-1.5", 108), ("TS 1.5 75", "BORGWARD-1.5", 114, {"debut": "1955-09"})],
   portes=4, places=5, reservoir=45, remarques="Berline, break (Combi), coupé et cabriolet ; " + IND)
mg(L, "P100", "P100", "1", "1959-09", "1961-12", [("2.2 L6 100", "BORGWARD-L6-2.2", 162)], portes=4, places=5, reservoir=60,
   remarques="« Grosse Borgward », suspension pneumatique ; " + IND)
mg(L, "BX5", "BX5", "1", "2017-03", "2021-12", [("1.4 TGDI 150", "BORGWARD-1.4T", 235), ("2.0 TGDI 224", "BORGWARD-2.0T", 300)], portes=5, places=5, reservoir=60,
   remarques="SUV compact (BX6 : version fastback), assemblé à Pékin ; quelques exemplaires vendus en Europe")
mg(L, "BX7", "BX7", "1", "2016-07", "2021-12", [("2.0 TGDI 224", "BORGWARD-2.0T", 300)], portes=5, places=5, reservoir=70,
   remarques="SUV, 5 à 7 places, transmission intégrale ; assemblé à Pékin")
mg(L, "BX7 TS", "BX7", "1", "2016-07", "2021-12", [("TS 2.0 TGDI 224", "BORGWARD-2.0T", 300)], portes=5, places=5, reservoir=70, remarques="Finition sportive du BX7")
mg(L, "BXi7", "BXi7", "1", "2019-01", "2021-12", [("Électrique 82 kWh 272", "BORGWARD-EV", 400, {"batterie": 82})], portes=5, places=5, reservoir=0,
   remarques="Version électrique du BX7, autonomie annoncée 500 km ; principalement Chine")

MOT = Motorisations("Borgward", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Borgward": L}
MOTEURS = MOT.moteurs()
