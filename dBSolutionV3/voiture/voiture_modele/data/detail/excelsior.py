"""Excelsior : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur belge de prestige (Bruxelles puis Zaventem, 1903-1932, repris par Imperia) : Type D (1910-1914), Adex (1920-1926)
et Albert Ier (1923-1929, six cylindres 5.3). Puissances en ch. Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "EXCELSIOR-3.0": f("ATM", "ESS", 3.0, "NC", 4, 1800, 1000, "SAE30", 5.0, 2000),
    "EXCELSIOR-L6-5.3": f("ATM", "ESS", 5.3, "NC", 6, 3000, 1600, "SAE30", 8.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Excelsior", lambda fam: "Excelsior")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Type D", "D", "1", "1910-01", "1914-12", [("3.0 20", "EXCELSIOR-3.0", 110)], portes=4, places=5, reservoir=60, remarques="Torpédo ; " + IND)
mg(L, "Adex", "Adex", "1", "1920-01", "1926-12", [("5.3 L6 100", "EXCELSIOR-L6-5.3", 280)], portes=4, places=5, reservoir=90,
   remarques="Torpédo six cylindres à arbre à cames en tête ; " + IND)
mg(L, "Albert I", "Albert I", "1", "1923-01", "1929-12", [("5.3 L6 130", "EXCELSIOR-L6-5.3", 320)], portes=4, places=5, reservoir=90,
   remarques="Berline et torpédo de prestige, victoires en course (24 Heures de Spa) ; " + IND)

MOT = Motorisations("Excelsior", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Excelsior": L}
MOTEURS = MOT.moteurs()
