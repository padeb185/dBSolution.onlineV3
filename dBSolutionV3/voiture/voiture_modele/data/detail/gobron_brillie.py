"""Gobron-Brillié : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur de Boulogne-sur-Seine (1898-1930), moteurs à pistons opposés : Gobron-Nagant (licence belge Nagant, 1900-1903) et
Record (voiture de record, première à dépasser 100 mph en 1904 avec Louis Rigolly). Puissances en ch.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "GOBRON-OP-2.3": f("ATM", "ESS", 2.3, "NC", 2, 1200, 800, "SAE30", 3.0, 1000),
    "GOBRON-OP-13.5": f("ATM", "ESS", 13.5, "NC", 4, 1200, 900, "SAE30", 10.0, 500),
}
mg = SaisieMoteurs(FAMILLES, "Gobron-Brillié", lambda fam: "Gobron-Brillié")
L = []
IND = "moteur à pistons opposés ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Gobron-Nagant", "Gobron-Nagant", "1", "1900-01", "1903-12", [("2.3 10", "GOBRON-OP-2.3", 70)], portes=0, places=4, reservoir=40, remarques="Torpédo et voiturette ; " + IND)
mg(L, "Record", "Record", "1", "1903-01", "1904-12", [("13.5 110", "GOBRON-OP-13.5", 700)], portes=0, places=1, reservoir=60,
   remarques="Voiture de record, 166 km/h à Ostende (1904) ; " + IND)

MOT = Motorisations("Gobron-Brillié", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Gobron-Brillié": L}
MOTEURS = MOT.moteurs()
