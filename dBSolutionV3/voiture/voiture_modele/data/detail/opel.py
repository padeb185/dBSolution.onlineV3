"""Opel et Opel OPC : générations, phases, motorisations (marché européen) et moteurs liés.
Opel : 1.2 Liter, Olympia, Kadett, Kapitän, Rekord, Commodore, Ascona, Manta, GT, Senator, Monza, Omega, Calibra, Vectra,
Insignia, Corsa, Tigra, Astra, Zafira, Meriva, Agila, Adam, Karl, Cascada, Speedster, Frontera, Antara, Mokka, Crossland,
Grandland, Ampera, Ampera-e. Opel OPC : Astra, Corsa, Vectra, Insignia, Meriva, Zafira OPC et modèles GSe / GSE.
Moteurs PSA repris de peugeot.py / citroen.py (mêmes codes et couples, puissances PSA), moteurs GM Daewoo / Chevrolet
repris de chevrolet.py, Fiat 1.9 de cadillac.py, Isuzu d'isuzu.py ; moteurs Opel ajoutés. Données anciennes indicatives.
Utilitaires (Combo, Vivaro, Movano, Zafira Life) non repris.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from . import citroen, peugeot
from .cadillac import FAMILLES as FAMILLES_CADILLAC
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET
from .isuzu import FAMILLES as FAMILLES_ISUZU
from .nsu import FAMILLES as FAMILLES_NSU

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

OPEL = {
    # avant-guerre et OHV / CIH
    "OPEL-SV-1.2": f("ATM", E_, 1.2, "NC", 4, 3200, 2000, "SAE30", 3.0, 3000),
    "OPEL-6-2.5": f("ATM", E_, 2.5, C, 6, 3600, 2000, "20W50", 4.5, 3000),
    "OHV-1.0": f("ATM", E_, 1.0, C, 4, 5400, 3000, "15W40", 2.75, 7500),
    "OHV-1.2": f("ATM", E_, 1.2, C, 4, 5600, 3400, "15W40", 2.75, 7500),
    "CIH-1.5": f("ATM", E_, 1.5, C, 4, 5200, 3000, "15W40", 3.8, 10000),
    "CIH-1.7": f("ATM", E_, 1.7, C, 4, 5200, 3000, "15W40", 3.8, 10000),
    "CIH-1.9": f("ATM", E_, 1.9, C, 4, 5400, 3000, "15W40", 3.8, 10000),
    "CIH-2.0": f("ATM", E_, 2.0, C, 4, 5200, 3400, "15W40", 3.8, 10000),
    "CIH-2.4": f("ATM", E_, 2.4, C, 4, 4800, 2600, "15W40", 4.5, 10000),
    "CIH6-2.5": f("ATM", E_, 2.5, C, 6, 5600, 4000, "15W40", 5.5, 10000),
    "CIH6-2.8": f("ATM", E_, 2.8, C, 6, 5200, 3400, "15W40", 5.5, 10000),
    "CIH6-3.0": f("ATM", E_, 3.0, C, 6, 5800, 4400, "15W40", 5.5, 10000),
    # Family 0 / 1 / 2
    "FAM0-1.0": f("ATM", E_, 1.0, C, 3, 5600, 3800, "10W40", 3.0, 15000),
    "FAM0-1.2": f("ATM", E_, 1.2, C, 4, 5600, 4000, "5W30", 3.5, 15000),
    "FAM0-1.4": f("ATM", E_, 1.4, C, 4, 6000, 4000, "5W30", 3.5, 15000),
    "FAM1-1.2": f("ATM", E_, 1.2, B, 4, 5600, 3000, "10W40", 3.0, 15000),
    "FAM1-1.4": f("ATM", E_, 1.4, B, 4, 5600, 3800, "10W40", 3.5, 15000),
    "FAM1-1.6": f("ATM", E_, 1.6, B, 4, 6000, 3800, "10W40", 3.5, 15000),
    "FAM2-1.6": f("ATM", E_, 1.6, B, 4, 5200, 2600, "10W40", 4.0, 15000),
    "FAM2-1.3": f("ATM", E_, 1.3, B, 4, 5800, 3800, "10W40", 3.5, 15000),
    "FAM2-1.8-16V": f("ATM", E_, 1.8, B, 4, 5600, 3800, "10W40", 4.25, 15000),
    "FAM2-1.8": f("ATM", E_, 1.8, B, 4, 5600, 3800, "10W40", 4.25, 15000),
    "FAM2-2.0": f("ATM", E_, 2.0, B, 4, 5400, 3000, "10W40", 4.25, 15000),
    "FAM2-2.0-16V": f("ATM", E_, 2.0, B, 4, 6000, 4800, "10W40", 4.25, 15000),
    "FAM2-2.2": f("ATM", E_, 2.2, C, 4, 5600, 4000, "5W30", 5.0, 15000),
    "FAM2-2.0T": f("TURBO", E_, 2.0, B, 4, 5600, 2400, "5W40", 4.25, 15000),
    "FAM1-1.6T": f("TURBO", E_, 1.6, B, 4, 5500, 2200, "5W40", 4.5, 15000),
    "A16XHT-1.6T": f("TURBO", E_, 1.6, C, 4, 5500, 1650, "5W30", 4.5, 30000),
    "A20NHT-2.0T": f("TURBO", E_, 2.0, C, 4, 5300, 2500, "5W30", 5.0, 30000),
    "B10XFT-1.0T": f("TURBO", E_, 1.0, C, 3, 5000, 1800, "0W20", 4.0, 30000),
    "B14XFT-1.4T": f("TURBO", E_, 1.4, C, 4, 5600, 2000, "5W30", 4.0, 30000),
    "D12XHT-1.2T": f("TURBO", E_, 1.2, C, 3, 5500, 2000, "0W20", 4.0, 30000),
    "B15XFT-1.5T": f("TURBO", E_, 1.5, C, 4, 5600, 2000, "0W20", 4.5, 30000),
    # V6
    "X25XE-2.5V6": f("ATM", E_, 2.5, B, 6, 6000, 3200, "10W40", 5.0, 15000, a="V"),
    "Y26SE-2.6V6": f("ATM", E_, 2.6, B, 6, 6000, 3600, "10W40", 5.0, 15000, a="V"),
    "X30XE-3.0V6": f("ATM", E_, 3.0, B, 6, 6200, 3600, "10W40", 5.0, 15000, a="V"),
    "Y32SE-3.2V6": f("ATM", E_, 3.2, B, 6, 6200, 4000, "5W30", 5.0, 15000, a="V"),
    "Z28NET-2.8V6T": f("TURBO", E_, 2.8, C, 6, 5500, 1800, "5W30", 6.0, 15000, a="V"),
    # diesel
    "OPEL-1.6D": f("ATM", D, 1.6, B, 4, 4600, 2400, "15W40", 4.5, 10000),
    "OPEL-1.7D": f("ATM", D, 1.7, B, 4, 4600, 2400, "15W40", 4.5, 10000),
    "OPEL-2.3TD": f("TURBO", D, 2.3, C, 4, 4200, 2200, "15W40", 5.5, 10000),
    "ISUZU-1.5TD": f("TURBO", D, 1.5, B, 3, 4400, 2600, "10W40", 3.5, 10000),
    "ISUZU-1.7TD": f("TURBO", D, 1.7, B, 4, 4400, 2400, "10W40", 5.0, 15000),
    "ISUZU-1.7CDTI": f("TURBO", D, 1.7, B, 4, 4000, 2300, "5W30", 5.0, 30000),
    "ECOTEC-2.0DTI": f("TURBO", D, 2.0, C, 4, 4300, 1800, "5W30", 5.5, 15000),
    "ECOTEC-2.2DTI": f("TURBO", D, 2.2, C, 4, 4000, 1600, "5W30", 5.5, 15000),
    "FIAT-1.3CDTI": f("TURBO", D, 1.3, C, 4, 4000, 1750, "5W30", 3.2, 30000),
    "A20DTH-2.0CDTI": f("TURBO", D, 2.0, C, 4, 4000, 1750, "5W30", 5.4, 30000),
    "B16DTH-1.6CDTI": f("TURBO", D, 1.6, C, 4, 3500, 2000, "5W30", 4.5, 30000),
    "D15DT-1.5D": f("TURBO", D, 1.5, B, 3, 3500, 1750, "0W20", 4.5, 30000),
}
SUZUKI = {"SUZUKI-K10": f("ATM", E_, 1.0, C, 3, 6000, 3800, "5W30", 3.0, 15000),
          "SUZUKI-K12": f("ATM", E_, 1.2, C, 4, 6000, 4800, "5W30", 3.5, 15000)}
PSA_FAM = {k: citroen.FAMILLES[k] for k in ("EB2F", "EB2FA", "EB2ADT", "EB2DT", "EB2DTS", "EB2ADTS", "EB2-MHEV", "EP6-PHEV", "DV5R", "DV6F",
                                            "E-CMP", "STLA-M", "STLA-SMART-EV", "DW10F", "EP6FADTXD")}
GM = {**{k: FAMILLES_CHEVROLET[k] for k in ("ECOTEC-1.4T", "ECOTEC-1.6", "ECOTEC-1.8", "VCDI-1.7", "VCDI-2.0", "VCDI-2.2", "VOLTEC-1.4", "GM-EV-BOLT",
                                            "B10D-1.0", "GM-2.4")},
      "GM-V6-3.2": FAMILLES_CADILLAC["GM-V6-3.2"]}
FIAT = {"FIAT-1.9TID": FAMILLES_CADILLAC["FIAT-1.9TID"]}
ISUZU = {k: FAMILLES_ISUZU[k] for k in ("6VD1-3.2", "4JB1-2.8TD")}
OPEL_NSU = {"OPEL-1.5": FAMILLES_NSU["OPEL-1.5"]}
FAMILLES = {**OPEL, **SUZUKI, **PSA_FAM, **GM, **FIAT, **ISUZU, **OPEL_NSU}


def motoriste(fam):
    if fam in PSA_FAM:
        return "Peugeot"
    if fam in GM:
        return "Chevrolet"
    if fam in FIAT or fam == "FIAT-1.3CDTI":
        return "Fiat"
    if fam in ISUZU or fam.startswith("ISUZU-"):
        return "Isuzu"
    if fam in SUZUKI:
        return "Suzuki"
    return "Opel"


PSA_TABLE = {**citroen.TABLE, **peugeot.TABLE}


def psa(nom, cle, *surcharges):
    """Variante à moteur PSA : famille et couple lus dans la table Peugeot / Citroën (codes partagés)."""
    fam, ch, nm = PSA_TABLE[cle][-3:]
    assert ch == int(nom.split()[-1]), (nom, cle)
    return (nom, fam, nm, *surcharges)


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Opel", motoriste)
L, OPC = [], []
IND = "données indicatives"

# ---------------------------------------------------------------- avant-guerre et années 1950
mg(L, "1.2 Liter", "1.2 Liter", "1", "1931-01", "1935-12", [("1.2 23", "OPEL-SV-1.2", 60)], portes=2, places=4, reservoir=25, remarques=IND)
mg(L, "Olympia", "Olympia", "1", "1935-02", "1953-12", [("1.3 24", "OPEL-1.5", 65, {"fin": "1937-12"}), ("1.5 37", "OPEL-1.5", 98, {"debut": "1938-01"})],
   portes=2, places=4, reservoir=30, remarques="Première voiture allemande de série à caisse autoporteuse ; production interrompue pendant la guerre ; " + IND)
mg(L, "Kadett", "Kadett (1936)", "1", "1936-12", "1940-05", [("1.1 23", "OPEL-SV-1.2", 60)], portes=2, places=4, reservoir=25, remarques=IND)
mg(L, "Kapitän", "Kapitän", "1", "1938-11", "1970-12", [("2.5 55", "OPEL-6-2.5", 150, {"fin": "1958-12"}), ("2.6 90", "CIH6-2.8", 186, {"debut": "1959-01"})],
   portes=4, places=6, reservoir=55, remarques="Plusieurs générations (dont Kapitän P2, A et B) ; " + IND)
mg(L, "Rekord", "Olympia Rekord", "1", "1953-03", "1957-07", [("1.5 40", "OPEL-1.5", 98)], portes=2, places=5, reservoir=40, remarques=IND)
mg(L, "Rekord", "Rekord P", "1", "1957-08", "1963-02", [("1.5 45", "OPEL-1.5", 101), ("1.7 55", "CIH-1.7", 120, {"debut": "1960-08"})], portes=2, places=5, reservoir=45,
   remarques="Rekord P1 et P2 ; " + IND)

# ---------------------------------------------------------------- Kadett
mg(L, "Kadett", "Kadett A", "1", "1962-08", "1965-07", [("1.0 40", "OHV-1.0", 68), ("1.0 S 48", "OHV-1.0", 73)], portes=2, places=4, reservoir=30, remarques=IND)
mg(L, "Kadett", "Kadett B", "1", "1965-08", "1973-07", [("1.1 45", "OHV-1.2", 78), ("1.1 S 55", "OHV-1.2", 88), ("1.9 90", "CIH-1.9", 147, {"debut": "1967-01"})],
   portes=2, places=4, reservoir=38, remarques="Berline, coupé (Rallye) et break Caravan ; " + IND)
mg(L, "Kadett", "Kadett C", "1", "1973-08", "1979-07", [("1.0 40", "OHV-1.0", 68), ("1.2 52", "OHV-1.2", 85), ("1.2 S 60", "OHV-1.2", 88), ("GT/E 1.9 105", "CIH-1.9", 155, {"debut": "1975-08", "fin": "1977-07"}),
                                                         ("GT/E 2.0 115", "CIH-2.0", 162, {"debut": "1977-08"})],
   portes=2, places=4, reservoir=45, remarques="Dont Kadett City et Aero ; " + IND)
mg(L, "Kadett", "Kadett D", "1", "1979-08", "1984-08", [("1.2 53", "OHV-1.2", 86), ("1.3 75", "FAM2-1.3", 102), ("GTE 1.8 115", "FAM2-1.8", 150, {"debut": "1983-01"}),
                                                         ("1.6 D 54", "OPEL-1.6D", 96, {"debut": "1982-01"})],
   portes=5, places=5, reservoir=42, remarques="Première Kadett à traction ; " + IND)
mg(L, "Kadett", "Kadett E", "1", "1984-09", "1991-08",
   [("1.2 55", "OHV-1.2", 88), ("1.3 75", "FAM2-1.3", 102), ("1.6 75", "FAM2-1.6", 125), ("GSi 2.0 115", "FAM2-2.0", 170, {"debut": "1986-08"}),
    ("GSi 16V 2.0 150", "FAM2-2.0-16V", 196, {"debut": "1988-03"}), ("1.7 D 57", "OPEL-1.7D", 105, {"debut": "1988-08"})],
   portes=5, places=5, reservoir=52, remarques="Voiture européenne de l'année 1985 ; berline, break, cabriolet ; " + IND)

# ---------------------------------------------------------------- Rekord / Commodore / Senator / Omega
mg(L, "Rekord", "Rekord A-B", "1", "1963-03", "1966-07", [("1.5 55", "CIH-1.5", 108), ("1.7 60", "CIH-1.7", 125)], portes=2, places=5, reservoir=45, remarques=IND)
mg(L, "Rekord", "Rekord C", "1", "1966-08", "1971-12", [("1.7 75", "CIH-1.7", 128), ("1.9 90", "CIH-1.9", 147)], portes=4, places=5, reservoir=55, remarques=IND)
mg(L, "Rekord", "Rekord D", "1", "1972-01", "1977-08", [("1.7 66", "CIH-1.7", 120), ("1.9 75", "CIH-1.9", 141), ("2.0 100", "CIH-2.0", 158, {"debut": "1975-01"}),
                                                         ("2100 D 60", "OPEL-2.3TD", 120, {"remarques": "Diesel 2.1 atmosphérique rattaché à la famille 2.3"})],
   portes=4, places=5, reservoir=65, remarques=IND)
mg(L, "Rekord", "Rekord E", "1", "1977-08", "1986-08", [("2.0 100", "CIH-2.0", 158), ("2.0 E 110", "CIH-2.0", 162, {"debut": "1982-09"}), ("1.8 90", "FAM2-1.8", 145, {"debut": "1982-09"}),
                                                         ("2.3 D 65", "OPEL-2.3TD", 130), ("2.3 TD 86", "OPEL-2.3TD", 177, {"debut": "1984-01"})],
   portes=4, places=5, reservoir=65, remarques="Berline et break Caravan ; " + IND)
mg(L, "Commodore", "Commodore", "1", "1967-02", "1982-08", [("2.5 115", "CIH6-2.5", 172), ("GS/E 2.8 160", "CIH6-2.8", 230, {"debut": "1970-01"})], portes=2, places=5, reservoir=70,
   remarques="Commodore A, B et C ; " + IND)
mg(L, "Senator", "Senator A", "1", "1978-03", "1987-08", [("2.5 136", "CIH6-2.5", 205), ("2.8 140", "CIH6-2.8", 220, {"fin": "1982-08"}), ("3.0 E 180", "CIH6-3.0", 248)],
   portes=4, places=5, reservoir=75, remarques=IND)
mg(L, "Monza", "Monza", "1", "1978-05", "1986-08", [("2.5 136", "CIH6-2.5", 205), ("3.0 E 180", "CIH6-3.0", 248)], portes=3, places=4, reservoir=75, remarques="Coupé du Senator ; " + IND)
mg(L, "Senator", "Senator B", "1", "1987-09", "1993-12", [("2.6 150", "CIH6-2.5", 220), ("3.0 177", "CIH6-3.0", 240), ("3.0 24V 204", "CIH6-3.0", 270, {"debut": "1989-09"})],
   portes=4, places=5, reservoir=75, remarques=IND)
mg(L, "Omega", "Omega A", "1", "1986-09", "1993-12",
   [("1.8 90", "FAM2-1.8", 145), ("2.0 115", "FAM2-2.0", 170), ("2.4 125", "CIH-2.4", 195, {"debut": "1988-09"}), ("3000 3.0 177", "CIH6-3.0", 240), ("3000 24V 3.0 204", "CIH6-3.0", 270, {"debut": "1989-09"}),
    ("2.3 TD 100", "OPEL-2.3TD", 215)], portes=4, places=5, reservoir=75, remarques="Voiture européenne de l'année 1987 ; berline et break Caravan ; " + IND)
mg(L, "Omega", "Omega B", "1", "1994-03", "2003-06",
   [("2.0 136", "FAM2-2.0", 185, {"fin": "1999-08"}), ("2.2 144", "FAM2-2.2", 203, {"debut": "1999-09"}), ("2.5 V6 170", "X25XE-2.5V6", 227, {"fin": "2000-12"}),
    ("2.6 V6 180", "Y26SE-2.6V6", 230, {"debut": "2001-01"}), ("3.0 V6 211", "X30XE-3.0V6", 270, {"fin": "2000-12"}), ("3.2 V6 218", "Y32SE-3.2V6", 290, {"debut": "2001-01"}),
    ("2.0 DTI 100", "ECOTEC-2.0DTI", 230, {"debut": "1998-01"}), ("2.2 DTI 120", "ECOTEC-2.2DTI", 280, {"debut": "2001-01"})],
   portes=4, places=5, reservoir=75, remarques="Berline et break ; restylage 1999 ; " + IND)

# ---------------------------------------------------------------- Ascona / Manta / GT / Calibra
mg(L, "GT", "GT", "1", "1968-09", "1973-08", [("1.1 60", "OHV-1.2", 88), ("1.9 90", "CIH-1.9", 147)], portes=2, places=2, reservoir=50, remarques=IND)
mg(L, "Ascona", "Ascona A", "1", "1970-09", "1975-07", [("1.6 68", "CIH-1.5", 115), ("1.9 90", "CIH-1.9", 147)], portes=4, places=5, reservoir=50, remarques="1.6 rattaché à la famille CIH 1.5 ; " + IND)
mg(L, "Ascona", "Ascona B", "1", "1975-08", "1981-08", [("1.6 75", "CIH-1.5", 120), ("1.9 90", "CIH-1.9", 147), ("2.0 E 110", "CIH-2.0", 162, {"debut": "1979-01"}), ("400 2.4 144", "CIH-2.4", 210, {"debut": "1979-01"})],
   portes=4, places=5, reservoir=50, remarques="Dont Ascona 400 (homologation rallye) ; " + IND)
mg(L, "Ascona", "Ascona C", "1", "1981-09", "1988-08", [("1.3 75", "FAM2-1.3", 102), ("1.6 75", "FAM2-1.6", 125), ("1.8 E 115", "FAM2-1.8", 150), ("2.0 115", "FAM2-2.0", 170, {"debut": "1986-08"}),
                                                          ("1.6 D 54", "OPEL-1.6D", 96)], portes=4, places=5, reservoir=61, remarques="Traction ; " + IND)
mg(L, "Manta", "Manta A", "1", "1970-09", "1975-07", [("1.6 68", "CIH-1.5", 115), ("1.9 90", "CIH-1.9", 147), ("GT/E 1.9 105", "CIH-1.9", 155, {"debut": "1974-01"})], portes=2, places=4, reservoir=50,
   remarques=IND)
mg(L, "Manta", "Manta B", "1", "1975-08", "1988-08", [("1.6 75", "CIH-1.5", 120), ("1.9 90", "CIH-1.9", 147, {"fin": "1979-12"}), ("2.0 E 110", "CIH-2.0", 162), ("GSi 2.0 110", "CIH-2.0", 162, {"debut": "1984-01"}),
                                                        ("1.8 90", "FAM2-1.8", 145, {"debut": "1982-09"}), ("400 2.4 144", "CIH-2.4", 210, {"debut": "1981-06", "fin": "1984-12"})],
   portes=2, places=4, reservoir=50, remarques="Coupé et CC (3 portes) ; " + IND)
mg(L, "Calibra", "Calibra", "1", "1989-09", "1997-06",
   [("2.0 115", "FAM2-2.0", 170, {"fin": "1994-12"}), ("2.0 16V 150", "FAM2-2.0-16V", 196, {"fin": "1994-12"}), ("2.0 16V 136", "FAM2-2.0", 185, {"debut": "1995-01"}),
    ("Turbo 4x4 2.0 204", "FAM2-2.0T", 280, {"debut": "1992-04"}), ("2.5 V6 170", "X25XE-2.5V6", 227, {"debut": "1993-09"})], portes=2, places=4, reservoir=65, remarques=IND)

# ---------------------------------------------------------------- Vectra / Insignia
mg(L, "Vectra", "Vectra A", "1", "1988-09", "1995-09",
   [("1.6 75", "FAM2-1.6", 125), ("1.8 90", "FAM2-1.8", 145), ("2.0 115", "FAM2-2.0", 170), ("2000 16V 2.0 150", "FAM2-2.0-16V", 196), ("Turbo 4x4 2.0 204", "FAM2-2.0T", 280, {"debut": "1992-04"}),
    ("2.5 V6 170", "X25XE-2.5V6", 227, {"debut": "1993-09"}), ("1.7 TD 82", "ISUZU-1.7TD", 168)], portes=4, places=5, reservoir=61, remarques="Berline et 5 portes ; " + IND)
mg(L, "Vectra", "Vectra B", "1", "1995-10", "2002-03",
   [("1.6 75", "FAM1-1.6", 128), ("1.6 16V 101", "FAM1-1.6", 150), ("1.8 16V 115", "FAM2-1.8-16V", 170), ("2.0 16V 136", "FAM2-2.0", 185), ("2.2 16V 147", "FAM2-2.2", 203, {"debut": "2000-01"}),
    ("2.5 V6 170", "X25XE-2.5V6", 227), ("i500 2.6 V6 195", "Y26SE-2.6V6", 250, {"debut": "1999-01", "remarques": "Version i500 de la Vectra B (2.5 V6 porté à 2.6)"}),
    ("1.7 TD 82", "ISUZU-1.7TD", 168, {"fin": "1996-12"}), ("2.0 DTI 100", "ECOTEC-2.0DTI", 230, {"debut": "1997-01"}), ("2.2 DTI 125", "ECOTEC-2.2DTI", 280, {"debut": "2000-01"})],
   portes=4, places=5, reservoir=60, remarques="Berline, 5 portes et break ; restylage 1999 ; " + IND)
mg(L, "Vectra", "Vectra C", "1", "2002-03", "2008-09",
   [("1.6 105", "FAM1-1.6", 150), ("1.8 122", "FAM2-1.8", 165), ("1.8 140", "ECOTEC-1.8", 175, {"debut": "2005-09"}), ("2.2 155", "FAM2-2.2", 220), ("2.0 Turbo 175", "FAM2-2.0T", 265),
    ("3.2 V6 211", "Y32SE-3.2V6", 300, {"fin": "2005-08"}), ("2.8 V6 Turbo 230", "Z28NET-2.8V6T", 330, {"debut": "2005-09"}), ("1.9 CDTI 100", "FIAT-1.9TID", 260, {"debut": "2004-01"}),
    ("1.9 CDTI 120", "FIAT-1.9TID", 280, {"debut": "2004-01"}), ("1.9 CDTI 150", "FIAT-1.9TID", 320, {"debut": "2004-01"}), ("2.2 DTI 125", "ECOTEC-2.2DTI", 280, {"fin": "2004-12"})],
   portes=4, places=5, reservoir=61, remarques="Berline, GTS et break ; Signum dérivé ; restylage 2005 ; " + IND)
mg(L, "Insignia", "Insignia A", "1", "2008-09", "2013-08",
   [("1.6 115", "ECOTEC-1.6", 155), ("1.8 140", "ECOTEC-1.8", 175), ("1.6 Turbo 180", "FAM1-1.6T", 230), ("1.4 Turbo 140", "ECOTEC-1.4T", 200, {"debut": "2010-09"}),
    ("2.0 Turbo 220", "A20NHT-2.0T", 350), ("2.8 V6 Turbo 260", "Z28NET-2.8V6T", 350, {"fin": "2010-12"}), ("2.0 CDTI 110", "A20DTH-2.0CDTI", 260), ("2.0 CDTI 130", "A20DTH-2.0CDTI", 300),
    ("2.0 CDTI 160", "A20DTH-2.0CDTI", 350), ("2.0 BiTurbo CDTI 195", "A20DTH-2.0CDTI", 400, {"debut": "2012-01"})],
   portes=5, places=5, reservoir=70, remarques="Voiture européenne de l'année 2009 ; berline 4 et 5 portes, Sports Tourer, Country Tourer")
mg(L, "Insignia", "Insignia A", "2", "2013-09", "2017-06",
   [("1.4 Turbo 140", "ECOTEC-1.4T", 200), ("1.6 Turbo 170", "A16XHT-1.6T", 280), ("2.0 Turbo 250", "A20NHT-2.0T", 400), ("2.0 CDTI 140", "A20DTH-2.0CDTI", 350),
    ("2.0 CDTI 170", "A20DTH-2.0CDTI", 400), ("2.0 BiTurbo CDTI 195", "A20DTH-2.0CDTI", 400), ("1.6 CDTI 136", "B16DTH-1.6CDTI", 320, {"debut": "2015-01"})],
   portes=5, places=5, reservoir=70, remarques="Restylage")
mg(L, "Insignia", "Insignia B", "1", "2017-06", "2022-12",
   [("1.5 Turbo 140", "B15XFT-1.5T", 250), ("1.5 Turbo 165", "B15XFT-1.5T", 250), ("2.0 Turbo 260", "A20NHT-2.0T", 400), ("1.6 CDTI 110", "B16DTH-1.6CDTI", 300, {"fin": "2020-06"}),
    ("1.6 CDTI 136", "B16DTH-1.6CDTI", 320, {"fin": "2020-06"}), ("2.0 CDTI 170", "A20DTH-2.0CDTI", 400, {"fin": "2020-06"}), ("1.5 D 122", "D15DT-1.5D", 300, {"debut": "2020-06"}),
    ("2.0 D 174", "A20DTH-2.0CDTI", 381, {"debut": "2020-06"})],
   portes=5, places=5, reservoir=62, remarques="Grand Sport, Sports Tourer, Country Tourer ; restylage 2020 ; GSi 2.0 Turbo 260 (4x4)")

# ---------------------------------------------------------------- Corsa / Tigra
mg(L, "Corsa", "Corsa A", "1", "1982-09", "1993-03",
   [("1.0 45", "OHV-1.0", 70), ("1.2 55", "FAM1-1.2", 88), ("1.3 70", "FAM1-1.4", 100), ("1.4 60", "FAM1-1.4", 103, {"debut": "1990-01"}), ("GSi 1.6 100", "FAM2-1.6", 135, {"debut": "1988-01"}),
    ("1.5 TD 67", "ISUZU-1.5TD", 132, {"debut": "1988-01"})], portes=3, places=5, reservoir=42, remarques="3 et 5 portes, berline 4 portes ; " + IND)
mg(L, "Corsa", "Corsa B", "1", "1993-03", "2000-08",
   [("1.0 54", "FAM0-1.0", 82, {"debut": "1996-09"}), ("1.2 45", "FAM1-1.2", 88), ("1.2 16V 65", "FAM0-1.2", 110, {"debut": "1998-01"}), ("1.4 60", "FAM1-1.4", 103), ("1.4 16V 90", "FAM1-1.4", 125),
    ("GSi 1.6 16V 106", "FAM1-1.6", 148, {"fin": "1998-06"}), ("1.5 TD 67", "ISUZU-1.5TD", 132), ("1.7 D 60", "ISUZU-1.7TD", 112, {"debut": "1997-01"})],
   portes=3, places=5, reservoir=46, remarques="Dont Corsa GSi ; " + IND)
mg(L, "Tigra", "Tigra A", "1", "1994-09", "2000-12", [("1.4 16V 90", "FAM1-1.4", 125), ("1.6 16V 106", "FAM1-1.6", 148)], portes=3, places=4, reservoir=46, remarques="Coupé sur base Corsa B ; " + IND)
mg(L, "Corsa", "Corsa C", "1", "2000-09", "2006-09",
   [("1.0 60", "FAM0-1.0", 88), ("1.2 75", "FAM0-1.2", 110), ("1.4 90", "FAM0-1.4", 125), ("1.8 125", "FAM2-1.8-16V", 170), ("1.7 DI 65", "ISUZU-1.7CDTI", 120, {"fin": "2003-06"}),
    ("1.7 CDTI 100", "ISUZU-1.7CDTI", 240, {"debut": "2003-07"}), ("1.3 CDTI 70", "FIAT-1.3CDTI", 170, {"debut": "2003-07"})], portes=3, places=5, reservoir=44, remarques="Restylage 2003 ; " + IND)
mg(L, "Tigra", "Tigra TwinTop", "1", "2004-09", "2009-06", [("1.4 90", "FAM0-1.4", 125), ("1.8 125", "FAM2-1.8-16V", 170), ("1.3 CDTI 70", "FIAT-1.3CDTI", 170)], portes=2, places=2, reservoir=45,
   remarques="Coupé-cabriolet")
mg(L, "Corsa", "Corsa D", "1", "2006-09", "2010-12",
   [("1.0 60", "FAM0-1.0", 88), ("1.2 80", "FAM0-1.2", 110), ("1.4 90", "FAM0-1.4", 125), ("GSi 1.6 Turbo 150", "FAM1-1.6T", 210, {"debut": "2007-06"}), ("1.3 CDTI 75", "FIAT-1.3CDTI", 190),
    ("1.3 CDTI 90", "FIAT-1.3CDTI", 200), ("1.7 CDTI 125", "ISUZU-1.7CDTI", 280)], portes=3, places=5, reservoir=45, remarques="3 et 5 portes")
mg(L, "Corsa", "Corsa D", "2", "2011-01", "2014-12",
   [("1.0 65", "FAM0-1.0", 95), ("1.2 85", "FAM0-1.2", 115), ("1.4 100", "FAM0-1.4", 130), ("1.4 Turbo 120", "ECOTEC-1.4T", 175, {"debut": "2012-01"}), ("1.3 CDTI 75", "FIAT-1.3CDTI", 190),
    ("1.3 CDTI 95", "FIAT-1.3CDTI", 190)], portes=3, places=5, reservoir=45, remarques="Restylage")
mg(L, "Corsa", "Corsa E", "1", "2014-11", "2019-06",
   [("1.2 70", "FAM0-1.2", 115), ("1.4 75", "FAM0-1.4", 130), ("1.4 90", "FAM0-1.4", 125), ("1.0 Turbo 90", "B10XFT-1.0T", 170), ("1.0 Turbo 115", "B10XFT-1.0T", 170),
    ("1.4 Turbo 100", "B14XFT-1.4T", 200), ("1.4 Turbo 150", "B14XFT-1.4T", 245), ("1.3 CDTI 75", "FIAT-1.3CDTI", 190), ("1.3 CDTI 95", "FIAT-1.3CDTI", 190)],
   portes=3, places=5, reservoir=45, remarques="3 et 5 portes ; GSi 1.4 Turbo 150 (2018)")
mg(L, "Corsa", "Corsa F", "1", "2019-11", "2023-08",
   [psa("1.2 75", "1.2 PureTech 75"), psa("1.2 Turbo 100", "1.2 PureTech 100"), psa("1.2 Turbo 130", "1.2 PureTech 130 EAT8"), psa("1.5 D 100", "1.5 BlueHDi 100"),
    psa("Corsa-e 136", "e-208 136", el(50))], portes=5, places=5, reservoir=44, remarques="Plateforme CMP (PSA)")
mg(L, "Corsa", "Corsa F", "2", "2023-09", None,
   [psa("1.2 75", "1.2 PureTech 75"), psa("1.2 Turbo 100", "1.2 PureTech 100"), psa("1.2 Hybrid 100", "1.2 Hybrid 100 e-DCS6", {"debut": "2024-06"}),
    psa("1.2 Hybrid 136", "1.2 Hybrid 136 e-DCS6", {"debut": "2024-06"}), psa("Electric 136", "e-208 136", el(50)), psa("Electric 156", "e-208 156", el(51))],
   portes=5, places=5, reservoir=44, remarques="Restylage ; Corsa-e renommée Corsa Electric")

# ---------------------------------------------------------------- Astra
mg(L, "Astra", "Astra F", "1", "1991-09", "1998-03",
   [("1.4 60", "FAM1-1.4", 103), ("1.4 16V 90", "FAM1-1.4", 125, {"debut": "1996-01"}), ("1.6 75", "FAM1-1.6", 128), ("1.6 16V 101", "FAM1-1.6", 150, {"debut": "1994-09"}),
    ("1.8 16V 116", "FAM2-1.8-16V", 170, {"debut": "1993-01"}), ("GSi 2.0 115", "FAM2-2.0", 170, {"fin": "1993-08"}), ("GSi 16V 2.0 150", "FAM2-2.0-16V", 196), ("2.0 16V 136", "FAM2-2.0", 185, {"debut": "1994-09"}),
    ("1.7 D 60", "OPEL-1.7D", 105), ("1.7 TD 82", "ISUZU-1.7TD", 168), ("1.7 TDS 68", "ISUZU-1.7TD", 132, {"debut": "1994-09"})],
   portes=5, places=5, reservoir=52, remarques="3 et 5 portes, berline, break Caravan, cabriolet ; restylage 1994 ; " + IND)
mg(L, "Astra", "Astra G", "1", "1998-03", "2004-12",
   [("1.2 16V 65", "FAM0-1.2", 110), ("1.4 16V 90", "FAM1-1.4", 125), ("1.6 75", "FAM1-1.6", 128), ("1.6 16V 101", "FAM1-1.6", 150), ("1.8 16V 116", "FAM2-1.8-16V", 170),
    ("1.8 16V 125", "FAM2-1.8-16V", 170, {"debut": "2000-09"}), ("2.2 16V 147", "FAM2-2.2", 203, {"debut": "2000-09"}), ("1.7 DTI 75", "ISUZU-1.7CDTI", 165), ("1.7 CDTI 80", "ISUZU-1.7CDTI", 170, {"debut": "2003-01"}),
    ("2.0 DTI 100", "ECOTEC-2.0DTI", 230), ("2.2 DTI 125", "ECOTEC-2.2DTI", 280, {"debut": "2002-01"})],
   portes=5, places=5, reservoir=52, remarques="3 et 5 portes, berline, break, coupé et cabriolet (Bertone) ; " + IND)
mg(L, "Astra", "Astra H", "1", "2004-03", "2010-06",
   [("1.4 90", "FAM0-1.4", 125), ("1.6 105", "FAM1-1.6", 150), ("1.6 115", "ECOTEC-1.6", 155, {"debut": "2006-09"}), ("1.8 125", "FAM2-1.8-16V", 170), ("1.8 140", "ECOTEC-1.8", 175, {"debut": "2006-09"}),
    ("2.0 Turbo 170", "FAM2-2.0T", 262), ("1.6 Turbo 180", "FAM1-1.6T", 230, {"debut": "2007-09"}), ("1.3 CDTI 90", "FIAT-1.3CDTI", 200), ("1.7 CDTI 100", "ISUZU-1.7CDTI", 240),
    ("1.7 CDTI 125", "ISUZU-1.7CDTI", 280, {"debut": "2007-01"}), ("1.9 CDTI 120", "FIAT-1.9TID", 280), ("1.9 CDTI 150", "FIAT-1.9TID", 320)],
   portes=5, places=5, reservoir=52, remarques="3 portes GTC, 5 portes, break, berline et TwinTop ; restylage 2007")
mg(L, "Astra", "Astra J", "1", "2009-12", "2015-09",
   [("1.4 100", "FAM0-1.4", 130), ("1.6 115", "ECOTEC-1.6", 155), ("1.4 Turbo 120", "ECOTEC-1.4T", 175), ("1.4 Turbo 140", "ECOTEC-1.4T", 200), ("1.6 Turbo 180", "FAM1-1.6T", 230),
    ("1.6 SIDI Turbo 200", "A16XHT-1.6T", 300, {"debut": "2013-06"}), ("1.3 CDTI 95", "FIAT-1.3CDTI", 190), ("1.7 CDTI 110", "ISUZU-1.7CDTI", 260), ("1.7 CDTI 130", "VCDI-1.7", 300),
    ("2.0 CDTI 160", "A20DTH-2.0CDTI", 350), ("2.0 BiTurbo CDTI 195", "A20DTH-2.0CDTI", 400, {"debut": "2012-09"}), ("1.6 CDTI 136", "B16DTH-1.6CDTI", 320, {"debut": "2014-01"})],
   portes=5, places=5, reservoir=56, remarques="5 portes, GTC, Sports Tourer, berline ; restylage 2012")
mg(L, "Astra", "Astra K", "1", "2015-09", "2019-09",
   [("1.4 100", "FAM0-1.4", 130), ("1.0 Turbo 105", "B10XFT-1.0T", 170), ("1.4 Turbo 125", "B14XFT-1.4T", 245), ("1.4 Turbo 150", "B14XFT-1.4T", 245), ("1.6 Turbo 200", "A16XHT-1.6T", 300),
    ("1.6 CDTI 110", "B16DTH-1.6CDTI", 300), ("1.6 CDTI 136", "B16DTH-1.6CDTI", 320), ("1.6 BiTurbo CDTI 160", "B16DTH-1.6CDTI", 350)],
   portes=5, places=5, reservoir=48, remarques="Voiture européenne de l'année 2016 ; 5 portes et Sports Tourer")
mg(L, "Astra", "Astra K", "2", "2019-10", "2021-12",
   [("1.2 Turbo 110", "D12XHT-1.2T", 195), ("1.2 Turbo 130", "D12XHT-1.2T", 225), ("1.2 Turbo 145", "D12XHT-1.2T", 225), ("1.4 Turbo 145", "B14XFT-1.4T", 236),
    ("1.5 D 105", "D15DT-1.5D", 260), ("1.5 D 122", "D15DT-1.5D", 300)], portes=5, places=5, reservoir=52, remarques="Restylage ; nouveaux trois cylindres")
mg(L, "Astra", "Astra L", "1", "2021-11", "2026-02",
   [psa("1.2 Turbo 110", "1.2 PureTech 110"), psa("1.2 Turbo 130", "1.2 PureTech 130"), psa("1.5 D 130", "1.5 BlueHDi 130"), psa("Hybrid 180", "Hybrid 180 e-EAT8", {"batterie": 12}),
    psa("Electric 156", "e-308 156", el(54, debut="2023-04")), psa("1.2 Hybrid 136", "1.2 Hybrid 136 e-DCS6", {"debut": "2024-09"})],
   portes=5, places=5, reservoir=52, remarques="5 portes et Sports Tourer ; plateforme EMP2 ; Plug-in Hybrid 180")
mg(L, "Astra", "Astra L", "2", "2026-03", None,
   [psa("1.2 Hybrid 145", "1.2 Hybrid 145 e-DCS6"), psa("Hybrid 195", "Plug-in Hybrid 195 e-DCS7", {"batterie": 17}), psa("1.5 D 130", "1.5 BlueHDi 130"), psa("Electric 156", "e-308 156", el(58))],
   portes=5, places=5, reservoir=52, remarques="Restylage (présenté en janvier 2026) ; " + IND)

# ---------------------------------------------------------------- monospaces
mg(L, "Zafira", "Zafira A", "1", "1999-04", "2005-06",
   [("1.6 16V 101", "FAM1-1.6", 150), ("1.8 16V 116", "FAM2-1.8-16V", 170), ("1.8 16V 125", "FAM2-1.8-16V", 170, {"debut": "2000-09"}), ("2.2 16V 147", "FAM2-2.2", 203, {"debut": "2001-09"}),
    ("2.0 DTI 100", "ECOTEC-2.0DTI", 230), ("2.2 DTI 125", "ECOTEC-2.2DTI", 280, {"debut": "2002-01"})], portes=5, places=7, reservoir=58, remarques="7 places (Flex7) ; " + IND)
mg(L, "Zafira", "Zafira B", "1", "2005-07", "2014-12",
   [("1.6 105", "FAM1-1.6", 150), ("1.6 115", "ECOTEC-1.6", 155, {"debut": "2008-01"}), ("1.8 140", "ECOTEC-1.8", 175), ("2.2 150", "FAM2-2.2", 215), ("1.6 Turbo 150", "FAM1-1.6T", 210, {"debut": "2010-01"}),
    ("1.7 CDTI 110", "ISUZU-1.7CDTI", 260, {"debut": "2009-01"}), ("1.9 CDTI 120", "FIAT-1.9TID", 280), ("1.9 CDTI 150", "FIAT-1.9TID", 320)], portes=5, places=7, reservoir=58,
   remarques="Restylage 2008 ; vendu en Zafira Family jusqu'en 2014")
mg(L, "Zafira", "Zafira C", "1", "2011-11", "2019-06",
   [("1.4 Turbo 120", "ECOTEC-1.4T", 175), ("1.4 Turbo 140", "ECOTEC-1.4T", 200), ("1.6 Turbo 170", "A16XHT-1.6T", 280), ("2.0 CDTI 110", "A20DTH-2.0CDTI", 260), ("2.0 CDTI 130", "A20DTH-2.0CDTI", 300),
    ("2.0 CDTI 165", "A20DTH-2.0CDTI", 350), ("1.6 CDTI 136", "B16DTH-1.6CDTI", 320, {"debut": "2014-06"}), ("2.0 BiTurbo CDTI 195", "A20DTH-2.0CDTI", 400, {"debut": "2012-09", "fin": "2016-08"})],
   portes=5, places=7, reservoir=58, remarques="Zafira Tourer ; restylage 2016")
mg(L, "Meriva", "Meriva A", "1", "2003-05", "2010-05",
   [("1.4 90", "FAM0-1.4", 125), ("1.6 87", "FAM1-1.6", 130), ("1.6 16V 105", "FAM1-1.6", 150), ("1.8 125", "FAM2-1.8-16V", 170), ("1.3 CDTI 75", "FIAT-1.3CDTI", 190), ("1.7 CDTI 100", "ISUZU-1.7CDTI", 240)],
   portes=5, places=5, reservoir=52, remarques="Restylage 2006")
mg(L, "Meriva", "Meriva B", "1", "2010-06", "2017-03",
   [("1.4 100", "FAM0-1.4", 130), ("1.4 Turbo 120", "ECOTEC-1.4T", 175), ("1.4 Turbo 140", "ECOTEC-1.4T", 200), ("1.3 CDTI 95", "FIAT-1.3CDTI", 190), ("1.7 CDTI 110", "ISUZU-1.7CDTI", 260),
    ("1.6 CDTI 136", "B16DTH-1.6CDTI", 320, {"debut": "2014-01"})], portes=5, places=5, reservoir=54, remarques="Portes arrière antagonistes")

# ---------------------------------------------------------------- petites et spéciales
mg(L, "Agila", "Agila A", "1", "2000-03", "2007-12", [("1.0 58", "FAM0-1.0", 85), ("1.2 75", "FAM0-1.2", 110), ("1.3 CDTI 70", "FIAT-1.3CDTI", 170, {"debut": "2003-09"})],
   portes=5, places=5, reservoir=41, remarques="Jumelle de la Suzuki Wagon R+")
mg(L, "Agila", "Agila B", "1", "2008-04", "2014-12", [("1.0 65", "SUZUKI-K10", 90), ("1.2 86", "SUZUKI-K12", 114), ("1.2 94", "SUZUKI-K12", 118, {"debut": "2010-01"})],
   portes=5, places=5, reservoir=35, remarques="Jumelle de la Suzuki Splash")
mg(L, "Adam", "Adam", "1", "2013-01", "2019-12",
   [("1.2 70", "FAM0-1.2", 115), ("1.4 87", "FAM0-1.4", 130), ("1.4 100", "FAM0-1.4", 130), ("1.0 Turbo 90", "B10XFT-1.0T", 170, {"debut": "2014-09"}), ("1.0 Turbo 115", "B10XFT-1.0T", 170, {"debut": "2014-09"}),
    ("S 1.4 Turbo 150", "ECOTEC-1.4T", 220, {"debut": "2014-09"})], portes=3, places=4, reservoir=38, remarques="Dont Adam Rocks (toit toile) et Adam S")
mg(L, "Karl", "Karl", "1", "2015-03", "2019-06", [("1.0 75", "B10D-1.0", 95)], portes=5, places=5, reservoir=32, remarques="Jumelle de la Chevrolet Spark ; dont Karl Rocks")
mg(L, "Cascada", "Cascada", "1", "2013-03", "2019-06",
   [("1.4 Turbo 120", "ECOTEC-1.4T", 175), ("1.4 Turbo 140", "ECOTEC-1.4T", 200), ("1.6 SIDI Turbo 170", "A16XHT-1.6T", 280), ("1.6 SIDI Turbo 200", "A16XHT-1.6T", 300),
    ("2.0 CDTI 165", "A20DTH-2.0CDTI", 350), ("2.0 BiTurbo CDTI 195", "A20DTH-2.0CDTI", 400)], portes=2, places=4, reservoir=56, remarques="Cabriolet 4 places")
mg(L, "Speedster", "Speedster", "1", "2000-06", "2005-12", [("2.2 147", "FAM2-2.2", 203), ("Turbo 2.0 200", "FAM2-2.0T", 250, {"debut": "2003-09"})], portes=2, places=2, reservoir=36,
   remarques="Roadster sur base Lotus Elise (Vauxhall VX220)")

# ---------------------------------------------------------------- SUV et 4x4
mg(L, "Frontera", "Frontera A", "1", "1991-09", "1998-08",
   [("2.0 115", "FAM2-2.0", 170), ("2.4 125", "CIH-2.4", 195), ("2.3 TD 100", "OPEL-2.3TD", 215), ("2.8 TD 113", "4JB1-2.8TD", 245, {"debut": "1995-01"})],
   portes=5, places=5, reservoir=80, remarques="Sport (3 portes) et 5 portes, base Isuzu ; " + IND)
mg(L, "Frontera", "Frontera B", "1", "1998-09", "2004-06",
   [("2.2 136", "FAM2-2.2", 207), ("3.2 V6 205", "6VD1-3.2", 290), ("2.2 DTI 116", "ECOTEC-2.2DTI", 260)], portes=5, places=5, reservoir=80, remarques="Base Isuzu ; " + IND)
mg(L, "Frontera", "Frontera (2024)", "1", "2025-02", None,
   [psa("1.2 Hybrid 110", "1.2 Hybrid 110 e-DCS6"), psa("1.2 Hybrid 136", "1.2 Hybrid 136 e-DCS6"), ("Electric 113", "STLA-SMART-EV", 125, el(44)),
    ("Electric Extended Range 113", "STLA-SMART-EV", 125, el(54, debut="2025-09"))],
   portes=5, places=5, reservoir=44, remarques="Plateforme Smart Car (Stellantis), 5 ou 7 places ; remplace le Crossland")
mg(L, "Antara", "Antara", "1", "2006-10", "2015-06",
   [("2.4 140", "GM-2.4", 220), ("2.4 167", "GM-2.4", 230, {"debut": "2010-09"}), ("3.2 V6 227", "GM-V6-3.2", 297, {"fin": "2010-08"}), ("2.0 CDTI 127", "VCDI-2.0", 295, {"fin": "2010-08"}),
    ("2.0 CDTI 150", "VCDI-2.0", 320, {"fin": "2010-08"}), ("2.2 CDTI 163", "VCDI-2.2", 350, {"debut": "2010-09"}), ("2.2 CDTI 184", "VCDI-2.2", 400, {"debut": "2010-09"})],
   portes=5, places=5, reservoir=65, remarques="Jumeau du Chevrolet Captiva ; restylage 2010")
mg(L, "Mokka", "Mokka A", "1", "2012-10", "2019-12",
   [("1.6 115", "ECOTEC-1.6", 155), ("1.4 Turbo 140", "ECOTEC-1.4T", 200), ("1.4 Turbo 152", "ECOTEC-1.4T", 245, {"debut": "2016-09"}), ("1.7 CDTI 130", "VCDI-1.7", 300),
    ("1.6 CDTI 136", "B16DTH-1.6CDTI", 320, {"debut": "2015-09"}), ("1.6 CDTI 110", "B16DTH-1.6CDTI", 300, {"debut": "2016-09"})],
   portes=5, places=5, reservoir=52, remarques="Mokka X à partir de 2016")
mg(L, "Mokka", "Mokka B", "1", "2020-10", "2024-08",
   [psa("1.2 Turbo 100", "1.2 PureTech 100"), psa("1.2 Turbo 130", "1.2 PureTech 130 EAT8"), psa("1.5 D 110", "1.5 BlueHDi 110"), psa("Mokka-e 136", "e-2008 136", el(50))],
   portes=5, places=5, reservoir=44, remarques="Plateforme CMP")
mg(L, "Mokka", "Mokka B", "2", "2024-09", None,
   [psa("1.2 Turbo 100", "1.2 PureTech 100"), psa("1.2 Turbo 136", "1.2 Hybrid 136 e-DCS6", {"remarques": "Hybride 48 V"}), psa("Electric 156", "e-2008 156", el(51))],
   portes=5, places=5, reservoir=44, remarques="Restylage ; Mokka-e renommé Mokka Electric")
mg(L, "Crossland", "Crossland", "1", "2017-06", "2024-12",
   [psa("1.2 82", "1.2 PureTech 82"), psa("1.2 Turbo 110", "1.2 PureTech 110"), psa("1.2 Turbo 130", "1.2 PureTech 130"), psa("1.5 D 100", "1.5 BlueHDi 100"),
    psa("1.5 D 120", "1.5 BlueHDi 120")], portes=5, places=5, reservoir=45, remarques="Crossland X jusqu'en 2020, puis Crossland ; base Peugeot 2008 / Citroën C3 Aircross")
mg(L, "Grandland", "Grandland X", "1", "2017-10", "2024-06",
   [psa("1.2 Turbo 130", "1.2 PureTech 130"), psa("1.6 Turbo 180", "1.6 PureTech 180 EAT8"), psa("1.5 D 130", "1.5 BlueHDi 130"), psa("2.0 D 180", "2.0 BlueHDi 180 EAT8", {"fin": "2020-12"}),
    psa("Hybrid 225", "Hybrid 225 e-EAT8", {"debut": "2020-01", "batterie": 13}), psa("Hybrid4 300", "Hybrid4 300 e-EAT8", {"debut": "2020-01", "batterie": 13})],
   portes=5, places=5, reservoir=53, remarques="Grandland X jusqu'en 2021, puis Grandland ; base Peugeot 3008")
mg(L, "Grandland", "Grandland (2024)", "1", "2025-01", None,
   [psa("1.2 Hybrid 145", "1.2 Hybrid 145 e-DCS6"), psa("Plug-in Hybrid 195", "Plug-in Hybrid 195 e-DCS7", {"batterie": 21}), psa("Electric 210", "e-3008 210", el(73)),
    psa("Electric Long Range 230", "e-3008 Long Range 230", el(97, debut="2025-06")), psa("Electric AWD 325", "e-3008 Dual Motor 325", el(73, debut="2025-06"))],
   portes=5, places=5, reservoir=55, remarques="Plateforme STLA Medium ; puissances alignées sur Peugeot")
mg(L, "Ampera", "Ampera", "1", "2011-11", "2015-12", [("1.4 Range Extender 150", "VOLTEC-1.4", 370, {"batterie": 16, "reservoir": 35})], portes=5, places=4, reservoir=35,
   remarques="Électrique à prolongateur d'autonomie, jumelle de la Chevrolet Volt")
mg(L, "Ampera-e", "Ampera-e", "1", "2017-05", "2020-12", [("Électrique 204", "GM-EV-BOLT", 360, el(60))], portes=5, places=5, reservoir=0,
   remarques="Jumelle de la Chevrolet Bolt")

# ---------------------------------------------------------------- Opel OPC / GSi / GSe / GSE
mg(OPC, "Astra OPC", "Astra G OPC", "1", "1999-09", "2004-12", [("2.0 16V 160", "FAM2-2.0", 190, {"fin": "2001-12"}), ("2.0 Turbo 200", "FAM2-2.0T", 250, {"debut": "2002-01"})],
   portes=3, places=5, reservoir=52, remarques="3 portes, coupé et break ; " + IND)
mg(OPC, "Astra OPC", "Astra H OPC", "1", "2005-09", "2010-12", [("2.0 Turbo 240", "FAM2-2.0T", 320)], portes=3, places=5, reservoir=52, remarques="Astra GTC OPC")
mg(OPC, "Astra OPC", "Astra J OPC", "1", "2012-06", "2015-12", [("2.0 Turbo 280", "FAM2-2.0T", 400)], portes=3, places=5, reservoir=56, remarques="Astra GTC OPC")
mg(OPC, "Corsa OPC", "Corsa D OPC", "1", "2007-06", "2014-12", [("1.6 Turbo 192", "FAM1-1.6T", 230), ("Nürburgring 1.6 Turbo 210", "FAM1-1.6T", 250, {"debut": "2011-09"})],
   portes=3, places=5, reservoir=45)
mg(OPC, "Corsa OPC", "Corsa E OPC", "1", "2015-06", "2019-06", [("1.6 Turbo 207", "FAM1-1.6T", 245)], portes=3, places=5, reservoir=45, remarques="Couple porté à 280 Nm en overboost")
mg(OPC, "Vectra OPC", "Vectra C OPC", "1", "2005-09", "2008-09", [("2.8 V6 Turbo 280", "Z28NET-2.8V6T", 355)], portes=5, places=5, reservoir=61, remarques="5 portes GTS et break")
mg(OPC, "Insignia OPC", "Insignia A OPC", "1", "2009-09", "2017-06", [("2.8 V6 Turbo 325", "Z28NET-2.8V6T", 435)], portes=5, places=5, reservoir=70,
   remarques="Berline 5 portes et Sports Tourer, transmission intégrale")
mg(OPC, "Insignia GSi", "Insignia B GSi", "1", "2017-09", "2020-06", [("2.0 Turbo 260", "A20NHT-2.0T", 400), ("2.0 BiTurbo CDTI 210", "A20DTH-2.0CDTI", 480)], portes=5, places=5, reservoir=62,
   remarques="Grand Sport et Sports Tourer ; GSi 2.0 Turbo 230 après 2020 non repris")
mg(OPC, "Meriva OPC", "Meriva A OPC", "1", "2006-01", "2010-05", [("1.6 Turbo 180", "FAM1-1.6T", 230)], portes=5, places=5, reservoir=52)
mg(OPC, "Zafira OPC", "Zafira A OPC", "1", "2001-09", "2005-06", [("2.0 Turbo 192", "FAM2-2.0T", 250), ("2.0 Turbo 200", "FAM2-2.0T", 250, {"debut": "2003-01"})], portes=5, places=7, reservoir=58)
mg(OPC, "Zafira OPC", "Zafira B OPC", "1", "2005-07", "2010-12", [("2.0 Turbo 240", "FAM2-2.0T", 320)], portes=5, places=7, reservoir=58)
mg(OPC, "Astra GSe", "Astra L GSe", "1", "2023-03", "2026-02", [psa("Hybrid 225", "Hybrid 225 e-EAT8", {"batterie": 12})], portes=5, places=5, reservoir=40,
   remarques="Hybride rechargeable ; 5 portes et Sports Tourer")
mg(OPC, "Grandland GSe", "Grandland X GSe", "1", "2022-09", "2024-06", [psa("Hybrid4 300", "Hybrid4 300 e-EAT8", {"batterie": 13})], portes=5, places=5, reservoir=43,
   remarques="Hybride rechargeable, transmission intégrale")
mg(OPC, "Mokka GSE", "Mokka B GSE", "1", "2025-06", None, [("Electric 281", "E-CMP", 345, el(54))], portes=5, places=5, reservoir=0,
   remarques="Électrique, base Abarth 600e / Alfa Romeo Junior Veloce ; " + IND)
mg(OPC, "Corsa GSE", "Corsa F GSE", "1", "2026-09", None, [("Electric 281", "E-CMP", 345, el(54))], portes=5, places=5, reservoir=0,
   remarques="Électrique, annoncée en 2026 ; " + IND)

MOT = Motorisations("Opel", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(OPC)

DETAIL = {"Opel": L, "Opel OPC": OPC}
MOTEURS = MOT.moteurs()
