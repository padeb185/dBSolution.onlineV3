"""Lamborghini : générations, phases, motorisations et moteurs liés.
350 GT, 400 GT, Miura, Islero, Espada, Jarama, Urraco, Countach, Jalpa, LM002, Diablo, Murciélago, Reventón, Gallardo,
Aventador, Huracán, Urus, Sián, Essenza SCV12, Countach LPI 800-4, Revuelto, Temerario, Fenomeno.
V12, V8 et V10 5.0 propres au motoriste « Lamborghini » ; V10 5.2 FSI et V8 4.0 TFSI du groupe repris d'audi.py
(motoriste « Audi », mêmes codes). Données des modèles anciens indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .audi import FAMILLES as FAMILLES_AUDI

E_ = "ESS"
C = "CHAINE"

PROPRES = {
    "LAMBO-V12-3.5": f("ATM", E_, 3.5, C, 12, 6500, 4500, "20W50", 12.0, 5000, a="V"),
    "LAMBO-V12-3.9": f("ATM", E_, 3.9, C, 12, 7000, 5000, "20W50", 12.0, 5000, a="V"),
    "LAMBO-V12-4.8": f("ATM", E_, 4.8, C, 12, 7000, 4500, "20W50", 13.0, 5000, a="V"),
    "LAMBO-V12-5.2": f("ATM", E_, 5.2, C, 12, 7000, 5200, "10W60", 13.0, 7500, a="V"),
    "LAMBO-V12-5.7": f("ATM", E_, 5.7, C, 12, 7000, 5200, "10W60", 14.0, 7500, a="V"),
    "LAMBO-V12-6.0": f("ATM", E_, 6.0, C, 12, 7500, 5500, "10W60", 14.0, 7500, a="V"),
    "LAMBO-V12-6.2": f("ATM", E_, 6.2, C, 12, 7500, 5400, "10W60", 14.0, 15000, a="V"),
    "LAMBO-V12-6.5": f("ATM", E_, 6.5, C, 12, 8250, 5500, "5W40", 15.0, 15000, a="V"),
    "LAMBO-V12-6.5-SCAP": f("HYB_E", E_, 6.5, C, 12, 8500, 6750, "5W40", 15.0, 15000, a="V"),
    "LAMBO-V12-6.5-PHEV": f("HYB_E", E_, 6.5, C, 12, 9250, 6750, "5W40", 15.0, 15000, a="V"),
    "LAMBO-V8-2.5": f("ATM", E_, 2.5, C, 8, 7500, 5750, "20W50", 9.0, 5000, a="V"),
    "LAMBO-V8-3.0": f("ATM", E_, 3.0, C, 8, 7500, 5750, "20W50", 9.0, 5000, a="V"),
    "LAMBO-V8-3.5": f("ATM", E_, 3.5, C, 8, 7000, 3500, "20W50", 9.0, 5000, a="V"),
    "LAMBO-V10-5.0": f("ATM", E_, 5.0, C, 10, 7800, 4500, "5W40", 9.0, 15000, a="V"),
    "LAMBO-V8-4.0TT-HYB": f("HYB_E", E_, 4.0, C, 8, 9750, 4000, "0W40", 10.0, 15000, a="V"),
}
AUDI = {k: FAMILLES_AUDI[k] for k in ("V10-5.2FSI", "V8-4.0TFSI", "V8-4.0PHEV")}
FAMILLES = {**PROPRES, **AUDI}


def el(kwh, **kw):
    return {"batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Lamborghini", lambda fam: "Audi" if fam in AUDI else "Lamborghini")
L = []

# ---------------------------------------------------------------- Ferruccio Lamborghini
mg(L, "350 GT", "350 GT", "1", "1964-03", "1966-12", [("3.5 V12 280", "LAMBO-V12-3.5", 325)], portes=2, places=2, reservoir=80,
   remarques="V12 Bizzarrini ; 120 exemplaires ; données indicatives")
mg(L, "400 GT", "400 GT", "1", "1966-03", "1968-12", [("3.9 V12 320", "LAMBO-V12-3.9", 373)], portes=2, places=4, reservoir=80,
   remarques="2+2 ; données indicatives")
mg(L, "Miura", "Miura", "1", "1966-12", "1973-01",
   [("P400 3.9 V12 350", "LAMBO-V12-3.9", 355, {"fin": "1969-03"}), ("P400 S 3.9 V12 370", "LAMBO-V12-3.9", 388, {"debut": "1969-01", "fin": "1971-03"}),
    ("P400 SV 3.9 V12 385", "LAMBO-V12-3.9", 400, {"debut": "1971-03"})], portes=2, places=2, reservoir=90, remarques="V12 central transversal ; données indicatives")
mg(L, "Islero", "Islero", "1", "1968-03", "1969-12", [("3.9 V12 320", "LAMBO-V12-3.9", 373), ("S 3.9 V12 350", "LAMBO-V12-3.9", 392, {"debut": "1969-01"})],
   portes=2, places=4, reservoir=85, remarques="Données indicatives")
mg(L, "Espada", "Espada", "1", "1968-03", "1978-06",
   [("3.9 V12 325", "LAMBO-V12-3.9", 376, {"fin": "1970-03"}), ("Series II 3.9 V12 350", "LAMBO-V12-3.9", 392, {"debut": "1970-03"})], portes=2, places=4,
   reservoir=93, remarques="GT 4 places ; Series III (1972) ; données indicatives")
mg(L, "Jarama", "Jarama", "1", "1970-03", "1976-12", [("GT 3.9 V12 350", "LAMBO-V12-3.9", 392), ("GTS 3.9 V12 365", "LAMBO-V12-3.9", 400, {"debut": "1972-03"})],
   portes=2, places=4, reservoir=93, remarques="Données indicatives")
mg(L, "Urraco", "Urraco", "1", "1973-01", "1979-12",
   [("P250 2.5 V8 220", "LAMBO-V8-2.5", 225), ("P300 3.0 V8 265", "LAMBO-V8-3.0", 275, {"debut": "1975-01"})], portes=2, places=4, reservoir=80,
   remarques="2+2 à moteur central ; P200 (Italie) non reprise ; données indicatives")
mg(L, "Jalpa", "Jalpa", "1", "1981-03", "1988-12", [("3.5 V8 255", "LAMBO-V8-3.5", 320)], portes=2, places=2, reservoir=80, remarques="Targa ; données indicatives")
mg(L, "Countach", "Countach", "1", "1974-03", "1990-07",
   [("LP400 3.9 V12 375", "LAMBO-V12-3.9", 368, {"fin": "1978-03"}), ("LP400 S 3.9 V12 353", "LAMBO-V12-3.9", 361, {"debut": "1978-03", "fin": "1982-03"}),
    ("LP500 S 4.8 V12 375", "LAMBO-V12-4.8", 410, {"debut": "1982-03", "fin": "1985-03"}),
    ("5000 Quattrovalvole 5.2 V12 455", "LAMBO-V12-5.2", 500, {"debut": "1985-03"})], portes=2, places=2, reservoir=120,
   remarques="25th Anniversary (1988) ; données indicatives")
mg(L, "LM002", "LM002", "1", "1986-01", "1993-12", [("5.2 V12 450", "LAMBO-V12-5.2", 500)], portes=4, places=5, reservoir=290,
   remarques="Tout-terrain, 301 exemplaires ; données indicatives")

# ---------------------------------------------------------------- V12
mg(L, "Diablo", "Diablo", "1", "1990-01", "1998-12",
   [("5.7 V12 492", "LAMBO-V12-5.7", 580), ("VT 5.7 V12 492", "LAMBO-V12-5.7", 580, {"debut": "1993-01"}), ("SV 5.7 V12 510", "LAMBO-V12-5.7", 580, {"debut": "1995-06"})],
   portes=2, places=2, reservoir=100, remarques="VT à transmission intégrale, Roadster (1995) ; données indicatives")
mg(L, "Diablo", "Diablo", "2", "1999-01", "2001-12",
   [("VT 5.7 V12 530", "LAMBO-V12-5.7", 605, {"fin": "1999-12"}), ("SV 5.7 V12 530", "LAMBO-V12-5.7", 605, {"fin": "1999-12"}),
    ("GT 6.0 V12 575", "LAMBO-V12-6.0", 630), ("VT 6.0 V12 550", "LAMBO-V12-6.0", 620, {"debut": "2000-01"})], portes=2, places=2, reservoir=100,
   remarques="Phares fixes ; 6.0 sous l'ère Audi ; données indicatives")
mg(L, "Murciélago", "Murciélago", "1", "2001-09", "2006-02", [("6.2 V12 580", "LAMBO-V12-6.2", 650)], portes=2, places=2, reservoir=100, remarques="Roadster (2004)")
mg(L, "Murciélago", "Murciélago", "2", "2006-03", "2010-11",
   [("LP640 6.5 V12 640", "LAMBO-V12-6.5", 660), ("LP670-4 SV 6.5 V12 670", "LAMBO-V12-6.5", 660, {"debut": "2009-03"})], portes=2, places=2, reservoir=100,
   remarques="Restylage LP640 ; LP670-4 SuperVeloce")
mg(L, "Reventón", "Murciélago", "1", "2008-01", "2010-12", [("6.5 V12 650", "LAMBO-V12-6.5", 660)], portes=2, places=2, reservoir=100,
   remarques="20 coupés et 15 roadsters")
mg(L, "Aventador", "LB834", "1", "2011-06", "2016-12",
   [("LP700-4 6.5 V12 700", "LAMBO-V12-6.5", 690), ("LP750-4 SV 6.5 V12 750", "LAMBO-V12-6.5", 690, {"debut": "2015-06"})], portes=2, places=2, reservoir=90,
   remarques="Coupé et Roadster (2013)")
mg(L, "Aventador", "LB834", "2", "2017-01", "2022-09",
   [("S 6.5 V12 740", "LAMBO-V12-6.5", 690), ("SVJ 6.5 V12 770", "LAMBO-V12-6.5", 720, {"debut": "2018-10"}),
    ("LP780-4 Ultimae 6.5 V12 780", "LAMBO-V12-6.5", 720, {"debut": "2021-07"})], portes=2, places=2, reservoir=90,
   remarques="Aventador S ; production arrêtée en septembre 2022")
mg(L, "Sian", "LB834", "1", "2020-06", "2021-12", [("FKP 37 6.5 V12 Hybride 819", "LAMBO-V12-6.5-SCAP", 720)], portes=2, places=2, reservoir=90,
   remarques="Hybride léger à supercondensateur ; 63 coupés et 19 roadsters")
mg(L, "Essenza SCV12", "LB834", "1", "2020-12", "2021-12", [("6.5 V12 830", "LAMBO-V12-6.5", 760)], portes=2, places=1, reservoir=90,
   remarques="Voiture de piste non homologuée, 40 exemplaires")
mg(L, "Countach LPI 800-4", "LB834", "1", "2022-03", "2023-06", [("6.5 V12 Hybride 814", "LAMBO-V12-6.5-SCAP", 720)], portes=2, places=2, reservoir=83,
   remarques="Hommage à la Countach, hybride à supercondensateur, 112 exemplaires")
mg(L, "Revuelto", "LB744", "1", "2023-10", None, [("6.5 V12 HPEV 1015", "LAMBO-V12-6.5-PHEV", 725, el(4))], portes=2, places=2, reservoir=75,
   remarques="Hybride rechargeable (V12 de 825 ch et trois moteurs électriques), boîte 8 rapports à double embrayage")
mg(L, "Fenomeno", "LB744", "1", "2026-06", None, [("6.5 V12 HPEV 1080", "LAMBO-V12-6.5-PHEV", 725, el(7))], portes=2, places=2, reservoir=75,
   remarques="Série limitée à 29 exemplaires sur base Revuelto ; date, couple et batterie indicatifs")

# ---------------------------------------------------------------- V10 / V8
mg(L, "Gallardo", "Gallardo", "1", "2003-03", "2008-02",
   [("5.0 V10 500", "LAMBO-V10-5.0", 510, {"fin": "2005-12"}), ("5.0 V10 520", "LAMBO-V10-5.0", 510, {"debut": "2006-01"}),
    ("Superleggera 5.0 V10 530", "LAMBO-V10-5.0", 510, {"debut": "2007-03"})], portes=2, places=2, reservoir=90, remarques="Coupé et Spyder (2005)")
mg(L, "Gallardo", "Gallardo", "2", "2008-03", "2013-11",
   [("LP560-4 5.2 V10 560", "V10-5.2FSI", 540), ("LP550-2 5.2 V10 550", "V10-5.2FSI", 540, {"debut": "2009-11"}),
    ("LP570-4 Superleggera 5.2 V10 570", "V10-5.2FSI", 540, {"debut": "2010-03"})], portes=2, places=2, reservoir=90,
   remarques="Restylage LP560-4 ; V10 FSI partagé avec l'Audi R8")
mg(L, "Huracán", "LB724", "1", "2014-03", "2019-02",
   [("LP610-4 5.2 V10 610", "V10-5.2FSI", 560), ("LP580-2 5.2 V10 580", "V10-5.2FSI", 540, {"debut": "2016-01"}),
    ("Performante 5.2 V10 640", "V10-5.2FSI", 600, {"debut": "2017-03"})], portes=2, places=2, reservoir=83, remarques="Coupé et Spyder (2016)")
mg(L, "Huracán", "LB724", "2", "2019-03", "2024-10",
   [("EVO 5.2 V10 640", "V10-5.2FSI", 600), ("EVO RWD 5.2 V10 610", "V10-5.2FSI", 560, {"debut": "2020-01"}), ("STO 5.2 V10 640", "V10-5.2FSI", 565, {"debut": "2021-06"}),
    ("Tecnica 5.2 V10 640", "V10-5.2FSI", 565, {"debut": "2022-06"}), ("Sterrato 5.2 V10 610", "V10-5.2FSI", 560, {"debut": "2023-03"})],
   portes=2, places=2, reservoir=83, remarques="Huracán EVO ; production arrêtée fin 2024")
mg(L, "Temerario", "LB634", "1", "2025-03", None, [("4.0 V8 Biturbo HPEV 920", "LAMBO-V8-4.0TT-HYB", 800, el(4))], portes=2, places=2, reservoir=78,
   remarques="Hybride rechargeable (V8 biturbo de 800 ch à 10 000 tr/min et trois moteurs électriques) ; date indicative")
mg(L, "Urus", "Urus", "1", "2018-04", "2022-08", [("4.0 V8 Biturbo 650", "V8-4.0TFSI", 850)], reservoir=85, remarques="SUV sur plateforme MLB evo")
mg(L, "Urus", "Urus", "2", "2022-09", "2024-08",
   [("S 4.0 V8 Biturbo 666", "V8-4.0TFSI", 850), ("Performante 4.0 V8 Biturbo 666", "V8-4.0TFSI", 850)], reservoir=85, remarques="Urus S et Urus Performante")
mg(L, "Urus", "Urus", "3", "2024-09", None, [("SE 4.0 V8 Biturbo PHEV 800", "V8-4.0PHEV", 950, {"batterie": 26})], reservoir=80,
   remarques="Urus SE hybride rechargeable ; date indicative")

MOT = Motorisations("Lamborghini", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Lamborghini": L}
MOTEURS = MOT.moteurs()
