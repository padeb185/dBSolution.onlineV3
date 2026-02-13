# your_app/utils_vin.py

VIN_YEAR_BASE = {
    "A": 1980, "B": 1981, "C": 1982, "D": 1983, "E": 1984, "F": 1985, "G": 1986, "H": 1987,
    "J": 1988, "K": 1989, "L": 1990, "M": 1991, "N": 1992, "P": 1993, "R": 1994, "S": 1995,
    "T": 1996, "V": 1997, "W": 1998, "X": 1999, "Y": 2000,
    "1": 2001, "2": 2002, "3": 2003, "4": 2004, "5": 2005, "6": 2006, "7": 2007, "8": 2008, "9": 2009,
}

def get_vin_year(code: str, after_2010: bool = True) -> int | None:
    code = code.upper()
    base_year = VIN_YEAR_BASE.get(code)
    if base_year is None:
        return None

    if after_2010:
        if base_year < 2010:
            return base_year + 30
        return base_year
    else:
        if base_year >= 2010:
            return base_year - 30
        return base_year
