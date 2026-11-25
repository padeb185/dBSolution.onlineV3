"""Gumpert (Gumpert Sportwagenmanufaktur, Altenburg, 2004-2013) : générations, phases, motorisations et moteurs liés.
Apollo (Basic, Sport, Speed) et Tornante. Moteur V8 Audi 4.2 biturbo repris d'apollo.py (même famille, même motoriste
« Apollo », mêmes codes) ; la marque Apollo (N, IE, EVO) est traitée dans apollo.py.
Très petites séries : données indicatives. Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ;
la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .apollo import FAMILLES as FAMILLES_APOLLO

FAMILLES = {"AUDI-V8-4.2BT": FAMILLES_APOLLO["AUDI-V8-4.2BT"]}

mg = SaisieMoteurs(FAMILLES, "Apollo")
L = []

mg(L, "Apollo", "Apollo", "1", "2005-06", "2012-12",
   [("Basic 4.2 V8 Biturbo 650", "AUDI-V8-4.2BT", 850), ("Sport 4.2 V8 Biturbo 700", "AUDI-V8-4.2BT", 878, {"debut": "2008-01"}),
    ("Speed 4.2 V8 Biturbo 800", "AUDI-V8-4.2BT", 1000, {"debut": "2009-01"})], portes=2, places=2, reservoir=120,
   remarques="Supercar homologuée route à châssis tubulaire, V8 Audi biturbo ; insolvabilité de Gumpert en 2012-2013 ; données indicatives")
mg(L, "Tornante", "Tornante", "1", "2011-03", "2012-12", [("4.2 V8 Biturbo 700", "AUDI-V8-4.2BT", 878)], portes=2, places=4, reservoir=100,
   remarques="GT 2+2 carrossée par Touring Superleggera, présentée à Genève 2011 ; quelques exemplaires seulement, données indicatives")

MOT = Motorisations("Apollo", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Gumpert": L}
MOTEURS = MOT.moteurs()
