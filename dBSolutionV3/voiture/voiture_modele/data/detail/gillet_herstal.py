"""Gillet Herstal : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur belge de motos (Herstal, 1919-1959) : Super Sport 500 et 720 RL (moto militaire à side-car tracté, deux-temps).
Puissances en ch. Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "GILLET-0.5": f("ATM", "ESS", 0.5, "NC", 1, 4500, 3000, "SAE30", 2.0, 3000),
    "GILLET-2T-0.72": f("ATM", "ESS", 0.72, "AUCUNE", 2, 4200, 3000, "CHOISIR", 0.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Gillet Herstal", lambda fam: "Gillet Herstal")
L = []
IND = "moto ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Super Sport 500", "Super Sport", "1", "1926-01", "1932-12", [("0.5 22", "GILLET-0.5", 35)], portes=0, places=2, reservoir=14, remarques="Moto sportive monocylindre ; " + IND)
mg(L, "720 RL", "720", "1", "1938-01", "1940-12", [("0.72 2T 22", "GILLET-2T-0.72", 45)], portes=0, places=3, reservoir=20,
   remarques="Moto militaire à side-car à roue motrice, bicylindre deux-temps (armée belge) ; " + IND)

MOT = Motorisations("Gillet Herstal", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Gillet Herstal": L}
MOTEURS = MOT.moteurs()
