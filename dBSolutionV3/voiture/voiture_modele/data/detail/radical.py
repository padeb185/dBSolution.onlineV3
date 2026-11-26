"""Radical Sportscars : générations, phases, motorisations (marché européen) et moteurs liés.
SR1, SR3 (dont RS, RSX, SL, XX), SR8, SR10 et RXC (dont Spyder et Turbo).
Moteurs Suzuki et Powertec (dérivés moto), V8 Powertec RP, 2.0 / 2.3 turbo Powertec sur base Ford ; V6 Ford 3.7 repris de ginetta.py
et 3.5 EcoBoost de ford.py (mêmes codes). Voitures de piste pour la plupart (SR3 SL et RXC homologuées route). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .ford import FAMILLES as FAMILLES_FORD
from .ginetta import FAMILLES as FAMILLES_GINETTA

E_ = "ESS"
C = "CHAINE"

MOTO = {
    "SUZUKI-1.3": f("ATM", E_, 1.3, C, 4, 10500, 8500, "10W40", 3.5, 5000),
    "POWERTEC-1.5": f("ATM", E_, 1.5, C, 4, 10500, 8500, "10W40", 3.5, 3000),
    "POWERTEC-V8-2.6": f("ATM", E_, 2.6, C, 8, 10500, 8500, "10W40", 5.0, 3000, a="V"),
    "POWERTEC-V8-2.8": f("ATM", E_, 2.8, C, 8, 10500, 8500, "10W40", 5.0, 3000, a="V"),
    "POWERTEC-2.0T": f("TURBO", E_, 2.0, C, 4, 6500, 4000, "5W40", 5.0, 5000),
    "POWERTEC-2.3T": f("TURBO", E_, 2.3, C, 4, 7000, 4500, "5W40", 5.0, 5000),
}
FORD = {"CYCLONE-3.7": FAMILLES_GINETTA["CYCLONE-3.7"], "ECOBOOST-V6-3.5": FAMILLES_FORD["ECOBOOST-V6-3.5"]}
FAMILLES = {**MOTO, **FORD}


def motoriste(fam):
    if fam in FORD:
        return "Ford"
    return "Suzuki" if fam == "SUZUKI-1.3" else "Powertec"


mg = SaisieMoteurs(FAMILLES, "Radical", motoriste)
L = []
P = "Voiture de piste (non homologuée route) ; données indicatives"

mg(L, "SR1", "SR1", "1", "2000-01", "2005-12", [("1.3 175", "SUZUKI-1.3", 140)], portes=0, places=1, reservoir=35, remarques=P + " ; dont SR1 Cup")
mg(L, "SR1", "SR1 (2017)", "1", "2017-01", None, [("1.3 185", "SUZUKI-1.3", 150)], portes=0, places=1, reservoir=35, remarques=P + " ; dont SR1 Cup")
mg(L, "SR3", "SR3", "1", "2002-01", "2008-12", [("1.3 230", "SUZUKI-1.3", 160), ("1.5 252", "POWERTEC-1.5", 175, {"debut": "2005-01"})], portes=0, places=2, reservoir=40, remarques=P)
mg(L, "SR3", "SR3 RS", "1", "2009-01", "2011-12", [("RS 1.5 264", "POWERTEC-1.5", 180)], portes=0, places=2, reservoir=40, remarques=P)
mg(L, "SR3", "SR3 RSX", "1", "2012-01", "2019-12", [("RSX 1.5 264", "POWERTEC-1.5", 180), ("RSX 1.5 Supersport 230", "POWERTEC-1.5", 170)], portes=0, places=2, reservoir=40,
   remarques=P)
mg(L, "SR3", "SR3 SL", "1", "2010-06", "2015-12", [("SL 2.0 Turbo 304", "POWERTEC-2.0T", 380)], portes=0, places=2, reservoir=50,
   remarques="Version homologuée route, 2.0 turbo Powertec (base Ford) ; données indicatives")
mg(L, "SR3", "SR3 XX", "1", "2020-01", None, [("XX 1.5 236", "POWERTEC-1.5", 170), ("XXR 1.5 264", "POWERTEC-1.5", 180, {"debut": "2022-01"})],
   portes=0, places=2, reservoir=40, remarques=P)
mg(L, "SR8", "SR8", "1", "2005-01", "2015-12", [("2.6 V8 368", "POWERTEC-V8-2.6", 350), ("RX 2.8 V8 466", "POWERTEC-V8-2.8", 380, {"debut": "2009-01"})],
   portes=0, places=2, reservoir=60, remarques=P + " ; record du Nürburgring pour une voiture homologable (2009)")
mg(L, "SR10", "SR10", "1", "2017-01", None, [("2.3 Turbo 441", "POWERTEC-2.3T", 500)], portes=0, places=2, reservoir=60, remarques=P + " ; base moteur Ford EcoBoost")
mg(L, "RXC", "RXC", "1", "2013-06", "2018-12",
   [("3.7 V6 385", "CYCLONE-3.7", 434), ("Spyder 3.7 V6 385", "CYCLONE-3.7", 434, {"debut": "2014-06"}), ("Turbo 3.5 V6 Biturbo 466", "ECOBOOST-V6-3.5", 650, {"debut": "2015-01"}),
    ("Turbo 600R 3.5 V6 Biturbo 608", "ECOBOOST-V6-3.5", 750, {"debut": "2016-06"})], portes=2, places=2, reservoir=70,
   remarques="Coupé et Spyder homologables route ; données indicatives")

MOT = Motorisations("Radical", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Radical": L}
MOTEURS = MOT.moteurs()
