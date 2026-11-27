"""Cunningham : générations, phases, motorisations (marché nord-américain) et moteurs liés.
James Cunningham, Son & Co. (Rochester) : V8 Model 1 (1916-1931) ; B.S. Cunningham Company (Briggs Cunningham) : C-3 (coupé et
cabriolet de route, 1952-1955) et C-4R (voiture de course, Le Mans 1952-1953), à V8 Chrysler Hemi 5.4.
Puissances brutes converties en ch (× 1,014). Données indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .facel_vega import FAMILLES as FAMILLES_FACEL

CUNNINGHAM = {"CUNNINGHAM-V8-7.2": f("ATM", "ESS", 7.2, "NC", 8, 2400, 1200, "SAE30", 8.0, 3000, a="V")}
CHRYSLER = {"CHRYSLER-HEMI-5.4": FAMILLES_FACEL["CHRYSLER-HEMI-5.4"]}
FAMILLES = {**CUNNINGHAM, **CHRYSLER}
mg = SaisieMoteurs(FAMILLES, "Cunningham", lambda fam: "Chrysler" if fam in CHRYSLER else "Cunningham")
L = []
IND = "marché nord-américain ; données indicatives (marque ancienne), à vérifier"

mg(L, "V8 Model 1", "V8", "1", "1916-01", "1931-12", [("7.2 V8 91", "CUNNINGHAM-V8-7.2", 340)], portes=4, places=5, reservoir=90, remarques="Torpédo, berline et limousine ; " + IND)
mg(L, "C-3", "C-3", "1", "1952-01", "1955-12", [("5.4 V8 223", "CHRYSLER-HEMI-5.4", 447)], portes=2, places=2, reservoir=90,
   remarques="Coupé et cabriolet carrossés par Vignale, environ 25 exemplaires ; " + IND)
mg(L, "C-4R", "C-4R", "1", "1952-01", "1953-12", [("5.4 V8 330", "CHRYSLER-HEMI-5.4", 515)], portes=0, places=2, reservoir=150,
   remarques="Barquette de course (4e aux 24 Heures du Mans 1952) ; " + IND)

MOT = Motorisations("Cunningham", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Cunningham": L}
MOTEURS = MOT.moteurs()
