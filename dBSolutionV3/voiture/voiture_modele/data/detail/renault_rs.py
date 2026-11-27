"""Renault RS (Renault Sport) : générations, phases, motorisations (marché européen) et moteurs liés.
Modèles Renault Sport : Spider (1996-1999), Clio RS (II, III, IV), Clio V6 (II), Twingo RS (II), Mégane RS (II, III, IV) et RS 01
(voiture de course). Moteurs repris de la table de renault_classiques.py (mêmes familles, codes et couples que les versions RS de
renault.py) ; V6 VR38 de la RS 01 ajouté. Les finitions « RS Line » (Arkana, Captur…) ne sont pas des modèles Renault Sport.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from . import renault_classiques as rc

NISSAN = {"VR38-3.8BT": f("TURBO", "ESS", 3.8, "CHAINE", 6, 6800, 5000, "0W40", 6.5, 5000, a="V")}
FAMILLES = {**rc.FAMILLES, **NISSAN}
mg = SaisieMoteurs(FAMILLES, "Renault", lambda fam: "Nissan" if fam in NISSAN else "Renault")
L = []


def t(cle, nom=None, *surcharges):
    """Variante reprise de la table de renault_classiques.py (même famille et couple) ; nom affiché facultatif."""
    v = rc.TABLE[cle]
    return (nom or cle, v[-3], v[-1], *surcharges)


mg(L, "Spider", "EF0", "1", "1996-03", "1999-12", [t("2.0 16v 150", "2.0 150")], portes=0, places=2, reservoir=50,
   remarques="Renault Sport Spider, roadster à châssis aluminium assemblé à Dieppe (pare-brise ou saute-vent)")

mg(L, "Clio RS", "Clio II", "1", "2000-01", "2004-03", [t("2.0 172")], portes=3, places=4, reservoir=50, remarques="Clio Renault Sport 172")
mg(L, "Clio RS", "Clio II", "2", "2004-04", "2006-06", [t("2.0 182")], portes=3, places=4, reservoir=50, remarques="Clio Renault Sport 182, dont Trophy")
mg(L, "Clio V6", "Clio II", "1", "2001-01", "2003-05", [t("V6 3.0 230")], portes=3, places=2, reservoir=60, remarques="V6 central arrière, assemblée par TWR")
mg(L, "Clio V6", "Clio II", "2", "2003-06", "2005-12", [t("V6 3.0 255")], portes=3, places=2, reservoir=60, remarques="Phase 2, assemblée à Dieppe")
mg(L, "Clio RS", "Clio III", "1", "2006-06", "2009-04", [t("2.0 197")], portes=3, places=4, reservoir=50, remarques="Clio Renault Sport 197")
mg(L, "Clio RS", "Clio III", "2", "2009-05", "2013-02", [t("2.0 203")], portes=3, places=4, reservoir=50, remarques="Clio Renault Sport 200, Cup, Gordini et Trophy")
mg(L, "Clio RS", "Clio IV", "1", "2013-03", "2016-04", [t("1.6 TCe 200"), t("Trophy 1.6 TCe 220", None, {"debut": "2015-03"})], portes=5, places=5, reservoir=45,
   remarques="5 portes, boîte EDC à double embrayage")
mg(L, "Clio RS", "Clio IV", "2", "2016-05", "2019-06", [t("1.6 TCe 200"), t("Trophy 1.6 TCe 220")], portes=5, places=5, reservoir=45, remarques="Dont RS 18")

mg(L, "Twingo RS", "Twingo II", "1", "2008-09", "2011-12", [t("1.6 133")], portes=3, places=4, reservoir=40, remarques="Twingo Renault Sport, Gordini RS (2009)")
mg(L, "Twingo RS", "Twingo II", "2", "2012-01", "2013-12", [t("1.6 133")], portes=3, places=4, reservoir=40, remarques="Phase 2")

mg(L, "Mégane RS", "Mégane II", "1", "2004-09", "2006-12", [t("2.0 T 225")], portes=3, places=4, reservoir=60, remarques="Mégane Renault Sport 3 et 5 portes")
mg(L, "Mégane RS", "Mégane II", "2", "2007-01", "2009-06", [t("R26 2.0 T 230", "2.0 T 230")], portes=3, places=4, reservoir=60,
   remarques="Dont R26 F1 Team et R26.R allégée (2008)")
mg(L, "Mégane RS", "Mégane III", "1", "2009-12", "2012-05", [t("2.0 T 250")], portes=3, places=4, reservoir=60, remarques="Coupé 3 portes")
mg(L, "Mégane RS", "Mégane III", "2", "2012-06", "2016-12", [t("2.0 T 265"), t("2.0 T 275", None, {"debut": "2014-06"})], portes=3, places=4, reservoir=60,
   remarques="RS 265, Trophy et Trophy-R (275)")
mg(L, "Mégane RS", "Mégane IV", "1", "2018-01", "2019-12", [t("1.8 TCe 280"), t("Trophy 1.8 TCe 300", None, {"debut": "2018-12"})], portes=5, places=5, reservoir=50,
   remarques="5 portes, quatre roues directrices 4Control")
mg(L, "Mégane RS", "Mégane IV", "2", "2020-01", "2023-12", [t("1.8 TCe 300"), t("Trophy 1.8 TCe 300", "Trophy 1.8 TCe 300")], portes=5, places=5, reservoir=50,
   remarques="RS 300, Trophy, Trophy-R et Ultime (dernière Renault Sport)")

mg(L, "RS 01", "RS 01", "1", "2014-01", "2017-12", [("3.8 V6 Biturbo 500", "VR38-3.8BT", 600)], portes=0, places=1, reservoir=65,
   remarques="Voiture de course (Renault Sport Trophy), non homologuée route ; V6 Nissan VR38")

MOT = Motorisations("Renault", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Renault RS": L}
MOTEURS = MOT.moteurs()
