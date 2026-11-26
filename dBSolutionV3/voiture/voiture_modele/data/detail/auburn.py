"""Auburn : générations, phases, motorisations (marché nord-américain) et moteurs liés.
6-40, 8-88, 8-120, 8-98, V12 et Speedster 851 / 852. Huit cylindres en ligne et V12 Lycoming, six cylindres Continental.
Puissances brutes converties en ch (× 1,014). Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
SV = "NC"
CONTINENTAL = {"CONTINENTAL-L6-3.7": f("ATM", E_, 3.7, SV, 6, 2400, 1200, "SAE30", 5.0, 2000)}
LYCOMING = {
    "LYCOMING-L8-4.4": f("ATM", E_, 4.4, SV, 8, 3400, 1600, "SAE30", 6.0, 3000),
    "LYCOMING-L8-4.9": f("ATM", E_, 4.9, SV, 8, 3300, 1600, "SAE30", 6.5, 3000),
    "LYCOMING-L8-4.6": f("ATM", E_, 4.6, SV, 8, 4000, 2000, "SAE30", 6.5, 3000),
    "LYCOMING-L8-4.6SC": f("TURBO", E_, 4.6, SV, 8, 4000, 2600, "SAE30", 6.5, 3000),
    "LYCOMING-V12-6.4": f("ATM", E_, 6.4, SV, 12, 3400, 1600, "SAE30", 8.0, 3000, a="V"),
}
FAMILLES = {**CONTINENTAL, **LYCOMING}


def motoriste(fam):
    return "Continental" if fam in CONTINENTAL else "Lycoming"


mg = SaisieMoteurs(FAMILLES, "Auburn", motoriste)
L = []
IND = "marché nord-américain ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "6-40", "6-40", "1", "1916-01", "1919-12", [("3.7 L6 41", "CONTINENTAL-L6-3.7", 190)], portes=4, places=5, reservoir=65, remarques="Torpédo ; " + IND)
mg(L, "8-88", "8-88", "1", "1925-01", "1927-12", [("4.4 L8 69", "LYCOMING-L8-4.4", 230)], portes=2, places=2, reservoir=70, remarques="Speedster, berlines et torpédos ; " + IND)
mg(L, "8-120", "8-120", "1", "1928-01", "1929-12", [("4.9 L8 117", "LYCOMING-L8-4.9", 300)], portes=4, places=5, reservoir=75, remarques="Berline et Speedster ; " + IND)
mg(L, "8-98", "8-98", "1", "1931-01", "1933-12", [("4.4 L8 99", "LYCOMING-L8-4.4", 260)], portes=4, places=5, reservoir=75, remarques="Berlines, cabriolets et Speedster ; " + IND)
mg(L, "V12", "V12", "1", "1932-01", "1934-12", [("6.4 V12 162", "LYCOMING-V12-6.4", 380)], portes=4, places=5, reservoir=90, remarques="Berline et Speedster 12-160 / 12-165 ; " + IND)
mg(L, "851", "851", "1", "1935-01", "1935-12", [("4.6 L8 117", "LYCOMING-L8-4.6", 290), ("Supercharged 4.6 L8 152", "LYCOMING-L8-4.6SC", 330)],
   portes=2, places=2, reservoir=80, remarques="Speedster (boat-tail), berlines et cabriolets ; compresseur en option ; " + IND)
mg(L, "852", "852", "1", "1936-01", "1936-12", [("4.6 L8 117", "LYCOMING-L8-4.6", 290), ("Supercharged 4.6 L8 152", "LYCOMING-L8-4.6SC", 330)],
   portes=2, places=2, reservoir=80, remarques="Speedster (boat-tail), berlines et cabriolets ; dernière Auburn ; " + IND)

MOT = Motorisations("Auburn", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Auburn": L}
MOTEURS = MOT.moteurs()
