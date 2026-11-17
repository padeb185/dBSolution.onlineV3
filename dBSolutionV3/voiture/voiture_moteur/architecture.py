"""
Architecture des moteurs (en ligne, en V, en VR, en W, à plat, rotatif, sans objet pour l'électrique).

architecture_par_defaut() déduit l'architecture du motoriste, du code moteur, du nombre de cylindres et du
type de moteur. Elle sert :
- au référentiel data/moteurs.py (clé « architecture », générée puis vérifiée à la main) ;
- à la migration qui complète les moteurs existants ;
- à MoteurVoiture.save() quand l'architecture n'est pas renseignée.
Les valeurs sont celles de models.ArchitectureMoteur (chaînes, pour éviter un import circulaire).
"""
import re

EN_LIGNE, V, VR, W, PLAT, ROTATIF, SANS = "EN_LIGNE", "V", "VR", "W", "PLAT", "ROTATIF", "SANS"

# Exceptions du référentiel (motoriste, code moteur) → architecture
EXCEPTIONS = {
    # 6 cylindres en ligne
    ("aston martin", "DB4_3.7L"): EN_LIGNE,
    ("aston martin", "DB5_4.0L"): EN_LIGNE,
    ("bentley", "R_TYPE_4.6L"): EN_LIGNE,
    ("gmc", "LM2 / 3.0 DURAMAX"): EN_LIGNE,
    ("hispano-suiza", "HS 35/40"): EN_LIGNE,
    ("hispano-suiza", "HS H6"): EN_LIGNE,
    ("jaguar", "XK4.2"): EN_LIGNE,
    ("jeep", "4.0L POWERTECH"): EN_LIGNE,
    ("jeep", "AMC 4.2"): EN_LIGNE,
    ("land rover", "DISCOVERY-P400"): EN_LIGNE,
    ("range rover", "RANGEROVER-P400"): EN_LIGNE,
    ("lexus", "2JZ-GE"): EN_LIGNE,
    ("toyota", "2JZ-GE"): EN_LIGNE,
    ("toyota", "B58"): EN_LIGNE,
    ("mercedes-amg", "C36-AMG-3.6"): EN_LIGNE,
    ("mercedes-benz", "M104"): EN_LIGNE,
    ("mercedes-benz", "M127"): EN_LIGNE,
    ("mercedes-benz", "M180"): EN_LIGNE,
    ("mercedes-benz", "M256"): EN_LIGNE,
    ("mercedes-benz", "M256E"): EN_LIGNE,
    ("morgan", "BMW-3.0-TURBO"): EN_LIGNE,
    ("nissan", "Z20"): EN_LIGNE,
    ("ram", "CUMMINS-5.9-DIESEL"): EN_LIGNE,
    ("ram", "CUMMINS-6.7-DIESEL"): EN_LIGNE,
    ("volvo", "B30"): EN_LIGNE,
    ("tvr", "TVR-SAGARIS-4.0"): EN_LIGNE,     # TVR Speed Six
    ("tvr", "TVR-TUSCAN-4.0"): EN_LIGNE,
    # 8 cylindres en ligne (Bugatti d'avant-guerre)
    ("bugatti", "T101_3.0"): EN_LIGNE,
    ("bugatti", "T35_2.3"): EN_LIGNE,
    ("bugatti", "T41_12.7"): EN_LIGNE,
    ("bugatti", "T57_3.3"): EN_LIGNE,
    # V4 étroit à une culasse (Lancia)
    ("lancia", "LANCIA-APPIA-1.1"): VR,
}

# Constructeurs dont les 6 cylindres sont tous en ligne
SIX_EN_LIGNE = {"bmw", "bmw m", "alpina"}
# Constructeurs de moteurs à plat
TOUS_A_PLAT = {"subaru", "subaru-sti"}
# VR5 / VR6 du groupe Volkswagen (à ne pas confondre avec les VR38 / VR30 Nissan, qui sont des V6)
GROUPE_VW = {"volkswagen", "audi", "seat", "skoda", "porsche"}


def architecture_par_defaut(motoriste, code_moteur, nombre_cylindres, type_moteur=""):
    m = (motoriste or "").strip().casefold()
    c = (code_moteur or "").strip().upper()
    n = int(nombre_cylindres or 0)

    if (m, c) in EXCEPTIONS:
        return EXCEPTIONS[(m, c)]
    if type_moteur == "ELEC":
        return SANS
    if type_moteur == "WANKEL" or "ROTARY" in c:
        return ROTATIF
    if n <= 0:
        return ""
    if re.search(r"(^|[^A-Z])W(8|12|16)(?!\d)", c):
        return W
    if m in GROUPE_VW and re.search(r"(^|[^A-Z])VR\d", c):
        return VR
    if m in TOUS_A_PLAT or re.search(r"BOXER|FLAT|AIR.COOLED|TYPE-[134]-|ENERTRON", c):
        return PLAT
    if m == "porsche":
        # Flat 4 / flat 6 sauf V6 / V8 (Cayenne, Panamera, Macan, 918) et 4 en ligne (924 / 944 / 968)
        if re.search(r"924|944|968|M44", c):
            return EN_LIGNE
        if re.search(r"V6|V8|TDI|PANAMERA|CAYENNE|MACAN|918|-EH", c) or n >= 8:
            return V
        return PLAT
    # « V6 », « V8 »… dans le code, si le chiffre correspond au nombre de cylindres (évite le DV6 Peugeot, un 4 en ligne)
    if n == 2 and re.search(r"V-?TWIN", c):
        return V
    if any(int(x) == n for x in re.findall(r"V(2|4|6|8|10|12)(?!\d)", c)):
        return V
    if any(int(x) == n for x in re.findall(r"(?:^|[^A-Z])[ILR](3|4|5|6|8)(?![0-9])", c)):
        return EN_LIGNE
    if n <= 5:
        return EN_LIGNE
    if n == 6:
        return EN_LIGNE if m in SIX_EN_LIGNE else V
    return V
