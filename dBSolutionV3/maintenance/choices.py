from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _


class RouesSerrageEtat(models.TextChoices):
    A_FAIRE = "A_FAIRE", _("À faire")
    FAIT = "FAIT", _("Fait")


TAUX_HORAIRE_CHOICES = [
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


from django.db import models
from django.utils.translation import gettext_lazy as _


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



from django.db import models
from django.utils.translation import gettext_lazy as _


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



from django.db import models
from django.utils.translation import gettext_lazy as _


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