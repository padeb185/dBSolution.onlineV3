"""Smart : générations, phases, motorisations (marché européen) et moteurs liés.
Fortwo (450 « City-Coupé / City-Cabrio », 451, 453 et EQ), Roadster, Forfour (454, 453 et EQ), #1, #3 et #5.
Moteurs Mitsubishi repris de mitsubishi.py, Renault de renault.py, plateforme électrique Geely SEA de volvo.py (mêmes codes) ;
trois cylindres Mercedes M160, diesels CDI, Mitsubishi 3B21 et électriques Smart ajoutés. Le futur #2 n'est pas repris.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .mitsubishi import FAMILLES as FAMILLES_MITSUBISHI
from .renault import FAMILLES as FAMILLES_RENAULT
from .volvo import FAMILLES as FAMILLES_VOLVO

E_, D = "ESS", "DSL"
C = "CHAINE"

MB = {
    "M160-0.6T": f("TURBO", E_, 0.6, C, 3, 5250, 2000, "5W40", 3.0, 20000),
    "M160-0.7T": f("TURBO", E_, 0.7, C, 3, 5250, 2000, "5W40", 3.0, 20000),
    "OM660-0.8CDI": f("TURBO", D, 0.8, C, 3, 4200, 1800, "5W30", 3.5, 20000),
    "OM639-1.5CDI": f("TURBO", D, 1.5, C, 3, 4000, 1600, "5W30", 4.5, 20000),
}
MITSU_PROPRES = {"3B21-1.0": f("ATM", E_, 1.0, C, 3, 5800, 4500, "5W30", 3.5, 20000), "3B21-1.0T": f("TURBO", E_, 1.0, C, 3, 5250, 3000, "5W30", 3.5, 20000)}
MITSU = {**MITSU_PROPRES, **{k: FAMILLES_MITSUBISHI[k] for k in ("4A90-1.1", "4A91-1.3", "4G15-1.5", "4G15T-1.5")}}
RENAULT = {k: FAMILLES_RENAULT[k] for k in ("H4D", "H4Bt")}
SMART = {"SMART-EV": electrique()}
GEELY = {"EV-SEA": FAMILLES_VOLVO["EV-SEA"]}
FAMILLES = {**MB, **MITSU, **RENAULT, **SMART, **GEELY}


def motoriste(fam):
    if fam in MB:
        return "Mercedes-Benz"
    if fam in MITSU:
        return "Mitsubishi"
    if fam in RENAULT:
        return "Renault"
    if fam in GEELY:
        return "Geely"
    return "Smart"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Smart", motoriste)
L = []

mg(L, "Fortwo", "450", "1", "1998-07", "2002-12",
   [("0.6 45", "M160-0.6T", 70), ("0.6 55", "M160-0.6T", 80), ("0.6 61", "M160-0.6T", 80, {"debut": "2000-01"}), ("0.8 CDI 41", "OM660-0.8CDI", 100, {"debut": "1999-11"})],
   portes=2, places=2, reservoir=22, remarques="Smart City-Coupé, City-Cabrio (2000) ; renommée Fortwo en 2004")
mg(L, "Fortwo", "450", "2", "2003-01", "2007-03",
   [("0.7 50", "M160-0.7T", 80), ("0.7 61", "M160-0.7T", 95), ("Brabus 0.7 75", "M160-0.7T", 108), ("0.8 CDI 41", "OM660-0.8CDI", 100)],
   portes=2, places=2, reservoir=33, remarques="Coupé et cabriolet ; restylage, Fortwo à partir de 2004")
mg(L, "Roadster", "452", "1", "2003-04", "2005-11", [("0.7 61", "M160-0.7T", 95), ("0.7 82", "M160-0.7T", 110), ("Brabus 0.7 101", "M160-0.7T", 130, {"debut": "2004-01"})],
   portes=2, places=2, reservoir=35, remarques="Roadster et Roadster-Coupé")
mg(L, "Forfour", "454", "1", "2004-04", "2006-06",
   [("1.1 75", "4A90-1.1", 100), ("1.3 95", "4A91-1.3", 125), ("1.5 109", "4G15-1.5", 145), ("Brabus 1.5 Turbo 177", "4G15T-1.5", 230, {"debut": "2005-01"}),
    ("1.5 CDI 68", "OM639-1.5CDI", 160), ("1.5 CDI 95", "OM639-1.5CDI", 210)], portes=5, places=4, reservoir=47, remarques="Jumelle de la Mitsubishi Colt")
mg(L, "Fortwo", "451", "1", "2007-04", "2014-10",
   [("1.0 61", "3B21-1.0", 88), ("1.0 71", "3B21-1.0", 92), ("1.0 Turbo 84", "3B21-1.0T", 120), ("Brabus 1.0 Turbo 102", "3B21-1.0T", 147, {"debut": "2008-01"}),
    ("0.8 CDI 45", "OM660-0.8CDI", 110, {"fin": "2009-12"}), ("0.8 CDI 54", "OM660-0.8CDI", 130, {"debut": "2010-01"}), ("Electric Drive 75", "SMART-EV", 130, el(18, debut="2012-06"))],
   portes=2, places=2, reservoir=33, remarques="Coupé et cabriolet ; restylage 2012 ; dont mhd (micro-hybride)")
mg(L, "Fortwo", "453", "1", "2014-11", "2019-12",
   [("1.0 61", "H4D", 91), ("1.0 71", "H4D", 91), ("0.9 Turbo 90", "H4Bt", 135), ("Brabus 0.9 Turbo 109", "H4Bt", 170, {"debut": "2016-04"}),
    ("Electric Drive 82", "SMART-EV", 160, el(18, debut="2017-02"))], portes=2, places=2, reservoir=28, remarques="Coupé et cabriolet ; plateforme commune Renault Twingo III")
mg(L, "Fortwo", "453", "2", "2020-01", "2024-03", [("EQ 82", "SMART-EV", 160, el(18))], portes=2, places=2, reservoir=0,
   remarques="EQ Fortwo, uniquement électrique (coupé et cabriolet)")
mg(L, "Forfour", "453", "1", "2014-11", "2019-12",
   [("1.0 61", "H4D", 91), ("1.0 71", "H4D", 91), ("0.9 Turbo 90", "H4Bt", 135), ("Brabus 0.9 Turbo 109", "H4Bt", 170, {"debut": "2016-04"}),
    ("Electric Drive 82", "SMART-EV", 160, el(18, debut="2017-02"))], portes=5, places=4, reservoir=35, remarques="Jumelle de la Renault Twingo III")
mg(L, "Forfour", "453", "2", "2020-01", "2021-12", [("EQ 82", "SMART-EV", 160, el(18))], portes=5, places=4, reservoir=0, remarques="EQ Forfour, uniquement électrique")
mg(L, "#1", "HX11", "1", "2022-10", None,
   [("Pro 272", "EV-SEA", 343, el(49)), ("Pro+ 272", "EV-SEA", 343, el(66)), ("Brabus 428", "EV-SEA", 543, el(66))], portes=5, places=5, reservoir=0,
   remarques="SUV compact électrique (plateforme Geely SEA)")
mg(L, "#3", "HC11", "1", "2023-10", None,
   [("Pro 272", "EV-SEA", 343, el(49)), ("Pro+ 272", "EV-SEA", 343, el(66)), ("Brabus 428", "EV-SEA", 543, el(66))], portes=5, places=5, reservoir=0, remarques="SUV coupé électrique")
mg(L, "#5", "HY11", "1", "2025-04", None,
   [("Pro+ 363", "EV-SEA", 373, el(100)), ("Premium 587", "EV-SEA", 710, el(100)), ("Brabus 646", "EV-SEA", 710, el(100))], portes=5, places=5, reservoir=0,
   remarques="Grand SUV électrique, architecture 800 V ; données indicatives")

MOT = Motorisations("Smart", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Smart": L}
MOTEURS = MOT.moteurs()
