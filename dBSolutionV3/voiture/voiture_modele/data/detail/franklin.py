"""Franklin : générations, phases, motorisations (marché nord-américain) et moteurs liés.
H.H. Franklin Manufacturing (Syracuse, 1902-1934), moteurs refroidis par air : Model A (quatre cylindres transversal), Series 9, Airman,
Olympic et V12. Puissances brutes converties en ch (× 1,014). Données indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "FRANKLIN-1.7": f("ATM", E_, 1.7, "NC", 4, 1800, 1000, "SAE30", 3.0, 2000),
    "FRANKLIN-L6-3.3": f("ATM", E_, 3.3, "NC", 6, 2500, 1200, "SAE30", 5.0, 3000),
    "FRANKLIN-L6-4.4": f("ATM", E_, 4.4, "NC", 6, 3100, 1600, "SAE30", 6.0, 3000),
    "FRANKLIN-V12-6.8": f("ATM", E_, 6.8, "NC", 12, 3100, 1600, "SAE30", 9.0, 3000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Franklin", lambda fam: "Franklin")
L = []
IND = "moteur refroidi par air ; marché nord-américain ; données indicatives (marque ancienne), à vérifier"

mg(L, "Model A", "A", "1", "1902-01", "1904-12", [("1.7 10", "FRANKLIN-1.7", 50)], portes=0, places=2, reservoir=30, remarques="Runabout, quatre cylindres transversal ; " + IND)
mg(L, "Series 9", "9", "1", "1925-01", "1927-12", [("3.3 L6 32", "FRANKLIN-L6-3.3", 160)], portes=4, places=5, reservoir=60, remarques="Berline ; " + IND)
mg(L, "Airman", "Airman", "1", "1928-01", "1932-12", [("4.4 L6 96", "FRANKLIN-L6-4.4", 260)], portes=4, places=5, reservoir=70,
   remarques="Berline nommée en hommage à Charles Lindbergh ; " + IND)
mg(L, "Olympic", "Olympic", "1", "1933-01", "1934-12", [("4.4 L6 101", "FRANKLIN-L6-4.4", 270)], portes=4, places=5, reservoir=70,
   remarques="Carrosserie Reo Flying Cloud ; " + IND)
mg(L, "V12", "V12", "1", "1932-01", "1934-12", [("6.8 V12 152", "FRANKLIN-V12-6.8", 380)], portes=4, places=5, reservoir=95, remarques="Berline et limousine V12 ; " + IND)

MOT = Motorisations("Franklin", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Franklin": L}
MOTEURS = MOT.moteurs()
