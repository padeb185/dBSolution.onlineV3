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

class CoteConduite(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    GAUCHE = "GAUCHE", _("Conduite à gauche")
    DROITE = "CONDUITE", _("Conduite à droite")


class FabricantCarrosserie(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    ORIGINE = "ORIGINE", _("Constructeur OEM")

    THREE_M = "3M", _("3M")
    AGC = "AGC", _("AGC Automotive")
    ALKAR = "ALKAR", _("Alkar")
    AUTOMOTIVE_LIGHTING = "AUTOMOTIVE_LIGHTING", _("Automotive Lighting")
    AXALTA = "AXALTA", _("Axalta")
    BLIC = "BLIC", _("Blic")
    BOSCH = "BOSCH", _("Bosch")
    CARGLASS = "CARGLASS", _("Carglass")
    CROMAX = "CROMAX", _("Cromax")
    DE_BEER = "DE_BEER", _("De Beer")
    DEPO = "DEPO", _("Depo")
    DIEDERICHS = "DIEDERICHS", _("Diederichs")
    DORMAN = "DORMAN", _("Dorman")
    FICOSA = "FICOSA", _("Ficosa")
    FLEX_N_GATE = "FLEX_N_GATE", _("Flex-N-Gate")
    FORVIA = "FORVIA", _("Forvia (Faurecia)")
    FUYAO = "FUYAO", _("Fuyao")
    GENTEX = "GENTEX", _("Gentex")
    GESTAMP = "GESTAMP", _("Gestamp")
    GLASURIT = "GLASURIT", _("Glasurit (BASF)")
    GUARDIAN = "GUARDIAN", _("Guardian Glass")
    HELLA = "HELLA", _("Hella (Forvia)")
    JUMASA = "JUMASA", _("Jumasa")
    KIRCHHOFF = "KIRCHHOFF", _("Kirchhoff Automotive")
    KLOKKERHOLM = "KLOKKERHOLM", _("Klokkerholm")
    KOITO = "KOITO", _("Koito")
    LECHLER = "LECHLER", _("Lechler")
    LESJOFORS = "LESJOFORS", _("Lesjöfors")
    MAGNA = "MAGNA", _("Magna")
    MARELLI = "MARELLI", _("Marelli (Magneti Marelli)")
    MEKRA = "MEKRA", _("Mekra Lang")
    MIPA = "MIPA", _("Mipa")
    MIRKA = "MIRKA", _("Mirka")
    NEXA = "NEXA", _("Nexa Autocolor")
    NOVOL = "NOVOL", _("Novol")
    PLASTIC_OMNIUM = "PLASTIC_OMNIUM", _("OPmobility (Plastic Omnium)")
    OSRAM = "OSRAM", _("Osram")
    PHILIPS = "PHILIPS", _("Philips")
    PILKINGTON = "PILKINGTON", _("Pilkington")
    POLCAR = "POLCAR", _("Polcar")
    PPG = "PPG", _("PPG")
    PRASCO = "PRASCO", _("Prasco")
    RM = "RM", _("R-M (BASF)")
    ROBERLO = "ROBERLO", _("Roberlo")
    SAINT_GOBAIN = "SAINT_GOBAIN", _("Saint-Gobain Sekurit")
    SIGNEDA = "SIGNEDA", _("Signeda")
    SIKA = "SIKA", _("Sika")
    SIKKENS = "SIKKENS", _("Sikkens (AkzoNobel)")
    SMR = "SMR", _("SMR (Motherson)")
    SPIES_HECKER = "SPIES_HECKER", _("Spies Hecker")
    STABILUS = "STABILUS", _("Stabilus (vérins)")
    STANDOX = "STANDOX", _("Standox")
    STANLEY = "STANLEY", _("Stanley Electric")
    SWF = "SWF", _("SWF")
    TEROSON = "TEROSON", _("Teroson (Henkel)")
    TRICO = "TRICO", _("Trico")
    TROTON = "TROTON", _("Troton")
    TYC = "TYC", _("TYC")
    TYG = "TYG", _("TYG (Tong Yang)")
    U_POL = "U_POL", _("U-POL")
    ULO = "ULO", _("Ulo")
    VALEO = "VALEO", _("Valeo")
    VAN_WEZEL = "VAN_WEZEL", _("Van Wezel")
    WEATHERTECH = "WEATHERTECH", _("WeatherTech")
    WURTH = "WURTH", _("Würth")
    XYG = "XYG", _("XYG")
    ZKW = "ZKW", _("ZKW")

    AUTRE = "AUTRE", _("Autre")


class FabricantLubrifiant(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    AISIN = "AISIN", _("Aisin")
    AMSOIL = "AMSOIL", _("Amsoil")
    BMW = "BMW", _("BMW")
    CASTROL = "CASTROL", _("Castrol")
    COMMA = "COMMA", _("Comma")
    ELF = "ELF", _("ELF")
    ENEOS = "ENEOS", _("ENEOS")
    EUROL = "EUROL", _("Eurol")
    FEBI = "FEBI", _("Febi Bilstein")
    FORD = "FORD", _("Ford")
    FUCHS = "FUCHS", _("Fuchs")
    GM = "GM", _("General Motors")
    HONDA = "HONDA", _("Honda")
    HYUNDAI_KIA = "HYUNDAI_KIA", _("Hyundai / Kia")
    KROON_OIL = "KROON_OIL", _("Kroon-Oil")
    LIQUI_MOLY = "LIQUI_MOLY", _("Liqui Moly")
    MANNOL = "MANNOL", _("Mannol")
    MERCEDES = "MERCEDES", _("Mercedes-Benz")
    MOBIL = "MOBIL", _("Mobil 1")
    MOPAR = "MOPAR", _("Mopar")
    MOTUL = "MOTUL", _("Motul")
    NISSAN = "NISSAN", _("Nissan")
    PENRITE = "PENRITE", _("Penrite")
    PENTOSIN = "PENTOSIN", _("Pentosin")
    PETRONAS = "PETRONAS", _("Petronas")
    PSA = "PSA", _("Peugeot / Citroën")
    PORSCHE = "PORSCHE", _("Porsche")
    RAVENOL = "RAVENOL", _("Ravenol")
    REDLINE = "REDLINE", _("Red Line")
    RENAULT = "RENAULT", _("Renault")
    ROWE = "ROWE", _("Rowe")
    SHELL = "SHELL", _("Shell")
    SWAG = "SWAG", _("SWAG")
    TOTAL = "TOTAL", _("TotalEnergies")
    TOYOTA = "TOYOTA", _("Toyota")
    VALVOLINE = "VALVOLINE", _("Valvoline")
    VOLKSWAGEN = "VOLKSWAGEN", _("Volkswagen")
    YACCO = "YACCO", _("Yacco")
    ZF = "ZF", _("ZF")

    AUTRE = "AUTRE", _("Autre")


class FabricantFiltre(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    ALCO = "ALCO", "ALCO Filters"
    ASHIKA = "ASHIKA", "Ashika"
    BALDWIN = "BALDWIN", "Baldwin Filters"
    BLUE_PRINT = "BLUE_PRINT", "Blue Print"
    BOSCH = "BOSCH", "Bosch"
    CHAMPION = "CHAMPION", "Champion"
    COMLINE = "COMLINE", "Comline"
    COOPERSFIAAM = "COOPERSFIAAM", "CoopersFiaam"
    DELPHI = "DELPHI", "Delphi"
    DENCKERMANN = "DENCKERMANN", "Denckermann"
    DONALDSON = "DONALDSON", "Donaldson"
    FEBI = "FEBI", "Febi Bilstein"
    FILTRON = "FILTRON", "Filtron"
    FLEETGUARD = "FLEETGUARD", "Fleetguard"
    FRAM = "FRAM", "Fram"
    HENGST = "HENGST", "Hengst"
    HERTH_BUSS = "HERTH_BUSS", "Herth+Buss"
    JAPANPARTS = "JAPANPARTS", "Japanparts"
    JC_PREMIUM = "JC_PREMIUM", "JC Premium"
    KN = "KN", "KN"
    KNECHT = "KNECHT", "Knecht"
    MAHLE = "MAHLE", "Mahle"
    MANN_FILTER = "MANN_FILTER", "MANN-Filter"
    MAXGEAR = "MAXGEAR", "Maxgear"
    MEYLE = "MEYLE", "Meyle"
    MISFAT = "MISFAT", "Misfat"
    NIPPARTS = "NIPPARTS", "Nipparts"
    OPEN_PARTS = "OPEN_PARTS", "Open Parts"
    PURFLUX = "PURFLUX", "Purflux"
    RIDEX = "RIDEX", "RIDEX"
    SCT = "SCT", "SCT Germany"
    SOFIMA = "SOFIMA", "Sofima"
    SWAG = "SWAG", "SWAG"
    TECNECO = "TECNECO", "Tecneco"
    TOPRAN = "TOPRAN", "Topran"
    UFI = "UFI", "UFI"
    VAICO = "VAICO", "Vaico"
    VALEO = "VALEO", "Valeo"
    WIX = "WIX", "WIX Filters"

    AUTRE = "AUTRE", _("Autre")


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
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    AISIN = "AISIN", "Aisin"
    ALCO = "ALCO", "ALCO Filters"
    ASHIKA = "ASHIKA", "Ashika"
    ATE = "ATE", "ATE"
    AUDI = "AUDI", "Audi"
    BALDWIN = "BALDWIN", "Baldwin"
    BEHR = "BEHR", "Behr"
    BERU = "BERU", "Beru"
    BLUE_PRINT = "BLUE_PRINT", "Blue Print"
    BMW = "BMW", "BMW"
    BOSCH = "BOSCH", "Bosch"
    BREMBO = "BREMBO", "Brembo"
    CHAMPION = "CHAMPION", "Champion"
    CITROEN = "CITROEN", "Citroën"
    COMLINE = "COMLINE", "Comline"
    CONTINENTAL = "CONTINENTAL", "Continental"
    DAYCO = "DAYCO", "Dayco"
    DELPHI = "DELPHI", "Delphi"
    DENCKERMANN = "DENCKERMANN", "Denckermann"
    DENSO = "DENSO", "Denso"
    DONALDSON = "DONALDSON", "Donaldson"
    EXIDE = "EXIDE", "Exide"
    FAG = "FAG", "FAG"
    FEBI_BILSTEIN = "FEBI_BILSTEIN", "Febi Bilstein"
    FERODO = "FERODO", "Ferodo"
    FILTRON = "FILTRON", "Filtron"
    FLEETGUARD = "FLEETGUARD", "Fleetguard"
    FORD = "FORD", "Ford"
    FRAM = "FRAM", "Fram"
    GATES = "GATES", "Gates"
    HELLA = "HELLA", "Hella"
    HENGST = "HENGST", "Hengst"
    HERTH_BUSS = "HERTH_BUSS", "Herth+Buss"
    HONDA = "HONDA", "Honda"
    HYUNDAI = "HYUNDAI", "Hyundai"
    JAPANPARTS = "JAPANPARTS", "Japanparts"
    JC_PREMIUM = "JC_PREMIUM", "JC Premium"
    JURID = "JURID", "Jurid"
    KIA = "KIA", "Kia"
    KNECHT = "KNECHT", "Knecht"
    KOYO = "KOYO", "Koyo"
    LEMFORDER = "LEMFORDER", "Lemförder"
    LUK = "LUK", "LuK"
    MAHLE = "MAHLE", "Mahle"
    MANN_FILTER = "MANN_FILTER", "MANN-Filter"
    MAXGEAR = "MAXGEAR", "Maxgear"
    MERCEDES = "MERCEDES", "Mercedes-Benz"
    MEYLE = "MEYLE", "Meyle"
    MOOG = "MOOG", "Moog"
    NGK = "NGK", "NGK"
    NIPPARTS = "NIPPARTS", "Nipparts"
    NISSAN = "NISSAN", "Nissan"
    NRF = "NRF", "NRF"
    NSK = "NSK", "NSK"
    NTN = "NTN", "NTN"
    OPEL = "OPEL", "Opel"
    OPEN_PARTS = "OPEN_PARTS", "Open Parts"
    OSRAM = "OSRAM", "Osram"
    PAGID = "PAGID", "Pagid"
    PEUGEOT = "PEUGEOT", "Peugeot"
    PHILIPS = "PHILIPS", "Philips"
    PIERBURG = "PIERBURG", "Pierburg"
    PORSCHE = "PORSCHE", "Porsche"
    PURFLUX = "PURFLUX", "Purflux"
    REMSA = "REMSA", "Remsa"
    RENAULT = "RENAULT", "Renault"
    RIDEX = "RIDEX", "RIDEX"
    SACHS = "SACHS", "Sachs"
    SIDEM = "SIDEM", "Sidem"
    SKF = "SKF", "SKF"
    SNR = "SNR", "SNR"
    SOFIMA = "SOFIMA", "Sofima"
    SWAG = "SWAG", "SWAG"
    TEXTAR = "TEXTAR", "Textar"
    TIMKEN = "TIMKEN", "Timken"
    TOPRAN = "TOPRAN", "Topran"
    TOYOTA = "TOYOTA", "Toyota"
    TRW = "TRW", "TRW"
    UFI = "UFI", "UFI"
    VAICO = "VAICO", "Vaico"
    VALEO = "VALEO", "Valeo"
    VARTA = "VARTA", "Varta"
    VDO = "VDO", "VDO"
    VOLKSWAGEN = "VOLKSWAGEN", "Volkswagen"
    WALKER = "WALKER", "Walker"
    WIX = "WIX", "WIX Filters"
    YUASA = "YUASA", "Yuasa"

    AUTRE = "AUTRE", _("Autre")


class TypeHuileDirection(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
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






class FabricantFrein(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    ADVICS = "ADVICS", _("Advics")
    AKEBONO = "AKEBONO", _("Akebono")
    ATE = "ATE", _("ATE")
    BENDIX = "BENDIX", _("Bendix")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    BOSCH = "BOSCH", _("Bosch")
    BREMBO = "BREMBO", _("Brembo")
    CIFAM = "CIFAM", _("Cifam")
    COMLINE = "COMLINE", _("Comline")
    DELPHI = "DELPHI", _("Delphi")
    DIXCEL = "DIXCEL", _("Dixcel")
    DON = "DON", _("DON")
    EBC = "EBC", _("EBC Brakes")
    FEBI = "FEBI", _("Febi Bilstein")
    FERODO = "FERODO", _("Ferodo")
    HELLA = "HELLA", _("Hella")
    HELLA_PAGID = "HELLA_PAGID", _("Hella Pagid")
    HERTH_BUSS = "HERTH_BUSS", _("Herth+Buss")
    ICER = "ICER", _("ICER")
    JAPANPARTS = "JAPANPARTS", _("Japanparts")
    JURID = "JURID", _("Jurid")
    LPR = "LPR", _("LPR")
    MAPCO = "MAPCO", _("Mapco")
    METELLI = "METELLI", _("Metelli")
    MEYLE = "MEYLE", _("Meyle")
    MINTEX = "MINTEX", _("Mintex")
    NIPPARTS = "NIPPARTS", _("Nipparts")
    NISSHINBO = "NISSHINBO", _("Nisshinbo")
    NK = "NK", _("NK")
    PAGID = "PAGID", _("Pagid")
    QUINTON_HAZELL = "QUINTON_HAZELL", _("Quinton Hazell")
    REMSA = "REMSA", _("Remsa")
    ROADHOUSE = "ROADHOUSE", _("Roadhouse")
    SKF = "SKF", _("SKF")
    SNR = "SNR", _("SNR")
    STOPTECH = "STOPTECH", _("StopTech")
    SWAG = "SWAG", _("SWAG")
    TEXTAR = "TEXTAR", _("Textar")
    TOMEX = "TOMEX", _("Tomex")
    TRW = "TRW", _("TRW")
    VALEO = "VALEO", _("Valeo")
    WINMAX = "WINMAX", _("Winmax")
    ZIMMERMANN = "ZIMMERMANN", _("Zimmermann")

    AUTRE = "AUTRE", _("Autre")


class RefroidissementFabricant(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

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
    PETRONAS = "PETRONAS", _("Petronas")
    PEUGEOT_CITROEN = "PEUGEOT_CITROEN", _("Peugeot Citroën")
    PORSCHE = "PORSCHE", _("Porsche")
    PRESTONE = "PRESTONE", _("Prestone")
    PUTOLINE = "PUTOLINE", _("Putoline")
    RAVENOL = "RAVENOL", _("Ravenol")
    RENAULT = "RENAULT", _("Renault")
    REPSOL = "REPSOL", _("Repsol")
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
    VAG = "VAG", _("VAG")
    VALEO = "VALEO", _("Valeo")
    VALVOLINE = "VALVOLINE", _("Valvoline")
    VOLVO = "VOLVO", _("Volvo")
    WOLF = "WOLF", _("Wolf")
    XENUM = "XENUM", _("Xenum")
    YACCO = "YACCO", _("Yacco")
    YAMAHA = "YAMAHA", _("Yamaha")

    AUTRE = "AUTRE", _("Autre")


class FabricantSuspension(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir un fabricant")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    AC_DELCO = "AC_DELCO", _("ACDelco")
    AIR_LIFT = "AIR_LIFT", _("Air Lift")
    AL_KO = "AL_KO", _("AL-KO")
    AP_SPORTFAHRWERKE = "AP_SPORTFAHRWERKE", _("AP Sportfahrwerke")
    ARN_NOTT = "ARNOTT", _("Arnott")
    BC_RACING = "BC_RACING", _("BC Racing")
    BILSTEIN = "BILSTEIN", _("Bilstein")
    BMW = "BMW", _("BMW")
    BOGE = "BOGE", _("Boge")
    BOSCH = "BOSCH", _("Bosch")
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
    KONI = "KONI", _("Koni")
    K_W = "K_W", _("KW Suspensions")
    KAYABA = "KAYABA", _("KYB")
    LEMFORDER = "LEMFORDER", _("Lemförder")
    LESJOFORS = "LESJOFORS", _("Lesjöfors")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    MAPCO = "MAPCO", _("Mapco")
    MAXGEAR = "MAXGEAR", _("Maxgear")
    MERCEDES_BENZ = "MERCEDES_BENZ", _("Mercedes-Benz")
    MEYLE = "MEYLE", _("Meyle")
    MONROE = "MONROE", _("Monroe")
    MOOG = "MOOG", _("Moog")
    NIPPARTS = "NIPPARTS", _("Nipparts")
    NK = "NK", _("NK")
    OPTIMAL = "OPTIMAL", _("Optimal")
    OROPARTS = "OROPARTS", _("Oro Parts")
    PORSCHE = "PORSCHE", _("Porsche")
    PROFIT = "PROFIT", _("Profit")
    QUINTON_HAZELL = "QUINTON_HAZELL", _("Quinton Hazell")
    RENAULT = "RENAULT", _("Renault")
    RIDEX = "RIDEX", _("Ridex")
    SACHS = "SACHS", _("Sachs")
    SNR = "SNR", _("SNR")
    SPIDAN = "SPIDAN", _("Spidan")
    ST_SUSPENSIONS = "ST_SUSPENSIONS", _("ST Suspensions")
    STELLANTIS = "STELLANTIS", _("Stellantis")
    SWAG = "SWAG", _("SWAG")
    TA_TECHNIX = "TA_TECHNIX", _("TA Technix")
    TEIN = "TEIN", _("Tein")
    TOYOTA = "TOYOTA", _("Toyota")
    TRW = "TRW", _("TRW")
    VOGTLAND = "VOGTLAND", _("Vogtland")
    VAG = "VAG", _("Volkswagen Audi Group")
    VOLVO = "VOLVO", _("Volvo")
    WEITEC = "WEITEC", _("Weitec")
    XYZ_RACING = "XYZ_RACING", _("XYZ Racing")
    ZF = "ZF", _("ZF")

    AUTRE = "AUTRE", _("Autre")


class FabricantRoulement(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir un fabricant")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    AIC = "AIC", _("AIC")
    ASHIKA = "ASHIKA", _("Ashika")
    AUTEX = "AUTEX", _("Autex")
    BENDIX = "BENDIX", _("Bendix")
    BGA = "BGA", _("BGA")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    BMW = "BMW", _("BMW")
    BORG_AND_BECK = "BORG_AND_BECK", _("Borg & Beck")
    BTA = "BTA", _("BTA")
    CORTECO = "CORTECO", _("Corteco")
    DAYCO = "DAYCO", _("Dayco")
    DELPHI = "DELPHI", _("Delphi")
    FAG = "FAG", _("FAG")
    FEBEST = "FEBEST", _("Febest")
    FEBI_BILSTEIN = "FEBI_BILSTEIN", _("Febi Bilstein")
    FLENNOR = "FLENNOR", _("Flennor")
    FORD = "FORD", _("Ford")
    GENERAL_MOTORS = "GENERAL_MOTORS", _("General Motors")
    GSP = "GSP", _("GSP")
    HERTH_BUSS = "HERTH_BUSS", _("Herth+Buss")
    HONDA = "HONDA", _("Honda")
    HYUNDAI = "HYUNDAI", _("Hyundai")
    INA = "INA", _("INA")
    JAPANPARTS = "JAPANPARTS", _("Japanparts")
    JAPKO = "JAPKO", _("Japko")
    JP_GROUP = "JP_GROUP", _("JP Group")
    KAMOKA = "KAMOKA", _("Kamoka")
    KAVO_PARTS = "KAVO_PARTS", _("Kavo Parts")
    KIA = "KIA", _("Kia")
    KOYO = "KOYO", _("Koyo")
    LPR = "LPR", _("LPR")
    MAPCO = "MAPCO", _("Mapco")
    MAXGEAR = "MAXGEAR", _("Maxgear")
    MAZDA = "MAZDA", _("Mazda")
    MERCEDES_BENZ = "MERCEDES_BENZ", _("Mercedes-Benz")
    METELLI = "METELLI", _("Metelli")
    MEYLE = "MEYLE", _("Meyle")
    MITSUBISHI = "MITSUBISHI", _("Mitsubishi")
    MOOG = "MOOG", _("Moog")
    NATIONAL = "NATIONAL", _("National")
    NIPPARTS = "NIPPARTS", _("Nipparts")
    NISSAN = "NISSAN", _("Nissan")
    NK = "NK", _("NK")
    NTN = "NTN", _("NTN")
    OPTIMAL = "OPTIMAL", _("Optimal")
    PEX = "PEX", _("PEX")
    PORSCHE = "PORSCHE", _("Porsche")
    QUINTON_HAZELL = "QUINTON_HAZELL", _("Quinton Hazell")
    RENAULT = "RENAULT", _("Renault")
    RIDEX = "RIDEX", _("Ridex")
    RUVILLE = "RUVILLE", _("Ruville")
    SKF = "SKF", _("SKF")
    VKBA = "VKBA", _("SKF VKBA")
    SNR = "SNR", _("SNR")
    SPIDAN = "SPIDAN", _("Spidan")
    STELLANTIS = "STELLANTIS", _("Stellantis")
    SUBARU = "SUBARU", _("Subaru")
    SUZUKI = "SUZUKI", _("Suzuki")
    SWAG = "SWAG", _("SWAG")
    TIMKEN = "TIMKEN", _("Timken")
    TOPRAN = "TOPRAN", _("Topran")
    TOYOTA = "TOYOTA", _("Toyota")
    TRISCAN = "TRISCAN", _("Triscan")
    TRW = "TRW", _("TRW")
    VAICO = "VAICO", _("Vaico")
    VAG = "VAG", _("Volkswagen Audi Group")
    VOLVO = "VOLVO", _("Volvo")
    WHEELPRO = "WHEELPRO", _("WheelPro")
    ZF = "ZF", _("ZF")

    AUTRE = "AUTRE", _("Autre")


class FabricantPneus(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir un fabricant")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

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
    GISLAVED = "GISLAVED", _("Gislaved")
    GITI = "GITI", _("Giti")
    GOFORM = "GOFORM", _("Goform")
    GOODYEAR = "GOODYEAR", _("Goodyear")
    GRENLANDER = "GRENLANDER", _("Grenlander")
    GT_RADIAL = "GT_RADIAL", _("GT Radial")
    HAIDA = "HAIDA", _("Haida")
    HANKOOK = "HANKOOK", _("Hankook")
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
    SAVA = "SAVA", _("Sava")
    SEMPERIT = "SEMPERIT", _("Semperit")
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
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    ACDELCO = "ACDELCO", _("ACDelco")
    AUTOLITE = "AUTOLITE", _("Autolite")
    BERU = "BERU", _("Beru")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    BORGWARNER = "BORGWARNER", _("BorgWarner")
    BOSCH = "BOSCH", _("Bosch")
    BRISK = "BRISK", _("Brisk")
    CHAMPION = "CHAMPION", _("Champion")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("DENSO")
    EYQUEM = "EYQUEM", _("Eyquem")
    FEBI = "FEBI", _("Febi Bilstein")
    HELLA = "HELLA", _("Hella")
    JAPANPARTS = "JAPANPARTS", _("Japanparts")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    MOPAR = "MOPAR", _("Mopar")
    MOTORCRAFT = "MOTORCRAFT", _("Motorcraft")
    NGK = "NGK", _("NGK")
    NPS = "NPS", _("NPS")
    PIERBURG = "PIERBURG", _("Pierburg")
    RIDEX = "RIDEX", _("RIDEX")
    VALEO = "VALEO", _("Valeo")


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
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    ACDELCO = "ACDELCO", _("ACDelco")
    BANNER = "BANNER", _("Banner")
    BOSCH = "BOSCH", _("Bosch")
    CENTRA = "CENTRA", _("Centra")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    EXIDE = "EXIDE", _("Exide")
    FIAMM = "FIAMM", _("Fiamm")
    FULMEN = "FULMEN", _("Fulmen")
    HANKOOK = "HANKOOK", _("Hankook")
    INTERSTATE = "INTERSTATE", _("Interstate")
    MOLL = "MOLL", _("Moll")
    MUTLU = "MUTLU", _("Mutlu")
    ODYSSEY = "ODYSSEY", _("Odyssey")
    OPTIMA = "OPTIMA", _("Optima")
    TAB = "TAB", _("TAB")
    TOPLA = "TOPLA", _("Topla")
    TUDOR = "TUDOR", _("Tudor")
    VARTA = "VARTA", _("Varta")
    YUASA = "YUASA", _("Yuasa")

    AUTRE = "AUTRE", _("Autre")


class FabricantEchappement(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    AKRAPOVIC = "AKRAPOVIC", _("Akrapovič")
    ARROW = "ARROW", _("Arrow")
    BASTUCK = "BASTUCK", _("Bastuck")
    BMW = "BMW", _("BMW")
    BORLA = "BORLA", _("Borla")
    BOSAL = "BOSAL", _("Bosal")
    COBRA = "COBRA", _("Cobra Sport")
    EBERSPACHER = "EBERSPACHER", _("Eberspächer")
    EISENMANN = "EISENMANN", _("Eisenmann")
    ERNST = "ERNST", _("Ernst")
    FOX = "FOX", _("FOX")
    IMASAF = "IMASAF", _("IMASAF")
    MAGNAFLOW = "MAGNAFLOW", _("MagnaFlow")
    MILLTEK = "MILLTEK", _("Milltek Sport")
    MIVV = "MIVV", _("MIVV")
    POLMO = "POLMO", _("Polmo")
    PORSCHE = "PORSCHE", _("Porsche")
    RAGAZZON = "RAGAZZON", _("Ragazzon")
    REMUS = "REMUS", _("Remus")
    SCORPION = "SCORPION", _("Scorpion")
    SUPERSPRINT = "SUPERSPRINT", _("Supersprint")
    WALKER = "WALKER", _("Walker")

    AUTRE = "AUTRE", _("Autre")


class FabricantCapteurEchappement(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    OEM = "OEM", _("Constructeur OEM")

    BOSCH = "BOSCH", _("Bosch")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    EPS = "EPS", _("EPS")
    ERA = "ERA", _("ERA")
    FACET = "FACET", _("Facet")
    FAE = "FAE", _("FAE")
    FEBI = "FEBI", _("Febi Bilstein")
    HELLA = "HELLA", _("Hella")
    HITACHI = "HITACHI", _("Hitachi")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    METZGER = "METZGER", _("Metzger")
    MEYLE = "MEYLE", _("Meyle")
    NGK = "NGK", _("NGK / NTK")
    PIERBURG = "PIERBURG", _("Pierburg")
    RIDEX = "RIDEX", _("Ridex")
    SIDAT = "SIDAT", _("SIDAT")
    STARK = "STARK", _("Stark")
    TOPRAN = "TOPRAN", _("Topran")
    VALEO = "VALEO", _("Valeo")
    VDO = "VDO", _("VDO")
    VEMO = "VEMO", _("Vemo")
    WALKER = "WALKER", _("Walker Products")

    AUTRE = "AUTRE", _("Autre")

class FabricantCapteur(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    OEM = "OEM", _("Constructeur OEM")

    BOSCH = "BOSCH", _("Bosch")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    EPS = "EPS", _("EPS")
    ERA = "ERA", _("ERA")
    FACET = "FACET", _("Facet")
    FAE = "FAE", _("FAE")
    FEBI = "FEBI", _("Febi Bilstein")
    HELLA = "HELLA", _("Hella")
    HITACHI = "HITACHI", _("Hitachi")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    METZGER = "METZGER", _("Metzger")
    MEYLE = "MEYLE", _("Meyle")
    NGK = "NGK", _("NGK / NTK")
    PIERBURG = "PIERBURG", _("Pierburg")
    RIDEX = "RIDEX", _("Ridex")
    SIDAT = "SIDAT", _("SIDAT")
    STARK = "STARK", _("Stark")
    TOPRAN = "TOPRAN", _("Topran")
    VALEO = "VALEO", _("Valeo")
    VDO = "VDO", _("VDO")
    VEMO = "VEMO", _("Vemo")
    WALKER = "WALKER", _("Walker Products")

    AUTRE = "AUTRE", _("Autre")


class FabricantSilentBloc(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    OEM = "OEM", _("Constructeur OEM")

    BIRTH = "BIRTH", _("Birth")
    CORTECO = "CORTECO", _("Corteco")
    DELPHI = "DELPHI", _("Delphi")
    FEBI = "FEBI", _("Febi Bilstein")
    LEMFORDER = "LEMFORDER", _("Lemförder")
    MAPCO = "MAPCO", _("Mapco")
    METZGER = "METZGER", _("Metzger")
    MEYLE = "MEYLE", _("Meyle")
    MOOG = "MOOG", _("Moog")
    OPTIMAL = "OPTIMAL", _("Optimal")
    POWERFLEX = "POWERFLEX", _("Powerflex")
    RIDEX = "RIDEX", _("Ridex")
    SACHS = "SACHS", _("Sachs")
    SASIC = "SASIC", _("Sasic")
    SIDEM = "SIDEM", _("Sidem")
    SKF = "SKF", _("SKF")
    SNR = "SNR", _("SNR")
    STARK = "STARK", _("Stark")
    STRONGFLEX = "STRONGFLEX", _("Strongflex")
    SUPERPRO = "SUPERPRO", _("SuperPro")
    SWAG = "SWAG", _("SWAG")
    TOPRAN = "TOPRAN", _("Topran")
    TRW = "TRW", _("TRW")
    VAICO = "VAICO", _("Vaico")

    AUTRE = "AUTRE", _("Autre")


class CourroieDistributionFabricant(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    ORIGINE = "ORIGINE", _("Constructeur OEM")

    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    BOSCH = "BOSCH", _("Bosch")
    CONTINENTAL = "CONTINENTAL", _("Continental / ContiTech")
    DAYCO = "DAYCO", _("Dayco")
    DOLZ = "DOLZ", _("DOLZ")
    FEBI = "FEBI", _("Febi Bilstein")
    GATES = "GATES", _("Gates")
    GRAF = "GRAF", _("GRAF")
    HEPU = "HEPU", _("HEPU")
    HUTCHINSON = "HUTCHINSON", _("Hutchinson")
    INA = "INA", _("INA")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    METELLI = "METELLI", _("Metelli")
    MEYLE = "MEYLE", _("Meyle")
    OPTIBELT = "OPTIBELT", _("Optibelt")
    QUINTON_HAZELL = "QUINTON_HAZELL", _("Quinton Hazell")
    SKF = "SKF", _("SKF")
    SNR = "SNR", _("SNR")
    SWAG = "SWAG", _("SWAG")

    AUTRE = "AUTRE", _("Autre")


class FabricantTurbo(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    AISIN = "AISIN", _("Aisin")
    ALANKO = "ALANKO", _("ALANKO")
    BE_TURBO = "BE_TURBO", _("BE Turbo")
    BORGWARNER = "BORGWARNER", _("BorgWarner")
    BOSCH_MAHLE = "BOSCH_MAHLE", _("Bosch Mahle Turbo Systems")
    BTS_TURBO = "BTS_TURBO", _("BTS Turbo")
    COMP_TURBO = "COMP_TURBO", _("Comp Turbo")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    CUMMINS = "CUMMINS", _("Cummins Turbo Technologies")
    DELPHI = "DELPHI", _("Delphi")
    ELSTOCK = "ELSTOCK", _("Elstock")
    GARRETT = "GARRETT", _("Garrett")
    HITACHI = "HITACHI", _("Hitachi")
    HOLSET = "HOLSET", _("Holset")
    HONEYWELL = "HONEYWELL", _("Honeywell")
    IHI = "IHI", _("IHI")
    JRONE = "JRONE", _("JRone")
    KKK = "KKK", _("KKK")
    LOBA = "LOBA", _("LOBA Motorsport")
    LUCAS = "LUCAS", _("Lucas")
    MAHLE = "MAHLE", _("MAHLE")
    MELETT = "MELETT", _("Melett")
    MITSUBISHI = "MITSUBISHI", _("Mitsubishi")
    MHI = "MHI", _("Mitsubishi Heavy Industries (MHI)")
    MOTAIR = "MOTAIR", _("Motair")
    NISSENS = "NISSENS", _("Nissens")
    NRF = "NRF", _("NRF")
    PRECISION = "PRECISION", _("Precision Turbo & Engine")
    PURE_TURBOS = "PURE_TURBOS", _("Pure Turbos")
    RIDEX = "RIDEX", _("RIDEX")
    ROTOMASTER = "ROTOMASTER", _("Rotomaster")
    SCHWITZER = "SCHWITZER", _("Schwitzer")
    SL_TURBO = "SL_TURBO", _("SL Turbo")
    STARK = "STARK", _("STARK")
    TTE = "TTE", _("The Turbo Engineers (TTE)")
    TIAL = "TIAL", _("TiAL Sport")
    TOYOTA = "TOYOTA", _("Toyota")
    TURBO_MOTOR = "TURBO_MOTOR", _("Turbo Motor")
    TURBO_TECHNICS = "TURBO_TECHNICS", _("Turbo Technics")
    TURBO_S_M = "TURBO_S_M", _("Turbo's Hoet")
    TURBONETICS = "TURBONETICS", _("Turbonetics")
    TURBOSMART = "TURBOSMART", _("Turbosmart")
    WEISTEC = "WEISTEC", _("Weistec")

    AUTRE = "AUTRE", _("Autre")


class FabricantIntercooler(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    ABAKUS = "ABAKUS", _("ABAKUS")
    AIRTEC = "AIRTEC", _("AIRTEC Motorsport")
    AMS = "AMS", _("AMS Performance")
    APR = "APR", _("APR")
    AVA = "AVA", _("AVA Cooling Systems")
    BEHR = "BEHR", _("Behr")
    BORGWARNER = "BORGWARNER", _("BorgWarner")
    COBB = "COBB", _("COBB Tuning")
    CSF = "CSF", _("CSF")
    CTS_TURBO = "CTS_TURBO", _("CTS Turbo")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    DINAN = "DINAN", _("Dinan")
    DO88 = "DO88", _("do88")
    FEBI = "FEBI", _("FEBI Bilstein")
    FORGE = "FORGE", _("Forge Motorsport")
    GARRETT = "GARRETT", _("Garrett")
    HANON = "HANON", _("Hanon Systems")
    HELLA = "HELLA", _("HELLA")
    IHI = "IHI", _("IHI")
    JP_GROUP = "JP_GROUP", _("JP Group")
    KALE = "KALE", _("KALE")
    KOYORAD = "KOYORAD", _("Koyorad")
    MAHLE = "MAHLE", _("MAHLE")
    MARELLI = "MARELLI", _("Marelli")
    MAXGEAR = "MAXGEAR", _("MAXGEAR")
    METZGER = "METZGER", _("Metzger")
    MEYLE = "MEYLE", _("MEYLE")
    MISHIMOTO = "MISHIMOTO", _("Mishimoto")
    MITSUBISHI = "MITSUBISHI", _("Mitsubishi")
    MODINE = "MODINE", _("Modine")
    NISSENS = "NISSENS", _("Nissens")
    NRF = "NRF", _("NRF")
    PRASCO = "PRASCO", _("Prasco")
    PROALLOY = "PROALLOY", _("Pro Alloy")
    PWR = "PWR", _("PWR")
    RIDEX = "RIDEX", _("RIDEX")
    SANDEN = "SANDEN", _("Sanden")
    STARK = "STARK", _("STARK")
    THERMOTEC = "THERMOTEC", _("Thermotec")
    TURBOSMART = "TURBOSMART", _("Turbosmart")
    TYC = "TYC", _("TYC")
    VALEO = "VALEO", _("Valeo")
    VAN_WEZEL = "VAN_WEZEL", _("Van Wezel")
    WAGNER_TUNING = "WAGNER_TUNING", _("Wagner Tuning")

    AUTRE = "AUTRE", _("Autre")


class FabricantVanneEGR(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    ABAKUS = "ABAKUS", _("ABAKUS")
    AISIN = "AISIN", _("Aisin")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    BOSCH = "BOSCH", _("Bosch")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    ERA = "ERA", _("ERA")
    ESEN_SKV = "ESEN_SKV", _("ESEN SKV")
    FACET = "FACET", _("Facet")
    FEBI = "FEBI", _("FEBI Bilstein")
    FISPA = "FISPA", _("FISPA")
    HELLA = "HELLA", _("HELLA")
    HERTH_BUSS = "HERTH_BUSS", _("Herth+Buss")
    HITACHI = "HITACHI", _("Hitachi")
    MAHLE = "MAHLE", _("MAHLE")
    MAPCO = "MAPCO", _("MAPCO")
    MARELLI = "MARELLI", _("Marelli")
    MAXGEAR = "MAXGEAR", _("MAXGEAR")
    MEAT_DORIA = "MEAT_DORIA", _("Meat & Doria")
    METZGER = "METZGER", _("Metzger")
    MEYLE = "MEYLE", _("MEYLE")
    NRF = "NRF", _("NRF")
    NTY = "NTY", _("NTY")
    PIERBURG = "PIERBURG", _("Pierburg")
    QUINTON_HAZELL = "QUINTON_HAZELL", _("Quinton Hazell")
    RIDEX = "RIDEX", _("RIDEX")
    SIDAT = "SIDAT", _("SIDAT")
    STARK = "STARK", _("STARK")
    SWAG = "SWAG", _("SWAG")
    TOPRAN = "TOPRAN", _("Topran")
    TRISCAN = "TRISCAN", _("Triscan")
    VALEO = "VALEO", _("Valeo")
    VDO = "VDO", _("VDO")
    VEMO = "VEMO", _("VEMO")
    WAHLER = "WAHLER", _("Wahler")

    AUTRE = "AUTRE", _("Autre")


class FabricantDurite(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    ABAKUS = "ABAKUS", _("ABAKUS")
    AIRTEC = "AIRTEC", _("AIRTEC Motorsport")
    BEHR = "BEHR", _("Behr")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    BOSCH = "BOSCH", _("Bosch")
    COHLINE = "COHLINE", _("Cohline")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    CONTITECH = "CONTITECH", _("ContiTech")
    DAYCO = "DAYCO", _("Dayco")
    DELPHI = "DELPHI", _("Delphi")
    DO88 = "DO88", _("do88")
    FEBI = "FEBI", _("FEBI Bilstein")
    FORGE = "FORGE", _("Forge Motorsport")
    FREUDENBERG = "FREUDENBERG", _("Freudenberg")
    GATES = "GATES", _("Gates")
    HELLA = "HELLA", _("HELLA")
    HERTH_BUSS = "HERTH_BUSS", _("Herth+Buss")
    HUTCHINSON = "HUTCHINSON", _("Hutchinson")
    IMPERGOM = "IMPERGOM", _("Impergom")
    JP_GROUP = "JP_GROUP", _("JP Group")
    MAHLE = "MAHLE", _("MAHLE")
    MAPCO = "MAPCO", _("MAPCO")
    MAXGEAR = "MAXGEAR", _("MAXGEAR")
    METZGER = "METZGER", _("Metzger")
    MEYLE = "MEYLE", _("MEYLE")
    MISHIMOTO = "MISHIMOTO", _("Mishimoto")
    NISSENS = "NISSENS", _("Nissens")
    NORMA = "NORMA", _("NORMA Group")
    NRF = "NRF", _("NRF")
    PARKER = "PARKER", _("Parker")
    PIERBURG = "PIERBURG", _("Pierburg")
    RAPRO = "RAPRO", _("Rapro")
    RIDEX = "RIDEX", _("RIDEX")
    SAMCO = "SAMCO", _("Samco Sport")
    STARK = "STARK", _("STARK")
    SWAG = "SWAG", _("SWAG")
    TEKNIKUM = "TEKNIKUM", _("Teknikum")
    THERMOTEC = "THERMOTEC", _("Thermotec")
    TOPRAN = "TOPRAN", _("Topran")
    TRISCAN = "TRISCAN", _("Triscan")
    VAICO = "VAICO", _("VAICO")
    VALEO = "VALEO", _("Valeo")
    VERITAS = "VERITAS", _("Veritas")
    WAGNER_TUNING = "WAGNER_TUNING", _("Wagner Tuning")

    AUTRE = "AUTRE", _("Autre")


class FabricantAlternateur(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    ACDELCO = "ACDELCO", _("ACDelco")
    ACKOJAP = "ACKOJAP", _("ACKOJA")
    ALANKO = "ALANKO", _("Alanko")
    AS_PL = "AS_PL", _("AS-PL")
    AUTEX = "AUTEX", _("Autex")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    BOSCH = "BOSCH", _("Bosch")
    BV_PSH = "BV_PSH", _("BV PSH")
    CASCO = "CASCO", _("Casco")
    CEVAM = "CEVAM", _("CEVAM")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    EAI = "EAI", _("EAI")
    ELSTOCK = "ELSTOCK", _("Elstock")
    ERA = "ERA", _("ERA")
    ERA_BENELUX = "ERA_BENELUX", _("ERA Benelux")
    EUROTEC = "EUROTEC", _("Eurotec")
    FEBI = "FEBI", _("Febi Bilstein")
    HC_CARGO = "HC_CARGO", _("HC-Cargo")
    HELLA = "HELLA", _("Hella")
    HERTH_BUSS = "HERTH_BUSS", _("Herth+Buss")
    HITACHI = "HITACHI", _("Hitachi")
    JP_GROUP = "JP_GROUP", _("JP Group")
    LAUBER = "LAUBER", _("Lauber")
    LUCAS = "LUCAS", _("Lucas")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    MAHLE = "MAHLE", _("Mahle")
    MANDO = "MANDO", _("Mando")
    MAPCO = "MAPCO", _("Mapco")
    MEAT_DORIA = "MEAT_DORIA", _("Meat & Doria")
    MITSUBISHI = "MITSUBISHI", _("Mitsubishi Electric")
    MOBILETRON = "MOBILETRON", _("Mobiletron")
    MOPAR = "MOPAR", _("Mopar")
    MOTORCRAFT = "MOTORCRAFT", _("Motorcraft")
    NIPPARTS = "NIPPARTS", _("Nipparts")
    POWERMAX = "POWERMAX", _("PowerMax")
    PRESTOLITE = "PRESTOLITE", _("Prestolite")
    QUINTON_HAZELL = "QUINTON_HAZELL", _("Quinton Hazell")
    REMY = "REMY", _("Remy")
    RIDEX = "RIDEX", _("Ridex")
    ROTOVIS = "ROTOVIS", _("Rotovis")
    SANDO = "SANDO", _("Sando")
    SNRA = "SNRA", _("SNRA")
    STARK = "STARK", _("Stark")
    TRW = "TRW", _("TRW")
    VALEO = "VALEO", _("Valeo")
    VDO = "VDO", _("VDO")
    VISTEON = "VISTEON", _("Visteon")
    WAI = "WAI", _("WAI Global")

    AUTRE = "AUTRE", _("Autre")


class FabricantCourroie(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    ACKOJA = "ACKOJA", _("ACKOJA")
    ASHIKA = "ASHIKA", _("Ashika")
    BANDO = "BANDO", _("Bando")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    BOSCH = "BOSCH", _("Bosch")
    CONTINENTAL = "CONTINENTAL", _("Continental / ContiTech")
    DAYCO = "DAYCO", _("Dayco")
    DOLZ = "DOLZ", _("Dolz")
    FEBI = "FEBI", _("Febi Bilstein")
    GATES = "GATES", _("Gates")
    GRAF = "GRAF", _("Graf")
    HEPU = "HEPU", _("HEPU")
    HERTH_BUSS = "HERTH_BUSS", _("Herth+Buss")
    HUTCHINSON = "HUTCHINSON", _("Hutchinson")
    INA = "INA", _("INA")
    JAPANPARTS = "JAPANPARTS", _("Japanparts")
    KAVO_PARTS = "KAVO_PARTS", _("Kavo Parts")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    MAPCO = "MAPCO", _("Mapco")
    METELLI = "METELLI", _("Metelli")
    MEYLE = "MEYLE", _("Meyle")
    MITSUBOSHI = "MITSUBOSHI", _("Mitsuboshi")
    NIPPARTS = "NIPPARTS", _("Nipparts")
    OPTIBELT = "OPTIBELT", _("Optibelt")
    QUINTON_HAZELL = "QUINTON_HAZELL", _("Quinton Hazell")
    RIDEX = "RIDEX", _("Ridex")
    SKF = "SKF", _("SKF")
    SNR = "SNR", _("SNR")
    STARK = "STARK", _("Stark")
    SWAG = "SWAG", _("SWAG")
    TOPRAN = "TOPRAN", _("Topran")
    TRISCAN = "TRISCAN", _("Triscan")
    VAICO = "VAICO", _("Vaico")
    VALEO = "VALEO", _("Valeo")

    AUTRE = "AUTRE", _("Autre")


class FabricantEmbrayage(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    OEM = "OEM", _("Constructeur OEM")

    ACT = "ACT", _("ACT (Advanced Clutch Technology)")
    AISIN = "AISIN", _("AISIN")
    ALFA_ROMEO = "ALFA_ROMEO", _("Alfa Romeo Original")
    AP_RACING = "AP_RACING", _("AP Racing")
    ASHIKA = "ASHIKA", _("ASHIKA")
    ATS = "ATS", _("ATS")
    AUDI = "AUDI", _("Audi Original")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    BMW = "BMW", _("BMW Original")
    BORG_BECK = "BORG_BECK", _("Borg & Beck")
    BORGWARNER = "BORGWARNER", _("BorgWarner")
    CARBONETIC = "CARBONETIC", _("Carbonetic")
    CEI = "CEI", _("CEI")
    CENTERFORCE = "CENTERFORCE", _("Centerforce")
    CITROEN = "CITROEN", _("Citroën Original")
    CLUTCH_MASTERS = "CLUTCH_MASTERS", _("Clutch Masters")
    COMPETITION_CLUTCH = "COMPETITION_CLUTCH", _("Competition Clutch")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    CUSCO = "CUSCO", _("CUSCO")
    DACIA = "DACIA", _("Dacia Original")
    DENCKERMANN = "DENCKERMANN", _("Denckermann")
    DKM = "DKM", _("DKM Clutch")
    EATON = "EATON", _("Eaton")
    EURORICAMBI = "EURORICAMBI", _("Euroricambi")
    EXEDY = "EXEDY", _("EXEDY")
    FCC = "FCC", _("F.C.C.")
    INCONNU = "INCONNU", _("Fabricant inconnu")
    FAST = "FAST", _("FAST")
    FCC_JAPAN = "FCC_JAPAN", _("FCC Japan")
    FEBI = "FEBI", _("febi bilstein")
    FIAT = "FIAT", _("Fiat Original")
    FIDANZA = "FIDANZA", _("Fidanza")
    FORD = "FORD", _("Ford Original")
    GREDDY = "GREDDY", _("GReddy / TRUST")
    HAMMER = "HAMMER", _("Hammer Kupplungen")
    HAYS = "HAYS", _("Hays Clutches")
    HELIX = "HELIX", _("Helix Autosport")
    HKS = "HKS", _("HKS")
    HONDA = "HONDA", _("Honda Original")
    HYUNDAI = "HYUNDAI", _("Hyundai Original")
    JAGUAR = "JAGUAR", _("Jaguar Original")
    JAPANPARTS = "JAPANPARTS", _("Japanparts")
    JAPKO = "JAPKO", _("JAPKO")
    JP_GROUP = "JP_GROUP", _("JP Group")
    JUN = "JUN", _("JUN Auto")
    KAMOKA = "KAMOKA", _("KAMOKA")
    KAWE = "KAWE", _("KAWE")
    KIA = "KIA", _("Kia Original")
    KNORR_BREMSE = "KNORR_BREMSE", _("Knorr-Bremse")
    LANCIA = "LANCIA", _("Lancia Original")
    LAND_ROVER = "LAND_ROVER", _("Land Rover Original")
    LEXUS = "LEXUS", _("Lexus Original")
    LIPE = "LIPE", _("LIPE Clutch")
    LPR = "LPR", _("LPR")
    LUK = "LUK", _("LuK / Schaeffler")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    MANTIC = "MANTIC", _("Mantic Clutch")
    MAPCO = "MAPCO", _("MAPCO")
    MAXGEAR = "MAXGEAR", _("MAXGEAR")
    MAZDA = "MAZDA", _("Mazda Original")
    MCLEOD = "MCLEOD", _("McLeod Racing")
    MECARM = "MECARM", _("MECARM")
    MERCEDES = "MERCEDES", _("Mercedes-Benz Original")
    MEYLE = "MEYLE", _("MEYLE")
    MINI = "MINI", _("MINI Original")
    MITSUBISHI = "MITSUBISHI", _("Mitsubishi Original")
    NATIONAL = "NATIONAL", _("National")
    NISMO = "NISMO", _("NISMO")
    NISSAN = "NISSAN", _("Nissan Original")
    NISSIN = "NISSIN", _("Nissin")
    NK = "NK", _("NK")
    NPC = "NPC", _("NPC Performance Clutches")
    NSK = "NSK", _("NSK")
    ORC = "ORC", _("Ogura Racing Clutch (ORC)")
    OPEL = "OPEL", _("Opel Original")
    OS_GIKEN = "OS_GIKEN", _("OS Giken")
    PEUGEOT = "PEUGEOT", _("Peugeot Original")
    PORSCHE = "PORSCHE", _("Porsche Original")
    QUARTER_MASTER = "QUARTER_MASTER", _("Quarter Master")
    QH = "QH", _("Quinton Hazell")
    RAICAM = "RAICAM", _("Raicam")
    RAM = "RAM", _("RAM Clutches")
    RENAULT = "RENAULT", _("Renault Original")
    RIDEX = "RIDEX", _("RIDEX")
    SACHS = "SACHS", _("SACHS / ZF")
    SAMKO = "SAMKO", _("SAMKO")
    SETCO = "SETCO", _("Setco Automotive")
    SOUTH_BEND = "SOUTH_BEND", _("South Bend Clutch")
    SPEC = "SPEC", _("SPEC Clutch")
    STARK = "STARK", _("STARK")
    STARLINE = "STARLINE", _("Starline")
    STATIM = "STATIM", _("STATIM")
    STI = "STI", _("STI")
    SUBARU = "SUBARU", _("Subaru Original")
    SUZUKI = "SUZUKI", _("Suzuki Original")
    TILTON = "TILTON", _("Tilton Engineering")
    TODA = "TODA", _("Toda Racing")
    TOYOTA = "TOYOTA", _("Toyota Original")
    TRD = "TRD", _("TRD")
    TWIN_DISC = "TWIN_DISC", _("Twin Disc")
    VALEO = "VALEO", _("Valeo")
    VOLKSWAGEN = "VOLKSWAGEN", _("Volkswagen Original")
    VOLVO = "VOLVO", _("Volvo Original")
    WABCO = "WABCO", _("WABCO / ZF")
    XTREME = "XTREME", _("Xtreme Clutch")
    TIELIU = "TIELIU", _("Zhejiang Tieliu")

    AUTRE = "AUTRE", _("Autre fabricant")


class FabricantJointSpi(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    OEM = "OEM", _("Constructeur OEM")

    AJUSA = "AJUSA", _("Ajusa")
    ALFA_ROMEO = "ALFA_ROMEO", _("Alfa Romeo Original")
    ARS = "ARS", _("ARS")
    ASHIKA = "ASHIKA", _("ASHIKA")
    AUDI = "AUDI", _("Audi Original")
    AUTOMEGA = "AUTOMEGA", _("AUTOMEGA")
    BGA = "BGA", _("BGA")
    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    BMW = "BMW", _("BMW Original")
    CITROEN = "CITROEN", _("Citroën Original")
    CORTECO = "CORTECO", _("Corteco")
    CUPRA = "CUPRA", _("CUPRA Original")
    DACIA = "DACIA", _("Dacia Original")
    DS = "DS", _("DS Automobiles Original")
    ELRING = "ELRING", _("Elring")
    INCONNU = "INCONNU", _("Fabricant inconnu")
    FAG = "FAG", _("FAG / Schaeffler")
    FAI = "FAI", _("FAI AutoParts")
    FEBEST = "FEBEST", _("FEBEST")
    FEBI = "FEBI", _("febi bilstein")
    FERRARI = "FERRARI", _("Ferrari Original")
    FIAT = "FIAT", _("Fiat Original")
    FORD = "FORD", _("Ford Original")
    FREUDENBERG = "FREUDENBERG", _("Freudenberg")
    GSP = "GSP", _("GSP")
    HONDA = "HONDA", _("Honda Original")
    HYUNDAI = "HYUNDAI", _("Hyundai Original")
    IMPERGOM = "IMPERGOM", _("IMPERGOM")
    INA = "INA", _("INA / Schaeffler")
    INFINITI = "INFINITI", _("Infiniti Original")
    JAGUAR = "JAGUAR", _("Jaguar Original")
    JAPANPARTS = "JAPANPARTS", _("Japanparts")
    JAPKO = "JAPKO", _("JAPKO")
    JP_GROUP = "JP_GROUP", _("JP Group")
    KACO = "KACO", _("KACO")
    KIA = "KIA", _("Kia Original")
    KOYO = "KOYO", _("Koyo / JTEKT")
    LANCIA = "LANCIA", _("Lancia Original")
    LAND_ROVER = "LAND_ROVER", _("Land Rover Original")
    LEXUS = "LEXUS", _("Lexus Original")
    MAPCO = "MAPCO", _("MAPCO")
    MASERATI = "MASERATI", _("Maserati Original")
    MASUMA = "MASUMA", _("Masuma")
    MAXGEAR = "MAXGEAR", _("MAXGEAR")
    MAZDA = "MAZDA", _("Mazda Original")
    MERCEDES = "MERCEDES", _("Mercedes-Benz Original")
    METZGER = "METZGER", _("Metzger")
    MEYLE = "MEYLE", _("MEYLE")
    MINI = "MINI", _("MINI Original")
    MITSUBISHI = "MITSUBISHI", _("Mitsubishi Original")
    MUSASHI = "MUSASHI", _("Musashi Oil Seal")
    NAK = "NAK", _("NAK")
    NISSAN = "NISSAN", _("Nissan Original")
    NOK = "NOK", _("NOK")
    NSK = "NSK", _("NSK")
    NTN = "NTN", _("NTN")
    SNR = "SNR", _("NTN-SNR")
    OPEL = "OPEL", _("Opel Original")
    ORIGINAL_IMPERIUM = "ORIGINAL_IMPERIUM", _("Original Imperium")
    PARKER = "PARKER", _("Parker")
    PAYEN = "PAYEN", _("Payen")
    PEUGEOT = "PEUGEOT", _("Peugeot Original")
    PORSCHE = "PORSCHE", _("Porsche Original")
    RENAULT = "RENAULT", _("Renault Original")
    RIDEX = "RIDEX", _("RIDEX")
    SAAB = "SAAB", _("Saab Original")
    SAKAGAMI = "SAKAGAMI", _("Sakagami")
    SEAT = "SEAT", _("SEAT Original")
    SKF = "SKF", _("SKF")
    SKODA = "SKODA", _("Škoda Original")
    STARK = "STARK", _("STARK")
    SUBARU = "SUBARU", _("Subaru Original")
    SUZUKI = "SUZUKI", _("Suzuki Original")
    SWAG = "SWAG", _("SWAG")
    TIMKEN = "TIMKEN", _("Timken")
    TOPRAN = "TOPRAN", _("TOPRAN")
    TOYOTA = "TOYOTA", _("Toyota Original")
    TRELLEBORG = "TRELLEBORG", _("Trelleborg")
    TRUCKTEC = "TRUCKTEC", _("TRUCKTEC Automotive")
    VAICO = "VAICO", _("VAICO")
    VICTOR_REINZ = "VICTOR_REINZ", _("Victor Reinz")
    VOLKSWAGEN = "VOLKSWAGEN", _("Volkswagen Original")
    VOLVO = "VOLVO", _("Volvo Original")

    AUTRE = "AUTRE", _("Autre fabricant")


class FabricantPompeCarburant(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    OEM = "OEM", _("Constructeur OEM")

    BOSCH = "BOSCH", _("Bosch")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    INCONNU = "INCONNU", _("Fabricant inconnu")
    HITACHI = "HITACHI", _("Hitachi")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    PIERBURG = "PIERBURG", _("Pierburg")
    TI_AUTOMOTIVE = "TI_AUTOMOTIVE", _("TI Automotive")
    VDO = "VDO", _("VDO")
    WALBRO = "WALBRO", _("Walbro")

    AUTRE = "AUTRE", _("Autre fabricant")


class FabricantPompeHautePression(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    OEM = "OEM", _("Constructeur OEM")

    BOSCH = "BOSCH", _("Bosch")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    INCONNU = "INCONNU", _("Fabricant inconnu")
    HITACHI = "HITACHI", _("Hitachi")
    VDO = "VDO", _("VDO")

    AUTRE = "AUTRE", _("Autre fabricant")


class FabricantRampeInjection(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    OEM = "OEM", _("Constructeur OEM")

    BOSCH = "BOSCH", _("Bosch")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    INCONNU = "INCONNU", _("Fabricant inconnu")
    HITACHI = "HITACHI", _("Hitachi")
    VDO = "VDO", _("VDO")

    AUTRE = "AUTRE", _("Autre fabricant")


class FabricantCapteurPressionRampe(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    OEM = "OEM", _("Constructeur OEM")

    BOSCH = "BOSCH", _("Bosch")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    INCONNU = "INCONNU", _("Fabricant inconnu")
    FACET = "FACET", _("Facet")
    FAE = "FAE", _("FAE")
    HELLA = "HELLA", _("Hella")
    VDO = "VDO", _("VDO")

    AUTRE = "AUTRE", _("Autre fabricant")


class FabricantTuyauxHautePression(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    OEM = "OEM", _("Constructeur OEM")

    BOSCH = "BOSCH", _("Bosch")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    INCONNU = "INCONNU", _("Fabricant inconnu")

    AUTRE = "AUTRE", _("Autre fabricant")


class FabricantInjecteur(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    OEM = "OEM", _("Constructeur OEM")

    BOSCH = "BOSCH", _("Bosch")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    INCONNU = "INCONNU", _("Fabricant inconnu")
    HITACHI = "HITACHI", _("Hitachi")
    KEIHIN = "KEIHIN", _("Keihin")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    SIEMENS = "SIEMENS", _("Siemens")
    VDO = "VDO", _("VDO")

    AUTRE = "AUTRE", _("Autre fabricant")


class FabricantConnecteurInjecteur(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    OEM = "OEM", _("Constructeur OEM")

    AMP = "AMP", _("AMP")
    BOSCH = "BOSCH", _("Bosch")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    INCONNU = "INCONNU", _("Fabricant inconnu")
    MOLEX = "MOLEX", _("Molex")
    TE_CONNECTIVITY = "TE_CONNECTIVITY", _("TE Connectivity")

    AUTRE = "AUTRE", _("Autre fabricant")


class FabricantAmpoule(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    BOSCH = "BOSCH", _("Bosch")
    GE = "GE", _("GE")
    HELLA = "HELLA", _("Hella")
    MTECH = "MTECH", _("M-Tech")
    NARVA = "NARVA", _("Narva")
    NEOLUX = "NEOLUX", _("Neolux")
    OSRAM = "OSRAM", _("Osram")
    PHILIPS = "PHILIPS", _("Philips")
    PIAA = "PIAA", _("PIAA")
    RING = "RING", _("Ring")
    TUNGSRAM = "TUNGSRAM", _("Tungsram")
    VALEO = "VALEO", _("Valeo")

    AUTRE = "AUTRE", _("Autre")


class FabricantMoteur(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    ABARTH = "ABARTH", _("Abarth")
    AER = "AER", _("AER")
    ALFA_ROMEO = "ALFA_ROMEO", _("Alfa Romeo")
    ALPINA = "ALPINA", _("Alpina")
    ALPINE = "ALPINE", _("Alpine")
    AMG = "AMG", _("AMG")
    ASTON_MARTIN = "ASTON_MARTIN", _("Aston Martin")
    AUDI = "AUDI", _("Audi")
    BENTLEY = "BENTLEY", _("Bentley")
    BMW = "BMW", _("BMW")
    BMW_M = "BMW_M", _("BMW M")
    BUGATTI = "BUGATTI", _("Bugatti")
    CITROEN = "CITROEN", _("Citroën")
    COSWORTH = "COSWORTH", _("Cosworth")
    COTAL = "COTAL", _("Cotal")
    CUMMINS = "CUMMINS", _("Cummins")
    DACIA = "DACIA", _("Dacia")
    DEUTZ = "DEUTZ", _("Deutz")
    FERRARI = "FERRARI", _("Ferrari")
    FIAT = "FIAT", _("Fiat")
    FORD = "FORD", _("Ford")
    GM = "GM", _("General Motors")
    GORDINI = "GORDINI", _("Gordini")
    HART = "HART", _("Hart")
    HONDA = "HONDA", _("Honda")
    HPD = "HPD", _("HPD (Honda Performance Development)")
    HYUNDAI = "HYUNDAI", _("Hyundai")
    ILMOR = "ILMOR", _("Ilmor")
    JAGUAR = "JAGUAR", _("Jaguar")
    JUDD = "JUDD", _("Judd")
    KIA = "KIA", _("Kia")
    LAMBORGHINI = "LAMBORGHINI", _("Lamborghini")
    LAND_ROVER = "LAND_ROVER", _("Land Rover")
    LEXUS = "LEXUS", _("Lexus")
    LOTUS = "LOTUS", _("Lotus")
    MASERATI = "MASERATI", _("Maserati")
    MAZDA = "MAZDA", _("Mazda")
    MCLAREN = "MCLAREN", _("McLaren")
    MECACHROME = "MECACHROME", _("Mecachrome")
    MERCEDES = "MERCEDES", _("Mercedes-Benz")
    MINI = "MINI", _("Mini")
    MITSUBISHI = "MITSUBISHI", _("Mitsubishi")
    MUGEN = "MUGEN", _("Mugen")
    NISMO = "NISMO", _("Nismo")
    NISSAN = "NISSAN", _("Nissan")
    OPEL = "OPEL", _("Opel")
    ORECA = "ORECA", _("Oreca")
    PERKINS = "PERKINS", _("Perkins")
    PEUGEOT = "PEUGEOT", _("Peugeot")
    PORSCHE = "PORSCHE", _("Porsche")
    RENAULT = "RENAULT", _("Renault")
    ROLLS_ROYCE = "ROLLS_ROYCE", _("Rolls-Royce")
    ROTAX = "ROTAX", _("Rotax")
    SEAT = "SEAT", _("Seat")
    SKODA = "SKODA", _("Škoda")
    SUBARU = "SUBARU", _("Subaru")
    SUZUKI = "SUZUKI", _("Suzuki")
    TOYOTA = "TOYOTA", _("Toyota")
    TRD = "TRD", _("TRD (Toyota Racing Development)")
    VM_MOTORI = "VM_MOTORI", _("VM Motori")
    VOLKSWAGEN = "VOLKSWAGEN", _("Volkswagen")
    VOLVO = "VOLVO", _("Volvo")
    YAMAHA = "YAMAHA", _("Yamaha")

    AUTRE = "AUTRE", _("Autre")


class FabricantBoite(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    AISIN = "AISIN", _("Aisin")
    ALBINS = "ALBINS", _("Albins")
    ALFA_ROMEO = "ALFA_ROMEO", _("Alfa Romeo")
    ALLISON = "ALLISON", _("Allison")
    AUDI = "AUDI", _("Audi")
    BMW = "BMW", _("BMW")
    BORGWARNER = "BORGWARNER", _("BorgWarner")
    CITROEN = "CITROEN", _("Citroën")
    DANA = "DANA", _("Dana")
    DRENTH = "DRENTH", _("Drenth")
    EATON = "EATON", _("Eaton")
    FERRARI = "FERRARI", _("Ferrari")
    FIAT = "FIAT", _("Fiat")
    FORD = "FORD", _("Ford")
    GM = "GM", _("General Motors")
    GETRAG = "GETRAG", _("Getrag (Magna)")
    GRAZIANO = "GRAZIANO", _("Graziano")
    HEWLAND = "HEWLAND", _("Hewland")
    HOLINGER = "HOLINGER", _("Holinger")
    HONDA = "HONDA", _("Honda")
    HYUNDAI = "HYUNDAI", _("Hyundai")
    HYUNDAI_TRANSYS = "HYUNDAI_TRANSYS", _("Hyundai Transys")
    JATCO = "JATCO", _("Jatco")
    MAZDA = "MAZDA", _("Mazda")
    MERCEDES = "MERCEDES", _("Mercedes-Benz")
    MITSUBISHI = "MITSUBISHI", _("Mitsubishi")
    NISSAN = "NISSAN", _("Nissan")
    OPEL = "OPEL", _("Opel")
    PEUGEOT = "PEUGEOT", _("Peugeot")
    PORSCHE = "PORSCHE", _("Porsche")
    PUNCH = "PUNCH", _("Punch Powertrain")
    QUAIFE = "QUAIFE", _("Quaife")
    RENAULT = "RENAULT", _("Renault")
    RICARDO = "RICARDO", _("Ricardo")
    SADEV = "SADEV", _("Sadev")
    SAMSONAS = "SAMSONAS", _("Samsonas")
    SUBARU = "SUBARU", _("Subaru")
    TOYOTA = "TOYOTA", _("Toyota")
    TREMEC = "TREMEC", _("Tremec")
    VOITH = "VOITH", _("Voith")
    VOLKSWAGEN = "VOLKSWAGEN", _("Volkswagen")
    VOLVO = "VOLVO", _("Volvo")
    XTRAC = "XTRAC", _("Xtrac")
    ZF = "ZF", _("ZF")

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
    CHOISIR = "CHOISIR", _("Choisir")
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
    CHOISIR = "CHOISIR", _("Choisir")

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
    CHOISIR = "CHOISIR", _("Choisir")

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
    CHOISIR = "CHOISIR", _("Choisir")

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
    CHOISIR = "CHOISIR", _("Choisir")
    # Volkswagen Group
    G11 = "G11", _("G 11 VAG")
    G12 = "G12", _("G 12 VAG")
    G12_PLUS = "G12_PLUS", _("G 12+ VAG")
    G12_PLUS_PLUS = "G12_PLUS_PLUS", _("G 12++ VAG")
    G13 = "G13", _("G 13")

    # BMW
    G48 = "G48", _("G 48 BMW")

    # Mercedes-Benz
    MB_325_0 = "MB_325_0", _("MB 325.0 Mercedes")
    MB_325_3 = "MB_325_3", _("MB 325.3 Mercedes")
    MB_325_5 = "MB_325_5", _("MB 325.5 Mercedes")

    # Renault / Dacia
    TYPE_D = "TYPE_D", _("Type D Renault")

    # PSA (Peugeot / Citroën)
    PSA_B71_5110 = "PSA_B71_5110", _("B71 5110 PSA")

    # Ford
    WSS_M97B44_D = "WSS_M97B44_D", _("WSS-M97B44-D Ford")
    WSS_M97B51_A1 = "WSS_M97B51_A1", _("WSS-M97B51-A1 Ford")

    # General Motors
    DEX_COOL = "DEX_COOL", _("Dex-Cool GM")

    # Toyota / Lexus
    TOYOTA_SLLC = "TOYOTA_SLLC", _("Toyota SLLC")

    # Honda
    HONDA_TYPE_2 = "HONDA_TYPE_2", _("Honda Type 2")

    # Nissan
    NISSAN_L248 = "NISSAN_L248", _("Nissan L248")
    NISSAN_L250 = "NISSAN_L250", _("Nissan L250")

    # Hyundai / Kia
    HYUNDAI_KIA_LLC = "HYUNDAI_KIA_LLC", _("Hyundai/Kia Long Life Coolant")

    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur")


class LiquideFreinsQualite(models.TextChoices):
        DOT3 = 'DOT 3', _("DOT 3")
        DOT4 = 'DOT 4', _("DOT 4")
        DOT5 = 'DOT 5', _("DOT 5")
        DOT51 = 'DOT 5.1', _("DOT 5.1")



class LaveGlaceQualite(models.TextChoices):
    HIVER = 'HIVER', _("Hiver")
    ETE = 'ETE', _("Eté")






class HuileBoiteEtat(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    # =========================================================
    # HUILES BOÎTES MANUELLES
    # =========================================================
    SEPTANTE_CINQ = "75W", _("75W")
    SEPTANTE_5_80 = "75W80", _("75W80")
    SEPTANTE_CINQ90 = "75W90", _("75W90")
    QUATRE_20 = "80W", _("80W")
    QUATRE_20_90 = "80W90", _("80W90")
    QUATRE_25_90 = "85W90", _("85W90")

    # =========================================================
    # ATF GÉNÉRIQUES
    # =========================================================
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

    # =========================================================
    # PORSCHE
    # =========================================================
    PORSCHE_PDK = "PORSCHE_PDK", _("Porsche PDK")
    PORSCHE_DCT = "PORSCHE_DCT", _("Porsche DCT")
    PORSCHE_TIPTRONIC = "PORSCHE_TIPTRONIC", _("Porsche Tiptronic")

    # =========================================================
    # VAG - VOLKSWAGEN / AUDI / SEAT / SKODA
    # =========================================================
    VAG_DSG_DQ250 = "VAG_DSG_DQ250", _("VAG DSG DQ250")
    VAG_DSG_DQ381 = "VAG_DSG_DQ381", _("VAG DSG DQ381")
    VAG_DSG_DQ500 = "VAG_DSG_DQ500", _("VAG DSG DQ500")
    VAG_DSG_DQ200 = "VAG_DSG_DQ200", _("VAG DSG DQ200")
    VAG_S_TRONIC = "VAG_S_TRONIC", _("Audi S tronic")
    VAG_MULTITRONIC = "VAG_MULTITRONIC", _("Audi Multitronic")
    VAG_TIPTRONIC = "VAG_TIPTRONIC", _("VAG Tiptronic")

    # =========================================================
    # FORD
    # =========================================================
    FORD_MERCON = "FORD_MERCON", _("Ford Mercon")
    FORD_MERCON_V = "FORD_MERCON_V", _("Ford Mercon V")
    FORD_MERCON_LV = "FORD_MERCON_LV", _("Ford Mercon LV")
    FORD_MERCON_ULV = "FORD_MERCON_ULV", _("Ford Mercon ULV")
    FORD_POWERSHIFT = "FORD_POWERSHIFT", _("Ford PowerShift")
    FORD_CVT = "FORD_CVT", _("Ford CVT")

    # =========================================================
    # ALFA ROMEO
    # =========================================================
    ALFA_TCT = "ALFA_TCT", _("Alfa Romeo TCT")
    ALFA_SELESPEED = "ALFA_SELESPEED", _("Alfa Romeo Selespeed")
    ALFA_ATF = "ALFA_ATF", _("Alfa Romeo ATF")
    ALFA_TUTELA = "ALFA_TUTELA", _("Alfa Romeo Tutela")

    # =========================================================
    # FERRARI
    # =========================================================
    FERRARI_DCT = "FERRARI_DCT", _("Ferrari DCT")
    FERRARI_F1 = "FERRARI_F1", _("Ferrari F1")
    FERRARI_GETRAG = "FERRARI_GETRAG", _("Ferrari Getrag")
    FERRARI_ATF = "FERRARI_ATF", _("Ferrari ATF")

    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur")
    AUTRE = "AUTRE", _("Autre")





class HuileBoiteAutoEtat(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")

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

    # =========================================================
    # PORSCHE
    # =========================================================
    PORSCHE_PDK = "PORSCHE_PDK", _("Porsche PDK")
    PORSCHE_DCT = "PORSCHE_DCT", _("Porsche DCT")
    PORSCHE_TIPTRONIC = "PORSCHE_TIPTRONIC", _("Porsche Tiptronic")

    # =========================================================
    # VAG - VOLKSWAGEN / AUDI / SEAT / SKODA
    # =========================================================
    VAG_DSG_DQ250 = "VAG_DSG_DQ250", _("VAG DSG DQ250")
    VAG_DSG_DQ381 = "VAG_DSG_DQ381", _("VAG DSG DQ381")
    VAG_DSG_DQ500 = "VAG_DSG_DQ500", _("VAG DSG DQ500")
    VAG_DSG_DQ200 = "VAG_DSG_DQ200", _("VAG DSG DQ200")
    VAG_S_TRONIC = "VAG_S_TRONIC", _("Audi S tronic")
    VAG_MULTITRONIC = "VAG_MULTITRONIC", _("Audi Multitronic")
    VAG_TIPTRONIC = "VAG_TIPTRONIC", _("VAG Tiptronic")

    # =========================================================
    # FORD
    # =========================================================
    FORD_MERCON = "FORD_MERCON", _("Ford Mercon")
    FORD_MERCON_V = "FORD_MERCON_V", _("Ford Mercon V")
    FORD_MERCON_LV = "FORD_MERCON_LV", _("Ford Mercon LV")
    FORD_MERCON_ULV = "FORD_MERCON_ULV", _("Ford Mercon ULV")
    FORD_POWERSHIFT = "FORD_POWERSHIFT", _("Ford PowerShift")
    FORD_CVT = "FORD_CVT", _("Ford CVT")

    # =========================================================
    # ALFA ROMEO
    # =========================================================
    ALFA_TCT = "ALFA_TCT", _("Alfa Romeo TCT")
    ALFA_SELESPEED = "ALFA_SELESPEED", _("Alfa Romeo Selespeed")
    ALFA_ATF = "ALFA_ATF", _("Alfa Romeo ATF")
    ALFA_TUTELA = "ALFA_TUTELA", _("Alfa Romeo Tutela")

    # =========================================================
    # FERRARI
    # =========================================================
    FERRARI_DCT = "FERRARI_DCT", _("Ferrari DCT")
    FERRARI_F1 = "FERRARI_F1", _("Ferrari F1")
    FERRARI_GETRAG = "FERRARI_GETRAG", _("Ferrari Getrag")
    FERRARI_ATF = "FERRARI_ATF", _("Ferrari ATF")

    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur")
    AUTRE = "AUTRE", _("Autre")


class FabricantAllumage(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    OEM = "OEM", _("Constructeur OEM")

    BERU = "BERU", _("Beru")
    BOSCH = "BOSCH", _("Bosch")
    BREMBO = "BREMBO", _("Brembo")
    BREMI = "BREMI", _("Bremi")
    CHAMPION = "CHAMPION", _("Champion")
    CONTINENTAL = "CONTINENTAL", _("Continental")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    ERA = "ERA", _("ERA")
    INCONNU = "INCONNU", _("Fabricant inconnu")
    FACET = "FACET", _("Facet")
    FEBI = "FEBI", _("Febi Bilstein")
    HELLA = "HELLA", _("Hella")
    HITACHI = "HITACHI", _("Hitachi")
    MAGNETI_MARELLI = "MAGNETI_MARELLI", _("Magneti Marelli")
    MEYLE = "MEYLE", _("Meyle")
    NGK = "NGK", _("NGK")
    VALEO = "VALEO", _("Valeo")
    VDO = "VDO", _("VDO")

    AUTRE = "AUTRE", _("Autre fabricant")


class EtatOKNotOKNiveau(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Faire")
    REMPLACE = "REMPLACE", _("Fait")





# maintenance/choices.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class MarqueAmortisseur(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    ORIGINE = "Origine", _("Constructeur OEM")

    BILSTEIN = "Bilstein", "Bilstein"
    BOGE = "Boge", "Boge"
    EIBACH = "Eibach", "Eibach"
    FOX = "Fox", "Fox"
    GABRIEL = "Gabriel", "Gabriel"
    HR = "H&R", "H&R"
    KONI = "Koni", "Koni"
    KW = "KW", "KW"
    KYB = "KYB", "KYB (Kayaba)"
    MAGNETI_MARELLI = "Magneti Marelli", "Magneti Marelli"
    MEYLE = "Meyle", "Meyle"
    MONROE = "Monroe", "Monroe"
    OHLINS = "Öhlins", "Öhlins"
    RANCHO = "Rancho", "Rancho"
    SACHS = "Sachs", "Sachs (ZF)"
    SHOWA = "Showa", "Showa"
    TEIN = "Tein", "Tein"
    TOKICO = "Tokico", "Tokico"

    AUTRE = "Autre", _("Autre")


class FabricantClim(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    ORIGINE = "ORIGINE", _("Constructeur OEM")

    ARKEMA = "ARKEMA", _("Arkema (Forane)")
    AVA = "AVA", _("AVA Quality Cooling")
    BLUECHEM = "BLUECHEM", _("Bluechem")
    BOSCH = "BOSCH", _("Bosch")
    CHEMOURS = "CHEMOURS", _("Chemours (Opteon)")
    CORTECO = "CORTECO", _("Corteco")
    DAIKIN = "DAIKIN", _("Daikin")
    DELPHI = "DELPHI", _("Delphi")
    DENSO = "DENSO", _("Denso")
    ECOTECHNICS = "ECOTECHNICS", _("Ecotechnics")
    ERRECOM = "ERRECOM", _("Errecom")
    FUCHS = "FUCHS", _("Fuchs")
    HANON = "HANON", _("Hanon Systems (ex-Halla Visteon)")
    HELLA = "HELLA", _("Hella / Behr Hella Service")
    HENGST = "HENGST", _("Hengst")
    HIGHLY = "HIGHLY", _("Highly")
    HONEYWELL = "HONEYWELL", _("Honeywell (Solstice)")
    IDEMITSU = "IDEMITSU", _("Idemitsu")
    KALE = "KALE", _("Kale")
    KOURA = "KOURA", _("Koura (Klea)")
    LIQUI_MOLY = "LIQUI_MOLY", _("Liqui Moly")
    MAHLE = "MAHLE", _("Mahle (ex-Behr)")
    MANN_FILTER = "MANN_FILTER", _("Mann-Filter")
    MARELLI = "MARELLI", _("Marelli (Magneti Marelli / Calsonic Kansei)")
    MEAT_DORIA = "MEAT_DORIA", _("Meat & Doria")
    NISSENS = "NISSENS", _("Nissens")
    NRF = "NRF", _("NRF")
    PURFLUX = "PURFLUX", _("Purflux")
    ROBINAIR = "ROBINAIR", _("Robinair")
    SANDEN = "SANDEN", _("Sanden")
    SELTEC = "SELTEC", _("Seltec")
    SPECTRONICS = "SPECTRONICS", _("Spectronics (Tracerline)")
    SPIN = "SPIN", _("Spin")
    TEXA = "TEXA", _("Texa")
    THERMOTEC = "THERMOTEC", _("Thermotec")
    TYC = "TYC", _("TYC")
    UFI = "UFI", _("UFI")
    UVIEW = "UVIEW", _("UView")
    VALEO = "VALEO", _("Valeo")
    VAN_WEZEL = "VAN_WEZEL", _("Van Wezel")
    WAECO = "WAECO", _("Waeco / Dometic")
    WIGAM = "WIGAM", _("Wigam")
    WURTH = "WURTH", _("Würth")
    WYNNS = "WYNNS", _("Wynn's")
    ZEXEL = "ZEXEL", _("Zexel")

    AUTRE = "AUTRE", _("Autre")


class FabricantCardan(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR_OEM = "CONSTRUCTEUR_OEM", _("Constructeur OEM")

    BLUE_PRINT = "BLUE_PRINT", _("Blue Print")
    BOSCH = "BOSCH", _("Bosch")
    CORTECO = "CORTECO", _("Corteco")
    DANA = "DANA", _("Dana / Spicer")
    DELPHI = "DELPHI", _("Delphi")
    FAG = "FAG", _("FAG / Schaeffler")
    FEBI = "FEBI", _("Febi Bilstein")
    GKN = "GKN", _("GKN / Löbro / Spidan")
    HYUNDAI_WIA = "HYUNDAI_WIA", _("Hyundai WIA")
    IFA = "IFA", _("IFA Rotorion")
    JAPANPARTS = "JAPANPARTS", _("Japanparts")
    MAPCO = "MAPCO", _("MAPCO")
    METELLI = "METELLI", _("Metelli")
    MEYLE = "MEYLE", _("Meyle")
    NEAPCO = "NEAPCO", _("Neapco")
    NTN_SNR = "NTN_SNR", _("NTN-SNR")
    QA1 = "QA1", _("QA1")
    RCV = "RCV", _("RCV Performance")
    RIDEX = "RIDEX", _("RIDEX")
    SKF = "SKF", _("SKF")
    SWAG = "SWAG", _("SWAG")
    DRIVESHAFT_SHOP = "DRIVESHAFT_SHOP", _("The Driveshaft Shop")
    TOPRAN = "TOPRAN", _("Topran")
    TRW = "TRW", _("TRW")
    VAICO = "VAICO", _("Vaico")
    ZF = "ZF", _("ZF / Lemförder")

    AUTRE = "AUTRE", _("Autre")


class FabricantEsthetique(models.TextChoices):
    """Marques de produits d'esthétique automobile (polish, cire, céramique, décontamination)."""
    CHOISIR = "CHOISIR", _("Choisir")
    CONSTRUCTEUR = "CONSTRUCTEUR", _("Constructeur OEM")

    THREE_M = "3M", "3M"
    ADAMS = "ADAMS", "Adam's Polishes"
    AUTOGLYM = "AUTOGLYM", "Autoglym"
    BILT_HAMBER = "BILT_HAMBER", "Bilt Hamber"
    CARPRO = "CARPRO", "CarPro"
    CHEMICAL_GUYS = "CHEMICAL_GUYS", "Chemical Guys"
    COLLINITE = "COLLINITE", "Collinite"
    DODO_JUICE = "DODO_JUICE", "Dodo Juice"
    FLEXIPADS = "FLEXIPADS", "Flexipads"
    GTECHNIQ = "GTECHNIQ", "Gtechniq"
    GYEON = "GYEON", "Gyeon"
    IGL = "IGL", "IGL Coatings"
    KOCH_CHEMIE = "KOCH_CHEMIE", "Koch-Chemie"
    LABOCOSMETICA = "LABOCOSMETICA", "Labocosmetica"
    LAKE_COUNTRY = "LAKE_COUNTRY", "Lake Country"
    MEGUIARS = "MEGUIARS", "Meguiar's"
    MENZERNA = "MENZERNA", "Menzerna"
    MOTHERS = "MOTHERS", "Mothers"
    NANOLEX = "NANOLEX", "Nanolex"
    ONYX = "ONYX", "Onyx Coating"
    RUPES = "RUPES", "Rupes"
    SCHOLL = "SCHOLL", "Scholl Concepts"
    SOFT99 = "SOFT99", "Soft99"
    SONAX = "SONAX", "Sonax"
    SWISSVAX = "SWISSVAX", "Swissvax"
    TURTLE_WAX = "TURTLE_WAX", "Turtle Wax"
    ZAINO = "ZAINO", "Zaino"

    AUTRE = "AUTRE", _("Autre")


