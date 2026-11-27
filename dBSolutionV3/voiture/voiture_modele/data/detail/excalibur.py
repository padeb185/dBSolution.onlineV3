"""Excalibur : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Néo-classiques de Milwaukee inspirés de la Mercedes SSK (Brooks Stevens) : Series I à V (1965-1989). V8 Chevrolet repris de
chevrolet.py et avanti.py (mêmes familles et couples) ; 7.4 de 1975 ajouté. Puissances SAE converties en ch (× 1,014) ;
jusqu'en 1971 puissances brutes. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .avanti import FAMILLES as FAMILLES_AVANTI
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET

FAMILLES = {**{k: FAMILLES_CHEVROLET[k] for k in ("SBC-5.4", "SBC-5.7", "BBC-7.4")}, "SBC-5.0": FAMILLES_AVANTI["SBC-5.0"]}
mg = SaisieMoteurs(FAMILLES, "Chevrolet", lambda fam: "Chevrolet")
L = []
NA = "marché nord-américain ; données indicatives"

mg(L, "Series I", "Series I", "1", "1965-01", "1969-12", [("5.4 V8 304", "SBC-5.4", 488)], portes=2, places=2, reservoir=95,
   remarques="Roadster SSK (et Phaeton à partir de 1966), châssis Studebaker puis maison ; " + NA)
mg(L, "Series II", "Series II", "1", "1970-01", "1974-12", [("5.7 V8 304", "SBC-5.7", 515)], portes=2, places=4, reservoir=95, remarques="Roadster et Phaeton ; " + NA)
mg(L, "Series III", "Series III", "1", "1975-01", "1979-12", [("7.4 V8 218", "BBC-7.4", 481)], portes=2, places=4, reservoir=95, remarques="Roadster et Phaeton, V8 454 ; " + NA)
mg(L, "Series IV", "Series IV", "1", "1980-01", "1984-12", [("5.0 V8 157", "SBC-5.0", 325)], portes=2, places=4, reservoir=95, remarques="Phaeton et Roadster ; " + NA)
mg(L, "Series V", "Series V", "1", "1985-01", "1989-12", [("5.0 V8 157", "SBC-5.0", 325)], portes=2, places=4, reservoir=95, remarques="Phaeton, Roadster et limousine ; " + NA)

MOT = Motorisations("Excalibur", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Excalibur": L}
MOTEURS = MOT.moteurs()
