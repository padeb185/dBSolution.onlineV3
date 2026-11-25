"""Auto Union : modèles, motorisations et moteurs liés.
Voitures de course Grand Prix (Type A à D, 1934-1939) et berlines d'après-guerre (1000, 1000 S, 1000 Universal, 1000 Sp, 1958-1965).
Les DKW, Horch et Wanderer restent dans leurs marques. Toutes les données sont indicatives (marque ancienne).
Moteurs deux-temps : distribution « aucune », huile « à choisir » (mélange). Compresseur classé « TURBO ».
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"

FAMILLES = {
    "AU-2T-1.0": f("ATM", E_, 0.98, "AUCUNE", 3, 4500, 2500, "CHOISIR", 0.0, 5000),
    "AU-V16-4.4C": f("TURBO", E_, 4.4, "NC", 16, 4500, 2700, "CHOISIR", 20.0, 1000, a="V"),
    "AU-V16-5.0C": f("TURBO", E_, 5.0, "NC", 16, 4800, 2700, "CHOISIR", 20.0, 1000, a="V"),
    "AU-V16-6.0C": f("TURBO", E_, 6.0, "NC", 16, 5000, 2500, "CHOISIR", 20.0, 1000, a="V"),
    "AU-V12-3.0C": f("TURBO", E_, 3.0, "NC", 12, 7000, 4000, "CHOISIR", 18.0, 1000, a="V"),
}

mg = SaisieMoteurs(FAMILLES, "Auto Union")
L = []
R = "Données indicatives (marque ancienne), à vérifier"
GP = "Voiture de course Grand Prix (moteur central), non homologuée route ; " + R

mg(L, "Type A", "Typ A", "1", "1934-01", "1934-12", [("Typ A 4.4 V16 Compresseur 295", "AU-V16-4.4C", 530)], portes=0, places=1, reservoir=200, remarques=GP)
mg(L, "Type B", "Typ B", "1", "1935-01", "1935-12", [("Typ B 5.0 V16 Compresseur 375", "AU-V16-5.0C", 660)], portes=0, places=1, reservoir=200, remarques=GP)
mg(L, "Type C", "Typ C", "1", "1936-01", "1937-12", [("Typ C 6.0 V16 Compresseur 520", "AU-V16-6.0C", 850)], portes=0, places=1, reservoir=200, remarques=GP)
mg(L, "Type D", "Typ D", "1", "1938-01", "1939-12", [("Typ D 3.0 V12 Compresseur 420", "AU-V12-3.0C", 550), ("Typ D 3.0 V12 Compresseur 485", "AU-V12-3.0C", 550, {"debut": "1939-01"})],
   portes=0, places=1, reservoir=200, remarques=GP + " ; réglementation 3 litres compresseur")
mg(L, "1000", "1000", "1", "1958-01", "1963-12", [("1000 44", "AU-2T-1.0", 83, {"fin": "1959-12"}), ("1000 S 50", "AU-2T-1.0", 86, {"debut": "1959-09"})],
   portes=2, places=5, reservoir=45, remarques="Berline et coupé 2 portes, trois cylindres deux-temps (ex-DKW 3=6) ; " + R)
mg(L, "1000 Universal", "1000", "U", "1959-01", "1962-12", [("Universal 44", "AU-2T-1.0", 83)], portes=3, places=5, reservoir=45, remarques="Break ; " + R)
mg(L, "1000 Sp", "1000 Sp", "1", "1958-01", "1965-12", [("1000 Sp 55", "AU-2T-1.0", 88)], portes=2, places=2, reservoir=45,
   remarques="Coupé (1958) et roadster (1961), carrosserie Baur ; " + R)

MOT = Motorisations("Auto Union", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Auto Union": L}
MOTEURS = MOT.moteurs()
