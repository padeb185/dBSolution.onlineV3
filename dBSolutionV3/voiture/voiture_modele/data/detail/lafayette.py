"""Lafayette : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Lafayette Motors (Indianapolis puis Milwaukee, 1920-1924) : Model 134 à V8 ; puis Lafayette, marque d'entrée de gamme de Nash (1934-1936),
devenue Nash Lafayette (1937-1940). Puissances brutes converties en ch (× 1,014). Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "LAFAYETTE-V8-5.6": f("ATM", "ESS", 5.6, "NC", 8, 2700, 1300, "SAE30", 6.5, 2000, a="V"),
    "NASH-L6-3.5": f("ATM", "ESS", 3.5, "NC", 6, 3400, 1600, "SAE30", 4.7, 3000),
    "NASH-L6-3.8": f("ATM", "ESS", 3.8, "NC", 6, 3400, 1600, "SAE30", 4.7, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Nash", lambda fam: "Lafayette" if fam.startswith("LAFAYETTE") else "Nash")
L = []
IND = "marché nord-américain ; données indicatives (marque ancienne), à vérifier"
mg(L, "Model 134", "134", "1", "1920-01", "1923-12", [("5.6 V8 101", "LAFAYETTE-V8-5.6", 300)], portes=4, places=7, reservoir=80, remarques="Voiture de luxe fondée par Charles Nash ; " + IND)
mg(L, "Nash Lafayette", "Lafayette", "1", "1934-01", "1940-12", [("3.5 L6 76", "NASH-L6-3.5", 210, {"fin": "1936-12"}), ("3.8 L6 91", "NASH-L6-3.8", 240, {"debut": "1937-01"})],
   portes=4, places=5, reservoir=60, remarques="Lafayette (1934-1936) puis Nash Lafayette 400 (1937-1940) ; " + IND)

MOT = Motorisations("Nash", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Lafayette": L}
MOTEURS = MOT.moteurs()
