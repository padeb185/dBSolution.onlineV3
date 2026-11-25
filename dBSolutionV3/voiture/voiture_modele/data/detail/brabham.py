"""Brabham : voitures de course (Formule 1, F2, prototypes) et hypercar BT62, motorisations et moteurs liés.
Moteurs de fournisseurs (Repco, Ford Cosworth, Alfa Romeo, BMW, Yamaha, Honda…) au motoriste « Brabham » (codes propres).
Toutes les monoplaces et prototypes de course ne sont pas homologués route ; données indicatives (puissances de course).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C, B = "CHAINE", "COURROIE"


def course(t, l, n, rpm, nmrpm, a="V"):
    return f(t, E_, l, C, n, rpm, nmrpm, "CHOISIR", 10.0, 1000, a=a)


FAMILLES = {
    "CLIMAX-FPF-2.5": course("ATM", 2.5, 4, 6750, 5000, a="EN_LIGNE"),
    "OLDS-V8-4.4": course("ATM", 4.4, 8, 6500, 4500),
    "HONDA-RA302E-1.0": course("ATM", 1.0, 4, 11000, 9500, a="EN_LIGNE"),
    "REPCO-740-3.0": course("ATM", 3.0, 8, 8000, 6000),
    "COSWORTH-DFV-3.0": course("ATM", 3.0, 8, 10500, 9000),
    "ALFA-115-12-3.0": course("ATM", 3.0, 12, 12000, 9500, a="PLAT"),
    "BMW-M12-1.5T": course("TURBO", 1.5, 4, 11000, 9000, a="EN_LIGNE"),
    "YAMAHA-OX99-3.5": course("ATM", 3.5, 12, 13000, 10500),
    "JUDD-GV-3.5": course("ATM", 3.5, 10, 13000, 10500),
    "BRABHAM-V8-5.4": f("ATM", E_, 5.4, C, 8, 7400, 6200, "0W40", 10.0, 5000, a="V"),
}

mg = SaisieMoteurs(FAMILLES, "Brabham")
L = []
R = "Voiture de course (non homologuée route) ; données indicatives"

mg(L, "BT14", "BT14", "1", "1965-01", "1966-12", [("BT14 Climax 2.5 240", "CLIMAX-FPF-2.5", 290)], portes=0, places=1, reservoir=80, remarques=R + " ; Formule Libre / Tasman")
mg(L, "BT17", "BT17", "1", "1965-01", "1966-12", [("BT17 Oldsmobile 4.4 V8 300", "OLDS-V8-4.4", 400)], portes=0, places=1, reservoir=90, remarques=R + " ; prototype sport")
mg(L, "BT18", "BT18", "1", "1966-01", "1966-12", [("BT18 Honda 1.0 150", "HONDA-RA302E-1.0", 100)], portes=0, places=1, reservoir=75, remarques=R + " ; Formule 2 (Honda), titre 1966")
mg(L, "BT24", "BT24", "1", "1967-01", "1968-12", [("BT24 Repco 740 3.0 V8 330", "REPCO-740-3.0", 320)], portes=0, places=1, reservoir=90, remarques=R + " ; F1, titres 1967 (Hulme)")
mg(L, "BT34", "BT34", "1", "1971-01", "1972-12", [("BT34 Cosworth DFV 3.0 V8 440", "COSWORTH-DFV-3.0", 330)], portes=0, places=1, reservoir=90, remarques=R + " ; F1 « lobster claw »")
mg(L, "BT44", "BT44", "1", "1974-01", "1975-12", [("BT44 Cosworth DFV 3.0 V8 465", "COSWORTH-DFV-3.0", 340)], portes=0, places=1, reservoir=90, remarques=R + " ; F1 (Gordon Murray)")
mg(L, "BT45", "BT45", "1", "1976-01", "1977-12", [("BT45 Alfa Romeo 3.0 Flat-12 520", "ALFA-115-12-3.0", 330)], portes=0, places=1, reservoir=90, remarques=R + " ; F1")
mg(L, "BT49", "BT49", "1", "1979-09", "1982-12", [("BT49 Cosworth DFV 3.0 V8 490", "COSWORTH-DFV-3.0", 360)], portes=0, places=1, reservoir=90, remarques=R + " ; F1, titre pilotes 1981 (Piquet)")
mg(L, "BT50", "BT50", "1", "1982-01", "1982-12", [("BT50 BMW 1.5 Turbo 570", "BMW-M12-1.5T", 440)], portes=0, places=1, reservoir=90, remarques=R + " ; F1")
mg(L, "BT52", "BT52", "1", "1983-01", "1983-12", [("BT52 BMW 1.5 Turbo 640", "BMW-M12-1.5T", 480)], portes=0, places=1, reservoir=90, remarques=R + " ; F1, titre pilotes 1983 (Piquet)")
mg(L, "BT56", "BT56", "1", "1987-01", "1987-12", [("BT56 BMW 1.5 Turbo 850", "BMW-M12-1.5T", 600)], portes=0, places=1, reservoir=90, remarques=R + " ; F1")
mg(L, "BT60", "BT60", "1", "1991-01", "1992-12", [("BT60Y Yamaha 3.5 V12 660", "YAMAHA-OX99-3.5", 390, {"fin": "1991-12"}), ("BT60B Judd 3.5 V10 680", "JUDD-GV-3.5", 400, {"debut": "1992-01"})],
   portes=0, places=1, reservoir=90, remarques=R + " ; F1, dernière Brabham de F1")
mg(L, "BT62", "BT62", "1", "2018-11", "2021-12", [("BT62 5.4 V8 710", "BRABHAM-V8-5.4", 667), ("BT62R 5.4 V8 710", "BRABHAM-V8-5.4", 667, {"debut": "2019-09"})],
   portes=2, places=2, reservoir=125, remarques="Hypercar de piste (70 ex. prévus) ; BT62R : conversion homologuée route ; données indicatives")
mg(L, "BT63", "BT63", "1", "2021-01", "2022-12", [("BT63 GT2 5.4 V8 700", "BRABHAM-V8-5.4", 660)], portes=2, places=1, reservoir=120, remarques=R + " ; GT2 (Fanatec GT2 European Series)")

MOT = Motorisations("Brabham", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Brabham": L}
MOTEURS = MOT.moteurs()
