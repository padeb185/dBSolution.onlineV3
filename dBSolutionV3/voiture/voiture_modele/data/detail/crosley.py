"""Crosley : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Petites voitures de Cincinnati (Powel Crosley) : CB-41 (bicylindre Waukesha, 1939-1942), CC (1946-1949), Hotshot et Super Sports
(roadsters, 1949-1952) et Farm-O-Road (1950-1952). Quatre cylindres 0.7 COBRA (tôle brasée) puis CIBA (fonte).
Puissances brutes converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
WAUKESHA = {"WAUKESHA-0.6": f("ATM", E_, 0.6, "NC", 2, 4000, 2500, "SAE30", 2.0, 3000, a="PLAT")}
CROSLEY = {
    "CROSLEY-COBRA-0.7": f("ATM", E_, 0.72, "NC", 4, 5400, 3000, "SAE30", 2.8, 3000),
    "CROSLEY-CIBA-0.7": f("ATM", E_, 0.72, "NC", 4, 5400, 3000, "SAE30", 2.8, 3000),
}
FAMILLES = {**WAUKESHA, **CROSLEY}
mg = SaisieMoteurs(FAMILLES, "Crosley", lambda fam: "Waukesha" if fam in WAUKESHA else "Crosley")
L = []
NA = "marché nord-américain ; données indicatives"

mg(L, "CB-41", "CB", "1", "1939-04", "1942-12", [("0.6 13", "WAUKESHA-0.6", 30)], portes=2, places=2, reservoir=30,
   remarques="Berline, cabriolet et utilitaires, bicylindre à plat refroidi par air ; " + NA)
mg(L, "CC", "CC", "1", "1946-01", "1949-12", [("COBRA 0.7 27", "CROSLEY-COBRA-0.7", 44, {"fin": "1948-12"}), ("CIBA 0.7 27", "CROSLEY-CIBA-0.7", 44, {"debut": "1949-01"})],
   portes=2, places=4, reservoir=30, remarques="Berline, break et cabriolet ; " + NA)
mg(L, "Hotshot", "Hotshot", "1", "1949-01", "1952-12", [("CIBA 0.7 27", "CROSLEY-CIBA-0.7", 44)], portes=0, places=2, reservoir=30,
   remarques="Roadster sans portes, freins à disque ; " + NA)
mg(L, "Super Sports", "Hotshot", "2", "1950-01", "1952-12", [("CIBA 0.7 27", "CROSLEY-CIBA-0.7", 44)], portes=2, places=2, reservoir=30,
   remarques="Hotshot à portes ; " + NA)
mg(L, "Farm-O-Road", "Farm-O-Road", "1", "1950-01", "1952-12", [("CIBA 0.7 27", "CROSLEY-CIBA-0.7", 44)], portes=0, places=2, reservoir=30,
   remarques="Petit utilitaire agricole et routier ; " + NA)

MOT = Motorisations("Crosley", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Crosley": L}
MOTEURS = MOT.moteurs()
