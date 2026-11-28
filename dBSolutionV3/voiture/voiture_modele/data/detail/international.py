"""International (Navistar, Lisle, Illinois) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Camions et tracteurs routiers : Loadstar, Transtar, 9000 Series, DuraStar, CXT (pick-up géant), LoneStar et LT Series. Moteurs Navistar
(DT466, MaxxForce, A26) et Cummins ajoutés ; V8 essence IH repris d'international_harvester.py. Puissances hp converties en ch (× 1,014).
Désignations, motorisations et dates indicatives (poids lourds, nombreuses configurations).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .international_harvester import FAMILLES as FAMILLES_IH

D = "DSL"
FAMILLES = {
    "IH-V8-6.4": FAMILLES_IH["IH-V8-6.4"],
    "NAV-DT466-7.6": f("TURBO", D, 7.6, "NC", 6, 2600, 1400, "15W40", 26.0, 25000),
    "CUMMINS-NTC-14.0": f("TURBO", D, 14.0, "NC", 6, 2100, 1300, "15W40", 36.0, 25000),
    "CUMMINS-ISX-15.0": f("TURBO", D, 15.0, "NC", 6, 1900, 1100, "15W40", 40.0, 40000),
    "NAV-MAXXFORCE13-12.4": f("TURBO", D, 12.4, "NC", 6, 1900, 1100, "15W40", 38.0, 40000),
    "NAV-A26-12.4": f("TURBO", D, 12.4, "NC", 6, 1800, 1000, "10W30", 40.0, 60000),
}
mg = SaisieMoteurs(FAMILLES, "International", lambda fam: "Cummins" if fam.startswith("CUMMINS") else ("International Harvester" if fam.startswith("IH") else "International"))
L = []
IND = "poids lourd, marché nord-américain ; motorisations multiples, données indicatives"

mg(L, "Loadstar", "Loadstar", "1", "1962-01", "1978-12", [("6.4 V8 238", "IH-V8-6.4", 481), ("Diesel 7.6 Turbo 213", "NAV-DT466-7.6", 840, {"debut": "1971-01"})], portes=2, places=3, reservoir=190,
   remarques="Camion moyen à cabine avancée ; " + IND)
mg(L, "Transtar", "Transtar", "1", "1968-01", "1985-12", [("Cummins 14.0 Turbo 355", "CUMMINS-NTC-14.0", 1450)], portes=2, places=2, reservoir=380, remarques="Tracteur routier ; " + IND)
mg(L, "9000 Series", "9000", "1", "1988-01", "2017-12", [("Cummins 15.0 Turbo 456", "CUMMINS-ISX-15.0", 2100)], portes=2, places=2, reservoir=570,
   remarques="Tracteurs 9100 à 9900i (Cummins, Detroit, Caterpillar) ; " + IND)
mg(L, "DuraStar", "DuraStar", "1", "2001-01", "2018-12", [("Diesel 7.6 Turbo 254", "NAV-DT466-7.6", 840)], portes=2, places=3, reservoir=190,
   remarques="Camion moyen (série 4000), DT466 puis MaxxForce DT ; " + IND)
mg(L, "CXT", "CXT", "1", "2004-01", "2008-12", [("Diesel 7.6 Turbo 304", "NAV-DT466-7.6", 1166)], portes=4, places=5, reservoir=265,
   remarques="Pick-up géant dérivé du 7300 (environ 6,6 t) ; " + IND)
mg(L, "LoneStar", "LoneStar", "1", "2008-01", "2023-12", [("MaxxForce 13 12.4 Turbo 482", "NAV-MAXXFORCE13-12.4", 2350), ("Cummins 15.0 Turbo 507", "CUMMINS-ISX-15.0", 2508, {"debut": "2013-01"})],
   portes=2, places=2, reservoir=570, remarques="Tracteur routier à capot rétro ; " + IND)
mg(L, "LT Series", "LT", "1", "2017-01", None, [("A26 12.4 Turbo 482", "NAV-A26-12.4", 2509), ("Cummins X15 15.0 Turbo 507", "CUMMINS-ISX-15.0", 2508)], portes=2, places=2, reservoir=570,
   remarques="Tracteur routier long-courrier ; " + IND)

MOT = Motorisations("International", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"International": L}
MOTEURS = MOT.moteurs()
