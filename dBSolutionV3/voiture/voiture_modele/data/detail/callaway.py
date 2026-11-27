"""Callaway : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Préparateur américain sur base Chevrolet Corvette : Twin Turbo (B2K, Corvette C4, 1987-1991), Sledgehammer (1988, exemplaire unique),
C12 (Corvette C5, 1998-2000) et C16 (Corvette C6, 2007-2010). V8 Chevrolet suralimentés ou réalésés par Callaway.
Puissances SAE converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET


def v8(t, l, rpm, nmrpm):
    return f(t, "ESS", l, "CHAINE", 8, rpm, nmrpm, "5W30", 5.5, 8000, a="V")


FAMILLES = {
    "LS1-5.7": FAMILLES_CHEVROLET["LS1-5.7"],
    "CALLAWAY-L98-5.7TT": v8("TURBO", 5.7, 4250, 2500),
    "CALLAWAY-SLEDGEHAMMER-5.7TT": v8("TURBO", 5.7, 6200, 5250),
    "CALLAWAY-LS3-6.2SC": v8("TURBO", 6.2, 6300, 4750),
}
mg = SaisieMoteurs(FAMILLES, "Callaway", lambda fam: "Chevrolet" if fam == "LS1-5.7" else "Callaway")
L = []
NA = "marché nord-américain ; données indicatives"

mg(L, "Twin Turbo", "B2K", "1", "1987-01", "1991-12", [("5.7 V8 TT 350", "CALLAWAY-L98-5.7TT", 630, {"fin": "1989-12"}), ("5.7 V8 TT 409", "CALLAWAY-L98-5.7TT", 780, {"debut": "1990-01"})],
   portes=2, places=2, reservoir=76, remarques="Corvette C4 biturbo, option RPO B2K proposée par Chevrolet ; " + NA)
mg(L, "Sledgehammer", "Sledgehammer", "1", "1988-01", "1988-12", [("5.7 V8 TT 911", "CALLAWAY-SLEDGEHAMMER-5.7TT", 1046)], portes=2, places=2, reservoir=76,
   remarques="Exemplaire unique sur Corvette C4, 409 km/h en 1988 ; " + NA)
mg(L, "C12", "C12", "1", "1998-01", "2000-12", [("5.7 V8 446", "LS1-5.7", 590)], portes=2, places=2, reservoir=72,
   remarques="Coupé et cabriolet sur Corvette C5, V8 LS1 préparé ; " + NA)
mg(L, "C16", "C16", "1", "2007-01", "2010-12", [("6.2 V8 Supercharged 625", "CALLAWAY-LS3-6.2SC", 786)], portes=2, places=2, reservoir=68,
   remarques="Coupé, cabriolet et Speedster sur Corvette C6, LS3 à compresseur ; " + NA)

MOT = Motorisations("Callaway", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Callaway": L}
MOTEURS = MOT.moteurs()
