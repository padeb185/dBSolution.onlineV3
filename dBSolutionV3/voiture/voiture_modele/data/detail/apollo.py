"""Apollo (Apollo Automobil, Denkendorf, ex-Gumpert) : générations, motorisations et moteurs liés.
Apollo N, Intensa Emozione et EVO. La Gumpert Apollo (2005-2013) reste dans la marque Gumpert.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "AUDI-V8-4.2BT": f("TURBO", "ESS", 4.2, "CHAINE", 8, 6800, 4000, "5W40", 9.0, 10000, a="V"),
    "F140-6.3": f("ATM", "ESS", 6.3, "CHAINE", 12, 9000, 6000, "5W40", 15.0, 10000, a="V"),
}

mg = SaisieMoteurs(FAMILLES, "Apollo")
L = []

mg(L, "N", "N", "1", "2016-01", "2016-12", [("N 4.2 V8 Biturbo 800", "AUDI-V8-4.2BT", 1000)], portes=2, places=2, reservoir=100,
   remarques="Évolution de la Gumpert Apollo (V8 Audi biturbo) ; production très limitée, données indicatives")
mg(L, "Intensa Emozione", "IE", "1", "2018-01", "2021-12", [("IE 6.3 V12 780", "F140-6.3", 760)], portes=2, places=2, reservoir=90,
   remarques="Hypercar homologuée route, V12 atmosphérique d'origine Ferrari, 10 exemplaires")
mg(L, "EVO", "EVO", "1", "2026-07", None, [("EVO 6.3 V12 800", "F140-6.3", 765)], portes=2, places=2, reservoir=90,
   remarques="Hypercar réservée à la piste (non homologuée route), 10 exemplaires ; première livraison à Goodwood 2026")

MOT = Motorisations("Apollo", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Apollo": L}
MOTEURS = MOT.moteurs()
