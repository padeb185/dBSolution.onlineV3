"""March Engineering (Bicester, 1969-1992) : voitures de course clients, générations et moteurs liés.
701 (Formule 1, 1970), 712M (Formule 2), 761 (Formule 1), 83G (IMSA GTP) et 86C (IndyCar, victoire à Indianapolis 1986).
Aucune n'est homologuée pour la route. Puissances, couples et dates indicatifs ; une variante par moteur principal.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "COSWORTH-DFV-3.0": f("ATM", "ESS", 3.0, "COURROIE", 8, 10500, 8500, "10W60", 8.0, 1000, a="V"),
    "COSWORTH-BDA-1.6": f("ATM", "ESS", 1.6, "COURROIE", 4, 9000, 7000, "10W60", 5.0, 1000),
    "CHEV-V8-5.7-COURSE": f("ATM", "ESS", 5.7, "CHAINE", 8, 7500, 5500, "10W60", 10.0, 1000, a="V"),
    "COSWORTH-DFX-2.65T": f("TURBO", "ESS", 2.65, "COURROIE", 8, 11000, 9000, "10W60", 8.0, 1000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Cosworth", lambda fam: "Chevrolet" if fam.startswith("CHEV") else "Cosworth")
L = []
IND = "voiture de course, non homologuée route ; données indicatives"
mg(L, "701", "701", "1", "1970-01", "1971-12", [("3.0 V8 DFV 440", "COSWORTH-DFV-3.0", 330)], portes=0, places=1, reservoir=180, remarques="Formule 1 ; " + IND)
mg(L, "712M", "712M", "1", "1971-01", "1972-12", [("1.6 BDA 220", "COSWORTH-BDA-1.6", 180)], portes=0, places=1, reservoir=100, remarques="Formule 2 ; " + IND)
mg(L, "761", "761", "1", "1976-01", "1977-12", [("3.0 V8 DFV 465", "COSWORTH-DFV-3.0", 340)], portes=0, places=1, reservoir=180, remarques="Formule 1, victoire au GP d'Italie 1976 ; " + IND)
mg(L, "83G", "83G", "1", "1983-01", "1985-12", [("5.7 V8 650", "CHEV-V8-5.7-COURSE", 700)], portes=0, places=2, reservoir=120, remarques="Prototype IMSA GTP ; " + IND)
mg(L, "86C", "86C", "1", "1986-01", "1987-12", [("2.65 V8 Turbo DFX 720", "COSWORTH-DFX-2.65T", 520)], portes=0, places=1, reservoir=150, remarques="IndyCar, victoire à Indianapolis 1986 ; " + IND)

MOT = Motorisations("Cosworth", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"March Engineering": L}
MOTEURS = MOT.moteurs()
