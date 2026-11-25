"""AM General (South Bend, Indiana) : modèles, motorisations et moteurs liés.
HMMWV (Humvee, militaire), Hummer H1 (version civile, 1992-2006) et camion M35 (version AM General).
Les Hummer H2, H3 et électriques (GM) relèvent des marques Hummer et GMC. Puissances américaines converties en ch (×1,014).
Toutes les données sont indicatives (véhicules militaires et petites séries).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_, D = "ESS", "DSL"
C = "CHAINE"

FAMILLES = {
    "GM-L05-5.7": f("ATM", E_, 5.7, C, 8, 4000, 2800, "10W30", 4.7, 5000, a="V"),
    "DDA-6.2D": f("ATM", D, 6.2, C, 8, 3600, 1700, "15W40", 6.6, 5000, a="V"),
    "GM-6.5D": f("ATM", D, 6.5, C, 8, 3400, 1800, "15W40", 7.6, 5000, a="V"),
    "GM-6.5TD": f("TURBO", D, 6.5, C, 8, 3400, 1800, "15W40", 7.6, 5000, a="V"),
    "DURAMAX-LLY-6.6": f("TURBO", D, 6.6, C, 8, 3200, 1600, "15W40", 9.5, 7500, a="V"),
    "LDT-465-7.8": f("TURBO", D, 7.8, C, 6, 2600, 1800, "15W40", 18.0, 5000),
}

mg = SaisieMoteurs(FAMILLES, "AM General")
L = []
IND = "Données indicatives"

mg(L, "HMMWV", "M998", "1", "1984-01", None,
   [("M998 6.2 V8 Diesel 152", "DDA-6.2D", 339, {"fin": "1993-12"}), ("M1097 6.5 V8 Diesel 162", "GM-6.5D", 393, {"debut": "1994-01"}),
    ("M1114 6.5 V8 Turbo Diesel 193", "GM-6.5TD", 515, {"debut": "1996-01"})], portes=4, places=4, reservoir=95,
   remarques=IND + " ; véhicule militaire (Humvee), nombreuses versions (M998, M1097, M1114, M1151…)")
mg(L, "Hummer H1", "H1", "1", "1992-01", "2006-06",
   [("5.7 V8 193", "GM-L05-5.7", 407, {"fin": "1995-12"}), ("6.2 V8 Diesel 152", "DDA-6.2D", 339, {"fin": "1993-12"}), ("6.5 V8 Diesel 172", "GM-6.5D", 393, {"debut": "1994-01", "fin": "1995-12"}),
    ("6.5 V8 Turbo Diesel 198", "GM-6.5TD", 583, {"debut": "1996-01", "fin": "2001-12"}), ("6.5 V8 Turbo Diesel 208", "GM-6.5TD", 597, {"debut": "2002-01", "fin": "2004-12"}),
    ("Alpha 6.6 Duramax 304", "DURAMAX-LLY-6.6", 705, {"debut": "2006-01"})], portes=4, places=4, reservoir=95,
   remarques=IND + " ; version civile du HMMWV (pick-up, Wagon, Open Top) ; vendue Hummer H1 à partir de 2000")
mg(L, "M35", "M35A2", "1", "1950-01", "1999-12", [("M35A2 LDT-465 Multicarburant 136", "LDT-465-7.8", 446)], portes=2, places=2, reservoir=190,
   remarques=IND + " ; camion militaire 2,5 t 6x6 (production AM General à partir de 1967)")

MOT = Motorisations("AM General", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"AM General": L}
MOTEURS = MOT.moteurs()
