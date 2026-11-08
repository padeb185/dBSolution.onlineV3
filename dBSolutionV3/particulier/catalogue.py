"""
Catalogue des marques et modèles proposés à la saisie d'un véhicule (application des particuliers).

Fichier : particulier/donnees/marques_modeles.json
    {"version": 3, "marques": {"Peugeot": {"208": [["1.2 PureTech", 100, "essence"], …],
                                            "205": [["1.6 GTI", 105, "essence", "1984-1994"], …]}, …}}
    marque → modèle → versions [libellé, puissance en ch, énergie (codes de Vehicule.energie), période facultative]
    Modèles depuis les années 70 (période = années de production, « 2020- » si toujours produit).
Pour ajouter une marque ou un modèle : modifier ce fichier dans le projet puis ./deploy.sh
(deploy.sh synchronise le projet et remplacerait une modification faite seulement sur le serveur).
Le fichier est relu dès que sa date de modification change, sans redémarrage.
Les suggestions n'imposent rien : la saisie reste libre dans l'application.
"""
import json
import os
import unicodedata
from pathlib import Path

FICHIER = Path(__file__).resolve().parent / "donnees" / "marques_modeles.json"
_cache = {"mtime": None, "donnees": None}

# Logos des marques : ceux de dBSolution (theme/static/images/marques/), en miniatures 128 px
# dans images/marques/mini/ (nom de fichier = nom de la marque en minuscules + .png)
DOSSIER_LOGOS = "images/marques/mini"


def _nfc(texte):
    return unicodedata.normalize("NFC", texte).strip().lower()


def logos(marques):
    """{marque: chemin statique du logo} : tous les logos + marques du catalogue
    (« Simca / Talbot » : logo de Simca, sinon de Talbot)."""
    from django.contrib.staticfiles import finders
    dossier = finders.find(DOSSIER_LOGOS)
    if not dossier or not os.path.isdir(dossier):
        return {}
    fichiers = {_nfc(os.path.splitext(f)[0]): f for f in os.listdir(dossier)}
    # Tous les logos de dBSolution (marque saisie librement, hors catalogue) …
    resultat = {os.path.splitext(f)[0]: f"{DOSSIER_LOGOS}/{f}" for f in fichiers.values()}
    # … et les marques du catalogue sous leur nom exact
    for marque in marques:
        for candidat in [marque, *marque.split("/")]:
            f = fichiers.get(_nfc(candidat))
            if f:
                resultat[marque] = f"{DOSSIER_LOGOS}/{f}"
                break
    return resultat


def catalogue():
    mtime = FICHIER.stat().st_mtime
    if _cache["mtime"] != mtime:
        with open(FICHIER, encoding="utf-8") as f:
            donnees = json.load(f)
        marques = donnees.get("marques", {})
        liste_logos = logos(marques)
        _cache.update(mtime=mtime, donnees={"version": f"{donnees.get('version', 1)}-{int(mtime)}-{len(liste_logos)}",
                                             "marques": marques, "logos": liste_logos})
    return _cache["donnees"]
