"""Haval (Great Wall Motor) : générations, phases, motorisations (marché européen) et moteurs liés.
Première présence par importateurs (H6 1re génération et H2, années 2010), puis lancement officiel : Jolion Pro Hybrid au Royaume-Uni
(février 2025), H6 Hybrid (janvier 2026) et Jolion Pro 1.5 Turbo (février 2026) en Allemagne. Modèles chinois et australiens
(H1, H4, H5, H7, H8, H9, Jolion de 1re génération) non repris. Moteur diesel repris de great_wall.py. Puissances en ch ; batterie
des hybrides non rechargeables arrondie. Données des modèles anciens indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .great_wall import FAMILLES as FAMILLES_GW

E_ = "ESS"
C = "CHAINE"

FAMILLES = {
    "GW4G15-1.5T": f("TURBO", E_, 1.5, C, 4, 5600, 2000, "5W30", 4.2, 10000),
    "GW4B15-1.5T": f("TURBO", E_, 1.5, C, 4, 5500, 1500, "0W20", 4.5, 15000),
    "GW4B15-1.5T-HEV": f("HYB_TE", E_, 1.5, C, 4, 6000, 4400, "0W20", 4.5, 15000),
    "GW4D20-2.0D": FAMILLES_GW["GW4D20-2.0D"],
}
mg = SaisieMoteurs(FAMILLES, "Great Wall")
L = []
IND = "données indicatives"

mg(L, "H6", "H6 (1re gén.)", "1", "2013-01", "2017-12", [("1.5 Turbo 150", "GW4G15-1.5T", 210), ("2.0 D 143", "GW4D20-2.0D", 305)], portes=5, places=5, reservoir=58,
   remarques="Vendu par des importateurs (Italie, Bulgarie) ; " + IND)
mg(L, "H2", "H2", "1", "2015-01", "2019-12", [("1.5 Turbo 150", "GW4G15-1.5T", 210)], portes=5, places=5, reservoir=50,
   remarques="Petit SUV vendu par des importateurs (Italie, Bulgarie) ; " + IND)
mg(L, "H6", "H6 (3e gén.)", "1", "2026-01", None, [("Hybrid 1.5 Turbo 243", "GW4B15-1.5T-HEV", 530, {"batterie": 2})], portes=5, places=5, reservoir=61,
   remarques="Hybride non rechargeable (DHT), 1.5 Turbo 150 ch + moteur électrique 177 ch, traction ; lancé en Allemagne en janvier 2026")
mg(L, "Jolion Pro", "Jolion Pro", "1", "2025-02", None,
   [("Hybrid 1.5 Turbo 189", "GW4B15-1.5T-HEV", 375, {"batterie": 2}), ("1.5 Turbo 177", "GW4B15-1.5T", 270, {"debut": "2026-02"})],
   portes=5, places=5, reservoir=55,
   remarques="Hybrid (DHT) au Royaume-Uni dès février 2025 ; 1.5 Turbo DCT7 en Allemagne dès février 2026 ; réservoir indicatif")

MOT = Motorisations("Great Wall", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Haval": L}
MOTEURS = MOT.moteurs()
