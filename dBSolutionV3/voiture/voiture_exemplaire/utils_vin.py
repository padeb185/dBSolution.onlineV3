from datetime import datetime
from typing import Optional


class VinDecoderService:
    """
    Service de décodage VIN.

    - Normalise automatiquement le VIN.
    - Normalise automatiquement la marque.
    - Détecte la marque via le WMI si elle n'est pas fournie.
    - Gère les cycles VIN de 30 ans.
    - Utilise des décodeurs spécifiques constructeur.
    - Utilise l'année d'immatriculation comme fallback.
    """

    # ========================================================
    # CYCLES ANNÉE VIN
    # ========================================================

    VIN_YEAR_CYCLES = {
        "A": [1980, 2010, 2040],
        "B": [1981, 2011, 2041],
        "C": [1982, 2012, 2042],
        "D": [1983, 2013, 2043],
        "E": [1984, 2014, 2044],
        "F": [1985, 2015, 2045],
        "G": [1986, 2016, 2046],
        "H": [1987, 2017, 2047],

        "J": [1988, 2018, 2048],
        "K": [1989, 2019, 2049],
        "L": [1990, 2020, 2050],
        "M": [1991, 2021, 2051],
        "N": [1992, 2022, 2052],

        "P": [1993, 2023, 2053],
        "R": [1994, 2024, 2054],
        "S": [1995, 2025, 2055],
        "T": [1996, 2026, 2056],

        "V": [1997, 2027, 2057],
        "W": [1998, 2028, 2058],
        "X": [1999, 2029, 2059],
        "Y": [2000, 2030, 2060],

        "1": [2001, 2031, 2061],
        "2": [2002, 2032, 2062],
        "3": [2003, 2033, 2063],
        "4": [2004, 2034, 2064],
        "5": [2005, 2035, 2065],
        "6": [2006, 2036, 2066],
        "7": [2007, 2037, 2067],
        "8": [2008, 2038, 2068],
        "9": [2009, 2039, 2069],
    }

    # ========================================================
    # CONSTRUCTEURS AVEC DÉCODEUR SPÉCIFIQUE
    # ========================================================

    NON_STANDARD_YEAR_DECODERS = {
        "BMW": "bmw_mini",
        "MINI": "bmw_mini",

        "MERCEDES-BENZ": "mercedes",

        "PORSCHE": "porsche",

        "VOLKSWAGEN": "vag",
        "AUDI": "vag",
        "SEAT": "vag",
        "SKODA": "vag",
        "CUPRA": "vag",
    }

    # ========================================================
    # WMI -> MARQUE
    # ========================================================

    WMI_MAP = {
        # BMW / MINI
        "WBA": "BMW",
        "WBS": "BMW",
        "WBY": "BMW",
        "WMW": "MINI",

        # Porsche
        "WP0": "PORSCHE",
        "WP1": "PORSCHE",

        # Mercedes-Benz
        "WDB": "MERCEDES-BENZ",
        "WDD": "MERCEDES-BENZ",
        "WDC": "MERCEDES-BENZ",
        "WDF": "MERCEDES-BENZ",
        "W1K": "MERCEDES-BENZ",
        "W1N": "MERCEDES-BENZ",
        "W1V": "MERCEDES-BENZ",

        # Volkswagen
        "WVW": "VOLKSWAGEN",
        "WVG": "VOLKSWAGEN",
        "WV1": "VOLKSWAGEN",
        "WV2": "VOLKSWAGEN",

        # Audi
        "WAU": "AUDI",
        "TRU": "AUDI",

        # Seat / Cupra
        "VSS": "SEAT",

        # Skoda
        "TMB": "SKODA",

        # Renault
        "VF1": "RENAULT",

        # Peugeot
        "VF3": "PEUGEOT",

        # Citroën
        "VF7": "CITROEN",

        # Ferrari
        "ZFF": "FERRARI",

        # Lamborghini
        "ZHW": "LAMBORGHINI",

        # Fiat
        "ZFA": "FIAT",

        # Alfa Romeo
        "ZAR": "ALFA ROMEO",

        # Volvo
        "YV1": "VOLVO",

        # Toyota
        "JTD": "TOYOTA",
        "JT1": "TOYOTA",
        "JT2": "TOYOTA",

        # Lexus
        "JTH": "LEXUS",

        # Nissan
        "JN1": "NISSAN",

        # Honda
        "JHM": "HONDA",

        # Mazda
        "JM1": "MAZDA",

        # Subaru
        "JF1": "SUBARU",

        # Ford
        "WF0": "FORD",

        # Opel
        "W0L": "OPEL",
    }

    # ========================================================
    # INITIALISATION
    # ========================================================

    def __init__(
        self,
        vin: str,
        brand: Optional[str] = None,
        registration_year: Optional[int] = None,
    ):
        self.vin = self._normalize_vin(vin)
        self.brand = self._normalize_brand(brand)
        self.registration_year = self._normalize_year(
            registration_year
        )

    # ========================================================
    # NORMALISATION VIN
    # ========================================================

    @staticmethod
    def _normalize_vin(
        vin: Optional[str],
    ) -> Optional[str]:

        if not vin:
            return None

        return str(vin).strip().upper()

    # ========================================================
    # NORMALISATION ANNÉE
    # ========================================================

    @staticmethod
    def _normalize_year(
        year,
    ) -> Optional[int]:

        if year is None:
            return None

        try:
            year = int(year)
        except (TypeError, ValueError):
            return None

        if 1800 <= year <= 2100:
            return year

        return None

    # ========================================================
    # NORMALISATION MARQUE
    # ========================================================

    @staticmethod
    def _normalize_brand(
        brand: Optional[str],
    ) -> Optional[str]:

        if not brand:
            return None

        brand = str(brand).strip().upper()

        aliases = {
            "MINI": "MINI",

            "BMW": "BMW",
            "BMW M": "BMW",

            "PORSCHE": "PORSCHE",

            "MERCEDES": "MERCEDES-BENZ",
            "MERCEDES BENZ": "MERCEDES-BENZ",
            "MERCEDES-BENZ": "MERCEDES-BENZ",

            "VW": "VOLKSWAGEN",
            "VOLKSWAGEN": "VOLKSWAGEN",

            "AUDI": "AUDI",

            "SEAT": "SEAT",

            "CUPRA": "CUPRA",

            "SKODA": "SKODA",
            "ŠKODA": "SKODA",

            "RENAULT": "RENAULT",

            "PEUGEOT": "PEUGEOT",

            "CITROEN": "CITROEN",
            "CITROËN": "CITROEN",

            "FERRARI": "FERRARI",

            "LAMBORGHINI": "LAMBORGHINI",

            "FIAT": "FIAT",

            "ALFA ROMEO": "ALFA ROMEO",
            "ALFA-ROMEO": "ALFA ROMEO",

            "VOLVO": "VOLVO",

            "TOYOTA": "TOYOTA",

            "LEXUS": "LEXUS",

            "NISSAN": "NISSAN",

            "HONDA": "HONDA",

            "MAZDA": "MAZDA",

            "SUBARU": "SUBARU",

            "FORD": "FORD",

            "OPEL": "OPEL",
        }

        return aliases.get(
            brand,
            brand,
        )

    # ========================================================
    # WMI
    # ========================================================

    def get_wmi(self) -> Optional[str]:

        if not self.vin or len(self.vin) < 3:
            return None

        return self.vin[:3]

    # ========================================================
    # MARQUE
    # ========================================================

    def get_brand(self) -> str:
        """
        Priorité :
        1. marque provenant de Django
        2. marque détectée via WMI
        """

        if self.brand:
            return self.brand

        wmi = self.get_wmi()

        if not wmi:
            return "UNKNOWN"

        return self.WMI_MAP.get(
            wmi,
            "UNKNOWN",
        )

    # ========================================================
    # CODE ANNÉE
    # ========================================================

    def get_year_code(self) -> Optional[str]:

        if not self.vin or len(self.vin) < 10:
            return None

        return self.vin[9]

    # ========================================================
    # ANNÉES ISO POSSIBLES
    # ========================================================

    def get_possible_iso_years(self) -> list[int]:

        code = self.get_year_code()

        if not code:
            return []

        years = self.VIN_YEAR_CYCLES.get(
            code,
            [],
        )

        current_year = datetime.now().year

        return [
            year
            for year in years
            if year <= current_year + 1
        ]

    # ========================================================
    # ANNÉE ISO
    # ========================================================

    def get_iso_year(self) -> Optional[int]:

        possible_years = self.get_possible_iso_years()

        if not possible_years:
            return None

        # ----------------------------------------------------
        # Année première immatriculation connue
        # ----------------------------------------------------

        if self.registration_year is not None:

            candidates = [
                year
                for year in possible_years
                if year <= self.registration_year + 1
            ]

            if candidates:
                return min(
                    candidates,
                    key=lambda year: abs(
                        year - self.registration_year
                    ),
                )

        # ----------------------------------------------------
        # Sinon cycle le plus récent plausible
        # ----------------------------------------------------

        return max(possible_years)

    # ========================================================
    # BMW / MINI
    # ========================================================

    def decode_bmw_mini_production_year(
        self,
    ) -> Optional[int]:

        brand = self.get_brand()

        if brand not in {
            "BMW",
            "MINI",
        }:
            return None

        year_code = self.get_year_code()

        # ----------------------------------------------------
        # Code ISO exploitable
        # ----------------------------------------------------

        if year_code in self.VIN_YEAR_CYCLES:

            iso_year = self.get_iso_year()

            if iso_year is not None:
                return iso_year

        # ----------------------------------------------------
        # Code non ISO
        #
        # Exemple :
        # MINI WMWRA31030TE24878
        #
        # position 10 = "0"
        #
        # "0" n'est pas converti arbitrairement en 2006.
        # ----------------------------------------------------

        if self.registration_year is not None:
            return self.registration_year

        return None

    # ========================================================
    # PORSCHE
    # ========================================================

    def decode_porsche_production_year(
        self,
    ) -> Optional[int]:

        if self.get_brand() != "PORSCHE":
            return None

        iso_year = self.get_iso_year()

        if iso_year is not None:
            return iso_year

        if self.registration_year is not None:
            return self.registration_year

        return None

    # ========================================================
    # MERCEDES-BENZ
    # ========================================================

    def decode_mercedes_production_year(
        self,
    ) -> Optional[int]:

        if self.get_brand() != "MERCEDES-BENZ":
            return None

        iso_year = self.get_iso_year()

        if iso_year is not None:
            return iso_year

        if self.registration_year is not None:
            return self.registration_year

        return None

    # ========================================================
    # VAG
    # ========================================================

    def decode_vag_production_year(
        self,
    ) -> Optional[int]:

        if self.get_brand() not in {
            "VOLKSWAGEN",
            "AUDI",
            "SEAT",
            "SKODA",
            "CUPRA",
        }:
            return None

        iso_year = self.get_iso_year()

        if iso_year is not None:
            return iso_year

        if self.registration_year is not None:
            return self.registration_year

        return None

    # ========================================================
    # ANNÉE DE PRODUCTION
    # ========================================================

    def get_production_year(
        self,
    ) -> Optional[int]:

        brand = self.get_brand()

        # ----------------------------------------------------
        # Décodeurs constructeur
        # ----------------------------------------------------

        decoder_type = self.NON_STANDARD_YEAR_DECODERS.get(
            brand
        )

        if decoder_type == "bmw_mini":
            return self.decode_bmw_mini_production_year()

        if decoder_type == "porsche":
            return self.decode_porsche_production_year()

        if decoder_type == "mercedes":
            return self.decode_mercedes_production_year()

        if decoder_type == "vag":
            return self.decode_vag_production_year()

        # ----------------------------------------------------
        # Autres constructeurs :
        # tentative ISO
        # ----------------------------------------------------

        iso_year = self.get_iso_year()

        if iso_year is not None:
            return iso_year

        # ----------------------------------------------------
        # Dernier fallback
        # ----------------------------------------------------

        if self.registration_year is not None:
            return self.registration_year

        return None

    # ========================================================
    # TYPE DE SOURCE UTILISÉE
    # ========================================================

    def get_year_source(self) -> str:

        production_year = self.get_production_year()

        if production_year is None:
            return "UNKNOWN"

        year_code = self.get_year_code()

        if (
            year_code in self.VIN_YEAR_CYCLES
            and production_year in self.get_possible_iso_years()
        ):
            return "VIN_ISO"

        if self.registration_year == production_year:
            return "REGISTRATION_YEAR"

        return "MANUFACTURER"

    # ========================================================
    # DÉCODAGE COMPLET
    # ========================================================

    def decode(self) -> dict:

        return {
            "vin": self.vin,
            "wmi": self.get_wmi(),
            "brand": self.get_brand(),

            "year_code": self.get_year_code(),

            "possible_model_years":
                self.get_possible_iso_years(),

            "model_year":
                self.get_iso_year(),

            "production_year":
                self.get_production_year(),

            "registration_year":
                self.registration_year,

            "year_source":
                self.get_year_source(),
        }