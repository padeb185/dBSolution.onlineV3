"""Caterham : générations, phases, motorisations (marché européen) et moteurs liés.
Seven (châssis Series 3, toutes époques), Seven CSR et Caterham 21. Les moteurs (Ford, Rover, Vauxhall, Suzuki)
sont rattachés au motoriste « Caterham ». Le coupé électrique Project V n'est pas encore produit.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom.
Le châssis large SV est une option de carrosserie sur les mêmes motorisations."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C, B = "CHAINE", "COURROIE"

FAMILLES = {
    "KENT-1.6": f("ATM", E_, 1.6, C, 4, 5500, 3500, "20W50", 4.0, 5000),
    "LOTUS-TC-1.6": f("ATM", E_, 1.6, C, 4, 6500, 5500, "20W50", 4.5, 5000),
    "ROVER-K-1.4": f("ATM", E_, 1.4, B, 4, 6250, 4000, "10W40", 4.0, 10000),
    "ROVER-K-1.6": f("ATM", E_, 1.6, B, 4, 6250, 4000, "10W40", 4.0, 10000),
    "ROVER-K-1.8": f("ATM", E_, 1.8, B, 4, 7000, 4500, "10W40", 4.0, 10000),
    "ROVER-K-1.8-VVC": f("ATM", E_, 1.8, B, 4, 7000, 4500, "10W40", 4.0, 10000),
    "VX-2.0-HPC": f("ATM", E_, 2.0, B, 4, 6000, 4800, "10W40", 4.5, 10000),
    "SIGMA-1.6": f("ATM", E_, 1.6, B, 4, 6800, 4500, "5W30", 4.0, 10000),
    "DURATEC-2.0": f("ATM", E_, 2.0, C, 4, 7600, 6300, "5W30", 4.5, 10000),
    "DURATEC-2.0-SC": f("TURBO", E_, 2.0, C, 4, 7700, 7350, "5W30", 4.5, 10000),
    "DURATEC-2.3": f("ATM", E_, 2.3, C, 4, 7500, 6000, "5W30", 4.5, 10000),
    "SUZUKI-K6A-T": f("TURBO", E_, 0.66, C, 3, 7000, 3400, "5W30", 3.0, 10000),
}

mg = SaisieMoteurs(FAMILLES, "Caterham")
L = []
R = "Roadster 2 places ; châssis large SV en option"

mg(L, "Seven", "S3", "1", "1973-05", "1990-12",
   [("Kent 1.6 84", "KENT-1.6", 130), ("Kent 1.6 GT 110", "KENT-1.6", 140, {"debut": "1980-01"}),
    ("Lotus Twin Cam 1.6 126", "LOTUS-TC-1.6", 153, {"fin": "1984-12"})], portes=0, places=2, reservoir=36,
   remarques="Reprise de la Lotus Seven Series 3 ; données indicatives")
mg(L, "Seven", "S3", "2", "1991-01", "2007-12",
   [("1.4 K 103", "ROVER-K-1.4", 127), ("1.6 K 115", "ROVER-K-1.6", 145), ("1.8 K 122", "ROVER-K-1.8", 160, {"debut": "1996-01"}),
    ("1.8 K Supersport 135", "ROVER-K-1.8", 165, {"debut": "1996-01"}), ("1.8 K VVC 150", "ROVER-K-1.8-VVC", 174, {"debut": "1996-01"}),
    ("2.0 HPC 175", "VX-2.0-HPC", 196, {"fin": "1998-12"}), ("Superlight R300 1.8 K 160", "ROVER-K-1.8-VVC", 180, {"debut": "2000-01"}),
    ("Superlight R400 1.8 K 190", "ROVER-K-1.8-VVC", 190, {"debut": "2000-01"}), ("Superlight R500 1.8 K 230", "ROVER-K-1.8-VVC", 203, {"debut": "1999-06"})],
   portes=0, places=2, reservoir=36, remarques=R + " ; moteurs Rover K-Series et Vauxhall")
mg(L, "Seven", "S3", "3", "2008-01", "2014-12",
   [("Roadsport 125 1.6 125", "SIGMA-1.6", 163), ("Roadsport 150 1.6 150", "SIGMA-1.6", 163), ("Roadsport 175 2.0 175", "DURATEC-2.0", 190),
    ("Superlight R300 2.0 175", "DURATEC-2.0", 190), ("Superlight R400 2.0 210", "DURATEC-2.0", 206),
    ("Superlight R500 2.0 263", "DURATEC-2.0", 245), ("160 0.66 Turbo 80", "SUZUKI-K6A-T", 107, {"debut": "2013-06"}),
    ("485 2.0 240", "DURATEC-2.0", 206, {"debut": "2013-01"}), ("620R 2.0 Compresseur 310", "DURATEC-2.0-SC", 297, {"debut": "2013-06"})],
   portes=0, places=2, reservoir=36, remarques=R + " ; moteurs Ford Sigma et Duratec")
mg(L, "Seven", "S3", "4", "2015-01", "2022-10",
   [("160 0.66 Turbo 80", "SUZUKI-K6A-T", 107, {"fin": "2020-12"}), ("170 0.66 Turbo 85", "SUZUKI-K6A-T", 116, {"debut": "2021-09"}),
    ("270 1.6 135", "SIGMA-1.6", 165), ("310 1.6 152", "SIGMA-1.6", 169), ("360 2.0 180", "DURATEC-2.0", 194),
    ("420 2.0 210", "DURATEC-2.0", 203), ("485 2.0 240", "DURATEC-2.0", 206, {"fin": "2019-12"}), ("620 2.0 Compresseur 310", "DURATEC-2.0-SC", 297),
    ("Super Seven 1600 1.6 135", "SIGMA-1.6", 165, {"debut": "2020-01"})], portes=0, places=2, reservoir=36,
   remarques=R + " ; versions S (route) et R (piste)")
mg(L, "Seven", "S3", "5", "2022-11", None,
   [("170 0.66 Turbo 85", "SUZUKI-K6A-T", 116), ("340 2.0 170", "DURATEC-2.0", 190), ("420 2.0 210", "DURATEC-2.0", 203),
    ("620 2.0 Compresseur 310", "DURATEC-2.0-SC", 297), ("Super Seven 600 0.66 Turbo 85", "SUZUKI-K6A-T", 116, {"debut": "2024-01"}),
    ("Super Seven 2000 2.0 180", "DURATEC-2.0", 194, {"debut": "2024-01"})], portes=0, places=2, reservoir=36,
   remarques=R + " ; le 340 remplace les 270/310 ; mises à jour 2026 (nouvelles couleurs, éclairage)")
mg(L, "Seven CSR", "CSR", "1", "2005-06", "2017-12",
   [("CSR 175 2.3 175", "DURATEC-2.3", 220), ("CSR 260 2.3 260", "DURATEC-2.3", 270), ("485 CSR 2.0 240", "DURATEC-2.0", 206, {"debut": "2014-01"})],
   portes=0, places=2, reservoir=40, remarques="Châssis CSR à suspension arrière indépendante ; CSR Twenty (2024) non reprise")
mg(L, "21", "21", "1", "1994-10", "1999-12", [("1.6 K 115", "ROVER-K-1.6", 145), ("1.8 K VVC 145", "ROVER-K-1.8-VVC", 174, {"debut": "1996-01"})],
   portes=2, places=2, reservoir=36, remarques="Roadster carrossé (environ 50 ex.) ; données indicatives")

MOT = Motorisations("Caterham", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Caterham": L}
MOTEURS = MOT.moteurs()
