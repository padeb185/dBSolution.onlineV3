from PIL import Image, ImageDraw, ImageFont
import os

# Dossier de sortie
output_dir = "./"  # change si tu veux un autre dossier

# Police (essaye DejaVuSans-Bold, sinon Pillow utilisera la police par défaut)
try:
    font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 90)
except:
    font_big = ImageFont.load_default()

# Couleurs
light_blue = (96, 165, 250)  # pour Ca
dark_blue = (37, 99, 235)    # pour Co
white = (255, 255, 255)
text_blue = (30, 64, 175)    # pour rs et sts

# Taille de l'image
width, height = 1300, 350
img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# Carrés et textes
sq = 160
y = 95

# Ca carré
draw.rounded_rectangle((60, y, 60+sq, y+sq), radius=25, fill=light_blue)
draw.text((60+40, y+40), "Ca", fill=white, font=font_big)

# rs collé après Ca
draw.text((60+sq+5, y+50), "rs", fill=text_blue, font=font_big)

# Co carré collé après rs
co_x = 60+sq+5+120
draw.rounded_rectangle((co_x, y, co_x+sq, y+sq), radius=25, fill=dark_blue)
draw.text((co_x+40, y+40), "Co", fill=white, font=font_big)

# sts collé après Co (corrigé pour CarsCosts)
draw.text((co_x+sq+5, y+50), "sts", fill=text_blue, font=font_big)

# Sauvegarde PNG
png_path = os.path.join(output_dir, "carscosts_logo_correct.png")
img.save(png_path)
print(f"PNG sauvegardé : {png_path}")

# Création SVG
svg_content = f'''
<svg xmlns="http://www.w3.org/2000/svg" width="1300" height="350">
  <rect x="60" y="95" width="160" height="160" rx="25" fill="#60a5fa"/>
  <text x="95" y="195" font-size="80" font-family="Arial" fill="white">Ca</text>

  <text x="225" y="205" font-size="80" font-family="Arial" fill="#1e40af">rs</text>

  <rect x="350" y="95" width="160" height="160" rx="25" fill="#2563eb"/>
  <text x="385" y="195" font-size="80" font-family="Arial" fill="white">Co</text>

  <text x="515" y="205" font-size="80" font-family="Arial" fill="#1e40af">sts</text>
</svg>
'''

svg_path = os.path.join(output_dir, "carscosts_logo_correct.svg")
with open(svg_path, "w") as f:
    f.write(svg_content)
print(f"SVG sauvegardé : {svg_path}")