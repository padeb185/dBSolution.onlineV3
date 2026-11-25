"""Koenigsegg (Ängelholm, Suède) : générations, phases, motorisations et moteurs liés.
CC8S, CCR, CCX, CCXR (+ Trevita), Agera (R, S, RS), One:1, Regera, Jesko (+ Absolut), CC850, Gemera, Sadair's Spear.
V8 Koenigsegg au motoriste « Koenigsegg » ; puissances maximales au bioéthanol E85 quand elles diffèrent (indiquées en remarque).
Très petites séries : dates indicatives. Prototype CC (1997) et CCGT1 (présentée en 2026, non livrée) non repris.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C = "CHAINE"

FAMILLES = {
    "KOENIGSEGG-V8-4.7S": f("TURBO", E_, 4.7, C, 8, 6500, 5000, "10W60", 12.0, 10000, a="V"),
    "KOENIGSEGG-V8-4.7TT": f("TURBO", E_, 4.7, C, 8, 7000, 5500, "10W60", 12.0, 10000, a="V"),
    "KOENIGSEGG-V8-5.0TT": f("TURBO", E_, 5.0, C, 8, 7800, 4100, "10W60", 12.0, 10000, a="V"),
    "KOENIGSEGG-V8-5.0TT-HYB": f("HYB_E", E_, 5.0, C, 8, 7800, 4100, "10W60", 12.0, 10000, a="V"),
}

E85 = "Puissance maximale au bioéthanol E85"
mg = SaisieMoteurs(FAMILLES, "Koenigsegg")
L = []

mg(L, "CC8S", "CC8S", "1", "2002-03", "2003-12", [("4.7 V8 Compresseur 655", "KOENIGSEGG-V8-4.7S", 750)], portes=2, places=2, reservoir=70,
   remarques="Premier modèle de série, 6 exemplaires ; V8 d'origine Ford Modular")
mg(L, "CCR", "CCR", "1", "2004-03", "2006-12", [("4.7 V8 Compresseur 806", "KOENIGSEGG-V8-4.7S", 920)], portes=2, places=2, reservoir=70,
   remarques="14 exemplaires ; deux compresseurs")
mg(L, "CCX", "CCX", "1", "2006-03", "2010-12", [("4.7 V8 Biturbo 806", "KOENIGSEGG-V8-4.7TT", 920)], portes=2, places=2, reservoir=82,
   remarques="Homologation mondiale (dont États-Unis) ; CCX Edition")
mg(L, "CCXR", "CCX", "1", "2007-06", "2010-12", [("4.7 V8 Biturbo 1018", "KOENIGSEGG-V8-4.7TT", 1060)], portes=2, places=2, reservoir=82,
   remarques=E85 + " ; CCXR Edition")
mg(L, "CCXR Trevita", "CCX", "1", "2009-10", "2010-12", [("4.7 V8 Biturbo 1018", "KOENIGSEGG-V8-4.7TT", 1060)], portes=2, places=2, reservoir=82,
   remarques=E85 + " ; carrosserie en fibre de carbone blanche, 2 exemplaires")
mg(L, "Agera", "Agera", "1", "2011-01", "2013-12", [("5.0 V8 Biturbo 960", "KOENIGSEGG-V8-5.0TT", 1100)], portes=2, places=2, reservoir=80,
   remarques="Agera S (2013, 1 030 ch) non détaillée")
mg(L, "Agera R", "Agera", "1", "2011-06", "2014-12", [("5.0 V8 Biturbo 1140", "KOENIGSEGG-V8-5.0TT", 1200)], portes=2, places=2, reservoir=80, remarques=E85)
mg(L, "One:1", "Agera", "1", "2014-03", "2015-12", [("5.0 V8 Biturbo 1360", "KOENIGSEGG-V8-5.0TT", 1371)], portes=2, places=2, reservoir=80,
   remarques=E85 + " (1 ch par kg) ; 7 exemplaires")
mg(L, "Agera RS", "Agera", "1", "2015-03", "2018-12",
   [("5.0 V8 Biturbo 1176", "KOENIGSEGG-V8-5.0TT", 1280), ("5.0 V8 Biturbo Pack 1MW 1360", "KOENIGSEGG-V8-5.0TT", 1371)], portes=2, places=2, reservoir=80,
   remarques="25 exemplaires ; record de vitesse 2017 (447 km/h de moyenne) ; Agera Final Edition (2018)")
mg(L, "Regera", "Regera", "1", "2016-09", "2022-06", [("5.0 V8 Biturbo Hybride 1500", "KOENIGSEGG-V8-5.0TT-HYB", 2000, {"batterie": 5})], portes=2, places=2,
   reservoir=77, remarques="Hybride rechargeable à transmission directe (Direct Drive), 80 exemplaires ; " + E85)
mg(L, "Jesko", "Jesko", "1", "2021-06", "2025-12", [("5.0 V8 Biturbo 1600", "KOENIGSEGG-V8-5.0TT", 1500)], portes=2, places=2, reservoir=72,
   remarques=E85 + " (1 280 ch à l'essence) ; boîte LST 9 rapports ; Jesko Attack ; 125 exemplaires, date de fin indicative")
mg(L, "Jesko Absolut", "Jesko", "1", "2022-06", "2025-12", [("5.0 V8 Biturbo 1600", "KOENIGSEGG-V8-5.0TT", 1500)], portes=2, places=2, reservoir=72,
   remarques=E85 + " ; version faible traînée pour la vitesse maximale ; date de fin indicative")
mg(L, "CC850", "CC850", "1", "2023-06", None, [("5.0 V8 Biturbo 1385", "KOENIGSEGG-V8-5.0TT", 1385)], portes=2, places=2, reservoir=72,
   remarques=E85 + " ; boîte Engage Shift System (manuelle 6 ou automatique 9) ; hommage à la CC8S ; date indicative")
mg(L, "Gemera", "Gemera HV8", "1", "2026-03", None, [("HV8 5.0 V8 Biturbo Hybride 2300", "KOENIGSEGG-V8-5.0TT-HYB", 2750, {"batterie": 15})], portes=2,
   places=4, reservoir=75, remarques="« Mega-GT » 4 places, 300 exemplaires ; production lancée en mars 2026 ; " + E85)
mg(L, "Sadair's Spear", "Jesko", "1", "2026-06", None, [("5.0 V8 Biturbo 1625", "KOENIGSEGG-V8-5.0TT", 1510)], portes=2, places=2, reservoir=72,
   remarques="Dérivée de la Jesko, 30 exemplaires ; " + E85 + " ; date et couple indicatifs")

MOT = Motorisations("Koenigsegg", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Koenigsegg": L}
MOTEURS = MOT.moteurs()
