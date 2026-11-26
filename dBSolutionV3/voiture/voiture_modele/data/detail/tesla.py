"""Tesla : générations, phases, versions (marché européen) et moteurs électriques liés.
Roadster, Model S, Model X, Model 3, Model Y et Cybertruck (Amérique du Nord). Versions Performance, P / Ludicrous et Plaid en variantes
(ex-marques « Tesla Performance » et « Tesla Roadster » regroupées ici). Semi (camion) non couvert.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom.
Tesla ne publie pas toujours puissances, couples ni capacités de batterie : valeurs usuelles de la presse, indicatives."""
from ._outil import Motorisations, SaisieMoteurs, electrique


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


FAMILLES = {"Tesla-Roadster": electrique(), "Tesla-S-X": electrique(), "Tesla-3-Y": electrique(), "Tesla-Cybertruck": electrique()}

mg = SaisieMoteurs(FAMILLES, "Tesla")
L = []

mg(L, "Roadster", "Roadster", "1", "2008-03", "2012-01",
   [("Roadster 248", "Tesla-Roadster", 270, el(53)), ("Roadster Sport 292", "Tesla-Roadster", 400, el(53, debut="2009-09"))],
   portes=2, places=2, reservoir=0, remarques="Roadster sur base Lotus Elise ; Roadster 2.5 (2010)")

# ---------------------------------------------------------------- Model S
mg(L, "Model S", "Model S", "1", "2013-08", "2016-03",
   [("S 60 306", "Tesla-S-X", 430, el(58)), ("S 85 367", "Tesla-S-X", 440, el(77)), ("S P85 421", "Tesla-S-X", 600, el(77)),
    ("S P85+ 421", "Tesla-S-X", 600, el(77, fin="2014-12", remarques="Performance Plus (châssis et pneus spécifiques)")),
    ("S 85D 422", "Tesla-S-X", 660, el(77, debut="2014-10")), ("S P85D 700", "Tesla-S-X", 967, el(77, debut="2014-10")),
    ("S 70D 333", "Tesla-S-X", 525, el(66, debut="2015-04")), ("S 90D 422", "Tesla-S-X", 660, el(82, debut="2015-07")),
    ("S P90D 772", "Tesla-S-X", 1140, el(82, debut="2015-07"))], portes=5, reservoir=0,
   remarques="Grande berline à hayon ; livraisons européennes à partir d'août 2013")
mg(L, "Model S", "Model S", "2", "2016-04", "2021-05",
   [("S 75D 333", "Tesla-S-X", 525, el(72)), ("S 90D 422", "Tesla-S-X", 660, el(82, fin="2017-03")), ("S 100D 422", "Tesla-S-X", 660, el(95, debut="2017-01")),
    ("S P100D 772", "Tesla-S-X", 1140, el(95, debut="2016-08")), ("S Grande Autonomie 422", "Tesla-S-X", 660, el(95, debut="2019-04")),
    ("S Performance 795", "Tesla-S-X", 1140, el(95, debut="2019-04"))], portes=5, reservoir=0, remarques="Restylage (face avant sans calandre)")
mg(L, "Model S", "Model S", "3", "2021-06", "2026-05",
   [("S Grande Autonomie 670", "Tesla-S-X", 1050, el(95)), ("S Plaid 1020", "Tesla-S-X", 1420, el(95))], portes=5, reservoir=0,
   remarques="Restylage « Palladium » (livraisons européennes 2022) ; fin de production le 10 mai 2026")

# ---------------------------------------------------------------- Model X
mg(L, "Model X", "Model X", "1", "2016-08", "2021-05",
   [("X 75D 333", "Tesla-S-X", 525, el(72)), ("X 90D 422", "Tesla-S-X", 660, el(82, fin="2017-03")), ("X P90D 772", "Tesla-S-X", 1140, el(82, fin="2017-03")),
    ("X 100D 422", "Tesla-S-X", 660, el(95, debut="2017-01")), ("X P100D 772", "Tesla-S-X", 1140, el(95, debut="2017-01")),
    ("X Grande Autonomie 422", "Tesla-S-X", 660, el(95, debut="2019-04")), ("X Performance 795", "Tesla-S-X", 1140, el(95, debut="2019-04"))],
   places=7, reservoir=0, remarques="SUV 5, 6 ou 7 places à portes « Falcon Wing »")
mg(L, "Model X", "Model X", "2", "2021-06", "2026-05",
   [("X Grande Autonomie 670", "Tesla-S-X", 1050, el(95)), ("X Plaid 1020", "Tesla-S-X", 1420, el(95))], places=7, reservoir=0,
   remarques="Restylage « Palladium » ; fin de production le 10 mai 2026")

# ---------------------------------------------------------------- Model 3
mg(L, "Model 3", "Model 3", "1", "2019-02", "2023-08",
   [("3 Standard Range Plus 325", "Tesla-3-Y", 420, el(55, fin="2021-06")), ("3 Propulsion 283", "Tesla-3-Y", 420, el(60, debut="2021-07")),
    ("3 Grande Autonomie 498", "Tesla-3-Y", 493, el(75)), ("3 Performance 513", "Tesla-3-Y", 660, el(75))], portes=4, reservoir=0,
   remarques="Berline ; livraisons européennes à partir de février 2019 ; batterie LFP sur la Propulsion (2021)")
mg(L, "Model 3", "Model 3", "2", "2023-09", None,
   [("3 Propulsion 283", "Tesla-3-Y", 420, el(60, fin="2026-01")), ("3 Grande Autonomie 498", "Tesla-3-Y", 493, el(79)),
    ("3 Performance 625", "Tesla-3-Y", 741, el(79, debut="2024-05")), ("3 Grande Autonomie Propulsion 366", "Tesla-3-Y", 420, el(79, debut="2025-03")),
    ("3 Standard 283", "Tesla-3-Y", 420, el(60, debut="2026-02"))], portes=4, reservoir=0,
   remarques="Restylage « Highland » ; Model 3 Standard (2026) remplace la Propulsion d'entrée")

# ---------------------------------------------------------------- Model Y
mg(L, "Model Y", "Model Y", "1", "2021-08", "2025-02",
   [("Y Grande Autonomie 514", "Tesla-3-Y", 493, el(75)), ("Y Performance 534", "Tesla-3-Y", 660, el(75)),
    ("Y Propulsion 299", "Tesla-3-Y", 420, el(60, debut="2022-08"))], reservoir=0,
   remarques="SUV compact 5 places (7 places en option) ; production Berlin (2022)")
mg(L, "Model Y", "Model Y", "2", "2025-03", None,
   [("Y Propulsion 299", "Tesla-3-Y", 420, el(62)), ("Y Grande Autonomie 514", "Tesla-3-Y", 493, el(77)),
    ("Y Performance 625", "Tesla-3-Y", 741, el(77, debut="2025-09")), ("Y Standard 299", "Tesla-3-Y", 420, el(62, debut="2025-10")),
    ("Y Standard Grande Autonomie Propulsion 349", "Tesla-3-Y", 420, el(77, debut="2026-02"))], reservoir=0,
   remarques="Restylage « Juniper » ; versions Standard (2025) ; Model YL 6 places non détaillé")

# ---------------------------------------------------------------- Cybertruck
mg(L, "Cybertruck", "Cybertruck", "1", "2023-11", None,
   [("AWD 608", "Tesla-Cybertruck", 1000, el(123)), ("Cyberbeast 857", "Tesla-Cybertruck", 1400, el(123)),
    ("Long Range RWD 367", "Tesla-Cybertruck", 600, el(123, debut="2025-04", fin="2025-09"))], portes=4, places=5, reservoir=0,
   remarques="Pick-up électrique à carrosserie inox, Amérique du Nord (non homologué en Europe) ; couples indicatifs")

MOT = Motorisations("Tesla", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Tesla": L}
MOTEURS = MOT.moteurs()
