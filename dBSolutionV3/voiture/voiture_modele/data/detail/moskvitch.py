"""Moskvitch (MZMA / AZLK, Moscou) : générations, phases, motorisations (marché soviétique et russe, export européen jusqu'aux années 1990) et moteurs liés.
400/401 (Opel Kadett K38), 402/403, 407, 410 / 411 (4x4), 408, 412, 426 (break), 2140, 2141 Aleko et 2142 ; marque relancée en 2022 avec des
JAC assemblées à Moscou (Moskvitch 3, 3e, 5, 6 et 8). Puissances en ch. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

FAMILLES = {
    "MZMA-1.1": f("ATM", "ESS", 1.1, "NC", 4, 3600, 2200, "SAE30", 3.0, 3000),
    "MZMA-1.2": f("ATM", "ESS", 1.2, "NC", 4, 4200, 2600, "20W50", 3.5, 5000),
    "MZMA-1.4": f("ATM", "ESS", 1.4, "CHAINE", 4, 4600, 2800, "20W50", 4.0, 5000),
    "UZAM-1.5": f("ATM", "ESS", 1.5, "CHAINE", 4, 5800, 3400, "15W40", 5.0, 10000),
    "UZAM-1.7": f("ATM", "ESS", 1.7, "CHAINE", 4, 5400, 3400, "15W40", 5.0, 10000),
    "RENAULT-F3R-2.0": f("ATM", "ESS", 2.0, "COURROIE", 4, 5500, 4000, "10W40", 5.0, 15000),
    "JAC-1.5T": f("TURBO", "ESS", 1.5, "CHAINE", 4, 5500, 1800, "5W30", 4.5, 10000),
    "JAC-EV": electrique(),
}
mg = SaisieMoteurs(FAMILLES, "Moskvitch", lambda fam: "Renault" if fam.startswith("RENAULT") else ("JAC" if fam.startswith("JAC") else "Moskvitch"))
L = []
IND = "données indicatives"
mg(L, "Moskvitch 400/401", "400", "1", "1946-12", "1956-12", [("1.1 23", "MZMA-1.1", 64, {"fin": "1953-12"}), ("1.1 26", "MZMA-1.1", 70, {"debut": "1954-01"})], portes=4, places=4, reservoir=31,
   remarques="Copie de l'Opel Kadett K38 (outillage récupéré à Rüsselsheim) ; " + IND)
mg(L, "Moskvitch 402/403", "402", "1", "1956-01", "1965-12", [("1.2 35", "MZMA-1.2", 69), ("403 1.4 45", "MZMA-1.4", 93, {"debut": "1962-01"})], portes=4, places=5, reservoir=35, remarques=IND)
mg(L, "Moskvitch 407", "407", "1", "1958-01", "1963-12", [("1.4 45", "MZMA-1.4", 93)], portes=4, places=5, reservoir=35, remarques="Largement exportée ; " + IND)
mg(L, "Moskvitch 410", "410", "1", "1957-01", "1961-12", [("1.2 35", "MZMA-1.2", 69), ("1.4 45", "MZMA-1.4", 93, {"debut": "1958-01"})], portes=4, places=5, reservoir=35, remarques="Berline 4x4 ; " + IND)
mg(L, "Moskvitch 411", "410", "B", "1958-01", "1961-12", [("1.4 45", "MZMA-1.4", 93)], portes=5, places=5, reservoir=35, remarques="Break 4x4 ; " + IND)
mg(L, "Moskvitch 408", "408", "1", "1964-01", "1976-12", [("1.4 50", "MZMA-1.4", 93)], portes=4, places=5, reservoir=46, remarques="Moskvitch Elite à l'export ; " + IND)
mg(L, "Moskvitch 412", "412", "1", "1967-01", "1976-12", [("1.5 75", "UZAM-1.5", 113)], portes=4, places=5, reservoir=46, remarques="Moteur UZAM à arbre à cames en tête ; " + IND)
mg(L, "Moskvitch 426", "408", "B", "1966-01", "1976-12", [("1.4 50", "MZMA-1.4", 93)], portes=5, places=5, reservoir=46, remarques="Break (427 avec moteur 1.5) ; " + IND)
mg(L, "Moskvitch 2140", "2140", "1", "1976-01", "1988-12", [("1.5 75", "UZAM-1.5", 113)], portes=4, places=5, reservoir=46, remarques="Moskvitch 1500 SL à l'export ; " + IND)
mg(L, "Moskvitch 2141 Aleko", "2141", "1", "1986-01", "2001-12", [("1.5 72", "UZAM-1.5", 106), ("1.7 85", "UZAM-1.7", 132, {"debut": "1997-01"}), ("2.0 145", "RENAULT-F3R-2.0", 185, {"debut": "1998-01"})],
   portes=5, places=5, reservoir=55, remarques="Traction (base Simca 1307) ; version Renault 2.0 à la fin ; " + IND)
mg(L, "Moskvitch 2142", "2142", "1", "1998-01", "2002-12", [("1.7 85", "UZAM-1.7", 132), ("2.0 145", "RENAULT-F3R-2.0", 185)], portes=4, places=5, reservoir=55, remarques="Berline tricorps (Svyatogor, Kniaz Vladimir) ; " + IND)
mg(L, "Moskvitch 3", "3", "1", "2022-11", None, [("1.5 Turbo 150", "JAC-1.5T", 210)], portes=5, places=5, reservoir=55, remarques="JAC JS4 assemblée à Moscou ; dont 3 Comfort ; marché russe ; " + IND)
mg(L, "Moskvitch 3e", "3", "E", "2022-11", None, [("Électrique 193", "JAC-EV", 340, {"batterie": 66})], portes=5, places=5, reservoir=0, remarques="JAC e-JS4 ; marché russe ; " + IND)
mg(L, "Moskvitch 6", "6", "1", "2023-09", None, [("1.5 Turbo 174", "JAC-1.5T", 285)], portes=5, places=5, reservoir=55, remarques="Liftback JAC J7 ; marché russe ; " + IND)
mg(L, "Moskvitch 5", "5", "1", "2024-01", None, [("1.5 Turbo 150", "JAC-1.5T", 210)], portes=5, places=5, reservoir=55, remarques="SUV compact ; marché russe ; " + IND)
mg(L, "Moskvitch 8", "8", "1", "2024-06", None, [("1.5 Turbo 174", "JAC-1.5T", 285)], portes=5, places=7, reservoir=55, remarques="SUV 7 places ; marché russe ; " + IND)

MOT = Motorisations("Moskvitch", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Moskvitch": L}
MOTEURS = MOT.moteurs()
