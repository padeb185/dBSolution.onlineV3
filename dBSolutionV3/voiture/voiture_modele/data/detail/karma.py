"""Karma (Karma Automotive, Irvine, Californie) : générations, phases, motorisations et moteurs liés.
Héritière de Fisker Automotive (rachat par Wanxiang, 2014) : Revero (2017-2019), Revero GT (2020), GS-6 (2021-2023, puis à nouveau
Revero), GSe-6 électrique, et Gyesera (EREV, 2025-) ; Kaveya et Amaris non encore produits. Électriques à prolongateur d'autonomie
(moteur thermique servant de générateur). Puissances hp converties en ch (× 1,014). Données indicatives (très petites séries).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

FAMILLES = {
    "KARMA-EREV-2.0": f("HYB_TE", "ESS", 2.0, "CHAINE", 4, 5500, 2000, "5W30", 5.0, 15000),
    "KARMA-EREV-1.5": f("HYB_TE", "ESS", 1.5, "CHAINE", 3, 5000, 1500, "0W30", 4.5, 15000),
    "KARMA-EV": electrique(),
}
mg = SaisieMoteurs(FAMILLES, "Karma")
L = []
IND = "marché nord-américain ; données indicatives"
mg(L, "Revero", "Revero", "1", "2016-09", "2019-12", [("EREV 409", "KARMA-EREV-2.0", 1330, {"batterie": 21})], portes=4, places=4, reservoir=40,
   remarques="Ex-Fisker Karma, deux moteurs électriques arrière, quatre cylindres 2.0 turbo GM en générateur ; " + IND)
mg(L, "Revero", "Revero", "2", "2020-01", "2020-12", [("GT EREV 543", "KARMA-EREV-1.5", 746, {"batterie": 28})], portes=4, places=4, reservoir=40,
   remarques="Revero GT : trois cylindres 1.5 turbo BMW en générateur ; " + IND)
mg(L, "GS-6", "Revero", "3", "2021-01", "2025-12", [("EREV 543", "KARMA-EREV-1.5", 746, {"batterie": 28})], portes=4, places=4, reservoir=40,
   remarques="Renommée Revero en 2024 ; environ 1 000 Revero / GS-6 produites au total ; " + IND)
mg(L, "GSe-6", "Revero", "E", "2021-01", "2022-12", [("Électrique 543", "KARMA-EV", 746, {"batterie": 104})], portes=4, places=4, reservoir=0, remarques="Version 100 % électrique ; " + IND)
mg(L, "Gyesera", "Gyesera", "1", "2025-12", None, [("EREV 574", "KARMA-EREV-1.5", 740, {"batterie": 28})], portes=4, places=4, reservoir=40,
   remarques="Grand coupé EREV succédant au Revero, moteur électrique arrière de 566 hp ; " + IND)

MOT = Motorisations("Karma", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Karma": L}
MOTEURS = MOT.moteurs()
