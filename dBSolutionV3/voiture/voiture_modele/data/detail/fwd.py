"""FWD (Four Wheel Drive Auto Company) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Constructeur de Clintonville (Wisconsin) de camions à quatre roues motrices : Model B (3 tonnes, 1912-1919) et HAR-1 (1941-1945).
Puissances brutes converties en ch (× 1,014). Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "WISCONSIN-6.4": f("ATM", "ESS", 6.4, "NC", 4, 1500, 900, "SAE30", 8.0, 2000),
    "WAUKESHA-L6-8.4": f("ATM", "ESS", 8.4, "NC", 6, 2400, 1200, "SAE30", 11.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "FWD", lambda fam: "Wisconsin" if fam.startswith("WISCONSIN") else "Waukesha")
L = []
IND = "camion 4x4 ; marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Model B", "B", "1", "1912-01", "1919-12", [("6.4 37", "WISCONSIN-6.4", 230)], portes=2, places=2, reservoir=110,
   remarques="Camion 3 tonnes, largement utilisé pendant la Première Guerre mondiale ; " + IND)
mg(L, "HAR-1", "HAR-1", "1", "1941-01", "1945-12", [("8.4 L6 128", "WAUKESHA-L6-8.4", 440)], portes=2, places=2, reservoir=200, remarques="Camion militaire ; " + IND)

MOT = Motorisations("FWD", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"FWD": L}
MOTEURS = MOT.moteurs()
