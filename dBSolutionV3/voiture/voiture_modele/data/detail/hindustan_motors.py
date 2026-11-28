"""Hindustan Motors : générations, phases, motorisations (marché indien) et moteurs liés.
Constructeur de Kolkata (Uttarpara) : Hindustan 10 et 14 (Morris), Landmaster (Morris Oxford II), Ambassador (Morris Oxford III, Mark I
à Mark IV, Nova, Classic, Grand, Avigo et Encore, 1958-2014) et Contessa (Vauxhall Victor FE, 1984-2002). Moteurs BMC B-Series, puis
Isuzu essence et diesel. Production arrêtée en 2014 ; marque Ambassador cédée à Peugeot (2017). Mitsubishi assemblées sous licence non
reprises. Puissances en ch. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"
FAMILLES = {
    "MORRIS-SV-1.1": f("ATM", E_, 1.1, "NC", 4, 3500, 2000, "SAE30", 3.0, 3000),
    "MORRIS-SV-1.5": f("ATM", E_, 1.5, "NC", 4, 4000, 2000, "SAE30", 3.5, 3000),
    "BMC-B-1.5": f("ATM", E_, 1.5, C, 4, 4800, 2400, "20W50", 4.5, 5000),
    "BMC-B-1.5D": f("ATM", D, 1.5, C, 4, 4000, 2200, "15W40", 4.5, 5000),
    "ISUZU-4ZB1-1.8": f("ATM", E_, 1.8, C, 4, 5000, 3000, "15W40", 4.0, 7500),
    "ISUZU-4EE-2.0D": f("ATM", D, 2.0, B, 4, 4600, 2500, "15W40", 5.0, 7500),
    "ISUZU-1.5D": f("ATM", D, 1.5, B, 4, 4800, 2500, "15W40", 4.5, 7500),
}
mg = SaisieMoteurs(FAMILLES, "Hindustan Motors", lambda fam: "Isuzu" if fam.startswith("ISUZU") else "Hindustan Motors")
L = []
IND = "marché indien ; données indicatives"

mg(L, "Hindustan 10", "Hindustan 10", "1", "1949-01", "1953-12", [("1.1 30", "MORRIS-SV-1.1", 70)], portes=4, places=4, reservoir=30, remarques="Morris Ten assemblée en Inde ; " + IND)
mg(L, "Hindustan 14", "Hindustan 14", "1", "1950-01", "1954-12", [("1.5 41", "MORRIS-SV-1.5", 95)], portes=4, places=5, reservoir=40, remarques="Morris Fourteen ; " + IND)
mg(L, "Landmaster", "Landmaster", "1", "1954-01", "1958-12", [("1.5 41", "MORRIS-SV-1.5", 95)], portes=4, places=5, reservoir=40, remarques="Morris Oxford II ; " + IND)
mg(L, "Ambassador", "Mark I", "1", "1958-01", "1962-12", [("1.5 55", "BMC-B-1.5", 101)], portes=4, places=5, reservoir=50, remarques="Morris Oxford III, moteur BMC B-Series ; " + IND)
mg(L, "Ambassador", "Mark II", "1", "1962-01", "1975-12", [("1.5 55", "BMC-B-1.5", 101)], portes=4, places=5, reservoir=50, remarques=IND)
mg(L, "Ambassador", "Mark III", "1", "1975-01", "1979-12", [("1.5 55", "BMC-B-1.5", 101), ("1.5 D 37", "BMC-B-1.5D", 83, {"debut": "1978-01"})], portes=4, places=5, reservoir=55,
   remarques="Première voiture diesel indienne (1978) ; " + IND)
mg(L, "Ambassador", "Mark IV", "1", "1979-01", "1990-12", [("1.5 55", "BMC-B-1.5", 101), ("1.5 D 37", "BMC-B-1.5D", 83)], portes=4, places=5, reservoir=55, remarques=IND)
mg(L, "Ambassador", "Nova / Classic", "1", "1990-01", "2011-12",
   [("1.5 55", "BMC-B-1.5", 101, {"fin": "2003-12"}), ("1.8 75", "ISUZU-4ZB1-1.8", 135, {"debut": "1992-01"}), ("1.5 D 37", "BMC-B-1.5D", 83, {"fin": "1999-12"}),
    ("2.0 D 52", "ISUZU-4EE-2.0D", 118, {"debut": "1998-01"})],
   portes=4, places=5, reservoir=55, remarques="Ambassador Nova (1990) puis Classic (1992) ; " + IND)
mg(L, "Ambassador Grand", "Grand", "1", "2003-01", "2013-12", [("1.8 75", "ISUZU-4ZB1-1.8", 135), ("2.0 D 52", "ISUZU-4EE-2.0D", 118)], portes=4, places=5, reservoir=55,
   remarques="Version modernisée (tableau de bord, sièges) ; " + IND)
mg(L, "Ambassador Avigo", "Avigo", "1", "2004-01", "2011-12", [("1.8 75", "ISUZU-4ZB1-1.8", 135), ("2.0 D 52", "ISUZU-4EE-2.0D", 118)], portes=4, places=5, reservoir=55,
   remarques="Face avant redessinée ; " + IND)
mg(L, "Ambassador Encore", "Encore", "1", "2013-01", "2014-05", [("1.5 D 50", "ISUZU-1.5D", 100)], portes=4, places=5, reservoir=55,
   remarques="Diesel BS-IV, dernière Ambassador (production arrêtée en mai 2014) ; " + IND)
mg(L, "Contessa", "Contessa", "1", "1984-01", "2002-12", [("1.5 50", "BMC-B-1.5", 98, {"fin": "1990-12"}), ("1.8 85", "ISUZU-4ZB1-1.8", 140, {"debut": "1987-01"}),
                                                          ("2.0 D 55", "ISUZU-4EE-2.0D", 120, {"debut": "1995-01"})], portes=4, places=5, reservoir=55,
   remarques="Carrosserie de la Vauxhall Victor FE ; Contessa Classic (1.8 GL Isuzu) ; " + IND)

MOT = Motorisations("Hindustan Motors", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Hindustan Motors": L}
MOTEURS = MOT.moteurs()
