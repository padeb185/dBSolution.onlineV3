"""Great Wall (GWM) : générations, phases, motorisations (marché européen) et moteurs liés.
Modèles vendus en Europe : Hover H5 et Steed 5 (première tentative, années 2010), Ora 03 (ex-Funky Cat, 2022-2026), Ora 07 et Wey 05 /
Wey 03 (SUV hybrides rechargeables, ex-Coffee 01 / 02). Haval reste une marque à part ; Tank, Poer et Wingle (hors Europe) ne sont pas
repris. Puissances en ch. Données des modèles anciens et couples indicatifs, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

FAMILLES = {
    "GW-4G69-2.4": f("ATM", "ESS", 2.4, "COURROIE", 4, 5250, 3000, "10W40", 4.5, 10000),
    "GW4D20-2.0D": f("TURBO", "DSL", 2.0, "CHAINE", 4, 4000, 1800, "5W30", 6.0, 10000),
    "GWM-ORA-EV": electrique(),
    "GWM-1.5T-PHEV": f("HYB_TE", "ESS", 1.5, "CHAINE", 4, 5500, 2000, "0W20", 4.5, 15000),
}
mg = SaisieMoteurs(FAMILLES, "Great Wall", lambda fam: "Mitsubishi" if fam == "GW-4G69-2.4" else "Great Wall")
L = []
IND = "données indicatives, à vérifier"

mg(L, "Hover H5", "H5", "1", "2010-01", "2014-12", [("2.4 126", "GW-4G69-2.4", 200), ("2.0 D 143", "GW4D20-2.0D", 305)], portes=5, places=5, reservoir=74,
   remarques="SUV 4x4 (assemblé en Bulgarie par Litex) ; " + IND)
mg(L, "Steed 5", "Wingle 5", "1", "2009-01", "2016-12", [("2.4 126", "GW-4G69-2.4", 200), ("2.0 D 143", "GW4D20-2.0D", 305)], portes=4, places=5, reservoir=70,
   remarques="Pick-up (Wingle 5) ; " + IND)
mg(L, "Ora 03", "Funky Cat", "1", "2022-09", "2026-04", [("Électrique 48 kWh 171", "GWM-ORA-EV", 250, {"batterie": 48}),
                                                       ("Électrique 63 kWh 171", "GWM-ORA-EV", 250, {"batterie": 63})], portes=5, places=5, reservoir=0,
   remarques="Citadine électrique Funky Cat, renommée Ora 03 (2023), retirée du Royaume-Uni en 2026 ; GT 63 kWh ; couple indicatif")
mg(L, "Ora 07", "Lightning Cat", "1", "2023-10", None, [("Pro Électrique 83 kWh 204", "GWM-ORA-EV", 340, {"batterie": 83}),
                                                       ("GT AWD Électrique 83 kWh 408", "GWM-ORA-EV", 680, {"batterie": 83})], portes=4, places=5, reservoir=0,
   remarques="Berline électrique ; couples indicatifs")
mg(L, "Wey 05", "Coffee 01", "1", "2022-09", "2024-12", [("Plug-in Hybrid 1.5 476", "GWM-1.5T-PHEV", 762, {"batterie": 39})], portes=5, places=5, reservoir=55,
   remarques="SUV hybride rechargeable (ex-Coffee 01), 4x4 ; " + IND)
mg(L, "Wey 03", "Coffee 02", "1", "2023-01", None, [("Plug-in Hybrid 1.5 237", "GWM-1.5T-PHEV", 530, {"batterie": 19})], portes=5, places=5, reservoir=55,
   remarques="SUV compact hybride rechargeable (ex-Coffee 02) ; " + IND)

MOT = Motorisations("Great Wall", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Great Wall": L}
MOTEURS = MOT.moteurs()
