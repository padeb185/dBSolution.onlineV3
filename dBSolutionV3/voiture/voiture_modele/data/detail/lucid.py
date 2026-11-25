"""Lucid : générations, motorisations (marché nord-américain, hp convertis en ch ×1,014) et moteurs liés.
Air (Pure, Touring, Grand Touring, Dream Edition, Sapphire) et Gravity (Touring, Grand Touring, GT-S). Électriques à moteurs
Lucid (motoriste « Lucid »). Couples de certaines versions indicatifs. Cosmos et Earth (annoncés) non repris.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique

FAMILLES = {"LUCID-EV": electrique()}


def el(kwh, **kw):
    return {"batterie": kwh, **kw}


NA = "Marché nord-américain (hp convertis en ch) ; vendue aussi en Europe et au Moyen-Orient"
mg = SaisieMoteurs(FAMILLES, "Lucid")
L = []

mg(L, "Air", "Air", "1", "2021-10", None,
   [("Dream Edition Range AWD 946", "LUCID-EV", 1390, el(118, fin="2022-12")), ("Dream Edition Performance AWD 1127", "LUCID-EV", 1390, el(118, fin="2022-12")),
    ("Grand Touring AWD 830", "LUCID-EV", 1200, el(117)), ("Touring AWD 629", "LUCID-EV", 1200, el(92, debut="2022-06")),
    ("Pure RWD 436", "LUCID-EV", 550, el(84, debut="2023-06")), ("Pure AWD 487", "LUCID-EV", 550, el(88, debut="2022-12", fin="2023-12")),
    ("Sapphire AWD 1251", "LUCID-EV", 1939, el(118, debut="2023-11"))], portes=4, places=5, reservoir=0,
   remarques=NA + " ; architecture 900 V ; Sapphire à trois moteurs ; couple de la Touring indicatif")
mg(L, "Gravity", "Gravity", "1", "2025-04", None,
   [("Grand Touring AWD 840", "LUCID-EV", 1232, el(123)), ("Touring AWD 568", "LUCID-EV", 1000, el(89, debut="2025-12")),
    ("GT-S AWD 1085", "LUCID-EV", 1500, el(123, debut="2026-06"))], portes=5, places=7, reservoir=0,
   remarques=NA + " ; SUV 5 ou 7 places ; livraisons européennes à l'automne 2026 ; couples indicatifs")

MOT = Motorisations("Lucid", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Lucid": L}
MOTEURS = MOT.moteurs()
