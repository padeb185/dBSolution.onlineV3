"""Mini (classique BMC/Rover puis BMW) : générations, phases, motorisations et moteurs liés.
Les familles de moteurs BMW définies ici (N12…B48) sont réutilisées par le fichier BMW."""
from ._outil import Motorisations, electrique, famille as f, gamme as g


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


L = []

# ---------------------------------------------------------------- Mini classique
L += g("Mini", "ADO15", "Mk1", "1959-08", "1967-09",
       ["850 34", ("Cooper 997 55", {"debut": "1961-09", "fin": "1964-01"}), ("Cooper 998 55", {"debut": "1964-01"}),
        ("Cooper S 1071 70", {"debut": "1963-03", "fin": "1964-08"}), ("Cooper S 1275 76", {"debut": "1964-03"})],
       portes=2, places=4, reservoir=25, remarques="Austin Seven / Morris Mini-Minor ; Traveller, Countryman, Van")
L += g("Mini", "ADO15", "Mk2", "1967-10", "1969-10",
       ["850 34", "1000 38", "Cooper 998 55", "Cooper S 1275 76"], portes=2, places=4, reservoir=25)
L += g("Mini", "ADO15", "Mk3-5", "1969-11", "1984-09",
       ["850 34", "1000 38", ("Cooper S 1275 76", {"fin": "1971-06"}), ("1275 GT 59", {"debut": "1969-11", "fin": "1980-08"})],
       portes=2, places=4, reservoir=25, remarques="Mini (marque autonome), Clubman (1969-1980), 1275 GT")
L += g("Mini", "ADO15", "Mk6-7", "1984-10", "2000-10",
       ["1000 40", ("1000 42", {"debut": "1988-01", "fin": "1992-12"}), ("Cooper 1.3 63", {"debut": "1990-07"}),
        ("1.3i 50", {"debut": "1992-01"}), ("1.3i 63", {"debut": "1996-10"})],
       portes=2, places=4, reservoir=34, remarques="Rover Mini, Cabriolet (1993-1996)")

# ---------------------------------------------------------------- Cooper (Hatch 3 et 5 portes)
L += g("Cooper", "R50", "1", "2001-07", "2004-06",
       ["One 1.6 90", "Cooper 1.6 115", ("One D 1.4 75", {"debut": "2003-06"}), ("One 1.4 75", {"debut": "2003-06"})],
       portes=3, places=4, reservoir=50, remarques="Hatch 3 portes")
L += g("Cooper", "R50", "2", "2004-07", "2006-11",
       ["One 1.6 90", "Cooper 1.6 116", "One D 1.4 88", "One 1.4 75"], portes=3, places=4, reservoir=50,
       remarques="Hatch 3 portes")
L += g("Cooper", "R53", "1", "2002-06", "2004-06", ["Cooper S 1.6 163"], portes=3, places=4, reservoir=50,
       remarques="Cooper S à compresseur")
L += g("Cooper", "R53", "2", "2004-07", "2006-11",
       ["Cooper S 1.6 170", "John Cooper Works 1.6 200", ("John Cooper Works 1.6 210", {"debut": "2005-09"}),
        ("John Cooper Works GP 1.6 218", {"debut": "2006-06"})], portes=3, places=4, reservoir=50,
       remarques="Cooper S à compresseur ; JCW en kit puis GP")
L += g("Cooper", "R56", "1", "2006-11", "2010-02",
       ["One 1.4 75", "One 1.4 95", "Cooper 1.6 120", "Cooper S 1.6 175", ("John Cooper Works 1.6 211", {"debut": "2008-09"}),
        ("Cooper D 1.6 110", {"debut": "2007-03"}), ("One D 1.4 88", {"debut": "2007-03", "fin": "2008-12"})],
       portes=3, places=4, reservoir=40, remarques="Hatch 3 portes")
L += g("Cooper", "R56", "2", "2010-03", "2014-02",
       ["One 1.6 75", "One 1.6 98", "Cooper 1.6 122", "Cooper S 1.6 184", "John Cooper Works 1.6 211",
        ("John Cooper Works GP 1.6 218", {"debut": "2012-11", "fin": "2013-12"}), "One D 1.6 90", "Cooper D 1.6 112",
        ("Cooper SD 2.0 143", {"debut": "2011-03"})], portes=3, places=4, reservoir=40, remarques="Hatch 3 portes")
L += g("Cooper", "F56", "1", "2014-03", "2018-02",
       ["One 1.2 75", "One 1.2 102", "Cooper 1.5 136", "Cooper S 2.0 192", ("John Cooper Works 2.0 231", {"debut": "2015-03"}),
        "One D 1.5 95", "Cooper D 1.5 116", "Cooper SD 2.0 170"], portes=3, places=4, reservoir=40,
       remarques="Hatch 3 portes (F55 : 5 portes)")
L += g("Cooper", "F56", "2", "2018-03", "2021-02",
       ["One 1.5 75", "One 1.5 102", "Cooper 1.5 136", "Cooper S 2.0 192", ("Cooper S 2.0 178", {"debut": "2019-07"}),
        "John Cooper Works 2.0 231", ("Cooper SE 184", el(33, debut="2020-03")), ("GP 2.0 306", {"debut": "2020-03", "fin": "2021-06"}),
        ("Cooper D 1.5 116", {"fin": "2020-06"}), ("Cooper SD 2.0 170", {"fin": "2020-06"})],
       portes=3, places=4, reservoir=40, remarques="Hatch 3 portes (F55 : 5 portes)")
L += g("Cooper", "F56", "3", "2021-03", "2024-02",
       ["One 1.5 75", "One 1.5 102", "Cooper 1.5 136", "Cooper S 2.0 178", "John Cooper Works 2.0 231",
        ("Cooper SE 184", el(33))], portes=3, places=4, reservoir=44, remarques="Hatch 3 portes (F55 : 5 portes)")
L += g("Cooper", "F55", "1", "2014-09", "2024-02",
       ["One 1.2 102", "One 1.5 102", "Cooper 1.5 136", "Cooper S 2.0 192", "Cooper S 2.0 178", "One D 1.5 95",
        "Cooper D 1.5 116", "Cooper SD 2.0 170"], places=5, reservoir=44,
       remarques="Hatch 5 portes ; phases identiques à la F56 (2018, 2021)")
L += g("Cooper", "F66", "1", "2024-03", None,
       ["Cooper C 1.5 156", "Cooper S 2.0 204", ("John Cooper Works 2.0 231", {"debut": "2024-09"})],
       portes=3, places=4, reservoir=44, remarques="Mini Cooper thermique 3 portes (F65 : 5 portes)")
L += g("Cooper", "F65", "1", "2024-07", None, ["Cooper C 1.5 156", "Cooper S 2.0 204"], places=5, reservoir=44,
       remarques="Mini Cooper thermique 5 portes")
L += g("Cooper", "J01", "1", "2024-03", None,
       [("Cooper E 184", el(41)), ("Cooper SE 218", el(54)), ("John Cooper Works E 258", el(54, debut="2025-01"))],
       portes=3, places=4, reservoir=0, remarques="Mini Cooper électrique 3 portes (fabriquée en Chine)")

# ---------------------------------------------------------------- Cabriolet
L += g("Convertible", "R52", "1", "2004-07", "2008-11",
       ["One 1.6 90", "Cooper 1.6 116", "Cooper S 1.6 170", ("John Cooper Works 1.6 210", {"debut": "2006-01"})],
       portes=2, places=4, reservoir=50, remarques="Cabriolet")
L += g("Convertible", "R57", "1", "2009-03", "2010-02",
       ["One 1.6 98", "Cooper 1.6 120", "Cooper S 1.6 175", "John Cooper Works 1.6 211"], portes=2, places=4,
       reservoir=40, remarques="Cabriolet")
L += g("Convertible", "R57", "2", "2010-03", "2015-12",
       ["One 1.6 98", "Cooper 1.6 122", "Cooper S 1.6 184", "John Cooper Works 1.6 211", "Cooper D 1.6 112",
        ("Cooper SD 2.0 143", {"debut": "2011-03"})], portes=2, places=4, reservoir=40, remarques="Cabriolet")
L += g("Convertible", "F57", "1", "2016-03", "2018-02",
       ["One 1.2 102", "Cooper 1.5 136", "Cooper S 2.0 192", "John Cooper Works 2.0 231", "Cooper D 1.5 116"],
       portes=2, places=4, reservoir=40, remarques="Cabriolet")
L += g("Convertible", "F57", "2", "2018-03", "2024-02",
       ["One 1.5 102", "Cooper 1.5 136", "Cooper S 2.0 192", ("Cooper S 2.0 178", {"debut": "2019-07"}),
        "John Cooper Works 2.0 231", ("Cooper D 1.5 116", {"fin": "2020-06"})], portes=2, places=4, reservoir=40,
       remarques="Cabriolet ; restylage 2021 non détaillé")
L += g("Convertible", "F67", "1", "2024-11", None,
       ["Cooper C 1.5 163", "Cooper S 2.0 204", ("John Cooper Works 2.0 231", {"debut": "2025-03"})],
       portes=2, places=4, reservoir=44, remarques="Cabriolet")

# ---------------------------------------------------------------- Clubman
L += g("Clubman", "R55", "1", "2007-11", "2010-02",
       ["One 1.4 95", "Cooper 1.6 120", "Cooper S 1.6 175", "John Cooper Works 1.6 211", "Cooper D 1.6 110"],
       places=4, reservoir=40, remarques="Break 3+1 portes et portes arrière battantes")
L += g("Clubman", "R55", "2", "2010-03", "2014-06",
       ["One 1.6 98", "Cooper 1.6 122", "Cooper S 1.6 184", "John Cooper Works 1.6 211", "One D 1.6 90",
        "Cooper D 1.6 112", ("Cooper SD 2.0 143", {"debut": "2011-03"})], places=4, reservoir=40,
       remarques="Break 3+1 portes et portes arrière battantes ; Clubvan")
L += g("Clubman", "F54", "1", "2015-09", "2019-08",
       ["One 1.5 102", "Cooper 1.5 136", "Cooper S 2.0 192", ("John Cooper Works 2.0 231", {"debut": "2016-09"}),
        "One D 1.5 116", "Cooper D 2.0 150", "Cooper SD 2.0 190"], reservoir=48, remarques="Break 6 portes")
L += g("Clubman", "F54", "2", "2019-09", "2024-02",
       ["One 1.5 102", "Cooper 1.5 136", "Cooper S 2.0 178", "John Cooper Works 2.0 306", "One D 1.5 116",
        "Cooper D 2.0 150", "Cooper SD 2.0 190"], reservoir=48, remarques="Break 6 portes")

# ---------------------------------------------------------------- Countryman / Paceman / Aceman
L += g("Countryman", "R60", "1", "2010-09", "2014-02",
       ["One 1.6 98", "Cooper 1.6 122", "Cooper S 1.6 184", ("John Cooper Works 1.6 218", {"debut": "2012-09"}),
        "One D 1.6 90", "Cooper D 1.6 112", ("Cooper SD 2.0 143", {"debut": "2011-03"})], reservoir=47, remarques="SUV ; ALL4")
L += g("Countryman", "R60", "2", "2014-03", "2016-12",
       ["One 1.6 98", "Cooper 1.6 122", "Cooper S 1.6 190", "John Cooper Works 1.6 218", "One D 1.6 90",
        "Cooper D 2.0 112", "Cooper SD 2.0 143"], reservoir=47, remarques="SUV ; ALL4")
L += g("Countryman", "F60", "1", "2017-02", "2020-05",
       ["One 1.5 102", "Cooper 1.5 136", "Cooper S 2.0 192", ("John Cooper Works 2.0 231", {"fin": "2019-06"}),
        ("John Cooper Works 2.0 306", {"debut": "2019-07"}), ("Cooper SE ALL4 224", {"reservoir": 36, "batterie": 8}),
        "One D 1.5 116", "Cooper D 2.0 150", "Cooper SD 2.0 190"], reservoir=51, remarques="SUV ; ALL4")
L += g("Countryman", "F60", "2", "2020-06", "2024-01",
       ["One 1.5 102", "Cooper 1.5 136", "Cooper S 2.0 178", "John Cooper Works 2.0 306",
        ("Cooper SE ALL4 224", {"reservoir": 36, "batterie": 10}), "One D 1.5 116", "Cooper D 2.0 150",
        "Cooper SD 2.0 190"], reservoir=51, remarques="SUV ; ALL4")
L += g("Countryman", "U25", "1", "2024-02", None,
       ["Countryman C 1.5 170", "Countryman S ALL4 2.0 218", "Countryman JCW ALL4 2.0 300", "Countryman D 2.0 163",
        ("Countryman E 204", el(66)), ("Countryman SE ALL4 313", el(66))], reservoir=54,
       remarques="SUV (base BMW X1 U11)")
L += g("Paceman", "R61", "1", "2013-03", "2016-10",
       ["Cooper 1.6 122", "Cooper S 1.6 184", "John Cooper Works 1.6 218", "Cooper D 1.6 112", "Cooper SD 2.0 143"],
       portes=3, places=4, reservoir=47, remarques="SUV coupé 3 portes ; ALL4")
L += g("Coupé", "R58", "1", "2011-10", "2015-06",
       ["Cooper 1.6 122", "Cooper S 1.6 184", "John Cooper Works 1.6 211", "Cooper SD 2.0 143"], portes=2, places=2,
       reservoir=40, remarques="Coupé 2 places")
L += g("Roadster", "R59", "1", "2012-03", "2015-06",
       ["Cooper 1.6 122", "Cooper S 1.6 184", "John Cooper Works 1.6 211", "Cooper SD 2.0 143"], portes=2, places=2,
       reservoir=40, remarques="Roadster 2 places")
L += g("Aceman", "J05", "1", "2024-11", None,
       [("Aceman E 184", el(43)), ("Aceman SE 218", el(54)), ("Aceman JCW 258", el(54, debut="2025-03"))],
       reservoir=0, remarques="Crossover électrique")

# ---------------------------------------------------------------- Moteurs
D, E_ = "DSL", "ESS"
FAMILLES = {
    # BMC A-Series
    "A-SERIES-0.85": f("ATM", E_, 0.85, "CHAINE", 4, 5500, 2900, "20W50", 4.8, 5000),
    "A-SERIES-1.0": f("ATM", E_, 1.0, "CHAINE", 4, 5500, 3000, "20W50", 4.8, 5000),
    "A-SERIES-1.1": f("ATM", E_, 1.1, "CHAINE", 4, 6000, 4500, "20W50", 4.8, 5000),
    "A-SERIES-1.3": f("ATM", E_, 1.3, "CHAINE", 4, 5800, 3000, "20W50", 4.8, 5000),
    # Tritec (Chrysler-BMW) et Toyota
    "TRITEC-1.4": f("ATM", E_, 1.4, "CHAINE", 4, 5500, 3500, "5W30", 4.2, 25000),
    "TRITEC-1.6": f("ATM", E_, 1.6, "CHAINE", 4, 6000, 4500, "5W30", 4.2, 25000),
    "TRITEC-1.6S": f("TURBO", E_, 1.6, "CHAINE", 4, 6000, 4000, "5W30", 4.2, 25000),
    "1ND-TV": f("TURBO", D, 1.4, "CHAINE", 4, 4000, 2000, "5W30", 4.4, 20000),
    # BMW / PSA « Prince »
    "N12-1.4": f("ATM", E_, 1.4, "CHAINE", 4, 6000, 4000, "5W30", 4.2, 25000),
    "N12-1.6": f("ATM", E_, 1.6, "CHAINE", 4, 6000, 4250, "5W30", 4.2, 25000),
    "N16-1.6": f("ATM", E_, 1.6, "CHAINE", 4, 6000, 4250, "5W30", 4.2, 25000),
    "N14-1.6T": f("TURBO", E_, 1.6, "CHAINE", 4, 5500, 1600, "5W30", 4.2, 25000),
    "N18-1.6T": f("TURBO", E_, 1.6, "CHAINE", 4, 5500, 1600, "5W30", 4.2, 25000),
    "DV6TED4": f("TURBO", D, 1.6, "COURROIE", 4, 4000, 1750, "5W30", 3.75, 20000),
    "N47C16": f("TURBO", D, 1.6, "CHAINE", 4, 4000, 1750, "5W30", 4.5, 25000),
    "N47C20": f("TURBO", D, 2.0, "CHAINE", 4, 4000, 1750, "5W30", 5.2, 25000),
    # BMW modulaires (B3x / B4x)
    "B38A12": f("TURBO", E_, 1.2, "CHAINE", 3, 4400, 1400, "0W20", 4.25, 30000),
    "B38A15": f("TURBO", E_, 1.5, "CHAINE", 3, 4500, 1250, "0W20", 4.25, 30000),
    "B38-PHEV": f("HYB_TE", E_, 1.5, "CHAINE", 3, 4400, 1250, "0W20", 4.25, 30000),
    "B48A20": f("TURBO", E_, 2.0, "CHAINE", 4, 5000, 1350, "0W20", 5.25, 30000),
    "B37C15": f("TURBO", D, 1.5, "CHAINE", 3, 4000, 1750, "0W30", 5.2, 30000),
    "B47C20": f("TURBO", D, 2.0, "CHAINE", 4, 4000, 1750, "0W30", 5.2, 30000),
    # électrique
    "MINI-EV": electrique(), "MINI-J01-EV": electrique(), "MINI-U25-EV": electrique(),
}

TABLE = {
    # Mini classique
    "850 34": ("Mini", "A-SERIES-0.85", 34, 60), "1000 38": ("Mini", "A-SERIES-1.0", 38, 70),
    "1000 40": ("Mini", "A-SERIES-1.0", 40, 69), "1000 42": ("Mini", "A-SERIES-1.0", 42, 78),
    "Cooper 997 55": ("Mini", "A-SERIES-1.0", 55, 73), "Cooper 998 55": ("Mini", "A-SERIES-1.0", 55, 77),
    "Cooper S 1071 70": ("Mini", "A-SERIES-1.1", 70, 84), "Cooper S 1275 76": ("Mini", "A-SERIES-1.3", 76, 108),
    "1275 GT 59": ("Mini", "A-SERIES-1.3", 59, 95), "Cooper 1.3 63": ("Mini", "A-SERIES-1.3", 63, 95),
    "1.3i 50": ("Mini", "A-SERIES-1.3", 50, 88), "1.3i 63": ("Mini", "A-SERIES-1.3", 63, 95),
    # R50 / R52 / R53
    "One 1.4 75": ("Mini", "TRITEC-1.4", 75, 120), "One 1.6 90": ("Mini", "TRITEC-1.6", 90, 140),
    "Cooper 1.6 115": ("Mini", "TRITEC-1.6", 115, 149), "Cooper 1.6 116": ("Mini", "TRITEC-1.6", 116, 150),
    "Cooper S 1.6 163": ("Mini", "TRITEC-1.6S", 163, 210), "Cooper S 1.6 170": ("Mini", "TRITEC-1.6S", 170, 220),
    "John Cooper Works 1.6 200": ("Mini", "TRITEC-1.6S", 200, 240),
    "John Cooper Works 1.6 210": ("Mini", "TRITEC-1.6S", 210, 245),
    "John Cooper Works GP 1.6 218": ("Mini", "TRITEC-1.6S", 218, 250),
    "One D 1.4 75": ("Toyota", "1ND-TV", 75, 180), "One D 1.4 88": ("Toyota", "1ND-TV", 88, 190),
    # R5x
    "One 1.4 75@R56": ("BMW", "N12-1.4", 75, 140), "One 1.4 95": ("BMW", "N12-1.4", 95, 140),
    "Cooper 1.6 120": ("BMW", "N12-1.6", 120, 160), "One 1.6 75": ("BMW", "N16-1.6", 75, 150),
    "One 1.6 98": ("BMW", "N16-1.6", 98, 153), "Cooper 1.6 122": ("BMW", "N16-1.6", 122, 160),
    "Cooper S 1.6 175": ("BMW", "N14-1.6T", 175, 240), "John Cooper Works 1.6 211@N14": ("BMW", "N14-1.6T", 211, 260),
    "Cooper S 1.6 184": ("BMW", "N18-1.6T", 184, 240), "Cooper S 1.6 190": ("BMW", "N18-1.6T", 190, 240),
    "John Cooper Works 1.6 211": ("BMW", "N18-1.6T", 211, 260),
    "John Cooper Works 1.6 218": ("BMW", "N18-1.6T", 218, 280),
    "John Cooper Works GP 1.6 218@R56": ("BMW", "N18-1.6T", 218, 260),
    "Cooper D 1.6 110": ("Peugeot", "DV6TED4", 110, 240),
    "One D 1.6 90": ("BMW", "N47C16", 90, 215), "Cooper D 1.6 112": ("BMW", "N47C16", 112, 270),
    "Cooper D 2.0 112": ("BMW", "N47C20", 112, 270), "Cooper SD 2.0 143": ("BMW", "N47C20", 143, 305),
    # F5x / F6x / U25
    "One 1.2 75": ("BMW", "B38A12", 75, 150), "One 1.2 102": ("BMW", "B38A12", 102, 180),
    "One 1.5 75": ("BMW", "B38A15", 75, 160), "One 1.5 102": ("BMW", "B38A15", 102, 190),
    "Cooper 1.5 136": ("BMW", "B38A15", 136, 220), "Cooper C 1.5 156": ("BMW", "B38A15", 156, 230),
    "Cooper C 1.5 163": ("BMW", "B38A15", 163, 250), "Countryman C 1.5 170": ("BMW", "B38A15", 170, 280),
    "Cooper SE ALL4 224": ("BMW", "B38-PHEV", 224, 385),
    "Cooper S 2.0 178": ("BMW", "B48A20", 178, 280), "Cooper S 2.0 192": ("BMW", "B48A20", 192, 280),
    "Cooper S 2.0 204": ("BMW", "B48A20", 204, 300), "Countryman S ALL4 2.0 218": ("BMW", "B48A20", 218, 360),
    "John Cooper Works 2.0 231": ("BMW", "B48A20", 231, 320), "John Cooper Works 2.0 306": ("BMW", "B48A20", 306, 450),
    "GP 2.0 306": ("BMW", "B48A20", 306, 450), "Countryman JCW ALL4 2.0 300": ("BMW", "B48A20", 300, 400),
    "One D 1.5 95": ("BMW", "B37C15", 95, 220), "One D 1.5 116": ("BMW", "B37C15", 116, 270),
    "Cooper D 1.5 116": ("BMW", "B37C15", 116, 270), "Cooper D 2.0 150": ("BMW", "B47C20", 150, 330),
    "Countryman D 2.0 163": ("BMW", "B47C20", 163, 360), "Cooper SD 2.0 170": ("BMW", "B47C20", 170, 360),
    "Cooper SD 2.0 190": ("BMW", "B47C20", 190, 400),
    # électrique
    "Cooper SE 184": ("BMW", "MINI-EV", 184, 270), "Cooper E 184": ("BMW", "MINI-J01-EV", 184, 290),
    "Cooper SE 218": ("BMW", "MINI-J01-EV", 218, 330), "John Cooper Works E 258": ("BMW", "MINI-J01-EV", 258, 350),
    "Aceman E 184": ("BMW", "MINI-J01-EV", 184, 290), "Aceman SE 218": ("BMW", "MINI-J01-EV", 218, 330),
    "Aceman JCW 258": ("BMW", "MINI-J01-EV", 258, 350),
    "Countryman E 204": ("BMW", "MINI-U25-EV", 204, 250), "Countryman SE ALL4 313": ("BMW", "MINI-U25-EV", 313, 494),
}

# Époques : la R56 phase 1 / R55 / R57 phase 1 (2006-2010) ont le N12 (One 1.4) et le N14 (JCW 211),
# la phase 2 (2010-) le N16/N18 ; la R50 a le Tritec 1.4.
ERES = {("R56", "1"): "N14", ("R57", "1"): "N14", ("R55", "1"): "N14", ("R56", "2"): "R56"}
TABLE["One 1.4 75@N14"] = TABLE.pop("One 1.4 75@R56")
TABLE.pop("John Cooper Works 1.6 211@R56", None)

MOT = Motorisations("Mini", FAMILLES, TABLE, ERES)
MOT.lier(L)

DETAIL = {"Mini": L}
MOTEURS = MOT.moteurs()
