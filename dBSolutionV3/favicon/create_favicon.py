from PIL import Image
from pathlib import Path

# Dossier du script
BASE_DIR = Path(__file__).resolve().parent

# Chemin réel vers l'image source
IMAGE_SOURCE = BASE_DIR.parent / "theme" / "static" / "images" / "favicon.png"

# Vérification
if not IMAGE_SOURCE.exists():
    raise FileNotFoundError(f"Image introuvable : {IMAGE_SOURCE}")

img = Image.open(IMAGE_SOURCE).convert("RGBA")
img = img.resize((256, 256), Image.LANCZOS)

# Sauvegarde du favicon.ico dans le dossier favicon/
output_path = BASE_DIR / "favicon.ico"
img.save(
    output_path,
    format="ICO",
    sizes=[(256,256)]
)

print("favicon.ico créé :", output_path)
