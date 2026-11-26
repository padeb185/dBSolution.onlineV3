"""Aptera : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Aptera (tricycle électrique solaire biplace), Launch Edition : trois moteurs-roues Elaphe, 128 kW (171 hp), batterie 42 kWh,
autonomie visée 400 miles. Certificat EPA obtenu pour la Launch Edition 2026 ; assemblage des 40 premiers exemplaires prévu
fin 2026, livraisons visées début 2027. Couple indicatif.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique

FAMILLES = {"APTERA-EV": electrique()}
mg = SaisieMoteurs(FAMILLES, "Aptera", lambda fam: "Aptera")
L = []

mg(L, "Aptera", "Launch Edition", "1", "2026-12", None, [("Launch Edition AWD 174", "APTERA-EV", 300)], portes=2, places=2, reservoir=0, batterie=42,
   remarques="Tricycle électrique à panneaux solaires (jusqu'à 40 miles par jour) ; début de production prévu fin 2026, livraisons début 2027 ; "
             "couple indicatif ; données à vérifier")

MOT = Motorisations("Aptera", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Aptera": L}
MOTEURS = MOT.moteurs()
