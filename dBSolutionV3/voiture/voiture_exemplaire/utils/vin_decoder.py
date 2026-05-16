from datetime import datetime


class VinDecoderService:
    """
    Décodage VIN compatible ISO + corrections constructeur.
    """

    # Séquence ISO (année VIN)
    VIN_SEQUENCE = "ABCDEFGHJKLMNPRSTVWXY123456789"

    # WMI -> constructeur
    WMI_MAP = {
        "WMW": "MINI",
        "WBA": "BMW",
        "WBS": "BMW M",
        "VF1": "Renault",
        "VF3": "Peugeot",
        "VF7": "Citroën",
        "WVW": "Volkswagen",
        "WAU": "Audi",
    }

    # corrections constructeur (cas réels terrain)
    BUILDER_YEAR_FIXES = {
        "MINI": {
            "0": 2006,  # ton cas réel R56
        }
    }

    def __init__(self, vin: str):
        self.vin = vin.upper() if vin else None

    # ------------------------
    # constructeur
    # ------------------------
    def get_wmi(self):
        if not self.vin or len(self.vin) < 3:
            return None
        return self.vin[:3]

    def get_brand(self):
        wmi = self.get_wmi()
        return self.WMI_MAP.get(wmi, "UNKNOWN")

    # ------------------------
    # année modèle
    # ------------------------
    def get_model_year(self):
        if not self.vin or len(self.vin) < 10:
            return None

        code = self.vin[9]  # 10e caractère

        brand = self.get_brand()

        # correction constructeur si existe
        if brand in self.BUILDER_YEAR_FIXES:
            fix = self.BUILDER_YEAR_FIXES[brand].get(code)
            if fix:
                return fix

        # logique ISO standard
        if code not in self.VIN_SEQUENCE:
            return None

        index = self.VIN_SEQUENCE.index(code)
        base_year = 1980 + index

        current_year = datetime.now().year

        # cycle 30 ans
        while base_year + 30 <= current_year + 1:
            base_year += 30

        return base_year

    # ------------------------
    # résumé complet
    # ------------------------
    def decode(self):
        return {
            "vin": self.vin,
            "brand": self.get_brand(),
            "wmi": self.get_wmi(),
            "model_year": self.get_model_year(),
        }