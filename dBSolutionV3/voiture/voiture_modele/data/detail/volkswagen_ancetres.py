"""Volkswagen (ancêtres et modèles anciens) : générations, phases, motorisations (marché européen) et moteurs liés.
KdF-Wagen (Type 60, 1938-1944), Kübelwagen (Type 82) et Schwimmwagen (Type 166) ; puis Type 3 (1500 / 1600), Type 4 (411 / 412),
K 70, Type 181, Iltis, Caddy (I) et LT (I) ; modèles absents de volkswagen.py et volkswagen_classiques.py.
Flat-4 refroidis par air et EA827 repris de volkswagen_classiques.py (mêmes familles, codes et couples) via sa table ;
flat-4 1.0 d'origine, quatre cylindres NSU du K 70 et diesels du LT ajoutés. Puissances en ch DIN.
Données d'avant 1970 indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from . import volkswagen_classiques as vwc

E_, D = "ESS", "DSL"
NOUVEAUX = {
    "BOXER-1.0": f("ATM", E_, 1.0, "NC", 4, 3000, 2000, "20W50", 2.5, 5000, a="PLAT"),
    "K70-1.6": f("ATM", E_, 1.6, "CHAINE", 4, 5200, 3500, "15W40", 4.0, 7500),
    "K70-1.8": f("ATM", E_, 1.8, "CHAINE", 4, 5300, 3500, "15W40", 4.0, 7500),
    "EA827-1.7": f("ATM", E_, 1.7, "COURROIE", 4, 5000, 3000, "15W40", 3.5, 7500),
    "VW-D24-2.4D": f("ATM", D, 2.4, "COURROIE", 6, 4300, 2500, "15W40", 6.5, 7500),
    "VW-D24-2.4TD": f("TURBO", D, 2.4, "COURROIE", 6, 4000, 2200, "15W40", 6.5, 7500),
}
FAMILLES = {**vwc.FAMILLES, **NOUVEAUX}
mg = SaisieMoteurs(FAMILLES, "Volkswagen", lambda fam: "Volkswagen")
L = []
IND = "données indicatives (modèle ancien), à vérifier"


def t(cle, nom=None, *surcharges):
    """Variante reprise de la table de volkswagen_classiques.py (même famille et couple) ; nom affiché facultatif."""
    v = vwc.TABLE[cle]
    return (nom or cle, v[-3], v[-1], *surcharges)


# ---------------------------------------------------------------- origines et véhicules militaires
mg(L, "KdF-Wagen", "Type 60", "1", "1938-05", "1944-12", [("1.0 24", "BOXER-1.0", 64)], portes=2, places=4, reservoir=40,
   remarques="« Voiture du peuple » de Ferdinand Porsche (prototypes VW 30 / VW 38), ancêtre de la Coccinelle ; quelques centaines d'exemplaires civils ; " + IND)
mg(L, "Kübelwagen", "Type 82", "1", "1940-03", "1945-12", [("1.0 24", "BOXER-1.0", 64, {"fin": "1943-02"}), t("1.1 25", None, {"debut": "1943-03"})],
   portes=4, places=4, reservoir=40, remarques="Véhicule militaire léger sur base KdF-Wagen ; " + IND)
mg(L, "Schwimmwagen", "Type 166", "1", "1942-01", "1944-12", [t("1.1 25")], portes=0, places=4, reservoir=50,
   remarques="Amphibie 4x4, véhicule le plus produit de son type (environ 15 000) ; " + IND)

# ---------------------------------------------------------------- années 1960-1970
mg(L, "Type 3", "Type 3", "1", "1961-09", "1973-07", [t("1.5 45", "1500 1.5 45"), t("1.5 54", "1500 S 1.5 54", {"debut": "1963-08", "fin": "1965-07"}),
                                                    t("1.6 54", "1600 1.6 54", {"debut": "1965-08"})], portes=2, places=4, reservoir=40,
   remarques="1500 / 1600 Notchback, Variant et Fastback (TL), moteur plat sous plancher ; " + IND)
mg(L, "Type 4", "411 / 412", "1", "1968-08", "1974-07", [("411 1.7 68", "TYPE4-1.7", 116), ("411 E 1.7 80", "TYPE4-1.7", 133, {"debut": "1969-08"}),
                                                       ("412 1.8 75", "TYPE4-1.8", 135, {"debut": "1973-08"})], portes=4, places=5, reservoir=50,
   remarques="Première VW quatre portes et monocoque (411, puis 412), berline et Variant ; " + IND)
mg(L, "K 70", "K 70", "1", "1970-09", "1975-02", [("1.6 75", "K70-1.6", 120), ("1.8 90", "K70-1.8", 147, {"debut": "1971-01"}), ("S 1.8 100", "K70-1.8", 152, {"debut": "1973-01"})],
   portes=4, places=5, reservoir=53, remarques="Première VW à traction avant et moteur à eau, conçue par NSU ; " + IND)
mg(L, "Type 181", "181", "1", "1969-01", "1983-12", [t("1.5 44", None, {"fin": "1970-07"}), t("1.6 44", None, {"debut": "1970-08"})], portes=4, places=4, reservoir=40,
   remarques="« Kurierwagen » / Thing / Trekker, véhicule de liaison découvrable ; " + IND)
mg(L, "Iltis", "183", "1", "1978-01", "1988-12", [("1.7 75", "EA827-1.7", 132), t("1.6 D 54", None, {"debut": "1984-01"})], portes=4, places=4, reservoir=83,
   remarques="Tout-terrain 4x4 de la Bundeswehr (Audi), vainqueur du Paris-Dakar 1980 ; " + IND)
mg(L, "Caddy", "14", "1", "1979-01", "1992-12", [t("1.5 70"), t("1.6 75"), t("1.6 D 54")], portes=2, places=2, reservoir=55,
   remarques="Pick-up dérivé de la Golf I (assemblé en Yougoslavie pour l'Europe à partir de 1982)")
mg(L, "LT", "LT1", "1", "1975-04", "1996-04", [("2.4 D 75", "VW-D24-2.4D", 140, {"debut": "1979-01"}), ("2.4 TD 102", "VW-D24-2.4TD", 192, {"debut": "1988-01"})],
   portes=4, places=3, reservoir=75, remarques="Utilitaire lourd (fourgon, plateau, châssis), six cylindres diesel ; versions essence non reprises ; " + IND)

MOT = Motorisations("Volkswagen", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Volkswagen": L}
MOTEURS = MOT.moteurs()
