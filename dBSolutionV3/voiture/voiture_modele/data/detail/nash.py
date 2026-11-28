"""Nash (Nash Motors, Kenosha, 1917-1957) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Model 681, Advanced Six, Ambassador, 600 (caisse autoporteuse), Airflyte, Statesman et Rambler (1950-1955) ; fusion avec Hudson dans AMC (1954).
Metropolitan et Nash-Healey à part ; V8 Packard (1955-1956) et AMC (1957) repris de hudson.py (mêmes codes).
Puissances brutes converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .hudson import FAMILLES as FAMILLES_HUDSON
from .nash_healey import FAMILLES as FAMILLES_NH

FAMILLES = {
    "NASH-L6-4.3": f("ATM", "ESS", 4.3, "NC", 6, 2400, 1200, "SAE30", 5.0, 2000),
    "NASH-L6-4.1-OHV": f("ATM", "ESS", 4.1, "NC", 6, 2800, 1400, "SAE30", 5.0, 3000),
    "NASH-L8-4.9": f("ATM", "ESS", 4.9, "NC", 8, 3400, 1600, "SAE30", 6.0, 3000),
    "NASH-L6-2.8": f("ATM", "ESS", 2.8, "NC", 6, 3800, 1600, "SAE30", 4.3, 3000),
    "NASH-L6-3.0": f("ATM", "ESS", 3.0, "NC", 6, 3800, 1600, "SAE30", 4.3, 3000),
    "NASH-L6-3.2": f("ATM", "ESS", 3.2, "NC", 6, 3800, 1600, "SAE30", 4.3, 3000),
    "NASH-L6-3.8": FAMILLES_NH["NASH-L6-3.8"], "NASH-L6-4.1": FAMILLES_NH["NASH-L6-4.1"],
    "PACKARD-V8-5.2": FAMILLES_HUDSON["PACKARD-V8-5.2"], "AMC-V8-5.4": FAMILLES_HUDSON["AMC-V8-5.4"],
}
mg = SaisieMoteurs(FAMILLES, "Nash", lambda fam: "Packard" if fam.startswith("PACKARD") else ("AMC" if fam.startswith("AMC") else "Nash"))
L = []
IND = "marché nord-américain ; données indicatives"
mg(L, "Model 681", "681", "1", "1918-01", "1921-12", [("4.3 L6 56", "NASH-L6-4.3", 200)], portes=4, places=5, reservoir=65, remarques="Première Nash (ex-Jeffery) ; " + IND)
mg(L, "Advanced Six", "Advanced Six", "1", "1925-01", "1930-12", [("4.1 L6 71", "NASH-L6-4.1-OHV", 220)], portes=4, places=5, reservoir=70, remarques=IND)
mg(L, "Ambassador", "1932", "1", "1932-01", "1949-12", [("4.9 L8 101", "NASH-L8-4.9", 290, {"fin": "1942-12"}), ("3.8 L6 114", "NASH-L6-3.8", 271, {"debut": "1946-01"})],
   portes=4, places=6, reservoir=75, remarques="Huit cylindres puis six cylindres d'après-guerre ; production interrompue de 1943 à 1945 ; " + IND)
mg(L, "Ambassador", "1950", "1", "1950-01", "1957-12",
   [("3.8 L6 117", "NASH-L6-3.8", 285, {"fin": "1951-12"}), ("4.1 L6 122", "NASH-L6-4.1", 311, {"debut": "1952-01"}), ("Le Mans 4.1 L6 142", "NASH-L6-4.1", 311, {"debut": "1953-01"}),
    ("5.2 V8 211", "PACKARD-V8-5.2", 407, {"debut": "1955-01", "fin": "1956-12"}), ("5.4 V8 259", "AMC-V8-5.4", 468, {"debut": "1957-01"})],
   portes=4, places=6, reservoir=76, remarques="Airflyte puis Ambassador ; V8 Packard puis AMC ; " + IND)
mg(L, "600", "600", "1", "1941-01", "1949-12", [("2.8 L6 76", "NASH-L6-2.8", 190, {"fin": "1942-12"}), ("2.8 L6 83", "NASH-L6-2.8", 195, {"debut": "1946-01"})], portes=4, places=6, reservoir=75,
   remarques="Première américaine de grande série à caisse autoporteuse ; " + IND)
mg(L, "Airflyte", "Airflyte", "1", "1949-01", "1951-12", [("3.0 L6 83", "NASH-L6-3.0", 198), ("3.8 L6 114", "NASH-L6-3.8", 271)], portes=4, places=6, reservoir=75,
   remarques="Carrosserie « baignoire renversée » (Statesman et Ambassador) ; " + IND)
mg(L, "Statesman", "1950", "1", "1950-01", "1956-12", [("3.0 L6 86", "NASH-L6-3.0", 203, {"fin": "1952-12"}), ("3.2 L6 101", "NASH-L6-3.2", 230, {"debut": "1953-01"})], portes=4, places=6, reservoir=75,
   remarques=IND)
mg(L, "Rambler", "1950", "1", "1950-04", "1955-12", [("2.8 L6 83", "NASH-L6-2.8", 195), ("3.2 L6 91", "NASH-L6-3.2", 220, {"debut": "1953-01"})], portes=2, places=5, reservoir=50,
   remarques="Compacte, cabriolet, break et berline ; devenue marque Rambler (AMC) ; " + IND)

MOT = Motorisations("Nash", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Nash": L}
MOTEURS = MOT.moteurs()
