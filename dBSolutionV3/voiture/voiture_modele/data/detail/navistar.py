"""Navistar (Lisle, Illinois) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
MXT (pick-up géant, 2006-2008, V8 diesel VT365). Les camions Navistar sont vendus sous la marque International (voir international.py) ;
« MaxxForce » désigne une gamme de moteurs (pas un véhicule) et n'est pas repris comme modèle. Puissances hp converties en ch (× 1,014).
Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "NAV-VT365-6.0": f("TURBO", "DSL", 6.0, "CHAINE", 8, 3300, 2000, "15W40", 14.0, 15000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "International")
L = []
mg(L, "MXT", "MXT", "1", "2006-01", "2008-12", [("Diesel V8 6.0 Turbo 304", "NAV-VT365-6.0", 834)], portes=4, places=5, reservoir=150,
   remarques="Pick-up géant dérivé du CXT, 4x4 ; marché nord-américain ; données indicatives")

MOT = Motorisations("International", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Navistar": L}
MOTEURS = MOT.moteurs()
