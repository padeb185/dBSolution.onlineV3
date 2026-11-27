"""Barkas : générations, phases, motorisations (marché européen) et moteurs liés.
V 901/2 (1954-1961) et B 1000 (1961-1991), utilitaires et minibus est-allemands (Karl-Marx-Stadt / Hainichen).
Trois cylindres deux-temps IFA / Wartburg et quatre cylindres Volkswagen 1.3 (B 1000-1, 1989-1991).
Puissances en ch DIN. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .volkswagen import FAMILLES as FAMILLES_VW

E_ = "ESS"
IFA = {
    "IFA-0.9-2T": f("ATM", E_, 0.9, "NC", 3, 3600, 2500, "SAE30", 2.5, 3000),
    "WARTBURG-1.0-2T": f("ATM", E_, 1.0, "NC", 3, 4300, 3000, "SAE30", 2.5, 5000),
}
VW = {"EA111-1.3": FAMILLES_VW["EA111-1.3"]}
FAMILLES = {**IFA, **VW}


def motoriste(fam):
    if fam in VW:
        return "Volkswagen"
    return "Wartburg" if fam == "WARTBURG-1.0-2T" else "IFA"


mg = SaisieMoteurs(FAMILLES, "Barkas", motoriste)
L = []
IND = "données indicatives"

mg(L, "V 901/2", "V 901/2", "1", "1954-01", "1961-12", [("0.9 2T 28", "IFA-0.9-2T", 63)], portes=3, places=3, reservoir=36,
   remarques="Fourgon et minibus, trois cylindres deux-temps (IFA F9) ; " + IND)
mg(L, "B 1000", "B 1000", "1", "1961-01", "1988-12", [("1.0 2T 42", "WARTBURG-1.0-2T", 96, {"fin": "1981-12"}), ("1.0 2T 46", "WARTBURG-1.0-2T", 98, {"debut": "1982-01"})],
   portes=4, places=8, reservoir=50, remarques="Fourgon, minibus, pick-up et ambulance ; trois cylindres deux-temps Wartburg ; " + IND)
mg(L, "B 1000", "B 1000-1", "1", "1989-01", "1991-12", [("1.3 58", "EA111-1.3", 99)], portes=4, places=8, reservoir=50,
   remarques="Quatre cylindres quatre-temps Volkswagen 1.3 (fabriqué sous licence) ; " + IND)

MOT = Motorisations("Barkas", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Barkas": L}
MOTEURS = MOT.moteurs()
