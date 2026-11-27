"""Freightliner : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Camions lourds de Daimler Truck North America : FLD (1989-2001), Century Class (1995-2010), Columbia (2001-2010), Coronado (2001-2020),
Cascadia (2007-), eCascadia (électrique, 2022-) et M2 (moyen tonnage, 2002-). Diesels Detroit Series 60 / DD13 / DD15 et Cummins
(6.7 repris de ram.py). Puissances SAE converties en ch (× 1,014). Versions représentatives, données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .ram import FAMILLES as FAMILLES_RAM

D = "DSL"
DETROIT = {
    "DETROIT-S60-12.7": f("TURBO", D, 12.7, "NC", 6, 1800, 1200, "15W40", 38.0, 40000),
    "DETROIT-S60-14.0": f("TURBO", D, 14.0, "NC", 6, 1800, 1200, "15W40", 38.0, 40000),
    "DETROIT-DD13": f("TURBO", D, 12.8, "NC", 6, 1625, 1100, "10W30", 40.0, 60000),
    "DETROIT-DD15": f("TURBO", D, 14.8, "NC", 6, 1625, 1000, "10W30", 42.0, 60000),
    "DETROIT-EPOWERTRAIN": electrique(km=40000),
}
CUMMINS = {"CUMMINS-6.7": FAMILLES_RAM["CUMMINS-6.7"]}
FAMILLES = {**DETROIT, **CUMMINS}
mg = SaisieMoteurs(FAMILLES, "Detroit", lambda fam: "Cummins" if fam in CUMMINS else "Detroit")
L = []
NA = "marché nord-américain ; versions représentatives, données indicatives"

mg(L, "FLD", "FLD", "1", "1989-01", "2001-12", [("12.7 Series 60 436", "DETROIT-S60-12.7", 1966)], portes=2, places=2, reservoir=570,
   remarques="Tracteur routier à capot long ; moteurs Cummins et Caterpillar aussi proposés ; " + NA)
mg(L, "Century Class", "Century", "1", "1995-01", "2010-12", [("14.0 Series 60 477", "DETROIT-S60-14.0", 2237)], portes=2, places=2, reservoir=570,
   remarques="Tracteur routier aérodynamique ; " + NA)
mg(L, "Columbia", "Columbia", "1", "2001-01", "2010-12", [("14.0 Series 60 477", "DETROIT-S60-14.0", 2237)], portes=2, places=2, reservoir=570, remarques="Tracteur routier ; " + NA)
mg(L, "Coronado", "Coronado", "1", "2001-01", "2020-12", [("14.0 Series 60 522", "DETROIT-S60-14.0", 2508, {"fin": "2010-12"}), ("DD15 512", "DETROIT-DD15", 2508, {"debut": "2011-01"})],
   portes=2, places=2, reservoir=570, remarques="Tracteur à capot long classique ; " + NA)
mg(L, "Cascadia", "Cascadia", "1", "2007-01", None, [("DD13 456", "DETROIT-DD13", 2237), ("DD15 512", "DETROIT-DD15", 2508)], portes=2, places=2, reservoir=570,
   remarques="Tracteur routier (DD13 370-525 hp, DD15 425-505 hp, Cummins X15) ; nouvelle génération en 2018 ; " + NA)
mg(L, "eCascadia", "eCascadia", "1", "2022-05", None, [("Électrique 291 kWh 324", "DETROIT-EPOWERTRAIN", 1800, {"batterie": 291}),
                                                       ("Électrique 438 kWh 477", "DETROIT-EPOWERTRAIN", 2600, {"batterie": 438})], portes=2, places=2, reservoir=0,
   remarques="Tracteur électrique Detroit ePowertrain, 4x2 (320 / 395 hp) ou 6x4 (425 / 470 hp) ; couples moteurs indicatifs ; " + NA)
mg(L, "M2", "M2", "1", "2002-01", None, [("6.7 Cummins 264", "CUMMINS-6.7", 895)], portes=2, places=3, reservoir=300,
   remarques="Camion porteur moyen tonnage (M2 106 / 112) ; " + NA)

MOT = Motorisations("Freightliner", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Freightliner": L}
MOTEURS = MOT.moteurs()
