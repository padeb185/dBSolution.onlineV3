"""SsangYong (KGM depuis 2023) : générations, phases, motorisations (marché européen) et moteurs liés.
Korando (KJ, C, IV, e-Motion), Musso (1993, Sports, Q200 / Grand, EV), Rexton (I, W, G4), Kyron, Actyon (I, Sports, II), Rodius,
Tivoli, XLV et Torres (dont Hybrid et EVX). La marque est devenue KG Mobility (KGM) en 2023 ; les modèles récents gardent ici la
marque SsangYong. Moteurs sous licence Mercedes (2.3, 3.2, 2.9 TD) repris de daewoo.py (mêmes codes) ; diesels Xdi / e-XDi,
essence e-XGi / T-GDI, hybride (BYD) et électriques ajoutés. Données anciennes et hybrides indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .daewoo import FAMILLES as FAMILLES_DAEWOO

E_, D = "ESS", "DSL"
C = "CHAINE"

SY = {
    "MB-2.9D": f("ATM", D, 2.9, C, 5, 4000, 2400, "15W40", 7.5, 10000),
    "D20DT-2.0": f("TURBO", D, 2.0, C, 4, 4000, 1800, "5W30", 7.0, 15000),
    "D27DT-2.7": f("TURBO", D, 2.7, C, 5, 4000, 1800, "5W30", 8.0, 15000),
    "D20DTR-2.0": f("TURBO", D, 2.0, C, 4, 4000, 1500, "5W30", 6.5, 20000),
    "D22DTR-2.2": f("TURBO", D, 2.2, C, 4, 3800, 1600, "5W30", 6.5, 20000),
    "D16DTF-1.6": f("TURBO", D, 1.6, C, 4, 4000, 1500, "5W30", 5.5, 20000),
    "G20-2.0": f("ATM", E_, 2.0, C, 4, 6000, 4000, "5W30", 5.0, 15000),
    "G16-1.6": f("ATM", E_, 1.6, C, 4, 6000, 4600, "5W30", 4.5, 15000),
    "G12GDI-1.2T": f("TURBO", E_, 1.2, C, 3, 5000, 1500, "0W30", 4.5, 15000),
    "G15GDI-1.5T": f("TURBO", E_, 1.5, C, 4, 5500, 1500, "0W30", 4.5, 15000),
    "G15GDI-1.5T-HEV": f("HYB_TE", E_, 1.5, C, 4, 5500, 1500, "0W20", 4.5, 15000),
    "G20GDI-2.0T": f("TURBO", E_, 2.0, C, 4, 5500, 1500, "0W30", 5.5, 15000),
    "SY-EV": electrique(),
}
MB = {k: FAMILLES_DAEWOO[k] for k in ("MB-2.3", "MB-3.2", "MB-2.9TD")}
FAMILLES = {**SY, **MB}


def motoriste(fam):
    return "Mercedes-Benz" if fam in MB else "SsangYong"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "SsangYong", motoriste)
L = []
IND = "données indicatives"
KGM = "vendu sous la marque KGM depuis 2023"

# ---------------------------------------------------------------- licence Mercedes
mg(L, "Musso", "FJ", "1", "1993-09", "2005-12", [("2.3 150", "MB-2.3", 214), ("3.2 220", "MB-3.2", 310, {"debut": "1997-01"}), ("2.9 D 98", "MB-2.9D", 192), ("2.9 TD 120", "MB-2.9TD", 250, {"debut": "1998-01"})],
   portes=5, places=5, reservoir=75, remarques="Vendu aussi sous la marque Daewoo (1998-2002) ; " + IND)
mg(L, "Korando", "KJ", "1", "1996-07", "2006-12", [("2.3 150", "MB-2.3", 214), ("3.2 220", "MB-3.2", 310), ("2.9 D 98", "MB-2.9D", 192), ("2.9 TD 120", "MB-2.9TD", 250)],
   portes=3, places=5, reservoir=70, remarques="Dont cabriolet ; vendu aussi sous la marque Daewoo ; " + IND)
mg(L, "Musso", "Sports", "1", "2002-01", "2006-12", [("2.9 TD 120", "MB-2.9TD", 250), ("3.2 220", "MB-3.2", 310)], portes=4, places=5, reservoir=75, remarques="Pick-up double cabine ; " + IND)
mg(L, "Rexton", "Y200", "1", "2001-09", "2006-06",
   [("2.3 150", "MB-2.3", 214), ("3.2 220", "MB-3.2", 310), ("2.9 TD 120", "MB-2.9TD", 250, {"fin": "2004-12"}), ("2.7 Xdi 163", "D27DT-2.7", 340, {"debut": "2004-01"})],
   portes=5, places=7, reservoir=80, remarques=IND)
mg(L, "Rexton", "Y200", "2", "2006-07", "2012-06", [("2.7 Xdi 165", "D27DT-2.7", 340), ("RX270 2.7 Xdi 186", "D27DT-2.7", 402), ("3.2 220", "MB-3.2", 310, {"fin": "2008-12"})],
   portes=5, places=7, reservoir=80, remarques="Rexton II ; " + IND)
mg(L, "Rexton", "Y290", "1", "2012-07", "2017-06", [("2.0 e-XDi 155", "D20DTR-2.0", 360), ("2.2 e-XDi 178", "D22DTR-2.2", 400, {"debut": "2016-01"})], portes=5, places=7, reservoir=78,
   remarques="Rexton W")

# ---------------------------------------------------------------- années 2000-2010
mg(L, "Kyron", "D100", "1", "2005-09", "2014-12", [("2.0 Xdi 141", "D20DT-2.0", 310), ("2.7 Xdi 165", "D27DT-2.7", 340), ("3.2 220", "MB-3.2", 310, {"fin": "2008-12"})],
   portes=5, places=5, reservoir=75, remarques=IND)
mg(L, "Actyon", "C100", "1", "2005-11", "2011-12", [("2.0 Xdi 141", "D20DT-2.0", 310), ("2.3 150", "MB-2.3", 214)], portes=5, places=5, reservoir=75, remarques="SUV coupé ; " + IND)
mg(L, "Actyon Sports", "Q100", "1", "2006-06", "2012-06", [("2.0 Xdi 141", "D20DT-2.0", 310), ("2.0 e-XDi 155", "D20DTR-2.0", 360, {"debut": "2012-01"})], portes=4, places=5, reservoir=75,
   remarques="Pick-up double cabine")
mg(L, "Rodius", "A100", "1", "2004-09", "2013-06", [("2.7 Xdi 165", "D27DT-2.7", 340), ("3.2 220", "MB-3.2", 310, {"fin": "2007-12"}), ("2.0 e-XDi 155", "D20DTR-2.0", 360, {"debut": "2012-01"})],
   portes=5, places=7, reservoir=80, remarques="Monospace jusqu'à 11 places (Stavic) ; " + IND)
mg(L, "Rodius", "A200", "1", "2013-07", "2019-12", [("2.0 e-XDi 155", "D20DTR-2.0", 360), ("2.2 e-XDi 178", "D22DTR-2.2", 400, {"debut": "2016-01"})], portes=5, places=7, reservoir=80,
   remarques="Turismo")
mg(L, "Korando", "C200", "1", "2010-09", "2019-06",
   [("2.0 e-XDi 175", "D20DTR-2.0", 360), ("2.0 e-XDi 149", "D20DTR-2.0", 360), ("2.0 149", "G20-2.0", 197), ("2.2 e-XDi 178", "D22DTR-2.2", 400, {"debut": "2016-01"})],
   portes=5, places=5, reservoir=57, remarques="Korando C ; restylage 2013")

# ---------------------------------------------------------------- génération actuelle
mg(L, "Tivoli", "X100", "1", "2015-06", "2019-06", [("1.6 e-XGi 128", "G16-1.6", 160), ("1.6 e-XDi 115", "D16DTF-1.6", 300)], portes=5, places=5, reservoir=47)
mg(L, "Tivoli", "X100", "2", "2019-07", None, [("1.2 T-GDI 128", "G12GDI-1.2T", 230), ("1.5 T-GDI 163", "G15GDI-1.5T", 280), ("1.6 e-XDi 136", "D16DTF-1.6", 324, {"fin": "2022-12"})],
   portes=5, places=5, reservoir=47, remarques="Restylage ; " + KGM)
mg(L, "XLV", "X100", "1", "2016-03", "2020-12", [("1.6 e-XGi 128", "G16-1.6", 160), ("1.6 e-XDi 115", "D16DTF-1.6", 300), ("1.5 T-GDI 163", "G15GDI-1.5T", 280, {"debut": "2019-07"})],
   portes=5, places=5, reservoir=47, remarques="Tivoli allongé (Tivoli Grand en 2021)")
mg(L, "Korando", "C300", "1", "2019-03", None,
   [("1.5 T-GDI 163", "G15GDI-1.5T", 280), ("1.6 e-XDi 136", "D16DTF-1.6", 324, {"fin": "2023-12"}), ("e-Motion 190", "SY-EV", 360, el(62, debut="2021-06"))], portes=5, places=5, reservoir=50,
   remarques="Korando IV ; e-Motion électrique ; " + KGM)
mg(L, "Rexton", "Y400", "1", "2017-06", "2020-12", [("2.2 e-XDi 181", "D22DTR-2.2", 420), ("2.0 T-GDI 225", "G20GDI-2.0T", 350, {"fin": "2019-12"})], portes=5, places=7, reservoir=70,
   remarques="Rexton G4")
mg(L, "Rexton", "Y400", "2", "2021-01", None, [("2.2 e-XDi 202", "D22DTR-2.2", 441)], portes=5, places=7, reservoir=70, remarques="Restylage ; " + KGM)
mg(L, "Musso", "Q200", "1", "2018-04", None, [("2.2 e-XDi 181", "D22DTR-2.2", 420, {"fin": "2020-12"}), ("2.2 e-XDi 202", "D22DTR-2.2", 441, {"debut": "2021-01"})],
   portes=4, places=5, reservoir=75, remarques="Pick-up ; Musso Grand (benne longue) ; " + KGM)
mg(L, "Musso", "EV", "1", "2025-08", None, [("EV 207", "SY-EV", 339, el(81))], portes=4, places=5, reservoir=0,
   remarques="Pick-up électrique (dérivé du Torres EVX) ; KGM")
mg(L, "Torres", "J100", "1", "2023-03", None,
   [("1.5 T-GDI 163", "G15GDI-1.5T", 280), ("Hybrid 1.5 T-GDI 204", "G15GDI-1.5T-HEV", 300, {"debut": "2025-10", "batterie": 2, "remarques": "Hybride Dual Tech (BYD) ; puissance système indicative"}),
    ("EVX 207", "SY-EV", 339, el(73, debut="2024-03", fin="2026-04")), ("EVX Grande batterie 207", "SY-EV", 339, el(81, debut="2026-05"))],
   portes=5, places=5, reservoir=50, remarques="KGM")
mg(L, "Actyon", "J120", "1", "2024-11", None,
   [("1.5 T-GDI 163", "G15GDI-1.5T", 280), ("Hybrid 1.5 T-GDI 204", "G15GDI-1.5T-HEV", 300, {"debut": "2026-03", "batterie": 2, "remarques": "Hybride Dual Tech (BYD) ; puissance système indicative"})],
   portes=5, places=5, reservoir=50, remarques="SUV coupé sur base Torres ; KGM")

MOT = Motorisations("SsangYong", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"SsangYong": L}
MOTEURS = MOT.moteurs()
