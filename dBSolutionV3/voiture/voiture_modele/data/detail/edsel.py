"""Edsel : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Marque de Ford (1958-1960) : Ranger, Pacer, Corsair, Citation (berlines, hardtops, cabriolets) et breaks Roundup, Villager et Bermuda.
V8 Ford FE / MEL et six cylindres Ford. Puissances brutes converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f


def v8(l, rpm, nmrpm):
    return f("ATM", "ESS", l, "CHAINE", 8, rpm, nmrpm, "20W50", 4.7, 3000, a="V")


FAMILLES = {
    "FORD-I6-3.7": f("ATM", "ESS", 3.7, "CHAINE", 6, 4200, 2000, "20W50", 4.7, 3000),
    "FORD-Y-4.8": v8(4.8, 4400, 2400), "FORD-FE-5.4": v8(5.4, 4400, 2800), "FORD-FE-5.8": v8(5.8, 4600, 2800),
    "FORD-FE-5.9": v8(5.9, 4600, 2900), "FORD-MEL-6.7": v8(6.7, 4600, 2900),
}
mg = SaisieMoteurs(FAMILLES, "Ford", lambda fam: "Ford")
L = []
NA = "marché nord-américain ; données indicatives"
E400_58 = [("5.9 V8 307", "FORD-FE-5.9", 542)]
E475_58 = [("6.7 V8 350", "FORD-MEL-6.7", 644)]
V59 = [("3.7 I6 147", "FORD-I6-3.7", 279), ("4.8 V8 203", "FORD-Y-4.8", 393), ("5.4 V8 228", "FORD-FE-5.4", 441), ("5.9 V8 307", "FORD-FE-5.9", 542)]
V60 = [("3.7 I6 147", "FORD-I6-3.7", 279), ("4.8 V8 188", "FORD-Y-4.8", 393), ("5.8 V8 304", "FORD-FE-5.8", 515)]

mg(L, "Ranger", "1958", "1", "1957-09", "1958-12", E400_58, portes=4, places=6, reservoir=76, remarques="Berline, hardtop ; " + NA)
mg(L, "Ranger", "1959", "1", "1959-01", "1959-12", V59, portes=4, places=6, reservoir=76, remarques="Berline, hardtop ; " + NA)
mg(L, "Ranger", "1960", "1", "1959-10", "1959-11", V60, portes=4, places=6, reservoir=76, remarques="Dernier millésime (environ 2 800 exemplaires) ; " + NA)
mg(L, "Pacer", "1958", "1", "1957-09", "1958-12", E400_58, portes=4, places=6, reservoir=76, remarques="Berline, hardtop, cabriolet ; " + NA)
mg(L, "Corsair", "1958", "1", "1957-09", "1958-12", E475_58, portes=4, places=6, reservoir=76, remarques="Berline et hardtop sur châssis long ; " + NA)
mg(L, "Corsair", "1959", "1", "1959-01", "1959-12", V59, portes=4, places=6, reservoir=76, remarques="Berline, hardtop, cabriolet ; " + NA)
mg(L, "Citation", "1958", "1", "1957-09", "1958-12", E475_58, portes=4, places=6, reservoir=76, remarques="Haut de gamme, berline, hardtop et cabriolet ; " + NA)
mg(L, "Roundup", "1958", "1", "1957-09", "1958-12", E400_58, portes=3, places=6, reservoir=76, remarques="Break 2 portes ; " + NA)
mg(L, "Villager", "1958", "1", "1957-09", "1958-12", E400_58, portes=5, places=6, reservoir=76, remarques="Break 4 portes ; " + NA)
mg(L, "Villager", "1959", "1", "1959-01", "1959-12", V59, portes=5, places=6, reservoir=76, remarques="Break 4 portes ; " + NA)
mg(L, "Villager", "1960", "1", "1959-10", "1959-11", V60, portes=5, places=6, reservoir=76, remarques="Break 4 portes ; " + NA)
mg(L, "Bermuda", "1958", "1", "1957-09", "1958-12", E400_58, portes=5, places=9, reservoir=76, remarques="Break haut de gamme à panneaux imitation bois ; " + NA)

MOT = Motorisations("Edsel", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Edsel": L}
MOTEURS = MOT.moteurs()
