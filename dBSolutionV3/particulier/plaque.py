"""
Plaque d'immatriculation en SVG pour les PDF (récapitulatif, certificat de cession) : même dessin que
l'application (carscosts_app/lib/widgets/plaque.dart) et dBSolution : bande bleue UE (étoiles + code pays)
ou écusson suisse, fond, couleur du texte et bordure propres au pays, largeur fixe de 9 caractères.
"""
import math
from html import escape

BLANC, NOIR, ROUGE = "#FFFFFF", "#000000", "#C8102E"
# pays : (code sur la bande, fond, texte, bordure, étoiles UE)
STYLES = {
    "BE": ("B", BLANC, "#8B0000", "#8B0000", True), "LU": ("L", "#FFEB3B", NOIR, NOIR, True),
    "NL": ("NL", "#F7C600", NOIR, NOIR, True), "FR": ("F", BLANC, NOIR, NOIR, True),
    "DE": ("D", BLANC, NOIR, NOIR, True), "AT": ("A", BLANC, NOIR, ROUGE, True),
    "IE": ("IRL", BLANC, NOIR, NOIR, True), "IT": ("I", BLANC, NOIR, NOIR, True),
    "ES": ("E", BLANC, NOIR, NOIR, True), "PT": ("P", BLANC, NOIR, NOIR, True),
    "GR": ("GR", BLANC, NOIR, NOIR, True), "CY": ("CY", BLANC, NOIR, NOIR, True),
    "MT": ("M", BLANC, NOIR, NOIR, True), "DK": ("DK", BLANC, NOIR, ROUGE, True),
    "SE": ("S", BLANC, NOIR, NOIR, True), "FI": ("FIN", BLANC, NOIR, NOIR, True),
    "EE": ("EST", BLANC, NOIR, NOIR, True), "LV": ("LV", BLANC, NOIR, NOIR, True),
    "LT": ("LT", BLANC, NOIR, NOIR, True), "PL": ("PL", BLANC, NOIR, NOIR, True),
    "CZ": ("CZ", BLANC, NOIR, NOIR, True), "SK": ("SK", BLANC, NOIR, NOIR, True),
    "HU": ("H", BLANC, NOIR, NOIR, True), "SI": ("SLO", BLANC, NOIR, "#00843D", True),
    "HR": ("HR", BLANC, NOIR, NOIR, True), "RO": ("RO", BLANC, NOIR, NOIR, True),
    "BG": ("BG", BLANC, NOIR, NOIR, True), "GB": ("UK", BLANC, NOIR, NOIR, False),
    "NO": ("N", BLANC, NOIR, NOIR, False), "CH": ("CH", BLANC, NOIR, NOIR, False),
}
BLEU_UE, JAUNE_UE, GRIS_BANDE = "#003399", "#FFDD00", "#374151"
CARACTERES = 9


def plaque_svg(numero, pays, hauteur=34):
    numero = (numero or "").upper().strip()
    if not numero:
        return ""
    code_pays = (pays or "").upper()
    code, fond, texte, bordure, etoiles = STYLES.get(code_pays, (code_pays, BLANC, NOIR, NOIR, False))
    defaut = code_pays not in STYLES
    h = float(hauteur)
    taille = h * 0.58
    largeur_car = taille * 0.68                       # Arial gras, majuscules et chiffres
    zone = max(CARACTERES, len(numero)) * largeur_car + 2 * h * 0.2
    bande = h * 0.62 if code else 0
    l = bande + zone
    e = max(1.0, h * 0.06)
    r = h * 0.12
    parties = [f'<rect x="{e / 2:.2f}" y="{e / 2:.2f}" width="{l - e:.2f}" height="{h - e:.2f}" rx="{r:.2f}" '
               f'fill="{fond}" stroke="{bordure}" stroke-width="{e:.2f}"/>']
    if code == "CH":
        # Écusson suisse
        sx, sy, ox, oy = h * 0.45 / 32, h * 0.53 / 38, (bande - h * 0.45) / 2, (h - h * 0.53) / 2
        p = lambda x, y: f"{ox + x * sx:.2f},{oy + y * sy:.2f}"  # noqa: E731
        parties.append(f'<path d="M{p(2, 2)} L{p(30, 2)} L{p(30, 17)} C{p(30, 27)} {p(23, 33)} {p(16, 36)} '
                       f'C{p(9, 33)} {p(2, 27)} {p(2, 17)} Z" fill="#DA291C"/>')
        parties.append(f'<rect x="{ox + 13.25 * sx:.2f}" y="{oy + 8 * sy:.2f}" width="{5.5 * sx:.2f}" height="{18 * sy:.2f}" fill="#fff"/>')
        parties.append(f'<rect x="{ox + 7 * sx:.2f}" y="{oy + 14.25 * sy:.2f}" width="{18 * sx:.2f}" height="{5.5 * sy:.2f}" fill="#fff"/>')
    elif code:
        couleur = GRIS_BANDE if defaut else BLEU_UE
        parties.append(f'<path d="M{e / 2 + r:.2f},{e / 2:.2f} H{bande:.2f} V{h - e / 2:.2f} H{e / 2 + r:.2f} '
                       f'Q{e / 2:.2f},{h - e / 2:.2f} {e / 2:.2f},{h - e / 2 - r:.2f} V{e / 2 + r:.2f} '
                       f'Q{e / 2:.2f},{e / 2:.2f} {e / 2 + r:.2f},{e / 2:.2f} Z" fill="{couleur}"/>')
        cx = bande / 2
        if etoiles:
            cy, rayon = h * 0.30, h * 0.4 * 0.35
            for i in range(12):
                a = -math.pi / 2 + i * math.pi / 6
                parties.append(f'<circle cx="{cx + math.cos(a) * rayon:.2f}" cy="{cy + math.sin(a) * rayon:.2f}" '
                               f'r="{h * 0.4 * 0.065:.2f}" fill="{JAUNE_UE}"/>')
            y_code = h * 0.82
        else:
            y_code = h * 0.62
        t_code = h * 0.27 if len(code) < 3 else h * 0.22
        parties.append(f'<text x="{cx:.2f}" y="{y_code:.2f}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
                       f'font-weight="bold" font-size="{t_code:.2f}" fill="#FFFFFF">{escape(code)}</text>')
    parties.append(f'<text x="{bande + zone / 2:.2f}" y="{h / 2 + taille * 0.36:.2f}" text-anchor="middle" '
                   f'font-family="Arial, Helvetica, sans-serif" font-weight="bold" font-size="{taille:.2f}" '
                   f'letter-spacing="{h * 0.02:.2f}" fill="{texte}">{escape(numero)}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{l:.1f}" height="{h:.1f}" viewBox="0 0 {l:.2f} {h:.2f}" '
            f'style="vertical-align: middle">{"".join(parties)}</svg>')
