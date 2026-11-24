"""BYD : générations, motorisations (marché européen) et moteurs liés.
Électriques : Tang, Han, Atto 3 / Atto 3 Evo, Dolphin, Dolphin Surf, Seal, Seal U, Atto 2, Sealion 7.
Hybrides rechargeables « Super Hybrid DM-i » : Seal U DM-i, Atto 2 DM-i, Seal 6 DM-i, Sealion 5 DM-i, Dolphin G DM-i.
Modèles chinois non vendus en Europe (Qin, Yuan Pro, Song, Han DM…) et marque Denza non repris.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f

FAMILLES = {
    "BYD-EV": electrique(),
    "BYD-DMI-1.5": f("HYB_E", "ESS", 1.5, "CHAINE", 4, 6000, 4500, "0W20", 4.2, 15000),
    "BYD-DMI-1.5T": f("HYB_E", "ESS", 1.5, "CHAINE", 4, 5500, 2000, "0W20", 4.2, 15000),
}


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


def ph(kwh, reservoir, **kw):
    return {"reservoir": reservoir, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "BYD")
L = []
IND = "batteries et couples indicatifs"

# ---------------------------------------------------------------- électriques
mg(L, "Tang", "EV", "1", "2021-10", None, [("Tang AWD 517", "BYD-EV", 680, el(86))], places=7, reservoir=0,
   remarques="SUV 7 places électrique ; batterie de 108,8 kWh annoncée en 2026 (non détaillée)")
mg(L, "Han", "EV", "1", "2022-10", "2024-12", [("Han AWD 517", "BYD-EV", 700, el(85))], portes=4, reservoir=0,
   remarques="Berline électrique ; fin de commercialisation européenne indicative")
mg(L, "Atto 3", "EA1", "1", "2022-10", "2025-12", [("Atto 3 204", "BYD-EV", 310, el(60)), ("Atto 3 Active 204", "BYD-EV", 310, el(50, debut="2024-06"))],
   reservoir=0, remarques="SUV compact électrique (Yuan Plus en Chine)")
mg(L, "Atto 3", "EA1", "2", "2026-01", None, [("Atto 3 Evo 313", "BYD-EV", 380, el(75)), ("Atto 3 Evo AWD 449", "BYD-EV", 560, el(75))], reservoir=0,
   remarques="Atto 3 Evo (recharge jusqu'à 220 kW) ; " + IND)
mg(L, "Dolphin", "EA1", "D", "2023-06", None,
   [("Active 95", "BYD-EV", 180, el(45)), ("Boost 177", "BYD-EV", 290, el(45)), ("Comfort 204", "BYD-EV", 310, el(60)), ("Design 204", "BYD-EV", 310, el(60))],
   reservoir=0, remarques="Compacte électrique")
mg(L, "Dolphin Surf", "Seagull", "1", "2025-06", None,
   [("Active 88", "BYD-EV", 175, el(30)), ("Boost 88", "BYD-EV", 175, el(43)), ("Comfort 156", "BYD-EV", 220, el(43))], places=4, reservoir=0,
   remarques="Citadine électrique (Seagull en Chine) ; 5 places depuis 2026")
mg(L, "Seal", "EP3", "1", "2023-09", None, [("Design 313", "BYD-EV", 360, el(83)), ("Excellence AWD 530", "BYD-EV", 670, el(83))], portes=4, reservoir=0,
   remarques="Berline électrique")
mg(L, "Seal U", "EV", "1", "2024-03", None, [("Comfort 218", "BYD-EV", 330, el(72)), ("Design 218", "BYD-EV", 330, el(87))], reservoir=0,
   remarques="SUV familial électrique")
mg(L, "Atto 2", "EA1", "2", "2025-01", None, [("Atto 2 177", "BYD-EV", 290, el(45)), ("Comfort 204", "BYD-EV", 310, el(65, debut="2025-09"))], reservoir=0,
   remarques="SUV urbain électrique (Yuan Up en Chine)")
mg(L, "Sealion 7", "EP3", "S", "2025-01", None, [("Comfort 313", "BYD-EV", 380, el(83)), ("Design AWD 530", "BYD-EV", 690, el(83)),
                                               ("Excellence AWD 530", "BYD-EV", 690, el(91))], reservoir=0, remarques="SUV coupé électrique")

# ---------------------------------------------------------------- hybrides rechargeables DM-i
mg(L, "Seal U DM-i", "DM-i 5.0", "1", "2024-06", None,
   [("Boost 218", "BYD-DMI-1.5", 300, ph(18, 60)), ("Design AWD 324", "BYD-DMI-1.5T", 550, ph(27, 60))], reservoir=60,
   remarques="SUV hybride rechargeable ; " + IND)
mg(L, "Atto 2 DM-i", "DM-i 5.0", "1", "2026-01", None,
   [("Atto 2 DM-i 166", "BYD-DMI-1.5", 300, ph(8, 45)), ("Atto 2 DM-i 212", "BYD-DMI-1.5", 300, ph(18, 45))], reservoir=45,
   remarques="SUV urbain hybride rechargeable ; " + IND)
mg(L, "Seal 6 DM-i", "DM-i 5.0", "1", "2025-10", None,
   [("Seal 6 DM-i 184", "BYD-DMI-1.5", 300, ph(10, 65)), ("Seal 6 DM-i 212", "BYD-DMI-1.5", 300, ph(19, 65))], portes=4, reservoir=65,
   remarques="Berline et Touring hybrides rechargeables ; " + IND)
mg(L, "Sealion 5 DM-i", "DM-i 5.0", "1", "2026-01", None, [("Sealion 5 DM-i 212", "BYD-DMI-1.5", 300, ph(18, 60))], reservoir=60,
   remarques="SUV hybride rechargeable ; date et données indicatives")
mg(L, "Dolphin G DM-i", "DM-i 5.0", "1", "2026-09", None, [("Dolphin G DM-i 166", "BYD-DMI-1.5", 300, ph(8, 45))], reservoir=45,
   remarques="Citadine hybride rechargeable (présentée le 27 mai 2026) ; motorisation reprise de l'Atto 2 DM-i, indicative")

MOT = Motorisations("BYD", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"BYD": L}
MOTEURS = MOT.moteurs()
