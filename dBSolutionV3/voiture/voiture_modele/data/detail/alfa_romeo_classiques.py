"""Alfa Romeo (ancêtres et modèles anciens) : générations, phases, motorisations (marché européen) et moteurs liés.
A.L.F.A. (Anonima Lombarda Fabbrica Automobili, Portello, 1910-1915) : 24 HP, 12 HP, 15 HP, 40-60 HP et 20-30 HP ;
Alfa Romeo d'avant-guerre (Nicola Romeo, Vittorio Jano) : RL, RM, 6C 1500, 6C 1750, 8C 2300, 6C 2300, 8C 2900 et 6C 2500 ;
après-guerre : 1900, 2000, 2600, Montreal, Alfa 6, 90, Arna et SZ / RZ (non repris dans alfa_romeo.py).
Moteurs Busso, boxer, double arbre et VM repris d'alfa_romeo.py (mêmes familles et couples) ; moteurs anciens ajoutés.
Puissances en ch. Données indicatives (modèles anciens), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .alfa_romeo import FAMILLES as FAMILLES_ALFA

E_ = "ESS"
C = "CHAINE"


def anc(t, l, n, rpm, nmrpm, q):
    return f(t, E_, l, "NC", n, rpm, nmrpm, "SAE30", q, 3000)


ANCIENS = {
    "ALFA-24HP-4.1": anc("ATM", 4.1, 4, 2200, 1200, 6.0),
    "ALFA-12HP-2.4": anc("ATM", 2.4, 4, 2200, 1200, 4.5),
    "ALFA-40HP-6.1": anc("ATM", 6.1, 4, 2200, 1400, 7.0),
    "ALFA-20HP-4.2": anc("ATM", 4.2, 4, 2400, 1400, 6.0),
    "AR-RL-L6-3.0": anc("ATM", 3.0, 6, 3500, 2000, 6.0),
    "AR-RM-2.0": anc("ATM", 2.0, 4, 3200, 1800, 4.5),
    "AR-6C-1.5": anc("ATM", 1.5, 6, 4500, 2800, 4.5),
    "AR-6C-1.5C": anc("TURBO", 1.5, 6, 5000, 3200, 4.5),
    "AR-6C-1.75": anc("ATM", 1.75, 6, 4400, 2800, 5.0),
    "AR-6C-1.75C": anc("TURBO", 1.75, 6, 4600, 3200, 5.0),
    "AR-8C-2.3C": anc("TURBO", 2.3, 8, 5200, 3500, 8.0),
    "AR-6C-2.3": anc("ATM", 2.3, 6, 4400, 2800, 6.0),
    "AR-8C-2.9C": anc("TURBO", 2.9, 8, 5200, 3600, 10.0),
    "AR-6C-2.5": anc("ATM", 2.5, 6, 4800, 3000, 6.5),
    "AR-1900": f("ATM", E_, 1.9, C, 4, 5200, 3500, "20W50", 6.0, 5000),
    "AR-2000": f("ATM", E_, 2.0, C, 4, 5300, 3700, "20W50", 6.5, 5000),
    "AR-2600-L6": f("ATM", E_, 2.6, C, 6, 5900, 4000, "20W50", 7.0, 5000),
    "AR-MONTREAL-V8-2.6": f("ATM", E_, 2.6, C, 8, 6500, 4750, "20W50", 9.0, 5000, a="V"),
    "BUSSO-2.0": f("ATM", E_, 2.0, "COURROIE", 6, 5600, 4000, "10W60", 6.0, 10000, a="V"),
}
REPRIS = {k: FAMILLES_ALFA[k] for k in ("AR-TC-1.8", "AR-TC-2.0", "AR-BOXER-1.2", "AR-BOXER-1.3", "BUSSO-2.5", "BUSSO-3.0", "VM-2.4TD", "VM-2.5TD")}
FAMILLES = {**ANCIENS, **REPRIS}
mg = SaisieMoteurs(FAMILLES, "Alfa Romeo", lambda fam: "Alfa Romeo")
L = []
IND = "données indicatives (modèle ancien), à vérifier"

# ---------------------------------------------------------------- A.L.F.A. (1910-1915)
mg(L, "24 HP", "24 HP", "1", "1910-06", "1913-12", [("4.1 42", "ALFA-24HP-4.1", 200)], portes=4, places=4, reservoir=70,
   remarques="Première voiture A.L.F.A. (Giuseppe Merosi) ; " + IND)
mg(L, "12 HP", "12 HP", "1", "1910-06", "1911-12", [("2.4 22", "ALFA-12HP-2.4", 95)], portes=4, places=4, reservoir=50, remarques="A.L.F.A. ; " + IND)
mg(L, "15 HP", "15 HP", "1", "1911-01", "1914-12", [("2.4 25", "ALFA-12HP-2.4", 100)], portes=4, places=4, reservoir=50, remarques="A.L.F.A., évolution de la 12 HP ; " + IND)
mg(L, "40-60 HP", "40-60 HP", "1", "1913-01", "1915-12", [("6.1 70", "ALFA-40HP-6.1", 300)], portes=4, places=4, reservoir=90,
   remarques="A.L.F.A. sportive, dont la Castagna aérodynamique ; " + IND)
mg(L, "20-30 HP", "20-30 HP", "1", "1914-01", "1921-12", [("4.2 49", "ALFA-20HP-4.2", 210), ("ES 4.2 67", "ALFA-20HP-4.2", 240, {"debut": "1920-01"})],
   portes=4, places=4, reservoir=70, remarques="Dernière A.L.F.A., première à porter le nom Alfa Romeo (1920) ; " + IND)

# ---------------------------------------------------------------- Alfa Romeo d'avant-guerre
mg(L, "RL", "RL", "1", "1922-01", "1927-12", [("3.0 L6 56", "AR-RL-L6-3.0", 170), ("Sport 3.0 L6 71", "AR-RL-L6-3.0", 190), ("SS 3.0 L6 83", "AR-RL-L6-3.0", 205)],
   portes=4, places=5, reservoir=70, remarques="Six cylindres Merosi, Normale, Turismo, Sport et Super Sport (Targa Florio 1923) ; " + IND)
mg(L, "RM", "RM", "1", "1923-01", "1925-12", [("2.0 40", "AR-RM-2.0", 120)], portes=4, places=4, reservoir=55, remarques="Quatre cylindres dérivé de la RL ; " + IND)
mg(L, "6C 1500", "6C 1500", "1", "1927-01", "1929-12", [("1.5 L6 44", "AR-6C-1.5", 85), ("Sport 1.5 L6 54", "AR-6C-1.5", 95), ("SS Compressore 1.5 L6 76", "AR-6C-1.5C", 120)],
   portes=4, places=4, reservoir=50, remarques="Première Alfa de Vittorio Jano, Sport double arbre ; " + IND)
mg(L, "6C 1750", "6C 1750", "1", "1929-01", "1933-12",
   [("1.75 L6 46", "AR-6C-1.75", 95), ("Sport 1.75 L6 55", "AR-6C-1.75", 105), ("SS Compressore 1.75 L6 85", "AR-6C-1.75C", 140), ("GS Compressore 1.75 L6 102", "AR-6C-1.75C", 155)],
   portes=2, places=2, reservoir=60, remarques="Turismo, Sport, Super Sport et Gran Sport (Zagato, Touring) ; Mille Miglia 1929-1930 ; " + IND)
mg(L, "8C 2300", "8C 2300", "1", "1931-01", "1934-12", [("2.3 L8 Compressore 142", "AR-8C-2.3C", 210), ("Monza 2.3 L8 Compressore 165", "AR-8C-2.3C", 230)],
   portes=2, places=2, reservoir=100, remarques="Huit cylindres double arbre à compresseur, victoires au Mans (1931-1934) ; " + IND)
mg(L, "6C 2300", "6C 2300", "1", "1934-01", "1939-12", [("2.3 L6 70", "AR-6C-2.3", 150), ("Pescara 2.3 L6 95", "AR-6C-2.3", 175)], portes=4, places=5, reservoir=70,
   remarques="Turismo, Gran Turismo et Pescara ; " + IND)
mg(L, "8C 2900", "8C 2900", "1", "1936-01", "1939-12", [("2.9 L8 Compressore 180", "AR-8C-2.9C", 260)], portes=2, places=2, reservoir=120,
   remarques="8C 2900 B, deux compresseurs, carrosseries Touring (Mille Miglia 1938) ; " + IND)
mg(L, "6C 2500", "6C 2500", "1", "1939-01", "1953-12", [("2.5 L6 87", "AR-6C-2.5", 170), ("Sport 2.5 L6 95", "AR-6C-2.5", 175), ("SS 2.5 L6 110", "AR-6C-2.5", 190)],
   portes=2, places=4, reservoir=80, remarques="Turismo, Sport, Super Sport, Freccia d'Oro et Villa d'Este ; dernière Alfa à châssis séparé ; " + IND)

# ---------------------------------------------------------------- après-guerre
mg(L, "1900", "1900", "1", "1950-10", "1959-12", [("1.9 80", "AR-1900", 132), ("TI 1.9 100", "AR-1900", 147, {"debut": "1951-01"}),
                                                 ("Super 1.9 90", "AR-1900", 147, {"debut": "1954-01"}), ("Super Sprint 1.9 115", "AR-1900", 157, {"debut": "1954-01"})],
   portes=4, places=5, reservoir=53, remarques="Première Alfa monocoque produite en série, berline et coupés Sprint (Touring) ; " + IND)
mg(L, "2000", "2000", "1", "1958-01", "1962-12", [("Berlina 2.0 105", "AR-2000", 154), ("Spider 2.0 115", "AR-2000", 162), ("Sprint 2.0 115", "AR-2000", 162, {"debut": "1960-01"})],
   portes=4, places=5, reservoir=60, remarques="Berline, Spider Touring et Sprint Bertone ; " + IND)
mg(L, "2600", "2600", "1", "1962-01", "1968-12", [("Berlina 2.6 L6 130", "AR-2600-L6", 192), ("Sprint 2.6 L6 145", "AR-2600-L6", 213), ("Spider 2.6 L6 145", "AR-2600-L6", 213)],
   portes=4, places=5, reservoir=60, remarques="Six cylindres double arbre, Berlina, Sprint, Spider et SZ ; " + IND)
mg(L, "Montreal", "105.64", "1", "1970-01", "1977-12", [("2.6 V8 200", "AR-MONTREAL-V8-2.6", 235)], portes=2, places=4, reservoir=63,
   remarques="Coupé Bertone (Gandini), V8 dérivé du Tipo 33 de compétition ; " + IND)
mg(L, "Alfa 6", "119", "1", "1979-05", "1986-12", [("2.5 V6 160", "BUSSO-2.5", 213), ("2.0 V6 135", "BUSSO-2.0", 170, {"debut": "1983-01"}), ("2.5 TD 105", "VM-2.5TD", 235, {"debut": "1983-01"})],
   portes=4, places=5, reservoir=78, remarques="Berline de luxe, premier V6 Busso ; " + IND)
mg(L, "90", "162", "1", "1984-09", "1987-12", [("1.8 120", "AR-TC-1.8", 167), ("2.0 128", "AR-TC-2.0", 172), ("2.5 V6 156", "BUSSO-2.5", 206), ("2.4 TD 110", "VM-2.4TD", 235)],
   portes=4, places=5, reservoir=68, remarques="Berline Bertone sur base Alfetta ; " + IND)
mg(L, "Arna", "920", "1", "1983-09", "1987-12", [("1.2 63", "AR-BOXER-1.2", 88), ("ti 1.3 86", "AR-BOXER-1.3", 118, {"debut": "1984-01"})], portes=5, places=5, reservoir=50,
   remarques="Coentreprise avec Nissan (caisse Cherry, mécanique Alfasud) ; " + IND)
mg(L, "SZ", "ES-30", "1", "1989-01", "1993-12", [("3.0 V6 210", "BUSSO-3.0", 245)], portes=2, places=2, reservoir=70,
   remarques="Coupé SZ (1989-1991, « Il Mostro ») et roadster RZ (1992-1993) carrossés par Zagato ; " + IND)

MOT = Motorisations("Alfa Romeo", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Alfa Romeo": L}
MOTEURS = MOT.moteurs()
