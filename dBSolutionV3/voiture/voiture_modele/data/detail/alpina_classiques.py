"""Alpina (modèles anciens, avant 1988) : générations, motorisations (marché européen) et moteurs liés.
Préparations puis voitures de constructeur (Alpina reconnu constructeur en 1983) sur base BMW : B6 2.8 et C1 (E21), B7 Turbo (E12),
B9 et B10 3.5, B7 Turbo (E28), B7 Turbo Coupé (E24), C1 / C2 / B3 2.7 / B6 3.5 (E30), B11 et B12 (E32).
Six cylindres BMW M20 / M30 et V12 M70 retravaillés au motoriste « Alpina » ; M30 3.5 repris d'alpina.py (même famille et couples).
Puissances en ch. Données indicatives (petites séries), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .alpina import FAMILLES as FAMILLES_ALPINA

E_ = "ESS"
C = "CHAINE"
B = "COURROIE"
FAMILLES = {
    "ALPINA-M30-3.5": FAMILLES_ALPINA["ALPINA-M30-3.5"],
    "ALPINA-M30-2.8": f("ATM", E_, 2.8, C, 6, 6200, 4500, "10W40", 5.75, 10000),
    "ALPINA-M30-3.0T": f("TURBO", E_, 3.0, C, 6, 5800, 3000, "10W40", 5.75, 10000),
    "ALPINA-M30-3.5T": f("TURBO", E_, 3.5, C, 6, 5800, 3000, "10W40", 5.75, 10000),
    "ALPINA-M20-2.3": f("ATM", E_, 2.3, B, 6, 5800, 4500, "10W40", 4.75, 10000),
    "ALPINA-M20-2.5": f("ATM", E_, 2.5, B, 6, 6000, 4500, "10W40", 4.75, 10000),
    "ALPINA-M20-2.7": f("ATM", E_, 2.7, B, 6, 5800, 4500, "10W40", 4.75, 10000),
    "ALPINA-M70-5.0": f("ATM", E_, 5.0, C, 12, 5300, 4000, "10W60", 8.0, 15000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Alpina", lambda fam: "Alpina")
L = []
IND = "données indicatives (petite série), à vérifier"

mg(L, "B6", "E21", "1", "1978-01", "1982-12", [("B6 2.8 200", "ALPINA-M30-2.8", 260)], portes=2, places=4, reservoir=58, remarques="Base BMW Série 3 E21 ; " + IND)
mg(L, "C1", "E21", "1", "1980-01", "1982-12", [("C1 2.3 170", "ALPINA-M20-2.3", 226)], portes=2, places=4, reservoir=58, remarques="Base BMW 323i E21 ; " + IND)
mg(L, "B7 Turbo", "E12", "1", "1978-01", "1981-12", [("B7 Turbo 3.0 300", "ALPINA-M30-3.0T", 451)], portes=4, places=5, reservoir=70,
   remarques="Base BMW Série 5 E12, l'une des berlines les plus rapides de son époque ; " + IND)
mg(L, "B9", "E28", "1", "1981-09", "1985-12", [("B9 3.5 245", "ALPINA-M30-3.5", 320)], portes=4, places=5, reservoir=70, remarques="Base BMW Série 5 E28 ; " + IND)
mg(L, "B10", "E28", "1", "1985-01", "1987-12", [("B10 3.5 261", "ALPINA-M30-3.5", 346)], portes=4, places=5, reservoir=70, remarques="Base BMW Série 5 E28 ; " + IND)
mg(L, "B7 Turbo", "E28", "1", "1984-01", "1987-12", [("B7 Turbo 3.5 300", "ALPINA-M30-3.5T", 500)], portes=4, places=5, reservoir=70, remarques="Base BMW Série 5 E28 ; " + IND)
mg(L, "B7 Turbo Coupé", "E24", "1", "1984-01", "1987-12", [("B7 Turbo Coupé 3.5 330", "ALPINA-M30-3.5T", 520)], portes=2, places=4, reservoir=70,
   remarques="Base BMW Série 6 E24 ; " + IND)
mg(L, "C1", "E30", "1", "1983-01", "1987-12", [("C1 2.3 170", "ALPINA-M20-2.3", 226)], portes=2, places=4, reservoir=55, remarques="Base BMW 323i E30 ; " + IND)
mg(L, "C2", "E30", "1", "1985-01", "1988-12", [("C2 2.5 185", "ALPINA-M20-2.5", 240), ("C2 2.7 210", "ALPINA-M20-2.7", 267, {"debut": "1986-01"})], portes=2, places=4,
   reservoir=55, remarques="Base BMW Série 3 E30 ; " + IND)
mg(L, "B3", "E30", "1", "1987-01", "1992-12", [("B3 2.7 204", "ALPINA-M20-2.7", 266)], portes=2, places=4, reservoir=55,
   remarques="Base BMW Série 3 E30 (berline, coupé, cabriolet, Touring) ; " + IND)
mg(L, "B6", "E30", "1", "1987-01", "1990-12", [("B6 3.5 254", "ALPINA-M30-3.5", 320)], portes=2, places=4, reservoir=55, remarques="Six cylindres 3.5 dans la Série 3 E30 ; " + IND)
mg(L, "B11", "E32", "1", "1987-01", "1993-12", [("B11 3.5 250", "ALPINA-M30-3.5", 330), ("B11 4.0 V8 315", "ALPINA-M30-3.5", 400, {"debut": "1993-01"})],
   portes=4, places=5, reservoir=90, remarques="Base BMW Série 7 E32 ; " + IND)
mg(L, "B12", "E32", "1", "1988-01", "1994-12", [("B12 5.0 350", "ALPINA-M70-5.0", 470)], portes=4, places=5, reservoir=102, remarques="V12 dans la Série 7 E32 ; " + IND)

MOT = Motorisations("Alpina", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Alpina": L}
MOTEURS = MOT.moteurs()
