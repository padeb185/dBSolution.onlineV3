"""DS Automobiles : générations, phases, motorisations (marché européen) et moteurs liés.
DS3 (ex-Citroën DS3), DS3 Crossback / DS 3, DS4, DS4 Crossback, N°4, DS5, DS7 Crossback / DS 7, N°7, DS9, N°8.
La DS de 1955 reste dans Citroën. Moteurs PSA / Stellantis rattachés au motoriste « DS Automobiles ».
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


FAMILLES = {
    # --- essence
    "EP3": f("ATM", E_, 1.4, C, 4, 6000, 4000, "5W30", 4.25, 20000),
    "EP6": f("ATM", E_, 1.6, C, 4, 6000, 4250, "5W30", 4.25, 20000),
    "EP6DT": f("TURBO", E_, 1.6, C, 4, 6000, 1400, "5W30", 4.25, 20000),
    "EP6CDTR": f("TURBO", E_, 1.6, C, 4, 6000, 1700, "5W30", 4.25, 20000),
    "EP6FDT": f("TURBO", E_, 1.6, C, 4, 5500, 1650, "0W30", 4.25, 25000),
    "EB2": f("ATM", E_, 1.2, B, 3, 5750, 2750, "0W30", 3.5, 25000),
    "EB2DT": f("TURBO", E_, 1.2, B, 3, 5500, 1500, "0W30", 3.5, 25000),
    "EB2DTS": f("TURBO", E_, 1.2, B, 3, 5500, 1750, "0W30", 3.5, 25000),
    "EB2-MHEV": f("HYB_TE", E_, 1.2, C, 3, 5500, 1750, "0W20", 3.5, 25000),
    "EP6-PHEV": f("HYB_E", E_, 1.6, C, 4, 6000, 3000, "0W30", 4.25, 25000),
    # --- diesel
    "DV4": f("TURBO", D, 1.4, B, 4, 4000, 1750, "5W30", 3.75, 20000),
    "DV6C": f("TURBO", D, 1.6, B, 4, 3600, 1750, "5W30", 3.75, 20000),
    "DV6F": f("TURBO", D, 1.6, B, 4, 3500, 1750, "0W30", 3.75, 25000),
    "DV5": f("TURBO", D, 1.5, C, 4, 3750, 1750, "0W30", 3.5, 25000),
    "DW10C": f("TURBO", D, 2.0, B, 4, 3750, 2000, "5W30", 5.25, 20000),
    "DW10F": f("TURBO", D, 2.0, B, 4, 3750, 2000, "0W30", 5.25, 25000),
    "DW10-HYB4": f("HYB_TE", D, 2.0, B, 4, 3750, 1750, "5W30", 5.25, 20000),
    # --- électriques
    "e-CMP": electrique(), "STLA-M-EV": electrique(), "eVMP-EV": electrique(),
}

mg = SaisieMoteurs(FAMILLES, "DS Automobiles")
L = []

# ---------------------------------------------------------------- DS3
mg(L, "DS3", "A55", "1", "2009-11", "2016-05",
   [("1.4 VTi 95", "EP3", 136), ("1.6 VTi 120", "EP6", 160), ("1.2 VTi 82", "EB2", 118, {"debut": "2012-09"}),
    ("1.6 THP 150", "EP6DT", 240, {"fin": "2012-12"}), ("1.6 THP 155", "EP6CDTR", 240, {"debut": "2013-01"}),
    ("Racing 1.6 THP 207", "EP6DT", 275, {"debut": "2010-12", "fin": "2013-12"}),
    ("1.4 HDi 70", "DV4", 160, {"fin": "2013-12"}), ("1.6 HDi 90", "DV6C", 215, {"fin": "2012-06"}),
    ("1.6 e-HDi 92", "DV6C", 230, {"debut": "2012-07"}), ("1.6 HDi 110", "DV6C", 240, {"fin": "2012-06"}),
    ("1.6 e-HDi 115", "DV6C", 270, {"debut": "2012-07"}), ("1.6 BlueHDi 100", "DV6F", 254, {"debut": "2014-09"}),
    ("1.6 BlueHDi 120", "DV6F", 285, {"debut": "2014-09"})], portes=3, places=4, reservoir=50,
   remarques="Vendue Citroën DS3 jusqu'en 2015 ; DS3 Cabrio (2013)")
mg(L, "DS3", "A55", "2", "2016-06", "2019-07",
   [("1.2 PureTech 82", "EB2", 118), ("1.2 PureTech 110", "EB2DT", 205), ("1.2 PureTech 130", "EB2DTS", 230),
    ("Performance 1.6 THP 208", "EP6CDTR", 300), ("1.6 BlueHDi 100", "DV6F", 254), ("1.6 BlueHDi 120", "DV6F", 285)],
   portes=3, places=4, reservoir=50, remarques="Restylage DS 3 et DS 3 Cabrio")
mg(L, "DS3", "D34", "1", "2019-05", "2022-12",
   [("1.2 PureTech 100", "EB2DT", 205), ("1.2 PureTech 130", "EB2DTS", 230), ("1.2 PureTech 155", "EB2DTS", 240),
    ("1.5 BlueHDi 100", "DV5", 250), ("1.5 BlueHDi 130", "DV5", 300), ("E-Tense 136", "e-CMP", 260, el(50))],
   reservoir=44, remarques="DS 3 Crossback (SUV urbain)")
mg(L, "DS3", "D34", "2", "2023-01", None,
   [("1.2 PureTech 100", "EB2DT", 205, {"fin": "2024-06"}), ("1.2 PureTech 130", "EB2DTS", 230, {"fin": "2024-06"}),
    ("1.5 BlueHDi 130", "DV5", 300, {"fin": "2024-06"}), ("1.2 Hybrid 136", "EB2-MHEV", 230, {"debut": "2024-03"}),
    ("E-Tense 156", "e-CMP", 260, el(54))], reservoir=44, remarques="DS 3 (restylage, sans « Crossback »)")

# ---------------------------------------------------------------- DS4 / N°4
mg(L, "DS4", "B75", "1", "2011-05", "2015-08",
   [("1.6 VTi 120", "EP6", 160), ("1.6 THP 155", "EP6CDTR", 240), ("1.6 THP 200", "EP6CDTR", 275),
    ("1.6 e-HDi 110", "DV6C", 270), ("2.0 HDi 160", "DW10C", 340)], reservoir=60, remarques="Vendue Citroën DS4 jusqu'en 2015")
mg(L, "DS4", "B75", "2", "2015-09", "2018-06",
   [("1.2 PureTech 130", "EB2DTS", 230), ("1.6 THP 165", "EP6CDTR", 240), ("1.6 THP 210", "EP6CDTR", 300),
    ("1.6 BlueHDi 120", "DV6F", 300), ("2.0 BlueHDi 150", "DW10F", 370), ("2.0 BlueHDi 180", "DW10F", 400)],
   reservoir=60, remarques="DS 4 restylée")
mg(L, "DS4 Crossback", "B75", "2", "2015-09", "2018-06",
   [("1.2 PureTech 130", "EB2DTS", 230), ("1.6 THP 165", "EP6CDTR", 240), ("1.6 BlueHDi 120", "DV6F", 300),
    ("2.0 BlueHDi 180", "DW10F", 400)], reservoir=60, remarques="DS 4 surélevée")
mg(L, "DS4", "D41", "1", "2021-09", "2025-05",
   [("1.2 PureTech 130", "EB2DTS", 230), ("1.6 PureTech 180", "EP6FDT", 250), ("1.6 PureTech 225", "EP6FDT", 300),
    ("1.5 BlueHDi 130", "DV5", 300), ("E-Tense 225", "EP6-PHEV", 360, ph(12, 40)),
    ("1.2 Hybrid 136", "EB2-MHEV", 230, {"debut": "2024-03"})], reservoir=52, remarques="Berline compacte (EMP2) ; Cross et Performance Line")
mg(L, "N°4", "D41", "2", "2025-06", None,
   [("1.2 Hybrid 145", "EB2-MHEV", 230), ("E-Tense 225", "EP6-PHEV", 360, ph(12, 40)), ("1.5 BlueHDi 130", "DV5", 300),
    ("E-Tense 213", "eVMP-EV", 343, el(58))], reservoir=52, remarques="Restylage de la DS 4, renommée N°4")

# ---------------------------------------------------------------- DS5
mg(L, "DS5", "B81", "1", "2011-11", "2015-06",
   [("1.6 THP 155", "EP6CDTR", 240), ("1.6 THP 200", "EP6CDTR", 275), ("1.6 HDi 110", "DV6C", 240),
    ("1.6 e-HDi 115", "DV6C", 270, {"debut": "2013-06"}), ("2.0 HDi 160", "DW10C", 340), ("Hybrid4 200", "DW10-HYB4", 450)],
   reservoir=60, remarques="Vendue Citroën DS5 jusqu'en 2015")
mg(L, "DS5", "B81", "2", "2015-07", "2018-05",
   [("1.6 THP 165", "EP6CDTR", 240), ("1.6 THP 210", "EP6CDTR", 300), ("1.6 BlueHDi 120", "DV6F", 300),
    ("2.0 BlueHDi 150", "DW10F", 370), ("2.0 BlueHDi 180", "DW10F", 400), ("Hybrid4 200", "DW10-HYB4", 450, {"fin": "2016-12"})],
   reservoir=60, remarques="DS 5 restylée")

# ---------------------------------------------------------------- DS7 / N°7
mg(L, "DS7", "X74", "1", "2018-02", "2022-06",
   [("1.2 PureTech 130", "EB2DTS", 230), ("1.6 PureTech 180", "EP6FDT", 250), ("1.6 PureTech 225", "EP6FDT", 300),
    ("1.5 BlueHDi 130", "DV5", 300), ("2.0 BlueHDi 180", "DW10F", 400),
    ("E-Tense 4x4 300", "EP6-PHEV", 520, ph(13, 43, debut="2019-10")), ("E-Tense 225", "EP6-PHEV", 360, ph(13, 43, debut="2020-09"))],
   reservoir=62, remarques="DS 7 Crossback")
mg(L, "DS7", "X74", "2", "2022-07", "2026-09",
   [("1.2 PureTech 130", "EB2DTS", 230, {"fin": "2023-12"}), ("1.5 BlueHDi 130", "DV5", 300),
    ("E-Tense 225", "EP6-PHEV", 360, ph(14, 43)), ("E-Tense 4x4 300", "EP6-PHEV", 520, ph(14, 43)),
    ("E-Tense 4x4 360", "EP6-PHEV", 520, ph(14, 43, debut="2022-09"))], reservoir=62, remarques="DS 7 (restylage, sans « Crossback »)")
mg(L, "N°7", "STLA-M", "1", "2026-10", None,
   [("1.2 Hybrid 145", "EB2-MHEV", 230, {"reservoir": 52}), ("E-Tense 230", "STLA-M-EV", 343, el(74)),
    ("E-Tense 245", "STLA-M-EV", 343, el(97)), ("E-Tense 4x4 350", "STLA-M-EV", 509, el(97))], reservoir=0,
   remarques="2e génération du DS 7 (STLA Medium) ; commandes mai 2026, livraisons octobre 2026 ; batteries indicatives")

# ---------------------------------------------------------------- DS9 / N°8
mg(L, "DS9", "X83", "1", "2021-01", None,
   [("1.6 PureTech 225", "EP6FDT", 300, {"fin": "2022-12"}), ("E-Tense 225", "EP6-PHEV", 360, ph(12, 51, fin="2022-06")),
    ("E-Tense 250", "EP6-PHEV", 360, ph(14, 51, debut="2022-07")), ("E-Tense 4x4 360", "EP6-PHEV", 520, ph(14, 51, debut="2022-01"))],
   portes=4, reservoir=51, remarques="Grande berline (produite en Chine) ; fin de commercialisation à vérifier")
mg(L, "N°8", "STLA-M", "1", "2025-03", None,
   [("E-Tense 230", "STLA-M-EV", 343, el(74)),
    ("E-Tense 245", "STLA-M-EV", 343, el(97)), ("E-Tense 4x4 350", "STLA-M-EV", 509, el(97))], reservoir=0,
   remarques="Crossover coupé 100 % électrique (STLA Medium), jusqu'à 750 km WLTP")

MOT = Motorisations("DS Automobiles", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"DS Automobiles": L}
MOTEURS = MOT.moteurs()
