"""Li Auto (Lixiang, Pékin) : générations, phases, motorisations (marché chinois) et moteurs liés.
Électriques à prolongateur d'autonomie (EREV : 1.5 turbo de 113 kW servant de générateur, deux moteurs électriques) : ONE, L9, L8, L7, L6 ;
électriques : MEGA (monospace) et i8. Non commercialisée en Europe (marché chinois). Puissances système en ch ; couples indicatifs.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

FAMILLES = {
    "LI-EREV-1.5T": f("HYB_TE", "ESS", 1.5, "CHAINE", 4, 5500, 2000, "0W20", 4.5, 20000),
    "LI-EV": electrique(),
}
mg = SaisieMoteurs(FAMILLES, "Li Auto")
L = []
IND = "marché chinois ; couples indicatifs"
mg(L, "Li ONE", "ONE", "1", "2019-12", "2022-10", [("EREV 41 kWh 333", "LI-EREV-1.5T", 455, {"batterie": 41})], portes=5, places=6, reservoir=45,
   remarques="Premier modèle, trois cylindres 1.2 turbo en générateur ; " + IND)
mg(L, "Li L9", "L9", "1", "2022-06", None, [("EREV 45 kWh 449", "LI-EREV-1.5T", 620, {"batterie": 45, "fin": "2024-02"}), ("EREV 52 kWh 449", "LI-EREV-1.5T", 620, {"batterie": 52, "debut": "2024-03"})],
   portes=5, places=6, reservoir=65, remarques="Grand SUV 6 places ; restylage en mai 2026 ; " + IND)
mg(L, "Li L8", "L8", "1", "2022-09", None, [("EREV 41 kWh 449", "LI-EREV-1.5T", 620, {"batterie": 41, "fin": "2025-04"}), ("EREV 52 kWh 449", "LI-EREV-1.5T", 620, {"batterie": 52, "debut": "2025-05"})],
   portes=5, places=6, reservoir=65, remarques="6 places, puis 5 places depuis juin 2026 ; " + IND)
mg(L, "Li L7", "L7", "1", "2023-02", None, [("EREV 43 kWh 449", "LI-EREV-1.5T", 620, {"batterie": 43, "fin": "2025-04"}), ("EREV 52 kWh 449", "LI-EREV-1.5T", 620, {"batterie": 52, "debut": "2025-05"})],
   portes=5, places=5, reservoir=65, remarques="SUV 5 places ; " + IND)
mg(L, "Li L6", "L6", "1", "2024-04", None, [("EREV 37 kWh 408", "LI-EREV-1.5T", 529, {"batterie": 37, "fin": "2026-06"}), ("EREV 51 kWh 408", "LI-EREV-1.5T", 529, {"batterie": 51, "debut": "2026-07"})],
   portes=5, places=5, reservoir=60, remarques="SUV intermédiaire ; restylage en juillet 2026 (batterie de 51 kWh) ; " + IND)
mg(L, "Li MEGA", "MEGA", "1", "2024-03", None, [("Électrique 103 kWh 544", "LI-EV", 542, {"batterie": 103, "fin": "2026-08"}), ("Électrique 108 kWh 544", "LI-EV", 542, {"batterie": 108, "debut": "2026-09"})],
   portes=5, places=7, reservoir=0, remarques="Monospace électrique 800 V, recharge 5C ; nouvelle génération en septembre 2026 ; " + IND)
mg(L, "Li i8", "i8", "1", "2025-08", None, [("Électrique 98 kWh 544", "LI-EV", 542, {"batterie": 98})], portes=5, places=6, reservoir=0, remarques="SUV électrique 6 places ; " + IND)

MOT = Motorisations("Li Auto", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Li Auto": L}
MOTEURS = MOT.moteurs()
