"""Graham : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Graham-Paige devenu Graham (Detroit, 1930-1941) : Blue Streak (huit cylindres, 1932-1934), Supercharger (premier compresseur abordable,
1934-1937), Spirit of Motion (« Sharknose », 1938-1940) et Hollywood (carrosserie Cord 810, 1940-1941).
Puissances brutes converties en ch (× 1,014). Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "GRAHAM-L8-4.0": f("ATM", E_, 4.0, "NC", 8, 3400, 1600, "SAE30", 6.5, 3000),
    "GRAHAM-L8-4.5SC": f("TURBO", E_, 4.5, "NC", 8, 4000, 2000, "SAE30", 7.0, 3000),
    "GRAHAM-L6-3.6": f("ATM", E_, 3.6, "NC", 6, 3800, 1600, "SAE30", 5.5, 3000),
    "GRAHAM-L6-3.6SC": f("TURBO", E_, 3.6, "NC", 6, 4000, 2400, "SAE30", 5.5, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Graham", lambda fam: "Graham")
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Blue Streak", "Blue Streak", "1", "1932-01", "1934-12", [("4.0 L8 96", "GRAHAM-L8-4.0", 260)], portes=4, places=5, reservoir=70,
   remarques="Berline huit cylindres à ailes enveloppantes (Amos Northup) ; " + IND)
mg(L, "Supercharger", "Supercharger", "1", "1934-01", "1937-12", [("4.5 L8 Supercharged 137", "GRAHAM-L8-4.5SC", 330, {"fin": "1935-12"}),
                                                                ("3.6 L6 Supercharged 114", "GRAHAM-L6-3.6SC", 250, {"debut": "1936-01"})],
   portes=4, places=5, reservoir=70, remarques="Compresseur centrifuge de série ; " + IND)
mg(L, "Spirit of Motion", "Sharknose", "1", "1938-01", "1940-12", [("3.6 L6 91", "GRAHAM-L6-3.6", 230), ("3.6 L6 Supercharged 118", "GRAHAM-L6-3.6SC", 255)],
   portes=4, places=5, reservoir=70, remarques="Berline « Sharknose » à calandre inclinée ; " + IND)
mg(L, "Hollywood", "Hollywood", "1", "1940-01", "1941-12", [("3.6 L6 94", "GRAHAM-L6-3.6", 232), ("3.6 L6 Supercharged 126", "GRAHAM-L6-3.6SC", 260)],
   portes=4, places=5, reservoir=70, remarques="Carrosserie reprise de la Cord 810 (propulsion), jumelle de la Hupmobile Skylark ; " + IND)

MOT = Motorisations("Graham", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Graham": L}
MOTEURS = MOT.moteurs()
