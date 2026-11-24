"""Dacia : générations, phases, motorisations (marché européen) et moteurs liés.
1300/1310, SupeRNova/Solenza, Logan, Sandero (Stepway en variantes), Jogger, Duster, Bigster, Lodgy, Dokker, Spring.
Les moteurs Renault reprennent les familles et les codes de renault.py (motoriste « Renault ») ; seuls les moteurs
propres à Dacia (1300, Spring) sont au motoriste « Dacia ». Utilitaires (Logan Van, Dokker Van) non repris.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .renault import FAMILLES as FAMILLES_RENAULT

E_, D = "ESS", "DSL"

PROPRES = {
    "DACIA-1.3": f("ATM", E_, 1.3, "CHAINE", 4, 5250, 3000, "20W50", 3.5, 7500),
    "DACIA-1.4": f("ATM", E_, 1.4, "CHAINE", 4, 5250, 3000, "20W50", 3.5, 7500),
    "SPRING-EV": electrique(),
}
AJOUTS_RENAULT = {
    "H4M": f("ATM", E_, 1.6, "CHAINE", 4, 5500, 4000, "5W30", 4.5, 30000),
    "HR18-ETECH": f("HYB_E", E_, 1.8, "CHAINE", 4, 5600, 3600, "0W20", 4.5, 30000),
    "HR12-LPG": f("TURBO", "LPG", 1.2, "CHAINE", 3, 5000, 1750, "0W20", 4.5, 30000),
    "HR12-HYBG": f("HYB_TE", "LPG", 1.2, "CHAINE", 3, 5000, 1750, "0W20", 4.5, 30000),
}
UTILISEES = ("K7J", "K7M", "K4M", "D4F", "H4D", "H4Bt", "H4Dt", "H4Dt-LPG", "H5Ft", "H5Ht", "HR12-MHEV", "HR16-ETECH", "K9K", "F8Q")
FAMILLES = {**{k: FAMILLES_RENAULT[k] for k in UTILISEES}, **AJOUTS_RENAULT, **PROPRES}


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Renault", lambda fam: "Dacia" if fam in PROPRES else "Renault")
L = []

# ---------------------------------------------------------------- anciennes
mg(L, "1300", "1300", "1", "1969-08", "1979-12", [("1300 54", "DACIA-1.3", 90)], portes=4, reservoir=47,
   remarques="Renault 12 sous licence ; données indicatives")
mg(L, "1300", "1300", "2", "1979-01", "2004-07", [("1310 1.3 56", "DACIA-1.3", 92), ("1410 1.4 63", "DACIA-1.4", 102, {"debut": "1986-01"})],
   portes=4, reservoir=47, remarques="1310 berline et break ; données indicatives")
mg(L, "Solenza", "SupeRNova", "1", "2000-10", "2005-12",
   [("SupeRNova 1.4 75", "K7J", 112, {"fin": "2003-06"}), ("Solenza 1.4 75", "K7J", 112, {"debut": "2003-07"}),
    ("Solenza 1.9 D 63", "F8Q", 120, {"debut": "2003-07"})], reservoir=50, remarques="SupeRNova puis Solenza (moteurs Renault)")

# ---------------------------------------------------------------- Logan
mg(L, "Logan", "L90", "1", "2004-09", "2008-08",
   [("1.4 MPI 75", "K7J", 112), ("1.6 MPI 87", "K7M", 128), ("1.6 16V 105", "K4M", 148, {"debut": "2006-06"}),
    ("1.5 dCi 68", "K9K", 160, {"debut": "2005-06"}), ("1.5 dCi 85", "K9K", 200, {"debut": "2007-01"})], portes=4, reservoir=50,
   remarques="Berline ; MCV break 7 places (2007)")
mg(L, "Logan", "L90", "2", "2008-09", "2012-12",
   [("1.4 MPI 75", "K7J", 112), ("1.6 MPI 90", "K7M", 128), ("1.6 16V 105", "K4M", 148), ("1.5 dCi 70", "K9K", 160),
    ("1.5 dCi 75", "K9K", 180, {"debut": "2010-06"}), ("1.5 dCi 90", "K9K", 200, {"debut": "2010-06"})], portes=4, reservoir=50, remarques="Restylage, MCV")
mg(L, "Logan", "L52", "1", "2012-12", "2016-08",
   [("1.2 16V 75", "D4F", 107), ("TCe 90", "H4Bt", 135), ("1.5 dCi 75", "K9K", 180), ("1.5 dCi 90", "K9K", 220)], portes=4, reservoir=50,
   remarques="Berline, MCV (2013)")
mg(L, "Logan", "L52", "2", "2016-09", "2020-12",
   [("SCe 75", "H4D", 97), ("TCe 90", "H4Bt", 140), ("1.5 dCi 90", "K9K", 220, {"fin": "2018-12"}), ("Blue dCi 95", "K9K", 220, {"debut": "2019-01"}),
    ("TCe 100 ECO-G 100", "H4Dt-LPG", 170, {"debut": "2019-09"})], portes=4, reservoir=50, remarques="Restylage, MCV et MCV Stepway")
mg(L, "Logan", "LJI", "1", "2020-12", None,
   [("SCe 65", "H4D", 95), ("TCe 90", "H4Dt", 160), ("TCe 100 ECO-G 100", "H4Dt-LPG", 170)], portes=4, reservoir=50,
   remarques="Berline (Europe de l'Est) ; restylage 2025 non détaillé")

# ---------------------------------------------------------------- Sandero
mg(L, "Sandero", "B90", "1", "2008-06", "2012-11",
   [("1.2 16V 75", "D4F", 107), ("1.4 MPI 75", "K7J", 112), ("1.6 MPI 90", "K7M", 128), ("Stepway 1.6 MPI 90", "K7M", 128, {"debut": "2009-09"}),
    ("1.6 16V 105", "K4M", 148), ("1.5 dCi 70", "K9K", 160), ("1.5 dCi 75", "K9K", 180, {"debut": "2010-06"}), ("1.5 dCi 90", "K9K", 200, {"debut": "2010-06"}),
    ("Stepway 1.5 dCi 90", "K9K", 200, {"debut": "2010-06"})], reservoir=50)
mg(L, "Sandero", "B52", "1", "2012-11", "2016-08",
   [("1.2 16V 75", "D4F", 107), ("TCe 90", "H4Bt", 135), ("Stepway TCe 90", "H4Bt", 135), ("1.5 dCi 75", "K9K", 180), ("1.5 dCi 90", "K9K", 220),
    ("Stepway 1.5 dCi 90", "K9K", 220)], reservoir=50)
mg(L, "Sandero", "B52", "2", "2016-09", "2020-12",
   [("SCe 75", "H4D", 97), ("TCe 90", "H4Bt", 140), ("Stepway TCe 90", "H4Bt", 140), ("1.5 dCi 90", "K9K", 220, {"fin": "2018-12"}),
    ("Blue dCi 95", "K9K", 220, {"debut": "2019-01"}), ("Stepway Blue dCi 95", "K9K", 220, {"debut": "2019-01"}),
    ("TCe 100 ECO-G 100", "H4Dt-LPG", 170, {"debut": "2019-09"})], reservoir=50, remarques="Restylage")
mg(L, "Sandero", "BJI", "1", "2020-12", "2025-11",
   [("SCe 65", "H4D", 95), ("TCe 90", "H4Dt", 160), ("TCe 100 ECO-G 100", "H4Dt-LPG", 170), ("TCe 110", "H4Dt", 200, {"debut": "2022-06"}),
    ("Stepway TCe 90", "H4Dt", 160), ("Stepway TCe 100 ECO-G 100", "H4Dt-LPG", 170), ("Stepway TCe 110", "H4Dt", 200, {"debut": "2022-06"})],
   reservoir=50, remarques="Plateforme CMF-B")
mg(L, "Sandero", "BJI", "2", "2025-12", None,
   [("SCe 65", "H4D", 95), ("TCe 100", "H4Dt", 170), ("ECO-G 120", "HR12-LPG", 200), ("Stepway TCe 100", "H4Dt", 170),
    ("Stepway ECO-G 120", "HR12-LPG", 200), ("Stepway Hybrid 155", "HR18-ETECH", 170, {"debut": "2026-10"})], reservoir=50,
   remarques="Restylage ; ECO-G 120 GPL disponible en boîte automatique")

# ---------------------------------------------------------------- Jogger / Lodgy / Dokker
mg(L, "Jogger", "RJI", "1", "2022-03", "2025-11",
   [("TCe 110", "H4Dt", 200), ("TCe 100 ECO-G 100", "H4Dt-LPG", 170), ("Hybrid 140", "HR16-ETECH", 148, {"debut": "2023-03"})], places=7, reservoir=50,
   remarques="Break 5 ou 7 places")
mg(L, "Jogger", "RJI", "2", "2025-12", None,
   [("TCe 100", "H4Dt", 170), ("ECO-G 120", "HR12-LPG", 200), ("Hybrid 155", "HR18-ETECH", 170)], places=7, reservoir=50, remarques="Restylage")
mg(L, "Lodgy", "J92", "1", "2012-03", "2022-06",
   [("1.6 MPI 85", "K7M", 134, {"fin": "2016-12"}), ("SCe 100", "H4M", 156, {"debut": "2014-09"}), ("TCe 115", "H5Ft", 190),
    ("TCe 130", "H5Ht", 240, {"debut": "2019-09"}), ("1.5 dCi 90", "K9K", 200, {"fin": "2018-12"}), ("1.5 dCi 110", "K9K", 240, {"fin": "2018-12"}),
    ("Blue dCi 95", "K9K", 220, {"debut": "2019-01"}), ("Blue dCi 115", "K9K", 260, {"debut": "2019-01"})], places=7, reservoir=50,
   remarques="Monospace 5 ou 7 places ; Stepway")
mg(L, "Dokker", "F67", "1", "2012-11", "2021-06",
   [("1.6 MPI 85", "K7M", 134, {"fin": "2016-12"}), ("SCe 100", "H4M", 156, {"debut": "2014-09"}), ("TCe 115", "H5Ft", 190),
    ("1.5 dCi 75", "K9K", 180, {"fin": "2018-12"}), ("1.5 dCi 90", "K9K", 200, {"fin": "2018-12"}), ("Blue dCi 95", "K9K", 220, {"debut": "2019-01"})],
   reservoir=50, remarques="Ludospace (version voiture), Stepway")

# ---------------------------------------------------------------- Duster / Bigster
mg(L, "Duster", "HSA", "1", "2010-04", "2013-09",
   [("1.6 16V 105", "K4M", 148, {"fin": "2011-12"}), ("1.6 16V 110", "K4M", 150, {"debut": "2012-01"}), ("1.5 dCi 85", "K9K", 200),
    ("1.5 dCi 90", "K9K", 200, {"debut": "2012-01"}), ("1.5 dCi 110", "K9K", 240)], reservoir=50, remarques="SUV 4x2 et 4x4")
mg(L, "Duster", "HSA", "2", "2013-10", "2017-12",
   [("1.6 SCe 115", "H4M", 156, {"debut": "2015-09"}), ("1.6 16V 105", "K4M", 145, {"fin": "2015-08"}), ("TCe 125", "H5Ft", 205),
    ("1.5 dCi 90", "K9K", 200), ("1.5 dCi 110", "K9K", 260)], reservoir=50, remarques="Restylage, 4x4")
mg(L, "Duster", "HJD", "1", "2018-01", "2024-03",
   [("SCe 115", "H4M", 156, {"fin": "2019-12"}), ("TCe 100", "H4Dt", 160, {"debut": "2019-09"}), ("TCe 130", "H5Ht", 240, {"debut": "2019-01"}),
    ("TCe 150", "H5Ht", 250, {"debut": "2019-01"}), ("TCe 100 ECO-G 100", "H4Dt-LPG", 170, {"debut": "2020-09"}),
    ("1.5 dCi 110", "K9K", 260, {"fin": "2018-12"}), ("Blue dCi 115", "K9K", 260, {"debut": "2019-01"})], reservoir=50,
   remarques="SUV 4x2 et 4x4 ; restylage 2021")
mg(L, "Duster", "CMF-B", "1", "2024-04", None,
   [("TCe 130", "HR12-MHEV", 230), ("TCe 100 ECO-G 100", "H4Dt-LPG", 170), ("Hybrid 140", "HR16-ETECH", 148),
    ("Hybrid-G 4x4 150", "HR12-HYBG", 230, {"debut": "2026-01"})], reservoir=50,
   remarques="3e génération ; TCe 130 micro-hybride 4x2 ou 4x4 ; Hybrid-G 150 4x4 (GPL + moteur électrique arrière) : date indicative")
mg(L, "Bigster", "CMF-B", "1", "2025-04", None,
   [("TCe 140", "HR12-MHEV", 230), ("ECO-G 140", "HR12-HYBG", 230), ("Hybrid 155", "HR18-ETECH", 170),
    ("Hybrid-G 4x4 150", "HR12-HYBG", 230, {"debut": "2026-01"})], reservoir=50, remarques="SUV segment C ; date Hybrid-G 150 4x4 indicative")

# ---------------------------------------------------------------- Spring
mg(L, "Spring", "BBG", "1", "2021-03", "2024-02",
   [("Electric 45", "SPRING-EV", 125, el(27)), ("Extreme 65", "SPRING-EV", 113, el(27, debut="2022-10"))], reservoir=0, remarques="Citadine électrique")
mg(L, "Spring", "BBG", "2", "2024-03", "2025-11",
   [("Electric 45", "SPRING-EV", 125, el(27)), ("Electric 65", "SPRING-EV", 113, el(27))], reservoir=0, remarques="Restylage (planche de bord)")
mg(L, "Spring", "BBG", "3", "2025-12", None,
   [("Electric 70", "SPRING-EV", 125, el(24)), ("Electric 100", "SPRING-EV", 136, el(24))], reservoir=0,
   remarques="Nouveaux moteurs 70 et 100 ch, batterie LFP ; couples indicatifs")

MOT = Motorisations("Renault", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Dacia": L}
MOTEURS = MOT.moteurs()
