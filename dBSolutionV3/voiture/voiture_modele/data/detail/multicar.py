"""Multicar (Waltershausen, Thuringe) : générations, phases, motorisations (marché européen) et moteurs liés.
Petits utilitaires porte-outils : M22 et M25 (RDA, diesels IFA), M26 (moteurs Iveco puis VW), Fumo et Tremo ; groupe Hako puis Aebi Schmidt.
Puissances en ch. Utilitaires aux configurations multiples : une motorisation représentative, données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "IFA-4VD-2.2D": f("ATM", "DSL", 2.2, "NC", 4, 2800, 1800, "15W40", 6.0, 5000),
    "IFA-4VD-2.5D": f("ATM", "DSL", 2.5, "NC", 4, 3000, 1800, "15W40", 6.0, 5000),
    "IVECO-2.8D": f("TURBO", "DSL", 2.8, "COURROIE", 4, 3600, 1800, "10W40", 6.0, 20000),
    "IVECO-F1C-3.0D": f("TURBO", "DSL", 3.0, "CHAINE", 4, 3500, 1400, "5W30", 6.5, 30000),
}
mg = SaisieMoteurs(FAMILLES, "IFA", lambda fam: "Iveco" if fam.startswith("IVECO") else "IFA")
L = []
IND = "utilitaire ; motorisations multiples, données indicatives"
mg(L, "M22", "M22", "1", "1964-01", "1978-12", [("Diesel 2.2 30", "IFA-4VD-2.2D", 110)], portes=2, places=2, reservoir=40, remarques=IND)
mg(L, "M25", "M25", "1", "1978-01", "1992-12", [("Diesel 2.5 45", "IFA-4VD-2.5D", 140)], portes=2, places=2, reservoir=45, remarques=IND)
mg(L, "M26", "M26", "1", "1992-01", "2010-12", [("Diesel 2.8 Turbo 103", "IVECO-2.8D", 250)], portes=2, places=2, reservoir=60, remarques="Moteurs Iveco puis VW TDI ; " + IND)
mg(L, "Fumo", "Fumo", "1", "2005-01", None, [("Diesel 3.0 Turbo 146", "IVECO-F1C-3.0D", 350)], portes=2, places=3, reservoir=80, remarques=IND)
mg(L, "Tremo", "Tremo", "1", "2010-01", None, [("Diesel 3.0 Turbo 146", "IVECO-F1C-3.0D", 350)], portes=2, places=2, reservoir=80, remarques="Porte-outils compact ; " + IND)

MOT = Motorisations("IFA", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Multicar": L}
MOTEURS = MOT.moteurs()
