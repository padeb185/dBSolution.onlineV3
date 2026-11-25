"""Lola (Lola Cars, Huntingdon) : voitures de course clients (prototypes sport), générations et moteurs liés.
T70 (Groupe 4/5), T212 (2 litres), B98/10 (LMP), B05/40 (LMP2), B12/80 (LMP2). Aucune n'est homologuée pour la route
(quelques T70 ont été immatriculées à titre privé). Puissances, couples et dates indicatifs ; une variante par moteur principal.
« T3000 » de l'ancienne liste non reprise (modèle non identifié).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C, B = "CHAINE", "COURROIE"

MOTORISTES = {
    "CHEVROLET-SB-5.0": "Chevrolet",
    "COSWORTH-FVC-1.8": "Cosworth",
    "ROUSH-V8-6.0": "Ford",
    "AER-P07-2.0T": "AER",
    "JUDD-HK-3.6": "Judd",
}
FAMILLES = {
    "CHEVROLET-SB-5.0": f("ATM", E_, 5.0, C, 8, 7000, 5000, "20W50", 8.0, 1000, a="V"),
    "COSWORTH-FVC-1.8": f("ATM", E_, 1.8, "NC", 4, 9000, 7000, "20W50", 6.0, 1000),
    "ROUSH-V8-6.0": f("ATM", E_, 6.0, C, 8, 7000, 5500, "10W60", 9.0, 1000, a="V"),
    "AER-P07-2.0T": f("TURBO", E_, 2.0, "NC", 4, 7500, 5500, "10W60", 7.0, 1000),
    "JUDD-HK-3.6": f("ATM", E_, 3.6, "NC", 8, 9500, 7500, "10W60", 8.0, 1000, a="V"),
}

COURSE = "Voiture de course client, non homologuée pour la route ; données indicatives"
mg = SaisieMoteurs(FAMILLES, "Lola", lambda fam: MOTORISTES[fam])
L = []

mg(L, "T70", "T70", "1", "1965-01", "1969-12", [("Chevrolet 5.0 V8 456", "CHEVROLET-SB-5.0", 500)], portes=0, places=1, reservoir=120,
   remarques="Spyder Mk I/II puis coupé Mk III et Mk IIIB ; " + COURSE)
mg(L, "T212", "T210", "1", "1970-01", "1971-12", [("Cosworth FVC 1.8 248", "COSWORTH-FVC-1.8", 200)], portes=0, places=1, reservoir=100,
   remarques="Barquette Groupe 5 de 2 litres (série T210/T212) ; " + COURSE)
mg(L, "B98/10", "B98/10", "1", "1998-01", "2000-12", [("Ford 6.0 V8 608", "ROUSH-V8-6.0", 680)], portes=0, places=1, reservoir=100,
   remarques="Prototype LMP ; moteurs Ford (Roush) ou Judd selon les équipes ; " + COURSE)
mg(L, "B05/40", "B05/40", "1", "2005-01", "2009-12", [("AER P07 2.0 Turbo 507", "AER-P07-2.0T", 510)], portes=0, places=1, reservoir=80,
   remarques="Prototype LMP2 ; aussi motorisé par Judd, Mazda ou Zytek ; " + COURSE)
mg(L, "B12/80", "B12/80", "1", "2012-01", "2013-12", [("Judd-BMW HK 3.6 V8 548", "JUDD-HK-3.6", 420)], portes=0, places=1, reservoir=75,
   remarques="Prototype LMP2 coupé ; aussi motorisé par Nissan ; " + COURSE)

MOT = Motorisations("Lola", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Lola": L}
MOTEURS = MOT.moteurs()
