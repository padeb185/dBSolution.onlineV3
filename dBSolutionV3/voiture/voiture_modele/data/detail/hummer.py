"""Hummer (General Motors, 1999-2010) : générations, phases, motorisations et moteurs liés.
H1 (version civile du HMMWV, moteurs et codes repris d'am_general.py), H2 et H2 SUT, H3 et H3T ; H2 et H3 vendus officiellement en Europe
(2005-2010). Hummer EV (2022-) rattaché à GMC (gmc.py). Moteurs GM repris de gmc.py ; V8 Vortec 6000 et cinq cylindres 3.5 ajoutés.
Puissances américaines converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .am_general import FAMILLES as FAMILLES_AMG
from .gmc import FAMILLES as FAMILLES_GMC

E_ = "ESS"
AMG = {k: FAMILLES_AMG[k] for k in ("GM-L05-5.7", "DDA-6.2D", "GM-6.5D", "GM-6.5TD", "DURAMAX-LLY-6.6")}
GMC = {k: FAMILLES_GMC[k] for k in ("LLR-3.7", "LMG-5.3", "L92-6.2")}
NOUVEAUX = {
    "LQ4-6.0": f("ATM", E_, 6.0, "CHAINE", 8, 5200, 4000, "5W30", 5.7, 12000, a="V"),
    "LL0-3.5": f("ATM", E_, 3.5, "CHAINE", 5, 5600, 2800, "5W30", 5.7, 12000),
}
FAMILLES = {**AMG, **GMC, **NOUVEAUX}
mg = SaisieMoteurs(FAMILLES, "Chevrolet", lambda fam: "AM General" if fam in AMG else "Chevrolet")
L = []
IND = "données indicatives"

mg(L, "H1", "H1", "1", "1992-01", "2006-06",
   [("5.7 V8 193", "GM-L05-5.7", 407, {"fin": "1995-12"}), ("6.2 V8 Diesel 152", "DDA-6.2D", 339, {"fin": "1993-12"}), ("6.5 V8 Diesel 172", "GM-6.5D", 393, {"debut": "1994-01", "fin": "1995-12"}),
    ("6.5 V8 Turbo Diesel 198", "GM-6.5TD", 583, {"debut": "1996-01", "fin": "2001-12"}), ("6.5 V8 Turbo Diesel 208", "GM-6.5TD", 597, {"debut": "2002-01", "fin": "2004-12"}),
    ("Alpha 6.6 Duramax 304", "DURAMAX-LLY-6.6", 705, {"debut": "2006-01"})],
   portes=4, places=4, reservoir=95, remarques="Construit par AM General (version civile du HMMWV), vendu Hummer H1 à partir de 2000 ; " + IND)
mg(L, "H2", "H2", "1", "2002-07", "2009-12",
   [("6.0 V8 320", "LQ4-6.0", 488, {"fin": "2004-12"}), ("6.0 V8 330", "LQ4-6.0", 495, {"debut": "2005-01", "fin": "2007-12"}), ("6.2 V8 398", "L92-6.2", 563, {"debut": "2008-01"})],
   portes=5, places=6, reservoir=121, remarques="SUV sur châssis GMT820 (Tahoe), construit par AM General ; dont H2 SUT (pick-up, 2005-2009) ; " + IND)
mg(L, "H3", "H3", "1", "2005-04", "2010-05",
   [("3.5 I5 223", "LL0-3.5", 305, {"fin": "2006-12"}), ("3.7 I5 245", "LLR-3.7", 325, {"debut": "2007-01"}), ("Alpha 5.3 V8 304", "LMG-5.3", 434, {"debut": "2008-01"})],
   portes=5, places=5, reservoir=87, remarques="SUV sur base GMC Canyon / Chevrolet Colorado ; dont H3T (pick-up, 2009-2010) ; " + IND)

MOT = Motorisations("Chevrolet", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Hummer": L}
MOTEURS = MOT.moteurs()
