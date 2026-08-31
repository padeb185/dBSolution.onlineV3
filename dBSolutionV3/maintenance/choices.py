from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

class RouesSerrageEtat(models.TextChoices):
    A_FAIRE = "A_FAIRE", _("À faire")
    FAIT = "FAIT", _("Fait")


# ============================================================
# TAUX HORAIRE
# ============================================================

TAUX_HORAIRE_CHOICES = [
    (Decimal("0.00"), _("0,00 €")),
    (Decimal("25.00"), _("25,00 €")),
    (Decimal("30.00"), _("30,00 €")),
    (Decimal("35.00"), _("35,00 €")),
    (Decimal("40.00"), _("40,00 €")),
    (Decimal("45.00"), _("45,00 €")),
    (Decimal("50.00"), _("50,00 €")),
    (Decimal("55.00"), _("55,00 €")),
    (Decimal("60.00"), _("60,00 €")),
    (Decimal("65.00"), _("65,00 €")),
    (Decimal("70.00"), _("70,00 €")),
    (Decimal("75.00"), _("75,00 €")),
    (Decimal("80.00"), _("80,00 €")),
    (Decimal("85.00"), _("85,00 €")),
    (Decimal("90.00"), _("90,00 €")),
    (Decimal("95.00"), _("95,00 €")),
    (Decimal("100.00"), _("100,00 €")),
    (Decimal("105.00"), _("105,00 €")),
    (Decimal("110.00"), _("110,00 €")),
    (Decimal("115.00"), _("115,00 €")),
    (Decimal("120.00"), _("120,00 €")),
    (Decimal("125.00"), _("125,00 €")),
    (Decimal("130.00"), _("130,00 €")),
]



class FabricantLubrifiant(models.TextChoices):
    CASTROL = "CASTROL", _("Castrol")
    MOTUL = "MOTUL", _("Motul")
    MOBIL = "MOBIL", _("Mobil 1")
    SHELL = "SHELL", _("Shell")
    TOTAL = "TOTAL", _("TotalEnergies")
    ELF = "ELF", _("ELF")
    LIQUI_MOLY = "LIQUI_MOLY", _("Liqui Moly")
    FUCHS = "FUCHS", _("Fuchs")
    VALVOLINE = "VALVOLINE", _("Valvoline")
    PENRITE = "PENRITE", _("Penrite")
    RAVENOL = "RAVENOL", _("Ravenol")
    ROWE = "ROWE", _("Rowe")
    ENEOS = "ENEOS", _("ENEOS")
    PETRONAS = "PETRONAS", _("Petronas")
    EUROL = "EUROL", _("Eurol")
    COMMA = "COMMA", _("Comma")
    MANNOL = "MANNOL", _("Mannol")
    YACCO = "YACCO", _("Yacco")
    REDLINE = "REDLINE", _("Red Line")
    AMSOIL = "AMSOIL", _("Amsoil")
    KROON_OIL = "KROON_OIL", _("Kroon-Oil")
    FEBI = "FEBI", _("Febi Bilstein")
    SWAG = "SWAG", _("SWAG")
    PENTOSIN = "PENTOSIN", _("Pentosin")
    ZF = "ZF", _("ZF")
    AISIN = "AISIN", _("Aisin")
    TOYOTA = "TOYOTA", _("Toyota")
    HONDA = "HONDA", _("Honda")
    NISSAN = "NISSAN", _("Nissan")
    MERCEDES = "MERCEDES", _("Mercedes-Benz")
    BMW = "BMW", _("BMW")
    VOLKSWAGEN = "VOLKSWAGEN", _("Volkswagen")
    PORSCHE = "PORSCHE", _("Porsche")
    RENAULT = "RENAULT", _("Renault")
    PSA = "PSA", _("Peugeot / Citroën")
    HYUNDAI_KIA = "HYUNDAI_KIA", _("Hyundai / Kia")
    FORD = "FORD", _("Ford")
    GM = "GM", _("General Motors")
    MOPAR = "MOPAR", _("Mopar")
    AUTRE = "AUTRE", _("Autre")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur")
    CHOISIR = "CHOISIR", _("Choisir")




class FabricantFiltre(models.TextChoices):
    BOSCH = "BOSCH", "Bosch"
    MANN_FILTER = "MANN_FILTER", "MANN-Filter"
    MAHLE = "MAHLE", "Mahle"
    KN = "KN", "KN"
    KNECHT = "KNECHT", "Knecht"
    PURFLUX = "PURFLUX", "Purflux"
    HENGST = "HENGST", "Hengst"
    UFI = "UFI", "UFI"
    FILTRON = "FILTRON", "Filtron"
    FRAM = "FRAM", "Fram"
    CHAMPION = "CHAMPION", "Champion"
    WIX = "WIX", "WIX Filters"
    NIPPARTS = "NIPPARTS", "Nipparts"
    BLUE_PRINT = "BLUE_PRINT", "Blue Print"
    JAPANPARTS = "JAPANPARTS", "Japanparts"
    HERTH_BUSS = "HERTH_BUSS", "Herth+Buss"
    SOFIMA = "SOFIMA", "Sofima"
    MISFAT = "MISFAT", "Misfat"
    FEBI = "FEBI", "Febi Bilstein"
    SWAG = "SWAG", "SWAG"
    SCT = "SCT", "SCT Germany"
    DENCKERMANN = "DENCKERMANN", "Denckermann"
    COMLINE = "COMLINE", "Comline"
    VALEO = "VALEO", "Valeo"
    DELPHI = "DELPHI", "Delphi"
    MEYLE = "MEYLE", "Meyle"
    RIDEX = "RIDEX", "RIDEX"
    TOPRAN = "TOPRAN", "Topran"
    VAICO = "VAICO", "Vaico"
    MAXGEAR = "MAXGEAR", "Maxgear"
    JC_PREMIUM = "JC_PREMIUM", "JC Premium"
    ASHIKA = "ASHIKA", "Ashika"
    ALCO = "ALCO", "ALCO Filters"
    DONALDSON = "DONALDSON", "Donaldson"
    FLEETGUARD = "FLEETGUARD", "Fleetguard"
    BALDWIN = "BALDWIN", "Baldwin Filters"
    COOPERSFIAAM = "COOPERSFIAAM", "CoopersFiaam"
    TECNECO = "TECNECO", "Tecneco"
    OPEN_PARTS = "OPEN_PARTS", "Open Parts"
    AUTRE = "AUTRE", _("Autre")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur")
    CHOISIR = "CHOISIR", _("Choisir")




class AmpouleAutomobile(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    # Halogènes H
    H1 = "H1", _("H1")
    H3 = "H3", _("H3")
    H4 = "H4", _("H4")
    H7 = "H7", _("H7")
    H8 = "H8", _("H8")
    H9 = "H9", _("H9")
    H10 = "H10", _("H10")
    H11 = "H11", _("H11")
    H12 = "H12", _("H12")
    H13 = "H13", _("H13")
    H15 = "H15", _("H15")
    H16 = "H16", _("H16")
    H18 = "H18", _("H18")
    H19 = "H19", _("H19")

    # HB (900x)
    HB1_9004 = "HB1_9004", _("HB1 (9004)")
    HB2_9003 = "HB2_9003", _("HB2 (9003)")
    HB3_9005 = "HB3_9005", _("HB3 (9005)")
    HB4_9006 = "HB4_9006", _("HB4 (9006)")
    HB5_9007 = "HB5_9007", _("HB5 (9007)")

    # Xénon D
    D1S = "D1S", _("D1S")
    D1R = "D1R", _("D1R")
    D2S = "D2S", _("D2S")
    D2R = "D2R", _("D2R")
    D3S = "D3S", _("D3S")
    D3R = "D3R", _("D3R")
    D4S = "D4S", _("D4S")
    D4R = "D4R", _("D4R")
    D5S = "D5S", _("D5S")
    D8S = "D8S", _("D8S")

    # Veilleuses / tableau de bord
    W1_2W = "W1_2W", _("W1.2W")
    W2W = "W2W", _("W2W")
    W3W = "W3W", _("W3W")
    W5W = "W5W", _("W5W")
    WY5W = "WY5W", _("WY5W")

    # Clignotants / stop
    P21W = "P21W", _("P21W")
    PY21W = "PY21W", _("PY21W")
    P21_5W = "P21_5W", _("P21/5W")
    R5W = "R5W", _("R5W")
    R10W = "R10W", _("R10W")

    # Navette
    C5W = "C5W", _("C5W")
    C10W = "C10W", _("C10W")

    # BA
    BA9S = "BA9S", _("BA9S")
    BA15S = "BA15S", _("BA15S")
    BA15D = "BA15D", _("BA15D")
    BAY15D = "BAY15D", _("BAY15D")
    BAU15S = "BAU15S", _("BAU15S")

    # Festoon
    SV7 = "SV7", _("SV7")
    SV8_5 = "SV8_5", _("SV8.5")

    # LED
    LED_H1 = "LED_H1", _("LED H1")
    LED_H4 = "LED_H4", _("LED H4")
    LED_H7 = "LED_H7", _("LED H7")
    LED_H11 = "LED_H11", _("LED H11")
    LED_W5W = "LED_W5W", _("LED W5W")
    LED_P21W = "LED_P21W", _("LED P21W")
    LED_P21_5W = "LED_P21_5W", _("LED P21/5W")

    AUTRE = "AUTRE", _("Autre")





class FabricantPiece(models.TextChoices):
    # Groupe Bosch
    BOSCH = "BOSCH", "Bosch"

    # Filtration
    MANN_FILTER = "MANN_FILTER", "MANN-Filter"
    MAHLE = "MAHLE", "Mahle"
    KNECHT = "KNECHT", "Knecht"
    HENGST = "HENGST", "Hengst"
    PURFLUX = "PURFLUX", "Purflux"
    UFI = "UFI", "UFI"
    FILTRON = "FILTRON", "Filtron"
    FRAM = "FRAM", "Fram"
    WIX = "WIX", "WIX Filters"
    ALCO = "ALCO", "ALCO Filters"
    SOFIMA = "SOFIMA", "Sofima"
    DONALDSON = "DONALDSON", "Donaldson"
    FLEETGUARD = "FLEETGUARD", "Fleetguard"
    BALDWIN = "BALDWIN", "Baldwin"

    # Allumage
    NGK = "NGK", "NGK"
    DENSO = "DENSO", "Denso"
    BERU = "BERU", "Beru"
    CHAMPION = "CHAMPION", "Champion"

    # Embrayage / Transmission
    LUK = "LUK", "LuK"
    SACHS = "SACHS", "Sachs"
    VALEO = "VALEO", "Valeo"
    AISIN = "AISIN", "Aisin"

    # Freinage
    BREMBO = "BREMBO", "Brembo"
    ATE = "ATE", "ATE"
    TEXTAR = "TEXTAR", "Textar"
    FERODO = "FERODO", "Ferodo"
    TRW = "TRW", "TRW"
    JURID = "JURID", "Jurid"
    PAGID = "PAGID", "Pagid"
    REMSA = "REMSA", "Remsa"

    # Suspension / Direction
    LEMFORDER = "LEMFORDER", "Lemförder"
    MEYLE = "MEYLE", "Meyle"
    FEBI_BILSTEIN = "FEBI_BILSTEIN", "Febi Bilstein"
    SWAG = "SWAG", "SWAG"
    MOOG = "MOOG", "Moog"
    SIDEM = "SIDEM", "Sidem"
    DELPHI = "DELPHI", "Delphi"

    # Roulements
    SKF = "SKF", "SKF"
    FAG = "FAG", "FAG"
    TIMKEN = "TIMKEN", "Timken"
    NSK = "NSK", "NSK"
    KOYO = "KOYO", "Koyo"
    NTN = "NTN", "NTN"
    SNR = "SNR", "SNR"

    # Courroies / Distribution
    CONTINENTAL = "CONTINENTAL", "Continental"
    GATES = "GATES", "Gates"
    DAYCO = "DAYCO", "Dayco"

    # Refroidissement
    BEHR = "BEHR", "Behr"
    HELLA = "HELLA", "Hella"
    NRF = "NRF", "NRF"

    # Électricité
    VARTA = "VARTA", "Varta"
    EXIDE = "EXIDE", "Exide"
    YUASA = "YUASA", "Yuasa"

    # Éclairage
    OSRAM = "OSRAM", "Osram"
    PHILIPS = "PHILIPS", "Philips"

    # Echappement / Capteurs
    WALKER = "WALKER", "Walker"
    PIERBURG = "PIERBURG", "Pierburg"
    VDO = "VDO", "VDO"

    # Constructeurs
    BMW = "BMW", "BMW"
    MERCEDES = "MERCEDES", "Mercedes-Benz"
    AUDI = "AUDI", "Audi"
    VOLKSWAGEN = "VOLKSWAGEN", "Volkswagen"
    PORSCHE = "PORSCHE", "Porsche"
    OPEL = "OPEL", "Opel"
    FORD = "FORD", "Ford"
    RENAULT = "RENAULT", "Renault"
    PEUGEOT = "PEUGEOT", "Peugeot"
    CITROEN = "CITROEN", "Citroën"
    TOYOTA = "TOYOTA", "Toyota"
    HONDA = "HONDA", "Honda"
    NISSAN = "NISSAN", "Nissan"
    HYUNDAI = "HYUNDAI", "Hyundai"
    KIA = "KIA", "Kia"

    # Aftermarket
    HERTH_BUSS = "HERTH_BUSS", "Herth+Buss"
    JAPANPARTS = "JAPANPARTS", "Japanparts"
    BLUE_PRINT = "BLUE_PRINT", "Blue Print"
    NIPPARTS = "NIPPARTS", "Nipparts"
    COMLINE = "COMLINE", "Comline"
    DENCKERMANN = "DENCKERMANN", "Denckermann"
    VAICO = "VAICO", "Vaico"
    TOPRAN = "TOPRAN", "Topran"
    RIDEX = "RIDEX", "RIDEX"
    MAXGEAR = "MAXGEAR", "Maxgear"
    JC_PREMIUM = "JC_PREMIUM", "JC Premium"
    ASHIKA = "ASHIKA", "Ashika"
    OPEN_PARTS = "OPEN_PARTS", "Open Parts"

    AUTRE = "AUTRE", _("Autre")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur")
    CHOISIR = "CHOISIR", _("Choisir")


class TypeHuileDirection(models.TextChoices):
    ATF_DEXRON_II = "ATF_DEXRON_II", _("ATF Dexron II")
    ATF_DEXRON_III = "ATF_DEXRON_III", _("ATF Dexron III")
    ATF_DEXRON_VI = "ATF_DEXRON_VI", _("ATF Dexron VI")
    CHF_7_1 = "CHF_7_1", _("CHF 7.1")
    CHF_11S = "CHF_11S", _("CHF 11S")
    CHF_202 = "CHF_202", _("CHF 202")
    LDS = "LDS", _("LDS")
    LHM = "LHM", _("LHM")
    PSF = "PSF", _("PSF")
    PSF_3 = "PSF_3", _("PSF-3")
    PSF_4 = "PSF_4", _("PSF-4")
    MB_236_3 = "MB_236_3", _("Mercedes-Benz 236.3")
    MB_345_0 = "MB_345_0", _("Mercedes-Benz 345.0")
    VW_G002000 = "VW_G002000", _("Volkswagen G 002 000")
    VW_G004000 = "VW_G004000", _("Volkswagen G 004 000")
    BMW_ATF = "BMW_ATF", _("BMW ATF")
    BMW_CHF = "BMW_CHF", _("BMW CHF")
    HONDA_PSF = "HONDA_PSF", _("Honda PSF")
    TOYOTA_PSF = "TOYOTA_PSF", _("Toyota PSF")
    MINERALE = "MINERALE", _("Huile minérale")
    SEMI_SYNTHETIQUE = "SEMI_SYNTHETIQUE", _("Huile semi-synthétique")
    SYNTHETIQUE = "SYNTHETIQUE", _("Huile synthétique")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Spécification constructeur")
    AUTRE = "AUTRE", _("Autre")
    CHOISIR = "CHOISIR", _("Choisir")





class FabricantFrein(models.TextChoices):
    ATE = "ATE", _("ATE")
    BREMBO = "BREMBO", _("Brembo")
    BOSCH = "BOSCH", _("Bosch")
    TRW = "TRW", _("TRW")
    FERODO = "FERODO", _("Ferodo")
    TEXTAR = "TEXTAR", _("Textar")
    PAGID = "PAGID", _("Pagid")
    JURID = "JURID", _("Jurid")
    DELPHI = "DELPHI", _("Delphi")
    VALEO = "VALEO", _("Valeo")
    HELLA = "HELLA", _("Hella")
    HELLA_PAGID = "HELLA_PAGID", _("Hella Pagid")
    ZIMMERMANN = "ZIMMERMANN", _("Zimmermann")
    MEYLE = "MEYLE", _("Meyle")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    NIPPARTS = "NIPPARTS", _("Nipparts")
    MINTEX = "MINTEX", _("Mintex")
    ROADHOUSE = "ROADHOUSE", _("Roadhouse")
    REMSA = "REMSA", _("Remsa")
    ICER = "ICER", _("ICER")
    EBC = "EBC", _("EBC Brakes")
    STOPTECH = "STOPTECH", _("StopTech")
    AKEBONO = "AKEBONO", _("Akebono")
    ADVICS = "ADVICS", _("Advics")
    NISSHINBO = "NISSHINBO", _("Nisshinbo")
    BENDIX = "BENDIX", _("Bendix")
    COMLINE = "COMLINE", _("Comline")
    FEBI = "FEBI", _("Febi Bilstein")
    SWAG = "SWAG", _("SWAG")
    MAPCO = "MAPCO", _("Mapco")
    NK = "NK", _("NK")
    JAPANPARTS = "JAPANPARTS", _("Japanparts")
    HERTH_BUSS = "HERTH_BUSS", _("Herth+Buss")
    DON = "DON", _("DON")
    TOMEX = "TOMEX", _("Tomex")
    LPR = "LPR", _("LPR")
    CIFAM = "CIFAM", _("Cifam")
    METELLI = "METELLI", _("Metelli")
    QUINTON_HAZELL = "QUINTON_HAZELL", _("Quinton Hazell")
    SKF = "SKF", _("SKF")
    SNR = "SNR", _("SNR")
    WINMAX = "WINMAX", _("Winmax")
    DIXCEL = "DIXCEL", _("Dixcel")
    AUTRE = "AUTRE", _("Autre")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur")
    CHOISIR = "CHOISIR", _("Choisir")





class RefroidissementFabricant(models.TextChoices):
    ABRO = "ABRO", _("ABRO")
    AISIN = "AISIN", _("AISIN")
    ARECA = "ARECA", _("Areca")
    BARDAHL = "BARDAHL", _("Bardahl")
    BASF_GLYSANTIN = "BASF_GLYSANTIN", _("BASF Glysantin")
    BEL_RAY = "BEL_RAY", _("Bel-Ray")
    BIZOL = "BIZOL", _("BIZOL")
    BMW = "BMW", _("BMW")
    BOLK = "BOLK", _("BOLK")
    BOSCH = "BOSCH", _("Bosch")
    CASTROL = "CASTROL", _("Castrol")
    CHAMPION = "CHAMPION", _("Champion")
    COMMA = "COMMA", _("Comma")
    ELF = "ELF", _("ELF")
    EUROL = "EUROL", _("Eurol")
    FEBI_BILSTEIN = "FEBI_BILSTEIN", _("Febi Bilstein")
    FUCHS = "FUCHS", _("Fuchs")
    GATES = "GATES", _("Gates")
    GENERAL_MOTORS = "GENERAL_MOTORS", _("General Motors")
    HEPU = "HEPU", _("HEPU")
    HOLTS = "HOLTS", _("Holts")
    HONDA = "HONDA", _("Honda")
    HYUNDAI = "HYUNDAI", _("Hyundai")
    IGOL = "IGOL", _("Igol")
    IPONE = "IPONE", _("IPONE")
    K2 = "K2", _("K2")
    KIA = "KIA", _("Kia")
    LIQUI_MOLY = "LIQUI_MOLY", _("Liqui Moly")
    MANNOL = "MANNOL", _("Mannol")
    MAZDA = "MAZDA", _("Mazda")
    MERCEDES_BENZ = "MERCEDES_BENZ", _("Mercedes-Benz")
    MEYLE = "MEYLE", _("Meyle")
    MILLERS_OILS = "MILLERS_OILS", _("Millers Oils")
    MITSUBISHI = "MITSUBISHI", _("Mitsubishi")
    MOBIL = "MOBIL", _("Mobil")
    MOPAR = "MOPAR", _("Mopar")
    MOTIP = "MOTIP", _("Motip")
    MOTOREX = "MOTOREX", _("Motorex")
    MOTUL = "MOTUL", _("Motul")
    NISSAN = "NISSAN", _("Nissan")
    OPEL = "OPEL", _("Opel")
    ORLEN = "ORLEN", _("Orlen")
    PEMCO = "PEMCO", _("Pemco")
    PEUGEOT_CITROEN = "PEUGEOT_CITROEN", _("Peugeot Citroën")
    PETRONAS = "PETRONAS", _("Petronas")
    PORSCHE = "PORSCHE", _("Porsche")
    PRESTONE = "PRESTONE", _("Prestone")
    PUTOLINE = "PUTOLINE", _("Putoline")
    RAVENOL = "RAVENOL", _("Ravenol")
    REPSOL = "REPSOL", _("Repsol")
    RENAULT = "RENAULT", _("Renault")
    ROWE = "ROWE", _("ROWE")
    SHELL = "SHELL", _("Shell")
    SONAX = "SONAX", _("Sonax")
    SUBARU = "SUBARU", _("Subaru")
    SUZUKI = "SUZUKI", _("Suzuki")
    SWAG = "SWAG", _("SWAG")
    TEXACO = "TEXACO", _("Texaco")
    TOTALENERGIES = "TOTALENERGIES", _("TotalEnergies")
    TOYOTA = "TOYOTA", _("Toyota")
    TRIPLE_QX = "TRIPLE_QX", _("Triple QX")
    VALEO = "VALEO", _("Valeo")
    VALVOLINE = "VALVOLINE", _("Valvoline")
    VAG = "VAG", _("VAG")
    VOLVO = "VOLVO", _("Volvo")
    WOLF = "WOLF", _("Wolf")
    XENUM = "XENUM", _("Xenum")
    YACCO = "YACCO", _("Yacco")
    YAMAHA = "YAMAHA", _("Yamaha")
    AUTRE = "AUTRE", _("Autre")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur")
    CHOISIR = "CHOISIR", _("Choisir")





class FabricantSuspension(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir un fabricant")

    AC_DELCO = "AC_DELCO", _("ACDelco")
    AIR_LIFT = "AIR_LIFT", _("Air Lift")
    AL_KO = "AL_KO", _("AL-KO")
    AP_SPORTFAHRWERKE = "AP_SPORTFAHRWERKE", _("AP Sportfahrwerke")
    ARN_NOTT = "ARNOTT", _("Arnott")
    BILSTEIN = "BILSTEIN", _("Bilstein")
    BOGE = "BOGE", _("Boge")
    BOSCH = "BOSCH", _("Bosch")
    BC_RACING = "BC_RACING", _("BC Racing")
    COBRA = "COBRA", _("Cobra Suspension")
    DELPHI = "DELPHI", _("Delphi")
    EIBACH = "EIBACH", _("Eibach")
    FEBEST = "FEBEST", _("Febest")
    FEBI_BILSTEIN = "FEBI_BILSTEIN", _("Febi Bilstein")
    GABRIEL = "GABRIEL", _("Gabriel")
    H_AND_R = "H_AND_R", _("H&R")
    JAPANPARTS = "JAPANPARTS", _("Japanparts")
    JAPKO = "JAPKO", _("Japko")
    JOM = "JOM", _("JOM")
    KAYABA = "KAYABA", _("KYB")
    K_W = "K_W", _("KW Suspensions")
    KONI = "KONI", _("Koni")
    LEMFORDER = "LEMFORDER", _("Lemförder")
    LESJOFORS = "LESJOFORS", _("Lesjöfors")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    MAPCO = "MAPCO", _("Mapco")
    MAXGEAR = "MAXGEAR", _("Maxgear")
    MEYLE = "MEYLE", _("Meyle")
    MONROE = "MONROE", _("Monroe")
    MOOG = "MOOG", _("Moog")
    NIPPARTS = "NIPPARTS", _("Nipparts")
    NK = "NK", _("NK")
    OPTIMAL = "OPTIMAL", _("Optimal")
    OROPARTS = "OROPARTS", _("Oro Parts")
    PROFIT = "PROFIT", _("Profit")
    QUINTON_HAZELL = "QUINTON_HAZELL", _("Quinton Hazell")
    RIDEX = "RIDEX", _("Ridex")
    SACHS = "SACHS", _("Sachs")
    SNR = "SNR", _("SNR")
    SPIDAN = "SPIDAN", _("Spidan")
    ST_SUSPENSIONS = "ST_SUSPENSIONS", _("ST Suspensions")
    SWAG = "SWAG", _("SWAG")
    TA_TECHNIX = "TA_TECHNIX", _("TA Technix")
    TEIN = "TEIN", _("Tein")
    TRW = "TRW", _("TRW")
    VOGTLAND = "VOGTLAND", _("Vogtland")
    WEITEC = "WEITEC", _("Weitec")
    XYZ_RACING = "XYZ_RACING", _("XYZ Racing")
    ZF = "ZF", _("ZF")

    BMW = "BMW", _("BMW")
    MERCEDES_BENZ = "MERCEDES_BENZ", _("Mercedes-Benz")
    PORSCHE = "PORSCHE", _("Porsche")
    RENAULT = "RENAULT", _("Renault")
    STELLANTIS = "STELLANTIS", _("Stellantis")
    TOYOTA = "TOYOTA", _("Toyota")
    VAG = "VAG", _("Volkswagen Audi Group")
    VOLVO = "VOLVO", _("Volvo")

    AUTRE = "AUTRE", _("Autre")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur")



class FabricantRoulement(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir un fabricant")

    AIC = "AIC", _("AIC")
    ASHIKA = "ASHIKA", _("Ashika")
    AUTEX = "AUTEX", _("Autex")
    BENDIX = "BENDIX", _("Bendix")
    BGA = "BGA", _("BGA")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    BORG_AND_BECK = "BORG_AND_BECK", _("Borg & Beck")
    BTA = "BTA", _("BTA")
    CORTECO = "CORTECO", _("Corteco")
    DAYCO = "DAYCO", _("Dayco")
    DELPHI = "DELPHI", _("Delphi")
    FAG = "FAG", _("FAG")
    FEBEST = "FEBEST", _("Febest")
    FEBI_BILSTEIN = "FEBI_BILSTEIN", _("Febi Bilstein")
    FLENNOR = "FLENNOR", _("Flennor")
    GSP = "GSP", _("GSP")
    HERTH_BUSS = "HERTH_BUSS", _("Herth+Buss")
    INA = "INA", _("INA")
    JAPANPARTS = "JAPANPARTS", _("Japanparts")
    JAPKO = "JAPKO", _("Japko")
    JP_GROUP = "JP_GROUP", _("JP Group")
    KAMOKA = "KAMOKA", _("Kamoka")
    KAVO_PARTS = "KAVO_PARTS", _("Kavo Parts")
    KOYO = "KOYO", _("Koyo")
    LPR = "LPR", _("LPR")
    MAPCO = "MAPCO", _("Mapco")
    MAXGEAR = "MAXGEAR", _("Maxgear")
    METELLI = "METELLI", _("Metelli")
    MEYLE = "MEYLE", _("Meyle")
    MOOG = "MOOG", _("Moog")
    NATIONAL = "NATIONAL", _("National")
    NIPPARTS = "NIPPARTS", _("Nipparts")
    NK = "NK", _("NK")
    NTN = "NTN", _("NTN")
    OPTIMAL = "OPTIMAL", _("Optimal")
    PEX = "PEX", _("PEX")
    QUINTON_HAZELL = "QUINTON_HAZELL", _("Quinton Hazell")
    RIDEX = "RIDEX", _("Ridex")
    RUVILLE = "RUVILLE", _("Ruville")
    SKF = "SKF", _("SKF")
    SNR = "SNR", _("SNR")
    SPIDAN = "SPIDAN", _("Spidan")
    SWAG = "SWAG", _("SWAG")
    TIMKEN = "TIMKEN", _("Timken")
    TOPRAN = "TOPRAN", _("Topran")
    TRISCAN = "TRISCAN", _("Triscan")
    TRW = "TRW", _("TRW")
    VAICO = "VAICO", _("Vaico")
    VKBA = "VKBA", _("SKF VKBA")
    WHEELPRO = "WHEELPRO", _("WheelPro")
    ZF = "ZF", _("ZF")

    BMW = "BMW", _("BMW")
    FORD = "FORD", _("Ford")
    GENERAL_MOTORS = "GENERAL_MOTORS", _("General Motors")
    HONDA = "HONDA", _("Honda")
    HYUNDAI = "HYUNDAI", _("Hyundai")
    KIA = "KIA", _("Kia")
    MAZDA = "MAZDA", _("Mazda")
    MERCEDES_BENZ = "MERCEDES_BENZ", _("Mercedes-Benz")
    MITSUBISHI = "MITSUBISHI", _("Mitsubishi")
    NISSAN = "NISSAN", _("Nissan")
    PORSCHE = "PORSCHE", _("Porsche")
    RENAULT = "RENAULT", _("Renault")
    STELLANTIS = "STELLANTIS", _("Stellantis")
    SUBARU = "SUBARU", _("Subaru")
    SUZUKI = "SUZUKI", _("Suzuki")
    TOYOTA = "TOYOTA", _("Toyota")
    VAG = "VAG", _("Volkswagen Audi Group")
    VOLVO = "VOLVO", _("Volvo")

    AUTRE = "AUTRE", _("Autre")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur")





class FabricantPneus(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir un fabricant")

    ACHILLES = "ACHILLES", _("Achilles")
    APOLLO = "APOLLO", _("Apollo")
    ARMSTRONG = "ARMSTRONG", _("Armstrong")
    ATTURO = "ATTURO", _("Atturo")
    AUSTONE = "AUSTONE", _("Austone")
    AVON = "AVON", _("Avon")
    BARUM = "BARUM", _("Barum")
    BFGOODRICH = "BFGOODRICH", _("BFGoodrich")
    BRIDGESTONE = "BRIDGESTONE", _("Bridgestone")
    CEAT = "CEAT", _("CEAT")
    CHAOYANG = "CHAOYANG", _("Chaoyang")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    COOPER = "COOPER", _("Cooper")
    CORDIANT = "CORDIANT", _("Cordiant")
    CST = "CST", _("CST")
    DAVANTI = "DAVANTI", _("Davanti")
    DAYTON = "DAYTON", _("Dayton")
    DEBICA = "DEBICA", _("Dębica")
    DOUBLE_COIN = "DOUBLE_COIN", _("Double Coin")
    DUNLOP = "DUNLOP", _("Dunlop")
    DURATURN = "DURATURN", _("Duraturn")
    EP_TYRES = "EP_TYRES", _("EP Tyres")
    EVENT = "EVENT", _("Event")
    FALKEN = "FALKEN", _("Falken")
    FEDERAL = "FEDERAL", _("Federal")
    FIREMAX = "FIREMAX", _("Firemax")
    FIRESTONE = "FIRESTONE", _("Firestone")
    FORTUNA = "FORTUNA", _("Fortuna")
    FULDA = "FULDA", _("Fulda")
    GENERAL_TIRE = "GENERAL_TIRE", _("General Tire")
    GITI = "GITI", _("Giti")
    GISLAVED = "GISLAVED", _("Gislaved")
    GOFORM = "GOFORM", _("Goform")
    GOODYEAR = "GOODYEAR", _("Goodyear")
    GRENLANDER = "GRENLANDER", _("Grenlander")
    GT_RADIAL = "GT_RADIAL", _("GT Radial")
    HANKOOK = "HANKOOK", _("Hankook")
    HAIDA = "HAIDA", _("Haida")
    HIFLY = "HIFLY", _("Hifly")
    INFINITY = "INFINITY", _("Infinity")
    KELLY = "KELLY", _("Kelly")
    KENDA = "KENDA", _("Kenda")
    KETER = "KETER", _("Keter")
    KLEBER = "KLEBER", _("Kleber")
    KORMORAN = "KORMORAN", _("Kormoran")
    KUMHO = "KUMHO", _("Kumho")
    LANDSAIL = "LANDSAIL", _("Landsail")
    LAUFENN = "LAUFENN", _("Laufenn")
    LEXANI = "LEXANI", _("Lexani")
    LINGLONG = "LINGLONG", _("Linglong")
    MARSHAL = "MARSHAL", _("Marshal")
    MATADOR = "MATADOR", _("Matador")
    MAXXIS = "MAXXIS", _("Maxxis")
    MICHELIN = "MICHELIN", _("Michelin")
    MILESTONE = "MILESTONE", _("Milestone")
    MINERVA = "MINERVA", _("Minerva")
    MITAS = "MITAS", _("Mitas")
    MOMO = "MOMO", _("MOMO")
    NANKANG = "NANKANG", _("Nankang")
    NEXEN = "NEXEN", _("Nexen")
    NOKIAN = "NOKIAN", _("Nokian Tyres")
    NORDEXX = "NORDEXX", _("Nordexx")
    OVATION = "OVATION", _("Ovation")
    PETLAS = "PETLAS", _("Petlas")
    PIRELLI = "PIRELLI", _("Pirelli")
    POWERTRAC = "POWERTRAC", _("Powertrac")
    PREMIORRI = "PREMIORRI", _("Premiorri")
    RADAR = "RADAR", _("Radar")
    RAPID = "RAPID", _("Rapid")
    RIKEN = "RIKEN", _("Riken")
    ROADSTONE = "ROADSTONE", _("Roadstone")
    ROCKBLADE = "ROCKBLADE", _("Rockblade")
    ROTALLA = "ROTALLA", _("Rotalla")
    SAILUN = "SAILUN", _("Sailun")
    SEMPERIT = "SEMPERIT", _("Semperit")
    SAVA = "SAVA", _("Sava")
    STAR_PERFORMER = "STAR_PERFORMER", _("Star Performer")
    SUMITOMO = "SUMITOMO", _("Sumitomo")
    SUNNY = "SUNNY", _("Sunny")
    TOYO = "TOYO", _("Toyo")
    TRIANGLE = "TRIANGLE", _("Triangle")
    TRISTAR = "TRISTAR", _("Tristar")
    TUNGA = "TUNGA", _("Tunga")
    UNIROYAL = "UNIROYAL", _("Uniroyal")
    VIKING = "VIKING", _("Viking")
    VREDESTEIN = "VREDESTEIN", _("Vredestein")
    WANLI = "WANLI", _("Wanli")
    WESTLAKE = "WESTLAKE", _("Westlake")
    WINDFORCE = "WINDFORCE", _("Windforce")
    YOKOHAMA = "YOKOHAMA", _("Yokohama")
    ZEETEX = "ZEETEX", _("Zeetex")

    AUTRE = "AUTRE", _("Autre")





class FabricantBougies(models.TextChoices):
    NGK = "NGK", _("NGK")
    DENSO = "DENSO", _("DENSO")
    BOSCH = "BOSCH", _("Bosch")
    CHAMPION = "CHAMPION", _("Champion")
    BERU = "BERU", _("Beru")
    EYQUEM = "EYQUEM", _("Eyquem")
    VALEO = "VALEO", _("Valeo")
    FEBI = "FEBI", _("Febi Bilstein")
    HELLA = "HELLA", _("Hella")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    DELPHI = "DELPHI", _("Delphi")
    BORGWARNER = "BORGWARNER", _("BorgWarner")
    MOTORCRAFT = "MOTORCRAFT", _("Motorcraft")
    ACDELCO = "ACDELCO", _("ACDelco")
    MOPAR = "MOPAR", _("Mopar")
    PIERBURG = "PIERBURG", _("Pierburg")
    RIDEX = "RIDEX", _("RIDEX")
    JAPANPARTS = "JAPANPARTS", _("Japanparts")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    NPS = "NPS", _("NPS")
    AUTOLITE = "AUTOLITE", _("Autolite")
    BRISK = "BRISK", _("Brisk")
    CHOISIR = "CHOISIR", _("Choisir")






class MatiereFrein(models.TextChoices):
    ACIER = 'ACIER', _("Acier")
    CARBONE = 'CARBONE', _("Carbone")
    CERAMIQUE = 'CERAMIQUE', _("Céramique")
    COMPOSITE = 'COMPOSITE', _("Composite")
    CHOISIR = "CHOISIR", _("Choisir")



class MatierePlaquetteFrein(models.TextChoices):
    ORGANIC = 'ORGANIC', _("Organique (NAO)")
    LOW_METALLIC = 'LOW_METALLIC', _("Semi-métallique")
    METALLIC = 'METALLIC', _("Métallique")
    CERAMIC = 'CERAMIC', _("Céramique haute performance")
    CHOISIR = "CHOISIR", _("Choisir")


class TypeDisqueFrein(models.TextChoices):
    MONOBLOC_PLEIN = 'MONOBLOC_PLEIN', _("Plein (monobloc)")
    VENTILE = 'VENTILE', _("Ventilé")
    RAINURE = 'RAINURE', _("Rainuré")
    PERCE = 'PERCE', _("Percé")
    RAINURE_PERCE = 'RAINURE_PERCE', _("Rainuré et percé")
    CHOISIR = "CHOISIR", _("Choisir")


class FabricantBatterie(models.TextChoices):
    BOSCH = "BOSCH", _("Bosch")
    VARTA = "VARTA", _("Varta")
    EXIDE = "EXIDE", _("Exide")
    YUASA = "YUASA", _("Yuasa")
    BANNER = "BANNER", _("Banner")
    FIAMM = "FIAMM", _("Fiamm")
    TUDOR = "TUDOR", _("Tudor")
    FULMEN = "FULMEN", _("Fulmen")
    CENTRA = "CENTRA", _("Centra")
    HANKOOK = "HANKOOK", _("Hankook")
    MUTLU = "MUTLU", _("Mutlu")
    TAB = "TAB", _("TAB")
    TOPLA = "TOPLA", _("Topla")
    ODYSSEY = "ODYSSEY", _("Odyssey")
    OPTIMA = "OPTIMA", _("Optima")
    INTERSTATE = "INTERSTATE", _("Interstate")
    ACDELCO = "ACDELCO", _("ACDelco")
    MOLL = "MOLL", _("Moll")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    AUTRE = "AUTRE", _("Autre")
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur")



class FabricantEchappement(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")

    AKRAPOVIC = "AKRAPOVIC", _("Akrapovič")
    REMUS = "REMUS", _("Remus")
    SUPERSPRINT = "SUPERSPRINT", _("Supersprint")
    MILLTEK = "MILLTEK", _("Milltek Sport")
    MAGNAFLOW = "MAGNAFLOW", _("MagnaFlow")
    BORLA = "BORLA", _("Borla")
    EISENMANN = "EISENMANN", _("Eisenmann")
    FOX = "FOX", _("FOX")
    BASTUCK = "BASTUCK", _("Bastuck")
    RAGAZZON = "RAGAZZON", _("Ragazzon")
    SCORPION = "SCORPION", _("Scorpion")
    COBRA = "COBRA", _("Cobra Sport")
    MIVV = "MIVV", _("MIVV")
    ARROW = "ARROW", _("Arrow")
    BOSAL = "BOSAL", _("Bosal")
    WALKER = "WALKER", _("Walker")
    EBERSPACHER = "EBERSPACHER", _("Eberspächer")
    IMASAF = "IMASAF", _("IMASAF")
    ERNST = "ERNST", _("Ernst")
    POLMO = "POLMO", _("Polmo")
    BMW = "BMW", _("BMW")
    PORSCHE = "PORSCHE", _("Porsche")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur")


    AUTRE = "AUTRE", _("Autre")




class FabricantCapteurEchappement(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")

    BOSCH = "BOSCH", _("Bosch")
    DENSO = "DENSO", _("Denso")
    NGK = "NGK", _("NGK / NTK")
    DELPHI = "DELPHI", _("Delphi")
    HELLA = "HELLA", _("Hella")
    VDO = "VDO", _("VDO")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    PIERBURG = "PIERBURG", _("Pierburg")
    FACET = "FACET", _("Facet")
    FEBI = "FEBI", _("Febi Bilstein")
    MEYLE = "MEYLE", _("Meyle")
    VEMO = "VEMO", _("Vemo")
    ERA = "ERA", _("ERA")
    FAE = "FAE", _("FAE")
    EPS = "EPS", _("EPS")
    RIDEX = "RIDEX", _("Ridex")
    STARK = "STARK", _("Stark")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    HITACHI = "HITACHI", _("Hitachi")
    VALEO = "VALEO", _("Valeo")
    WALKER = "WALKER", _("Walker Products")
    SIDAT = "SIDAT", _("SIDAT")
    METZGER = "METZGER", _("Metzger")
    TOPRAN = "TOPRAN", _("Topran")

    OEM = "OEM", _("Origine constructeur (OEM)")
    AUTRE = "AUTRE", _("Autre")



class FabricantSilentBloc(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")

    LEMFORDER = "LEMFORDER", _("Lemförder")
    FEBI = "FEBI", _("Febi Bilstein")
    MEYLE = "MEYLE", _("Meyle")
    TRW = "TRW", _("TRW")
    MOOG = "MOOG", _("Moog")
    SACHS = "SACHS", _("Sachs")
    SKF = "SKF", _("SKF")
    SNR = "SNR", _("SNR")
    DELPHI = "DELPHI", _("Delphi")
    SIDEM = "SIDEM", _("Sidem")
    CORTECO = "CORTECO", _("Corteco")
    SWAG = "SWAG", _("SWAG")
    VAICO = "VAICO", _("Vaico")
    MAPCO = "MAPCO", _("Mapco")
    OPTIMAL = "OPTIMAL", _("Optimal")
    BIRTH = "BIRTH", _("Birth")
    SASIC = "SASIC", _("Sasic")
    METZGER = "METZGER", _("Metzger")
    TOPRAN = "TOPRAN", _("Topran")
    RIDEX = "RIDEX", _("Ridex")
    STARK = "STARK", _("Stark")

    POWERFLEX = "POWERFLEX", _("Powerflex")
    SUPERPRO = "SUPERPRO", _("SuperPro")
    STRONGFLEX = "STRONGFLEX", _("Strongflex")

    OEM = "OEM", _("Origine constructeur (OEM)")
    AUTRE = "AUTRE", _("Autre")



class CourroieDistributionFabricant(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")

    CONTINENTAL = "CONTINENTAL", _("Continental / ContiTech")
    GATES = "GATES", _("Gates")
    DAYCO = "DAYCO", _("Dayco")
    BOSCH = "BOSCH", _("Bosch")
    SKF = "SKF", _("SKF")
    INA = "INA", _("INA")
    SNR = "SNR", _("SNR")
    HUTCHINSON = "HUTCHINSON", _("Hutchinson")
    OPTIBELT = "OPTIBELT", _("Optibelt")
    MEYLE = "MEYLE", _("Meyle")
    FEBI = "FEBI", _("Febi Bilstein")
    SWAG = "SWAG", _("SWAG")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    METELLI = "METELLI", _("Metelli")
    HEPU = "HEPU", _("HEPU")
    GRAF = "GRAF", _("GRAF")
    DOLZ = "DOLZ", _("DOLZ")
    QUINTON_HAZELL = "QUINTON_HAZELL", _("Quinton Hazell")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")

    ORIGINE = "ORIGINE", _("Pièce d'origine / OEM")
    AUTRE = "AUTRE", _("Autre")




class FabricantTurbo(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")

    GARRETT = "GARRETT", _("Garrett")
    BORGWARNER = "BORGWARNER", _("BorgWarner")
    KKK = "KKK", _("KKK")
    SCHWITZER = "SCHWITZER", _("Schwitzer")

    MITSUBISHI = "MITSUBISHI", _("Mitsubishi")
    MHI = "MHI", _("Mitsubishi Heavy Industries (MHI)")
    IHI = "IHI", _("IHI")

    HOLSET = "HOLSET", _("Holset")
    CUMMINS = "CUMMINS", _("Cummins Turbo Technologies")

    CONTINENTAL = "CONTINENTAL", _("Continental")
    MAHLE = "MAHLE", _("MAHLE")
    BOSCH_MAHLE = "BOSCH_MAHLE", _("Bosch Mahle Turbo Systems")

    HITACHI = "HITACHI", _("Hitachi")
    TOYOTA = "TOYOTA", _("Toyota")
    AISIN = "AISIN", _("Aisin")

    HONEYWELL = "HONEYWELL", _("Honeywell")
    ROTOMASTER = "ROTOMASTER", _("Rotomaster")

    TURBO_TECHNICS = "TURBO_TECHNICS", _("Turbo Technics")
    TURBOSMART = "TURBOSMART", _("Turbosmart")
    TURBONETICS = "TURBONETICS", _("Turbonetics")
    PRECISION = "PRECISION", _("Precision Turbo & Engine")
    COMP_TURBO = "COMP_TURBO", _("Comp Turbo")
    TIAL = "TIAL", _("TiAL Sport")

    TTE = "TTE", _("The Turbo Engineers (TTE)")
    LOBA = "LOBA", _("LOBA Motorsport")
    WEISTEC = "WEISTEC", _("Weistec")
    PURE_TURBOS = "PURE_TURBOS", _("Pure Turbos")

    MELETT = "MELETT", _("Melett")
    JRONE = "JRONE", _("JRone")
    SL_TURBO = "SL_TURBO", _("SL Turbo")

    NISSENS = "NISSENS", _("Nissens")
    DELPHI = "DELPHI", _("Delphi")
    NRF = "NRF", _("NRF")

    RIDEX = "RIDEX", _("RIDEX")
    STARK = "STARK", _("STARK")
    ALANKO = "ALANKO", _("ALANKO")
    LUCAS = "LUCAS", _("Lucas")
    BTS_TURBO = "BTS_TURBO", _("BTS Turbo")
    BE_TURBO = "BE_TURBO", _("BE Turbo")
    TURBO_MOTOR = "TURBO_MOTOR", _("Turbo Motor")
    MOTAIR = "MOTAIR", _("Motair")
    ELSTOCK = "ELSTOCK", _("Elstock")
    TURBO_S_M = "TURBO_S_M", _("Turbo's Hoet")

    AUTRE = "AUTRE", _("Autre")





class FabricantIntercooler(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")

    # Fabricants OEM / équipementiers
    MAHLE = "MAHLE", _("MAHLE")
    BEHR = "BEHR", _("Behr")
    VALEO = "VALEO", _("Valeo")
    DENSO = "DENSO", _("Denso")
    DELPHI = "DELPHI", _("Delphi")
    MODINE = "MODINE", _("Modine")
    HANON = "HANON", _("Hanon Systems")
    SANDEN = "SANDEN", _("Sanden")
    MARELLI = "MARELLI", _("Marelli")
    NRF = "NRF", _("NRF")
    NISSENS = "NISSENS", _("Nissens")
    AVA = "AVA", _("AVA Cooling Systems")
    KOYORAD = "KOYORAD", _("Koyorad")
    TYC = "TYC", _("TYC")

    # Turbo / systèmes de suralimentation
    GARRETT = "GARRETT", _("Garrett")
    BORGWARNER = "BORGWARNER", _("BorgWarner")
    MITSUBISHI = "MITSUBISHI", _("Mitsubishi")
    IHI = "IHI", _("IHI")

    # Performance / compétition
    WAGNER_TUNING = "WAGNER_TUNING", _("Wagner Tuning")
    MISHIMOTO = "MISHIMOTO", _("Mishimoto")
    FORGE = "FORGE", _("Forge Motorsport")
    AIRTEC = "AIRTEC", _("AIRTEC Motorsport")
    DO88 = "DO88", _("do88")
    CSF = "CSF", _("CSF")
    PWR = "PWR", _("PWR")
    PROALLOY = "PROALLOY", _("Pro Alloy")
    TURBOSMART = "TURBOSMART", _("Turbosmart")
    AMS = "AMS", _("AMS Performance")
    APR = "APR", _("APR")
    CTS_TURBO = "CTS_TURBO", _("CTS Turbo")
    DINAN = "DINAN", _("Dinan")
    COBB = "COBB", _("COBB Tuning")

    # Aftermarket / remplacement
    HELLA = "HELLA", _("HELLA")
    RIDEX = "RIDEX", _("RIDEX")
    STARK = "STARK", _("STARK")
    FEBI = "FEBI", _("FEBI Bilstein")
    MEYLE = "MEYLE", _("MEYLE")
    METZGER = "METZGER", _("Metzger")
    VAN_WEZEL = "VAN_WEZEL", _("Van Wezel")
    PRASCO = "PRASCO", _("Prasco")
    THERMOTEC = "THERMOTEC", _("Thermotec")
    KALE = "KALE", _("KALE")
    JP_GROUP = "JP_GROUP", _("JP Group")
    MAXGEAR = "MAXGEAR", _("MAXGEAR")
    ABAKUS = "ABAKUS", _("ABAKUS")

    AUTRE = "AUTRE", _("Autre")



class FabricantVanneEGR(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")

    # Équipementiers / OEM
    BOSCH = "BOSCH", _("Bosch")
    PIERBURG = "PIERBURG", _("Pierburg")
    WAHLER = "WAHLER", _("Wahler")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    VDO = "VDO", _("VDO")
    HELLA = "HELLA", _("HELLA")
    VALEO = "VALEO", _("Valeo")
    MARELLI = "MARELLI", _("Marelli")
    HITACHI = "HITACHI", _("Hitachi")
    AISIN = "AISIN", _("Aisin")
    MAHLE = "MAHLE", _("MAHLE")

    # Aftermarket
    FEBI = "FEBI", _("FEBI Bilstein")
    SWAG = "SWAG", _("SWAG")
    MEYLE = "MEYLE", _("MEYLE")
    METZGER = "METZGER", _("Metzger")
    ERA = "ERA", _("ERA")
    FACET = "FACET", _("Facet")
    VEMO = "VEMO", _("VEMO")
    TOPRAN = "TOPRAN", _("Topran")
    MAPCO = "MAPCO", _("MAPCO")
    TRISCAN = "TRISCAN", _("Triscan")
    SIDAT = "SIDAT", _("SIDAT")
    FISPA = "FISPA", _("FISPA")
    NRF = "NRF", _("NRF")
    NTY = "NTY", _("NTY")
    RIDEX = "RIDEX", _("RIDEX")
    STARK = "STARK", _("STARK")
    MAXGEAR = "MAXGEAR", _("MAXGEAR")
    ABAKUS = "ABAKUS", _("ABAKUS")
    ESEN_SKV = "ESEN_SKV", _("ESEN SKV")
    MEAT_DORIA = "MEAT_DORIA", _("Meat & Doria")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    HERTH_BUSS = "HERTH_BUSS", _("Herth+Buss")
    QUINTON_HAZELL = "QUINTON_HAZELL", _("Quinton Hazell")

    AUTRE = "AUTRE", _("Autre")





class FabricantDurite(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")

    # OEM / grands équipementiers
    CONTINENTAL = "CONTINENTAL", _("Continental")
    CONTITECH = "CONTITECH", _("ContiTech")
    GATES = "GATES", _("Gates")
    DAYCO = "DAYCO", _("Dayco")
    HUTCHINSON = "HUTCHINSON", _("Hutchinson")
    PARKER = "PARKER", _("Parker")
    COHLINE = "COHLINE", _("Cohline")
    NORMA = "NORMA", _("NORMA Group")
    VERITAS = "VERITAS", _("Veritas")
    FREUDENBERG = "FREUDENBERG", _("Freudenberg")
    TEKNIKUM = "TEKNIKUM", _("Teknikum")

    # Refroidissement / moteur
    MAHLE = "MAHLE", _("MAHLE")
    BEHR = "BEHR", _("Behr")
    VALEO = "VALEO", _("Valeo")
    NISSENS = "NISSENS", _("Nissens")
    NRF = "NRF", _("NRF")
    METZGER = "METZGER", _("Metzger")
    MEYLE = "MEYLE", _("MEYLE")
    FEBI = "FEBI", _("FEBI Bilstein")
    SWAG = "SWAG", _("SWAG")
    TOPRAN = "TOPRAN", _("Topran")
    VAICO = "VAICO", _("VAICO")

    # Turbo / intercooler / admission
    FORGE = "FORGE", _("Forge Motorsport")
    SAMCO = "SAMCO", _("Samco Sport")
    DO88 = "DO88", _("do88")
    MISHIMOTO = "MISHIMOTO", _("Mishimoto")
    WAGNER_TUNING = "WAGNER_TUNING", _("Wagner Tuning")
    AIRTEC = "AIRTEC", _("AIRTEC Motorsport")

    # Carburant / huile / hydraulique
    BOSCH = "BOSCH", _("Bosch")
    DELPHI = "DELPHI", _("Delphi")
    PIERBURG = "PIERBURG", _("Pierburg")
    HELLA = "HELLA", _("HELLA")

    # Aftermarket
    IMPERGOM = "IMPERGOM", _("Impergom")
    RAPRO = "RAPRO", _("Rapro")
    THERMOTEC = "THERMOTEC", _("Thermotec")
    TRISCAN = "TRISCAN", _("Triscan")
    MAPCO = "MAPCO", _("MAPCO")
    JP_GROUP = "JP_GROUP", _("JP Group")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    HERTH_BUSS = "HERTH_BUSS", _("Herth+Buss")
    RIDEX = "RIDEX", _("RIDEX")
    STARK = "STARK", _("STARK")
    MAXGEAR = "MAXGEAR", _("MAXGEAR")
    ABAKUS = "ABAKUS", _("ABAKUS")

    AUTRE = "AUTRE", _("Autre")




class FabricantAlternateur(models.TextChoices):
    BOSCH = "BOSCH", _("Bosch")
    VALEO = "VALEO", _("Valeo")
    DENSO = "DENSO", _("Denso")
    DELPHI = "DELPHI", _("Delphi")
    HITACHI = "HITACHI", _("Hitachi")
    MITSUBISHI = "MITSUBISHI", _("Mitsubishi Electric")
    HELLA = "HELLA", _("Hella")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    LUCAS = "LUCAS", _("Lucas")
    PRESTOLITE = "PRESTOLITE", _("Prestolite")
    REMY = "REMY", _("Remy")
    MANDO = "MANDO", _("Mando")
    AS_PL = "AS_PL", _("AS-PL")
    HC_CARGO = "HC_CARGO", _("HC-Cargo")
    MAHLE = "MAHLE", _("Mahle")
    VISTEON = "VISTEON", _("Visteon")
    MOTORCRAFT = "MOTORCRAFT", _("Motorcraft")
    ACDELCO = "ACDELCO", _("ACDelco")
    MOPAR = "MOPAR", _("Mopar")
    MOBILETRON = "MOBILETRON", _("Mobiletron")
    ERA = "ERA", _("ERA")
    MEAT_DORIA = "MEAT_DORIA", _("Meat & Doria")
    FEBI = "FEBI", _("Febi Bilstein")
    HERTH_BUSS = "HERTH_BUSS", _("Herth+Buss")
    JP_GROUP = "JP_GROUP", _("JP Group")
    MAPCO = "MAPCO", _("Mapco")
    RIDEX = "RIDEX", _("Ridex")
    STARK = "STARK", _("Stark")
    WAI = "WAI", _("WAI Global")
    POWERMAX = "POWERMAX", _("PowerMax")
    BV_PSH = "BV_PSH", _("BV PSH")
    ELSTOCK = "ELSTOCK", _("Elstock")
    CEVAM = "CEVAM", _("CEVAM")
    SNRA = "SNRA", _("SNRA")
    LAUBER = "LAUBER", _("Lauber")
    CASCO = "CASCO", _("Casco")
    SANDO = "SANDO", _("Sando")
    EUROTEC = "EUROTEC", _("Eurotec")
    ALANKO = "ALANKO", _("Alanko")
    ROTOVIS = "ROTOVIS", _("Rotovis")
    EAI = "EAI", _("EAI")
    AUTEX = "AUTEX", _("Autex")
    QUINTON_HAZELL = "QUINTON_HAZELL", _("Quinton Hazell")
    TRW = "TRW", _("TRW")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    VDO = "VDO", _("VDO")
    NIPPARTS = "NIPPARTS", _("Nipparts")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    ACKOJAP = "ACKOJAP", _("ACKOJA")
    ERA_BENELUX = "ERA_BENELUX", _("ERA Benelux")

    AUTRE = "AUTRE", _("Autre")
    CHOISIR = "CHOISIR", _("Choisir")





class FabricantCourroie(models.TextChoices):
    CONTINENTAL = "CONTINENTAL", _("Continental / ContiTech")
    GATES = "GATES", _("Gates")
    DAYCO = "DAYCO", _("Dayco")
    BOSCH = "BOSCH", _("Bosch")
    SKF = "SKF", _("SKF")
    INA = "INA", _("INA")
    SNR = "SNR", _("SNR")
    HUTCHINSON = "HUTCHINSON", _("Hutchinson")
    OPTIBELT = "OPTIBELT", _("Optibelt")
    MITSUBOSHI = "MITSUBOSHI", _("Mitsuboshi")
    BANDO = "BANDO", _("Bando")
    MEYLE = "MEYLE", _("Meyle")
    FEBI = "FEBI", _("Febi Bilstein")
    SWAG = "SWAG", _("SWAG")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    QUINTON_HAZELL = "QUINTON_HAZELL", _("Quinton Hazell")
    MAPCO = "MAPCO", _("Mapco")
    RIDEX = "RIDEX", _("Ridex")
    STARK = "STARK", _("Stark")
    VAICO = "VAICO", _("Vaico")
    TOPRAN = "TOPRAN", _("Topran")
    TRISCAN = "TRISCAN", _("Triscan")
    METELLI = "METELLI", _("Metelli")
    GRAF = "GRAF", _("Graf")
    HEPU = "HEPU", _("HEPU")
    DOLZ = "DOLZ", _("Dolz")
    KAVO_PARTS = "KAVO_PARTS", _("Kavo Parts")
    JAPANPARTS = "JAPANPARTS", _("Japanparts")
    ASHIKA = "ASHIKA", _("Ashika")
    HERTH_BUSS = "HERTH_BUSS", _("Herth+Buss")
    NIPPARTS = "NIPPARTS", _("Nipparts")
    ACKOJA = "ACKOJA", _("ACKOJA")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    VALEO = "VALEO", _("Valeo")

    AUTRE = "AUTRE", _("Autre")
    CHOISIR = "CHOISIR", _("Choisir")





class FabricantEmbrayage(models.TextChoices):
    # ============================================================
    # GRANDS ÉQUIPEMENTIERS / OEM
    # ============================================================
    CHOISIR = "CHOISIR", _("Choisir")

    LUK = "LUK", _("LuK / Schaeffler")
    SACHS = "SACHS", _("SACHS / ZF")
    VALEO = "VALEO", _("Valeo")
    EXEDY = "EXEDY", _("EXEDY")
    AISIN = "AISIN", _("AISIN")
    FCC = "FCC", _("F.C.C.")
    BORGWARNER = "BORGWARNER", _("BorgWarner")
    EATON = "EATON", _("Eaton")
    TWIN_DISC = "TWIN_DISC", _("Twin Disc")
    SETCO = "SETCO", _("Setco Automotive")
    TIELIU = "TIELIU", _("Zhejiang Tieliu")
    RAICAM = "RAICAM", _("Raicam")
    NISSIN = "NISSIN", _("Nissin")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    NSK = "NSK", _("NSK")
    FCC_JAPAN = "FCC_JAPAN", _("FCC Japan")

    # ============================================================
    # PERFORMANCE / SPORT / COMPÉTITION
    # ============================================================

    AP_RACING = "AP_RACING", _("AP Racing")
    TILTON = "TILTON", _("Tilton Engineering")
    OS_GIKEN = "OS_GIKEN", _("OS Giken")
    ACT = "ACT", _("ACT (Advanced Clutch Technology)")
    SPEC = "SPEC", _("SPEC Clutch")
    CENTERFORCE = "CENTERFORCE", _("Centerforce")
    CLUTCH_MASTERS = "CLUTCH_MASTERS", _("Clutch Masters")
    COMPETITION_CLUTCH = "COMPETITION_CLUTCH", _("Competition Clutch")
    HELIX = "HELIX", _("Helix Autosport")
    MANTIC = "MANTIC", _("Mantic Clutch")
    QUARTER_MASTER = "QUARTER_MASTER", _("Quarter Master")
    MCLEOD = "MCLEOD", _("McLeod Racing")
    HAYS = "HAYS", _("Hays Clutches")
    RAM = "RAM", _("RAM Clutches")
    SOUTH_BEND = "SOUTH_BEND", _("South Bend Clutch")
    XTREME = "XTREME", _("Xtreme Clutch")
    DKM = "DKM", _("DKM Clutch")
    FIDANZA = "FIDANZA", _("Fidanza")
    CARBONETIC = "CARBONETIC", _("Carbonetic")
    NPC = "NPC", _("NPC Performance Clutches")

    # ============================================================
    # JAPON / PERFORMANCE JAPONAISE
    # ============================================================

    HKS = "HKS", _("HKS")
    CUSCO = "CUSCO", _("CUSCO")
    ORC = "ORC", _("Ogura Racing Clutch (ORC)")
    ATS = "ATS", _("ATS")
    NISMO = "NISMO", _("NISMO")
    TRD = "TRD", _("TRD")
    STI = "STI", _("STI")
    TODA = "TODA", _("Toda Racing")
    JUN = "JUN", _("JUN Auto")
    GREDDY = "GREDDY", _("GReddy / TRUST")

    # ============================================================
    # EUROPE / AFTERMARKET
    # ============================================================

    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    FEBI = "FEBI", _("febi bilstein")
    MEYLE = "MEYLE", _("MEYLE")
    MAPCO = "MAPCO", _("MAPCO")
    RIDEX = "RIDEX", _("RIDEX")
    STARK = "STARK", _("STARK")
    NK = "NK", _("NK")
    JP_GROUP = "JP_GROUP", _("JP Group")
    MAXGEAR = "MAXGEAR", _("MAXGEAR")
    KAMOKA = "KAMOKA", _("KAMOKA")
    DENCKERMANN = "DENCKERMANN", _("Denckermann")
    STATIM = "STATIM", _("STATIM")
    MECARM = "MECARM", _("MECARM")
    KAWE = "KAWE", _("KAWE")
    NATIONAL = "NATIONAL", _("National")
    BORG_BECK = "BORG_BECK", _("Borg & Beck")
    QH = "QH", _("Quinton Hazell")
    LPR = "LPR", _("LPR")
    FAST = "FAST", _("FAST")
    SAMKO = "SAMKO", _("SAMKO")
    STARLINE = "STARLINE", _("Starline")
    ASHIKA = "ASHIKA", _("ASHIKA")
    JAPANPARTS = "JAPANPARTS", _("Japanparts")
    JAPKO = "JAPKO", _("JAPKO")

    # ============================================================
    # POIDS LOURDS / UTILITAIRES / INDUSTRIEL
    # ============================================================

    KNORR_BREMSE = "KNORR_BREMSE", _("Knorr-Bremse")
    WABCO = "WABCO", _("WABCO / ZF")
    HAMMER = "HAMMER", _("Hammer Kupplungen")
    LIPE = "LIPE", _("LIPE Clutch")
    CEI = "CEI", _("CEI")
    EURORICAMBI = "EURORICAMBI", _("Euroricambi")

    # ============================================================
    # CONSTRUCTEURS / PIÈCES D'ORIGINE
    # ============================================================

    BMW = "BMW", _("BMW Original")
    MINI = "MINI", _("MINI Original")
    MERCEDES = "MERCEDES", _("Mercedes-Benz Original")
    AUDI = "AUDI", _("Audi Original")
    VOLKSWAGEN = "VOLKSWAGEN", _("Volkswagen Original")
    PORSCHE = "PORSCHE", _("Porsche Original")
    FORD = "FORD", _("Ford Original")
    OPEL = "OPEL", _("Opel Original")
    PEUGEOT = "PEUGEOT", _("Peugeot Original")
    CITROEN = "CITROEN", _("Citroën Original")
    RENAULT = "RENAULT", _("Renault Original")
    DACIA = "DACIA", _("Dacia Original")
    FIAT = "FIAT", _("Fiat Original")
    ALFA_ROMEO = "ALFA_ROMEO", _("Alfa Romeo Original")
    LANCIA = "LANCIA", _("Lancia Original")
    VOLVO = "VOLVO", _("Volvo Original")
    TOYOTA = "TOYOTA", _("Toyota Original")
    LEXUS = "LEXUS", _("Lexus Original")
    HONDA = "HONDA", _("Honda Original")
    NISSAN = "NISSAN", _("Nissan Original")
    MAZDA = "MAZDA", _("Mazda Original")
    SUBARU = "SUBARU", _("Subaru Original")
    MITSUBISHI = "MITSUBISHI", _("Mitsubishi Original")
    SUZUKI = "SUZUKI", _("Suzuki Original")
    HYUNDAI = "HYUNDAI", _("Hyundai Original")
    KIA = "KIA", _("Kia Original")
    LAND_ROVER = "LAND_ROVER", _("Land Rover Original")
    JAGUAR = "JAGUAR", _("Jaguar Original")

    # ============================================================
    # GÉNÉRIQUE
    # ============================================================

    OEM = "OEM", _("Origine constructeur (OEM)")
    AUTRE = "AUTRE", _("Autre fabricant")
    INCONNU = "INCONNU", _("Fabricant inconnu")




class FabricantJointSpi(models.TextChoices):

    CHOISIR = "CHOISIR", _("Choisir")
    # ============================================================
    # GRANDS FABRICANTS / OEM
    # ============================================================

    CORTECO = "CORTECO", _("Corteco")
    FREUDENBERG = "FREUDENBERG", _("Freudenberg")
    ELRING = "ELRING", _("Elring")
    VICTOR_REINZ = "VICTOR_REINZ", _("Victor Reinz")
    SKF = "SKF", _("SKF")
    NOK = "NOK", _("NOK")
    NAK = "NAK", _("NAK")
    KACO = "KACO", _("KACO")
    TRELLEBORG = "TRELLEBORG", _("Trelleborg")
    PARKER = "PARKER", _("Parker")
    SAKAGAMI = "SAKAGAMI", _("Sakagami")
    MUSASHI = "MUSASHI", _("Musashi Oil Seal")
    ARS = "ARS", _("ARS")
    PAYEN = "PAYEN", _("Payen")
    AJUSA = "AJUSA", _("Ajusa")

    # ============================================================
    # ROULEMENTS / TRANSMISSION / ÉTANCHÉITÉ
    # ============================================================

    FAG = "FAG", _("FAG / Schaeffler")
    INA = "INA", _("INA / Schaeffler")
    SNR = "SNR", _("NTN-SNR")
    NTN = "NTN", _("NTN")
    KOYO = "KOYO", _("Koyo / JTEKT")
    TIMKEN = "TIMKEN", _("Timken")
    NSK = "NSK", _("NSK")

    # ============================================================
    # AFTERMARKET EUROPÉEN
    # ============================================================

    FEBI = "FEBI", _("febi bilstein")
    SWAG = "SWAG", _("SWAG")
    MEYLE = "MEYLE", _("MEYLE")
    METZGER = "METZGER", _("Metzger")
    TOPRAN = "TOPRAN", _("TOPRAN")
    VAICO = "VAICO", _("VAICO")
    MAPCO = "MAPCO", _("MAPCO")
    JP_GROUP = "JP_GROUP", _("JP Group")
    MAXGEAR = "MAXGEAR", _("MAXGEAR")
    RIDEX = "RIDEX", _("RIDEX")
    STARK = "STARK", _("STARK")
    AUTOMEGA = "AUTOMEGA", _("AUTOMEGA")
    TRUCKTEC = "TRUCKTEC", _("TRUCKTEC Automotive")
    BGA = "BGA", _("BGA")
    FAI = "FAI", _("FAI AutoParts")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    IMPERGOM = "IMPERGOM", _("IMPERGOM")
    ORIGINAL_IMPERIUM = "ORIGINAL_IMPERIUM", _("Original Imperium")

    # ============================================================
    # AFTERMARKET ASIATIQUE
    # ============================================================

    ASHIKA = "ASHIKA", _("ASHIKA")
    JAPANPARTS = "JAPANPARTS", _("Japanparts")
    JAPKO = "JAPKO", _("JAPKO")
    FEBEST = "FEBEST", _("FEBEST")
    GSP = "GSP", _("GSP")
    MASUMA = "MASUMA", _("Masuma")

    # ============================================================
    # CONSTRUCTEURS / PIÈCES D'ORIGINE
    # ============================================================

    BMW = "BMW", _("BMW Original")
    MINI = "MINI", _("MINI Original")
    MERCEDES = "MERCEDES", _("Mercedes-Benz Original")
    AUDI = "AUDI", _("Audi Original")
    VOLKSWAGEN = "VOLKSWAGEN", _("Volkswagen Original")
    SKODA = "SKODA", _("Škoda Original")
    SEAT = "SEAT", _("SEAT Original")
    CUPRA = "CUPRA", _("CUPRA Original")
    PORSCHE = "PORSCHE", _("Porsche Original")

    OPEL = "OPEL", _("Opel Original")
    FORD = "FORD", _("Ford Original")
    VOLVO = "VOLVO", _("Volvo Original")
    SAAB = "SAAB", _("Saab Original")

    PEUGEOT = "PEUGEOT", _("Peugeot Original")
    CITROEN = "CITROEN", _("Citroën Original")
    DS = "DS", _("DS Automobiles Original")
    RENAULT = "RENAULT", _("Renault Original")
    DACIA = "DACIA", _("Dacia Original")

    FIAT = "FIAT", _("Fiat Original")
    ALFA_ROMEO = "ALFA_ROMEO", _("Alfa Romeo Original")
    LANCIA = "LANCIA", _("Lancia Original")
    MASERATI = "MASERATI", _("Maserati Original")
    FERRARI = "FERRARI", _("Ferrari Original")

    TOYOTA = "TOYOTA", _("Toyota Original")
    LEXUS = "LEXUS", _("Lexus Original")
    HONDA = "HONDA", _("Honda Original")
    NISSAN = "NISSAN", _("Nissan Original")
    INFINITI = "INFINITI", _("Infiniti Original")
    MAZDA = "MAZDA", _("Mazda Original")
    SUBARU = "SUBARU", _("Subaru Original")
    MITSUBISHI = "MITSUBISHI", _("Mitsubishi Original")
    SUZUKI = "SUZUKI", _("Suzuki Original")

    HYUNDAI = "HYUNDAI", _("Hyundai Original")
    KIA = "KIA", _("Kia Original")

    JAGUAR = "JAGUAR", _("Jaguar Original")
    LAND_ROVER = "LAND_ROVER", _("Land Rover Original")

    # ============================================================
    # GÉNÉRIQUE
    # ============================================================

    OEM = "OEM", _("Origine constructeur (OEM)")
    AUTRE = "AUTRE", _("Autre fabricant")
    INCONNU = "INCONNU", _("Fabricant inconnu")



class FabricantPompeCarburant(models.TextChoices):
    BOSCH = "BOSCH", _("Bosch")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    VDO = "VDO", _("VDO")
    PIERBURG = "PIERBURG", _("Pierburg")
    HITACHI = "HITACHI", _("Hitachi")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    WALBRO = "WALBRO", _("Walbro")
    TI_AUTOMOTIVE = "TI_AUTOMOTIVE", _("TI Automotive")
    OEM = "OEM", _("Origine constructeur (OEM)")
    AUTRE = "AUTRE", _("Autre fabricant")
    INCONNU = "INCONNU", _("Fabricant inconnu")
    CHOISIR = "CHOISIR", _("Choisir")


class FabricantPompeHautePression(models.TextChoices):
    BOSCH = "BOSCH", _("Bosch")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    VDO = "VDO", _("VDO")
    HITACHI = "HITACHI", _("Hitachi")
    OEM = "OEM", _("Origine constructeur (OEM)")
    AUTRE = "AUTRE", _("Autre fabricant")
    INCONNU = "INCONNU", _("Fabricant inconnu")
    CHOISIR = "CHOISIR", _("Choisir")


class FabricantRampeInjection(models.TextChoices):
    BOSCH = "BOSCH", _("Bosch")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    VDO = "VDO", _("VDO")
    HITACHI = "HITACHI", _("Hitachi")
    OEM = "OEM", _("Origine constructeur (OEM)")
    AUTRE = "AUTRE", _("Autre fabricant")
    INCONNU = "INCONNU", _("Fabricant inconnu")
    CHOISIR = "CHOISIR", _("Choisir")


class FabricantCapteurPressionRampe(models.TextChoices):
    BOSCH = "BOSCH", _("Bosch")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    VDO = "VDO", _("VDO")
    HELLA = "HELLA", _("Hella")
    FACET = "FACET", _("Facet")
    FAE = "FAE", _("FAE")
    OEM = "OEM", _("Origine constructeur (OEM)")
    AUTRE = "AUTRE", _("Autre fabricant")
    INCONNU = "INCONNU", _("Fabricant inconnu")
    CHOISIR = "CHOISIR", _("Choisir")


class FabricantTuyauxHautePression(models.TextChoices):
    BOSCH = "BOSCH", _("Bosch")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    OEM = "OEM", _("Origine constructeur (OEM)")
    AUTRE = "AUTRE", _("Autre fabricant")
    INCONNU = "INCONNU", _("Fabricant inconnu")
    CHOISIR = "CHOISIR", _("Choisir")


class FabricantInjecteur(models.TextChoices):
    BOSCH = "BOSCH", _("Bosch")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    VDO = "VDO", _("VDO")
    SIEMENS = "SIEMENS", _("Siemens")
    HITACHI = "HITACHI", _("Hitachi")
    KEIHIN = "KEIHIN", _("Keihin")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    OEM = "OEM", _("Origine constructeur (OEM)")
    AUTRE = "AUTRE", _("Autre fabricant")
    INCONNU = "INCONNU", _("Fabricant inconnu")
    CHOISIR = "CHOISIR", _("Choisir")


class FabricantConnecteurInjecteur(models.TextChoices):
    BOSCH = "BOSCH", _("Bosch")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    TE_CONNECTIVITY = "TE_CONNECTIVITY", _("TE Connectivity")
    AMP = "AMP", _("AMP")
    MOLEX = "MOLEX", _("Molex")
    OEM = "OEM", _("Origine constructeur (OEM)")
    AUTRE = "AUTRE", _("Autre fabricant")
    INCONNU = "INCONNU", _("Fabricant inconnu")
    CHOISIR = "CHOISIR", _("Choisir")


class FabricantAmpoule(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    BOSCH = "BOSCH", _("Bosch")
    OSRAM = "OSRAM", _("Osram")
    PHILIPS = "PHILIPS", _("Philips")
    HELLA = "HELLA", _("Hella")
    VALEO = "VALEO", _("Valeo")
    NARVA = "NARVA", _("Narva")
    GE = "GE", _("GE")
    RING = "RING", _("Ring")
    PIAA = "PIAA", _("PIAA")
    MTECH = "MTECH", _("M-Tech")
    NEOLUX = "NEOLUX", _("Neolux")
    TUNGSRAM = "TUNGSRAM", _("Tungsram")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur")
    AUTRE = "AUTRE", _("Autre")






class TVAConfig:
    """
    Configuration commune des pays et taux de TVA.
    """

    PAYS_CHOICES = [
        ("AT", _("Autriche")),
        ("BE", _("Belgique")),
        ("BG", _("Bulgarie")),
        ("CY", _("Chypre")),
        ("CZ", _("Tchéquie")),
        ("DE", _("Allemagne")),
        ("DK", _("Danemark")),
        ("EE", _("Estonie")),
        ("ES", _("Espagne")),
        ("FI", _("Finlande")),
        ("FR", _("France")),
        ("GR", _("Grèce")),
        ("HR", _("Croatie")),
        ("HU", _("Hongrie")),
        ("IE", _("Irlande")),
        ("IT", _("Italie")),
        ("LT", _("Lituanie")),
        ("LU", _("Luxembourg")),
        ("LV", _("Lettonie")),
        ("MT", _("Malte")),
        ("NL", _("Pays-Bas")),
        ("PL", _("Pologne")),
        ("PT", _("Portugal")),
        ("RO", _("Roumanie")),
        ("SE", _("Suède")),
        ("SI", _("Slovénie")),
        ("SK", _("Slovaquie")),
    ]

    TVA_PIECES = {
        "AT": 20,
        "BE": 21,
        "BG": 20,
        "CY": 19,
        "CZ": 21,
        "DE": 19,
        "DK": 25,
        "EE": 24,
        "ES": 21,
        "FI": 25.5,
        "FR": 20,
        "GR": 24,
        "HR": 25,
        "HU": 27,
        "IE": 23,
        "IT": 22,
        "LT": 21,
        "LU": 17,
        "LV": 21,
        "MT": 18,
        "NL": 21,
        "PL": 23,
        "PT": 23,
        "RO": 21,
        "SE": 25,
        "SI": 22,
        "SK": 23,
    }

    DEFAULT_PAYS = "BE"

    @classmethod
    def get_tva(cls, pays):
        """
        Retourne le taux de TVA du pays.
        Belgique par défaut si le pays n'est pas trouvé.
        """
        return cls.TVA_PIECES.get(
            pays,
            cls.TVA_PIECES[cls.DEFAULT_PAYS],
        )

    #taux_tva = TVAConfig.get_tva(self.pays)



class LiquideDirectionQualite(models.TextChoices):

    # Hydraulique direction assistée (Pentosin / CHF)
    CHF_7_1 = "CHF_7_1", _("CHF 7.1")
    CHF_11S = "CHF_11S", _("CHF 11S")
    CHF_202 = "CHF_202", _("CHF 202")
    CHF_1_PLUS = "CHF_1_PLUS", _("CHF 1+")
    CHF_LIFEGUARD = "CHF_LIFEGUARD", _("CHF Lifeguard Fluid")

    # --- Porsche spécifiques (très important : base CHF) ---
    PORSCHE_CHF_11S = "PORSCHE_CHF_11S", _("Porsche / Pentosin CHF 11S (direction assistée)")
    PORSCHE_CHF_202 = "PORSCHE_CHF_202", _("Porsche / Pentosin CHF 202 (hydraulique moderne)")
    PORSCHE_ATF_D3 = "PORSCHE_ATF_D3", _("Porsche ATF Dexron III (anciens modèles)")

    # --- BMW spécifiques (très important) ---
    BMW_CHF_11S = "BMW_CHF_11S", _("BMW / Pentosin CHF 11S (direction assistée)")
    BMW_CHF_202 = "BMW_CHF_202", _("BMW / Pentosin CHF 202 (direction assistée moderne)")
    BMW_CHF_7_1 = "BMW_CHF_7_1", _("BMW CHF 7.1 (anciens systèmes hydrauliques)")
    BMW_ATF_D3 = "BMW_ATF_D3", _("BMW ATF Dexron III (anciens modèles direction assistée)")

    # Fluides spécifiques Renault / ELF
    RENAULT_MATIC_D2 = "RENAULT_MATIC_D2", _("Renaultmatic D2 (ELF)")
    RENAULT_MATIC_D3_SYN = "RENAULT_MATIC_D3_SYN", _("Renaultmatic D3 SYN (ELF)")
    ELF_MATIC_G3 = "ELF_MATIC_G3", _("ELF Matic G3")

    # --- Renault spécifiques (atelier / OEM) ---
    RENAULT_PSF_D3 = "RENAULT_PSF_D3", _("Renault PSF Dexron III (direction assistée hydraulique)")
    RENAULT_ELF_PSF = "RENAULT_ELF_PSF", _("Renault / ELF liquide direction assistée")

    # Autres constructeurs
    PSF_HYUNDAI_KIA = "PSF_HYUNDAI_KIA", _("PSF Hyundai / Kia")
    PSF_TOYOTA = "PSF_TOYOTA", _("PSF Toyota")
    PSF_HONDA = "PSF_HONDA", _("PSF Honda")

    # Universel
    UNIVERSAL_PSF = "UNIVERSAL_PSF", _("Liquide direction assistée universel")



class HuileEtat(models.TextChoices):
    ZERO_16 = "0W16", _("0W16")
    ZERO_20 = "0W20", _("0W20")
    ZERO_30 = "0W30", _("0W30")
    ZERO_40 = "0W40", _("0W40")
    CINQ_20 = "5W20", _("5W20")
    CINQ_30 = "5W30", _("5W30")
    CINQ_40 = "5W40", _("5W40")
    DIX_40 = "10W40", _("10W40")
    DIX_50 = "10W50", _("10W50")
    DIX_60 = "10W60", _("10W60")
    QUINZE_40 = "15W40", _("15W40")
    QUINZE_50 = "15W50", _("15W50")
    VINGT_50 = "20W50", _("20W50")


class HuileBoiteNiveauxEtat(models.TextChoices):
    SEPTANTE_CINQ = "75W", _("75W")
    SEPTANTE_5_80 = "75W80", _("75W80")
    SEPTANTE_CINQ90  = "75W90", _("75W90")
    QUATRE_20 = "80W", "80W"
    QUATRE_20_90 = "80W90", _("80W90")
    QUATRE_25_90 = "85W90", _("85W90")

    ATF3 = "ATF_III", _("ATF III")
    ATF_DSG = "ATF_DSG", _("ATF DSG")
    ATF_DCT = "ATF_DCT", _("ATF DCT")
    ATF_CVT = "ATF_CVT", _("ATF CVT")
    ATF_DEXRON_II = "ATF_DEXRON_II", _("ATF Dexron II")
    ATF_DEXRON_III = "ATF_DEXRON_III", _("ATF Dexron III")
    ATF_DEXRON_VI = "ATF_DEXRON_VI", _("ATF Dexron VI")
    ATF_MERCON = "ATF_MERCON", _("ATF Mercon")
    ATF_MERCON_V = "ATF_MERCON_V", _("ATF Mercon V")
    ATF_MERCON_LV = "ATF_MERCON_LV", _("ATF Mercon LV")
    ATF_MULTI = "ATF_MULTI", _("ATF Multi Vehicle")
    ATF_WS = "ATF_WS", _("ATF Toyota WS")
    ATF_ZF_LIFEGUARD = "ATF_ZF_LIFEGUARD", _("ZF Lifeguard")
    ATF_MOPAR = "ATF_MOPAR", _("Mopar ATF+4")
    ATF_AISIN = "ATF_AISIN", _("Aisin ATF")
    ATF_MBV236 = "ATF_MBV236", _("Mercedes MB 236.x")
    ATF_VOLVO = "ATF_VOLVO", _("Volvo ATF")
    ATF_HONDA = "ATF_HONDA", _("Honda ATF DW-1")
    ATF_NISSAN = "ATF_NISSAN", _("Nissan Matic")




class HuilePontEtat(models.TextChoices):
    SEPTANTE_CINQ80 = "75W80", _("75W80")
    SEPTANTE_CINQ85 = "75W85", _("75W85")
    SEPTANTE_CINQ90 = "75W90", _("75W90")
    SEPTANTE_CINQ110 = "75W110", _("75W110")
    SEPTANTE_CINQ140 = "75W140", _("75W140")

    QUATRE_VINGT90 = "80W90", _("80W90")
    QUATRE_VINGT140 = "80W140", _("80W140")

    QUATRE_VINGT_CINQ90 = "85W90", _("85W90")
    QUATRE_VINGT_CINQ140 = "85W140", _("85W140")

    SAE90 = "SAE90", _("SAE 90")
    SAE140 = "SAE140", _("SAE 140")

    PORSCHE_75W90 = "PORSCHE_75W90", _("Porsche 75W90")
    PORSCHE_75W140 = "PORSCHE_75W140", _("Porsche 75W140")

    AUTRE = "AUTRE", _("Autre")
    INCONNUE = "INCONNUE", _("Huile inconnue")

class RefroidissementQualiteEtat(models.TextChoices):
    # Volkswagen Group
    G11 = "G11", _("G 11")
    G12 = "G12", _("G 12")
    G12_PLUS = "G12_PLUS", _("G 12+")
    G12_PLUS_PLUS = "G12_PLUS_PLUS", _("G 12++")
    G13 = "G13", _("G 13")

    # BMW
    G48 = "G48", _("G 48")

    # Mercedes-Benz
    MB_325_0 = "MB_325_0", _("MB 325.0")
    MB_325_3 = "MB_325_3", _("MB 325.3")
    MB_325_5 = "MB_325_5", _("MB 325.5")

    # Renault / Dacia
    TYPE_D = "TYPE_D", _("Type D")

    # PSA (Peugeot / Citroën)
    PSA_B71_5110 = "PSA_B71_5110", _("PSA B71 5110")

    # Ford
    WSS_M97B44_D = "WSS_M97B44_D", _("WSS-M97B44-D")
    WSS_M97B51_A1 = "WSS_M97B51_A1", _("WSS-M97B51-A1")

    # General Motors
    DEX_COOL = "DEX_COOL", _("Dex-Cool")

    # Toyota / Lexus
    TOYOTA_SLLC = "TOYOTA_SLLC", _("Toyota SLLC")

    # Honda
    HONDA_TYPE_2 = "HONDA_TYPE_2", _("Honda Type 2")

    # Nissan
    NISSAN_L248 = "NISSAN_L248", _("Nissan L248")
    NISSAN_L250 = "NISSAN_L250", _("Nissan L250")

    # Hyundai / Kia
    HYUNDAI_KIA_LLC = "HYUNDAI_KIA_LLC", _("Hyundai/Kia Long Life Coolant")

class LiquideFreinsQualite(models.TextChoices):
        DOT3 = 'DOT 3', _("DOT 3")
        DOT4 = 'DOT 4', _("DOT 4")
        DOT5 = 'DOT 5', _("DOT 5")
        DOT51 = 'DOT 5.1', _("DOT 5.1")



class LaveGlaceQualite(models.TextChoices):
    HIVER = 'HIVER', _("Hiver")
    ETE = 'ETE', _("Eté")






class HuileBoiteEtat(models.TextChoices):
    SEPTANTE_CINQ = "75W", _("75W")
    SEPTANTE_5_80 = "75W80", _("75W80")
    SEPTANTE_CINQ90  = "75W90", _("75W90")
    QUATRE_20 = "80W", "80W"
    QUATRE_20_90 = "80W90", _("80W90")
    QUATRE_25_90 = "85W90", _("85W90")
    ATF3 = "ATF_III", _("ATF III")
    ATF_DSG = "ATF_DSG", _("ATF DSG")
    ATF_DCT = "ATF_DCT", _("ATF DCT")
    ATF_CVT = "ATF_CVT", _("ATF CVT")
    ATF_DEXRON_II = "ATF_DEXRON_II", _("ATF Dexron II")
    ATF_DEXRON_III = "ATF_DEXRON_III", _("ATF Dexron III")
    ATF_DEXRON_VI = "ATF_DEXRON_VI", _("ATF Dexron VI")
    ATF_MERCON = "ATF_MERCON", _("ATF Mercon")
    ATF_MERCON_V = "ATF_MERCON_V", _("ATF Mercon V")
    ATF_MERCON_LV = "ATF_MERCON_LV", _("ATF Mercon LV")
    ATF_MULTI = "ATF_MULTI", _("ATF Multi Vehicle")
    ATF_WS = "ATF_WS", _("ATF Toyota WS")
    ATF_ZF_LIFEGUARD = "ATF_ZF_LIFEGUARD", _("ZF Lifeguard")
    ATF_MOPAR = "ATF_MOPAR", _("Mopar ATF+4")
    ATF_AISIN = "ATF_AISIN", _("Aisin ATF")
    ATF_MBV236 = "ATF_MBV236", _("Mercedes MB 236.x")
    ATF_VOLVO = "ATF_VOLVO", _("Volvo ATF")
    ATF_HONDA = "ATF_HONDA", _("Honda ATF DW-1")
    ATF_NISSAN = "ATF_NISSAN", _("Nissan Matic")





class HuileBoiteAutoEtat(models.TextChoices):
    ATF3 = "ATF_III", _("ATF III")
    ATF_DSG = "ATF_DSG", _("ATF DSG")
    ATF_DCT = "ATF_DCT", _("ATF DCT")
    ATF_CVT = "ATF_CVT", _("ATF CVT")
    ATF_DEXRON_II = "ATF_DEXRON_II", _("ATF Dexron II")
    ATF_DEXRON_III = "ATF_DEXRON_III", _("ATF Dexron III")
    ATF_DEXRON_VI = "ATF_DEXRON_VI", _("ATF Dexron VI")
    ATF_MERCON = "ATF_MERCON", _("ATF Mercon")
    ATF_MERCON_V = "ATF_MERCON_V", _("ATF Mercon V")
    ATF_MERCON_LV = "ATF_MERCON_LV", _("ATF Mercon LV")
    ATF_MULTI = "ATF_MULTI", _("ATF Multi Vehicle")
    ATF_WS = "ATF_WS", _("ATF Toyota WS")
    ATF_ZF_LIFEGUARD = "ATF_ZF_LIFEGUARD", _("ZF Lifeguard")
    ATF_MOPAR = "ATF_MOPAR", _("Mopar ATF+4")
    ATF_AISIN = "ATF_AISIN", _("Aisin ATF")
    ATF_MBV236 = "ATF_MBV236", _("Mercedes MB 236.x")
    ATF_VOLVO = "ATF_VOLVO", _("Volvo ATF")
    ATF_HONDA = "ATF_HONDA", _("Honda ATF DW-1")
    ATF_NISSAN = "ATF_NISSAN", _("Nissan Matic")


class FabricantAllumage(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")

    OEM = "OEM", _("Origine constructeur (OEM)")

    BOSCH = "BOSCH", _("Bosch")
    NGK = "NGK", _("NGK")
    BERU = "BERU", _("Beru")
    DENSO = "DENSO", _("Denso")
    DELPHI = "DELPHI", _("Delphi")
    HELLA = "HELLA", _("Hella")
    VALEO = "VALEO", _("Valeo")
    BREMBO = "BREMBO", _("Brembo")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    CHAMPION = "CHAMPION", _("Champion")
    BREMI = "BREMI", _("Bremi")
    HITACHI = "HITACHI", _("Hitachi")
    VDO = "VDO", _("VDO")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    FACET = "FACET", _("Facet")
    ERA = "ERA", _("ERA")
    MEYLE = "MEYLE", _("Meyle")
    FEBI = "FEBI", _("Febi Bilstein")

    AUTRE = "AUTRE", _("Autre fabricant")
    INCONNU = "INCONNU", _("Fabricant inconnu")

