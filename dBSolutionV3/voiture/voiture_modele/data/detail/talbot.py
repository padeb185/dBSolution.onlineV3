"""Talbot (1979-1986, puis utilitaires jusqu'en 1994) : générations, phases, motorisations (marché européen) et moteurs liés.
Horizon, 1510 / Solara, Samba, Tagora, Sunbeam (dont Sunbeam Lotus) et Express. Marque reprise par PSA après Simca / Chrysler Europe.
Les Talbot-Lago d'avant-guerre et d'après-guerre (T15, T26, Lago Sport…) relèvent de la marque Talbot-Lago ; Matra Rancho et
Murena (Talbot-Matra) de la marque Matra.
Moteurs Poissy et Simca 1.6 repris de simca.py, moteurs PSA (X, XUD, PRV) de peugeot.py, citroen.py et renault_classiques.py
(mêmes codes) ; Simca 2.2, PSA XD2S, Chrysler UK, Lotus 2.2 et moteurs Fiat de l'Express ajoutés. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .citroen import FAMILLES as FAMILLES_CITROEN
from .peugeot import FAMILLES as FAMILLES_PEUGEOT
from .renault_classiques import FAMILLES as FAMILLES_RENAULT
from .simca import FAMILLES as FAMILLES_SIMCA

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

PROPRES = {
    "SIMCA-2.2": f("ATM", E_, 2.2, C, 4, 5400, 3000, "15W40", 4.5, 7500),
    "XD2S-2.3": f("TURBO", D, 2.3, C, 4, 4150, 2000, "15W40", 6.0, 7500),
    "ROOTES-1.0": f("ATM", E_, 0.93, C, 4, 5600, 3000, "15W40", 3.5, 7500),
    "ROOTES-1.3": f("ATM", E_, 1.3, C, 4, 5000, 2600, "15W40", 3.5, 7500),
    "ROOTES-1.6": f("ATM", E_, 1.6, C, 4, 5000, 2600, "15W40", 4.0, 7500),
    "LOTUS-2.2": f("ATM", E_, 2.2, B, 4, 5750, 4500, "20W50", 5.0, 7500),
    "FIAT-2.0-EXPRESS": f("ATM", E_, 2.0, B, 4, 5200, 3000, "15W40", 4.5, 10000),
    "SOFIM-2.5D": f("ATM", D, 2.5, B, 4, 4200, 2200, "15W40", 6.0, 10000),
}
SIMCA = {k: FAMILLES_SIMCA[k] for k in ("POISSY-1.1", "POISSY-1.3", "POISSY-1.4", "SIMCA-1.6")}
PSA = {"XV8": FAMILLES_PEUGEOT["XV8"], "XW7": FAMILLES_PEUGEOT["XW7"], "XY": FAMILLES_CITROEN["XY"], "XUD9": FAMILLES_CITROEN["XUD9"],
       "PRV-2.7": FAMILLES_RENAULT["PRV-2.7"]}
FAMILLES = {**PROPRES, **SIMCA, **PSA}
MOTORISTES = {"XV8": "Peugeot", "XW7": "Peugeot", "XY": "Peugeot", "XUD9": "Peugeot", "XD2S-2.3": "Peugeot", "PRV-2.7": "PRV",
              "LOTUS-2.2": "Lotus", "FIAT-2.0-EXPRESS": "Fiat", "SOFIM-2.5D": "Fiat", "ROOTES-1.0": "Chrysler UK", "ROOTES-1.3": "Chrysler UK", "ROOTES-1.6": "Chrysler UK"}


def motoriste(fam):
    return MOTORISTES.get(fam, "Simca")


mg = SaisieMoteurs(FAMILLES, "Talbot", motoriste)
L = []
IND = "données indicatives"

mg(L, "Sunbeam", "Sunbeam", "1", "1979-08", "1981-12",
   [("1.0 42", "ROOTES-1.0", 69), ("1.3 59", "ROOTES-1.3", 95), ("1.6 69", "ROOTES-1.6", 125), ("Ti 1.6 100", "ROOTES-1.6", 131), ("Lotus 2.2 150", "LOTUS-2.2", 203, {"debut": "1979-10"})],
   portes=3, places=4, reservoir=40, remarques="Ex-Chrysler Sunbeam (Royaume-Uni) ; Sunbeam Lotus championne du monde des rallyes 1981 ; " + IND)
mg(L, "Horizon", "Horizon", "2", "1980-01", "1986-12",
   [("1.1 59", "POISSY-1.1", 86), ("1.3 68", "POISSY-1.3", 102), ("1.5 83", "POISSY-1.4", 122), ("1.9 D 65", "XUD9", 120, {"debut": "1983-01"})],
   portes=5, places=5, reservoir=47, remarques="Suite de la Simca Horizon ; " + IND)
mg(L, "1510", "C6", "1", "1980-01", "1986-12", [("1.3 68", "POISSY-1.3", 102), ("1.5 85", "POISSY-1.4", 122), ("1.6 90", "SIMCA-1.6", 134, {"debut": "1981-01"})],
   portes=5, places=5, reservoir=60, remarques="Suite des Simca 1307 / 1308 / 1309 (Talbot Alpine au Royaume-Uni) ; " + IND)
mg(L, "Solara", "C6", "2", "1980-04", "1986-12", [("1.3 68", "POISSY-1.3", 102), ("1.5 85", "POISSY-1.4", 122), ("SX 1.6 90", "SIMCA-1.6", 134, {"debut": "1981-01"})],
   portes=4, places=5, reservoir=60, remarques="Berline tricorps dérivée de la 1510 ; " + IND)
mg(L, "Samba", "Samba", "1", "1981-12", "1986-12",
   [("1.0 45", "XV8", 66), ("1.1 50", "XW7", 79), ("1.4 72", "XY", 110), ("Rallye 1.3 90", "XY", 105, {"debut": "1983-01"}), ("Cabriolet 1.4 80", "XY", 112, {"debut": "1982-09"})],
   portes=3, places=4, reservoir=40, remarques="Base Peugeot 104 ; dont cabriolet Pininfarina ; " + IND)
mg(L, "Tagora", "Tagora", "1", "1980-10", "1983-12", [("2.2 115", "SIMCA-2.2", 178), ("2.3 TD 80", "XD2S-2.3", 186), ("SX 2.7 V6 165", "PRV-2.7", 232)], portes=4, places=5, reservoir=70,
   remarques="Grande berline, environ 20 000 exemplaires ; " + IND)
mg(L, "Express", "Express", "1", "1982-01", "1994-12", [("2.0 78", "FIAT-2.0-EXPRESS", 147), ("2.5 D 75", "SOFIM-2.5D", 147)], portes=4, places=2, reservoir=80,
   remarques="Utilitaire jumeau des Fiat Ducato / Peugeot J5 / Citroën C25 ; " + IND)

MOT = Motorisations("Talbot", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Talbot": L}
MOTEURS = MOT.moteurs()
