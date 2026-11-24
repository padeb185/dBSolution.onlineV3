"""Buick : générations, motorisations (marché nord-américain — Buick n'est pas vendu en Europe) et moteurs liés.
Electra, Skylark, Riviera, LeSabre, Park Avenue, Century, Regal, LaCrosse, Lucerne, Verano, Cascada, Rendezvous, Rainier,
Terraza, Encore, Encore GX, Envision, Enclave, Envista. Modèles d'avant 1985, modèles chinois (Electra E5…) et concepts non repris.
Puissances converties des hp américains en ch (×1,014, arrondi). Données antérieures à 2000 indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C, B = "CHAINE", "COURROIE"

FAMILLES = {
    "GM-3800": f("ATM", E_, 3.8, C, 6, 5200, 4000, "5W30", 4.3, 12000, a="V"),
    "GM-3800-SC": f("TURBO", E_, 3.8, C, 6, 5200, 3600, "5W30", 4.3, 12000, a="V"),
    "GM-3.1": f("ATM", E_, 3.1, C, 6, 5200, 4000, "5W30", 4.3, 12000, a="V"),
    "GM-3.4": f("ATM", E_, 3.4, C, 6, 5200, 4000, "5W30", 4.3, 12000, a="V"),
    "GM-3.5": f("ATM", E_, 3.5, C, 6, 5600, 4400, "5W30", 4.3, 12000, a="V"),
    "GM-3.9": f("ATM", E_, 3.9, C, 6, 5700, 3200, "5W30", 4.3, 12000, a="V"),
    "GM-3.6": f("ATM", E_, 3.6, C, 6, 6800, 5000, "5W30", 5.7, 12000, a="V"),
    "GM-4.6-V8": f("ATM", E_, 4.6, C, 8, 5600, 4400, "5W30", 7.1, 12000, a="V"),
    "GM-5.3-V8": f("ATM", E_, 5.3, C, 8, 5200, 4000, "5W30", 5.7, 12000, a="V"),
    "GM-4.2-I6": f("ATM", E_, 4.2, C, 6, 6000, 4600, "5W30", 6.6, 12000),
    "GM-2.3-QUAD4": f("ATM", E_, 2.3, C, 4, 6000, 4800, "5W30", 3.8, 12000),
    "GM-2.4": f("ATM", E_, 2.4, C, 4, 6700, 4900, "5W30", 4.7, 12000),
    "GM-2.4-EASSIST": f("HYB_TE", E_, 2.4, C, 4, 6700, 4900, "5W30", 4.7, 12000),
    "GM-2.5": f("ATM", E_, 2.5, C, 4, 6300, 4400, "5W30", 4.7, 12000),
    "GM-2.0T": f("TURBO", E_, 2.0, C, 4, 5300, 2000, "5W30", 4.7, 12000),
    "GM-2.5T": f("TURBO", E_, 2.5, C, 4, 5600, 2000, "0W20", 5.2, 12000),
    "GM-1.4T": f("TURBO", E_, 1.4, B, 4, 4900, 1850, "5W30", 4.0, 12000),
    "GM-1.6T": f("TURBO", E_, 1.6, C, 4, 5500, 2000, "5W30", 4.5, 12000),
    "GM-1.2T": f("TURBO", E_, 1.2, C, 3, 5000, 2500, "0W20", 3.8, 12000),
    "GM-1.3T": f("TURBO", E_, 1.3, C, 3, 5600, 1600, "0W20", 3.8, 12000),
}

mg = SaisieMoteurs(FAMILLES, "Buick")
L = []
NA = "Marché nord-américain"
IND = NA + " ; données indicatives"

# ---------------------------------------------------------------- berlines et coupés
mg(L, "Electra", "C-body", "1", "1985-01", "1990-12", [("Electra 3.8 V6 152", "GM-3800", 271)], portes=4, reservoir=68, remarques=IND + " ; Electra / Park Avenue traction")
mg(L, "Skylark", "N-body", "1", "1992-01", "1998-12", [("2.3 Quad 4 117", "GM-2.3-QUAD4", 190), ("3.3 V6 162", "GM-3.1", 251), ("3.1 V6 157", "GM-3.1", 251, {"debut": "1994-01"})],
   portes=4, reservoir=57, remarques=IND + " ; coupé et berline")
mg(L, "Riviera", "G-body", "1", "1995-01", "1999-12", [("3.8 V6 208", "GM-3800", 312), ("3.8 V6 Supercharged 243", "GM-3800-SC", 380)], portes=2, places=5, reservoir=76,
   remarques=IND + " ; coupé")
mg(L, "LeSabre", "H-body", "1", "1992-01", "1999-12", [("3.8 V6 172", "GM-3800", 305), ("3.8 V6 208", "GM-3800", 312, {"debut": "1996-01"})], portes=4, reservoir=68, remarques=IND)
mg(L, "LeSabre", "H-body", "2", "2000-01", "2005-12", [("3.8 V6 208", "GM-3800", 312)], portes=4, reservoir=68, remarques=NA)
mg(L, "Park Avenue", "C-body", "2", "1997-01", "2005-12", [("3.8 V6 208", "GM-3800", 312), ("Ultra 3.8 V6 Supercharged 243", "GM-3800-SC", 380)], portes=4, reservoir=70,
   remarques=NA)
mg(L, "Century", "W-body", "1", "1997-01", "2005-12", [("3.1 V6 162", "GM-3.1", 251), ("3.1 V6 177", "GM-3.1", 258, {"debut": "2000-01"})], portes=4, reservoir=65, remarques=NA)
mg(L, "Regal", "W-body", "1", "1997-01", "2004-12", [("3.8 V6 198", "GM-3800", 312), ("GS 3.8 V6 Supercharged 243", "GM-3800-SC", 380)], portes=4, reservoir=65, remarques=NA)
mg(L, "Regal", "Epsilon II", "1", "2011-01", "2017-12",
   [("2.4 185", "GM-2.4", 233), ("2.4 eAssist 185", "GM-2.4-EASSIST", 233, {"debut": "2012-01"}), ("Turbo 2.0 223", "GM-2.0T", 353), ("GS 2.0 Turbo 263", "GM-2.0T", 400, {"debut": "2012-01"})],
   portes=4, reservoir=70, remarques=NA + " ; base Opel Insignia")
mg(L, "Regal", "E2XX", "1", "2018-01", "2020-12", [("Sportback 2.0 Turbo 254", "GM-2.0T", 401), ("TourX 2.0 Turbo 254", "GM-2.0T", 401), ("GS 3.6 V6 314", "GM-3.6", 381)],
   reservoir=62, remarques=NA + " ; Sportback et TourX (base Opel Insignia B)")
mg(L, "LaCrosse", "W-body", "1", "2005-01", "2009-12", [("3.8 V6 203", "GM-3800", 312), ("3.6 V6 243", "GM-3.6", 305), ("Super 5.3 V8 304", "GM-5.3-V8", 438, {"debut": "2008-01"})],
   portes=4, reservoir=64, remarques=NA)
mg(L, "LaCrosse", "Epsilon II", "1", "2010-01", "2016-12", [("2.4 eAssist 185", "GM-2.4-EASSIST", 233), ("3.6 V6 308", "GM-3.6", 359)], portes=4, reservoir=70, remarques=NA)
mg(L, "LaCrosse", "P2XX", "1", "2017-01", "2019-12", [("3.6 V6 314", "GM-3.6", 381), ("2.5 eAssist 197", "GM-2.5", 260, {"debut": "2018-01"})], portes=4, reservoir=60, remarques=NA)
mg(L, "Lucerne", "G-body", "2", "2006-01", "2011-12", [("3.8 V6 200", "GM-3800", 312), ("3.9 V6 230", "GM-3.9", 325, {"debut": "2009-01"}), ("4.6 V8 279", "GM-4.6-V8", 393)],
   portes=4, reservoir=70, remarques=NA)
mg(L, "Verano", "Delta II", "1", "2012-01", "2017-12", [("2.4 182", "GM-2.4", 232), ("Turbo 2.0 254", "GM-2.0T", 352, {"debut": "2013-01"})], portes=4, reservoir=59, remarques=NA)
mg(L, "Cascada", "Delta II", "C", "2016-01", "2019-12", [("1.6 Turbo 203", "GM-1.6T", 300)], portes=2, places=4, reservoir=56, remarques=NA + " ; base Opel Cascada")

# ---------------------------------------------------------------- SUV et monospaces
mg(L, "Rendezvous", "U-body", "1", "2002-01", "2007-12", [("3.4 V6 188", "GM-3.4", 285), ("3.6 V6 248", "GM-3.6", 319, {"debut": "2004-01"})], places=7, reservoir=70, remarques=NA)
mg(L, "Rainier", "GMT360", "1", "2004-01", "2007-12", [("4.2 I6 279", "GM-4.2-I6", 373), ("5.3 V8 294", "GM-5.3-V8", 441)], reservoir=83, remarques=NA)
mg(L, "Terraza", "U-body", "2", "2005-01", "2007-12", [("3.5 V6 203", "GM-3.5", 298), ("3.9 V6 243", "GM-3.9", 325, {"debut": "2006-01"})], places=7, reservoir=79, remarques=NA + " ; monospace")
mg(L, "Encore", "Gamma II", "1", "2013-01", "2022-12", [("1.4 Turbo 140", "GM-1.4T", 200), ("1.4 Turbo 155", "GM-1.4T", 240, {"debut": "2017-01"})], reservoir=53,
   remarques=NA + " ; jumeau Opel Mokka")
mg(L, "Encore GX", "GEM", "1", "2020-01", None, [("1.2 Turbo 139", "GM-1.2T", 236), ("1.3 Turbo 157", "GM-1.3T", 255)], reservoir=50, remarques=NA + " ; produit en Corée du Sud")
mg(L, "Envision", "D2XX", "1", "2016-01", "2020-12", [("2.5 199", "GM-2.5", 260), ("2.0 Turbo 256", "GM-2.0T", 400)], reservoir=65, remarques=NA + " ; produit en Chine")
mg(L, "Envision", "E2", "1", "2021-01", None, [("2.0 Turbo 231", "GM-2.0T", 350)], reservoir=56, remarques=NA + " ; AWD de série, produit en Chine ; restylage 2024")
mg(L, "Enclave", "Lambda", "1", "2008-01", "2017-12", [("3.6 V6 279", "GM-3.6", 366), ("3.6 V6 292", "GM-3.6", 360, {"debut": "2009-01"})], places=7, reservoir=83, remarques=NA)
mg(L, "Enclave", "C1XX", "1", "2018-01", "2024-06", [("3.6 V6 314", "GM-3.6", 361)], places=7, reservoir=82, remarques=NA)
mg(L, "Enclave", "C1XX", "2", "2024-07", None, [("2.5 Turbo 333", "GM-2.5T", 441)], places=7, reservoir=82, remarques=NA + " ; 3e génération (millésime 2025)")
mg(L, "Envista", "GEM", "E", "2023-07", None, [("1.2 Turbo 139", "GM-1.2T", 236)], reservoir=50, remarques=NA + " ; crossover traction, produit en Corée du Sud")

MOT = Motorisations("Buick", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Buick": L}
MOTEURS = MOT.moteurs()
