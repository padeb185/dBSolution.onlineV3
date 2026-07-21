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