"""Eagle : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Marque de Chrysler (1988-1998) issue du rachat d'AMC : Medallion (Renault 21), Premier, Vista et Summit (Mitsubishi), Talon
(Mitsubishi Eclipse) et Vision (plate-forme LH). L'AMC Eagle (1980-1988) reste dans amc.py. Moteurs repris de renault_classiques.py,
jeep.py, mitsubishi.py et chrysler.py (mêmes familles). Puissances SAE converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .chrysler import FAMILLES as FAMILLES_CHRYSLER
from .jeep import FAMILLES as FAMILLES_JEEP
from .mitsubishi import FAMILLES as FAMILLES_MITSUBISHI
from .renault_classiques import FAMILLES as FAMILLES_RENAULT

RENAULT = {k: FAMILLES_RENAULT[k] for k in ("J7T", "PRV-3.0")}
AMC = {"AMC-2.5": FAMILLES_JEEP["AMC-2.5"]}
MITSUBISHI = {k: FAMILLES_MITSUBISHI[k] for k in ("4G15-1.5", "4G92-1.6", "4G93-1.8", "4G63-2.0", "4G63T-2.0", "4G64-2.4")}
CHRYSLER = {k: FAMILLES_CHRYSLER[k] for k in ("NEON-2.0", "EGA-3.3", "EGJ-3.5")}
FAMILLES = {**RENAULT, **AMC, **MITSUBISHI, **CHRYSLER}


def motoriste(fam):
    if fam in RENAULT:
        return "Renault"
    if fam in AMC:
        return "AMC"
    if fam in MITSUBISHI:
        return "Mitsubishi"
    return "Chrysler"


mg = SaisieMoteurs(FAMILLES, "Eagle", motoriste)
L = []
NA = "marché nord-américain ; données indicatives"

mg(L, "Medallion", "Medallion", "1", "1988-01", "1989-12", [("2.2 104", "J7T", 168)], portes=4, places=5, reservoir=66, remarques="Renault 21 importée, berline et break ; " + NA)
mg(L, "Premier", "Premier", "1", "1988-01", "1992-12", [("2.5 113", "AMC-2.5", 192, {"fin": "1988-12"}), ("3.0 V6 152", "PRV-3.0", 233)], portes=4, places=5, reservoir=64,
   remarques="Berline conçue par AMC / Renault (Giugiaro), assemblée à Bramalea ; " + NA)
mg(L, "Vista", "Vista", "1", "1989-01", "1991-12", [("1.5 82", "4G15-1.5", 121), ("2.0 97", "4G63-2.0", 151)], portes=3, places=4, reservoir=45,
   remarques="Mitsubishi Mirage / Colt Vista importées ; " + NA)
mg(L, "Summit", "Summit", "1", "1989-01", "1996-12", [("1.5 93", "4G15-1.5", 126), ("1.6 115", "4G92-1.6", 134, {"fin": "1992-12"}), ("1.8 115", "4G93-1.8", 157, {"debut": "1993-01"}),
                                                     ("Wagon 2.4 138", "4G64-2.4", 199, {"debut": "1992-01"})], portes=4, places=5, reservoir=50,
   remarques="Mitsubishi Mirage importée (berline, coupé, Summit Wagon) ; " + NA)
mg(L, "Talon", "1G", "1", "1990-01", "1994-12", [("2.0 137", "4G63-2.0", 170), ("TSi 2.0 Turbo 198", "4G63T-2.0", 275)], portes=2, places=4, reservoir=60,
   remarques="Jumelle des Mitsubishi Eclipse / Plymouth Laser (Diamond-Star), TSi AWD ; " + NA)
mg(L, "Talon", "2G", "1", "1995-01", "1998-12", [("2.0 142", "NEON-2.0", 176), ("TSi 2.0 Turbo 213", "4G63T-2.0", 292)], portes=2, places=4, reservoir=64,
   remarques="Coupé, 2.0 DOHC Chrysler 420A ou turbo Mitsubishi ; " + NA)
mg(L, "Vision", "LH", "1", "1993-01", "1997-12", [("3.3 V6 155", "EGA-3.3", 244), ("3.5 V6 217", "EGJ-3.5", 300)], portes=4, places=5, reservoir=68,
   remarques="Berline grande routière LH (cab-forward) ; " + NA)

MOT = Motorisations("Eagle", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Eagle": L}
MOTEURS = MOT.moteurs()
