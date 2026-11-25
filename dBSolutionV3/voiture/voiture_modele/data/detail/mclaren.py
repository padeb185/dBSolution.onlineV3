"""McLaren : générations, phases, motorisations (marché européen) et moteurs liés.
F1 (+ F1 LM), MP4-12C, 650S, 675LT, Sports Series (540C, 570S, 570GT, 600LT, 620R), P1, 720S, Senna, Speedtail, GT/GTS, Elva,
765LT, Sabre, Artura, 750S, Solus GT, W1 ; versions Spider dans des modèles séparés comme dans l'ancienne liste.
V8 McLaren (M838T, M840T) au motoriste « McLaren » ; V12 BMW de la F1 au motoriste « BMW M » ; V10 de la Solus GT au motoriste
« Judd ». « Speedtail LM » de l'ancienne liste non reprise (modèle non identifié).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
C = "CHAINE"

FAMILLES = {
    "BMW-S70/2-6.1": f("ATM", E_, 6.1, C, 12, 7400, 5600, "10W60", 12.0, 10000, a="V"),
    "M838T-3.8": f("TURBO", E_, 3.8, C, 8, 7000, 3000, "5W40", 8.5, 15000, a="V"),
    "M838TQ-3.8-HYB": f("HYB_TE", E_, 3.8, C, 8, 7500, 4000, "5W40", 8.5, 15000, a="V"),
    "M840T-4.0": f("TURBO", E_, 4.0, C, 8, 7500, 5500, "5W40", 8.5, 15000, a="V"),
    "M840T-4.0-HYB": f("HYB_TE", E_, 4.0, C, 8, 7500, 5500, "5W40", 8.5, 15000, a="V"),
    "MHP8-4.0-HYB": f("HYB_E", E_, 4.0, C, 8, 9000, 5000, "5W40", 9.0, 15000, a="V"),
    "M630-3.0-HYB": f("HYB_E", E_, 3.0, C, 6, 7500, 2250, "5W40", 7.0, 15000, a="V"),
    "JUDD-V10-5.2": f("ATM", E_, 5.2, "NC", 10, 9500, 8000, "10W60", 10.0, 5000, a="V"),
}
MOTORISTES = {"BMW-S70/2-6.1": "BMW M", "JUDD-V10-5.2": "Judd"}
mg = SaisieMoteurs(FAMILLES, "McLaren", lambda fam: MOTORISTES.get(fam, "McLaren"))
L = []

mg(L, "F1", "F1", "1", "1993-12", "1998-05", [("6.1 V12 627", "BMW-S70/2-6.1", 650)], portes=2, places=3, reservoir=90,
   remarques="Conduite centrale, 64 exemplaires route ; F1 GTR (course) et F1 GT non détaillées")
mg(L, "F1 LM", "F1", "1", "1995-10", "1996-12", [("LM 6.1 V12 680", "BMW-S70/2-6.1", 705)], portes=2, places=3, reservoir=90, remarques="5 exemplaires")
mg(L, "F1 GTR Road Version", "F1", "1", "1997-01", "1997-12", [("GTR 6.1 V12 627", "BMW-S70/2-6.1", 650)], portes=2, places=3, reservoir=90,
   remarques="Exemplaires de course convertis pour la route ; données indicatives")
mg(L, "MP4-12C", "P11", "1", "2011-06", "2014-04", [("3.8 V8 Biturbo 600", "M838T-3.8", 600, {"fin": "2012-09"}), ("3.8 V8 Biturbo 625", "M838T-3.8", 600, {"debut": "2012-10"})],
   portes=2, places=2, reservoir=72, remarques="Renommée 12C en 2012")
mg(L, "MP4-12C Spider", "P11", "1", "2012-12", "2014-04", [("3.8 V8 Biturbo 625", "M838T-3.8", 600)], portes=2, places=2, reservoir=72)
mg(L, "650S", "P11", "2", "2014-03", "2017-04", [("3.8 V8 Biturbo 650", "M838T-3.8", 678)], portes=2, places=2, reservoir=72)
mg(L, "650S Spider", "P11", "2", "2014-06", "2017-04", [("3.8 V8 Biturbo 650", "M838T-3.8", 678)], portes=2, places=2, reservoir=72)
mg(L, "675LT", "P11", "3", "2015-06", "2016-12", [("3.8 V8 Biturbo 675", "M838T-3.8", 700)], portes=2, places=2, reservoir=72, remarques="500 exemplaires")
mg(L, "675LT Spider", "P11", "3", "2016-01", "2017-06", [("3.8 V8 Biturbo 675", "M838T-3.8", 700)], portes=2, places=2, reservoir=72, remarques="500 exemplaires")
mg(L, "570S", "P13", "1", "2015-06", "2021-06",
   [("540C 3.8 V8 Biturbo 540", "M838T-3.8", 540), ("570S 3.8 V8 Biturbo 570", "M838T-3.8", 600), ("570GT 3.8 V8 Biturbo 570", "M838T-3.8", 600, {"debut": "2016-06"}),
    ("600LT 3.8 V8 Biturbo 600", "M838T-3.8", 620, {"debut": "2018-09"}), ("620R 3.8 V8 Biturbo 620", "M838T-3.8", 620, {"debut": "2020-06"})], portes=2, places=2,
   reservoir=72, remarques="Gamme Sports Series (coupés et Spider)")
mg(L, "P1", "P12", "1", "2013-10", "2015-12", [("3.8 V8 Biturbo Hybride 916", "M838TQ-3.8-HYB", 900, {"batterie": 5})], portes=2, places=2, reservoir=64,
   remarques="375 exemplaires ; P1 GTR (piste) non reprise")
mg(L, "720S", "P14", "1", "2017-05", "2023-06", [("4.0 V8 Biturbo 720", "M840T-4.0", 770)], portes=2, places=2, reservoir=72)
mg(L, "720S Spider", "P14", "1", "2019-03", "2023-06", [("4.0 V8 Biturbo 720", "M840T-4.0", 770)], portes=2, places=2, reservoir=72)
mg(L, "Senna", "P15", "1", "2018-10", "2019-12", [("4.0 V8 Biturbo 800", "M840T-4.0", 800)], portes=2, places=2, reservoir=72,
   remarques="500 exemplaires ; Senna GTR (piste) non reprise")
mg(L, "Speedtail", "BP23", "1", "2020-02", "2021-12", [("4.0 V8 Biturbo Hybride 1070", "M840T-4.0-HYB", 1150, {"batterie": 2})], portes=2, places=3, reservoir=72,
   remarques="Conduite centrale, 106 exemplaires")
mg(L, "GT", "P16", "1", "2019-09", "2023-06", [("4.0 V8 Biturbo 620", "M840T-4.0", 630)], portes=2, places=2, reservoir=72, remarques="Grand tourisme")
mg(L, "GT", "P16", "2", "2023-07", None, [("GTS 4.0 V8 Biturbo 635", "M840T-4.0", 630)], portes=2, places=2, reservoir=72,
   remarques="McLaren GTS ; fin de production annoncée pour 2027 (date indicative)")
mg(L, "Elva", "P17", "1", "2020-12", "2021-12", [("4.0 V8 Biturbo 815", "M840T-4.0", 800)], portes=0, places=2, reservoir=72, remarques="Roadster sans pare-brise, 149 exemplaires")
mg(L, "765LT", "P14", "2", "2020-09", "2022-12", [("4.0 V8 Biturbo 765", "M840T-4.0", 800)], portes=2, places=2, reservoir=72, remarques="765 exemplaires")
mg(L, "765LT Spider", "P14", "2", "2021-06", "2022-12", [("4.0 V8 Biturbo 765", "M840T-4.0", 800)], portes=2, places=2, reservoir=72, remarques="765 exemplaires")
mg(L, "McLaren Sabre", "Sabre", "1", "2021-01", "2021-12", [("4.0 V8 Biturbo 835", "M840T-4.0", 800)], portes=2, places=2, reservoir=72,
   remarques="15 exemplaires pour les États-Unis (MSO) ; données indicatives")
mg(L, "Artura", "P16 Artura", "1", "2022-07", "2024-12", [("3.0 V6 Biturbo Hybride 680", "M630-3.0-HYB", 720, {"batterie": 7})], portes=2, places=2, reservoir=66,
   remarques="Hybride rechargeable ; fin de production annoncée pour 2028")
mg(L, "Artura", "P16 Artura", "2", "2025-01", None, [("3.0 V6 Biturbo Hybride 700", "M630-3.0-HYB", 720, {"batterie": 7})], portes=2, places=2, reservoir=66,
   remarques="Mise à jour 700 ch ; Artura Spider (2024) ; fin de production annoncée pour 2028")
mg(L, "750S", "P14", "3", "2023-06", None, [("4.0 V8 Biturbo 750", "M840T-4.0", 800)], portes=2, places=2, reservoir=72,
   remarques="Coupé et Spider ; fin de production annoncée pour 2027")
mg(L, "McLaren Solus", "Solus GT", "1", "2023-10", "2024-12", [("5.2 V10 840", "JUDD-V10-5.2", 650)], portes=0, places=1, reservoir=60,
   remarques="Solus GT, voiture de piste non homologuée, 25 exemplaires")
mg(L, "W1", "P18", "1", "2025-03", None, [("4.0 V8 Biturbo Hybride 1275", "MHP8-4.0-HYB", 1340, {"batterie": 1})], portes=2, places=2, reservoir=72,
   remarques="Hypercar hybride (V8 de 928 ch et module électrique de 347 ch), 399 exemplaires ; date indicative")

MOT = Motorisations("McLaren", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"McLaren": L}
MOTEURS = MOT.moteurs()
