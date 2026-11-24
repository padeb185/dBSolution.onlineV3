"""Cupra (marque indépendante depuis 2018) : générations, phases, motorisations (marché européen) et moteurs liés.
Ateca, Leon (5 portes et Sportstourer), Formentor, Born, Tavascan, Terramar, Raval.
Les versions Cupra antérieures (Seat Leon Cupra, Ibiza Cupra…) relèvent de Seat ; Leon Competición (course) non reprise.
Moteurs du groupe Volkswagen : familles et codes de volkswagen.py (motoriste « Volkswagen ») et du 2.5 TFSI d'audi.py (« Audi »).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .audi import FAMILLES as FAMILLES_AUDI
from .volkswagen import FAMILLES as FAMILLES_VW

VW = ("EA211-1.5TSI", "EA211-1.5eTSI", "EA211-1.4TSI-PHEV", "EA211-1.5TSI-PHEV", "EA888-2.0TSI", "EA288evo-2.0TDI",
      "MEB-EV", "MEB-AWD")
AUDI = ("EA855-2.5TFSI",)
FAMILLES = {**{k: FAMILLES_VW[k] for k in VW}, **{k: FAMILLES_AUDI[k] for k in AUDI}}


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Volkswagen", lambda fam: "Audi" if fam in AUDI else "Volkswagen")
L = []

mg(L, "Ateca", "KH7", "1", "2018-09", "2024-06", [("2.0 TSI 4Drive 300", "EA888-2.0TSI", 400)], reservoir=55,
   remarques="SUV (base Seat Ateca), restylage 2020")
mg(L, "Leon", "KL", "1", "2020-10", "2024-08",
   [("1.4 e-Hybrid 204", "EA211-1.4TSI-PHEV", 350, ph(13, 40)), ("VZ 1.4 e-Hybrid 245", "EA211-1.4TSI-PHEV", 400, ph(13, 40)),
    ("VZ 2.0 TSI 245", "EA888-2.0TSI", 370), ("VZ 2.0 TSI 300", "EA888-2.0TSI", 400), ("VZ 2.0 TSI 4Drive 310", "EA888-2.0TSI", 400, {"debut": "2021-01"}),
    ("1.5 eTSI 150", "EA211-1.5eTSI", 250, {"debut": "2021-09"})], reservoir=50, remarques="5 portes et Sportstourer (4Drive : Sportstourer)")
mg(L, "Leon", "KL", "2", "2024-09", None,
   [("1.5 TSI 150", "EA211-1.5TSI", 250), ("1.5 eTSI 150", "EA211-1.5eTSI", 250), ("1.5 e-Hybrid 204", "EA211-1.5TSI-PHEV", 350, ph(20, 40)),
    ("VZ 1.5 e-Hybrid 272", "EA211-1.5TSI-PHEV", 400, ph(20, 40)), ("VZ 2.0 TSI 300", "EA888-2.0TSI", 400),
    ("VZ 2.0 TSI 4Drive 333", "EA888-2.0TSI", 420)], reservoir=50, remarques="Restylage ; Leon VZ et VZ TCR 2026 non détaillées")
mg(L, "Formentor", "KM", "1", "2020-09", "2024-03",
   [("1.5 TSI 150", "EA211-1.5TSI", 250), ("2.0 TSI 4Drive 190", "EA888-2.0TSI", 320), ("VZ 2.0 TSI 245", "EA888-2.0TSI", 370, {"debut": "2021-06"}),
    ("VZ 2.0 TSI 4Drive 310", "EA888-2.0TSI", 400), ("VZ5 2.5 TFSI 390", "EA855-2.5TFSI", 480, {"debut": "2021-09", "fin": "2023-12"}),
    ("1.4 e-Hybrid 204", "EA211-1.4TSI-PHEV", 350, ph(13, 40, debut="2021-01")), ("VZ 1.4 e-Hybrid 245", "EA211-1.4TSI-PHEV", 400, ph(13, 40, debut="2021-01")),
    ("2.0 TDI 150", "EA288evo-2.0TDI", 360, {"debut": "2021-06"}), ("1.5 eTSI 150", "EA211-1.5eTSI", 250, {"debut": "2021-09"})], reservoir=55,
   remarques="SUV coupé")
mg(L, "Formentor", "KM", "2", "2024-04", None,
   [("1.5 TSI 150", "EA211-1.5TSI", 250), ("1.5 eTSI 150", "EA211-1.5eTSI", 250), ("2.0 TSI 4Drive 204", "EA888-2.0TSI", 320),
    ("VZ 2.0 TSI 4Drive 265", "EA888-2.0TSI", 400), ("VZ 2.0 TSI 4Drive 333", "EA888-2.0TSI", 420),
    ("1.5 e-Hybrid 204", "EA211-1.5TSI-PHEV", 350, ph(20, 45)), ("VZ 1.5 e-Hybrid 272", "EA211-1.5TSI-PHEV", 400, ph(20, 45)),
    ("VZ5 2.5 TFSI 390", "EA855-2.5TFSI", 480, {"debut": "2026-03"})], reservoir=55, remarques="Restylage ; date du retour de la VZ5 indicative")
mg(L, "Terramar", "KH8", "1", "2024-10", None,
   [("1.5 eTSI 150", "EA211-1.5eTSI", 250), ("2.0 TSI 4Drive 204", "EA888-2.0TSI", 320), ("VZ 2.0 TSI 4Drive 265", "EA888-2.0TSI", 400),
    ("1.5 e-Hybrid 204", "EA211-1.5TSI-PHEV", 350, ph(20, 45)), ("VZ 1.5 e-Hybrid 272", "EA211-1.5TSI-PHEV", 400, ph(20, 45))],
   reservoir=55, remarques="SUV (Györ)")
mg(L, "Born", "MEB", "1", "2021-11", "2026-05",
   [("Born 150", "MEB-EV", 310, el(45)), ("Born 204", "MEB-EV", 310, el(58)),
    ("Born e-Boost 231", "MEB-EV", 310, el(58)), ("Born e-Boost 77 kWh 231", "MEB-EV", 310, el(77, debut="2022-06")),
    ("VZ 326", "MEB-EV", 545, el(79, debut="2024-09"))], reservoir=0, remarques="Compacte électrique (Zwickau)")
mg(L, "Born", "MEB", "2", "2026-06", None,
   [("Born 190", "MEB-EV", 310, el(59)), ("Born 231", "MEB-EV", 310, el(79)), ("VZ 326", "MEB-EV", 545, el(79))], reservoir=0,
   remarques="Restylage (été 2026) ; puissances et batteries indicatives")
mg(L, "Tavascan", "MEB", "1", "2024-06", None,
   [("Endurance 286", "MEB-EV", 545, el(77)), ("VZ 4Drive 340", "MEB-AWD", 679, el(77))], reservoir=0, remarques="SUV coupé électrique (produit en Chine)")
mg(L, "Raval", "MEB+", "1", "2026-07", None,
   [("V Endurance 211", "MEB-EV", 290, el(52)), ("VZ 226", "MEB-EV", 290, el(52)), ("Raval 116", "MEB-EV", 220, el(37, debut="2026-09")),
    ("V Plus 135", "MEB-EV", 245, el(37, debut="2026-09"))], reservoir=0,
   remarques="Citadine électrique (Martorell) ; couples indicatifs")

MOT = Motorisations("Volkswagen", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Cupra": L}
MOTEURS = MOT.moteurs()
