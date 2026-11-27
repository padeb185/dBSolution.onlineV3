"""Case : générations, phases, motorisations (marché nord-américain) et moteurs liés.
J.I. Case (Racine, Wisconsin), constructeur de machines agricoles ayant produit des automobiles (1911-1927) : Model 40 et Model V.
Puissances brutes converties en ch (× 1,014). Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "CASE-5.4": f("ATM", "ESS", 5.4, "NC", 4, 1800, 1000, "SAE30", 6.0, 2000),
    "CONTINENTAL-L6-4.2": f("ATM", "ESS", 4.2, "NC", 6, 2600, 1200, "SAE30", 5.5, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Case", lambda fam: "Continental" if fam.startswith("CONTINENTAL") else "Case")
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Model 40", "40", "1", "1911-01", "1916-12", [("5.4 41", "CASE-5.4", 200)], portes=4, places=5, reservoir=65, remarques="Torpédo ; " + IND)
mg(L, "Model V", "V", "1", "1922-01", "1927-12", [("4.2 L6 51", "CONTINENTAL-L6-4.2", 220)], portes=4, places=5, reservoir=65, remarques="Berline, six cylindres Continental ; " + IND)

MOT = Motorisations("Case", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Case": L}
MOTEURS = MOT.moteurs()
