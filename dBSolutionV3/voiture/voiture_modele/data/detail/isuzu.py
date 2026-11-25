"""Isuzu : générations, phases, motorisations et moteurs liés.
Marché européen par défaut : Trooper, Piazza, Gemini, Rodeo (pick-up), D-Max (dont D-Max EV). Modèles d'autres marchés,
signalés en remarque : 117 Coupé, Bellett, Florian (Japon), Panther (Indonésie), MU-X (Asie, Australie), Amigo, Axiom,
Ascender et VehiCROSS (Amérique du Nord, hp convertis en ch ×1,014). Isuzu a quitté le marché automobile nord-américain en 2009.
Moteurs Isuzu au motoriste « Isuzu » ; moteurs GM de l'Ascender repris de gmc.py et chevrolet.py (motoriste « Chevrolet »).
Données anciennes indicatives. Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ;
la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .gmc import FAMILLES as FAMILLES_GMC

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

PROPRES = {
    "G150": f("ATM", E_, 1.5, C, 4, 5400, 3200, "20W50", 4.0, 5000),
    "G161W": f("ATM", E_, 1.6, C, 4, 6400, 5000, "20W50", 4.0, 5000),
    "G180": f("ATM", E_, 1.8, C, 4, 5800, 3800, "20W50", 4.0, 5000),
    "G200": f("ATM", E_, 2.0, C, 4, 5600, 3600, "20W50", 4.0, 5000),
    "4ZC1-2.0T": f("TURBO", E_, 2.0, B, 4, 5400, 3000, "10W40", 4.5, 10000),
    "4XC1-1.5": f("ATM", E_, 1.5, B, 4, 5600, 3600, "10W40", 3.5, 10000),
    "4ZD1-2.3": f("ATM", E_, 2.3, B, 4, 4600, 2600, "10W40", 4.5, 10000),
    "4ZE1-2.6": f("ATM", E_, 2.6, B, 4, 4600, 2600, "10W40", 4.5, 10000),
    "6VD1-3.2": f("ATM", E_, 3.2, B, 6, 5400, 3000, "10W40", 5.0, 10000, a="V"),
    "6VE1-3.5": f("ATM", E_, 3.5, B, 6, 5400, 3000, "5W30", 5.0, 10000, a="V"),
    "C223-2.2D": f("ATM", D, 2.2, B, 4, 4600, 2400, "15W40", 5.0, 7500),
    "4FB1-1.8D": f("ATM", D, 1.8, B, 4, 5000, 3000, "15W40", 4.5, 7500),
    "4JA1-2.5D": f("ATM", D, 2.5, C, 4, 3900, 2000, "15W40", 6.0, 10000),
    "4JB1-2.8TD": f("TURBO", D, 2.8, C, 4, 3600, 2000, "15W40", 6.0, 10000),
    "4JG2-3.1TD": f("TURBO", D, 3.1, C, 4, 3600, 2000, "15W40", 6.5, 10000),
    "4JX1-3.0TD": f("TURBO", D, 3.0, C, 4, 3900, 2000, "5W30", 7.0, 10000),
    "4JA1-2.5TD": f("TURBO", D, 2.5, C, 4, 3900, 1800, "10W40", 6.0, 10000),
    "4JH1-3.0TD": f("TURBO", D, 3.0, C, 4, 3800, 2000, "10W40", 7.0, 10000),
    "4JK1-2.5TD": f("TURBO", D, 2.5, C, 4, 3600, 1800, "5W30", 7.0, 20000),
    "4JJ1-3.0TD": f("TURBO", D, 3.0, C, 4, 3600, 1800, "5W30", 7.0, 20000),
    "RZ4E-1.9": f("TURBO", D, 1.9, C, 4, 3600, 2000, "5W30", 6.0, 20000),
    "ISUZU-2.2D": f("TURBO", D, 2.2, C, 4, 3600, 1600, "5W30", 6.5, 20000),
    "ISUZU-EV": electrique(),
}
GM = {k: FAMILLES_GMC[k] for k in ("LL8-4.2", "LMG-5.3")}
FAMILLES = {**PROPRES, **GM}


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


NA = "Marché nord-américain (hp convertis en ch)"
JP = "Marché japonais"
mg = SaisieMoteurs(FAMILLES, "Isuzu", lambda fam: "Chevrolet" if fam in GM else "Isuzu")
L = []

# ---------------------------------------------------------------- japonaises historiques
mg(L, "Bellett", "PR", "1", "1963-11", "1973-12", [("1.5 68", "G150", 113), ("1600 GT 90", "G161W", 125, {"debut": "1964-04"})], portes=4, reservoir=45,
   remarques=JP + " ; berline, coupé GT ; données indicatives")
mg(L, "117 Coupé", "PA", "1", "1968-12", "1981-05",
   [("1.6 DOHC 120", "G161W", 145, {"fin": "1972-12"}), ("1.8 115", "G180", 152, {"debut": "1970-11"}), ("2.0 135", "G200", 172, {"debut": "1977-01"})],
   portes=2, places=4, reservoir=55, remarques=JP + " ; dessinée par Giugiaro ; données indicatives")
mg(L, "Isuzu Florian", "PA20", "1", "1967-11", "1983-04",
   [("1.6 95", "G161W", 132), ("1.8 100", "G180", 145, {"debut": "1970-11"}), ("2.2 D 62", "C223-2.2D", 137, {"debut": "1973-01"})], portes=4, reservoir=50,
   remarques=JP + " ; données indicatives")
mg(L, "Gemini", "PF", "1", "1974-11", "1987-01", [("1.6 100", "G180", 132), ("1.8 D 61", "4FB1-1.8D", 113, {"debut": "1979-11"})], portes=4, reservoir=50,
   remarques=JP + " ; plateforme GM T (cousine de l'Opel Kadett C) ; données indicatives")
mg(L, "Gemini", "JT", "1", "1985-05", "1990-12", [("1.5 73", "4XC1-1.5", 115)], portes=4, reservoir=42,
   remarques="Traction avant ; vendue en Europe sous les noms Gemini ou Isuzu (« I-Mark » en Amérique du Nord) ; données indicatives")
mg(L, "Piazza", "JR", "1", "1981-06", "1991-12", [("2.0 120", "G200", 167), ("2.0 Turbo 150", "4ZC1-2.0T", 226, {"debut": "1984-06"})], portes=3, places=4,
   reservoir=58, remarques="Dessinée par Giugiaro ; Piazza Turbo vendue en Europe (châssis « Handling by Lotus », 1988) ; données indicatives")

# ---------------------------------------------------------------- 4x4
mg(L, "Trooper", "UBS", "1", "1981-09", "1991-12",
   [("2.3 96", "4ZD1-2.3", 177), ("2.6 115", "4ZE1-2.6", 196, {"debut": "1988-01"}), ("2.2 D 61", "C223-2.2D", 137, {"fin": "1986-12"}),
    ("2.8 TD 95", "4JB1-2.8TD", 220, {"debut": "1987-01"})], portes=5, places=5, reservoir=83, remarques="3 et 5 portes ; données indicatives")
mg(L, "Trooper", "UBS", "2", "1991-12", "2002-12",
   [("3.2 V6 177", "6VD1-3.2", 260, {"fin": "1997-12"}), ("3.5 V6 215", "6VE1-3.5", 314, {"debut": "1998-01"}), ("3.1 TD 114", "4JG2-3.1TD", 260, {"fin": "1998-06"}),
    ("3.0 DTI 159", "4JX1-3.0TD", 333, {"debut": "1998-07"})], portes=5, places=7, reservoir=85,
   remarques="Deuxième génération, 3 et 5 portes ; restylage 1998 ; vendu aussi comme Opel Monterey")
mg(L, "VehiCROSS", "UGS", "1", "1997-04", "2001-12", [("3.5 V6 218", "6VE1-3.5", 312)], portes=3, places=4, reservoir=65,
   remarques=NA + " et Japon (3.2 V6) ; SUV 3 portes")
mg(L, "Amigo", "UBS", "1", "1989-01", "1994-12", [("2.3 97", "4ZD1-2.3", 171), ("2.6 122", "4ZE1-2.6", 203)], portes=3, places=4, reservoir=60, remarques=NA)
mg(L, "Amigo", "UBS", "2", "1998-01", "2000-12", [("2.2 132", "4ZD1-2.3", 197), ("3.2 V6 208", "6VD1-3.2", 290)], portes=3, places=4, reservoir=60,
   remarques=NA + " ; renommé Rodeo Sport en 2001 ; données indicatives")
mg(L, "Axiom", "UPR", "1", "2001-10", "2004-12", [("3.5 V6 233", "6VE1-3.5", 312, {"fin": "2003-12"}), ("3.5 V6 DI 253", "6VE1-3.5", 333, {"debut": "2004-01"})],
   reservoir=80, remarques=NA)
mg(L, "Ascender", "GMT360", "1", "2002-10", "2008-12",
   [("4.2 I6 279", "LL8-4.2", 373), ("5.3 V8 294", "LMG-5.3", 441, {"fin": "2004-12"}), ("5.3 V8 304", "LMG-5.3", 434, {"debut": "2005-01", "fin": "2006-12"})],
   places=7, reservoir=83, remarques=NA + " ; version de la GMC Envoy")
mg(L, "MU-X", "RF10", "1", "2013-10", "2021-01", [("2.5 TD 136", "4JK1-2.5TD", 320), ("3.0 TD 177", "4JJ1-3.0TD", 380)], places=7, reservoir=70,
   remarques="Marchés asiatiques et australien ; non commercialisé en Europe")
mg(L, "MU-X", "RJ", "1", "2021-01", None, [("1.9 Ddi 150", "RZ4E-1.9", 350), ("3.0 Ddi 190", "4JJ1-3.0TD", 450)], places=7, reservoir=80,
   remarques="Marchés asiatiques et australien ; non commercialisé en Europe")
mg(L, "Panther", "TBR", "1", "1991-01", "2017-12", [("2.5 D 80", "4JA1-2.5D", 167)], places=8, reservoir=70,
   remarques="Monospace pour le marché indonésien ; données indicatives")

# ---------------------------------------------------------------- pick-up européens
mg(L, "Rodeo", "TFR", "1", "2002-09", "2007-06", [("2.5 TD 101", "4JA1-2.5TD", 216), ("3.0 TD 130", "4JH1-3.0TD", 280)], portes=4, reservoir=76,
   remarques="Pick-up (base TF), cabines simple, allongée et double ; renommé D-Max en Europe en 2007")
mg(L, "D-Max", "TFR", "1", "2007-07", "2012-09", [("2.5 TD 136", "4JK1-2.5TD", 294), ("3.0 TD 163", "4JJ1-3.0TD", 360)], portes=4, reservoir=76,
   remarques="Ancien Rodeo européen ; cabines simple, allongée et double")
mg(L, "D-Max", "RT50", "1", "2012-10", "2017-05", [("2.5 TD 163", "4JK1-2.5TD", 400)], portes=4, reservoir=76, remarques="Cabines simple, allongée et double")
mg(L, "D-Max", "RT50", "2", "2017-06", "2020-11", [("1.9 Ddi 164", "RZ4E-1.9", 360)], portes=4, reservoir=76, remarques="Restylage, moteur 1.9 Euro 6")
mg(L, "D-Max", "RG", "1", "2020-12", "2024-02", [("1.9 Ddi 164", "RZ4E-1.9", 360)], portes=4, reservoir=76, remarques="Troisième génération")
mg(L, "D-Max", "RG", "2", "2024-03", None,
   [("1.9 Ddi 164", "RZ4E-1.9", 360, {"fin": "2026-04"}), ("EV 190", "ISUZU-EV", 325, el(67, debut="2025-10")), ("2.2 Ddi 163", "ISUZU-2.2D", 400, {"debut": "2026-05"})],
   portes=4, reservoir=76,
   remarques="Restylage ; D-Max EV (4x4 permanent, 66,9 kWh) ; nouveau 2.2 diesel et boîte automatique 8 rapports en 2026 (couple indicatif)")

MOT = Motorisations("Isuzu", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Isuzu": L}
MOTEURS = MOT.moteurs()
