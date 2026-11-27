"""Chery : générations, phases, motorisations (marché européen) et moteurs liés.
Gamme européenne de la marque Chery (lancée en 2025, à côté d'Omoda et Jaecoo) : Tiggo 4 (hybride CSH), Tiggo 7 et Tiggo 8
(1.6 TGDI essence et Super Hybrid rechargeable 1.5 TGDI). Les modèles destinés à la Chine et aux marchés émergents (Arrizo, QQ,
Tiggo 3 / 5 / e) ne sont pas repris. Couples des versions hybrides indicatifs.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C = "CHAINE"
FAMILLES = {
    "CHERY-1.6TGDI": f("TURBO", E_, 1.6, C, 4, 5500, 2000, "0W30", 4.5, 15000),
    "CHERY-1.5TGDI-HEV": f("HYB_TE", E_, 1.5, C, 4, 5500, 2000, "0W20", 4.3, 15000),
    "CHERY-1.5TGDI-PHEV": f("HYB_TE", E_, 1.5, C, 4, 5500, 2000, "0W20", 4.3, 15000),
}
mg = SaisieMoteurs(FAMILLES, "Chery", lambda fam: "Chery")
L = []
SH = "Super Hybrid (CSH) rechargeable, batterie LFP 18,3 kWh, boîte DHT ; 204 ch annoncés au Royaume-Uni, 279 ch sur d'autres marchés"

mg(L, "Tiggo 4", "Tiggo 4", "1", "2025-06", None, [("Hybrid 1.5 TGDI 204", "CHERY-1.5TGDI-HEV", 310, {"batterie": 2})], portes=5, places=5, reservoir=51,
   remarques="SUV compact hybride non rechargeable (CSH, batterie 1,83 kWh) ; couple indicatif")
mg(L, "Tiggo 7", "Tiggo 7", "1", "2025-06", None,
   [("1.6 TGDI 147", "CHERY-1.6TGDI", 275), ("Super Hybrid 1.5 TGDI 204", "CHERY-1.5TGDI-PHEV", 365, {"batterie": 18}),
    ("Super Hybrid 1.5 TGDI 279", "CHERY-1.5TGDI-PHEV", 525, {"batterie": 18})], portes=5, places=5, reservoir=51,
   remarques="SUV familial, 1.6 TGDI en traction ou 4x4 (DCT 7) ; " + SH + " ; couples hybrides indicatifs")
mg(L, "Tiggo 8", "Tiggo 8", "1", "2025-07", None,
   [("1.6 TGDI 147", "CHERY-1.6TGDI", 275), ("Super Hybrid 1.5 TGDI 204", "CHERY-1.5TGDI-PHEV", 365, {"batterie": 18}),
    ("Super Hybrid 1.5 TGDI 279", "CHERY-1.5TGDI-PHEV", 525, {"batterie": 18})], portes=5, places=7, reservoir=60,
   remarques="SUV 7 places ; " + SH + " ; couples hybrides indicatifs")

MOT = Motorisations("Chery", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Chery": L}
MOTEURS = MOT.moteurs()
