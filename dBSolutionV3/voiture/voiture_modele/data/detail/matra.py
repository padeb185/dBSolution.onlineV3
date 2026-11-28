"""Matra (Matra Automobile, Romorantin) : générations, phases, motorisations (marché français) et moteurs liés.
Djet (ex-René Bonnet, Renault Gordini), 530 (V4 Ford Taunus), Bagheera et Murena (trois places de front, moteurs Simca / Talbot) et Rancho
(Simca 1100). Espace (vendu Renault) et Avantime non repris ici. Puissances en ch DIN. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "RENAULT-1.1-GORDINI": f("ATM", "ESS", 1.1, "CHAINE", 4, 6500, 4500, "20W50", 3.0, 5000),
    "FORD-V4-1.7": f("ATM", "ESS", 1.7, "CHAINE", 4, 4800, 2800, "20W50", 3.5, 5000, a="V"),
    "SIMCA-1.3": f("ATM", "ESS", 1.3, "CHAINE", 4, 6000, 4400, "20W50", 3.5, 7500),
    "SIMCA-1.4": f("ATM", "ESS", 1.4, "CHAINE", 4, 5800, 3200, "20W50", 3.5, 7500),
    "SIMCA-1.6": f("ATM", "ESS", 1.6, "CHAINE", 4, 5600, 3200, "20W50", 4.0, 7500),
    "TALBOT-2.2": f("ATM", "ESS", 2.2, "CHAINE", 4, 5800, 3000, "20W50", 4.5, 7500),
}
mg = SaisieMoteurs(FAMILLES, "Simca", lambda fam: "Renault" if fam.startswith("RENAULT") else ("Ford" if fam.startswith("FORD") else ("Talbot" if fam.startswith("TALBOT") else "Simca")))
L = []
IND = "données indicatives"
mg(L, "Matra Djet", "Djet", "1", "1965-01", "1968-12", [("V 1.1 70", "RENAULT-1.1-GORDINI", 85), ("VS 1.1 95", "RENAULT-1.1-GORDINI", 102)], portes=2, places=2, reservoir=50,
   remarques="Première voiture de série à moteur central arrière, caisse en polyester ; " + IND)
mg(L, "Matra 530", "530", "1", "1967-03", "1973-12", [("1.7 V4 73", "FORD-V4-1.7", 132)], portes=2, places=2, reservoir=60, remarques="Coupé targa 2+2 à V4 Ford Taunus ; " + IND)
mg(L, "Matra Bagheera", "Bagheera", "1", "1973-04", "1980-07", [("1.3 84", "SIMCA-1.3", 108), ("S 1.4 90", "SIMCA-1.4", 117, {"debut": "1975-09"})], portes=3, places=3, reservoir=60,
   remarques="Trois places de front ; " + IND)
mg(L, "Matra Murena", "Murena", "1", "1980-09", "1983-12", [("1.6 92", "SIMCA-1.6", 131), ("2.2 118", "TALBOT-2.2", 181), ("S 2.2 142", "TALBOT-2.2", 186, {"debut": "1982-01"})],
   portes=3, places=3, reservoir=56, remarques="Châssis galvanisé, trois places de front ; " + IND)
mg(L, "Matra Rancho", "Rancho", "1", "1977-03", "1984-12", [("1.4 80", "SIMCA-1.4", 116)], portes=5, places=5, reservoir=60, remarques="Break de loisirs sur base Simca 1100 ; " + IND)

MOT = Motorisations("Simca", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Matra": L}
MOTEURS = MOT.moteurs()
