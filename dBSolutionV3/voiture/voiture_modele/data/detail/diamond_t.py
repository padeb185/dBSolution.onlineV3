"""Diamond T : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Constructeur de camions de Chicago : Model 201 (pick-up, 1937-1949), Model 968 (camion militaire 6x6, 1941-1945) et Model 980 / 981
(tracteur porte-char, 1940-1945). Six cylindres Hercules essence et diesel. Puissances brutes converties en ch (× 1,014).
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "HERCULES-QXB-3.7": f("ATM", "ESS", 3.7, "NC", 6, 3200, 1400, "SAE30", 6.0, 3000),
    "HERCULES-RXC-8.7": f("ATM", "ESS", 8.7, "NC", 6, 2300, 1200, "SAE30", 11.0, 3000),
    "HERCULES-DFXE-14.6": f("ATM", "DSL", 14.6, "NC", 6, 1600, 1000, "SAE30", 24.0, 5000),
}
mg = SaisieMoteurs(FAMILLES, "Hercules", lambda fam: "Hercules")
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Model 201", "201", "1", "1937-01", "1949-12", [("3.7 L6 74", "HERCULES-QXB-3.7", 230)], portes=2, places=3, reservoir=70, remarques="Pick-up ; " + IND)
mg(L, "Model 968", "968", "1", "1941-01", "1945-12", [("8.7 L6 133", "HERCULES-RXC-8.7", 450)], portes=2, places=2, reservoir=230, remarques="Camion militaire 6x6 4 tonnes ; " + IND)
mg(L, "Model 980", "980", "1", "1940-01", "1945-12", [("14.6 Diesel 188", "HERCULES-DFXE-14.6", 920)], portes=2, places=2, reservoir=380,
   remarques="Tracteur porte-char M20 (980 / 981, treuil) ; " + IND)

MOT = Motorisations("Diamond T", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Diamond T": L}
MOTEURS = MOT.moteurs()
