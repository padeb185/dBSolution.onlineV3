# your_app/utils_vin.py
from datetime import datetime

VIN_YEAR_BASE = {
    "A": 1980, "B": 1981, "C": 1982, "D": 1983, "E": 1984, "F": 1985, "G": 1986, "H": 1987,
    "J": 1988, "K": 1989, "L": 1990, "M": 1991, "N": 1992, "P": 1993, "R": 1994, "S": 1995,
    "T": 1996, "V": 1997, "W": 1998, "X": 1999, "Y": 2000,
    "1": 2001, "2": 2002, "3": 2003, "4": 2004, "5": 2005,
    "6": 2006, "7": 2007, "8": 2008, "9": 2009,
}


VIN_SEQUENCE = "ABCDEFGHJKLMNPRSTVWXY123456789"

# corrections constructeur (BMW / MINI)
BMW_VIN_FIXES = {
    "0": 2006,  # ton cas réel MINI R56
}

def get_vin_year(code: str, brand: str | None = None) -> int | None:
    if not code:
        return None

    code = code.upper()

    # ------------------------
    # 1. FIX constructeur (BMW/MINI)
    # ------------------------
    if brand == "BMW" or brand == "MINI":
        if code in BMW_VIN_FIXES:
            return BMW_VIN_FIXES[code]

    # ------------------------
    # 2. ISO STANDARD EU
    # ------------------------
    if code not in VIN_SEQUENCE:
        return None

    index = VIN_SEQUENCE.index(code)

    base_year = 1980 + index
    current_year = datetime.now().year

    # cycle 30 ans
    while base_year + 30 <= current_year + 1:
        base_year += 30

    return base_year