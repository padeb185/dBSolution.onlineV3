"""Jonckheere (Roulers / Roeselare, Belgique) : générations, phases, motorisations (marché européen) et moteurs liés.
Carrossier d'autocars sur châssis DAF, Volvo, Scania, Mercedes ou VDL : Bermuda, Mistral, Monaco (autocar à étage) et Arc ; intégré au
groupe VDL (marque VDL Jonckheere jusqu'en 2012). Une motorisation représentative par modèle (le moteur dépend du châssis choisi).
Nombre de portes : 2 (portes de service) ; places : capacité indicative. Puissances en ch. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

D = "DSL"
FAMILLES = {
    "DAF-DKX-11.6": f("TURBO", D, 11.6, "NC", 6, 2200, 1400, "15W40", 30.0, 30000),
    "DAF-XE-12.6": f("TURBO", D, 12.6, "NC", 6, 1900, 1100, "15W40", 35.0, 60000),
    "VOLVO-D12-12.1": f("TURBO", D, 12.1, "NC", 6, 1900, 1100, "15W40", 35.0, 60000),
    "PACCAR-MX-12.9": f("TURBO", D, 12.9, "NC", 6, 1900, 1100, "10W40", 36.0, 80000),
}
mg = SaisieMoteurs(FAMILLES, "DAF", lambda fam: "Volvo" if fam.startswith("VOLVO") else "DAF")
L = []
IND = "autocar ; moteur selon châssis, données indicatives"

mg(L, "Bermuda", "Bermuda", "1", "1978-01", "1990-12", [("Diesel 11.6 Turbo 280", "DAF-DKX-11.6", 1050)], portes=2, places=50, reservoir=400, remarques="Châssis DAF, Volvo, Scania ou Mercedes ; " + IND)
mg(L, "Mistral", "Mistral", "1", "1993-01", "2012-12", [("Diesel 12.6 Turbo 381", "DAF-XE-12.6", 1750)], portes=2, places=50, reservoir=450, remarques="Mistral 50 et 70 ; " + IND)
mg(L, "Monaco", "Monaco", "1", "1990-01", "2012-12", [("Diesel 12.1 Turbo 420", "VOLVO-D12-12.1", 2000)], portes=2, places=80, reservoir=500,
   remarques="Autocar à étage (impériale) ; " + IND)
mg(L, "Arc", "Arc", "1", "2005-01", "2012-12", [("Diesel 12.9 Turbo 410", "PACCAR-MX-12.9", 1900)], portes=2, places=50, reservoir=450, remarques="Sur châssis VDL SB4000 ; " + IND)

MOT = Motorisations("DAF", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Jonckheere": L}
MOTEURS = MOT.moteurs()
