"""De Tomaso (Modène) : modèles, motorisations et moteurs liés.
Vallelunga, Mangusta, Pantera, Deauville, Longchamp, Guarà et P72 (renaissance de la marque).
Moteurs Ford (et BMW pour la Guarà) au motoriste « De Tomaso » (codes propres). Données indicatives (petites séries).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C, B = "CHAINE", "COURROIE"


def v8(t, l, rpm, nmrpm, q=5.7, d=C):
    return f(t, E_, l, d, 8, rpm, nmrpm, "20W50", q, 5000, a="V")


FAMILLES = {
    "FORD-KENT-1.5": f("ATM", E_, 1.5, C, 4, 6200, 4500, "20W50", 3.5, 5000),
    "FORD-289-4.7": v8("ATM", 4.7, 6000, 4000),
    "FORD-302-5.0": v8("ATM", 5.0, 5000, 3000),
    "FORD-351C-5.8": v8("ATM", 5.8, 5400, 3500),
    "BMW-M62-4.0": f("ATM", E_, 4.0, C, 8, 5700, 3900, "10W40", 7.5, 15000, a="V"),
    "FORD-MOD-4.6": f("ATM", E_, 4.6, C, 8, 6000, 4800, "5W30", 6.0, 15000, a="V"),
    "FORD-COYOTE-5.0SC": f("TURBO", E_, 5.0, C, 8, 7500, 6000, "5W50", 9.0, 10000, a="V"),
}

mg = SaisieMoteurs(FAMILLES, "De Tomaso")
L = []
IND = "Données indicatives"

mg(L, "Vallelunga", "Vallelunga", "1", "1964-01", "1968-12", [("Vallelunga 1.5 104", "FORD-KENT-1.5", 125)], portes=2, places=2, reservoir=40,
   remarques=IND + " ; coupé à moteur central (environ 50 ex.)")
mg(L, "Mangusta", "Mangusta", "1", "1967-01", "1971-12", [("Mangusta 4.7 V8 310", "FORD-289-4.7", 441), ("Mangusta USA 5.0 V8 233", "FORD-302-5.0", 393, {"debut": "1969-01"})],
   portes=2, places=2, reservoir=100, remarques=IND + " ; coupé Giugiaro (Ghia) à moteur central")
mg(L, "Pantera", "Pantera", "1", "1971-01", "1990-12",
   [("Pantera 5.8 V8 330", "FORD-351C-5.8", 441), ("Pantera L 5.8 V8 270", "FORD-351C-5.8", 407, {"debut": "1972-01", "fin": "1974-12"}),
    ("Pantera GTS 5.8 V8 350", "FORD-351C-5.8", 451, {"debut": "1974-01"}), ("Pantera GT5-S 5.8 V8 350", "FORD-351C-5.8", 451, {"debut": "1984-01"})],
   portes=2, places=2, reservoir=80, remarques=IND + " ; coupé à moteur central V8 Ford Cleveland")
mg(L, "Pantera", "Pantera", "2", "1990-01", "1993-12", [("Pantera 90 Si 5.0 V8 305", "FORD-302-5.0", 441)], portes=2, places=2, reservoir=80,
   remarques=IND + " ; restylage Gandini (environ 40 ex.)")
mg(L, "Deauville", "Deauville", "1", "1970-01", "1985-12", [("Deauville 5.8 V8 330", "FORD-351C-5.8", 441)], portes=4, places=5, reservoir=100,
   remarques=IND + " ; berline 4 portes (Ghia)")
mg(L, "Longchamp", "Longchamp", "1", "1972-01", "1989-12", [("Longchamp 5.8 V8 330", "FORD-351C-5.8", 441), ("Longchamp Spyder 5.8 V8 300", "FORD-351C-5.8", 430, {"debut": "1980-01"})],
   portes=2, places=4, reservoir=100, remarques=IND + " ; coupé 2+2 et Spyder (cabriolet)")
mg(L, "Guarà", "Guarà", "1", "1993-01", "2004-12", [("Guarà 4.0 V8 283", "BMW-M62-4.0", 400, {"fin": "1998-12"}), ("Guarà 4.6 V8 309", "FORD-MOD-4.6", 410, {"debut": "1998-01"})],
   portes=2, places=2, reservoir=90, remarques=IND + " ; coupé, Spider et Barchetta à moteur central")
mg(L, "P72", "P72", "1", "2024-01", None, [("P72 5.0 V8 Compresseur 710", "FORD-COYOTE-5.0SC", 820)], portes=2, places=2, reservoir=70,
   remarques="Supercar néo-rétro (72 ex.), V8 Ford Coyote à compresseur, boîte manuelle ; date de début de livraison indicative")

MOT = Motorisations("De Tomaso", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"De Tomaso": L}
MOTEURS = MOT.moteurs()
