"""Imperia (Nessonvaux, Belgique) : générations, phases, motorisations (marché européen) et moteurs liés.
Type 4/5 CV (1906-1910), 11 CV à distributeur rotatif (1924-1928), Type 9-11, TA-8 / TA-9 / TA-11 (traction avant, licence Adler) et
assemblage de la Standard Vanguard (1948-1958). Projet Imperia GP hybride (2010) non produit en série, non repris.
Puissances en ch. Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "IMPERIA-1C-0.7": f("ATM", E_, 0.7, "NC", 1, 1600, 1000, "SAE30", 1.5, 1000),
    "IMPERIA-L4-1.8": f("ATM", E_, 1.8, "NC", 4, 3000, 1800, "SAE30", 4.0, 3000),
    "IMPERIA-L4-1.1": f("ATM", E_, 1.1, "NC", 4, 3800, 2200, "SAE30", 3.0, 3000),
    "IMPERIA-L4-1.7": f("ATM", E_, 1.7, "NC", 4, 3800, 2200, "SAE30", 3.5, 3000),
    "STANDARD-2.1": f("ATM", E_, 2.1, "CHAINE", 4, 4200, 2000, "20W50", 4.5, 5000),
}
mg = SaisieMoteurs(FAMILLES, "Imperia", lambda fam: "Standard" if fam.startswith("STANDARD") else "Imperia")
L = []
IND = "données indicatives (marque ancienne), à vérifier"

mg(L, "Type 4/5 CV", "4/5 CV", "1", "1906-01", "1910-12", [("0.7 5", "IMPERIA-1C-0.7", 20)], portes=0, places=2, reservoir=20, remarques="Voiturette monocylindre ; " + IND)
mg(L, "11 CV", "11 CV", "1", "1924-01", "1928-12", [("1.8 35", "IMPERIA-L4-1.8", 95)], portes=4, places=4, reservoir=50, remarques="Moteur à distributeur rotatif (Burt-McCollum) ; " + IND)
mg(L, "Type 9-11", "9-11", "1", "1928-01", "1934-12", [("1.1 28", "IMPERIA-L4-1.1", 65), ("1.7 40", "IMPERIA-L4-1.7", 95)], portes=4, places=4, reservoir=45, remarques=IND)
mg(L, "TA-8", "TA", "1", "1934-01", "1939-12", [("1.1 30", "IMPERIA-L4-1.1", 68)], portes=4, places=4, reservoir=40, remarques="Traction avant sous licence Adler Trumpf Junior ; " + IND)
mg(L, "TA-9", "TA", "1", "1936-01", "1939-12", [("1.3 34", "IMPERIA-L4-1.1", 75)], portes=4, places=4, reservoir=40, remarques="Licence Adler Trumpf ; " + IND)
mg(L, "TA-11", "TA", "1", "1937-01", "1939-12", [("1.7 45", "IMPERIA-L4-1.7", 105)], portes=4, places=4, reservoir=45, remarques="Licence Adler Trumpf 1.7 ; " + IND)
mg(L, "Standard Vanguard", "Vanguard", "1", "1948-01", "1958-12", [("2.1 68", "STANDARD-2.1", 155)], portes=4, places=6, reservoir=55,
   remarques="Standard Vanguard assemblée en Belgique ; " + IND)

MOT = Motorisations("Imperia", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Imperia": L}
MOTEURS = MOT.moteurs()
