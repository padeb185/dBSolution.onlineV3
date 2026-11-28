"""Minerva (Anvers, 1902-1956) : générations, phases, motorisations (marché européen) et moteurs liés.
Minervette, Type CC, 20 CV, AC, AK, AL (huit cylindres) et M4, à moteurs sans soupapes Knight à partir de 1910 ; Minerva-Land Rover
(Land Rover assemblé sous licence pour l'armée belge, 1951-1956). Puissances en ch. Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "MINERVA-1C-0.4": f("ATM", "ESS", 0.4, "NC", 1, 1800, 1200, "SAE30", 1.0, 1000),
    "MINERVA-KNIGHT-L4-4.1": f("ATM", "ESS", 4.1, "NC", 4, 2000, 1200, "SAE30", 6.0, 2000),
    "MINERVA-KNIGHT-L6-3.6": f("ATM", "ESS", 3.6, "NC", 6, 2600, 1400, "SAE30", 6.0, 2000),
    "MINERVA-KNIGHT-L4-2.0": f("ATM", "ESS", 2.0, "NC", 4, 3000, 1600, "SAE30", 4.0, 3000),
    "MINERVA-KNIGHT-L6-5.9": f("ATM", "ESS", 5.9, "NC", 6, 3000, 1600, "SAE30", 8.0, 3000),
    "MINERVA-KNIGHT-L8-6.6": f("ATM", "ESS", 6.6, "NC", 8, 3000, 1600, "SAE30", 9.0, 3000),
    "ROVER-2.0": f("ATM", "ESS", 2.0, "CHAINE", 4, 4000, 2000, "20W50", 5.0, 5000),
}
mg = SaisieMoteurs(FAMILLES, "Minerva", lambda fam: "Rover" if fam.startswith("ROVER") else "Minerva")
L = []
IND = "données indicatives (marque ancienne), à vérifier"
mg(L, "Minervette", "Minervette", "1", "1904-01", "1906-12", [("0.4 4", "MINERVA-1C-0.4", 15)], portes=0, places=2, reservoir=15, remarques="Voiturette monocylindre ; " + IND)
mg(L, "Type CC", "CC", "1", "1911-01", "1914-12", [("4.1 Knight 50", "MINERVA-KNIGHT-L4-4.1", 200)], portes=4, places=5, reservoir=70, remarques="Moteur sans soupapes Knight ; " + IND)
mg(L, "20 CV", "20 CV", "1", "1920-01", "1923-12", [("3.6 L6 Knight 60", "MINERVA-KNIGHT-L6-3.6", 200)], portes=4, places=5, reservoir=70, remarques=IND)
mg(L, "AC", "AC", "1", "1925-01", "1927-12", [("2.0 Knight 40", "MINERVA-KNIGHT-L4-2.0", 120)], portes=4, places=5, reservoir=55, remarques=IND)
mg(L, "AK", "AK", "1", "1927-01", "1937-12", [("5.9 L6 Knight 125", "MINERVA-KNIGHT-L6-5.9", 350)], portes=4, places=7, reservoir=100, remarques="Grande routière de luxe 32 CV ; " + IND)
mg(L, "AL", "AL", "1", "1930-01", "1937-12", [("6.6 L8 Knight 125", "MINERVA-KNIGHT-L8-6.6", 380)], portes=4, places=7, reservoir=110, remarques="Huit cylindres 40 CV ; " + IND)
mg(L, "M4", "M4", "1", "1934-01", "1937-12", [("2.0 Knight 45", "MINERVA-KNIGHT-L4-2.0", 125)], portes=4, places=5, reservoir=55, remarques=IND)
mg(L, "TT Land Rover", "Minerva-Land Rover", "1", "1951-01", "1956-12", [("2.0 52", "ROVER-2.0", 136)], portes=0, places=6, reservoir=45,
   remarques="Land Rover Series I assemblé sous licence pour l'armée belge, carrosserie en acier ; " + IND)

MOT = Motorisations("Minerva", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Minerva": L}
MOTEURS = MOT.moteurs()
